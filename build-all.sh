#!/bin/bash

function cleanup() {
    echo "Stopping container..."
    docker stop "${CTID}" >/dev/null
    echo "Removing container..."
    docker rm "${CTID}" >/dev/null
}

function build() {
    CTID="$1"
    tool="$2"
    shift; shift;
    buildopts="$@"
    echo "Building $tool $buildopts"
    docker cp "${tool}/${tool}.spec" "$CTID:/root/"
    for p in "${tool}"/*.patch; do
        docker cp "$p" "${CTID}:/root/rpmbuild/SOURCES"
    done || true
    docker exec "$CTID" spectool -g -R "/root/${tool}.spec"
    docker exec "$CTID" yum-builddep -y "/root/${tool}.spec"
    docker exec "$CTID" rpmbuild -bb "/root/${tool}.spec" $buildopts
    docker exec "$CTID" rm -rf /root/rpmbuild/BUILD
    docker exec "$CTID" mkdir /root/rpmbuild/BUILD
}

if docker -v |grep -q podman; then
  echo "using podman, test likely wont work"
  PODMAN=1
fi

TAG=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --image-tag)
            TAG=$2
            shift
            ;;
        *)
            echo "Unkown option: $1"
            ;;
    esac
    shift
done

if [ -z $TAG ]; then
    echo "No tag specified, using quay.io/fbs/el7-bpf-specs:llvm_12_latest"
    TAG="quay.io/fbs/el7-bpf-specs:llvm_12_latest"
fi

echo "Using $TAG as base"
CTID=$(docker create -t "$TAG")
if [ $? -ne 0 ]; then
    >&2 echo "Failed to spawn docker CT"
    exit 1
fi

set -e

docker start "$CTID"
docker exec -i "$CTID" yum install -y gcc
build "${CTID}" "bpftool"
build "${CTID}" "bcc"

docker exec -i "${CTID}" find /root/rpmbuild/RPMS/ -name '*bcc*.rpm' -exec yum install -y {} +
build "${CTID}" "bpftrace"

docker cp "${CTID}:/root/rpmbuild/RPMS" .
cleanup
echo "##############################################"
echo "Finished:"
echo "Builder Image: ${TAG}"
echo "RPMs can be found in: $(readlink -f RPMS)"

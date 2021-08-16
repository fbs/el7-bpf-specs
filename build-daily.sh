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
    local buildopts="$@"
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

if ! SHA=$(curl -s https://api.github.com/repos/iovisor/bpftrace/commits/master | jq -r '.sha' | cut -c 1-7); then
  echo "Could not determine latest commit hash"
  exit 1
else
  echo "Using commit hash: $SHA"
  pkg_date=$(date '+%Y%m%d')
  echo "Using date tag: $pkg_date"
  sed -i "1i%global commitid $SHA" bpftrace/bpftrace.spec
  sed -i "2i%global date_tag $pkg_date" bpftrace/bpftrace.spec
fi

docker exec "$CTID" \
  curl -so /etc/yum.repos.d/bpftools.repo http://repos.baslab.org/rhel/7/bpftools/bpftools.repo

docker exec "$CTID" yum install -y epel-release
docker exec "$CTID" yum install -y bcc-static bcc-devel

build "${CTID}" "bpftrace"

docker cp "${CTID}:/root/rpmbuild/RPMS" .
cleanup
find "RPMS" -name "*ebpftoolsbuilder*" -delete

echo "##############################################"
echo "Finished:"
echo "RPMs can be found in: $(readlink -f RPMS)"

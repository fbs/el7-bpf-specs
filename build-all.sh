#!/bin/bash

if [ $EUID -ne 0 ]; then
    >&2 echo "requires root"
    exit 1
fi

TAG=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --builder-tag)
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
    echo "No tag specified, building the builder container"
    TAG="ebpftools-llvm-clang:$(date +%y%m%d_%s)"
    docker build . -f llvm-clang-builder.Dockerfile -t $TAG
    echo "Builder tag: $TAG"
fi

function cleanup() {
    docker cp "${CTID}:/root/rpmbuild/RPMS" .
    docker stop "${CTID}"
    docker rm "${CTID}"
}

function build() {
    CTID="$1"
    tool="$2"
    echo "Building $tool"
    docker cp "${tool}/${tool}.spec" "$CTID:/root/"
    for p in "${tool}/*.patch"; do
        docker cp "$p" "${CTID}:/root/rpmbuild/SOURCES"
    done || true
    docker exec "$CTID" spectool -g -R "/root/${tool}.spec"
    docker exec "$CTID" yum-builddep -y "/root/${tool}.spec"
    docker exec "$CTID" rpmbuild -bb "/root/${tool}.spec"
}

echo "Using $TAG as base"
CTID=$(docker create -t "$TAG")
if [ $? -ne 0 ]; then
    >&2 echo "Failed to spawn docker CT"
    exit 1
fi

docker start "$CTID"
docker exec "$CTID" yum install -y gcc
build "${CTID}" "bpftool"
build "${CTID}" "bcc"
build "${CTID}" "bpftrace"
cleanup

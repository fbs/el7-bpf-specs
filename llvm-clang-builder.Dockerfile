FROM centos:7

# Build the builder container

COPY llvm-clang/llvm-clang.spec /

# Dependencies
RUN yum install -y rpmdevtools rpm-build centos-release-scl epel-release \
    && sed '/sclo-source/,$d' /etc/yum.repos.d/CentOS-SCLo-* \
    && yum-builddep -y llvm-clang.spec \
    && (rpmbuild --nobuild llvm-clang.spec  || true) \
    && spectool -g -R llvm-clang.spec \
    && rpmbuild -bb llvm-clang.spec \
    && rm -rf /root/rpmbuild/BUILD \
    && (find /root/rpmbuild/RPMS/ -type f -name '*.rpm'| xargs yum install -y) \
    && rm -rf /var/cache/yum

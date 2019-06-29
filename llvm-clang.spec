%global maj_ver 8
%global min_ver 0
%global patch_ver 0
%define _unpackaged_files_terminate_build 0

Name:     ebpftoolsbuilder-llvm-clang
Version:	%{maj_ver}.%{min_ver}.%{patch_ver}
Release:  0%{?dist}
Summary:	The Low Level Virtual Machine
License:	NCSA
URL:		  http://llvm.org
Source0:	http://llvm.org/releases/%{version}/llvm-%{version}.src.tar.xz
Source1:	http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.xz

ExclusiveArch:  x86_64

BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
BuildRequires:  bison
BuildRequires:  cmake3
BuildRequires:  flex
BuildRequires:  make
BuildRequires:  libxml2-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  devtoolset-7-toolchain

%description
A build of LLVM and Clang to make bpftrace and BCC possible on
RH7. Don't use this as your daily compiler!

%package libs
Summary: Libs required for running the dynamically linked version of bpftrace

%description libs
Libs required for running the dynamically linked version of bpftrace

%prep

%setup -n llvm-8.0.0.src -q
%setup -T -D -a 1 -n llvm-8.0.0.src -q
mv cfe-8.0.0.src tools/clang
mkdir build

%build

. /opt/rh/devtoolset-7/enable
cd build

cmake3 .. \
  -DBUILD_SHARED_LIBS=OFF \
  -DLLVM_BUILD_LLVM_DYLIB=ON \
  -DLLVM_LINK_LLVM_DYLIB=OFF \
  -DLIBCLANG_BUILD_STATIC=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=/usr \
	-DLLVM_LIBDIR_SUFFIX=64 \
  -DCLANG_BUILD_EXAMPLES=OFF \
  -DCLANG_INCLUDE_DOCS=OFF \
  -DCLANG_INCLUDE_TESTS=OFF \
  -DLLVM_APPEND_VC_REV=OFF \
  -DLLVM_BUILD_DOCS=OFF \
  -DLLVM_BUILD_EXAMPLES=OFF \
  -DLLVM_BUILD_TESTS=OFF \
  -DLLVM_BUILD_TOOLS=ON \
  -DLLVM_ENABLE_ASSERTIONS=OFF \
  -DLLVM_ENABLE_CXX1Y=ON \
  -DLLVM_ENABLE_EH=ON \
  -DLLVM_ENABLE_LIBCXX=OFF \
  -DLLVM_ENABLE_PIC=ON \
  -DLLVM_ENABLE_RTTI=ON \
  -DLLVM_ENABLE_SPHINX=OFF \
  -DLLVM_ENABLE_TERMINFO=OFF \
  -DLLVM_INCLUDE_DOCS=OFF \
  -DLLVM_INCLUDE_EXAMPLES=OFF \
  -DLLVM_INCLUDE_GO_TESTS=OFF \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_INCLUDE_TOOLS=ON \
  -DLLVM_INCLUDE_UTILS=OFF \
  -DLLVM_PARALLEL_LINK_JOBS=1 \
  -DLLVM_TARGETS_TO_BUILD="host;BPF"

%make_build

%install

cd build
%make_install

# Need libclang for static linking
find . -name 'libclang.a' -exec cp {} %{buildroot}%{_libdir} \;
# Links to libclang.so for some reason which makes libclang.so a
# package dependency
rm %{buildroot}%{_bindir}/c-index-test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/*.a
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_includedir}/clang
%{_includedir}/clang-c
%{_libdir}/clang/%{version}
%{_libdir}/cmake/
%{_libdir}/lib*.so
%{_libdir}/lib*.so.%{maj_ver}

%files libs
%{_libdir}/libLLVM*.so
%{_libdir}/libclang.so*

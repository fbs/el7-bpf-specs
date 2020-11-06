%global pkgname bpftrace
%global commitid 487dd81

# The static build is a bit of a hack and
# doesn't build th docs and tools package
# so ignore other files
%global _unpackaged_files_terminate_build 0
# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post %{nil}
%global _find_debuginfo_opts -g

Name:           %{pkgname}
Version:        0.11.0
%if "%{?commitid}" != ""
Release:        5.%{?commitid}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0

URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/v%{version}.tar.gz
Patch0:         0001-build-EL7-support.patch
Patch1:         0001-tools-ext4dist-based-on-xfsdist.patch
Patch2:         0001-tools-Patch-for-RHEL7.patch

Patch100:       0001-build-Force-disable-optimization.patch
Patch101:       0001-Do-not-require-libbpf-for-static-build.patch
Patch102:       0001-Don-t-require-libbpf-for-build.patch


ExclusiveArch:  x86_64

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake3
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  devtoolset-8-gcc-c++
BuildRequires:  ebpftoolsbuilder-llvm-clang-libs
BuildRequires:  binutils-devel

# For static:
BuildRequires:  bcc-devel
BuildRequires:  bcc-static
BuildRequires:  glibc-static
BuildRequires:  zlib-static
BuildRequires:  ncurses-static
BuildRequires:  elfutils-libelf-devel-static
BuildRequires:  ebpftoolsbuilder-llvm-clang

Requires:       kernel-devel
Requires:       binutils

obsoletes:      bpftrace-static

%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap

%package tools
Summary:        Command line tools for BPFtrace
BuildArch:      noarch

%description tools
Command line tools for BPFtrace

%package doc
Summary:        BPFtrace documentation
BuildArch:      noarch

%description doc
BPFtrace documentation

%prep

%if "%{?commitid}" != ""
rm -rf bpftrace
git clone %{url} bpftrace
cd bpftrace
git checkout %{commitid}

%setup -n bpftrace -D -T

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%else
%autosetup -p1 -n bpftrace-%{version}
%endif

%build
. /opt/rh/devtoolset-8/enable
%cmake3 . \
  -DCMAKE_BUILD_TYPE=Debug \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DSTATIC_LIBC=ON \
  -DSTATIC_LINKING=1

%make_build
./tests/bpftrace_test --gtest_filter='*:-procmon.*'

%install
%make_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{pkgname}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{pkgname}\([0-9.]\+\)\?$=#!%{_bindir}/%{pkgname}=' {} \;

%files
%license LICENSE
%{_bindir}/%{pkgname}

%exclude %{_datadir}

%files doc
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md

%files tools
%dir %{_datadir}/%{pkgname}
%dir %{_datadir}/%{pkgname}/tools
%dir %{_datadir}/%{pkgname}/tools/doc
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{pkgname}/tools/*.bt
%{_datadir}/%{pkgname}/tools/doc/*.txt

%changelog
* Fri Nov 6 2020 bas smit - 0.11.0-5
- bpftrace 0.11 487dd81 with bcc compatiblity fix

* Tue Nov 3 2020 bas smit - 0.11.0-4
- bpftrace 0.11

* Fri Sep 11 2020 bas smit - 0.11.0-3
- bpftrace 0.11 91b0705

* Fri Aug 21 2020 bas smit - 0.11.0-2
- bpftrace 0.11 2476917

* Thu Jul 16 2020 bas smit - 0.11.0-1
- bpftrace 0.11!

* Thu Jun 25 2020 bas smit - 0.10.0-2
- Builds are now static by default

* Tue Apr 14 2020 bas smit - 0.10.0-1
- 0.10.0 release

* Tue Mar 3 2020 bas smit - 0.9.4-2
- Build with devtoolset-8

* Tue Feb 18 2020 bas smit - 0.9.4-1
- 0.9.4 release!

* Fri Nov 22 2019 bas smit - 0.9.3
- 0.9.3 release!

* Thu Nov 7 2019 bas smit - 0.9.2
- Update to latest release

* Sun Jun 30 2019 bas smit - 0.9.1
- Adept for centos 7

* Thu Apr 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-3
- Rebuilt for bcc 0.9.0

* Mon Apr 22 2019 Neal Gompa <ngompa@datto.com> - 0.9-2
- Fix Source0 reference
- Use make_build macro for calling make

* Mon Apr  1 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.9-1
- Build on aarch64 and s390x

* Mon Mar 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-0
- Updated to version 0.9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-2.20181210gitc49b333
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181210gitc49b333
- Updated to latest upstream (c49b333c034a6d29a7ce90f565e27da1061af971)

* Wed Nov 07 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181107git029717b
- Initial import

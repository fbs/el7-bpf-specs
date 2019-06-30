%bcond_with static

%global pkgname bpftrace

Name:           %{pkgname}%{?with_static:-static}
Version:        0.9.1
Release:        0%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        ASL 2.0

URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/v%{version}.tar.gz
Patch0:         001-bpftrace-build.patch

ExclusiveArch:  x86_64

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake3
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  devtoolset-7-gcc-c++
BuildRequires:  bcc-devel
%if %{with static}
BuildRequires:  bcc-static
BuildRequires:  glibc-static
BuildRequires:  ncurses-static
BuildRequires:  elfutils-libelf-devel-static
%else
BuildRequires:  ebpftoolsbuilder-llvm-clang-libs
%endif

Requires:       kernel-devel

Conflicts: bpftrace%{!?with_static:-static}

%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap


%prep
%autosetup -p1 -n bpftrace-%{version}

%build
. /opt/rh/devtoolset-7/enable
%cmake3 . \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_VERBOSE_MAKEFILE=0 \
        -DBUILD_TESTING:BOOL=OFF \
        -DBUILD_SHARED_LIBS:BOOL=OFF \
%if %{with static}
        -DSTATIC_LINKING=1
%endif

%make_build

%install
%make_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{pkgname}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{pkgname}\([0-9.]\+\)\?$=#!%{_bindir}/%{pkgname}=' {} \;

# Move man pages to the right location
mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_prefix}/man/* %{buildroot}%{_mandir}/


%files
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
%dir %{_datadir}/%{pkgname}
%dir %{_datadir}/%{pkgname}/tools
%dir %{_datadir}/%{pkgname}/tools/doc
%{_bindir}/%{pkgname}
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{pkgname}/tools/*.bt
%{_datadir}/%{pkgname}/tools/doc/*.txt


%changelog
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

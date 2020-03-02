%bcond_with static
%bcond_with git

%global pkgname bpftrace

%define commitid f156a0f

%if %{with static}
# The static build is a bit of a hack and
# doesn't build th docs and tools package
# so ignore other files
%global _unpackaged_files_terminate_build 0
# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post %{nil}
%global _find_debuginfo_opts -g
%endif

Name:           %{pkgname}%{?with_static:-static}
Version:        0.9.4
%if %{with git}
Release:        1.%{commitid}%{?dist}
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

%if %{with static}
Patch100:       0001-build-Force-disable-optimization.patch
Patch101:       0001-Add-lib-iberty-dependency-for-static-builds.patch
%endif

%if ! %{with git}
Patch999:       0001-ast-add-missing-parameter-name.patch
%endif

ExclusiveArch:  x86_64


BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake3
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  devtoolset-7-gcc-c++
BuildRequires:  ebpftoolsbuilder-llvm-clang-libs

# For static:
BuildRequires:  bcc-devel
BuildRequires:  bcc-static
BuildRequires:  glibc-static
BuildRequires:  zlib-static
BuildRequires:  ncurses-static
BuildRequires:  elfutils-libelf-devel-static
BuildRequires:  ebpftoolsbuilder-llvm-clang
BuildRequires:  binutils-devel

Requires:       kernel-devel
Requires:       binutils

Conflicts: bpftrace%{!?with_static:-static}

%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap

%if !%{with static}
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

%endif

%prep

%if %{with git}
rm -rf bpftrace
git clone %{url} bpftrace
cd bpftrace
git checkout %{commitid}

%setup -n bpftrace -D -T

%patch0 -p1
%patch1 -p1
%patch2 -p1
%if %{with static}
%patch100 -p1
%patch101 -p1
%endif
%else
%autosetup -p1 -n bpftrace-%{version}
%endif

%build
. /opt/rh/devtoolset-7/enable
%cmake3 . \
  -DCMAKE_BUILD_TYPE=Debug \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
%if %{with static}
  -DSTATIC_LIBC=ON \
  -DSTATIC_LINKING=1
%endif

%make_build
./tests/bpftrace_test

%install
%make_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{pkgname}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{pkgname}\([0-9.]\+\)\?$=#!%{_bindir}/%{pkgname}=' {} \;

%if ! %{with git}
# Move man pages to the right location
mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_prefix}/man/* %{buildroot}%{_mandir}/
%endif


%files
%license LICENSE
%{_bindir}/%{pkgname}

%if !%{with static}
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
%endif


%changelog
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

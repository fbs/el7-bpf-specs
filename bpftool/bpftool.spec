Name: bpftool
Version: 5.5.7
Release: 1%{?dist}
Summary: Inspection and simple manipulation of eBPF programs and maps
License: GPLv2
URL: http://www.kernel.org/
Source0: https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz

BuildRequires: elfutils-libelf-devel
BuildRequires: zlib
BuildRequires: gcc
BuildRequires: make
BuildRequires: glibc-devel
BuildRequires: python-docutils
BuildRequires: binutils-devel

%description
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%prep

%autosetup -p1 -n linux-%{version}

%build

sed -i '1s/python3/python/' scripts/bpf_helpers_doc.py
cd tools/bpf/bpftool/
sed -i '/#include <linux\/if.h>/d' net.c
make
make doc

%install

cd tools/bpf/bpftool/
%make_install prefix=/usr  doc-install

mv %{buildroot}/usr/man %{buildroot}%{_mandir}

%files

%{_sbindir}/bpftool
%exclude %{_datadir}/bash-completion/completions/bpftool
%{_mandir}

%changelog
* Mon Mar 2 2020 bas smit - 5.5.7-1
Bump version, disable static

* Mon Jul 1 2019 bas smit - 0.0.1
- Initial version

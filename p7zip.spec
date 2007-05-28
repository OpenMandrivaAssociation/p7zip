%define	name	p7zip
%define	version	4.47
%define	release	%mkrel 1

Summary:	7-zip compatible compression program
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
License:	LGPL
Group:		Archiving/Compression
Url:		http://p7zip.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with
highest compression ratio. Original version can be found at
http://www.7zip.org.

%prep
%setup -q -n %{name}_%{version}
%ifarch x86_64
cp makefile.linux_amd64 makefile.machine
%endif
%ifarch %ix86 alpha ppc
cp makefile.linux_x86_ppc_alpha makefile.machine
%endif
perl -pi -e "s/-O2/%optflags/" makefile.glb
find DOCS -type d|xargs chmod 755
find README ChangeLog TODO DOCS -type f|xargs chmod 644
%build
%make

%install
rm -rf $RPM_BUILD_ROOT
install -m755 bin/7za -D $RPM_BUILD_ROOT%{_bindir}/7za

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog TODO DOCS/*
%{_bindir}/7za



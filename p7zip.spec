%define	name	p7zip
%define	version	4.58
%define	release	%mkrel 2

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
highest compression ratio.

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
#all3

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall DEST_HOME=%buildroot%_prefix DEST_MAN=%buildroot%_mandir DEST_SHARE=%buildroot%_libdir/%name
chmod -R +w %buildroot
rm -f %buildroot%_libdir/p7zip/Codecs/Rar29.so


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog TODO DOCS/*
%{_bindir}/7za
#%_libdir/p7zip
%_mandir/man1/*


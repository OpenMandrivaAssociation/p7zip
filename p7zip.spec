Summary:	7-zip compatible compression program
Name:		p7zip
Version:	9.20.1
Release:	3
License:	LGPLv2+
Group:		Archiving/Compression
Url:		http://p7zip.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
%ifarch %ix86
BuildRequires:	nasm
%endif
%ifarch x86_64
BuildRequires:	yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with
highest compression ratio.

%prep
%setup -qn %{name}_%{version}
%apply_patches
%ifarch x86_64
cp makefile.linux_amd64_asm makefile.machine
%endif
%ifarch %ix86
cp makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch alpha ppc
cp makefile.linux_x86_ppc_alpha_gcc_4.X makefile.machine
%endif
#gw really use our flags:
perl -pi -e "s/-s /%optflags /" makefile.machine
find DOCS -type d|xargs chmod 755
find README ChangeLog TODO DOCS -type f|xargs chmod 644
%build
%make all3

%install
%makeinstall DEST_HOME=%{buildroot}%{_prefix} DEST_MAN=%{buildroot}%{_mandir} DEST_SHARE=%{buildroot}%{_libdir}/%{name}
chmod -R +w %{buildroot}
#gw don't package this, it is non-free like unrar
rm -f %{buildroot}%{_libdir}/p7zip/Codecs/Rar29.so DOCS/unRarLicense.txt
#gw fix paths in wrapper scripts and man pages
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_bindir}/* %{buildroot}%{_mandir}/man1/*

%files
%doc README ChangeLog TODO DOCS/*
%{_bindir}/7za
%{_bindir}/7zr
%{_bindir}/7z
%{_libdir}/p7zip
%{_mandir}/man1/*


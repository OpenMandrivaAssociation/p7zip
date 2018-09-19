Summary:	7-zip compatible compression program
Name:		p7zip
Version:	16.02
Release:	2
License:	LGPLv2+
Group:		Archiving/Compression
Url:		http://p7zip.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
%ifarch %{ix86}
BuildRequires:	nasm
%endif
%ifarch %{x86_64}
BuildRequires:	yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with
highest compression ratio.

%prep
%setup -qn %{name}_%{version}
%apply_patches

%ifarch %{x86_64}
cp makefile.linux_amd64_asm makefile.machine
%else
%ifarch %{ix86}
cp makefile.linux_x86_asm_gcc_4.X makefile.machine
%else
cp makefile.linux_any_cpu makefile.machine
%endif
%endif

#gw really use our flags:
sed -i -e "s/^OPTFLAGS=.*/OPTFLAGS=%{optflags}/" makefile.machine
sed -i -e "s/^LINK_SHARED=/LINK_SHARED=%{optflags} /" makefile.machine
# And our compiler
sed -i -e "s|^CC=.*|CC=%{__cc}|" makefile.machine
sed -i -e "s|^CXX=.*|CXX=%{__cxx} -Wno-error=c++11-narrowing|" makefile.machine

find DOC -type d|xargs chmod 755
find README ChangeLog TODO DOC -type f|xargs chmod 644

%build
%make_build all3

%install
%make_install DEST_HOME=%{buildroot}%{_prefix} DEST_MAN=%{buildroot}%{_mandir} DEST_SHARE=%{buildroot}%{_libdir}/%{name}

chmod -R +w %{buildroot}
#gw don't package this, it is non-free like unrar
rm -f %{buildroot}%{_libdir}/p7zip/Codecs/Rar29.so DOC/unRarLicense.txt
#gw fix paths in wrapper scripts and man pages
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_bindir}/* %{buildroot}%{_mandir}/man1/*
#find . -perm 0640 | xargs chmod 0644

%files
%doc README ChangeLog TODO DOC/*
%{_bindir}/7za
%{_bindir}/7zr
%{_bindir}/7z
%{_libdir}/p7zip
%{_mandir}/man1/*


%global optflags %{optflags} -O3 -fuse-ld=bfd
%global ldflags %{ldflags} -fuse-ld=bfd

# (tpg) enable PGO build
%bcond_without pgo

Summary:	7-zip compatible compression program
Name:		p7zip
Version:	16.02
Release:	4
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
%autosetup -n %{name}_%{version} -p1

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
%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
sed -i -e "s/^OPTFLAGS=.*/OPTFLAGS=%{optflags} -fprofile-instr-generate/" makefile.machine
sed -i -e "s/^LINK_SHARED=.*/LINK_SHARED=%{optflags} -fprofile-instr-generate/" makefile.machine
%make_build all3
make test

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

sed -i -e "s/^OPTFLAGS=.*/OPTFLAGS=%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)/" makefile.machine
sed -i -e "s/^LINK_SHARED=.*/LINK_SHARED=%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)/" makefile.machine
CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%make_build all3

%install
%make_install DEST_HOME=%{buildroot}%{_prefix} DEST_MAN=%{buildroot}%{_mandir} DEST_SHARE=%{buildroot}%{_libdir}/%{name}

chmod -R +w %{buildroot}
#gw don't package this, it is non-free like unrar
rm -f %{buildroot}%{_libdir}/p7zip/Codecs/Rar29.so DOC/unRarLicense.txt
#gw fix paths in wrapper scripts and man pages
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_bindir}/* %{buildroot}%{_mandir}/man1/*
#find . -perm 0640 | xargs chmod 0644

rm -rf %{buildroot}%{_docdir}/%{name}

%files
%doc README ChangeLog TODO
%{_bindir}/7za
%{_bindir}/7zr
%{_bindir}/7z
%{_libdir}/p7zip
%{_mandir}/man1/*

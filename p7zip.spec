# (tpg) 2019-07-09
# BUILDSTDERR: /usr/bin/ld.bfd: /usr/bin/../lib64/gcc/x86_64-openmandriva-linux-gnu/9.1.1/../../../../lib64/crt1.o: in function `_start':
# BUILDSTDERR: /builddir/build/BUILD/glibc-2.29/csu/../sysdeps/x86_64/start.S:110: undefined reference to `main'
%define _disable_ld_no_undefined 1

# (tpg) enable PGO build
%bcond_with pgo

Summary:	7-zip compatible compression program
Name:		p7zip
Version:	17.04
Release:	1
License:	LGPLv2+
Group:		Archiving/Compression
Url:		http://p7zip.sourceforge.net/
Source0:	https://github.com/jinfeihan57/p7zip/archive/v%{version}/%{name}-%{version}.tar.gz
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
%autosetup -n %{name}-%{version} -p1

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
export LD_LIBRARY_PATH="$(pwd)"
sed -i -e "s/^OPTFLAGS=.*/OPTFLAGS=%{optflags} -fprofile-generate/" makefile.machine
sed -i -e "s/^LINK_SHARED=.*/LINK_SHARED=%{optflags} -fprofile-generate/" makefile.machine
%make_build all3
make test

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f *.profraw

make clean

sed -i -e "s/^OPTFLAGS=.*/OPTFLAGS=%{optflags} -fprofile-use=$PROFDATA/" makefile.machine
sed -i -e "s/^LINK_SHARED=.*/LINK_SHARED=%{optflags} -fprofile-use=$PROFDATA/" makefile.machine
CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
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
%doc %{_mandir}/man1/*

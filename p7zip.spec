%define	name	p7zip
%define	version	9.20.1
%define	release	%mkrel 2

Summary:	7-zip compatible compression program
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/p7zip/%{name}_%{version}_src_all.tar.bz2
License:	LGPLv2+
Group:		Archiving/Compression
Url:		http://p7zip.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%ifarch %ix86
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with
highest compression ratio.

%prep
%setup -q -n %{name}_%{version}
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
rm -rf $RPM_BUILD_ROOT
%makeinstall DEST_HOME=%buildroot%_prefix DEST_MAN=%buildroot%_mandir DEST_SHARE=%buildroot%_libdir/%name
chmod -R +w %buildroot
#gw don't package this, it is non-free like unrar
rm -f %buildroot%_libdir/p7zip/Codecs/Rar29.so DOCS/unRarLicense.txt
#gw fix paths in wrapper scripts and man pages
perl -pi -e "s^%buildroot^^" %buildroot%_bindir/* %buildroot%_mandir/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog TODO DOCS/*
%{_bindir}/7za
%{_bindir}/7zr
%{_bindir}/7z
%_libdir/p7zip
%_mandir/man1/*



%changelog
* Fri Mar 30 2012 Götz Waschk <waschk@mandriva.org> 9.20.1-2mdv2012.0
+ Revision: 788314
- yearly rebuild

* Sun Mar 27 2011 Götz Waschk <waschk@mandriva.org> 9.20.1-1
+ Revision: 648618
- new version
- drop patch

* Sun Aug 15 2010 Götz Waschk <waschk@mandriva.org> 9.13-2mdv2011.0
+ Revision: 570239
- fix paths in man pages (bug #60660)

* Sat Aug 07 2010 Götz Waschk <waschk@mandriva.org> 9.13-1mdv2011.0
+ Revision: 567347
- new version
- update patch 0

* Sun Feb 14 2010 Götz Waschk <waschk@mandriva.org> 9.04-3mdv2010.1
+ Revision: 505879
- update build deps
- use the right makefiles
- really use our optimization flags
- fix format strings

* Sun Jun 07 2009 Götz Waschk <waschk@mandriva.org> 9.04-1mdv2010.0
+ Revision: 383769
- update to new version 9.04

* Sat Feb 14 2009 Götz Waschk <waschk@mandriva.org> 4.65-1mdv2009.1
+ Revision: 340325
- update to new version 4.65

* Sun Nov 30 2008 Götz Waschk <waschk@mandriva.org> 4.61-1mdv2009.1
+ Revision: 308588
- update to new version 4.61

* Thu Sep 04 2008 Götz Waschk <waschk@mandriva.org> 4.58-4mdv2009.0
+ Revision: 280737
- fix wrapper scripts
- remove unrar readme
- update license
- add 7z and 7zr (bug #43503)
- add man pages

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 4.58-2mdv2009.0
+ Revision: 268355
- rebuild early 2009.0 package (before pixel changes)

* Sun Jun 08 2008 Götz Waschk <waschk@mandriva.org> 4.58-1mdv2009.0
+ Revision: 216942
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill zip URL from description

* Sun Dec 16 2007 Funda Wang <fwang@mandriva.org> 4.57-1mdv2008.1
+ Revision: 120503
- update to new version 4.57

* Tue Oct 09 2007 Götz Waschk <waschk@mandriva.org> 4.55-1mdv2008.1
+ Revision: 96137
- new version

* Sat Sep 01 2007 Götz Waschk <waschk@mandriva.org> 4.53-1mdv2008.0
+ Revision: 77366
- new version

* Thu Jul 26 2007 Götz Waschk <waschk@mandriva.org> 4.51-1mdv2008.0
+ Revision: 56052
- new version

* Sun Jul 15 2007 Götz Waschk <waschk@mandriva.org> 4.49-1mdv2008.0
+ Revision: 52333
- new version

* Sun Jul 01 2007 Götz Waschk <waschk@mandriva.org> 4.48-1mdv2008.0
+ Revision: 46790
- new version

* Mon May 28 2007 Götz Waschk <waschk@mandriva.org> 4.47-1mdv2008.0
+ Revision: 32085
- new version

* Sun Apr 22 2007 Götz Waschk <waschk@mandriva.org> 4.45-1mdv2008.0
+ Revision: 16899
- new version


* Sat Jan 27 2007 Götz Waschk <waschk@mandriva.org> 4.44-1mdv2007.0
+ Revision: 114279
- new version

* Wed Jan 24 2007 Götz Waschk <waschk@mandriva.org> 4.43-2mdv2007.1
+ Revision: 112820
- rebuild
- Import p7zip

* Sun Sep 24 2006 Götz Waschk <waschk@mandriva.org> 4.43-1mdv2007.0
- New version 4.43

* Mon May 29 2006 Götz Waschk <waschk@mandriva.org> 4.42-1mdk
- New release 4.42

* Sun Apr 16 2006 Götz Waschk <waschk@mandriva.org> 4.39-1mdk
- New release 4.39

* Mon Apr 03 2006 Jerome Soyer <saispo@mandriva.org> 4.37-1mdk
- New release 4.37

* Mon Feb 13 2006 Götz Waschk <waschk@mandriva.org> 4.33-1mdk
- New release 4.33

* Tue Jan 17 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.30-2mdk
- build on all archs
- %%mkrel

* Sat Nov 26 2005 Götz Waschk <waschk@mandriva.org> 4.30-1mdk
- New release 4.30

* Sat Oct 08 2005 Götz Waschk <waschk@mandriva.org> 4.29-1mdk
- new version

* Fri Sep 23 2005 Götz Waschk <waschk@mandriva.org> 4.27-1mdk
- New release 4.27

* Sun Jun 05 2005 Götz Waschk <waschk@mandriva.org> 4.20-1mdk
- New release 4.20

* Sat May 14 2005 Götz Waschk <waschk@mandriva.org> 4.18-1mdk
- New release 4.18

* Sat Apr 09 2005 Götz Waschk <waschk@linux-mandrake.com> 4.16-1mdk
- fix build
- New release 4.16

* Wed Mar 16 2005 Götz Waschk <waschk@linux-mandrake.com> 4.14.01-2mdk
- add docs

* Mon Jan 24 2005 Goetz Waschk <waschk@linux-mandrake.com> 4.14.01-1mdk
- New release 4.14.01

* Sat Jan 15 2005 waschk@linux-mandrake.com 4.14-1mdk
- New release 4.14

* Fri Dec 17 2004 Goetz Waschk <waschk@linux-mandrake.com> 4.13-1mdk
- New release 4.13

* Fri Nov 19 2004 Götz Waschk <waschk@linux-mandrake.com> 4.12-1mdk
- fix build
- drop patch
- New release 4.12

* Tue Oct 26 2004 Götz Waschk <waschk@linux-mandrake.com> 4.10-2mdk
- don't link statically

* Sun Oct 24 2004 Götz Waschk <waschk@linux-mandrake.com> 4.10-1mdk
- remove 7z and keep 7za
- fix source URL
- New release 4.10

* Fri Sep 17 2004 Götz Waschk <waschk@linux-mandrake.com> 0.91-1mdk
- initial package


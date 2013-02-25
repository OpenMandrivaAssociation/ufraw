%bcond_with	cinepaint

%if %{with cinepaint}
%define cinepaint_dir %(pkg-config --variable=programplugindir cinepaint-gtk)
%endif

Name:		ufraw
Version:	0.18
Release:	5
Summary:	Graphical tool to convert raw images of digital cameras
Group:		Graphics
URL:		http://ufraw.sourceforge.net/
Source0:	http://downloads.sourceforge.net/sourceforge/ufraw/%{name}-%{version}.tar.gz
License:	GPLv2+
BuildRequires:	gimp-devel >= 2.0
BuildRequires:	gtk+2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRequires:	lcms-devel
BuildRequires:	imagemagick
BuildRequires:	libexiv-devel
BuildRequires:	bzip2-devel
BuildRequires:	cfitsio-devel
BuildRequires:	libgomp-devel
BuildRequires:	lensfun-devel
%if %{with cinepaint}
BuildRequires:	cinepaint-devel
%endif
BuildRequires:	pkgconfig(gtkimageview)

%description
UFRaw is a utility to read and manipulate raw images from digital cameras.
It can be used by itself or as a Gimp plug-in.
It reads raw images using Dave Coffin's raw conversion utility DCRaw.
And it supports basic color management using Little CMS, allowing
the user to apply color profiles.

Raw images are the data directly read from the CCD of the camera,
without in-camera processing, without lossy JPEG compression, and in
36 or 48 bits color depth (TIFF has 24 bits). Problem of the raw
images is that they are in proprietary, camera-specific formats as
they are exactly what the CCD has captured, and the CCDs on differnt
cameras are very different. It also contains info about the camera
settings.

%package	gimp
Summary:	Reads the raw image formats of digital cameras into GIMP
Group:		Graphics
Requires:	gimp
Conflicts:	dcraw-gimp2.0 rawphoto
 
%description	gimp
A GIMP plug-in which reads and processes raw images from most digital
cameras. The conversion is done by the dcraw software and so all
cameras supported by dcraw are also supported by this plug-in.

In contrary to the original GIMP plug-in of dcraw this one is much
more comfortable, especially because of the life preview image but
also due to more options.

%if %{with cinepaint}
%package	cinepaint
Summary:	Reads the raw image formats of digital cameras into Cinepaint
Group:		Graphics
Requires:	cinepaint
 
%description	cinepaint
A Cinepaint plug-in which reads and processes raw images from most digital
cameras. The conversion is done by the dcraw software and so all
cameras supported by dcraw are also supported by this plug-in.
%endif

%prep
%setup -q

%build
export CPPFLAGS="-I/usr/include/lensfun"
%configure2_5x --enable-mime
%make

%install
%makeinstall_std schemasdir=%{_sysconfdir}/gconf/schemas
%find_lang ufraw

install -d %{buildroot}%{_datadir}/icons/{large,mini}

convert icons/ufraw.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert icons/ufraw.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
cp icons/ufraw.png %{buildroot}%{_liconsdir}/%{name}.png

%define schemas ufraw

%files -f %{name}.lang
%doc README
%{_sysconfdir}/gconf/schemas/ufraw.schemas
%{_bindir}/*
%{_datadir}/applications/ufraw.desktop
%{_datadir}/pixmaps/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_mandir}/man1/*

%files gimp
%{_libdir}/gimp/2.0/plug-ins/*

%if %{with cinepaint}
%files cinepaint
%{cinepaint_dir}/plug-ins/*
%endif


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.18-2mdv2011.0
+ Revision: 670739
- mass rebuild

* Tue Feb 22 2011 Götz Waschk <waschk@mandriva.org> 0.18-1
+ Revision: 639280
- update to new version 0.18

* Wed Dec 01 2010 Funda Wang <fwang@mandriva.org> 0.17-4mdv2011.0
+ Revision: 604409
- rebuild for new exiv2

* Sat Aug 21 2010 Funda Wang <fwang@mandriva.org> 0.17-3mdv2011.0
+ Revision: 571620
- rebuild for new cfitsio

* Tue Aug 03 2010 Funda Wang <fwang@mandriva.org> 0.17-2mdv2011.0
+ Revision: 565566
- rebuild for new exiv2

* Fri Apr 02 2010 Frederic Crozat <fcrozat@mandriva.com> 0.17-1mdv2010.1
+ Revision: 530776
- Release 0.17
- Remove patch1 (merged upstream)

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.16-3mdv2010.1
+ Revision: 488806
- rebuilt against libjpeg v8

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 0.16-2mdv2010.1
+ Revision: 484192
- Rebuild for new libexiv2

* Fri Oct 16 2009 Frederic Crozat <fcrozat@mandriva.com> 0.16-1mdv2010.0
+ Revision: 457831
- Release 0.16
- Remove patch2 (merged upstream)
- Update patch1 (partially merged)

* Sun Aug 16 2009 Oden Eriksson <oeriksson@mandriva.com> 0.15-2mdv2010.0
+ Revision: 416859
- P2: fix build with gcc-4.4 (fedora)
- rebuilt against libjpeg v7

* Wed Dec 24 2008 Frederic Crozat <fcrozat@mandriva.com> 0.15-1mdv2009.1
+ Revision: 318385
- Release 0.15
- Build with OpenMP (multi-core) support

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sun Oct 19 2008 Frederic Crozat <fcrozat@mandriva.com> 0.14.1-1mdv2009.1
+ Revision: 295409
- Release 0.14.1

* Thu Oct 16 2008 Funda Wang <fwang@mandriva.org> 0.14-1mdv2009.1
+ Revision: 294230
- BR cfitsio
- New version 0.14
- there is no use shipping two .desktop files

* Mon Sep 08 2008 Funda Wang <fwang@mandriva.org> 0.13-5mdv2009.0
+ Revision: 282456
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.13-4mdv2009.0
+ Revision: 225896
- rebuild
- fix spacing at top of description
- fix description

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Dec 29 2007 Frederic Crozat <fcrozat@mandriva.com> 0.13-3mdv2008.1
+ Revision: 139175
- Patch0 (CVS): various CVS fixes :fix integer overflow in Canon exposure, additional WB settings, fix incandescent 400D WB, fix window resizing

  + Thierry Vignaud <tv@mandriva.org>
    - auto-convert XDG menu entry
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 26 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.13-2mdv2008.1
+ Revision: 112022
- Rebuild for new exiv2

* Tue Nov 13 2007 Frederic Crozat <fcrozat@mandriva.com> 0.13-1mdv2008.1
+ Revision: 108434
- Release 0.13

* Mon Sep 24 2007 Frederic Crozat <fcrozat@mandriva.com> 0.12.1-2mdv2008.0
+ Revision: 92579
- Fix build (icon extension)

* Thu Aug 16 2007 Funda Wang <fwang@mandriva.org> 0.12.1-1mdv2008.0
+ Revision: 64262
- liblcms has renamed to lcms

  + Frederic Crozat <fcrozat@mandriva.com>
    - Release 0.12.1

* Wed Aug 01 2007 Frederic Crozat <fcrozat@mandriva.com> 0.12-2mdv2008.0
+ Revision: 57557
- Fix cinepaint plugin path
- build with gtkimageview support for 2008.0 and later

* Tue Jul 31 2007 Frederic Crozat <fcrozat@mandriva.com> 0.12-1mdv2008.0
+ Revision: 56889
- Release 0.12
- add conditional build for cinepaint plugin (disabled)
- clean buildrequires

* Fri Apr 20 2007 Angelo Naselli <anaselli@mandriva.org> 0.11-2mdv2008.0
+ Revision: 16411
- rebuilt against exiv2 0.14


* Wed Mar 07 2007 Frederic Crozat <fcrozat@mandriva.com> 0.11-1mdv2007.0
+ Revision: 134331
- Release 0.11

* Sun Mar 04 2007 Angelo Naselli <anaselli@mandriva.org> 0.10-5mdv2007.1
+ Revision: 132337
- rebuilt for new libexiv2

* Fri Mar 02 2007 Frederic Crozat <fcrozat@mandriva.com> 0.10-4mdv2007.1
+ Revision: 131484
- Don't package mimetype file, it is merged in shared-mime-info now

* Thu Mar 01 2007 Frederic Crozat <fcrozat@mandriva.com> 0.10-3mdv2007.1
+ Revision: 130674
-Clean specfile
-enable mimetype and gconf schema building
-fix Buildrequires
-install thumbnailer for gnome
-fix .desktop
-fix icon generation

* Tue Dec 05 2006 Pascal Terjan <pterjan@mandriva.org> 0.10-2mdv2007.1
+ Revision: 90781
- Enable debug
- always create XDG menu
- fix categories

* Mon Nov 27 2006 Pascal Terjan <pterjan@mandriva.org> 0.10-1mdv2007.1
+ Revision: 87349
- 0.10
- Import ufraw

* Wed Aug 09 2006 Till Kamppeter <till@mandriva.com> 0.9-1mdv2007.0
- Updated to version 0.9 final.
- Added XDG menu stuff.

* Wed May 10 2006 Lenny Cartier <lenny@mandriva.com> 0.8-1mdk
- Updated to version 0.8 final.

* Tue Mar 07 2006 Till Kamppeter <till@mandriva.com> 0.7-1mdk
- Updated to version 0.7 final.

* Fri Feb 03 2006 Till Kamppeter <till@mandriva.com> 0.7-0.1mdk
- Updated to the state of the CVS of 03/02/2006 (based on dcraw 8.03).
- Introduced %%mkrel.

* Wed Nov 16 2005 Till Kamppeter <till@mandriva.com> 0.6-1mdk
- Updated to version 0.6 final.

* Tue Oct 04 2005 Till Kamppeter <till@mandriva.com> 0.6-0.1mdk
- Updated to the state of the CVS of 03/10/2005 (0.6 generation of
  UFRaw).

* Fri Sep 16 2005 Till Kamppeter <till@mandriva.com> 0.5-0.4mdk
- Do the update really.
- Added man page.

* Thu Sep 15 2005 Till Kamppeter <till@mandriva.com> 0.5-0.3mdk
- Updated to the state of the CVS of 14/09/2005 (Fix for Sigma SD9 and
  SD10 DSLRs, bug 18552).

* Mon Aug 15 2005 Till Kamppeter <till@mandriva.com> 0.5-0.2mdk
- Updated to the state of the CVS of 14/08/2005 (underlying dcraw updated
  to 7.49, now new cameras like Minolta Alpha/Dynax/Maxxum 5D supported).

* Thu Aug 04 2005 Till Kamppeter <till@mandriva.com> 0.5-0.1mdk
- Updated to the state of the CVS of 03/08/2005 (dcraw 7.x intergrated).

* Mon Mar 07 2005 Till Kamppeter <till@mandrakesoft.com> 0.4-2mdk
- Added standalone version.

* Mon Mar 07 2005 Till Kamppeter <till@mandrakesoft.com> 0.4-1mdk
- Updated to version 0.4.
- New URL.
- Added "Requires: gimp".

* Mon Nov 08 2004 Till Kamppeter <till@mandrakesoft.com> 0.2-1mdk
- First release for Mandrakelinux


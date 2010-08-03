%define	name		ufraw
%define	version		0.17
%define	release		%mkrel 2

%define build_cinepaint 0
%{?_with_cinepaint: %global build_cinepaint 1}

%if build_cinepaint
%define cinepaint_dir %(pkg-config --variable=programplugindir cinepaint-gtk)
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Graphical tool to convert raw images of digital cameras
Group:		Graphics
URL:		http://ufraw.sourceforge.net/
Source0:	http://downloads.sourceforge.net/sourceforge/ufraw/%{name}-%{version}.tar.gz
License:	GPLv2+
BuildRequires:	libgimp-devel >= 2.0 gtk+2-devel libjpeg-devel
BuildRequires:	libtiff-devel zlib-devel lcms-devel imagemagick
BuildRequires:	libexiv-devel bzip2-devel cfitsio-devel
BuildRequires:	libgomp-devel lensfun-devel
%if %build_cinepaint
BuildRequires: cinepaint-devel
%endif
%if %mdkver >= 200800
BuildRequires: gtkimageview-devel
%endif
Buildroot:	%_tmppath/%name-%version-%release-root

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

%package gimp
Summary: 	Reads the raw image formats of digital cameras into GIMP
Group: 		Graphics
Requires: 	gimp
Conflicts:	dcraw-gimp2.0 rawphoto
 
%description gimp
A GIMP plug-in which reads and processes raw images from most digital
cameras. The conversion is done by the dcraw software and so all
cameras supported by dcraw are also supported by this plug-in.

In contrary to the original GIMP plug-in of dcraw this one is much
more comfortable, especially because of the life preview image but
also due to more options.

%if %build_cinepaint
%package cinepaint
Summary: 	Reads the raw image formats of digital cameras into Cinepaint
Group: 		Graphics
Requires: 	cinepaint
 
%description cinepaint
A Cinepaint plug-in which reads and processes raw images from most digital
cameras. The conversion is done by the dcraw software and so all
cameras supported by dcraw are also supported by this plug-in.
%endif

%prep
%setup -q

%build
%configure2_5x --enable-mime
%make

%install
rm -fr %buildroot
%makeinstall_std schemasdir=%{_sysconfdir}/gconf/schemas
%find_lang ufraw

install -d %buildroot%{_datadir}/icons/{large,mini}

convert icons/ufraw.png -resize 32x32 %buildroot%{_iconsdir}/%{name}.png
convert icons/ufraw.png -resize 16x16 %buildroot%{_miconsdir}/%{name}.png
cp icons/ufraw.png %buildroot%{_liconsdir}/%{name}.png

%clean
rm -fr %buildroot

%define schemas ufraw

# Update menus
%if %mdkversion < 200900
%post
%post_install_gconf_schemas %schemas
%update_desktop_database
%update_menus
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%_sysconfdir/gconf/schemas/ufraw.schemas
%_bindir/*
%_datadir/applications/ufraw.desktop
%_datadir/pixmaps/*.png
%_iconsdir/*.png
%_liconsdir/*.png
%_miconsdir/*.png
%_mandir/man1/*

%files gimp
%defattr(-,root,root)
%{_libdir}/gimp/2.0/plug-ins/*

%if %build_cinepaint
%files cinepaint
%defattr(-,root,root)
%{cinepaint_dir}/plug-ins/*
%endif

%bcond_with	cinepaint
%undefine _debugsource_packages

%if %{with cinepaint}
%define cinepaint_dir %(pkg-config --variable=programplugindir cinepaint-gtk)
%endif

Name:		ufraw
Version:	0.22
Release:	13
Summary:	Graphical tool to convert raw images of digital cameras
Group:		Graphics
URL:		http://ufraw.sourceforge.net/
Source0:  https://sourceforge.net/projects/ufraw/files/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/sergiomb2/ufraw/02bc2df0c6c2d9d1892bd16a58e319d81e79559d/beautify_style.sh

# Patch create at upstream issue https://sourceforge.net/p/ufraw/bugs/419/
#Patch0: ufraw-0.22-openmandriva-wrong-variable-dcrawcc.patch
#Import mga patch to fix ARMv7 and aarch64 build.
#Patch2: 05_fix_build_due_to_unsigned_char.patch
#Patch3: ufraw-0.22-exiv2-0.27.patch
Patch4:  https://github.com/sergiomb2/ufraw/compare/ufraw-0-22..684af0548ed76fd97635687fa90a754a7a04a017.diff

License:	GPLv2+
BuildRequires:	gimp-devel >= 2.0
BuildRequires:	pkgconfig(gtk+-x11-2.0)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(lensfun)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(jasper)
%if %{with cinepaint}
BuildRequires:	cinepaint-devel
%endif
BuildRequires:	pkgconfig(gtkimageview)
BuildRequires: pkgconfig(libssh)	

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
# Not using autosetup because patches touch SOURCE1
%setup -q
cp %{SOURCE1} .
%autopatch -p1
./autogen.sh

%build
export CPPFLAGS="-I/usr/include/lensfun"
%configure --enable-mime
%make_build

%install
%make_install schemasdir=%{_sysconfdir}/gconf/schemas
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
%{_datadir}/appdata/ufraw.appdata.xml
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

%global codename sphericalcow
# Package is only arch specific due to missing deps on arm
# Debuginfo package is useless.
%global debug_package %{nil}

Name: arquetype-logos
Summary: arquetype logos for release 22
Version: 21.0.5
Release: 4%{?dist}
Group: System Environment/Base
URL: https://git.fedorahosted.org/git/fedora-logos.git
Source0: arquetype-logos-%{version}.tar.bz2
License: Licensed only for approved usage, see COPYING for details. 
Obsoletes: redhat-logos
Obsoletes: gnome-logos
Provides: redhat-logos = %{version}-%{release}
Provides: gnome-logos = %{version}-%{release}
Provides: system-logos = %{version}-%{release}
Conflicts: kdebase <= 3.1.5
Conflicts: anaconda-images <= 10
Conflicts: redhat-artwork <= 5.0.5

Obsoletes:  fedora-logos
Provides:   fedora-logos 


# For splashtolss.sh
%ifarch x86_64 i686
BuildRequires: syslinux-perl, netpbm-progs
%endif
Requires(post): coreutils
BuildRequires: hardlink
# For _kde4_* macros:
BuildRequires: kde-filesystem
# For optimizing png files
BuildRequires: optipng
# For generating the EFI icon
BuildRequires: ImageMagick
BuildRequires: libicns-utils

%description
arquetype logos for release 22

%package httpd
Summary: Fedora-related icons and pictures used by httpd
Provides: system-logos-httpd = %{version}-%{release}
BuildArch: noarch

Obsoletes:  fedora-logos-httpd
Provides:   fedora-logos-httpd

%description httpd
arquetype logos for release 22

%prep
%setup -q

%build
make bootloader/arquetype.icns

%install
# should be ifarch i386
%if 0%{?fedora} <= 17
mkdir -p $RPM_BUILD_ROOT/boot/grub
install -p -m 644 -D bootloader/splash.xpm.gz $RPM_BUILD_ROOT/boot/grub/splash.xpm.gz
%endif
mkdir -p $RPM_BUILD_ROOT/boot/grub2/themes/system/
install -p -m 644 bootloader/background.png $RPM_BUILD_ROOT/boot/grub2/themes/system/background.png
pushd $RPM_BUILD_ROOT/boot/grub2/themes/system/
# We have to do a cp here instead of an ls because some envs require that
# /boot is VFAT, which doesn't support symlinks.
cp -a background.png fireworks.png
popd
# end i386 bits

mkdir -p $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/arquetype-%{codename}/
for i in firstboot/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/firstboot/themes/arquetype-%{codename}/
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/arquetype.icns $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
# To regenerate these files, run:
# pngtopnm foo.png | ppmtoapplevol > foo.vol
install -p -m 644 bootloader/arquetype.vol bootloader/arquetype-media.vol $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/pixmaps
done

for i in rnotes/* ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/anaconda/pixmaps/$i
  install -p -m 644 $i/* $RPM_BUILD_ROOT%{_datadir}/anaconda/pixmaps/$i
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
for i in plymouth/charge/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
done

for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  pushd $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  ln -s ../../../hicolor/$size/apps/arquetype-logo-icon.png icon-panel-menu.png
  ln -s ../../../hicolor/$size/apps/arquetype-logo-icon.png gnome-main-menu.png
  ln -s ../../../hicolor/$size/apps/arquetype-logo-icon.png kmenu.png
  ln -s ../../../hicolor/$size/apps/arquetype-logo-icon.png start-here.png
  popd
  for i in icons/hicolor/$size/apps/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  done
done

mkdir -p $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/48x48/apps/
install -p -m 644 icons/hicolor/48x48/apps/anaconda.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/48x48/apps/
mkdir -p $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/
install -p -m 644 icons/hicolor/scalable/apps/anaconda.svg $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/scalable/apps/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_datadir}/icons/hicolor/16x16/apps/arquetype-logo-icon.png favicon.png
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/xfce4_xicon1.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 icons/hicolor/scalable/apps/arquetype-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg
install -p -m 644 icons/hicolor/scalable/apps/anaconda.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/anaconda.svg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
ln -s ../apps/start-here.svg .
popd

(cd anaconda; make DESTDIR=$RPM_BUILD_ROOT install)
%ifarch i686 x86_64
(cd anaconda; make DESTDIR=$RPM_BUILD_ROOT install-lss)
%endif

# Variant art
pushd anaconda
for i in cloud server workstation ; do
  cp -a $i $RPM_BUILD_ROOT%{_datadir}/anaconda/pixmaps/
done
popd

for i in 16 22 24 32 36 48 96 256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/arquetype-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places/start-here.png
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/arquetype-logo-icon.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-arquetype.png 
done

# DO NOT REMOVE THIS ICON!!! We still support the Leonidas and Solar themes!
mkdir -p $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/
install -p -m 644 kde-splash/Leonidas-arquetype.png $RPM_BUILD_ROOT%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a fedora/*.svg $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a css3 $RPM_BUILD_ROOT%{_datadir}/%{name}/

# save some dup'd icons
# Except in /boot. Because some people think it is fun to use VFAT for /boot.
/usr/sbin/hardlink -v %{buildroot}/usr

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_datadir}/icons/Bluecurve || :
touch --no-create %{_datadir}/icons/Arquetype || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor || :
  touch --no-create %{_datadir}/icons/Bluecurve || :
  touch --no-create %{_datadir}/icons/Arquetype || :
  touch --no-create %{_kde4_iconsdir}/oxygen ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/Arquetype &>/dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Bluecurve &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/Arquetype &>/dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &>/dev/null || :

%files
%doc COPYING
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/firstboot/themes/arquetype-%{codename}/
%{_datadir}/plymouth/themes/charge/
# No one else before us owns this, so we shall.
%dir %{_kde4_sharedir}/kde4/
%{_kde4_iconsdir}/oxygen/
# DO NOT REMOVE THIS ICON!!! We still support the Leonidas and Solar themes!
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

%{_datadir}/pixmaps/*
%exclude %{_datadir}/pixmaps/poweredby.png
%{_datadir}/anaconda/pixmaps/*
%ifarch x86_64 i686
%{_datadir}/anaconda/boot/splash.lss
%endif
%{_datadir}/anaconda/boot/syslinux-splash.png
%{_datadir}/anaconda/boot/splash.png
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/icons/Bluecurve/*/apps/*
%{_datadir}/%{name}/

# we multi-own these directories, so as not to require the packages that
# provide them, thereby dragging in excess dependencies.
%dir %{_datadir}/icons/Bluecurve/
%dir %{_datadir}/icons/Bluecurve/16x16/
%dir %{_datadir}/icons/Bluecurve/16x16/apps/
%dir %{_datadir}/icons/Bluecurve/22x22/
%dir %{_datadir}/icons/Bluecurve/22x22/apps/
%dir %{_datadir}/icons/Bluecurve/24x24/
%dir %{_datadir}/icons/Bluecurve/24x24/apps/
%dir %{_datadir}/icons/Bluecurve/32x32/
%dir %{_datadir}/icons/Bluecurve/32x32/apps/
%dir %{_datadir}/icons/Bluecurve/36x36/
%dir %{_datadir}/icons/Bluecurve/36x36/apps/
%dir %{_datadir}/icons/Bluecurve/48x48/
%dir %{_datadir}/icons/Bluecurve/48x48/apps/
%dir %{_datadir}/icons/Bluecurve/96x96/
%dir %{_datadir}/icons/Bluecurve/96x96/apps/
%dir %{_datadir}/icons/Bluecurve/256x256/
%dir %{_datadir}/icons/Bluecurve/256x256/apps/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/16x16/
%dir %{_datadir}/icons/hicolor/16x16/apps/
%dir %{_datadir}/icons/hicolor/16x16/places/
%dir %{_datadir}/icons/hicolor/22x22/
%dir %{_datadir}/icons/hicolor/22x22/apps/
%dir %{_datadir}/icons/hicolor/22x22/places/
%dir %{_datadir}/icons/hicolor/24x24/
%dir %{_datadir}/icons/hicolor/24x24/apps/
%dir %{_datadir}/icons/hicolor/24x24/places/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/
%dir %{_datadir}/icons/hicolor/32x32/places/
%dir %{_datadir}/icons/hicolor/36x36/
%dir %{_datadir}/icons/hicolor/36x36/apps/
%dir %{_datadir}/icons/hicolor/36x36/places/
%dir %{_datadir}/icons/hicolor/48x48/
%dir %{_datadir}/icons/hicolor/48x48/apps/
%dir %{_datadir}/icons/hicolor/48x48/places/
%dir %{_datadir}/icons/hicolor/96x96/
%dir %{_datadir}/icons/hicolor/96x96/apps/
%dir %{_datadir}/icons/hicolor/96x96/places/
%dir %{_datadir}/icons/hicolor/256x256/
%dir %{_datadir}/icons/hicolor/256x256/apps/
%dir %{_datadir}/icons/hicolor/256x256/places/
%dir %{_datadir}/icons/hicolor/scalable/
%dir %{_datadir}/icons/hicolor/scalable/apps/
%dir %{_datadir}/icons/hicolor/scalable/places/
%dir %{_datadir}/anaconda
%dir %{_datadir}/anaconda/boot/
%dir %{_datadir}/anaconda/pixmaps/
%dir %{_datadir}/firstboot/
%dir %{_datadir}/firstboot/themes/
%dir %{_datadir}/plymouth/
%dir %{_datadir}/plymouth/themes/
# DO NOT REMOVE THESE DIRS!!! We still support the Leonidas and Solar themes!
%dir %{_kde4_appsdir}
%dir %{_kde4_appsdir}/ksplash
%dir %{_kde4_appsdir}/ksplash/Themes/
%dir %{_kde4_appsdir}/ksplash/Themes/Leonidas/
%dir %{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
# should be ifarch i386
%if 0%{?fedora} <= 17
/boot/grub/splash.xpm.gz
%endif
/boot/grub2/themes/system/background.png
/boot/grub2/themes/system/fireworks.png
# end i386 bits

%files httpd
%doc COPYING
%{_datadir}/pixmaps/poweredby.png

%changelog
* Mon Mar 16 2015 Arquetype Team <arquetype.project@gmail.com>
- arquetype logos for release 22

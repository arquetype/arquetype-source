%global bgname arquetype
%global Bg_Name Arquetype
# Extras will be enabled later
%global with_extras 0 

Name:           %{bgname}-backgrounds
Version:        21.91.0
Release:        1%{?dist}
Summary:        Arquetype 22 default desktop background

Group:          Applications/Multimedia
License:        CC-BY-SA
URL:            https://fedoraproject.org/wiki/F22_Artwork
Source0:        https://fedorahosted.org/released/design-team/%{name}-%{version}.tar.xz

BuildArch:      noarch

# for %%_kde4_* macros
BuildRequires:  kde-filesystem
Requires:       %{name}-gnome = %{version}-%{release}
Requires:       %{name}-kde = %{version}-%{release}
Requires:       %{name}-xfce = %{version}-%{release}
Requires:       %{name}-mate = %{version}-%{release}

Obsoletes:      f22-backgrounds
Provides:       f22-backgrounds


%description
This package contains desktop backgrounds for the Arquetype 22 default theme.
Pulls in themes for GNOME, KDE, Mate and Xfce desktops.

%package        base
Summary:        Base images for Arquetype 22 default background
Group:          Applications/Multimedia
License:        CC-BY-SA

Obsoletes:      f22-backgrounds-base
Provides:       f22-backgrounds-base

%description    base
This package contains base images for Arquetype 22 default background.


%package        kde
Summary:        Arquetype 22 default wallpaper for KDE
Group:          Applications/Multimedia

Requires:       %{name}-base = %{version}-%{release}
Requires:       kde-filesystem

Obsoletes:      f22-backgrounds-kde
Provides:       f22-backgrounds-kde

%description    kde
This package contains KDE desktop wallpaper for the Arquetype 22
default theme.

%package        gnome
Summary:        Arquetype 22 default wallpaper for Gnome and Cinnamon
Group:          Applications/Multimedia

Requires:       %{name}-base = %{version}-%{release}

Obsoletes:      f22-backgrounds-gnome
Provides:       f22-backgrounds-gnome

%description    gnome
This package contains Gnome/Cinnamon desktop wallpaper for the
Arquetype 22 default theme.

%package        mate
Summary:        Arquetype 22 default wallpaper for Mate
Group:          Applications/Multimedia

Requires:       %{name}-base = %{version}-%{release}

Obsoletes:      f22-backgrounds-mate
Provides:       f22-backgrounds-mate

%description    mate
This package contains Mate desktop wallpaper for the Arquetype 22
default theme.

%package        xfce
Summary:        Arquetype 22 default background for XFCE4
Group:          Applications/Multimedia

Requires:       %{name}-base = %{version}-%{release}
Requires:       xfdesktop

Obsoletes:      f22-backgrounds-xfce
Provides:       f22-backgrounds-xfce

%description    xfce
This package contains XFCE4 desktop background for the Arquetype 22
default theme.

%if %{with_extras}
%package        extras-base
Summary:        Base images for Arquetype Extras Backrounds
Group:          Applications/Multimedia
License:        CC-BY and CC-BY-SA

%description    extras-base
This package contains base images for Arquetype supplemental
wallpapers.

%package        extras-gnome
Summary:        Extra Arquetype Wallpapers for Gnome and Cinnamon
Group:          Applications/Multimedia

Requires:       %{name}-extras-base

%description    extras-gnome
This package contains Arquetype supplemental wallpapers for Gnome
and Cinnamon

%package        extras-mate
Summary:        Extra Arquetype Wallpapers for Mate
Group:          Applications/Multimedia

Requires:       %{name}-extras-base

%description    extras-mate
This package contains Arquetype supplemental wallpapers for Mate

%package        extras-kde
Summary:        Extra Arquetype Wallpapers for KDE
Group:          Applications/Multimedia

Requires:       %{name}-extras-base

%description    extras-kde
This package contains Arquetype supplemental wallpapers for Gnome

%package        extras-xfce
Summary:        Extra Arquetype Wallpapers for XFCE
Group:          Applications/Multimedia

Requires:       %{name}-extras-base

%description    extras-xfce
This package contains Arquetype supplemental wallpapers for XFCE
%endif

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc

%files base
%doc CC-BY-SA-3.0 Attribution
%dir %{_datadir}/backgrounds/%{bgname}
%dir %{_datadir}/backgrounds/%{bgname}/default
%{_datadir}/backgrounds/%{bgname}/default/normalish
%{_datadir}/backgrounds/%{bgname}/default/standard
%{_datadir}/backgrounds/%{bgname}/default/wide
%{_datadir}/backgrounds/%{bgname}/default/tv-wide
%{_datadir}/backgrounds/%{bgname}/default/%{bgname}.xml

%files kde
%{_kde4_datadir}/wallpapers/%{Bg_Name}/

%files gnome
%{_datadir}/gnome-background-properties/%{bgname}.xml

%files mate
%{_datadir}/mate-background-properties/%{bgname}.xml

%files xfce
%{_datadir}/xfce4/backdrops/%{bgname}.png

%if %{with_extras}
%files extras-base
%doc CC-BY-SA-3.0 CC-BY-3.0 CC0-1.0 Attribution-Extras
%{_datadir}/backgrounds/%{bgname}/extras/*.jpg
%{_datadir}/backgrounds/%{bgname}/extras/*.png
%{_datadir}/backgrounds/%{bgname}/extras/%{bgname}-extras.xml

%files extras-gnome
%{_datadir}/gnome-background-properties/%{bgname}-extras.xml

%files extras-kde
%{_kde4_datadir}/wallpapers/%{Bg_Name}_*/

%files extras-mate
%{_datadir}/mate-background-properties/%{bgname}-extras.xml

%files extras-xfce
%{_datadir}/xfce4/backdrops/*.jpg
%{_datadir}/xfce4/backdrops/*.png
%endif

%changelog
* Wed Feb 25 2015 Martin Sourada <mso@fedoraproject.org> - 21.91.0-1
- Initial RPM package

Name:           caledonia-plasma5-theme
Version:        1.9
Release:        %{?dist}
# license stated in CHANGELOG and metadata.desktop
License:        CC-BY-SA
Summary:        An elegant dark theme for Plasma
URL:            http://sourceforge.net/projects/caledonia/
Group:          User Interface/Desktops
Source:         caledonia.tar.gz
BuildArch:      noarch
BuildRequires: kde-filesystem

%description
Caledonia is an elegant dark theme for Plasma-KDE, originally based on Ember,
and with several new elements(originals, obtained from other themes, remixed
or re-created). Contains monochrome icons, progress bars and scroll bars
elegantly decorated, a minimalist logout, and much more.

%prep
%setup -q -c

%build

%install
mkdir -pv %buildroot/usr/share/plasma
rm -rf Caledonia/INSTALL
cp -rp Caledonia %buildroot/usr/share/plasma
rm  %buildroot/usr/share/plasma/Caledonia/*/.directory

%files
%doc Caledonia/CHANGELOG.txt
/usr/share/plasma/Caledonia

%changelog
* Sat Mar 21 2015 Arquetype Team <arquetype.project@gmail.com>
- Plasma5 theme


Summary: Package and settings manager for Wine
Name: winetricks
Version: 20130919
Release: 1%{?dist}
BuildArch: noarch
License: GPL+
Group: System Utilities
# Source update from: http://winetricks.googlecode.com/svn/trunk/src/winetricks
Source0: http://winetricks.org/%{name}
Source2: %{name}.png
URL: http://wiki.winehq.org/winetricks
Requires: wine, cabextract, unzip, wget
Obsoletes: %name < %version

%description
Winetricks is an easy way to work around problems in Wine. It has a menu of
supported games/apps for which it can do all the workarounds automatically.
It also lets you install missing DLLs or tweak various Wine settings individually.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/%{name}

#icons
mkdir -p %{buildroot}%{_datadir}/icons/
install -m 644 %{SOURCE2} %buildroot/%{_datadir}/icons/

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Winetricks
GenericName=Winetricks
Comment=Winetricks is an easy way to work around problems in Wine.
Icon=/usr/share/icons/winetricks.png
Type=Application
Categories=Application;Game;
Exec=winetricks
StartupNotify=false
Terminal=false
EOF

%files
%defattr(755, root, root)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Thu Nov 07 2013 David Vásquez <davidjeremias82@gmail.com> - 20130919
- Updated to 20130919

* Thu Jun 06 2013 David Vásquez <davidjeremias82@gmail.com> - 20130416
- Rebuild for Fedora


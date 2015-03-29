%define release_name Hotaru
%define dist_version 22
%define bug_version 22

Summary:        Arquetype release files
Name:           arquetype-release
Version:        22
Release:        0.14
License:        MIT
Group:          System Environment/Base
URL:            http://fedoraproject.org
Source:         %{name}-%{version}.tar.bz2
Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})

Requires:       arquetype-repos

Obsoletes:      fedora-release
Provides:       fedora-release

BuildArch:      noarch

%description
Arquetype release files such as various /etc/ files that define the release.

%package nonproduct
Summary:        Base package for non-product-specific default configurations
Provides:       system-release-nonproduct
Provides:       system-release-nonproduct(%{version})
Provides:       system-release-product
# turned out to be a bad name
Provides:       arquetype-release-standard = 22-0.8
Obsoletes:      arquetype-release-standard < 22-0.8

Requires:       arquetype-release = %{version}-%{release}

Obsoletes:      fedora-release-nonproduct
Provides:       fedora-release-nonproduct

Conflicts:      fedora-release-cloud
Conflicts:      fedora-release-server
Conflicts:      fedora-release-workstation

Conflicts:      arquetype-release-cloud
Conflicts:      arquetype-release-server
Conflicts:      arquetype-release-workstation

%description nonproduct
Provides a base package for non-product-specific configuration files to
depend on.

%package cloud
Summary:        Base package for Arquetype Cloud-specific default configurations
Provides:       system-release-cloud
Provides:       system-release-cloud(%{version})
Provides:       system-release-product

Requires:       arquetype-release = %{version}-%{release}

Obsoletes:      fedora-release-cloud
Provides:       fedora-release-cloud

Conflicts:      fedora-release-server
Conflicts:      fedora-release-nonproduct
Conflicts:      fedora-release-workstation

Conflicts:      arquetype-release-server
Conflicts:      arquetype-release-nonproduct
Conflicts:      arquetype-release-workstation

%description cloud
Provides a base package for Arquetype Cloud-specific configuration files to
depend on.

%package server
Summary:        Base package for Arquetype Server-specific default configurations
Provides:       system-release-server
Provides:       system-release-server(%{version})
Provides:       system-release-product

Requires:       arquetype-release = %{version}-%{release}

Obsoletes:      fedora-release-server
Provides:       fedora-release-server

Requires:       systemd
Requires:       cockpit
Requires:       rolekit
Requires(post):	sed
Requires(post):	systemd

Conflicts:      fedora-release-cloud
Conflicts:      fedora-release-nonproduct
Conflicts:      fedora-release-workstation

Conflicts:      arquetype-release-cloud
Conflicts:      arquetype-release-nonproduct
Conflicts:      arquetype-release-workstation


%description server
Provides a base package for Arquetype Server-specific configuration files to
depend on.

%package workstation
Summary:        Base package for Arquetype Workstation-specific default configurations
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Provides:       system-release-product

Requires:       arquetype-release = %{version}-%{release}

Obsoletes:      fedora-release-workstation
Provides:       fedora-release-workstation

Conflicts:      fedora-release-cloud
Conflicts:      fedora-release-server
Conflicts:      fedora-release-nonproduct

Conflicts:      arquetype-release-cloud
Conflicts:      arquetype-release-server
Conflicts:      arquetype-release-nonproduct

# needed for captive portal support
Requires:       NetworkManager-config-connectivity-fedora
Requires(post): /usr/bin/glib-compile-schemas
Requires(postun): /usr/bin/glib-compile-schemas

%description workstation
Provides a base package for Arquetype Workstation-specific configuration files to
depend on.

%prep
%setup -q
sed -i 's|@@VERSION@@|%{dist_version}|g' Arquetype-Legal-README.txt

%build

%install
install -d $RPM_BUILD_ROOT/etc
echo "Arquetype release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/arquetype-release
echo "cpe:/o:arquetypeproject:arquetype:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/arquetype-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s arquetype-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s arquetype-release $RPM_BUILD_ROOT/etc/system-release

install -d $RPM_BUILD_ROOT/usr/lib
cat << EOF >>$RPM_BUILD_ROOT/usr/lib/os-release
NAME=Arquetype
VERSION="%{dist_version} (%{release_name})"
ID=arquetype
VERSION_ID=%{dist_version}
PRETTY_NAME="Arquetype %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:arquetypeproject:arquetype:%{dist_version}"
HOME_URL="http://arquetype.org/"
EOF

ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%arquetype                %{dist_version}
%%dist                .fc%{dist_version}
%%fc%{dist_version}                1
EOF

# Add Product-specific presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 80-server.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/

# Override the list of enabled gnome-shell extensions for Workstation
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
install -m 0644 org.gnome.shell.gschema.override %{buildroot}%{_datadir}/glib-2.0/schemas/

%post server
if [ $1 -eq 1 ] ; then
        # Initial installation; fix up after %%systemd_post in packages
	# possibly installed before our preset file was added
	units=$(sed -n 's/^enable//p' \
		< %{_prefix}/lib/systemd/system-preset/80-server.preset)
        /usr/bin/systemctl preset $units >/dev/null 2>&1 || :
fi

%postun workstation
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans workstation
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE Arquetype-Legal-README.txt
%config %attr(0644,root,root) /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/arquetype-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist

%files nonproduct
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files cloud
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files server
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_prefix}/lib/systemd/system-preset/80-server.preset

%files workstation
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override

%changelog
* Sat Mar 14 2015 Arquetype Team <arquetype.project@gmail.com>
- Beta release for Arquetype 22

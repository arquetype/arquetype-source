Summary:        Arquetype package repositories
Name:           arquetype-repos
Version:        22
Release:        0.3
License:        MIT
Group:          System Environment/Base
URL:            https://git.fedorahosted.org/cgit/fedora-repos.git/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       fedora-repos(%{version})
Requires:       system-release(%{version})
Obsoletes:      fedora-repos-rawhide < 22-0.3
Obsoletes:      fedora-repos-anaconda < 22-0.3

Obsoletes:      fedora-repos
Provides:       fedora-repos

BuildArch:      noarch

%description
Arquetype package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       arquetype-repos = %{version}-%{release}
Obsoletes:      fedora-release-rawhide <= 22-0.3

Obsoletes:      fedora-repos-rawhide
Provides:       fedora-repos-rawhide

%description rawhide
This package provides the rawhide repo definitions.


%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in arquetype*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/arquetype.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) /etc/yum.repos.d/arquetype-updates.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Sat Mar 14 2015 Arquetype Team <arquetype.project@gmail.com>
- Setup for arquetype 22 branch

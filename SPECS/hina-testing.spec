Name:           hina-testing
Version:        6
Release:        2
Summary:        hina-testing rpm repository

Group:          System Environment/Base
License:        MIT

URL:            http://naruh.com/pub/hina-testing/
Source0:        RPM-GPG-KEY-hina-testing
Source1:        hina-testing.repo

BuildArch:     noarch
Requires:      redhat-release >=  %{version}
Conflicts:     fedora-release

%description
This package contains yum configuration and GPG key for
hina-testing rpm repository.

%prep
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -Dpm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/

%clean
rm -rf $RPM_BUILD_ROOT

%post

%preun

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Wed Jan 16 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 6-1
- Initial commit.

%global         gitcommit 29d65e0
Name:           ruby-build
Version:        20130104.git.2.%{gitcommit}
Release:        1%{?dist}.hn
Summary:        Compile and install Ruby
License:        MIT
URL:            https://github.com/sstephenson/ruby-build/
Group:          System Environment/Daemons

Source0:        https://github.com/sstephenson/ruby-build/tarball/%{gitcommit}

%define _prefix /opt/rbenv/plugins/ruby-build
Prefix:         %{_prefix}

BuildArch:      noarch

Requires:       rbenv

%description
ruby-build is an rbenv plugin that provides an rbenv install command to compile
and install different versions of Ruby on UNIX-like systems.

You can also use ruby-build without rbenv in environments where you need
precise control over Ruby version installation.

%prep
%setup -n sstephenson-ruby-build-%{gitcommit}

%build

%install
rm -rf $RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_prefix}
cp -pr * $RPM_BUILD_ROOT%{_prefix}

%files
%doc %{_prefix}/CHANGELOG.md
%doc %{_prefix}/LICENSE
%doc %{_prefix}/README.md
%{_bindir}/rbenv-install
%{_bindir}/rbenv-uninstall
%{_bindir}/ruby-build
%{_prefix}/install.sh
%{_prefix}/share/
%{_prefix}/test/

%changelog

* Fri Jan 18 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 20130104.git.2.29d65e0
- Add 1.9.3p374
* Sat Dec 29 2012 Hiroaki Nakamura <hnakamur@gmail.com> - 20130104.git.1.4f45814
- Initial version

%global         gitcommit 045f6c1
Name:           rbenv
Version:        0.4.0.git.1.%{gitcommit}
Release:        1%{?dist}.hn
Summary:        Simple Ruby Version Management
License:        MIT
URL:            https://github.com/sstephenson/rbenv/
Group:          System Environment/Daemons

Source0:        https://github.com/sstephenson/rbenv/tarball/%{gitcommit}

%define _prefix /opt/%{name}
Prefix:         %{_prefix}

BuildArch:      noarch

%description
rbenv lets you easily switch between multiple versions of Ruby. It's simple,
unobtrusive, and follows the UNIX tradition of single-purpose tools that do one
thing well.

%prep
%setup -q -n sstephenson-rbenv-%{gitcommit}

%build

%install
rm -rf $RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/etc
cp -pr . $RPM_BUILD_ROOT%{_prefix}
cat <<'EOF' > $RPM_BUILD_ROOT%{_prefix}/etc/bashrc
export RBENV_ROOT=%{_prefix}
export PATH="$RBENV_ROOT/bin:$PATH"
eval "$(rbenv init -)"
EOF

%files
%{_prefix}/

%changelog

* Fri Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 0.4.0.20130109
- Change version scheme to increase monotonously.
* Wed Dec 26 2012 Hiroaki Nakamura <hnakamur@gmail.com> - git-c3fe192
- Initial version.

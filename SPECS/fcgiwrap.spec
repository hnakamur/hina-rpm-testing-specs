%global         gitcommit b9f03e6
Name:           fcgiwrap
Version:        1.0.3.git.1.%{gitcommit}
Release:        1%{?dist}.hn
Summary:        Simple FastCGI wrapper for CGI scripts
License:        MIT
URL:            http://nginx.localdomain.pl/
Group:          System Environment/Daemons

Source0:        https://github.com/gnosek/fcgiwrap/tarball/%{gitcommit}

%define _prefix /opt
Prefix: %{_prefix}

BuildRequires:      autoconf
BuildRequires:      fcgi-devel
Requires:           spawn-fcgi

%description
fcgiwrap is a simple server for running CGI applications over FastCGI.
It hopes to provide clean CGI support to Nginx (and other web servers
that may need it).


%prep
%setup -q -n gnosek-fcgiwrap-%{gitcommit}


%build
autoreconf -i
%configure --prefix=""
make


%install
make install DESTDIR=%{buildroot}

%files
%doc README.rst
%{_sbindir}/fcgiwrap
%{_mandir}/man8/fcgiwrap.8*

%changelog

* Fri Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3.20120908-1
- Change version to increase monotonously.
* Wed Jan  9 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3-3.gitb9f03e6377
- Make the rpm relocatable.
* Tue Dec 25 2012 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3-2.gitb9f03e6377
* Tue Jan 31 2012 Craig Barnes <cr@igbarn.es> - 1.0.3-1.git1328862
- Initial package

Name:           ruby193p374
Version:        1.9.3p374
%define src_ver 1.9.3-p374
Release:        1%{?dist}.hn
Summary:        Ruby installation managed by rbenv
License:        2-clause BSD or Ruby
URL:            http://www.ruby-lang.org/
Group:          Development/Languages

Source0:        http://pyyaml.org/download/libyaml/yaml-0.1.4.tar.gz
Source1:        http://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{src_ver}.tar.gz

%define rbenvroot /opt/rbenv
%define _prefix %{rbenvroot}/versions/%{src_ver}
Prefix:         %{_prefix}


%define extra_pkg_config_path /opt/%{_lib}/pkgconfig

Requires:       rbenv
Requires:       openssl101 >= 1.0.1c

BuildRequires:  gcc
BuildRequires:  ruby-build >= 20130104.git.2.29d65e0
BuildRequires:  zlib-devel
BuildRequires:  openssl101-devel >= 1.0.1c
BuildRequires:  readline-devel

%description
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl).  It is simple, straight-forward, and extensible.

%prep

%build

%install
export PKG_CONFIG_PATH=%{extra_pkg_config_path}:$PKG_CONFIG_PATH

RUBY_BUILD_CACHE_PATH=$RPM_SOURCE_DIR \
  CONFIGURE_OPTS="--prefix %{_prefix}" \
  DESTDIR=$RPM_BUILD_ROOT \
  CFLAGS="`pkg-config --cflags openssl`" \
  LDFLAGS="`pkg-config --libs-only-L openssl`" \
  LIBS="`pkg-config --libs-only-l openssl`" \
  %{rbenvroot}/plugins/ruby-build/bin/ruby-build \
  %{src_ver} $RPM_BUILD_ROOT%{_prefix}

%files
%{_prefix}/

%changelog

* Fri Jan 18 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.9.3p374-1
- Initial version

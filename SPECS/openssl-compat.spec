Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl-compat
Version: 1.0.0
%define release_ver 25
%define release_suffix _3.1
%define origrelease %{release_ver}%{?dist}%{release_suffix}
Release: %{release_ver}%{?dist}%{release_suffix}
Source0: http://mirror.centos.org/centos/%{rhel}/updates/%{_arch}/Packages/openssl-%{version}-%{origrelease}.%{_arch}.rpm
License: Freely distributable
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation. 

OpenSSL is based on the excellent SSLeay library developed from Eric A.
Young and Tim J. Hudson.  The OpenSSL toolkit is licensed under an
Apache-style licence, which basically means that you are free to get and
use it for commercial and non-commercial purposes. 

This package contains the base OpenSSL cryptography and SSL/TLS 
libraries and tools.

%define buildwork %{_builddir}/%{name}-%{version}-%{release}.%{_arch}

%prep
rm -rf %{buildwork}
mkdir -p %{buildwork}
cd %{buildwork}
rpm2cpio %{SOURCE0} | cpio -idm

%build 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/
cp -pr %{buildwork}/usr/lib64 $RPM_BUILD_ROOT/usr/lib64

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%attr(0755,root,root) %{_libdir}/

%post
ldconfig

%postun
ldconfig

%changelog
* Fri Feb  8 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.0-25
- Use openssl-1.0.0-25.el6_3.1.rpm

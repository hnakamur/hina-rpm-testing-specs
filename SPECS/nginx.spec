#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx

%define extra_pkg_config_path /opt/lib64/pkgconfig

Summary: high performance web server
Name: nginx
Version: 1.2.6
Release: 4%{?dist}.hn
Vendor: nginx inc.
URL: http://nginx.org/

Source0: http://nginx.org/download/%{name}-%{version}.tar.gz
Source1: logrotate
Source2: nginx.daemontools.run
Source3: nginx.conf
Source4: nginx.vh.default.conf
Source5: nginx.vh.example_ssl.conf

License: 2-clause BSD-like license
Group: System Environment/Daemons

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre8-devel >= 8.32
BuildRequires: perl
BuildRequires: openssl101-devel >= 1.0.1c
Requires: openssl101 >= 1.0.1c
Requires: pcre8 >= 8.32
Requires(post): daemontools
Requires(pre): shadow-utils
Provides: webserver

%description
nginx [engine x] is a HTTP and reverse proxy server, as well as
a mail proxy server

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx
%description debug
not stripped version of nginx build with the debugging log support

%prep
%setup -q

%build
export PKG_CONFIG_PATH=%{extra_pkg_config_path}:$PKG_CONFIG_PATH

./configure \
        --prefix=%{_sysconfdir}/nginx/ \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-cc-opt="%{optflags} $(pkg-config --cflags libpcre) $(pkg-config --cflags openssl)" \
        --with-ld-opt="$(pkg-config --libs libpcre) $(pkg-config --libs openssl)" \
        --with-pcre-jit \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/%{name}-%{version}/objs/nginx \
        %{_builddir}/%{name}-%{version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx/ \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-cc-opt="%{optflags} $(pkg-config --cflags libpcre) $(pkg-config --cflags openssl)" \
        --with-ld-opt="$(pkg-config --libs libpcre) $(pkg-config --libs openssl)" \
        --with-pcre-jit \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

# install daemontools  stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/service
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/service/run

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/%{name}-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx

%dir %{_sysconfdir}/nginx/service
%attr(0755,root,root) %{_sysconfdir}/nginx/service/run

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post

%preun
if [ $1 -eq 0 ]; then
  [ -s /service/nginx ] && rm /service/nginx || :
  svok %{_sysconfdir}/nginx/service/nginx &&
    svc -tx %{_sysconfdir}/nginx/service/nginx || :
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service nginx upgrade &>/dev/null || :
fi

%changelog
* Thu Jan 24 2013 Hiroaki Nakamura <hnakamur@gmail.com> 1.2.6-4
- Use daemontools instead of initscript. Drop suse support.

* Fri Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com> 1.2.6-3
- Update for changes of name in dependent packages.

* Fri Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com>
- Link with pcre 8.32 jit enabled and openssl 1.0.1c

* Tue Dec 11 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.6

* Tue Nov 13 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.5

* Tue Sep 25 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.4

* Tue Aug  7 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.3
- nginx-debug package now actually contains non stripped binary

* Tue Jul  3 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.2

* Tue Jun  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.1

* Mon Apr 23 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.0

* Thu Apr 12 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.15

* Thu Mar 15 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.14
- OpenSUSE init script and SuSE specific changes to spec file added

* Mon Mar  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.13

* Mon Feb  6 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.12
- banner added to install script

* Thu Dec 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.11
- init script enhancements (thanks to Gena Makhomed)
- one second sleep during upgrade replaced with 0.1 sec usleep

* Tue Nov 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.10

* Tue Nov  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.9
- nginx-debug package added

* Tue Oct 11 2011 Sergey Budnevitch <sb@nginx.com>
- spec file cleanup (thanks to Yury V. Zaytsev)
- log dir permitions fixed
- logrotate creates new logfiles with nginx owner
- "upgrade" argument to init-script added (based on fedora one)

* Sat Oct  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.8
- built with mp4 module

* Fri Sep 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.7

* Tue Aug 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.6
- replace "conf.d/*" config include with "conf.d/*.conf" in default nginx.conf

* Tue Aug 10 2011 Sergey Budnevitch
- Initial release

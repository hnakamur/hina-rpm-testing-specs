%define redis_port     6379
%define redis_group    redis
%define redis_user     redis
%define redis_gid_max  476
%define redis_uid_max  476

Name:           redis
Version:        2.6.9
Release:        5%{?dist}.hn
Summary:        An open source, advanced key-value store.
License:        BSD
URL:            http://redis.io/
Group:          Applications/Services

Source0:        http://redis.googlecode.com/files/redis-%{version}.tar.gz
Source1:        redis_conf
Source2:        redis.upstart.conf

Requires:       daemontools

Prefix:         %{_prefix}

%description
Redis is an open source, advanced key-value store. It is often referred to as a
data structure server since keys can contain strings, hashes, lists, sets and
sorted sets.

%prep
%setup -q

%build
make PREFIX=%{_prefix}

%install
make install PREFIX=$RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/redis
sed 's/\${redis_port}/'%{redis_port}'/' \
  %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/redis/%{redis_port}.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init
sed '
s/\${redis_port}/'%{redis_port}'/g
s/\${redis_user}/'%{redis_user}'/g
s/\${redis_group}/'%{redis_group}'/g
' \
  %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/init/redis_%{redis_port}.conf
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/redis/%{redis_port}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/redis

%pre
getent group %{redis_group} >/dev/null || \
    groupadd -r -K SYS_GID_MAX=%{redis_gid_max} %{redis_group}
getent passwd %{redis_user} >/dev/null || \
    useradd -r -K SYS_UID_MAX=%{redis_uid_max} -g %{redis_group} \
    -s /sbin/nologin -d %{_sharedstatedir}/redis -c "redis user" %{redis_user}

%preun
if [ "$1" = "0" ]; then
  status redis_%{redis_port} | grep -q start && stop redis_%{redis_port} || :
fi

%files
%{_prefix}/
%config %{_sysconfdir}/redis/%{redis_port}.conf
%config %{_sysconfdir}/init/redis_%{redis_port}.conf
%attr(0755,%{redis_user},%{redis_group}) %dir %{_sharedstatedir}/redis
%attr(0755,%{redis_user},%{redis_group}) %dir %{_sharedstatedir}/redis/%{redis_port}
%attr(0755,%{redis_user},%{redis_group}) %dir %{_localstatedir}/log/redis

%changelog

* Thu Jan 17 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-5
- Use setuidgid to execute redis in upstart.
* Thu Jan 17 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-4
- Use execas to execute redis in upstart.
* Thu Jan 17 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-3
- Create group and user for redis.
* Thu Jan 17 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-2
- Add upstart config and remove SysV init script.
* Thu Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-1
- Initial version

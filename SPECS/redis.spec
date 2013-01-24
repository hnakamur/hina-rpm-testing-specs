%define redis_port     6379
%define redis_group    redis
%define redis_user     redis
%define redis_gid_max  476
%define redis_uid_max  476

Name:           redis
Version:        2.6.9
Release:        6%{?dist}.hn
Summary:        An open source, advanced key-value store.
License:        BSD
URL:            http://redis.io/
Group:          Applications/Services

Source0:        http://redis.googlecode.com/files/redis-%{version}.tar.gz
Source1:        redis.conf
Source2:        redis.daemontools.run

Requires(post): daemontools

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
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/redis/service/redis_%{redis_port}
sed 's/\${redis_port}/'%{redis_port}'/' \
  %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/redis/%{redis_port}.conf
sed 's/\${redis_port}/'%{redis_port}'/' \
  %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/redis/service/redis_%{redis_port}/run
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
  [ -s /service/redis_%{redis_port} ] && rm /service/redis_%{redis_port} || :
  svok %{_sysconfdir}/redis/service/redis_%{redis_port} &&
    svc -tx %{_sysconfdir}/redis/service/redis_%{redis_port} || :
fi

%files
%{_prefix}/
%config %{_sysconfdir}/redis/%{redis_port}.conf
%attr(0755,%{redis_user},%{redis_group}) %{_sysconfdir}/redis/service/redis_%{redis_port}/run
%attr(0755,%{redis_user},%{redis_group}) %dir %{_sharedstatedir}/redis
%attr(0755,%{redis_user},%{redis_group}) %dir %{_sharedstatedir}/redis/%{redis_port}
%attr(0755,%{redis_user},%{redis_group}) %dir %{_localstatedir}/log/redis

%changelog

* Thu Jan 17 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 2.6.9-6
- Use daemontools instead of upstart.
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

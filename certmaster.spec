Summary:	Remote certificate distribution framework
Name:		certmaster
Version:	0.25
Release:	0.1
Source0:	http://people.fedoraproject.org/~alikins/files/certmaster/%{name}-%{version}.tar.gz
# Source0-md5:	83d6115f2cff4af18e150274602c71c1
Source1:	%{name}.init
Patch0:		%{name}-setup.patch
License:	GPL v2+
Group:		Applications/System
URL:		https://fedorahosted.org/certmaster
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	python >= 1:2.3
Requires:	python-pyOpenSSL
Requires:	rc-scripts
Conflicts:	func < 0.18
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
certmaster is a easy mechanism for distributing SSL certificates.

%prep
%setup -q
%patch0 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pki/%{name}/ca
install -d $RPM_BUILD_ROOT/var/lib/certmaster/triggers/{sign,request,remove}/{pre,post}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/certmaster

ln -s %{_bindir}/certmaster-sync $RPM_BUILD_ROOT/var/lib/certmaster/triggers/sign/post/certmaster-sync
ln -s %{_bindir}/certmaster-sync $RPM_BUILD_ROOT/var/lib/certmaster/triggers/remove/post/certmaster-sync

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add certmaster
%service certmaster restart

%preun
if [ "$1" = 0 ] ; then
	%service certmaster stop
	/sbin/chkconfig --del certmaster
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/certmaster
%attr(755,root,root) %{_bindir}/certmaster-request
%attr(755,root,root) %{_bindir}/certmaster-sync
%attr(755,root,root) %{_bindir}/certmaster-ca
%attr(754,root,root) /etc/rc.d/init.d/certmaster
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/minion-acl.d
%dir %{_sysconfdir}/pki/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/certmaster/minion.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/certmaster/certmaster.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/certmaster_rotate
%{_mandir}/man1/*.1*

%{py_sitescriptdir}/certmaster/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/certmaster-*.egg-info
%endif

%attr(700,root,root) %dir /var/lib/certmaster
%attr(700,root,root) %dir /var/lib/certmaster/certmaster
%attr(700,root,root) %dir /var/lib/certmaster/certmaster/certs
%attr(700,root,root) %dir /var/lib/certmaster/certmaster/csrs
%dir /var/lib/certmaster/peers
%dir /var/lib/certmaster/triggers/sign
%dir /var/lib/certmaster/triggers/sign/pre
%dir /var/lib/certmaster/triggers/sign/post
%dir /var/lib/certmaster/triggers/request
%dir /var/lib/certmaster/triggers/request/pre
%dir /var/lib/certmaster/triggers/request/post
%dir /var/lib/certmaster/triggers/remove
%dir /var/lib/certmaster/triggers/remove/pre
%dir /var/lib/certmaster/triggers/remove/post

%attr(755,root,root) /var/lib/certmaster/triggers/remove/post/certmaster-sync
%attr(755,root,root) /var/lib/certmaster/triggers/sign/post/certmaster-sync

%dir /var/log/certmaster

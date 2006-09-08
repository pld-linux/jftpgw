Summary:	FTP proxy/gateway that uses the FTP protocol
Summary(pl):	Proxy/bramka FTP u¿ywaj±ca protoko³u FTP
Name:		jftpgw
Version:	0.13.5
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.mcknight.de/jftpgw/%{name}-%{version}.tar.gz
# Source0-md5:	f1997ff094d8f243582a127bf732b2fd
Source1:	%{name}.conf
Source2:	%{name}.init
URL:		http://www.mcknight.de/jftpgw/
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Provides:	user(jftpgw)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
jftpgw is an FTP proxy/gateway that uses the FTP protocol (unlike
those FTP proxies that fetch an FTP file but work as an HTTP proxy).
You can use it to make servers behind a firewall/NAT server
(masquerading server) accessible or to allow users behind such
solutions to transfer files to and from the outside of the LAN.

%description -l pl
jftpgw jest proxy/bramk± FTP, u¿ywaj±c± protoko³u FTP (w
przeciwieñstwie do tych proxy FTP, które ¶ci±gaj± pliki po FTP, ale
dzia³aj± jako proxy HTTP). Mo¿na u¿ywaæ jej, aby udostêpniæ serwery za
firewallem/maskarad±, albo ¿eby pozwoliæ u¿ytkownikom w podobnej
sytuacji na przesy³anie plików na i z zewn±trz sieci lokalnej.

%prep
%setup -q

%build
%configure2_13 \
	--with-logpath=/var/log
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/{log,run}/jftpgw}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jftpgw.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jftpgw
touch $RPM_BUILD_ROOT/var/log/jftpgw/jftpgw.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 27 -s /bin/false -g nobody -c "jftpgw ftp proxy daemon" -d /tmp jftpgw

%post
/sbin/chkconfig --add jftpgw
if [ -f /var/run/jftpgw/jftpgw.pid ]; then
	/etc/rc.d/init.d/jftpgw restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/run/jftpgw/jftpgw.pid ]; then
		/etc/rc.d/init.d/jftpgw stop >&2
	fi
	/sbin/chkconfig --del jftpgw
fi

%postun
if [ "$1" = "0" ]; then
	%userremove jftpgw
fi

%files
%defattr(644,root,root,755)
%doc doc/config.html
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/jftpgw
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_mandir}/man1/*
%dir /var/log/jftpgw
%attr(644,jftpgw,root) /var/log/jftpgw/jftpgw.log
%attr(755,jftpgw,root) /var/run/jftpgw

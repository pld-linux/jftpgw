Summary:	FTP proxy/gateway that uses the FTP protocol
Summary(pl):	Proxy/bramka FTP u¿ywaj±ca protoko³u FTP
Name:		jftpgw
Version:	0.13.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.mcknight.de/jftpgw/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.init
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.mcknight.de/jftpgw/
BuildRequires(post,preun):	/sbin/chkconfig
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
przeciwieñtwie do tych proxy FTP, które ¶ci±gaj± pliki po FTP, ale
dzia³aj± jako proxy HTTP). Mo¿na u¿ywaæ jej, aby udostêpniæ serwery za
firewallem/maskarad±, albo ¿eby pozwoliæ u¿ytkownikom w podobnej
sytuacji na przesy³anie plików na i z zewn±trz sieci lokalnej.

%prep
%setup -q
%patch0 -p1

%build
%configure2_13 \
	--with-logpath=/var/log
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/var/log/
install -d $RPM_BUILD_ROOT/var/run/jftpgw/
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jftpgw.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jftpgw
touch $RPM_BUILD_ROOT/var/log/jftpgw.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add jftpgw

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del jftpgw
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/jftpgw
%dir %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%{_mandir}/man1/*
# TODO: nobody cannot own any files!
#%attr(644,nobody,nobody) /var/log/jftpgw.log
#%attr(755,nobody,nobody) /var/run/jftpgw/

Summary:	FTP proxy/gateway that uses the FTP protocol
Summary(pl):	FTP proxy/gateway u¿ywaj±ce protoko³u FTP
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
FTP proxy/gateway

%description -l pl
FTP proxy/gateway

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
/sbin/chkconfig --del jftpgw
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/jftpgw
%config(noreplace) %{_sysconfdir}/*
%{_mandir}/man1/*
%attr(644,nobody,nobody) /var/log/jftpgw.log
%attr(755,nobody,nobody) /var/run/jftpgw/

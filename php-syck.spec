%define modname syck
%define soname %{modname}.so
%define inifile A62_%{modname}.ini

Summary:	YAML-1.0 parser and emitter
Name:		php-%{modname}
Version:	0.9.3
Release:	%mkrel 14
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/syck
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires:	php-hash
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	file
BuildRequires:	syck-devel >= 0.55
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A binding to the Syck library.  YAML(tm) (rhymes with "camel") is a
straightforward machine parsable data serialization format designed for human
readability and interaction with scripting languages. YAML is optimized for
data serialization, configuration settings, log files, Internet messaging and
filtering.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CHANGELOG TODO package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

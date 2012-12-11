%define modname syck
%define soname %{modname}.so
%define inifile A62_%{modname}.ini

Summary:	YAML-1.0 parser and emitter
Name:		php-%{modname}
Version:	0.9.3
Release:	%mkrel 20
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/syck
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		syck-0.9.3-php54x.diff
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

%patch0 -p0

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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-20mdv2012.0
+ Revision: 797004
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-19
+ Revision: 761310
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-18
+ Revision: 696477
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-17
+ Revision: 695472
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-16
+ Revision: 646692
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-15mdv2011.0
+ Revision: 629883
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-14mdv2011.0
+ Revision: 628197
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-13mdv2011.0
+ Revision: 600538
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-12mdv2011.0
+ Revision: 588875
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-11mdv2010.1
+ Revision: 514665
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-10mdv2010.1
+ Revision: 485490
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-9mdv2010.1
+ Revision: 468261
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-8mdv2010.0
+ Revision: 451363
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.9.3-7mdv2010.0
+ Revision: 397612
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-6mdv2010.0
+ Revision: 377033
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-5mdv2009.1
+ Revision: 346641
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-4mdv2009.1
+ Revision: 341820
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-3mdv2009.1
+ Revision: 323108
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-2mdv2009.1
+ Revision: 310313
- rebuilt against php-5.2.7

* Fri Nov 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-1mdv2009.1
+ Revision: 305429
- 0.9.3

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-4mdv2009.0
+ Revision: 238434
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-3mdv2009.0
+ Revision: 200275
- rebuilt for php-5.2.6

* Tue Feb 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-2mdv2008.1
+ Revision: 162769
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 23 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdv2008.1
+ Revision: 111657
- 0.9.2

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-3mdv2008.1
+ Revision: 107728
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-2mdv2008.0
+ Revision: 77583
- rebuilt against php-5.2.4

* Tue Aug 07 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdv2008.0
+ Revision: 59850
- Import php-syck



* Tue Aug 07 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdv2008.0
- initial Mandriva package

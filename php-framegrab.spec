%define modname framegrab
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B11_%{modname}.ini

Summary:	A video frame grabber extension
Name:		php-%{modname}
Version:	0.1.1
Release:	%mkrel 5
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/framegrab/
Source0:	http://pecl.php.net/get/framegrab-%{version}.tgz
Source1:	B11_framegrab.ini
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Provides a set of classes and functions for grabbing video frames from video
capture devices.

%prep

%setup -q -n framegrab-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild
export FRAMEGRAB_SHARED_LIBADD=`pkg-config --libs libpng`

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
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

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
%doc package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


#
# Conditional build:
%bcond_without	python2	# Python 2 binding
%bcond_without	python3	# Python 3 binding
#
Summary:	Braille translator and back-translator library
Summary(pl.UTF-8):	Biblioteka tłumacząca na i z alfabetu Braille'a
Name:		liblouis
Version:	3.11.0
Release:	1
License:	LGPL v2.1+ (library), GPL v3+ (tools)
Group:		Libraries
#Source0Download: http://liblouis.org/downloads/
Source0:	https://github.com/liblouis/liblouis/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e749d3c0933f60dbd3f7ee94034ec214
Patch0:		%{name}-info.patch
URL:		http://liblouis.org/
BuildRequires:	help2man
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-modules >= 1:2.6}
%{?with_python3:BuildRequires:	python3-modules >= 1:3.2}
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo >= 5
BuildRequires:	yaml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Liblouis is an open-source braille translator and back-translator. It
features support for computer and literary braille, supports
contracted and uncontracted translation for many, many languages

%description -l pl.UTF-8
Liblouis to mający otwarte źródła tłumacz na i z alfabetu Braille'a.
Ma obsługę komputerowego i literackiego Braille'a, obowiązujących
i nie obowiązujących tłumaczeń dla naprawdę wielu języków.

%package devel
Summary:	Header files for liblouis library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liblouis
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for liblouis library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki liblouis.

%package static
Summary:	Static liblouis library
Summary(pl.UTF-8):	Statyczna biblioteka liblouis
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liblouis library.

%description static -l pl.UTF-8
Statyczna biblioteka liblouis.

%package -n python-louis
Summary:	Python ctypes binding for liblouis
Summary(pl.UTF-8):	Wiązania Pythona oparte na ctypes do biblioteki liblouis
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-louis
Python ctypes binding for liblouis.

%description -n python-louis -l pl.UTF-8
Wiązania Pythona oparte na ctypes do biblioteki liblouis.

%package -n python3-louis
Summary:	Python 3 ctypes binding for liblouis
Summary(pl.UTF-8):	Wiązania Pythona 3 oparte na ctypes do biblioteki liblouis
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-louis
Python 3 ctypes binding for liblouis.

%description -n python3-louis -l pl.UTF-8
Wiązania Pythona 3 oparte na ctypes do biblioteki liblouis.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' tools/lou_maketable.d/lou_maketable.in

%build
%configure \
	--enable-ucs4

%{__make} -j1 \
	dlname="liblouis.so.17"

%if %{with python2}
cd python
LD_LIBRARY_PATH=$(pwd)/../liblouis/.libs \
%py_build
cd ..
%endif

%if %{with python2}
cd python
LD_LIBRARY_PATH=$(pwd)/../liblouis/.libs \
%py3_build
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python2}
cd python
LD_LIBRARY_PATH=$(pwd)/../liblouis/.libs \
%py_install
cd ..
%py_postclean
%endif

%if %{with python3}
cd python
LD_LIBRARY_PATH=$(pwd)/../liblouis/.libs \
%py3_install
cd ..
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblouis.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/liblouis

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/lou_allround
%attr(755,root,root) %{_bindir}/lou_checkhyphens
%attr(755,root,root) %{_bindir}/lou_checktable
%attr(755,root,root) %{_bindir}/lou_checkyaml
%attr(755,root,root) %{_bindir}/lou_compare
%attr(755,root,root) %{_bindir}/lou_debug
%attr(755,root,root) %{_bindir}/lou_tableinfo
%attr(755,root,root) %{_bindir}/lou_trace
%attr(755,root,root) %{_bindir}/lou_translate
%attr(755,root,root) %{_libdir}/liblouis.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblouis.so.19
%{_datadir}/liblouis
%{_mandir}/man1/lou_allround.1*
%{_mandir}/man1/lou_checkhyphens.1*
%{_mandir}/man1/lou_checktable.1*
%{_mandir}/man1/lou_checkyaml.1*
%{_mandir}/man1/lou_debug.1*
%{_mandir}/man1/lou_tableinfo.1*
%{_mandir}/man1/lou_trace.1*
%{_mandir}/man1/lou_translate.1*

%files devel
%defattr(644,root,root,755)
%doc HACKING doc/liblouis.html
%attr(755,root,root) %{_libdir}/liblouis.so
%{_includedir}/liblouis
%{_pkgconfigdir}/liblouis.pc
%{_infodir}/liblouis.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/liblouis.a

%if %{with python2}
%files -n python-louis
%defattr(644,root,root,755)
%doc python/README
%dir %{py_sitescriptdir}/louis
%{py_sitescriptdir}/louis/__init__.py[co]
%{py_sitescriptdir}/louis-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-louis
%defattr(644,root,root,755)
%doc python/README
%attr(755,root,root) %{_bindir}/lou_maketable
# FIXME: should be in %{_datadir} or %{_libexecdir}
%{_bindir}/lou_maketable.d
%dir %{py3_sitescriptdir}/louis
%{py3_sitescriptdir}/louis/__init__.py
%{py3_sitescriptdir}/louis/__pycache__
%{py3_sitescriptdir}/louis-%{version}-py*.egg-info
%endif

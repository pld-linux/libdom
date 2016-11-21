#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Implementation of W3C DOM
Summary(pl.UTF-8):	Implementacja W3C DOM
Name:		libdom
Version:	0.3.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	c9dbc908997bb4bd2271b4ee892280aa
URL:		http://www.netsurf-browser.org/projects/libdom/
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libhubbub-devel >= 0.3.3
BuildRequires:	libparserutils-devel >= 0.2.3
BuildRequires:	libwapcaplet-devel >= 0.4.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	netsurf-buildsystem >= 1.5
BuildRequires:	pkgconfig
Requires:	libparserutils >= 0.2.3
Requires:	libwapcaplet >= 0.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibDOM is an implementation of the W3C DOM, written in C. It is
currently in development for use with NetSurf and is intended to be
suitable for use in other projects too.

%description -l pl.UTF-8
LibDOM to implementacja W3C DOM, napisana w C. Jest rozwijana do
wykorzystania w ramach projektu NetSurf, ale także z myślą o
możliwości użycia w innych projektach.

%package devel
Summary:	libdom library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel >= 1.95
Requires:	libhubbub-devel >= 0.3.1

%description devel
This package contains the include files and other resources you can
use to incorporate libdom into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libdom w swoich
programach.

%package static
Summary:	libdom static library
Summary(pl.UTF-8):	Statyczna biblioteka libdom
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libdom library.

%description static -l pl.UTF-8
Statyczna biblioteka libdom.

%prep
%setup -q

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libdom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdom.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdom.so
%{_includedir}/dom
%{_pkgconfigdir}/libdom.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdom.a
%endif

#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Implementation of W3C DOM
Name:		libdom
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	055878cf633a935031517e2e209062f6
#Patch0:		lib.patch
URL:		http://www.netsurf-browser.org/projects/libdom/
BuildRequires:	libhubbub-devel >= 0.3.0
BuildRequires:	libparserutils-devel >= 0.2.0
BuildRequires:	libwapcaplet-devel >= 0.2.1
BuildRequires:	libxml2-devel
BuildRequires:	netsurf-buildsystem >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibDOM is an implementation of the W3C DOM, written in C. It is
currently in development for use with NetSurf and is intended to be
suitable for use in other projects too.

%package devel
Summary:	libdom library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libdom into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libdom w swoich
programach.

%package static
Summary:	libdom static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libdom
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libdom libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libdom.

%prep
%setup -q
#%%patch0 -p1

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdom.so.*.*.*
%ghost %{_libdir}/libdom.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdom.so
%{_includedir}/dom
%{_pkgconfigdir}/libdom.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdom.a
%endif

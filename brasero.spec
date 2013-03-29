Summary:	Disc burning application for GNOME
Name:		brasero
Version:	3.8.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/3.8/%{name}-%{version}.tar.xz
# Source0-md5:	0a380af9dc134084fb04f54f2a656e6f
URL:		http://www.gnome.org/projects/brasero/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	intltool
BuildRequires:	libburn-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libisofs-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	nautilus-devel
BuildRequires:	pkg-config
BuildRequires:	totem-pl-parser-devel
BuildRequires:	tracker-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	gtk+-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	%{name}-libs = %{version}-%{release}
Suggests:	cdrdao
Suggests:	cdrkit
Suggests:	dvd+rw-tools
Suggests:	dvdauthor
Suggests:	gstreamer-plugins-good
Suggests:	libdvdcss
Suggests:	vcdimager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Brasero is a CD/DVD mastering tool for the GNOME desktop. It is
designed to be simple and easy to use.

%package libs
Summary:	Brasero library
Group:		X11/Libraries

%description libs
Brasero library.

%package devel
Summary:	Header files for Brasero library
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Brasero library.

%package apidocs
Summary:	Brasero library API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Brasero library API documentation.

%package -n nautilus-extension-brasero
Summary:	Brasero extension for Nautilus
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description -n nautilus-extension-brasero
Brasero integration for Nautilus.

%prep
%setup -q

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-caches 		\
	--disable-cdrtools		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/brasero3/plugins/lib*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%post -n nautilus-extension-brasero
%update_desktop_database_post

%postun -n nautilus-extension-brasero
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/brasero
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/brasero3
%dir %{_libdir}/brasero3/plugins
%attr(755,root,root) %{_libdir}/brasero3/plugins/*.so
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_desktopdir}/brasero.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_mandir}/man1/brasero.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbrasero-burn3.so.?
%attr(755,root,root) %ghost %{_libdir}/libbrasero-media3.so.?
%attr(755,root,root) %ghost %{_libdir}/libbrasero-utils3.so.?
%attr(755,root,root) %{_libdir}/libbrasero-burn3.so.*.*.*
%attr(755,root,root) %{_libdir}/libbrasero-media3.so.*.*.*
%attr(755,root,root) %{_libdir}/libbrasero-utils3.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn3.so
%attr(755,root,root) %{_libdir}/libbrasero-media3.so
%attr(755,root,root) %{_libdir}/libbrasero-utils3.so
%{_includedir}/brasero3
%{_pkgconfigdir}/libbrasero-burn3.pc
%{_pkgconfigdir}/libbrasero-media3.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbrasero-burn
%{_gtkdocdir}/libbrasero-media

%files -n nautilus-extension-brasero
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libnautilus-brasero-extension.so
%{_desktopdir}/brasero-nautilus.desktop


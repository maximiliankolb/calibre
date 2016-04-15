%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%global __provides_exclude_from ^%{_libdir}/%{name}/%{name}/plugins/.*\.so$

Name:           calibre
Version:        2.55.0
Release:        1%{?dist}
Summary:        E-book converter and library manager
Group:          Applications/Multimedia
License:        GPLv3
URL:            http://calibre-ebook.com/

# SourceURL: curl -L http://code.calibre-ebook.com/dist/src > calibre-%%{version}.tar.xz
# Upstream packages some unfree fonts which we cannot redistribute.
# While we're at it, also delete the liberation fonts which we already have.
#
# Download the upstream tarball and invoke this script while in the tarball's
# directory:
# ./getsources.sh %%{version}

Source0:        %{name}-%{version}-nofonts.tar.xz
Source1:        getsources.sh
Source2:        calibre-mount-helper
Source3:        calibre-gui.appdata.xml
#
# Disable auto update from inside the app
#
Patch1:         %{name}-no-update.patch
#
# Do not display multiple apps in desktop files, only the main app
# This is so gnome-software only 'sees' calibre once. 
# 
Patch3:         calibre-nodisplay.patch

BuildRequires:  python >= 2.6
BuildRequires:  python-devel >= 2.6
BuildRequires:  ImageMagick-devel
BuildRequires:  python-setuptools
BuildRequires:  python-qt5-devel
BuildRequires:  python-qt5
BuildRequires:  python-qt5-webkit
BuildRequires:  podofo-devel
BuildRequires:  desktop-file-utils
BuildRequires:  python-mechanize
BuildRequires:  python-lxml
BuildRequires:  python-dateutil
BuildRequires:  python-imaging
BuildRequires:  xdg-utils
BuildRequires:  python-BeautifulSoup
BuildRequires:  chmlib-devel
BuildRequires:  python-cssutils >= 0.9.9
BuildRequires:  sqlite-devel
BuildRequires:  libicu-devel
BuildRequires:  libpng-devel
BuildRequires:  libmtp-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  web-assets-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  libXrender-devel
BuildRequires:  systemd-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  openssl-devel
# calibre installer is so smart that it check for the presence of the
# directory (and then installs in the wrong place)
BuildRequires:  bash-completion
BuildRequires:  python-apsw
BuildRequires:  glib2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libinput-devel
BuildRequires:  libxkbcommon-devel
#
# If python-feedparser is installed at build time there's problems with links. 
# See https://bugzilla.redhat.com/show_bug.cgi?id=1026469
BuildConflicts: python-feedparser

%{?pyqt5_requires}
# once ^^ %%pyqt5_requires is everywhere, can drop python-qt5 dep below -- rex

# Add hard dep to specific qtbase pkg, see build message below -- rex
# Project MESSAGE: This project is using private headers and will therefore be tied to this specific Qt module build version.
# Project MESSAGE: Running this project against other versions of the Qt modules may crash at any arbitrary point.
# Project MESSAGE: This is not a bug, but a result of using Qt internals. You have been warned!
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

Requires:       python-qt5
Requires:       python-qt5-webkit
Requires:       qt5-qtwebkit
Requires:       qt5-qtsvg
Requires:       qt5-qtsensors
Requires:       python-cherrypy
Requires:       python-cssutils
Requires:       ImageMagick
Requires:       odfpy
Requires:       python-lxml
Requires:       python-imaging
Requires:       python-mechanize
Requires:       python-dateutil
Requires:       python-genshi
Requires:       python-BeautifulSoup
Requires:       poppler-utils
# Require the packages of the files which are symlinked by calibre
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts
Requires:       liberation-mono-fonts
Requires:       python-feedparser
Requires:       python-netifaces
Requires:       python-dns
Requires:       python-cssselect
Requires:       python-apsw
Requires:       mathjax

%description
Calibre is meant to be a complete e-library solution. It includes library
management, format conversion, news feeds to ebook conversion as well as
e-book reader sync features.

Calibre is primarily a ebook cataloging program. It manages your ebook
collection for you. It is designed around the concept of the logical book,
i.e. a single entry in the database that may correspond to ebooks in several
formats. It also supports conversion to and from a dozen different ebook
formats.

Supported input formats are: MOBI, LIT, PRC, EPUB, CHM, ODT, HTML, CBR, CBZ,
RTF, TXT, PDF and LRS.

%prep
%setup -q -n %{name}-%{version}

# don't check for new upstream version (that's what packagers do)
%patch1 -p1 -b .no-update
# Hide individual launchers for ebook-edit, ebook-viewer and lrfviewer as they
# are all accessible in the main calibre GUI.
%patch3 -p1 -b .nodisplay

# dos2unix newline conversion
sed -i 's/\r//' src/calibre/web/feeds/recipes/*

# remove shebangs
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*.py
sed -i -e '/^#![ ]*\//, 1d' src/calibre/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*.py
sed -i -e '/^#!\//, 1d' src/templite/*.py
sed -i -e '/^#!\//, 1d' resources/default_tweaks.py
sed -i -e '/^#!\//, 1d' resources/catalog/section_list_templates.py

chmod -x src/calibre/*/*/*/*.py \
    src/calibre/*/*/*.py \
    src/calibre/*/*.py \
    src/calibre/*.py

rm -rvf resources/viewer/mathjax

%build
OVERRIDE_CFLAGS="%{optflags}" python setup.py build

%install
mkdir -p %{buildroot}%{_datadir}

# create directories for xdg-utils
mkdir -p %{buildroot}%{_datadir}/icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor
mkdir -p %{buildroot}%{_datadir}/packages
mkdir -p %{buildroot}%{_datadir}/mime
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/desktop-directories

# create directory for gnome software data
mkdir -p %{buildroot}%{_datadir}/appdata

# create directory for calibre environment module
# the install script assumes it's there.
mkdir -p %{buildroot}%{python_sitelib}

# create directory for completion files, so calibre knows where
# to install them
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

XDG_DATA_DIRS="%{buildroot}%{_datadir}" \
XDG_UTILS_INSTALL_MODE="system" \
LIBPATH="%{_libdir}" \
python setup.py install --root=%{buildroot}%{_prefix} \
                        --prefix=%{_prefix} \
                        --libdir=%{_libdir} \
                        --staging-libdir=%{buildroot}%{_libdir} \
                        --staging-sharedir=%{buildroot}%{_datadir}

# remove shebang from init_calibre.py here because
# it just got spawned by the install script
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/init_calibre.py

# icons
mkdir -p %{buildroot}%{_datadir}/pixmaps/
cp -p resources/images/library.png                \
   %{buildroot}%{_datadir}/pixmaps/%{name}-gui.png
cp -p resources/images/viewer.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-viewer.png
cp -p resources/images/tweak.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-ebook-edit.png

# every file is empty here
find %{buildroot}%{_datadir}/mime -maxdepth 1 -type f -print -delete

# packages aren't allowed to register mimetypes like this
rm -f %{buildroot}%{_datadir}/applications/defaults.list
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache
rm -f %{buildroot}%{_datadir}/mime/application/*.xml
rm -f %{buildroot}%{_datadir}/mime/text/*.xml

desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-ebook-viewer.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-gui.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-lrfviewer.desktop

# mimetype icon for lrf
rm -rf %{buildroot}%{_datadir}/icons/hicolor/128x128
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -p resources/images/mimetypes/lrf.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-sony-bbeb.png
cp -p resources/images/viewer.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/calibre-viewer.png

# these are provided as separate packages
rm -rf %{buildroot}%{_libdir}/%{name}/{odf,cherrypy,encutils,cssutils}
rm -rf %{buildroot}%{_libdir}/%{name}/cal/utils/genshi
rm -rf %{buildroot}%{_libdir}/%{name}/cal/trac

# rm empty feedparser files.
rm -rf %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.*

ln -s %{python_sitelib}/feedparser.py \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.py
ln -s %{python_sitelib}/feedparser.pyc \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.pyc
ln -s %{python_sitelib}/feedparser.pyo \
      %{buildroot}%{_libdir}/%{name}/%{name}/web/feeds/feedparser.pyo

# link to system fonts after we have deleted (see Source0) the non-free ones
# http://bugs.calibre-ebook.com/ticket/3832
ln -s %{_datadir}/fonts/liberation/LiberationMono-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-BoldItalic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationMono-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationMono-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Italic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationMono-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationMono-Regular.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-BoldItalic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Italic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSans-Regular.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSerif-BoldItalic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-BoldItalic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSerif-Bold.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSerif-Italic.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Italic.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSerif-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/liberation/LiberationSerif-Regular.ttf

# delete locales, calibre stores them in a zip file now
rm -rf %{buildroot}%{_datadir}/%{name}/localization/locales/

rm -f %{buildroot}%{_bindir}/%{name}-uninstall

cp -p %{SOURCE2} %{buildroot}%{_bindir}/calibre-mount-helper

cp -p %{SOURCE3} %{buildroot}%{_datadir}/appdata/

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%preun
rm %{_datadir}/%{name}/viewer/mathjax

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
ln -s %{_jsdir}/mathjax %{_datadir}/%{name}/viewer/

%files
%doc COPYRIGHT LICENSE Changelog.yaml
%{_bindir}/calibre
%{_bindir}/calibre-complete
%{_bindir}/calibre-customize
%{_bindir}/calibre-debug
%{_bindir}/calibre-parallel
%{_bindir}/calibre-server
%{_bindir}/calibre-smtp
%{_bindir}/calibre-mount-helper
%{_bindir}/calibredb
%{_bindir}/ebook-convert
%{_bindir}/ebook-device
%{_bindir}/ebook-meta
%{_bindir}/ebook-viewer
%{_bindir}/fetch-ebook-metadata
%{_bindir}/lrf2lrs
%{_bindir}/lrfviewer
%{_bindir}/lrs2lrf
%{_bindir}/markdown-calibre
%{_bindir}/web2disk
%{_bindir}/ebook-polish
%{_bindir}/ebook-edit
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/apps/*
%{python_sitelib}/init_calibre.py*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/appdata/calibre*.appdata.xml

%changelog
* Fri Apr 15 2016 Kevin Fenzi <kevin@scrye.com> - 2.55.0-1
- Update to 2.55.0. Fixes bug #1327565

* Sat Apr 02 2016 Kevin Fenzi <kevin@scrye.com> - 2.54.0-1
- Update to 2.54.0. Fixes bug #1323395

* Fri Mar 11 2016 Kevin Fenzi <kevin@scrye.com> - 2.53.0-1
- Update to 2.53.0. Fixes bug #1316887

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 2.52.0-3
- +(Build)Requires: python-qt5-webkit

* Mon Feb 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.52.0-2
- Repack the sources w/o fonts

* Sat Feb 27 2016 Kevin Fenzi <kevin@scrye.com> - 2.52.0-1
- Update to 2.52.0. Fixes bug #1312514

* Fri Feb 12 2016 Kevin Fenzi <kevin@scrye.com> - 2.51.0-1
- Update to 2.51.0. Fixes bug #1306996

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Kevin Fenzi <kevin@scrye.com> - 2.50.1-1
- Update to 2.50.1

* Fri Jan 15 2016 Helio Chissini de Castro <helio@kde.org> - 2.49.0-1
- Update to 2.49.0 release. Close bug #1298908

* Mon Jan 04 2016 Helio Chissini de Castro <helio@kde.org> - 2.48.0-2
- Add missing qt5-qtsensors dependency. Package don't do proper autodeps

* Fri Jan 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.48.0-1
- Update to 2.48.0. Fixes bug #1295048

* Fri Dec 11 2015 Kevin Fenzi <kevin@scrye.com> - 2.46.0-1
- Update to 2.46.0. Fixes bug #1290767

* Mon Dec 07 2015 Helio Chissini de Castro <helio@kde.org> - 2.45.0-3
- Remove invalid static that breaks compilation againt qt 5.6.0. Deserve review due real necessity
- %%files: remove redundant icon references

* Sun Dec 06 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.45.0-2
- Rebuild for qt5-qtbase

* Fri Nov 27 2015 Kevin Fenzi <kevin@scrye.com> - 2.45.0-1
- Update to 2.45.0. Fixes bug #1286161

* Fri Nov 13 2015 Kevin Fenzi <kevin@scrye.com> - 2.44.0-1
- Update to 2.44.0. Fixes bug #1281767

* Fri Nov 06 2015 Kevin Fenzi <kevin@scrye.com> - 2.43.0-1
- Update to 2.43.0.

* Sun Nov 01 2015 Kevin Fenzi <kevin@scrye.com> 2.42.0-1
- Update to 2.42.0. Fixes bug #1276799

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 2.41.0-2
- rebuild for ICU 56.1

* Fri Oct 16 2015 Kevin Fenzi <kevin@scrye.com> 2.41.0-1
- Update to 2.41.0. Fixes bug #1272439

* Fri Oct 09 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.0-2
- Rebuild for qt5-qtbase-5.1

* Fri Oct 02 2015 Kevin Fenzi <kevin@scrye.com> 2.40.0-1
- Update to 3.40.0. Fixes bug #1268278

* Fri Sep 25 2015 Kevin Fenzi <kevin@scrye.com> 2.39.0-1
- Update to 2.39.0. Fixes bug #1266488

* Fri Sep 11 2015 Kevin Fenzi <kevin@scrye.com> 2.38.0-1
- Update to 2.38.0. Fixes bug #1262317

* Fri Sep 04 2015 Kevin Fenzi <kevin@scrye.com> 2.37.1-1
- Update to 2.37.1. Fixes bug #1260094

* Fri Aug 28 2015 Kevin Fenzi <kevin@scrye.com> 2.36.0-1
- Update to 2.36.0. Fixes bug #1257920

* Tue Aug 25 2015 Rex Dieter <rdieter@fedoraproject.org> 2.35.0-2
- bump release

* Tue Aug 25 2015 Rex Dieter <rdieter@fedoraproject.org> 2.35.0-1.1
- rebuild (for f22 python-qt5)

* Mon Aug 17 2015 Kevin Fenzi <kevin@scrye.com> 2.35.0-1
- Update to 2.35.0. Fixes bug #1253863

* Fri Aug 07 2015 Kevin Fenzi <kevin@scrye.com> 2.34.0-1
- Update to 2.34.0. Fixes bug #1251473

* Sat Aug 01 2015 Rex Dieter <rdieter@fedoraproject.org> 2.33.0-4
- fix typo from previous commit

* Fri Jul 31 2015 Rex Dieter <rdieter@fedoraproject.org> 2.33.0-3
- Add versioned qt5-qtbase runtime dependency

* Thu Jul 30 2015 Rex Dieter <rdieter@fedoraproject.org> 2.33.0-2
- rebuild (sip/python-qt5)

* Sat Jul 25 2015 Kevin Fenzi <kevin@scrye.com> 2.33.0-1
- Update to 2.33.0

* Sat Jul 18 2015 Kevin Fenzi <kevin@scrye.com> 2.32.1-1
- Update to 2.32.1. Fixes bug #1244180

* Fri Jul 17 2015 Kevin Fenzi <kevin@scrye.com> 2.32.0-1
- Update to 2.32.0. Fixed bug #1244180

* Sat Jun 20 2015 Kevin Fenzi <kevin@scrye.com> 2.31.0-1
- Update to 2.31.0. Fixes bug #1233674

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kevin Fenzi <kevin@scrye.com> 2.30.0-1
- Update to 2.30.0. Fixes bug #1228667

* Sat May 30 2015 Kevin Fenzi <kevin@scrye.com> 2.29.0-1
- Update to 2.29.0. Fixes bug #1226315

* Fri May 15 2015 Kevin Fenzi <kevin@scrye.com> 2.28.0-1
- Update to 2.28.0. Fixes bug #1221988

* Fri May 01 2015 Kevin Fenzi <kevin@scrye.com> 2.27.0-1
- Update to 2.27.0

* Fri Apr 24 2015 Kevin Fenzi <kevin@scrye.com> 2.26.0-1
- Update to 2.26.0

* Fri Apr 17 2015 Kevin Fenzi <kevin@scrye.com> 2.25.0-1
- Update to 2.25.0

* Fri Apr 10 2015 Kevin Fenzi <kevin@scrye.com> 2.24.0-1
- Update to 2.24

* Fri Apr 03 2015 Kevin Fenzi <kevin@scrye.com> 2.23.0-1
- Update to 2.23.0

* Sat Mar 21 2015 Kevin Fenzi <kevin@scrye.com> 2.22.0-1
- Update to 2.22.0

* Fri Mar 13 2015 Kevin Fenzi <kevin@scrye.com> 2.20.0-2
- Apply upstream patch to fix metadata cover editing. Fixes bug #1199836

* Fri Feb 20 2015 Kevin Fenzi <kevin@scrye.com> 2.20.0-1
- Update to 2.20.0

* Fri Feb 06 2015 Kevin Fenzi <kevin@scrye.com> 2.19.0-1
- Update to 2.19.0

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 2.18.0-2
- Bump for rebuild.

* Fri Jan 30 2015 Kevin Fenzi <kevin@scrye.com> 2.18.0-1
- Update to 2.18.0

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 2.17.0-2
- rebuild for ICU 54.1

* Fri Jan 23 2015 Kevin Fenzi <kevin@scrye.com> 2.17.0-1
- Update to 2.17.0

* Fri Jan 09 2015 Kevin Fenzi <kevin@scrye.com> 2.16.0-1
- Update to 2.16.0

* Tue Jan 06 2015 Rex Dieter <rdieter@fedoraproject.org> 2.15.0-2
- +%%{?pyqt5_requires}

* Fri Jan 02 2015 Kevin Fenzi <kevin@scrye.com> 2.15.0-1
- Update to 2.15.0

* Fri Dec 26 2014 Kevin Fenzi <kevin@scrye.com> 2.14.0-1
- Update to 2.14.0

* Fri Dec 19 2014 Kevin Fenzi <kevin@scrye.com> 2.13.0-1
- Update to 2.13.0

* Fri Nov 28 2014 Kevin Fenzi <kevin@scrye.com> 2.12.0-1
- Update to 2.12.0

* Fri Nov 21 2014 Kevin Fenzi <kevin@scrye.com> 2.11.0-1
- Update to 2.11.0

* Fri Nov 14 2014 Kevin Fenzi <kevin@scrye.com> 2.10.0-1
- Update to 2.10.0

* Fri Nov 07 2014 Kevin Fenzi <kevin@scrye.com> 2.9.0-1
- Update to 2.9.0

* Fri Oct 31 2014 Kevin Fenzi <kevin@scrye.com> 2.8.0-1
- Update to 2.8.0

* Mon Oct 27 2014 Kevin Fenzi <kevin@scrye.com> 2.7.0-1
- Update to 2.7.0

* Thu Oct 16 2014 Kevin Fenzi <kevin@scrye.com> 2.6.0-1
- Update to 2.6.0

* Fri Oct 03 2014 Kevin Fenzi <kevin@scrye.com> 2.5.0-1
- Update to 2.5.0

* Fri Sep 26 2014 Kevin Fenzi <kevin@scrye.com> 2.4.0-1
- Update to 2.4.0

* Thu Sep 11 2014 Kevin Fenzi <kevin@scrye.com> 2.3.0-1
- Update to 2.3.0

* Fri Sep 05 2014 Kevin Fenzi <kevin@scrye.com> 2.2.0-1
- Update to 2.2.0

* Sun Aug 31 2014 Kevin Fenzi <kevin@scrye.com> 2.1.0-1
- Update to 2.1.0

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 2.0.0-3
- rebuild for ICU 53.1

* Sat Aug 23 2014 Kevin Fenzi <kevin@scrye.com> 2.0.0-2
- Add missing qt5-qtsvg Requires. Fixes bug #1133234

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 2.0.0-1
- Update to 2.0.0 fixes bug #1133091
- Move to Qt5 interface.

* Tue Aug 19 2014 Kevin Fenzi <kevin@scrye.com> 1.48.0-1
- Update to 1.48.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.46.0-3
- update mime scriptlet

* Fri Aug 01 2014 Kalev Lember <kalevlember@gmail.com> 1.46.0-2
- Hide individual launchers for ebook-edit, ebook-viewer and lrfviewer

* Fri Jul 25 2014 Kevin Fenzi <kevin@scrye.com> 1.46.0-1
- Update to 1.46.0

* Fri Jul 18 2014 Kevin Fenzi <kevin@scrye.com> 1.45.0-1
- Update to 1.45.0

* Fri Jul 11 2014 Kevin Fenzi <kevin@scrye.com> 1.44.0-1
- Update to 1.44.0

* Fri Jul 04 2014 Kevin Fenzi <kevin@scrye.com> 1.43.0-1
- Update to 1.43.0

* Fri Jun 27 2014 Kevin Fenzi <kevin@scrye.com> 1.42.0-1
- Update to 1.42.0

* Sat Jun 21 2014 Kevin Fenzi <kevin@scrye.com> 1.41.0-1
- Update to 1.41.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Kevin Fenzi <kevin@scrye.com> 1.39.0-1
- Update to 1.39.0

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 1.38.0-1
- Update to 1.38.0

* Fri May 16 2014 Kevin Fenzi <kevin@scrye.com> 1.37.0-1
- Update to 1.37.0

* Fri May 09 2014 Kevin Fenzi <kevin@scrye.com> 1.36.0-1
- Update to 1.36.0

* Thu May 08 2014 Kevin Fenzi <kevin@scrye.com> 1.35.0-1
- Update to 1.35.0

* Thu Apr 24 2014 Kevin Fenzi <kevin@scrye.com> 1.34.0-1
- Update to 1.34.0

* Fri Apr 18 2014 Kevin Fenzi <kevin@scrye.com> 1.33.0-1
- Update to 1.33.0

* Sun Apr 13 2014 Kevin Fenzi <kevin@scrye.com> 1.32.0-1
- Update to 1.32.0

* Mon Mar 31 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 1.30.0-2
- Rebuild for libMagickWand and libMagickCore

* Sun Mar 30 2014 Kevin Fenzi <kevin@scrye.com> 1.30.0-1
- Update to 1.30.0

* Tue Mar 25 2014 Kevin Fenzi <kevin@scrye.com> 1.29.0-1
- Update to 1.29

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> 1.28.0-2
- rebuild (sip)

* Sat Mar 15 2014 Kevin Fenzi <kevin@scrye.com> 1.28.0-1
- Update to 1.28.0

* Fri Mar 07 2014 Kevin Fenzi <kevin@scrye.com> 1.27.0-1
- Update to 1.27.0

* Thu Feb 27 2014 Kevin Fenzi <kevin@scrye.com> 1.26.0-1
- Update to 1.26.0

* Sat Feb 22 2014 Kevin Fenzi <kevin@scrye.com> 1.25.0-1
- Update to 1.25.0

* Fri Feb 14 2014 Kevin Fenzi <kevin@scrye.com> 1.24.0-1
- Update to 1.24.0

* Thu Feb 13 2014 Kevin Fenzi <kevin@scrye.com> 1.23.0-2
- Rebuild for new icu

* Fri Feb 07 2014 Kevin Fenzi <kevin@scrye.com> 1.23.0-1
- Update to 1.23.0
- Add BuildConflicts: python-feedparser. Bug #1026469

* Sun Feb 02 2014 Kevin Fenzi <kevin@scrye.com> 1.22.0-2
- Install calibre-ebook-edit icon properly. Fixes bug #1060556

* Fri Jan 31 2014 Kevin Fenzi <kevin@scrye.com> 1.22.0-1
- Update to 1.22.0

* Fri Jan 24 2014 Kevin Fenzi <kevin@scrye.com> 1.21.0-1
- Update to 1.21.0

* Fri Jan 24 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 1.20.0-2
- Add appdata

* Sat Jan 18 2014 Kevin Fenzi <kevin@scrye.com> 1.20.0-1
- Update to 1.20.0

* Fri Jan 10 2014 Kevin Fenzi <kevin@scrye.com> 1.19.0-1
- Update to 1.19.0

* Sat Dec 28 2013 Kevin Fenzi <kevin@scrye.com> 1.17.0-1
- Update to 1.17.0

* Sat Dec 07 2013 Kevin Fenzi <kevin@scrye.com> 1.14.0-1
- Update to 1.14.0

* Sat Nov 30 2013 Kevin Fenzi <kevin@scrye.com> 1.13.0-1
- Update to 1.13.0

* Sat Nov 16 2013 Kevin Fenzi <kevin@scrye.com> 1.11.0-1
- Update to 1.11.0

* Mon Nov 04 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 1.9.0-4
- Work around rpm's inability to replace directory with a symlink

* Mon Nov 04 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 1.9.0-3
- Fix bash completion directory detection

* Mon Nov 04 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 1.9.0-2
- Unbundle MathJax (#1017204)
- Package zsh completion script, move bash completion script to /usr/share

* Fri Nov 01 2013 Kevin Fenzi <kevin@scrye.com> 1.9.0-1
- Update to 1.9.0

* Sat Oct 19 2013 Kevin Fenzi <kevin@scrye.com> 1.7.0-1
- Update to 1.7.0

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-2
- rebuild (sip)

* Sun Oct 13 2013 Kevin Fenzi <kevin@scrye.com> 1.6.0-1
- Update to 1.6.0

* Sat Sep 28 2013 Kevin Fenzi <kevin@scrye.com> 1.5.0-1
- Update to 1.5.0

* Fri Sep 20 2013 Kevin Fenzi <kevin@scrye.com> 1.4.0-1
- Update to 1.4.0

* Fri Sep 13 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-2
- Update to 1.3.0

* Fri Aug 30 2013 Kevin Fenzi <kevin@scrye.com> 1.1.0-2
- Update to 1.1.0

* Mon Aug 26 2013 Kevin Fenzi <kevin@scrye.com> 1.0.0-2
- Add requires on python-apsw. Fixes bug #1000835

* Fri Aug 23 2013 Kevin Fenzi <kevin@scrye.com> 1.0.0-1
- Update to 1.0.0

* Wed Aug 14 2013 Kevin Fenzi <kevin@scrye.com> 0.9.43-1
- Update to 0.9.43

* Fri Aug 02 2013 Kevin Fenzi <kevin@scrye.com> 0.9.42-1
- Update to 0.9.42

* Fri Jul 19 2013 Kevin Fenzi <kevin@scrye.com> 0.9.40-1
- Update to 0.9.40

* Fri Jul 12 2013 Kevin Fenzi <kevin@scrye.com> 0.9.39-1
- Update to 0.9.39

* Fri Jul 05 2013 Kevin Fenzi <kevin@scrye.com> 0.9.38-1
- Update to 0.9.38
- Add patch for new python-pillow

* Sun Jun 23 2013 Kevin Fenzi <kevin@scrye.com> 0.9.36-1
- Update to 0.9.36

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.35-2
- rebuild (sip)

* Sat Jun 15 2013 Kevin Fenzi <kevin@scrye.com> 0.9.35-1
- Update to 0.9.35

* Fri Jun 07 2013 Kevin Fenzi <kevin@scrye.com> 0.9.34-1
- Update to 0.9.34

* Fri May 31 2013 Kevin Fenzi <kevin@scrye.com> 0.9.33-1
- Update to 0.9.33

* Fri May 24 2013 Kevin Fenzi <kevin@scrye.com> 0.9.32-1
- Update to 0.9.32

* Fri May 17 2013 Kevin Fenzi <kevin@scrye.com> 0.9.31-1
- Update to 0.9.31

* Sat May 11 2013 Kevin Fenzi <kevin@scrye.com> 0.9.30-1
- Update to 0.9.30

* Sat May 04 2013 Kevin Fenzi <kevin@scrye.com> 0.9.29-1
- Update to 0.9.29

* Sat Apr 27 2013 Kevin Fenzi <kevin@scrye.com> 0.9.28-1
- Update to 0.9.28

* Sat Apr 13 2013 Kevin Fenzi <kevin@scrye.com> 0.9.27-1
- Update to 0.9.27

* Sat Apr 06 2013 Kevin Fenzi <kevin@scrye.com> 0.9.26-1
- Update to 0.9.26

* Fri Mar 29 2013 Kevin Fenzi <kevin@scrye.com> 0.9.25-1
- Update to 0.9.25

* Sat Mar 23 2013 Kevin Fenzi <kevin@scrye.com> 0.9.24-1
- Update to 0.9.24

* Mon Mar 18 2013 Kevin Fenzi <kevin@scrye.com> 0.9.23-2
- Rebuild for new ImageMagick

* Fri Mar 15 2013 Kevin Fenzi <kevin@scrye.com> 0.9.23-1
- Update to 0.9.23

* Fri Mar 08 2013 Kevin Fenzi <kevin@scrye.com> 0.9.22-1
- Update to 0.9.22

* Sat Mar 02 2013 Kevin Fenzi <kevin@scrye.com> 0.9.21-1
- Update to 0.9.21

* Fri Feb 22 2013 Kevin Fenzi <kevin@scrye.com> 0.9.20-1
- Update to 0.9.20

* Sat Feb 16 2013 Kevin Fenzi <kevin@scrye.com> 0.9.19-1
- Update to 0.9.19
- Drop no longer shipped epub-fix in place of new ebook-polish

* Fri Feb 08 2013 Kevin Fenzi <kevin@scrye.com> 0.9.18-1
- Update to 0.9.18

* Tue Feb 05 2013 Kevin Fenzi <kevin@scrye.com> 0.9.17-2
- Drop django-tagging Requires. Fixes bug #908122

* Fri Feb 01 2013 Kevin Fenzi <kevin@scrye.com> 0.9.17-1
- Update to 0.9.17

* Sat Jan 26 2013 Kevin Fenzi <kevin@scrye.com> 0.9.15-2
- Rebuild for new icu

* Tue Jan 22 2013 Kevin Fenzi <kevin@scrye.com> 0.9.15-1
- Update to 0.9.15

* Mon Jan 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.14-2
- Fix import of PIL in bundled textile so it will work with python-pillow

* Fri Jan 11 2013 Kevin Fenzi <kevin@scrye.com> 0.9.14-1
- Update to 0.9.14

* Fri Jan 04 2013 Kevin Fenzi <kevin@scrye.com> 0.9.13-1
- Update to 0.9.13

* Thu Dec 27 2012 Kevin Fenzi <kevin@scrye.com> 0.9.12-1
- Update to 0.9.12

* Sun Dec 23 2012 Kevin Fenzi <kevin@scrye.com> 0.9.11-1
- Update to 0.9.11

* Mon Dec 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-2
- PyQt4 0.9.6 build regression in calibre (#887511)

* Sun Dec 09 2012 Kevin Fenzi <kevin@scrye.com> 0.9.9-1
- Update to 0.9.9

* Fri Nov 30 2012 Kevin Fenzi <kevin@scrye.com> 0.9.8-1
- Update to 0.9.8

* Fri Nov 23 2012 Kevin Fenzi <kevin@scrye.com> 0.9.7-1
- Update to 0.9.7

* Sun Nov 18 2012 Kevin Fenzi <kevin@scrye.com> 0.9.6-2
- Another better approach to unbundling feedparser.

* Fri Nov 09 2012 Kevin Fenzi <kevin@scrye.com> 0.9.6-1
- Update to 0.9.6

* Fri Nov 09 2012 Kevin Fenzi <kevin@scrye.com> 0.9.5-2
- add python-cssselect to requires. Fixes bug #874332

* Sat Nov 03 2012 Kevin Fenzi <kevin@scrye.com> 0.9.5-1
- Update to 0.9.5

* Tue Oct 30 2012 Kevin Fenzi <kevin@scrye.com> 0.9.4-1
- Update to 0.9.4
- Removed 0 length feedparser python files. Fixes bug #868108

* Sat Oct 13 2012 Kevin Fenzi <kevin@scrye.com> 0.9.2-1
- Update to 0.9.2

* Sat Oct 06 2012 Kevin Fenzi <kevin@scrye.com> 0.9.1-1
- Update to 0.9.1

* Wed Oct 03 2012 Kevin Fenzi <kevin@scrye.com> 0.9.0-3
- Add requires on python-dns. Fixes bug #862921

* Tue Oct 02 2012 Kevin Fenzi <kevin@scrye.com> 0.9.0-2
- Rebuild for new sip version

* Fri Sep 28 2012 Kevin Fenzi <kevin@scrye.com> 0.9.0-1
- Update to 0.9.0

* Fri Sep 21 2012 Kevin Fenzi <kevin@scrye.com> 0.8.70-1
- Update to 0.8.70

* Sun Sep 16 2012 Kevin Fenzi <kevin@scrye.com> 0.8.69-1
- Update to 0.8.69

* Sat Sep 08 2012 Kevin Fenzi <kevin@scrye.com> 0.8.68-2
- Add requires for python-netifaces which is needed now.

* Sat Sep 08 2012 Kevin Fenzi <kevin@scrye.com> 0.8.68-1
- Update to 0.8.68

* Mon Sep 03 2012 Kevin Fenzi <kevin@scrye.com> 0.8.67-1
- Update to 0.8.67

* Fri Aug 24 2012 Kevin Fenzi <kevin@scrye.com> 0.8.66-1
- Update to 0.8.66

* Sat Aug 18 2012 Kevin Fenzi <kevin@scrye.com> 0.8.65-1
- Update to 0.8.65

* Mon Aug 13 2012 Kevin Fenzi <kevin@scrye.com> 0.8.64-2
- Unbundle feedparser. Fixes bug #847825

* Sat Aug 11 2012 Kevin Fenzi <kevin@scrye.com> 0.8.64-1
- Update to 0.8.64
- Add libmtp-devel to BuildRequires

* Sun Aug 05 2012 Kevin Fenzi <kevin@scrye.com> 0.8.63-1
- Update to 0.8.63

* Fri Jul 27 2012 Kevin Fenzi <kevin@scrye.com> 0.8.62-1
- Update to 0.8.62

* Sat Jul 21 2012 Kevin Fenzi <kevin@scrye.com> 0.8.61-1
- Update to 0.8.61

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Kevin Fenzi <kevin@scrye.com> 0.8.60-1
- Update to 0.8.60
- Fix new font links. Fixes bug 840319

* Fri Jul 06 2012 Kevin Fenzi <kevin@scrye.com> 0.8.59-1
- Update to 0.8.59

* Fri Jun 15 2012 Kevin Fenzi <kevin@scrye.com> 0.8.56-1
- Update to 0.8.56

* Sat Jun 09 2012 Kevin Fenzi <kevin@scrye.com> 0.8.55-1
- Update to 0.8.55

* Sat Jun 02 2012 Kevin Fenzi <kevin@scrye.com> 0.8.54-1
- Update to 0.8.54
- No longer BuildRequires poppler, instead uses poppler-tools from python.

* Sat May 26 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.53-1
- Update to 0.8.53
- Drop upstreamed poppler 0.20.0 patch.

* Sun May 20 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.52-1
- Update to 0.8.52
- Drop man pages patch, as upstream no longer ships man pages.

* Thu May 17 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.51-2
- Add patch for new poppler 0.20.0

* Sat May 12 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.51-1
- Update to 0.5.51

* Fri May 04 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.50-1
- Update to 0.8.50.
- Add python-cssutils 0.9.9 requirement.

* Fri Apr 27 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.49-1
- Update to 0.8.49

* Wed Apr 25 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.48-2
- Use bundled pyPdf. Approved by  FPC at: https://fedorahosted.org/fpc/ticket/167

* Mon Apr 23 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.48-1
- Update to 0.8.48

* Fri Apr 13 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.47-1
- Update to 0.8.47

* Fri Apr 06 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.46-1
- Update to 0.8.46

* Fri Mar 30 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.45-1
- Update to 0.8.45

* Fri Mar 23 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.44-1
- Update to 0.8.44

* Sat Mar 17 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.43-1
- Update to 0.8.43

* Mon Mar 12 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.42-1
- Update to 0.8.42

* Thu Mar 01 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.41-2
- Rebuild for new ImageMagick

* Fri Feb 24 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.41-1
- Update to 0.8.41

* Fri Feb 17 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.40-1
- Update to 0.8.40

* Fri Feb 10 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.39-1
- Update to 0.8.39

* Fri Jan 27 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.37-1
- Update to 0.8.37

* Fri Jan 20 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.36-1
- Update to 0.8.36

* Tue Jan 17 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.35-1
- Update to 0.8.35

* Fri Jan 06 2012 Kevin Fenzi <kevin@scrye.com> - 0.8.34-1
- Update to 0.8.34

* Sat Dec 31 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.33-2
- Fix no-update patch to prevent exception when trying to close
  the Plugin Preferences dialog (BZ #769714)

* Fri Dec 30 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.33-1
- Update to 0.8.33

* Fri Dec 23 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.32-1
- Update to 0.8.32

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.31-2
- rebuild (sip/PyQt4)

* Fri Dec 16 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.31-1
- Update to 0.8.31

* Fri Dec 09 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.30-1
- Update to 0.8.30

* Fri Dec 02 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.29-1
- Update to 0.8.29

* Fri Nov 25 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.28-1
- Update to 0.8.28

* Fri Nov 18 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.27-1
- Update to 0.8.27

* Sat Nov 12 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.26-1
- Update to 0.8.26

* Sun Nov 06 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.25-1
- Update to 0.8.25
- Rebuild for new libpng

* Fri Oct 28 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.24-1
- Update to 0.8.24

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.8.22-2
- rebuild(poppler)

* Fri Oct 14 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.22-1
- Update to 0.8.22

* Sun Oct 09 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.21-1
- Update to 0.8.21

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.8.20-2
- Rebuild (poppler-0.18.0)

* Fri Sep 23 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.20-1
- Update to 0.8.20

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.8.19-2
- Rebuild (poppler-0.17.3)

* Fri Sep 16 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.19-1
- Update to 0.8.19

* Fri Sep 09 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.18-1
- Update to 0.8.18 and add patch to work with poppler 0.17.3

* Thu Sep 08 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.17-2
- Rebuild for new libicu

* Fri Sep 02 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.17-1
- Update to 0.8.17

* Fri Aug 26 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.16-1
- Update to 0.8.16

* Sat Aug 20 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.15-1
- Update to 0.8.15

* Fri Aug 12 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.14-1
- Update to 0.8.14

* Fri Aug 05 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.13-1
- Update to 0.8.13

* Sun Jul 31 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.12-1
- Update to 0.8.12

* Fri Jul 22 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.11-1
- Update to 0.8.11

* Sat Jul 16 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.10-1
- Update to 0.8.10
- Add patch to work with poppler 0.17

* Fri Jul 01 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.8-1
- Update to 0.8.8

* Mon Jun 27 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.7-1
- Update to 0.8.7
- Update no-update patch
- Adapt locales handling to upstream changes
  (locale files are now placed into a single zip file)

* Sat Jun 04 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.4-1
- Update to 0.8.4

* Fri May 27 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.3-1
- Update to 0.8.3

* Sun May 22 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.2-1
- Update to 0.8.2

* Fri May 13 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.1-1
- Update to 0.8.1

* Fri May 06 2011 Kevin Fenzi <kevin@scrye.com> - 0.8.0-1
- Update to 0.8.0

* Wed May 04 2011 Dan Horák <dan@danny.cz> - 0.7.59-2
- rebuilt against podofo 0.9.1

* Sat Apr 30 2011 Kevin Fenzi <kevin@scrye.com> - 0.7.59-1
- Update to 0.7.59

* Fri Apr 22 2011 Kevin Fenzi <kevin@scrye.com> - 0.7.57-1
- Update to 0.7.57

* Sat Apr 16 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.56-1
- Update to 0.7.56

* Sat Apr 16 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.55-1
- Update to 0.7.55

* Thu Apr 14 2011 Dan Horák <dan@danny.cz> - 0.7.54-2
- rebuilt against podofo 0.9.0

* Fri Apr 08 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.54-1
- Update to 0.7.54

* Sat Apr 02 2011 Kevin Fenzi <kevin@scrye.com> - 0.7.53-1
- Update to 0.7.53

* Sat Mar 26 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.52-1
- Update to 0.7.52

* Tue Mar 22 2011 Christian Krause <chkr@fedoraproject.org> - 0.7.50-2
- Add patch to fix crash on pdf export (BZ #673604)

* Sun Mar 20 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.50-1
- Update to 0.7.50

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.7.49-2
- Rebuild (poppler-0.16.3)

* Fri Mar 11 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.49-1
- Update to 0.7.49

* Mon Mar 07 2011 Caolán McNamara <caolam@redhat.com> - 0.7.47-2
- rebuild for icu 4.6

* Fri Feb 25 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.47-1
- Update to 0.7.47

* Fri Feb 18 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.46-1
- Update to 0.7.46

* Sat Feb 12 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.45-1
- Update to 0.7.45

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.44-1
- Update to 0.7.44

* Thu Jan 27 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.42-2
- track sip-api

* Sat Jan 22 2011 Christian Krause <chkr@fedoraproject.org> - 0.7.42-1
- Update to 0.7.42

* Fri Jan 14 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.40-1
- Update to 0.7.40

* Fri Jan 14 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.39-1
- Update to 0.7.39

* Tue Jan 11 2011 Christian Krause <chkr@fedoraproject.org> - 0.7.38-3
- Fix crash on exit (BZ 559484, 642877, 651727)

* Mon Jan 10 2011 Christian Krause <chkr@fedoraproject.org> - 0.7.38-2
- Remove obsolete BuildRoot tag and %%clean section
- Require font packages which contain files which are symlinked
  by calibre
- Remove unnecessary shebang from internal python files
- Update scriptlets for icon cache
- Don't package mimeinfo.cache, it is auto-generated by
  update-mime-database

* Fri Jan 07 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.38-1
- Update to 0.7.38

* Mon Jan 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.36-2
- rebuild (poppler)

* Sat Jan 01 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.36-1
- Update to 0.7.36

* Thu Dec 23 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.35-1
- Update to 0.7.35

* Fri Dec 17 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.34-1
- Update to 0.7.34

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.33-2
- rebuild (poppler)

* Fri Dec 10 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.33-1
- Update to 0.7.33

* Fri Dec 03 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.32-1
- Update to 0.7.32

* Fri Nov 26 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.30-1
- Update to 0.7.30

* Fri Nov 19 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.29-1
- Update to 0.7.29

* Sat Nov 13 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.28-1
- Update to 0.7.28

* Fri Nov 05 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.27-1
- Update to 0.7.27

* Tue Nov 02 2010 Dan Horák <dan@danny.cz> - 0.7.26-2
- rebuilt against podofo 0.8.4

* Sat Oct 30 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.26-1
- Update to 0.7.26

* Fri Oct 29 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.25-1
- Update to 0.7.25
- http://calibre-ebook.com/whats-new for full changelog

* Fri Oct 22 2010 Dan Horák <dan@danny.cz> - 0.7.24-2
- rebuilt against podofo 0.8.3

* Tue Oct 19 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.24-1
- Update to 0.7.24

* Sat Oct 09 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.23-1
- Update to 0.7.23
- Fix up mount helper with our own local script.
- Change files to list binaries so missing ones can more easily be noted.

* Mon Oct 04 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.22-1
- Update to 0.7.22

* Fri Oct 01 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.21-1
- Update to 0.7.21

* Wed Sep 29 2010 jkeating - 0.7.20-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.20-1
- Update to 0.7.20

* Wed Sep 15 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.18-3
- Rebuild for new ImageMagick

* Mon Sep 13 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.18-2
- Fix svg/png changes.

* Sun Sep 12 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.18-1
- Update to 0.7.18
- Require > 0.9.6 cssutils

* Fri Sep 03 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.17-1
- Update to 0.7.17

* Fri Aug 27 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.16-1
- Update to 0.7.16

* Sat Aug 21 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.15-1
- Update to 0.7.15

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.14-2
- rebuild (poppler)

* Fri Aug 13 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.14-1
- Update to 0.7.14

* Fri Aug 06 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.13-1
- Update to 0.7.13

* Mon Aug 02 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.12-1
- Update to 0.7.12

* Fri Jul 30 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.11-1
- Update to 0.7.11

* Fri Jul 30 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.10-2
- Rebuilt for python2.7

* Fri Jul 23 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.10-1
- Update to 0.7.10

* Sat Jul 17 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.9-1
- Update to 0.7.9

* Sun Jul 11 2010 Michal Nowak <mnowak@redhat.com> - 0.7.8-1
- Update to 0.7.8
- build tar.xz instead of tar.bz2

* Fri Jul 02 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.7-1
- Update to 0.7.7

* Wed Jun 30 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.6-1
- Update to 0.7.6

* Fri Jun 25 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.5-1
- Update to 0.7.5

* Sun Jun 20 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.4-1
- Update to 0.7.4

* Tue Jun 08 2010 Dan Horák <dan@danny.cz> - 0.7.1-2
- rebuilt with podofo 0.8.1

* Mon Jun 07 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.1-1
- Update to 0.7.1
- Added versioned dep on python-cssutils to make sure at least 0.9.6 is installed.

* Fri Jun 04 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.0-1
- Update to 0.7.0

* Fri May 28 2010 Kevin Fenzi <kevin@tummy.com> - 0.6.55-1
- Update to 0.6.55

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 0.6.54-1
- Update to 0.6.54

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 0.6.53-1
- Update to 0.6.53

* Wed May  5 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.6.47-2
- Rebuild against new poppler

* Sat Apr 10 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.47-1
- new upstream release 0.6.47
- new chmlib requirement
- create directory for calibre's environment module
- use bzip2 instead of gzip when preparing tarball in generate-tarball.sh
- remove cssutils patches (we now have python-cssutils 0.9.6 in Fedora)

* Fri Feb 26 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.42-1
- new upstream release 0.6.42
- remove shebang from default_tweaks.py

* Mon Feb  1 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.37-1
- new upstream release 0.6.37

* Fri Jan 29 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.36-1
- new upstream release 0.6.36
- fixed a cssprofiles issue with loading the profiles

* Tue Jan 26 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.35-3
- added -cssprofiles patch to cvs

* Tue Jan 26 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.35-2
- remove python-cssutils 0.9.6 dependency

* Mon Jan 25 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.35-1
- new upstream release
- fedora includes cssutils >= 0.9.6 now; removed the cssprofiles patch
- removed -executables patch, upstream fixed it: http://bugs.calibre-ebook.com/ticket/4437

* Wed Jan  6 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.32-2
- fix for package tagged without adding new patch to cvs

* Wed Jan  6 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.32-1
- new upstream release 0.6.32
- project website has changed
- added python-BeautifulSoup BuildRequire
- new patch to fix full buildpath in binary files

* Sun Dec  6 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.26-1
- New upstream version
- Regenerated no-update patch because of code relocation

* Wed Dec  2 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.25-1
- New upstream release

* Wed Nov 18 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.24-1
- New upstream release: http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.2416Nov2009

* Mon Nov 16 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.23-1
- new upstream release: http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.2313Nov2009
- patch to stop checking for new upstream version

* Sat Nov  7 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.21-1
- new upstream version: http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.2106Nov2009
- added python-BeautifulSoup requirement

* Wed Nov  4 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.6.20-1
- new upstream version:
http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.2030Oct2009
- upstream now ships correct .desktop files
- fixed missing dependency: PyQt4
- fixed calibre-gui icon

* Thu Oct 22 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.19-3
- removed unfree fonts from source package

* Thu Oct 22 2009 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 0.6.19-2
- readability enhancements
- added python-genshi requires
- removed libwmf require since ImageMagick provides libwmf-lite as a
  dependency and that's what we actually need

* Wed Oct 21 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.6.19-1
- new upstream version:
  http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.1920Oct2009
- delete fonts, calibre can find the system fonts
- specify libdir as an install option, so calibre will link properly
  even on 64bit

* Mon Oct 19 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.6.18-1
- updated requires list
- new upstream release
- can override CFLAGS now
- removed trac and genshi duplicates
- use xdg env variables to do desktop integration in the buildroot
- added xdg-utils buildrequire
- install udev rules in /usr/lib even on 64bit and don't own the whole dir
- removed wrongly used Version field from .desktop files

* Mon Oct 12 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.6.17-2
- mimick what calibre's desktop-integration script does (mimetypes, icons etc.)
- removed unneeded INSTALL file
- marked bash completion file as config(noreplace) and take ownership of the dir

* Sat Oct 10 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.6.17-1
- new upstream release: http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.1709Oct2009
- the install process changed significantly
- locales were added

* Thu Sep 10 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.6.11-1
- new upstream release: http://calibre.kovidgoyal.net/wiki/Changelog#Version0.6.1104Sep2009
- minor path fixes
- rearranged files section

* Fri Aug 28 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> 0.6.10-1
- handle desktop files
- don't compress manpages and don't list them as duplicates
- added lrfviewer icon

* Tue Aug 25 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> 0.6.8-1
- Initial RPM release

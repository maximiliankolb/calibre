%{?_sip_api:Requires: python3-pyqt5-sip-api(%{_sip_api_major}) >= %{_sip_api}}

%global __provides_exclude_from ^%{_libdir}/calibre/calibre/plugins/.*\.so$

%global _python_bytecompile_extra 0

Name:           calibre
Version:        4.10.1
Release:        1%{?dist}
Summary:        E-book converter and library manager
License:        GPLv3
URL:            https://calibre-ebook.com/

# SourceURL: curl -L http://code.calibre-ebook.com/dist/src > calibre-%%{version}.tar.xz
# Upstream packages some unfree fonts which we cannot redistribute.
# While we're at it, also delete the liberation fonts which we already have.
#
# Download the upstream tarball and invoke this script while in the tarball's
# directory:
# ./getsources.sh %%{version}

Source0:        calibre-%{version}-nofonts.tar.xz
Source1:        getsources.sh

# Disable auto update from inside the app
Patch1:         calibre-no-update.patch

# Do not display multiple apps in desktop files, only the main app
# This is so gnome-software only 'sees' calibre once.
Patch3:         calibre-nodisplay.patch

# Patches that are not suitable for upstream:
# skip unrardll tests if unrardll has been removed.
Patch4:         https://github.com/keszybz/calibre/commit/497810f8adb992bfecf04e8eacf4ac1340ee6fe0.patch
# sgml was removed, so disable test for it.
Patch5:         https://github.com/keszybz/calibre/commit/01bf854923741bf8d6a6328f17d61e0ec5ac3c9f.patch

ExclusiveArch: %{qt5_qtwebengine_arches}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-qt5-devel
BuildRequires:  python3-qt5
BuildRequires:  podofo-devel
BuildRequires:  desktop-file-utils
BuildRequires:  xdg-utils
BuildRequires:  chmlib-devel
BuildRequires:  sqlite-devel
BuildRequires:  libicu-devel
BuildRequires:  libpng-devel
BuildRequires:  libmtp-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  web-assets-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  libXrender-devel
BuildRequires:  openssl-devel
# calibre installer is so smart that it check for the presence of the
# directory (and then installs in the wrong place)
BuildRequires:  bash-completion
BuildRequires:  glib2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libinput-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libappstream-glib
BuildRequires:  optipng
BuildRequires:  python3dist(apsw)
BuildRequires:  python3dist(mechanize)
BuildRequires:  python3dist(lxml)
BuildRequires:  python3dist(python-dateutil)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(css-parser)
BuildRequires:  python3dist(feedparser)
BuildRequires:  python3dist(netifaces)
BuildRequires:  python3dist(beautifulsoup4)
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(pygments)
BuildRequires:  python3dist(soupsieve)
BuildRequires:  python3dist(msgpack)
BuildRequires:  python3dist(regex)
BuildRequires:  python3dist(html5-parser) >= 0.4.8
BuildRequires:  python3dist(html2text)
BuildRequires:  python3dist(zeroconf)
BuildRequires:  python3dist(markdown) >= 3.0
BuildRequires:  hunspell-devel
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  python-qt5-webengine
BuildRequires:  hyphen-devel
BuildRequires:  mathjax
# Those are only used for tests. Do not add to runtime deps.
BuildRequires:  /usr/bin/jpegtran
BuildRequires:  /usr/bin/JxrDecApp

%{?pyqt5_requires}
# once ^^ %%pyqt5_requires is everywhere, can drop python-qt5 dep below -- rex

# Add hard dep to specific qtbase pkg, see build message below -- rex
# Project MESSAGE: This project is using private headers and will therefore be tied to this specific Qt module build version.
# Project MESSAGE: Running this project against other versions of the Qt modules may crash at any arbitrary point.
# Project MESSAGE: This is not a bug, but a result of using Qt internals. You have been warned!
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

Requires:       python3-qt5
Requires:       python-qt5-webengine
Requires:       qt5-qtwebengine
Requires:       qt5-qtsvg
Requires:       qt5-qtsensors
Requires:       poppler-utils
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts
Requires:       liberation-mono-fonts
Requires:       mathjax
Requires:       optipng
Requires:       python3dist(odfpy)
Requires:       python3dist(lxml)
Requires:       python3dist(pillow)
Requires:       python3dist(mechanize)
Requires:       python3dist(python-dateutil)
Requires:       python3dist(beautifulsoup4)
Requires:       python3dist(soupsieve)
Requires:       python3dist(css-parser)
Requires:       python3dist(feedparser)
Requires:       python3dist(netifaces)
Requires:       python3dist(dnspython)
Requires:       python3dist(apsw)
Requires:       python3dist(psutil)
Requires:       python3dist(pygments)
Requires:       python3dist(msgpack)
Requires:       python3dist(regex)
Requires:       python3dist(html5-parser) >= 0.4.8
Requires:       python3dist(html2text)
Requires:       python3dist(markdown) >= 3.0
Recommends:     python3dist(zeroconf)

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
%autosetup -n calibre-%{version} -p1

# remove shebangs
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*/*/*.py
sed -i -e '/^#![ ]*\//, 1d' src/calibre/*/*.py
sed -i -e '/^#!\//, 1d' src/calibre/*.py
sed -i -e '/^#!\//, 1d' src/css_selectors/*.py
sed -i -e '/^#!\//, 1d' src/polyglot/*.py
sed -i -e '/^#!\//, 1d' src/templite/*.py
sed -i -e '/^#!\//, 1d' src/tinycss/*/*.py
sed -i -e '/^#!\//, 1d' src/tinycss/*.py
sed -i -e '/^#!\//, 1d' resources/default_tweaks.py

chmod -x src/calibre/*/*/*/*.py \
    src/calibre/*/*/*.py \
    src/calibre/*/*.py \
    src/calibre/*.py

# remove bundled MathJax
rm -rvf resources/mathjax

# Skip tests that require removed fonts
sed -r -i 's/\b(test_actual_case|test_clone|test_file_add|test_file_removal|test_file_rename|test_folder_type_map_case|test_merge_file)\b/_skipped_\1/' src/calibre/ebooks/oeb/polish/tests/container.py
# Skip test that fails in mock
sed -r -i 's/\btest_bonjour\b/_skipped_\0/' src/calibre/srv/tests/loop.py

%build
# unbundle MathJax
CALIBRE_PY3_PORT=1 \
%__python3 setup.py mathjax \
    --system-mathjax \
    --path-to-mathjax %{_jsdir}/mathjax/

OVERRIDE_CFLAGS="%{optflags}" \
CALIBRE_PY3_PORT=1 \
%__python3 setup.py build

%install
mkdir -p %{buildroot}%{_datadir}

# create directory for calibre environment module
# the install script assumes it's there.
mkdir -p %{buildroot}%{python3_sitelib}

# create directory for completion files, so calibre knows where
# to install them
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

LIBPATH="%{_libdir}" \
CALIBRE_PY3_PORT=1 \
%__python3 setup.py install --root=%{buildroot}%{_prefix} \
                            --prefix=%{_prefix} \
                            --libdir=%{_libdir} \
                            --staging-root=%{buildroot}%{_prefix} \
                            --staging-libdir=%{buildroot}%{_libdir} \
                            --staging-sharedir=%{buildroot}%{_datadir}

# remove shebang from init_calibre.py here because
# it just got spawned by the install script
sed -i -e '/^#!\//, 1d' %{buildroot}%{python3_sitelib}/init_calibre.py

# there are some python files there, do byte-compilation on them
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/calibre

# icons
mkdir -p %{buildroot}%{_datadir}/pixmaps/
cp -p resources/images/library.png                \
   %{buildroot}%{_datadir}/pixmaps/calibre-gui.png
cp -p resources/images/viewer.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-viewer.png
cp -p resources/images/tweak.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-ebook-edit.png

# packages aren't allowed to register mimetypes like this
rm -f %{buildroot}%{_datadir}/applications/defaults.list
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache
rm -f %{buildroot}%{_datadir}/mime/application/*.xml
rm -f %{buildroot}%{_datadir}/mime/text/*.xml

# check .desktop files
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/calibre-ebook-edit.desktop \
    %{buildroot}%{_datadir}/applications/calibre-ebook-viewer.desktop \
    %{buildroot}%{_datadir}/applications/calibre-gui.desktop \
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
rm -rf %{buildroot}%{_libdir}/calibre/odf

# link to system fonts after we have deleted (see Source0) the non-free ones
# http://bugs.calibre-ebook.com/ticket/3832
%if 0%{?fedora} >= 31
# In fedora 31 liberation fonts moved directories.
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-mono/LiberationMono-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-mono/LiberationMono-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-mono/LiberationMono-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-mono/LiberationMono-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Regular.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-sans/LiberationSans-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-sans/LiberationSans-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-sans/LiberationSans-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-sans/LiberationSans-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Regular.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-serif/LiberationSerif-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-serif/LiberationSerif-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-serif/LiberationSerif-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation-serif/LiberationSerif-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Regular.ttf
%else
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationMono-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationMono-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationMono-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationMono-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationMono-Regular.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSans-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSans-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSans-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSans-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSans-Regular.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSerif-BoldItalic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-BoldItalic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSerif-Bold.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Bold.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSerif-Italic.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Italic.ttf
ln -s --relative \
      %{buildroot}%{_datadir}/fonts/liberation/LiberationSerif-Regular.ttf \
      %{buildroot}%{_datadir}/calibre/fonts/liberation/LiberationSerif-Regular.ttf
%endif

# Remove these 2 appdata files, we can only include one
rm -f %{buildroot}/%{_datadir}/metainfo/calibre-ebook-edit.appdata.xml
rm -f %{buildroot}/%{_datadir}/metainfo/calibre-ebook-viewer.appdata.xml

# rename MathJax folder to allow upgrade from 4.8.0-1 and earlier, which
# relied on a symlink handled by the %%preun and %%posttrans scriptlets
mv %{buildroot}%{_datadir}/calibre/mathjax %{buildroot}%{_datadir}/calibre/mathjax-fedora

%check
# ignore tests on 32 bit arches for now as there's a pdf issue
CALIBRE_PY3_PORT=1 python3 setup.py test \
%ifarch i686 armv7hl
|| :
%endif

appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/calibre-gui.appdata.xml

%preun
if [ -L %{_datadir}/calibre/mathjax ]; then
    rm -f %{_datadir}/calibre/mathjax
fi

%posttrans
ln -s -r %{_datadir}/calibre/mathjax-fedora %{_datadir}/calibre/mathjax

%files
%license LICENSE
%doc Changelog.yaml COPYRIGHT README.md
%{_bindir}/calibre
%{_bindir}/calibre-complete
%{_bindir}/calibre-customize
%{_bindir}/calibre-debug
%{_bindir}/calibre-parallel
%{_bindir}/calibre-server
%{_bindir}/calibre-smtp
%{_bindir}/calibredb
%{_bindir}/ebook-convert
%{_bindir}/ebook-device
%{_bindir}/ebook-edit
%{_bindir}/ebook-meta
%{_bindir}/ebook-polish
%{_bindir}/ebook-viewer
%{_bindir}/fetch-ebook-metadata
%{_bindir}/lrf2lrs
%{_bindir}/lrfviewer
%{_bindir}/lrs2lrf
%{_bindir}/markdown-calibre
%{_bindir}/web2disk
%{_libdir}/calibre/
%{_datadir}/calibre/
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/apps/*
%{python3_sitelib}/init_calibre.py
%{python3_sitelib}/__pycache__/init_calibre.*.py*
%{_datadir}/bash-completion/completions
%{_datadir}/zsh/site-functions/_calibre
%{_datadir}/metainfo/*.appdata.xml

%changelog
* Sat Feb 15 2020 Kevin Fenzi <kevin@scrye.com> - 4.10.1-1
- Update to 4.10.1. Fixes bug #1794445

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Marcus A. Romer <aimylios@gmx.de> - 4.8.0-3
- Add workaround to allow upgrade from 4.8.0-1 and earlier
  (required by the change in method to unbundle MathJax).

* Sun Jan 12 2020 Marcus A. Romer <aimylios@gmx.de> - 4.8.0-2
- Update dependencies.
- Remove some obsolete packaging workarounds.

* Fri Jan 03 2020 Jan Grulich <jgrulich@redhat.com> - 4.8.0-1
- Update to 4.8.0

* Mon Dec 30 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.7.0-1
- Update to 4.7.0 (#1786880, #1773700)

* Wed Dec 25 2019 Jan Grulich <jgrulich@redhat.com> - 4.6.0-2
- rebuild (qt5)

* Thu Dec 19 2019 Kevin Fenzi <kevin@scrye.com> - 4.6.0-1
- Update to 4.6.0. Fixes bug #1783084 and #1780004

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 4.5.0-2
- rebuild (qt5)

* Fri Nov 29 2019 Kevin Fenzi <kevin@scrye.com> - 4.5.0-1
- Update to 4.5.0. Fixes bug #1778002

* Thu Nov 21 2019 Kevin Fenzi <kevin@scrye.com> - 4.4.0-1
- Update to 4.4.0. Fixes bug #1775470

* Sat Nov 09 2019 Kevin Fenzi <kevin@scrye.com> - 4.3.0-1
- Update to 4.3.0.
- Include new per command bash-completions.

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 4.1.0-2
- Rebuild for ICU 65

* Wed Oct 09 2019 Kevin Fenzi <kevin@scrye.com> - 4.1.0-1
- Update to 4.1.0. Fixes bug #1759626

* Thu Oct 03 2019 Kevin Fenzi <kevin@scrye.com> - 4.0.0-1
- Update to 4.0.

* Wed Sep 25 2019 Jan Grulich <jgrulich@redhat.com> - 3.48.0-3
- rebuild (qt5)

* Mon Sep 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 3.48.0-2
- Requires: python3-pyqt5-sip-api (#1748527)

* Fri Sep 13 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.48.0-1
- Update to 3.48.0 (#1751909)

* Tue Sep 03 2019 Kevin Fenzi <kevin@scrye.com> - 3.47.1-2
- Adjust sip requires to Require the python3-sip-api package.

* Mon Sep 02 2019 Kevin Fenzi <kevin@scrye.com> - 3.47.1-1
- Update 3.47.1. Fixes bug #1747848

* Sat Aug 31 2019 Kevin Fenzi <kevin@scrye.com> - 3.47.0-1
- Update to 3.47.0

* Tue Aug 20 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.46.0-2.git20190819
- Rebuilt for Python 3.8

>>>>>>> origin/master
* Mon Aug 19 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.46.0-1.git20190819
- Update to the latest version + various patches (#1667497)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Kevin Fenzi <kevin@scrye.com> - 3.36.0-8
- Add patch for kindle-s. Fixes bug #1731734

* Tue Jun 25 2019 Kevin Fenzi <kevin@scrye.com> - 3.36.0-7
- Adjust for liberation fonts moving around.

* Mon Jun 17 2019 Jan Grulich <jgrulich@redhat.com> - 3.36.0-6
- rebuild (qt5)

* Sat Jun 15 2019 Kevin Fenzi <kevin@scrye.com> - 3.36.0-5
- Rebuild for new qt5.

* Sun Mar 03 2019 Kevin Fenzi <kevin@scrye.com> - 3.36.0-4
- Rebuild for new qt5.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 3.36.0-2
- Rebuild for ICU 63

* Sun Dec 23 2018 Kevin Fenzi <kevin@scrye.com> - 3.36.0-1
- Update to 3.36.

* Thu Dec 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.34.0-2
- rebuild (qt5)

* Sat Dec 01 2018 Kevin Fenzi <kevin@scrye.com> - 3.34.0-1
- Update to 3.34.

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 3.29.0-2
- rebuild (qt5)

* Tue Aug 14 2018 Kevin Fenzi <kevin@scrye.com> - 3.29.0-1
- Update to 3.29.0. Fixes bug #1614778

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.28.0-3
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.28.0-2
- Rebuild for new binutils

* Thu Jul 26 2018 Kevin Fenzi <kevin@scrye.com> - 3.28.0-1
- Update to 3.28.0. Fixes bug #1605186

* Thu Jul 26 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.27.1-5
- Use versioned python macros
- Do explicit byte compilation to conform to new guidelines

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Sandro Mani <manisandro@gmail.com> - 3.27.1-3
- Rebuild (podofo)

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 3.27.1-2
- Rebuild for ICU 62

* Sat Jul  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.27.1-1
- Update to 3.27.1. Fixes bug #1598761

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.26.1-2
- rebuild (qt5)

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 3.26.1-1
- Update to 3.26.1. Fixes bug #1591735

* Sun Jun 03 2018 Kevin Fenzi <kevin@scrye.com> - 3.25.0-1
- Update to 3.25.0. Fixes bug #1585171

* Wed May 30 2018 Kevin Fenzi <kevin@scrye.com> - 3.24.2-1
- Update to 3.24.2.

* Tue May 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 3.23.0-2
- rebuild (qt5)

* Fri May 04 2018 Kevin Fenzi <kevin@scrye.com> - 3.23.0-1
- Update to 3.23.0. Fixes bug #1574953

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 3.22.1-2
- Rebuild for ICU 61.1

* Fri Apr 20 2018 Kevin Fenzi <kevin@scrye.com> - 3.22.1-1
- Update to 3.22.1. Fixes bug #1569983

* Sat Apr 07 2018 Kevin Fenzi <kevin@scrye.com> - 3.21.0-1
- Update to 3.21.0. Fixes bug #1564477

* Fri Mar 23 2018 Kevin Fenzi <kevin@scrye.com> - 3.20.0-1
- Update to 3.20.0. Fixes bug #1559848

* Fri Mar 09 2018 Kevin Fenzi <kevin@scrye.com> - 3.19.0-1
- Update to 3.19.0. Fixes bug #1553719
- Fix for CVE-2018-7889 - bug #1553917,1553919

* Sat Feb 24 2018 Kevin Fenzi <kevin@scrye.com> - 3.18.0-1
- Update to 3.18.0. Fixes bug #1548599

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 3.17.0-2
- rebuild (qt5)

* Fri Feb 09 2018 Kevin Fenzi <kevin@scrye.com> - 3.17.0-1
- Update to 3.17.0. Fixes bug #1543837

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Kevin Fenzi <kevin@scrye.com> - 3.16.0-1
- Update to 3.16.0. Fixes bug #1531515

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.14.0-3
- Remove obsolete scriptlets

* Wed Dec 20 2017 Jan Grulich <jgrulich@redhat.com> - 3.14.0-2
- rebuild (qt5)

* Thu Dec 14 2017 Kevin Fenzi <kevin@scrye.com> - 3.14.0-1
- Update to 3.14.0.

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 3.12.0-3
- Rebuild for ICU 60.1

* Mon Nov 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.12.0-2
- rebuild (qt5)

* Fri Nov 10 2017 Kevin Fenzi <kevin@scrye.com> - 3.12.0-1
- Update to 3.12.0. Fixes bug #1511910

* Wed Nov 08 2017 Kevin Fenzi <kevin@scrye.com> - 3.11.1-2
- Rebuild for upgrade path.

* Thu Nov 02 2017 Kevin Fenzi <kevin@scrye.com> - 3.11.1-1
- Update to 3.11.1. Fixes bug #1508861

* Mon Oct 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.10.0-2
- rebuild (qt5)

* Fri Oct 20 2017 Kevin Fenzi <kevin@scrye.com> - 3.10.0-1
- Update to 3.10.0. Fixes bug #1480024

* Tue Oct 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.4.0-5
- rebuild (qt5)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Kevin Fenzi <kevin@scrye.com> - 3.4.0-2
- Fix dependencies. Bug #1473976

* Thu Jul 20 2017 Kevin Fenzi <kevin@scrye.com> - 3.4.0-1
- Update to 3.4.0. Fixes bug #1471092

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.3.0-2
- rebuild (qt5)

* Fri Jul 07 2017 Kevin Fenzi <kevin@scrye.com> - 3.3.0-1
- Update to 3.3.0. Fixes bug #1468560

* Thu Jul 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.2.1-2
- rebuild (sip)

* Fri Jun 30 2017 Kevin Fenzi <kevin@scrye.com> - 3.2.1-1
- Update to 3.2.1. Fixes bug #1466763

* Sat Jun 24 2017 Kevin Fenzi <kevin@scrye.com> - 3.1.1-1
- Update to 3.1.1. Fixes bug #1464428

* Sun Jun 18 2017 Kevin Fenzi <kevin@scrye.com> - 3.0.0-2
- Fix Requires for 3.0.0. Fixes bug #1462534

* Fri Jun 16 2017 Kevin Fenzi <kevin@scrye.com> - 3.0.0-1
- Update to 3.0.0.

* Fri May 19 2017 Kevin Fenzi <kevin@scrye.com> - 2.85.1-1
- Update to 2.85.1. Fixes bug #1448630

* Tue May 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.83.0-2
- Add patch to build under qt 5.9.0

* Fri May 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.83.0-2
- rebuild (qt5)

* Tue Apr 18 2017 Kevin Fenzi <kevin@scrye.com> - 2.83.0-1
- Update to 2.83.0. Fixes bug #1442893

* Fri Mar 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.82.0-2
- Rebuild for qt-5.8

* Sun Mar 19 2017 Kevin Fenzi <kevin@scrye.com> - 2.82.0-1
- Update to 2.82.0. Fixes bug #1433634

* Sat Mar 11 2017 Kevin Fenzi <kevin@scrye.com> - 2.81.0-1
- Update to 2.81.0. Fixes bug #1431106

* Sat Mar 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.80.0-2
- Update to new name of python2-odfpy

* Fri Feb 24 2017 Kevin Fenzi <kevin@scrye.com> - 2.80.0-1
- Update to 2.80.0. Fixes bug #1426586

* Sun Feb 12 2017 Kevin Fenzi <kevin@scrye.com> - 2.79.1-1
- Update to 2.79.1. Fixes bug #1421443

* Fri Feb 10 2017 Kevin Fenzi <kevin@scrye.com> - 2.79.0-1
- Update to 2.79.0. Fixes bug #1421124

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.78.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Sandro Mani <manisandro@gmail.com> - 2.78.0-2
- Rebuild (podofo)

* Fri Jan 27 2017 Kevin Fenzi <kevin@scrye.com> - 2.78.0-1
- Update to 2.78.0. Fixes bug #1409216

* Sun Jan 01 2017 Rex Dieter <rdieter@math.unl.edu> - 2.76.0-2
- rebuild (sip)

* Fri Dec 30 2016 Kevin Fenzi <kevin@scrye.com> - 2.76.0-1
- Update to 2.76.0.

* Sun Dec 25 2016 Kevin Fenzi <kevin@scrye.com> - 2.75.1-1
- Update to 2.75.1. Fixes bug #1408585

* Fri Dec 23 2016 Kevin Fenzi <kevin@scrye.com> - 2.75.0-1
- Update to 2.75.0. Fixes bug #1408440

* Fri Dec 09 2016 Jon Ciesla <limburgher@gmail.com> - 2.74.0-1
- 2.74.0

* Fri Nov 25 2016 Kevin Fenzi <kevin@scrye.com> - 2.73.0-1
- Update to 2.73.0. Fixes bug #1396680

* Mon Oct 31 2016 Kevin Fenzi <kevin@scrye.com> - 2.71.0-1
- Update to 2.71.0. Fixes bug #1390174

* Sat Oct 15 2016 Kevin Fenzi <kevin@scrye.com> - 2.70.0-1
- Update to 2.70.0. Fixes bug #1385274

* Fri Sep 30 2016 Kevin Fenzi <kevin@scrye.com> - 2.69.0-1
- Update to 2.69.0. Fixes bugs #1380712 and #1379156

* Fri Sep 23 2016 Jon Ciesla <limburgher@gmail.com> - 2.68.0-2
- podofo rebuild.

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 2.68.0-1
- Update to 2.68.0. Fixes bug #1376793

* Thu Sep 08 2016 Kevin Fenzi <kevin@scrye.com> - 2.67.0-1
- Update to 2.67.0. Fixes bug #1374303

* Fri Sep 02 2016 Kevin Fenzi <kevin@scrye.com> - 2.66.0-1
- Update to 2.66.0. Fixes bug #1372696

* Fri Aug 26 2016 Kevin Fenzi <kevin@scrye.com> - 2.65.1-1
- Update to 2.65.1. Fixes bug #1370676

* Sun Aug 14 2016 Kevin Fenzi <kevin@scrye.com> - 2.64.0-1
- Update to 2.64.0. Fixes bug #1366588

* Mon Aug 08 2016 Kevin Fenzi <kevin@scrye.com> - 2.63.0-2
- Rebuild for qt5

* Sat Jul 23 2016 Kevin Fenzi <kevin@scrye.com> - 2.63.0-1
- Update to 2.63.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.62.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.62.0-2
- rebuild (qt5)

* Sat Jul 09 2016 Kevin Fenzi <kevin@scrye.com> - 2.62.0-1
- Update to 2.62. Fixes bug #1354088

* Mon Jul 04 2016 Kevin Fenzi <kevin@scrye.com> - 2.61.0-1
- Update to 2.61. Fixes bug #1351380

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.60.0-2
- rebuild (qt5)

* Fri Jun 24 2016 Kevin Fenzi <kevin@scrye.com> - 2.60.0-1
- Update to 2.60.0. Fixes bug #1349870
- Fix Requires. Fixes bug #1347961

* Sat Jun 18 2016 Kevin Fenzi <kevin@scrye.com> - 2.59.0-1
- Update to 2.59.0. Fixes bug #1347688

* Fri Jun 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.58.0-2
- rebuild (qt5-qtbase)

* Fri Jun 03 2016 Kevin Fenzi <kevin@scrye.com> - 2.58.0-1
- Update to 2.58.0. Fixes bug #1342516

* Sat May 21 2016 Kevin Fenzi <kevin@scrye.com> - 2.57.1-1
- Update to 2.57.1. Fixes bug #1338386

* Fri Apr 29 2016 Kevin Fenzi <kevin@scrye.com> - 2.56.0-1
- Update to 2.56.0. Fixes bug #1331734

* Tue Apr 26 2016 Kevin Fenzi <kevin@scrye.com> - 2.55.0-5
- Rebuild again for qt oddness. Fixes bug #1330750

* Wed Apr 20 2016 Kevin Fenzi <kevin@scrye.com> - 2.55.0-4
- Rebuild again for libicu

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.55.0-3
- BR: qt5-qtbase-private-devel

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2.55.0-2
- rebuild for ICU 57.1

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

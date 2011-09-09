%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           calibre
Version:        0.8.18
Release:        1%{?dist}
Summary:        E-book converter and library management
Group:          Applications/Multimedia
License:        GPLv3
URL:            http://calibre-ebook.com/

# SourceURL: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

# Upstream packages some unfree fonts which we cannot redistribute.
# While we're at it, also delete the liberation fonts which we already have.
#
# Download the upstream tarball and invoke this script while in the tarball's
# directory:
# ./generate-tarball.sh %{version}
Source0:        %{name}-%{version}-nofonts.tar.xz
Source1:        generate-tarball.sh
Source2:        calibre-mount-helper
Patch0:         %{name}-manpages.patch
Patch1:         %{name}-no-update.patch
Patch3:         calibre-0.8.10-poppler.patch
Patch4:		calibre-0.8.18-poppler-0.17.3.patch

BuildRequires:  python >= 2.6
BuildRequires:  python-devel >= 2.6
BuildRequires:  ImageMagick-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  qt-devel 
BuildRequires:  PyQt4-devel
BuildRequires:  poppler-qt4-devel >= 0.12
BuildRequires:  podofo-devel
BuildRequires:  desktop-file-utils
BuildRequires:  python-mechanize
BuildRequires:  python-lxml
BuildRequires:  python-dateutil
BuildRequires:  python-imaging
BuildRequires:  xdg-utils
BuildRequires:  python-BeautifulSoup
BuildRequires:  chmlib-devel
BuildRequires:  python-cssutils > 0.9.6
BuildRequires:  sqlite-devel
BuildRequires:  libicu-devel

Requires:       PyQt4
Requires:       pyPdf
Requires:       python-cherrypy
Requires:       python-cssutils
Requires:       ImageMagick
Requires:       odfpy
Requires:       django-tagging
Requires:       python-lxml
Requires:       python-imaging
Requires:       python-mechanize
Requires:       python-dateutil
Requires:       python-genshi
Requires:       python-BeautifulSoup
# Require the packages of the files which are symlinked by calibre
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts
Requires:       liberation-mono-fonts
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%define __provides_exclude_from ^%{_libdir}/%{name}/%{name}/plugins/.*\.so$


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
%setup -q -n %{name}

# don't append calibre1 to the name of the manpages. No need to compress either
# upstream won't fix: http://bugs.calibre-ebook.com/ticket/3770#comment:7
%patch0 -p1 -b .manpages

# don't check for new upstream version (that's what packagers do)
%patch1 -p1 -b .no-update

# work with poppler 0.17
%patch3 -p1 -b .poppler-fix

# fix for poppler 0.17.3
%patch4 -p1 -b .poppler-0.17.3

# dos2unix newline conversion
%{__sed} -i 's/\r//' src/calibre/web/feeds/recipes/*

# remove shebangs
%{__sed} -i -e '/^#!\//, 1d' src/calibre/*/*/*/*.py
%{__sed} -i -e '/^#!\//, 1d' src/calibre/*/*/*.py
%{__sed} -i -e '/^#![ ]*\//, 1d' src/calibre/*/*.py
%{__sed} -i -e '/^#!\//, 1d' src/calibre/*.py
%{__sed} -i -e '/^#!\//, 1d' src/templite/*.py
%{__sed} -i -e '/^#!\//, 1d' resources/default_tweaks.py
%{__sed} -i -e '/^#!\//, 1d' resources/catalog/section_list_templates.py

%{__chmod} -x src/calibre/*/*/*/*.py
%{__chmod} -x src/calibre/*/*/*.py
%{__chmod} -x src/calibre/*/*.py
%{__chmod} -x src/calibre/*.py

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

# create directory for calibre environment module
# the install script assumes it's there.
mkdir -p %{buildroot}%{python_sitelib}

XDG_DATA_DIRS="%{buildroot}%{_datadir}" \
XDG_UTILS_INSTALL_MODE="system" \
LIBPATH="%{_libdir}" \
python setup.py install --root=%{buildroot}%{_prefix} \
                        --prefix=%{_prefix} \
                        --libdir=%{_libdir} \
                        --staging-libdir=%{buildroot}%{_libdir} \
# remove shebang from init_calibre.py here because
# it just got spawned by the install script
%{__sed} -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/init_calibre.py
                        
# icons
mkdir -p %{buildroot}%{_datadir}/pixmaps/
cp -p resources/images/library.png                \
   %{buildroot}%{_datadir}/pixmaps/%{name}-gui.png
cp -p resources/images/viewer.png                 \
   %{buildroot}%{_datadir}/pixmaps/calibre-viewer.png

# every file is empty here
find %{buildroot}%{_datadir}/mime -maxdepth 1 -type f|xargs rm -f 

# packages aren't allowed to register mimetypes like this
rm -f %{buildroot}%{_datadir}/applications/defaults.list
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-ebook-viewer.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-gui.desktop
desktop-file-validate \
%{buildroot}%{_datadir}/applications/calibre-lrfviewer.desktop


mv %{buildroot}%{_datadir}/mime/packages/calibre-mimetypes \
   %{buildroot}%{_datadir}/mime/packages/calibre-mimetypes.xml

# mimetype icon for lrf
rm -rf %{buildroot}%{_datadir}/icons/hicolor/128x128
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -p resources/images/mimetypes/lrf.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/application-x-sony-bbeb.png
cp -p resources/images/viewer.png \
      %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/calibre-viewer.png

# don't put bash completions in /usr/etc
mv %{buildroot}%{_prefix}%{_sysconfdir} %{buildroot}

# these are provided as separate packages
rm -rf %{buildroot}%{_libdir}/%{name}/{odf,cherrypy,pyPdf,encutils,cssutils}
rm -rf %{buildroot}%{_libdir}/%{name}/cal/utils/genshi
rm -rf %{buildroot}%{_libdir}/%{name}/cal/trac

# link to system fonts after we have deleted (see Source0) the non-free ones
# http://bugs.calibre-ebook.com/ticket/3832
ln -s %{_datadir}/fonts/liberation/LiberationSans-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/prs500/tt0003m_.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSerif-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/prs500/tt0011m_.ttf
ln -s %{_datadir}/fonts/liberation/LiberationMono-Regular.ttf \
      %{buildroot}%{_datadir}/%{name}/fonts/prs500/tt0419m_.ttf

# http://bugs.calibre-ebook.com/ticket/3770#comment:7
# man pages
mv %{buildroot}%{_datadir}/%{name}/man %{buildroot}%{_mandir}

# delete locales, calibre stores them in a zip file now
rm -rf %{buildroot}%{_datadir}/%{name}/localization/locales/

%{__rm} -f %{buildroot}%{_bindir}/%{name}-uninstall   

install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/calibre-mount-helper

%post
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
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
%{_bindir}/epub-fix
%{_bindir}/fetch-ebook-metadata
%{_bindir}/lrf2lrs
%{_bindir}/lrfviewer
%{_bindir}/lrs2lrf
%{_bindir}/markdown-calibre
%{_bindir}/pdfmanipulate
%{_bindir}/web2disk
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%{_datadir}/icons/hicolor/scalable/apps/*
%{python_sitelib}/init_calibre.py*
%{_mandir}/man1/*

%changelog
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

* Sun Apr 16 2011 Kevin Fenzi <kevin@tummy.com> - 0.7.56-1
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

* Fri Oct 30 2010 Kevin Fenzi <kevin@tummy.com> - 0.7.26-1
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

Name: kdebase-runtime
Summary: KDE Runtime
Version: 4.3.4
Release: 9%{?dist}

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv2+
Group: User Interface/Desktops
URL: http://www.kde.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdebase-runtime-%{version}.tar.bz2
Source1: khelpcenter.desktop

# make PulseAudio the global default
Patch0: kdebase-runtime-4.1.70-pulseaudio.patch

# add shortcuts for search provider
Patch1: kdebase-runtime-4.1.x-searchproviders-shortcuts.patch

# make knetattach only show in KDE
Patch2: kdebase-runtime-4.2.85-knetattach.patch

# make icontheme inherit working
Patch3: kdebase-runtime-4.1.1-iconthemes-inherit.patch

# add autostart-condition
Patch4: kdebase-runtime-4.3.0-nepomuk-autostart.patch

# use manpath binary if available to construct the man path
Patch5: kdebase-runtime-4.3.1-manpath.patch

# add OnlyShowIn=KDE  to Desktop/Home.desktop (like trash.desktop)
Patch6: kdebase-runtime-4.3.3-home_onlyshowin_kde.patch

# disable webkit
Patch7: kdebase-runtime-4.3.4-webkit.patch

# Upstream patches 4.3
Patch100: kdebase-runtime-4.3-startmenu.patch
Patch101: kdebase-runtime-4.3.5.patch
Patch102: kdebase-runtime-4.3.4-kde#210463.patch

# Upstream patches 4.4

# security fixes

Provides: kdebase4-runtime = %{version}-%{release}
Obsoletes: kdebase4-runtime < %{version}-%{release}

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
%ifnarch s390 s390x
Requires: eject
%endif
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: htdig
Requires: oxygen-icon-theme >= %{version}
Requires: hal-storage-addon

BuildRequires: kde-filesystem
BuildRequires: alsa-lib-devel
BuildRequires: bzip2-devel
BuildRequires: clucene-core-devel
BuildRequires: hal-devel
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdelibs-experimental-devel
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: libsmbclient-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: OpenEXR-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: pulseaudio-libs-devel
BuildRequires: qimageblitz-devel
BuildRequires: soprano-devel >= 2.3.0
BuildRequires: xorg-x11-font-utils
BuildRequires: xorg-x11-proto-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
Core runtime for the KDE 4.


%package libs
Summary: Runtime libraries for %{name}
Group: System Environment/Libraries
Requires: kdelibs4%{?_isa} >= %{version}
Requires: kdepimlibs%{?_isa} >= %{version}
Requires: %{name} = %{version}-%{release}

%description libs
%{summary}.


%prep
%setup -q

%patch0 -p1 -b .pulseaudio
%patch1 -p1 -b .searchproviders-shortcuts
%patch2 -p1 -b .knetattach
%patch3 -p1 -b .iconthemes-inherit
%patch4 -p1 -b .nepomuk-autostart
#patch5 -p1 -b .manpath
%patch6 -p1 -b .home_onlyshowin_kde
%patch7 -p1 -b .nowebkit

%patch100 -p1 -b .startmenu
%patch101 -p1 -b .kde435
%patch102 -p1 -b .kde#210463

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# kdesu symlink
ln -s %{_kde4_libexecdir}/kdesu %{buildroot}%{_kde4_bindir}/kdesu

# omit hicolor index.theme, use one from hicolor-icon-theme
rm -f %{buildroot}%{_kde4_iconsdir}/hicolor/index.theme

# remove country flags because some people/countries forbid some other
# people/countries' flags :-(
rm -f %{buildroot}%{_kde4_datadir}/locale/l10n/*/flag.png

# install this service for KDE 3 applications
# NOTE: This is not a standard .desktop file, but an "almost standard" one
#       installed into a KDE-3-specific directory, as usual for KDE 3 services,
#       so we can't use desktop-file-install for it.
install -p -D %{SOURCE1} %{buildroot}%{_datadir}/services/khelpcenter.desktop

# FIXME: -devel type files, omit for now
rm -vf  %{buildroot}%{_kde4_libdir}/lib{kwalletbackend,molletnetwork}.so


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime &> /dev/null

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
    touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
    gtk-update-icon-cache %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
    gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
    update-desktop-database -q &> /dev/null ||:
    update-mime-database %{_kde4_datadir}/mime &> /dev/null
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_kde4_bindir}/*
%{_kde4_appsdir}/*
%{_kde4_configdir}/*.knsrc
%{_kde4_datadir}/autostart/nepomukserver.desktop
%{_kde4_datadir}/config.kcfg/
%{_datadir}/dbus-1/interfaces/*
%{_datadir}/dbus-1/services/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/mime/packages/network.xml
%{_kde4_datadir}/sounds/*
%{_kde4_iconsdir}/default.kde4
%{_kde4_libdir}/kconf_update_bin/*
%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libdir}/kde4/kcm_*.so
%{_kde4_libdir}/kde4/kded_*.so
%{_kde4_libexecdir}/*
%{_libdir}/strigi/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_docdir}/HTML/en/*
%{_kde4_sysconfdir}/xdg/menus/kde-information.menu
%{_kde4_datadir}/applications/kde4/Help.desktop
%{_kde4_datadir}/applications/kde4/knetattach.desktop
%{_kde4_configdir}/kshorturifilterrc
%{_kde4_datadir}/desktop-directories/*.directory
%{_kde4_datadir}/emoticons/kde4/
%{_kde4_datadir}/locale/en_US/entry.desktop
%{_kde4_datadir}/locale/l10n/
%{_datadir}/services/khelpcenter.desktop

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/libkwalletbackend.so.*
%{_kde4_libdir}/libmolletnetwork.so.*
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/kde4/plugins/phonon_platform/
%{_kde4_libdir}/kde4/plugins/styles/

%changelog
* Thu Jun 24 2010 Than Ngo <than@redhat.com> - 4.3.4-9
- Resolves: bz#607100, Requires: hal-storage-addon 
- Resolves: bz#597271, drop WebKit support in Qt

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 4.3.4-7
- rebuilt against qt 4.6.2

* Mon Jan 25 2010 Than Ngo <than@redhat.com> - 4.3.4-6
- backport patch from stable branch
  fix kde#210463, Don't watch subdirs for changes unless they've been listed.

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 4.3.4-5
- backport 4.3.5 fixes

* Mon Dec 21 2009 Than Ngo <than@redhat.com> - 4.3.4-4
- Repositioning the KDE Brand
- add kde to the user startmenu instead of the global one
- cleanup

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.4-2
- phonon/pulseaudio patch from mandriva, kudos to coling (f12)

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Sat Nov 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-5
- disable manpath patch for now, does more harm than good (#532071)

* Fri Nov 13 2009 Than Ngo <than@redhat.com> - 4.3.3-4
- rhel cleanup, fix conditional for RHEL

* Wed Nov 11 2009 Than Ngo <than@redhat.com> - 4.3.3-3
- rhel cleanup, drop BR on openslp-devel

* Thu Nov 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-2
- add OnlyShowIn=KDE to Desktop/Home.desktop (like trash.desktop)

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-1
- 4.3.3

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.2-4
- Conflicts: kdebase4 < 4.3.0 instead 

* Wed Oct 14 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.2-3
- Conflicts: kdebase < 6:4.3.0
- Requires: oxygen-icon-theme >= %%{version}

* Tue Oct 06 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.2-2
- BR: bzip2-devel xz-devel
- -libs: move Requires: kdepimlibs... here

* Sun Oct 04 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Wed Sep 30 2009 Nils Philippsen <nils@redhat.com> - 4.3.1-4
- fix manpath patch (spotted by Kevin Kofler)

* Wed Sep 30 2009 Nils Philippsen <nils@redhat.com> - 4.3.1-3
- if available, use the "manpath" command in the man kioslave to determine man
  page file locations

* Tue Sep 15 2009 Rex Dieter <rdieter@fedorproject.org> - 4.3.1-2
- restore some previously inadvertantly omitted nepomuk ontologies

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Wed Aug 12 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0-4
- unbreak fish kioslave protocol (#516416)

* Mon Aug 10 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0-3
- fix Oxygen comboboxes' text being garbled (drawn twice); fixes kdebug:202701
- fix Locale control module crashing when dragging languages around (kdebug:201578)

* Tue Aug 04 2009 Than Ngo <than@redhat.com> - 4.3.0-2
- respin

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-2
- respin (soprano-2.3.0) 
- License: LGPLv2+

* Thu Jul 09 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Thu Jul 02 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.95-3
- drop unneeded BR: ImageMagick (#509241)

* Mon Jun 29 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.95-2
- don't start nepomuk server unconditionally (#487322)

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Tue Jun 02 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.85-3
- Drop old Fedora < 8 conditionals

* Tue May 19 2009 Than Ngo <than@redhat.com> - 4.2.85-2
- file conflicts with kdepim

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Thu Apr 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-4
- fix persistent systray notifications (#485796)

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-3
- -flags subpkg
- koji/noarch hacks dropped

* Wed Apr 01 2009 Than Ngo <than@redhat.com> - 4.2.2-2
- drop kdebase-runtime-4.2.1-pulseaudio-cmake.patch

* Mon Mar 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Mar 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-3
- flags subpkg (not enabled)
- optimize scriptlets

* Tue Mar  3 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.1-2
- fix PulseAudio cmake detection

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.0-7
- #486059 -  missing dependency on htdig

* Thu Feb 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-6
- -libs: include %%{_kde4_libdir}/libkwalletbackend.so.* here

* Thu Feb 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-5
- Req: %%{name}-libs%%{?_isa} for multilib sanity (#456926)

* Mon Feb 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-4
- own %%_kde4_datadir/locale/l10n/

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-3
- respun tarball

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-2
- Files not trashed to the correct location in Dolphin/Konqueror
  (#481598, kdebug#178479)
- omit --with-samba crud

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0
- +BR: pulseaudio-libs-devel xine-lib-devel
- -BR: giflib-devel pcre-devel

* Tue Jan 13 2009 Rex Dieter <rdieter@fedoraproject.org> 4.1.96-2
- tarball respin
- drop extraneous deps (that are in kdelibs)

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Mon Dec 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.85-2
- include %%_bindir/kdesu symlink

* Thu Dec 11 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-5
- don't ship libkwalletbackend.so devel symlink (conflicts with kdelibs3-devel,
  and should be in a -devel package if it gets shipped)

* Thu Nov 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-4
- BR strigi-devel >= 0.5.11.1 because 0.5.11 is broken

* Thu Nov 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-3
- readd still relevant part of the Phonon PulseAudio patch (for the KCM)

* Wed Nov 19 2008 Than Ngo <than@redhat.com> 4.1.80-2
- drop kdebase-runtime-4.0.72-pulseaudio.patch/icons, it's part of phonon

* Fri Nov 19 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.1.80-1
- 4.1.80
- Drop upstreamed patch kdebase-runtime-4.1.2-kioexec.patch
- BR cmake >= 2.6.2
- Use 'make install/fast'
- Drop subpkg phonon-backend-xine and related file entries: this has to be
  part of phonon now that it moved there
- Drop xine-lib-devel BR
- Add libkwalletbackend to files list
- Drop _default_patch_fuzz 2

* Thu Nov 13 2008 Than Ngo <than@redhat.com> 4.1.3-5
- apply upstream patch to fix X crash when disabling compositing

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Tue Oct 14 2008 Than Ngo <than@redhat.com> 4.1.2-5
- apply upstream patch, kioexec processes never terminate

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.1.2-4
- fix broken audio-backend-jack.svgz

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.1.2-3
- add missing icons

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem
- grow -libs, kde4 styles are unavailable for i386 applications (#456826)

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org. 4.1.2-1
- 4.1.2

* Tue Sep 16 2008 Than Ngo <than@redhat.com> 4.1.1-3
- fix inherit issue in iconthemes, preview icons
  do not show

* Mon Sep 01 2008 Than Ngo <than@redhat.com> 4.1.1-2
- fix #460710, knetattach is kio_remote's wizard program, don't show
  it in the menu.

* Thu Aug 28 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Aug 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-3
- fix PA not being default in the Xine backend (KCM part, see phonon-4.2.0-4)

* Tue Aug 12 2008 Than Ngo <than@redhat.com> 4.1.0-2
- crash fix when stopping a service that is not yet initialized

* Fri Jul 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-1.1
- don't remove autostart directory on F8- (does not conflict, fixes build
  failure due to nepomukserver.desktop listed in filelist but not found)

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-2
- phonon-backend-xine: drop Obsoletes/Requires upgrade hack

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-4
- respin

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-3
- -phonon-backend-xine: new subpkg

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Thu Jun 05 2008 Than Ngo <than@redhat.com> 4.0.80-2
- add searchproviders-shortcuts for redhat bugzilla

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta 1

* Tue May 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-2
- BR new minimum version of soprano-devel

* Tue May 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72 (4.1 alpha 1)
- drop upstreamed deinterlace-crash patch
- drop khelpcenter patch (fixed upstream)
- update Phonon PulseAudio patch
- drop Fedora 7 support
- update file list

* Mon Apr 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-10.1
- omit conflicting icons (kde3_desktop=1 case)

* Thu Apr 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-10
- oxygen-icon-theme: build noarch

* Thu Apr 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-9
- %%post/%%postun: hicolor icon theme scriptlets

* Thu Apr 17 2008 Than Ngo <than@redhat.com> 4.0.3-8
- only omit hicolor index.theme (#439374)

* Thu Apr 17 2008 Than Ngo <than@redhat.com> 4.0.3-7
- fix khelpcenter, search plugins/settings in correct path (#443016)

* Tue Apr 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-6
- respin (at f13's request)

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-5
- pulseaudio patch (use as default, if available)

* Sat Apr 05 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-4
- don't crash if we don't have deinterlacing support in xine-lib (#440299)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild for the new %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- update file list for _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-5
- don't own %%_kde4_docdir/HTML/en/

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-4
- oxygen-icon-theme, oxygen-icon-theme-scalable pkgs
- include noarch build hooks (not enabled)

* Fri Mar 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-3
- BR libxcb-devel everywhere (including F7)

* Fri Mar 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-2
- if building for a KDE 4 desktop, include the khelpcenter.desktop service
  description for KDE 3 here so help works in KDE 3 apps

* Fri Feb 29 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Mon Feb 25 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-3
- %%files: don't own %%_kde4_libdir/kde4/plugins (thanks wolfy!)

* Sat Feb 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-2
- reenable kio_smb everywhere (including F9) now that we have a GPLv3 qt4
  (kio_smb itself is already GPLv2+)

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- 4.0.1

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0.0-2
- respun tarball

* Mon Jan 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.0-1
- update to 4.0.0
- update file list, don't remove renamed khotnewstuff.knsrc for KDE 3 desktop

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-1
- kde-3.97.0

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.2-4
- disable kioslave/smb (f9+, samba-3.2.x/gplv3 ickiness)

* Sun Dec 02 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.96.2-3
- build without libxcb in F7 as we STILL don't have it (see #373361)

* Sat Dec 01 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.96.2-2
- no longer set kde3_desktop on F9
- update file list for !kde3_desktop (Sebastian Vahl)
- don't ship country flags even for full version (as in kdebase 3)

* Thu Nov 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.2-1
- kde-3.96.2

* Tue Nov 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.1-1
- kde-3.96.1

* Sun Nov 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.0-3
- fix %%files (unpackaged %%_libdir/strigi/strigiindex_sopranobackend.so)

* Sat Nov 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.0-2
- BR: clucene-core-devel libsmbclient-devel libXScrnSaver-devel

* Thu Nov 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.96.0-1
- kde-3.96.0

* Fri Nov 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.95.2-1
- kdebase-runtime-3.95.2

* Wed Nov 07 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.95.0-1
- kdebase-runtime-3.95.0

* Fri Nov 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.94.0-3
- Provides: oxygen-icon-theme ...

* Thu Oct 25 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.94.0-2
- patch dolphin.desktop to get Dolphin to start from the menu

* Fri Oct 19 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.94.0-1
- update to 3.94.0

* Thu Oct 4 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.93.0-5
- don't make this the default kdebase on F9 yet
- drop ExcludeArch: ppc64 (#300601)

* Fri Sep 21 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.93.0-4
- ExcludeArch: ppc64 (#300601)
- update description

* Thu Sep 13 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.93.0-3
- add missing BR alsa-lib-devel

* Wed Sep 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.93.0-2
- remove files which conflict with KDE 3
- move devel symlinks to %%{_kde4_libdir}/kde4/devel/
- Conflicts with KDE 3 versions of dolphin pre d3lphin rename

* Wed Sep 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.93.0-1
- update to 3.93.0
- drop kde4home patch (no longer applied)
- drop KDM ConsoleKit patch (KDM is now in kdebase-workspace)
- remove kdebase-kdm Obsoletes/Provides (for the same reason)
- remove KDM (and KDM session) setup code (for the same reason)
- remove rss-glx conflict (Plasma is now in kdebase-workspace)
- remove redhat-startkde patch (startkde is now in kdebase-workspace)
- remove kde4-opt.sh (all the code in it is commented out)
- remove kde4-xdg_menu_prefix.sh (only needed for kdebase-workspace)
- remove bogus BRs on automake and libtool
- remove workspace-only BRs
- add BR qimageblitz-devel, xine-lib-devel (all), libxcb-devel (F8+)
- remove workspace files and directories
- handle icons (moved from kdelibs4)
- add mkdir %%{buildroot} in %%install

* Tue Aug 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92.0-4
- use macros.kde4
- License: GPLv2

* Mon Jul 30 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.92.0-3
- bump rss-glx Conflicts because the conflict is still there in 0.8.1.p-7.fc8
- rss-glx conflict only needed if "%%{_prefix}" == "/usr"
- consolekit_kdm patch only needs BR dbus-devel, not ConsoleKit-devel

* Mon Jul 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92.0-2
- consolekit_kdm patch (#228111, kde#147790)
- update startkde patch

* Sat Jul 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.92.0-1
- kde-3.92 (kde-4-beta1)

* Wed Jul 25 2007 Than Ngo <than@redhat.com> - 3.91.0-6
- fix startkde
- add env/shutdown directory

* Thu Jul 19 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.91.0-5
- kde4.desktop: fix session Name

* Tue Jul 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.91.0-4
- cleanup/fix kde4.desktop
- kdepimlibs4->kdepimlibs

* Thu Jun 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.91.0-3
- fix %%_sysconfdir for %%_prefix != /usr case.

* Thu Jun 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.91.0-2
- updated kde4home.diff
- CMAKE_BUILD_TYPE=RelWithDebInfo (we're already using %%optflags)

* Wed Jun 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.91.0-1
- kde-3.91.0
- CMAKE_BUILD_TYPE=debug

* Sat Jun 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.90.1-2
- specfile cleanup (%%prefix issues mostly)

* Sun May 13 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.90.1-1
- update to 3.90.1
- bump cmake BR to 2.4.5 as required upstream now
- don't set execute bits by hand anymore, cmake has been fixed
- use multilibs in /opt/kde4
- add BR openssl-devel, NetworkManager-devel, bluez-libs-devel
- add explicit BRs on strigi-devel, zlib-devel, bzip2-devel, libpng-devel
  in case we want to drop the Rs on these from kdelibs4-devel
- consistently add all BRs as -devel Rs, not just almost all, until we can
  figure out which, if any, are really needed
- BR libsmbclient-devel instead of samba on F>=7, EL>=6

* Fri Mar 23 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.80.3-4
- restore minimum version requirement for cmake
- build against libxklavier on EL5
- don't set QT4DIR and PATH anymore, qdbuscpp2xml has been fixed

* Mon Mar 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.80.3-3
- +eXecute perms for %%{_prefix}/lib/*

* Fri Feb 23 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.80.3-2
- rebuild for patched FindKDE4Internal.cmake

* Wed Feb 21 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.80.3-1
- update to 3.80.3
- update and improve parallel-installability patch
- drop obsolete joydevice.h patch
- remove translations of "KDE" without the "4" from kde4.desktop
- resync BR and -devel Requires
- don't set LD_LIBRARY_PATH
- set QT4DIR and PATH so CMake's direct $QT4DIR/qdbuscpp2xml calls work
- fix missing underscore in _datadir
- install kde4.desktop in install, not prep
- fix invalid syntax in kde4.desktop

* Wed Nov 29 2006 Chitlesh Goorah <chitlesh [AT] fedoraproject DOT org> 3.80.2-0.3.20061003svn
- dropped -DCMAKE_SKIP_RPATH=TRUE from cmake
- compiling with QA_RPATHS=0x0003; export QA_RPATHS

* Sun Nov 26 2006 Chitlesh Goorah <chitlesh [AT] fedoraproject DOT org> 3.80.2-0.2.20061003svn
- parallel build support
- added -DCMAKE_SKIP_RPATH=TRUE to cmake to skip rpath
- dropped qt4-devel >= 4.2.0, kdelibs4-devel as BR
- spec file cleanups and added clean up in %%install
- fixed PATH for libkdecore.so.5; cannot open shared object file;
- added Logitech mouse support
- added dbus-devel, hal-devel and more as BR
- fixed broken joydevice.h - Kevin Kofler
- added file kde4.desktop

* Sun Oct 08 2006 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.80.2-0.1.20061003svn
- first Fedora RPM (parts borrowed from the OpenSUSE kdebase 4 RPM and the Fedora kdebase 3 RPM)
- apply parallel-installability patch

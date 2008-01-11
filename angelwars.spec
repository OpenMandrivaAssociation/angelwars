%define	name	angelwars
%define	version	0.24
%define release	%mkrel 11
%define Summary	Fast-paced, old-fashioned side-scrolling space shooter

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.sourceforge.net/angel-wars/%{name}-%{version}.tar.bz2
Source1:	http://download.sourceforge.net/angel-wars/%{name}-media-%{version}.tar.bz2
Source2:	http://download.sourceforge.net/angel-wars/%{name}-docs-%{version}.tar.bz2
Source3:	http://download.sourceforge.net/angel-wars/%{name}-levels-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		%{name}-gcc32.fix.patch.bz2
Patch1:		%{name}-missing-zlib-flag.patch.bz2
License:	Artistic
Url:		http://angel-wars.sourceforge.net/
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL-devel SDL_mixer-devel oggvorbis-devel
BuildRequires:	smpeg-devel png-devel jpeg-devel

%description
Angel Wars is a traditional "space shooter" with an unusual premise--the
player is a rebellious minion of Satan bent on taking the universe over
for himself. It is written in C++ and aims to be as object-oriented and
platform-independent as possible.

%prep
%setup -q -b1 -b2 -b3
%patch0 -p1
%patch1
# remove .xvpics directories
find . -type d -name .xvpics | xargs rm -rf

%build
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir}
perl -pi -e "s#images/#%{_gamesdatadir}/%{name}/images/#g" %{name}/*.cc
perl -pi -e "s#levels/#%{_gamesdatadir}/%{name}/levels/#g" %{name}/*.cc
perl -pi -e "s#sounds/#%{_gamesdatadir}/%{name}/sounds/#g" %{name}/*.cc
perl -pi -e "s#images/#%{_gamesdatadir}/%{name}/images/#g" %{name}/*/*.txt
perl -pi -e "s#levels/#%{_gamesdatadir}/%{name}/levels/#g" %{name}/*/*.txt
perl -pi -e "s#sounds/#%{_gamesdatadir}/%{name}/sounds/#g" %{name}/*/*.txt
#Really ugly workaround for lousy perl skills(this will be done in another way if I ever
#get the time and skillz;)
perl -pi -e "s#%{_gamesdatadir}/%{name}/images/%{_gamesdatadir}/%{name}#%{_gamesdatadir}/%{name}/images#g" %{name}/levels/*.txt

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT%{_gamesbindir} datadir=$RPM_BUILD_ROOT%{_gamesdatadir}
install -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -a %{name}/images $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -a %{name}/levels $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
cp -a %{name}/sounds $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Angel Wars
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc %{name}/docs/*
%{_gamesdatadir}/%{name}
%{_gamesbindir}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop


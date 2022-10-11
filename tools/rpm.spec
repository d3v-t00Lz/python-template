%global modname pytemplate
%global completions_dir %( pkg-config --variable=completionsdir bash-completions )

Name:           python3-%{modname}
Version:        0.0.1
Release:        1%{?dist}
Summary:        TODO
License:        MIT
URL:            https://pypi.io/project/%{modname}
Source0:        https://pypi.io/packages/source/d/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-shtab
BuildRequires:  python3-rpm-macros
# PT:GUI
BuildRequires:  desktop-file-utils
# PT:GUI

%?python_enable_dependency_generator

%description

TODO

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install
DESTDIR="%{buildroot}" COMPLETIONS_DIR="%{completions_dir}" MAN_DIR=%{_mandir}/man1 make install_linux

# PT:QT
touch %{buildroot}/%{_datadir}/applications/%{modname}_qt.desktop

desktop-file-install                                        \
    --set-name="%{modname}"                                 \
    --set-icon="%{modname}"                                 \
    --set-key="Exec" --set-value="%{modname}_qt %U"         \
    --add-category="Graphics"                               \
    --set-key="Type" --set-value="Application"              \
    --delete-original                                       \
    --dir=%{buildroot}%{_datadir}/applications              \
    %{buildroot}/%{_datadir}/applications/%{modname}_qt.desktop
# PT:QT

# PT:SDL2
touch %{buildroot}/%{_datadir}/applications/%{modname}_sdl2.desktop

desktop-file-install                                        \
    --set-name="%{modname}"                                 \
    --set-icon="%{modname}"                                 \
    --set-key="Exec" --set-value="%{modname}_sdl2 %U"       \
    --add-category="Graphics"                               \
    --set-key="Type" --set-value="Application"              \
    --delete-original                                       \
    --dir=%{buildroot}%{_datadir}/applications              \
    %{buildroot}/%{_datadir}/applications/%{modname}_sdl2.desktop
# PT:SDL2

%check
# Redundant of `make rpm`, and the target OS may not have all required
# packages available in the repos
#%{__python3} make test

%files -n python3-%{modname}
#%doc CHANGELOG
%license LICENSE
%attr(755, root, root) %{_bindir}/%{modname}*
%{python3_sitelib}/%{modname}*/
# PT:GUI
%{_datadir}/applications/%{modname}*.desktop
%{_datadir}/pixmaps/%{modname}.png
# PT:GUI
# PT:SYSTEMD
%{_unitdir}/%{modname}.service
# PT:SYSTEMD

# PT:CLI
%{_mandir}/man1/*
%{completions_dir}/*
# PT:CLI

%exclude %dir %{_bindir}
%exclude %dir /usr/lib

%changelog

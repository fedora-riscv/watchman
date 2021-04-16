# some Python tests are failing
# The following tests FAILED:
#          40 - CacheTest.future (Child aborted)
#         290 - test_py::tests.integration.test_site_spawn.TestSiteSpawn.test_failingSpawner (Failed)
#         292 - test_py::tests.integration.test_site_spawn.TestSiteSpawn.test_spawner (Failed)
# Errors while running CTest
%bcond_with tests

Name:           watchman
Version:        2021.04.12.00
Release:        1%{?dist}
Summary:        File alteration monitoring service

%global stripped_version %(echo %{version} | sed -r 's/\\.0([[:digit:]])/.\\1/g')

License:        ASL 2.0
URL:            https://facebook.github.io/%{name}/
Source0:        https://github.com/facebook/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        tmpfiles-%{name}.conf
Patch0:         %{name}-destdir.patch

# Folly is known not to work on big-endian CPUs
# TODO: file bz once this is approved
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  folly-devel
BuildRequires:  pcre-devel
# for %%{_tmpfilesdir}
BuildRequires:  systemd-rpm-macros

%description
Watchman exists to watch files and record when they actually change. It can also
trigger actions (such as rebuilding assets) when matching files change.


%package -n python3-py%{name}
Summary:        Python bindings for %{name}
License:        BSD and MIT
BuildRequires:  procps-ng
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
# watchman-diag shells out to ps
Requires:       procps-ng

%description -n python3-py%{name}
The python3-py%{name} package contains Python bindings for %{name}.


%prep
%autosetup -p1
# Fix pywatchman version.
sed -i "s|version=\"1.4.1\"|version=\"%{version}\"|" python/setup.py


%build
%cmake \
  -DINSTALL_WATCHMAN_STATE_DIR=ON
%cmake_build


%install
%cmake_install
mkdir -p %{buildroot}%{_tmpfilesdir}
cp -p %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf


%if %{with tests}
%check
%ctest
%endif


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md README.markdown
%attr(02777,root,root) %dir %{_var}/run/%{name}
%{_bindir}/%{name}
%{_tmpfilesdir}/%{name}.conf

%files -n python3-py%{name}
%license python/LICENSE
%{_bindir}/%{name}-*
%{python3_sitearch}/py%{name}
%{python3_sitearch}/py%{name}-%{stripped_version}-py%{python3_version}.egg-info


%changelog
* Fri Apr 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.04.12.00-1
- Update to 2021.04.12.00

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 2021.03.29.00-2
- Rebuilt for removed libstdc++ symbol (#1937698)

* Mon Mar 29 2021 Michel Alexandre Salim <michel@michel-slm.name> - 2021.03.29.00-1
- Update to 2021.03.29.00

* Wed Mar 24 2021 Michel Alexandre Salim <michel@michel-slm.name> - 2021.03.22.00-1
- Update to 2021.03.22.00

* Mon Mar 15 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.03.15.00-1
- Update to 2021.03.15.00

* Wed Feb 03 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.02.01.00-1
- Update to 2021.02.01.00

* Tue Jan 26 17:51:20 PST 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 2021.01.25.00-1
- Update to 2021.01.25.00

* Tue Dec 29 12:16:46 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.12.28.00-1
- Update to 2020.12.28.00

* Tue Dec 22 20:48:10 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.12.21.00-1
- Update to 2020.12.21.00

* Tue Dec  1 12:26:55 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-7
- Recreate state directory with tmpfiles (bz #1903141)

* Mon Nov 30 16:23:46 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-6
- Rebuild for folly-2020.11.30.00

* Mon Nov 23 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-5
- Rebuild for folly-2020.11.23.00

* Mon Nov 16 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-4
- Rebuild for folly-2020.11.16.00

* Thu Nov 12 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-3
- Also install Watchman's state directory

* Wed Nov 11 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-2
- Support enabling tests
- Add ExcludeArch on s390x for Folly dependency
- Rename Python subpackage
- Fix version number and licensing for Python subpackage
- Move Python scripts to the Python subpackage

* Tue Nov 10 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 2020.09.21.00-1
- Initial package

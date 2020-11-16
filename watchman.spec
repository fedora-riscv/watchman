# some Python tests are failing
# The following tests FAILED:
#          40 - CacheTest.future (Child aborted)
#         290 - test_py::tests.integration.test_site_spawn.TestSiteSpawn.test_failingSpawner (Failed)
#         292 - test_py::tests.integration.test_site_spawn.TestSiteSpawn.test_spawner (Failed)
# Errors while running CTest
%bcond_with tests

Name:           watchman
Version:        2020.09.21.00
Release:        4%{?dist}
Summary:        File alteration monitoring service

License:        ASL 2.0
URL:            https://facebook.github.io/%{name}/
Source0:        https://github.com/facebook/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-destdir.patch

# Folly is known not to work on big-endian CPUs
# TODO: file bz once this is approved
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  folly-devel
BuildRequires:  pcre-devel

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
sed -ie "s|version=\"1.4.1\"|version=\"%{version}\"|" python/setup.py


%build
%cmake \
  -DINSTALL_WATCHMAN_STATE_DIR=ON
%cmake_build


%install
%cmake_install


%if %{with tests}
%check
%ctest
%endif


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md README.markdown
%dir %{_var}/run/%{name}
%{_bindir}/%{name}

%files -n python3-py%{name}
%license python/LICENSE
%{_bindir}/%{name}-*
%{python3_sitearch}/py%{name}
%{python3_sitearch}/py%{name}-%{version}-py%{python3_version}.egg-info


%changelog
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

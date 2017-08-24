%global pylib_version 1.4.29

Name:           pytest
Version:        3.2.1
Release:        3%{?dist}
Summary:        Simple powerful testing with Python
License:        MIT
URL:            http://pytest.org
Source0:        https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

# The test in this specfile use pytest-timeout
# When building pytest for the first time with new Python version
# that is not possible as it depends on pytest
%bcond_without timeout

%bcond_without python2
%bcond_without python3
%bcond_without platform_python

BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-setuptools_scm
BuildRequires:  python2-py >= %{pylib_version}
BuildRequires:  %{_bindir}/sphinx-build
BuildRequires:  %{_bindir}/rst2html
BuildRequires:  python2-hypothesis
%if %{with timeout}
BuildRequires:  python2-pytest-timeout
%endif
BuildRequires:  python2-mock
BuildRequires:  python2-twisted
BuildRequires:  python2-jinja2
BuildRequires:  python2-nose
BuildRequires:  python2-argcomplete
BuildRequires:  python2-decorator
%endif

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-py >= %{pylib_version}
BuildRequires:  %{_bindir}/sphinx-build
BuildRequires:  %{_bindir}/rst2html
BuildRequires:  python3-hypothesis
%if %{with timeout}
BuildRequires:  python3-pytest-timeout
%endif
BuildRequires:  python3-mock
BuildRequires:  python3-twisted
BuildRequires:  python3-jinja2
BuildRequires:  python3-nose
BuildRequires:  python3-argcomplete
BuildRequires:  python3-decorator
%endif

%if %{with platform_python}
BuildRequires:  platform-python-devel
BuildRequires:  platform-python-setuptools
BuildRequires:  platform-python-setuptools_scm
BuildRequires:  platform-python-py >= %{pylib_version}
# doc requirements are skipped
# requirements for optional tests are skipped
BuildRequires:  platform-python-hypothesis
%endif


%description
py.test provides simple, yet powerful testing for Python.


%if %{with python2}
%package -n python2-%{name}
Summary:        Simple powerful testing with Python
Requires:       python2-setuptools
Requires:       python2-py >= %{pylib_version}
%{?python_provide:%python_provide python2-%{name}}
# the python2 package was named pytest up to 2.8.7-2
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < 2.8.7-3

%description -n python2-%{name}
py.test provides simple, yet powerful testing for Python.
%endif


%if %{with python3}
%package -n python3-%{name}
Summary:        Simple powerful testing with Python
Requires:       python3-setuptools
Requires:       python3-py >= %{pylib_version}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
py.test provides simple, yet powerful testing for Python.
%endif


%if %{with platform_python}
%package -n platform-python-%{name}
Summary:        Simple powerful testing with Python
Requires:       platform-python-setuptools
Requires:       platform-python-py >= %{pylib_version}

%description -n platform-python-%{name}
py.test provides simple, yet powerful testing for Python.
%endif


%prep
%setup -qc -n %{name}-%{version}
mv %{name}-%{version} python2
cp -a python2 python3
cp -a python2 platform-python


%build
%if %{with python2}
pushd python2
%{py2_build}
for l in doc/* ; do
  make -C $l html PYTHONPATH=$(pwd)
done
for f in README CHANGELOG CONTRIBUTING ; do
  rst2html ${f}.rst > ${f}.html
done
popd
%endif

%if %{with python3}
pushd python3
%{py3_build}
for l in doc/* ; do
  make -C $l html PYTHONPATH=$(pwd)
done
for f in README CHANGELOG CONTRIBUTING ; do
  rst2html ${f}.rst > ${f}.html
done
popd
%endif

%if %{with platform_python}
pushd platform-python
%{platform_py_build}
popd
%endif


%install
%if %{with python2}
pushd python2
%{py2_install}
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python2_version}
ln -snf pytest-%{python2_version} %{buildroot}%{_bindir}/pytest-2
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python2_version}
ln -snf py.test-%{python2_version} %{buildroot}%{_bindir}/py.test-2

mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done
popd

# remove shebangs from all scripts
find %{buildroot}%{python2_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;
%endif

%if %{with python3}
pushd python3
%{py3_install}
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest-%{python3_version}
ln -snf pytest-%{python3_version} %{buildroot}%{_bindir}/pytest-3
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test-%{python3_version}
ln -snf py.test-%{python3_version} %{buildroot}%{_bindir}/py.test-3

mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done
popd

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;
%endif

%if %{with platform_python}
pushd platform-python
%{platform_py_install}
rm %{buildroot}%{_bindir}/pytest
rm %{buildroot}%{_bindir}/py.test

# remove shebangs from all scripts
find %{buildroot}%{platform_python_sitelib} \
     -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;
%endif

%if %{with python2}
# use 2.X per default
ln -snf pytest-%{python2_version} %{buildroot}%{_bindir}/pytest
ln -snf py.test-%{python2_version} %{buildroot}%{_bindir}/py.test
%endif


%check
%if %{with python2}
pushd python2
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{buildroot}%{_bindir}/pytest-%{python2_version} -r s testing \
  %if %{with timeout}
  --timeout=20
  %endif

popd
%endif

%if %{with python3}
pushd python3
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/pytest-%{python3_version} -r s testing \
  %if %{with timeout}
  --timeout=20
  %endif

popd
%endif

%if %{with platform_python}
pushd platform-python
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{platform_python_sitelib} \
  %{__platform_python} -m pytest -r s testing

popd
%endif


%if %{with python2}
%files -n python2-%{name}
%doc python2/CHANGELOG.html
%doc python2/README.html
%doc python2/CONTRIBUTING.html
%doc python2/_htmldocs/html
%license python2/LICENSE
%{_bindir}/pytest
%{_bindir}/pytest-2
%{_bindir}/pytest-%{python2_version}
%{_bindir}/py.test
%{_bindir}/py.test-2
%{_bindir}/py.test-%{python2_version}
%{python2_sitelib}/*
%endif


%if %{with python3}
%files -n python3-%{name}
%doc python3/CHANGELOG.html
%doc python3/README.html
%doc python3/CONTRIBUTING.html
%doc python3/_htmldocs/html
%license python3/LICENSE
%{_bindir}/pytest-3
%{_bindir}/pytest-%{python3_version}
%{_bindir}/py.test-3
%{_bindir}/py.test-%{python3_version}
%{python3_sitelib}/*
%exclude %dir %{python3_sitelib}/__pycache__
%endif


%if %{with platform_python}
%files -n platform-python-%{name}
%doc platform-python/CHANGELOG.rst
%doc platform-python/README.rst
%doc platform-python/CONTRIBUTING.rst
%license platform-python/LICENSE
%{platform_python_sitelib}/*
%exclude %dir %{platform_python_sitelib}/__pycache__
%endif


%changelog
* Thu Aug 24 2017 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-3
- Rebuilt for rhbz#1484607

* Fri Aug 11 2017 Petr Viktorin <pviktori@redhat.com> - 3.2.1-2
- Add subpackage for platform-python (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Wed Aug  9 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.1-1
- Update to 3.2.1.

* Wed Aug 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.2.0-1
- 3.2.0.

* Sun Jul 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.3-1
- Update to 3.1.3.
- Update BRs.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun  3 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.1-1
- Update to 3.1.1.
- Add BR on setuptools_scm.

* Wed Mar 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.7-1
- Update to 3.0.7.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.6-1
- Update to 3.0.6.
- Drop patch applied upstream.

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.5-2
- Rebuild for Python 3.6

* Tue Dec  6 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.5-1
- Update to 3.0.5.

* Mon Nov 28 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.4-1
- Update to 3.0.4.

* Fri Sep 30 2016 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.
- Update requirements.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.2-1
- Update to 2.9.2.

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sat Apr  9 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.1-1
- Update to 2.9.1.
- Packaging updates.

* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-2
- Use new python macros
- Fix python3 package file ownership

* Sun Jan 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.7-1
- Update to 2.8.7.

* Fri Jan 22 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.6-1
- Update to 2.8.6.

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-1
- Update to 2.8.5

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-3
- Re-enable pexpect in tests

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.2-1
- Update to 2.8.2.

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 2.7.3-2
- Rebuilt for Python3.5 rebuild

* Thu Sep 17 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.3-1
- Update to 2.7.3.
- Provide additional symlinks to the pytest executables (rhbz#1249891).

* Mon Sep 14 2015 Orion Poplawski <orion@cora.nwra.com> - 2.7.2-2
- Provide python2-pytest, use python_provide macro

* Thu Jun 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.2-1
- Update to 2.7.2.
- Small fixes.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.1-1
- Update to 2.7.1.

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.0-1
- Update to 2.7.0.
- Apply updated Python packaging guidelines.
- Mark LICENSE with %%license.

* Tue Dec  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.4-1
- Update to 2.6.4.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.3-1
- Update to 2.6.3.

* Fri Aug  8 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.0-1
- Update to 2.6.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 2.5.2-2
- Redbuild for python 3.4

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-2
- Only run tests from the 'testing' subdir in %%check.

* Sat Oct  5 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-1
- Update to 2.4.2.
- Add buildroot's bindir to PATH while running the testsuite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-3
- Disable tests using pexpect for now, fails on F19.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-2
- Use python-sphinx for rhel > 6 (rhbz#973318).
- Update BR to use python-pexpect instead of pexpect.

* Sat May 25 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-1
- Update to 2.3.5.
- Docutils needed now to build README.html.
- Add some BR optionally used by the testsuite.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.4-1
- Update to 2.3.4.

* Sun Oct 28 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.2-1
- Update to 2.3.2.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Re-enable some tests, ignore others.
- Docs are available in English and Japanese now.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-4
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.
- Disable failing tests for Python3.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-1
- Update to 2.2.4.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.3-1
- Update to 2.2.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Tue Dec 13 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.

* Wed Oct 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.3-1
- Update to 2.1.3.

* Tue Sep 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-2
- Fix: python3 dependencies.

* Sun Aug 28 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-2
- Update Requires and BuildRequires tags.

* Tue Aug  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.

* Mon May 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Mar 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.2-1
- Update to 2.0.2.

* Sun Jan 16 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- New package.

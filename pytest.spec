%if (! 0%{?rhel}) || 0%{?rhel} > 6
%global with_python3 1
%endif
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           pytest
Version:        2.1.0
Release:        1%{?dist}
Summary:        Simple powerful testing with Python

Group:          Development/Languages
License:        MIT
URL:            http://pytest.org
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-py >= 1.4.1
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-py >= 1.4.1
%endif # with_python3
# pytest was separated from pylib at that point
Conflicts:      python-py < 1.4.0

%description
py.test provides simple, yet powerful testing for Python.


%if 0%{?with_python3}
%package -n python3-pytest
Summary:        Simple powerful testing with Python
Group:          Development/Languages


%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.
%endif # with_python3


%prep
%setup -q

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

make -C doc html PYTHONPATH=$(pwd)

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

popd
%endif # with_python3

# remove hidden file
rm doc/_build/html/.buildinfo

# use 2.X per default
pushd %{buildroot}%{_bindir}
ln -snf py.test-2.* py.test
popd


%clean
rm -rf %{buildroot}


%check
PYTHONPATH=%{buildroot}%{python_sitelib} \
  %{buildroot}%{_bindir}/py.test
%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/py.test-3.*
popd
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README.txt
%doc doc/_build/html
%{_bindir}/py.test
%{_bindir}/py.test-2.*
%{python_sitelib}/*


%if 0%{?with_python3}
%files -n python3-pytest
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README.txt
%doc doc/_build/html
%{_bindir}/py.test-3.*
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Tue Aug  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.

* Mon May 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Mar 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.2-1
- Update to 2.0.2.

* Sun Jan 16 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- New package.

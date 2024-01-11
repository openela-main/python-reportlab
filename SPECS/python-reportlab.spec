%global cmapdir %(echo `rpm -qls ghostscript | grep CMap | awk '{print $2}'`)
%global pypi reportlab

Name:           python-%{pypi}
Version:        3.4.0
Release:        8%{?dist}.2
Summary:        Library for generating PDFs and graphics
License:        BSD
URL:            http://www.reportlab.org/
Source0:        https://pypi.python.org/packages/source/r/%{pypi}/%{pypi}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=1769661
Patch0:         python-reportlab-3.4.0-color-eval.patch

# https://issues.redhat.com/browse/RHEL-7009
Patch1:         python-reportlab-3.4.0-invalid-char.patch
Patch2:         python-reportlab-3.4.0-unichar-element.patch

%package -n     python3-%{pypi}
Summary:        Library for generating PDFs and graphics
BuildRequires:  python3-devel
BuildRequires:  python3-pillow

Requires:       dejavu-sans-fonts
Requires:       python3-pillow
%{?python_provide:%python_provide python3-%{pypi}}

%description
This is the ReportLab PDF Toolkit. It allows rapid creation of rich PDF
documents, and also creation of charts in a variety of bitmap and vector
formats.

%description -n python3-%{pypi}
This is the ReportLab PDF Toolkit. It allows rapid creation of rich PDF 
documents, and also creation of charts in a variety of bitmap and vector 
formats.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       python3-%{pypi} = %{version}-%{release}
Obsoletes:      %{name}-docs < %{version}-%{release}

%description    doc                  
Contains the documentation for ReportLab.

%prep
%setup -qn reportlab-%{version}
%patch0 -p1 -b .color-eval
%patch1 -p1
%patch2 -p1 -b .unichar-element
# clean up hashbangs from libraries
find src -name '*.py' | xargs sed -i -e '/^#!\//d'
# patch the CMap path by adding Fedora ghostscript path before the match
sed -i '/\~\/\.local\/share\/fonts\/CMap/i''\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ '\'%{cmapdir}\''\,' src/reportlab/rl_settings.py
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
CFLAGS="%{optflags}" %py3_build

# a bit of a horrible hack due to a chicken-and-egg problem. The docs
# require reportlab, which isn't yet installed, but is at least built.
PYTHONPATH="`pwd`/`ls -d build/lib*`" %{__python3} docs/genAll.py

%install
%py3_install

# Remove bundled fonts
rm -rf %{buildroot}%{python3_sitearch}/reportlab/fonts

%check
# These tests actually fail because of the removed fonts
%{__python3} setup.py tests

%files -n python3-%{pypi}
%doc README.txt CHANGES.md 
%license LICENSE.txt
%{python3_sitearch}/reportlab/
%{python3_sitearch}/reportlab-%{version}-py%{python3_version}.egg-info

%files doc
%doc demos/ tools/
#%doc docs/*.pdf

%changelog
* Wed Sep 27 2023 Marek Kasik <mkasik@redhat.com> - 3.4.0-8.el8_9.2
- Rebuild for 8.9.0 y-branch
- Resolves: RHEL-7009

* Tue Sep 26 2023 Marek Kasik <mkasik@redhat.com> - 3.4.0-8.el8_9.1
- Do not evaluate unichar element
- Replace an invalid char with a correct one (rpminspect)
- Resolves: RHEL-7009

* Wed Jan 15 2020 Marek Kasik <mkasik@redhat.com> - 3.4.0-8
- Fix Requires for doc subpackage
- Resolves: #1788556

* Tue Jan 14 2020 Marek Kasik <mkasik@redhat.com> - 3.4.0-7
- Do not eval strings passed to toColor
- Resolves: #1788556

* Thu May 31 2018 Marek Kasik <mkasik@redhat.com> - 3.4.0-6
- Remove python2-reportlab subpackage
- Resolves: #1567162

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 24 2017 williamjmorenor@gmail.com - 3.4.0-4
- Adjust requirements

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 William Moreno <williamjmorenor@gmail.com> - 3.4.0-1
- Update to 3.4.0 upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Apr 09 2016 William Moreno <williamjmorenor@gmail.com> - 3.3.0-1
- Update to v3.3.0
- Update python macros
- Enable %%test
- Use license macro
- Provide python2 subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Oct 26 2015 Peter Gordon <peter@thecodergeek.com> - 3.2.0-1
- Update to new upstream release (3.2.0)
- Drop font locations patches (fixed upstream):
  - 3.1.8-font-locations.patch
  - 2.5-font-locations.patch
- Resolves: #1175228 (python-reportlab-3.2.0 is available).
- Resolves: #1277162 (Wrong dependency version number for pillow.)
- Resolves: #1267446 (Missing Requires: on pillow)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 22 2014 Christopher Meng <rpm@cicku.me> - 3.1.8-1
- Update to 3.1.8
- Documentation package should be -doc instead of -docs.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5-6
- Add a dep on python-imaging to process images

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.5-2
- Update to version 2.5 of reportlab.
- Remove tabs in specfile.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 23 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.3-2
- Do not bundle fonts
- Point the config to Fedora's font locations

* Thu Nov 12 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.3-1
- Updated to 2.3
- New version is no longer noarch.

* Fri Apr 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.1-6
- Rebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-4
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1-3
- Rebuild for Python 2.6

* Mon Jan  7 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.1-2
- Remove luxi font. (#427845)
- Add patch to not search for the luxi font.

* Sat May 26 2007 Brian Pepple <bpepple@fedoraproject.org> - 2.1-1
- Update to 2.1.

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-2
- Make docs subpackage.

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-1
- Update to 2.0.

* Fri Dec  8 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-2
- Rebuild against new python.

* Thu Sep  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-1
- Update to 1.20.1.

* Tue Feb 14 2006 Brian Pepple <bdpepple@ameritech.net> - 1.20-5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 26 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-4
- Add dist tag. (#176479)

* Mon May  9 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-3.fc4
- Switchback to sitelib patch.
- Make package noarch.

* Thu Apr  7 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-2.fc4
- Use python_sitearch to fix x86_64 build.

* Wed Mar 30 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-1.fc4
- Rebuild for Python 2.4.
- Update to 1.20.
- Switch to the new python macros for python-abi
- Add dist tag.

* Sat Apr 24 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.2
- Removed ghosts.

* Sat Mar 20 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.1
- Initial Fedora RPM build.


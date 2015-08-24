Name:			arduino-mk
Version:		1.5
Summary:		Program your Arduino from the command line
Packager:		Simon John <git@the-jedi.co.uk>
URL:            https://github.com/sudar/Arduino-Makefile
Source:         %{name}-%{version}.tar.gz
Group:			Development/Tools
License:		LGPLv2+
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch

%if 0%{?suse_version}
# opensuse installs arduino in arduino-<version> instead of just arduino 
%define arduino_version %(rpm -q --qf '%{VERSION}' arduino)
%define arduino_dir %{_datadir}/arduino-%{arduino_version}
Release:		1
Requires:		arduino = %{arduino_version} python-pyserial
BuildRequires:	arduino
%else
%define arduino_dir %{_datadir}/arduino
Release:		1%{dist}
Requires:		arduino-core pyserial
BuildRequires:	arduino-core
%endif


%description
Arduino is an open-source electronics prototyping platform based on 
flexible, easy-to-use hardware and software. It's intended for artists, 
designers, hobbyists, and anyone interested in creating interactive 
objects or environments.

This package will install a Makefile to allow for CLI programming of the 
Arduino platform.

%prep
%setup -q
# quick and dirty adjustment to opensuses arduino directories with version included
%if 0%{?suse_version}
sed -i "s,/usr/share/arduino,%{arduino_dir},g" Arduino.mk arduino-mk-vars.md Common.mk README.md examples/MakefileExample/Makefile-example.mk
%endif

%install
mkdir -p %{buildroot}/%{arduino_dir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_docdir}/%{name}/examples
install -m 755 -d %{buildroot}/%{_docdir}/%{name}
install -m 755 -d %{buildroot}/%{_docdir}/%{name}/examples
for dir in `find examples -type d` ; do install -m 755 -d %{buildroot}/%{_docdir}/%{name}/$dir ; done
for file in `find examples -type f ! -name .gitignore` ; do install -m 644 $file %{buildroot}/%{_docdir}/%{name}/$file ; done
install -m 644 *.mk arduino-mk-vars.md %{buildroot}/%{arduino_dir}
install -m 644 licence.txt %{buildroot}/%{_docdir}/%{name}
install -m 755 bin/ard-reset-arduino %{buildroot}/%{_bindir}/ard-reset-arduino
install -m 644 ard-reset-arduino.1 %{buildroot}/%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/ard-reset-arduino
%{_mandir}/man1/ard-reset-arduino.1*
%{arduino_dir}/*.mk
%{arduino_dir}/arduino-mk-vars.md
%doc %{_docdir}/%{name}/licence.txt
%docdir %{_docdir}/%{name}/examples
%{_docdir}/%{name}/examples

%changelog
* Mon Aug 24 2015 Bernd Wachter <bwachter-pkg@lart.info>
- Make spec file usable with OpenSuSE
* Sat Apr 12 2014 Simon John <git@the-jedi.co.uk>
- Put manpage back.
* Fri Apr 04 2014 Simon John <git@the-jedi.co.uk>
- Removed BuildRequires of python3/pyserial.
* Wed Apr 02 2014 Simon John <git@the-jedi.co.uk>
- Added BuildRequires of python3-pyserial. Need to look into Requires.
* Mon Mar 24 2014 Simon John <git@the-jedi.co.uk>
- Replaced perl/help2man with pyserial for reset script.
* Tue Feb 04 2014 Simon John <git@the-jedi.co.uk>
- Added arduino-mk-vars.md to the files to be installed/packaged.
* Sat Feb 01 2014 Simon John <git@the-jedi.co.uk>
- Updated version.
* Mon Jan 13 2014 Simon John <git@the-jedi.co.uk>
- Removed arduino-mk subdirectory
* Mon Dec 30 2013 Simon John <git@the-jedi.co.uk>
- Initial release.

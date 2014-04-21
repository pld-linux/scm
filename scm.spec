%define	slib_ver	3b4
Summary:	Scheme implementation
Summary(pl.UTF-8):	Implementacja Scheme
Name:		scm
Version:	5f1
Release:	2
License:	LGPL v3+
Group:		Development/Languages/Scheme
Source0:	http://groups.csail.mit.edu/mac/ftpdir/scm/%{name}-%{version}.zip
# Source0-md5:	98be8275f5c69d234c55a8a995a500dd
Source1:	http://groups.csail.mit.edu/mac/ftpdir/scm/slib-%{slib_ver}.tar.gz
# Source1-md5:	dcada65c4df4209c8f71211095bcef8e
Patch0:		%{name}-info.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-texinfo.patch
URL:		http://people.csail.mit.edu/jaffer/SCM
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
Requires:	scm-slib >= %{slib_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SCM is a portable Scheme language implementation. SCM conforms to
Revised^5 Report on the Algorithmic Language Scheme and the IEEE P1178
specification.

%description -l pl.UTF-8
SCM jest przenośną implementacją języka Scheme. SCM jest zgodna ze
specyfikacją Revised^5 Report on the Algorithmic Language Scheme oraz
IEEE P1178.

%prep
%setup -q -c -a1
%patch0 -p0
%patch1 -p0
%patch2 -p0

ln -s slib-%{slib_ver} slib

%{__sed} -i -e 's/install-lib install-infoz /install-lib install-info /' scm/Makefile

%build
cd scm
# not autoconf-generated
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

%{__make} scm.info Xlibscm.info hobbit.info

%{__make} scmlit \
	CC="%{__cc} %{rpmcflags}" \
	LD="%{__cc} %{rpmldflags} %{rpmcflags}"
%{__make} all \
	CC="%{__cc} %{rpmcflags}" \
	LD="%{__cc} %{rpmldflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C scm install \
	DESTDIR=$RPM_BUILD_ROOT

# let rpm autogenerate depecdencies
chmod 755 $RPM_BUILD_ROOT%{_libdir}/scm/*.so

# creation handled by (noarch) scm-slib package
touch $RPM_BUILD_ROOT%{_libdir}/scm/slibcat
# at least require[s].scm expects slib in ../slib relative to %{_libdir}/scm
ln -sf ../share/slib $RPM_BUILD_ROOT%{_libdir}/slib

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc scm/{ANNOUNCE,ChangeLog,QUICKREF,README}
%attr(755,root,root) %{_bindir}/scm
%attr(755,root,root) %{_bindir}/scmlit
%dir %{_libdir}/scm
%attr(755,root,root) %{_libdir}/scm/*.so
%attr(755,root,root) %{_libdir}/scm/build
%{_libdir}/scm/*.scm
%{_libdir}/scm/*.h
%{_libdir}/scm/COPYING
%{_libdir}/scm/COPYING.LESSER
%ghost %{_libdir}/scm/slibcat
%{_libdir}/slib
%{_includedir}/scm.h
%{_includedir}/scmfig.h
%{_includedir}/scmflags.h
%{_mandir}/man1/scm.1*
%{_infodir}/Xlibscm.info*
%{_infodir}/hobbit.info*
%{_infodir}/scm.info*

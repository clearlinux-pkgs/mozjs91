#
# Inspired by the Arch Linux equivalent package.....
#
Name     : mozjs91
Version  : 91.5.1
Release  : 11
URL      : https://archive.mozilla.org/pub/firefox/releases/91.5.1esr/source/firefox-91.5.1esr.source.tar.xz
Source0  : https://archive.mozilla.org/pub/firefox/releases/91.5.1esr/source/firefox-91.5.1esr.source.tar.xz
Group    : Development/Tools
Summary  : JavaScript interpreter and libraries
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-3-Clause-Clear GPL-2.0 LGPL-2.0 LGPL-2.1 MIT MPL-2.0-no-copyleft-exception
Requires: mozjs91-bin = %{version}-%{release}
Requires: mozjs91-lib = %{version}-%{release}
Requires: pypi-psutil
Requires: pypi-pyopenssl
Requires: pypi-pyasn1
Requires: pypi-wheel
BuildRequires : autoconf213
BuildRequires : icu4c-dev
BuildRequires : llvm-dev
BuildRequires : ncurses-dev
BuildRequires : nspr-dev
BuildRequires : pypi-pbr
BuildRequires : pypi-pip
BuildRequires : pkgconfig(libffi)
BuildRequires : pkgconfig(x11)
BuildRequires : pypi-psutil
BuildRequires : python3-core
BuildRequires : python3-dev
BuildRequires : readline-dev
BuildRequires : rustc
BuildRequires : pypi-setuptools
BuildRequires : zlib-dev

Patch1: fix-soname.patch
Patch2: copy-headers.patch
Patch3: init_patch.patch
Patch4: emitter.patch
Patch5: spidermonkey_checks_disable.patch

%description
JavaScript interpreter and libraries - Version 91

%package bin
Summary: bin components for the mozjs91 package.
Group: Binaries

%description bin
bin components for the mozjs91 package.


%package dev
Summary: dev components for the mozjs91 package.
Group: Development
Requires: mozjs91-lib = %{version}-%{release}
Requires: mozjs91-bin = %{version}-%{release}
Provides: mozjs91-devel = %{version}-%{release}

%description dev
dev components for the mozjs91 package.


%package lib
Summary: lib components for the mozjs91 package.
Group: Libraries

%description lib
lib components for the mozjs91 package.


%prep
%setup -q -n firefox-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# use system zlib for perf
rm -rf ../../modules/zlib


%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1501084420
export CFLAGS="-Os -falign-functions=4 -fno-semantic-interposition -fassociative-math -fno-signed-zeros "
export FCFLAGS="-O3 -falign-functions=32 -fno-semantic-interposition "
export FFLAGS="$CFLAGS -O3 -falign-functions=32 -fno-semantic-interposition "
export CXXFLAGS="-Os -falign-functions=4 -fno-semantic-interposition -fassociative-math -fno-signed-zeros"
export AUTOCONF="/usr/bin/autoconf213"
CFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp '
CXXFLAGS+=' -fno-delete-null-pointer-checks -fno-strict-aliasing -fno-tree-vrp '
export CC=gcc CXX=g++ PYTHON3=/usr/bin/python3

pushd js/src

autoconf213
%configure --disable-static \
    --prefix=/usr \
    --disable-debug \
    --enable-debug-symbols \
    --disable-strip \
    --disable-jemalloc \
    --enable-optimize="-O3" \
    --enable-posix-nspr-emulation \
    --enable-readline \
    --enable-release \
    --enable-shared-js \
    --enable-tests \
    --with-intl-api \
    --with-system-zlib \
    --with-x \
    --program-suffix=91 \
    --without-system-icu

make %{?_smp_mflags}
popd


%install
export SOURCE_DATE_EPOCH=1501084420
rm -rf %{buildroot}
pushd js/src
%make_install
popd
rm %{buildroot}/usr/lib64/*.ajs

cp %{buildroot}/usr/lib64/libmozjs-91.so %{buildroot}/usr/lib64/libmozjs-91.so.0

%files
%defattr(-,root,root,-)

%files bin
%defattr(-,root,root,-)
/usr/bin/js91
/usr/bin/js91-config

%files dev
%defattr(-,root,root,-)
/usr/include/mozjs-91/
/usr/lib64/pkgconfig/mozjs-91.pc

%files lib
%defattr(-,root,root,-)
/usr/lib64/libmozjs-91.so
/usr/lib64/libmozjs-91.so.0

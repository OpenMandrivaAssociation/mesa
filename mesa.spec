# (cg) Cheater...
%define Werror_cflags %{nil}

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define git 0
%define git_branch 9.2

%define opengl_ver 3.0

%define relc	0

# bootstrap option: Build without requiring an X server
# (which in turn requires mesa to build)
%bcond_without hardware
%bcond_without bootstrap
%bcond_without vdpau
%bcond_with va
%bcond_without wayland
%bcond_without egl
%bcond_without opencl
%bcond_without tfloat
%ifarch %arm mips sparc
%bcond_with intel
%else
%bcond_without intel
%endif

%if %{relc}
%define vsuffix -rc%{relc}
%else
%define vsuffix %{nil}
%endif

%define osmesamajor	8
%define libosmesa	%mklibname osmesa %{osmesamajor}
%define devosmesa	%mklibname osmesa -d

%define eglmajor	1
%define eglname		egl
%define libegl		%mklibname %{eglname} %{eglmajor}
%define devegl		%mklibname %{eglname} -d

%define glmajor		1
%define glname		gl
%define libgl		%mklibname %{glname} %{glmajor}
%define devgl		%mklibname %{glname} -d

%define glesv1major	1
%define glesv1name	glesv1
%define libglesv1	%mklibname %{glesv1name}_ %{glesv1major}
%define devglesv1	%mklibname %{glesv1name} -d

%define glesv2major	2
%define glesv2name	glesv2
%define libglesv2	%mklibname %{glesv2name}_ %{glesv2major}
%define devglesv2	%mklibname %{glesv2name} -d

%define devglesv3	%mklibname glesv3 -d

%define openvgmajor	1
%define openvgname	openvg
%define libopenvg	%mklibname %{openvgname} %{openvgmajor}
%define devopenvg	%mklibname %{openvgname} -d

%define glapimajor	0
%define glapiname	glapi
%define libglapi	%mklibname %{glapiname} %{glapimajor}
%define devglapi	%mklibname %{glapiname} -d

%define dridrivers	%mklibname dri-drivers

%define dricoremajor	1
%define dricorename	dricore
%define libdricore	%mklibname %{dricorename} %{dricoremajor}
%define devdricore	%mklibname %{dricorename} -d

%define gbmmajor	1
%define gbmname		gbm
%define libgbm		%mklibname %{gbmname} %{gbmmajor}
%define devgbm		%mklibname %{gbmname} -d

%define xatrackermajor	1
%define xatrackername	xatracker
%define libxatracker	%mklibname %xatrackername %{xatrackermajor}
%define devxatracker	%mklibname %xatrackername -d

%define clmajor		1
%define clname		opencl
%define libcl		%mklibname %clname %clmajor
%define devcl		%mklibname %clname -d

%define waylandeglmajor	1
%define waylandeglname	wayland-egl
%define libwaylandegl	%mklibname %{waylandeglname} %{waylandeglmajor}
%define devwaylandegl	%mklibname %{waylandeglname} -d

%define libvadrivers	%mklibname va-drivers

%define mesasrcdir	%{_prefix}/src/Mesa/
%define driver_dir	%{_libdir}/dri

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i915,i965,nouveau,r200,radeon,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"r200,radeon,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i915,i965,mga,r200,radeon,swrast"
%define	dri_drivers_alpha	"r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,radeon,swrast"
%define dri_drivers_mipsel	"r200,radeon,swrast"
%define dri_drivers_arm		"nouveau,r200,radeon,swrast"
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}

%define short_ver 9.2.3

Summary:	OpenGL 3.0 compatible 3D graphics library
Name:		mesa
Version:	9.2.3
%if %{relc}
%if %{git}
Release:	0.rc%{relc}.0.%{git}.1
%else
Release:	0.rc%{relc}.1
%endif
%else
%if %{git}
Release:	0.%{git}.1
%else
Release:	1
%endif
%endif
Group:		System/Libraries
License:	MIT
Url:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git_branch}-%{git}.tar.xz
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%short_ver/MesaLib-%{short_ver}%{vsuffix}.tar.bz2
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install
Source100:	%{name}.rpmlintrc

# fedora patches
Patch15: mesa-9.2-hardware-float.patch
Patch20: mesa-9.2-evergreen-big-endian.patch

# Instructions to setup your repository clone
# git://git.freedesktop.org/git/mesa/mesa
# git checkout mesa_7_5_branch
# git branch mdv-cherry-picks
# git am ../02??-*.patch
# git branch mdv-redhat
# git am ../03??-*.patch
# git branch mdv-patches
# git am ../09??-*.patch

# In order to update to the branch via patches, issue this command:
# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'

# Cherry picks
# git format-patch --start-number 200 mesa_7_5_branch..mdv-cherry-picks

# Mandriva & Mageia patches

# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'
Patch201: 0201-revert-fix-glxinitializevisualconfigfromtags-handling.patch
Patch202: GLX_INDIRECT_RENDERING_mesa9_1.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	gccmakedep
BuildRequires:	libxml2-python
BuildRequires:	makedepend
BuildRequires:	llvm-devel >= 3.3
BuildRequires:	pkgconfig(expat)
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(libdrm) >= 2.4.22
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(x11)		>= 1.3.3
BuildRequires:	pkgconfig(xdamage)	>= 1.1.1
BuildRequires:	pkgconfig(xext)		>= 1.1.1
BuildRequires:	pkgconfig(xfixes)	>= 4.0.3
BuildRequires:	pkgconfig(xi)		>= 1.3
BuildRequires:	pkgconfig(xmu)		>= 1.0.3
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xt)		>= 1.0.5
BuildRequires:	pkgconfig(xxf86vm)	>= 1.1.0
%if %{with opencl}
BuildRequires:	pkgconfig(libclc)
BuildRequires:	clang-devel clang
%endif
%if ! %{with bootstrap}
BuildRequires:	pkgconfig(xorg-server)	>= 1.11.0
%endif
BuildRequires:	pkgconfig(xvmc)
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau)	>= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva)	>= 0.31.0
%endif
%if %{with wayland}
BuildRequires:	wayland-devel		>= 1.0.2
%endif

# package mesa
Requires:	%{libgl} = %{version}-%{release}

%description
Mesa is an OpenGL 3.0 compatible 3D graphics library.

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Requires:	%{dridrivers}-radeon = %{EVRD}
%ifnarch %arm
Requires:	%{dridrivers}-intel = %{EVRD}
%endif
Requires:	%{dridrivers}-nouveau = %{EVRD}
Requires:	%{dridrivers}-swrast = %{EVRD}
%ifarch %arm
Requires:	%{dridrivers}-freedreno = %{EVRD}
%endif
Provides:	dri-drivers = %{EVRD}

%description -n %{dridrivers}
DRI and XvMC drivers.

%package -n	%{dridrivers}-radeon
Summary:	DRI Drivers for AMD/ATI Radeon graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
%define __noautoreq '.*llvmradeon.*'

%description -n %{dridrivers}-radeon
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets

%package -n	%{dridrivers}-vmwgfx
Summary:	DRI Drivers for VMWare guest OS
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-vmwgfx
DRI and XvMC drivers for VMWare guest Operating Systems.

%ifnarch %arm
%package -n	%{dridrivers}-intel
Summary:	DRI Drivers for Intel graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-intel
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets
%endif

%package -n	%{dridrivers}-nouveau
Summary:	DRI Drivers for NVIDIA graphics chipsets using the Nouveau driver
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-nouveau
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets

%package -n	%{dridrivers}-swrast
Summary:	DRI Drivers for software rendering
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-swrast
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets

%ifarch %arm
%package -n	%{dridrivers}-freedreno
Summary:	DRI Drivers for software rendering
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-freedreno
DRI and XvMC drivers for Adreno graphics chipsets
%endif

%package	xorg-drivers
Summary:	Mesa/Gallium XOrg drivers
Group:		System/X11
Requires:	%{name}-xorg-drivers-radeon = %{EVRD}
Requires:	%{name}-xorg-drivers-nouveau = %{EVRD}

%description xorg-drivers
Xorg drivers from the Mesa/Gallium project

%package	xorg-drivers-radeon
Summary:	Mesa/Gallium XOrg drivers for AMD/ATI Radeon chipsets
Group:		System/X11

%description xorg-drivers-radeon
Xorg drivers from the Mesa/Gallium project for AMD/ATI Radeon graphics chipsets

%package	xorg-drivers-nouveau
Summary:	Mesa/Gallium XOrg drivers for NVIDIA chipsets using the Nouveau driver
Group:		System/X11

%description xorg-drivers-nouveau
Xorg drivers from the Mesa/Gallium project for NVIDIA graphics chipsets

%package -n	%{libdricore}
Summary:	Shared library for DRI drivers
Group:		System/Libraries

%description -n %{libdricore}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
DRI core part.

%package -n	%{devdricore}
Summary:	Development files for DRI core
Group:		Development/C
Requires:	%{libdricore} = %{version}-%{release}

%description -n %{devdricore}
This package contains the headers needed to compile DRI drivers.

%package -n	%{libosmesa}
Summary:	Mesa offscreen rendering library
Group:		System/Libraries

%description -n %{libosmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n	%{devosmesa}
Summary:	Development files for libosmesa
Group:		Development/C
Requires:	%{libosmesa} = %{version}-%{release}

%description -n %{devosmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%if %{with va}
%package -n	%{libvadrivers}
Summary:	Mesa libVA video acceleration drivers
Group:		System/Libraries

%description -n %{libvadrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
libVA drivers for video acceleration
%endif

%package -n	%{libgl}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Suggests:	%{dridrivers} >= %{version}-%{release}
%if %{with tfloat}
Requires:	%mklibname txc-dxtn
%endif
Obsoletes:	%{_lib}mesagl1 < %{version}-%{release}

%description -n %{libgl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
GL and GLX parts.

%package -n	%{devgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{libgl} = %{version}-%{release}
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{version}-%{release}

%description -n %{devgl}
This package contains the headers needed to compile Mesa programs.

%if %{with egl}
%package -n	%{libegl}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0

%description -n %{libegl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL parts.

%package -n	%{devegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libegl} = %{version}-%{release}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{version}-%{release}

%description -n %{devegl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL development parts.
%endif

%package -n %{libglapi}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%description -n %{libglapi}
This package provides the glapi shared library used by gallium.

%package -n %{devglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Requires:	%{libglapi} = %{version}-%{release}
Obsoletes:	%{_lib}glapi0-devel < %{version}-%{release}

%description -n %{devglapi}
This package contains the headers needed to compile programs against
the glapi shared library.

%if ! %{with bootstrap}
%package -n %{libxatracker}
Summary:	Files for mesa (xatracker libs)
Group:		System/Libraries

%description -n %{libxatracker}
This package provides the xatracker shared library used by gallium.
 
%package -n %{devxatracker}
Summary:	Development files for xatracker libs
Group:		Development/C
Requires:	%{libxatracker} = %{version}-%{release}

%description -n %{devxatracker}
This package contains the headers needed to compile programs against
the xatracker shared library.
%endif

%package -n %{libglesv1}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1 < 8.0

%description -n %{libglesv1}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%package -n %{devglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1} = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{version}-%{release}

%description -n %{devglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%package -n %{libglesv2}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0

%description -n %{libglesv2}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%package -n %{devglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2} = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{version}-%{release}

%description -n %{devglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%package -n %{devglesv3}
Summary:	Development files for glesv3 libs
Group:		Development/C
# there is no pkgconfig 
Provides:	glesv3-devel = %{version}-%{release}

%description -n %{devglesv3}
This package contains the headers needed to compile OpenGL ES 3 programs.

%package -n %{libopenvg}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaopenvg1 < 8.0

%description -n %{libopenvg}
OpenVG is a royalty-free, cross-platform API that provides a low-level hardware
acceleration interface for vector graphics libraries such as Flash and SVG.

%package -n %{devopenvg}
Summary:	Development files for OpenVG libs
Group:		Development/C
Requires:	%{libopenvg} = %{version}-%{release}
Requires:	%{devegl} = %{version}-%{release}
Obsoletes:	%{_lib}mesaopenvg1-devel < 8.0

%description -n %{devopenvg}
Development files for OpenVG library.

%if %{with opencl}
%package -n %{libcl}
Summary:	OpenCL libs
Group:		System/Libraries

%description -n %{libcl}
Open Computing Language (OpenCL) is a framework for writing programs that
execute across heterogeneous platforms consisting of central processing units
(CPUs), graphics processing units (GPUs), DSPs and other processors.

OpenCL includes a language (based on C99) for writing kernels (functions that
execute on OpenCL devices), plus application programming interfaces (APIs) that
are used to define and then control the platforms. OpenCL provides parallel
computing using task-based and data-based parallelism. OpenCL is an open
standard maintained by the non-profit technology consortium Khronos Group.
It has been adopted by Intel, Advanced Micro Devices, Nvidia, and ARM Holdings.

%package -n %{devcl}
Summary:	Development files for OpenCL libs
Group:		Development/Other
Requires:	%{libcl} = %{version}-%{release}
Provides:	lib%{libcl}-devel = %{version}-%{release}

%description -n %{devcl}
Development files for the OpenCL library
%endif

%if %{with vdpau}
%package -n	%{_lib}vdpau-driver-nouveau
Summary:	VDPAU plugin for nouveau driver
Group:		System/Libraries

%description -n %{_lib}vdpau-driver-nouveau
This packages provides a VPDAU plugin to enable video acceleration
with the nouveau driver.

%package -n	%{_lib}vdpau-driver-r300
Summary:	VDPAU plugin for r300 driver
Group:		System/Libraries

%description -n %{_lib}vdpau-driver-r300
This packages provides a VPDAU plugin to enable video acceleration
with the r300 driver.

%package -n	%{_lib}vdpau-driver-r600
Summary:	VDPAU plugin for r600 driver
Group:		System/Libraries

%description -n %{_lib}vdpau-driver-r600
This packages provides a VPDAU plugin to enable video acceleration
with the r600 driver.

%package -n	%{_lib}vdpau-driver-radeonsi
Summary:	VDPAU plugin for radeonsi driver
Group:		System/Libraries

%description -n %{_lib}vdpau-driver-radeonsi
This packages provides a VPDAU plugin to enable video acceleration
with the radeonsi driver.

%package -n	%{_lib}vdpau-driver-softpipe
Summary:	VDPAU plugin for softpipe driver
Group:		System/Libraries

%description -n %{_lib}vdpau-driver-softpipe
This packages provides a VPDAU plugin to enable video acceleration
with the softpipe driver.
%endif

%if %{with wayland}
%package -n %{libgbm}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries

%description -n %{libgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%package -n %{devgbm}
Summary:	Development files for Mesa (gbm libs)
Group:		Development/C
Requires:	%{libgbm} = %{version}-%{release}

%description -n %{devgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.

%package -n %{libwaylandegl}
Summary:	Files for Mesa (Wayland EGL libs)
Group:		System/Libraries

%description -n %{libwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform parts.

%package -n %{devwaylandegl}
Summary:	Development files for Mesa (Wayland EGL libs)
Group:		Development/C
Requires:	%{libwaylandegl} = %{version}-%{release}

%description -n %{devwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform development parts.
%endif

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{devgl} = %{version}-%{release}
Requires:	%{devegl} = %{version}-%{release}
Requires:	%{devglapi} = %{version}-%{release}
Requires:	%{devglesv1} = %{version}-%{release}
Requires:	%{devglesv2} = %{version}-%{release}

%description common-devel
Mesa common metapackage devel

%prep
%if %{git}
%setup -qn %{name}-%{git_branch}-%{git}
%else
%setup -qn Mesa-%{short_ver}%{vsuffix}
%endif

%apply_patches
chmod +x %{SOURCE5}

#sed -i 's/CFLAGS="$CFLAGS -Werror=implicit-function-declaration"//g' configure.ac
#sed -i 's/CFLAGS="$CFLAGS -Werror=missing-prototypes"//g' configure.ac

autoreconf -vfi

# Duplicate source tree for OSMesa, since building both versions out-of-tree
# would break build. - Anssi 12/2012
all=$(ls)
mkdir -p build-osmesa
cp -a $all build-osmesa

%build
# fix build - TODO: should this be fixed in llvm somehow, or maybe the library
# symlinks should be moved to %{_libdir}? -Anssi 08/2012
export LDFLAGS="-L%{_libdir}/llvm"

GALLIUM_DRIVERS="swrast"
%if %{with hardware}
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,svga,r300,r600,radeonsi,nouveau"
%if %{with intel}
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,i915,ilo"
%endif
%ifarch %arm
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,freedreno"
%endif
%endif

%configure2_5x \
	--enable-dri \
	--enable-glx \
	--with-dri-driverdir=%{driver_dir} \
	--with-dri-drivers="%{dri_drivers}" \
	--with-clang-libdir=%{_prefix}/lib \
%if %{with egl}
	--enable-egl \
	--enable-gallium-egl \
	--enable-gbm \
	--enable-shared-glapi \
%else
	--disable-egl \
%endif
%if %{with wayland}
	--with-egl-platforms=x11,wayland,drm,fbdev \
%else
	--with-egl-platforms=x11,drm,fbdev \
%endif
%if ! %{with bootstrap}
	--enable-xorg \
	--enable-xa \
%endif
	--enable-gles1 \
	--enable-gles2 \
	--enable-gles3 \
	--enable-openvg \
%if %{with opencl}
	--enable-opencl \
%endif
	--enable-gallium-egl \
	--enable-gallium-g3dvl \
	--enable-xvmc \
%if %{with vdpau}
	--enable-vdpau \
%else		
	--disable-vdpau \
%endif
%if %{with va}
	--enable-va \
%else
	--disable-va \
%endif
	--with-gallium-drivers=$GALLIUM_DRIVERS \
%if %{with hardware}
	--enable-gallium-llvm \
	--enable-r600-llvm-compiler \
%else
	--disable-gallium-llvm \
%endif
%if %{with tfloat}
	--enable-texture-float  \
%endif
	# end of configure options


# Build OSMesa separately, since we want to build OSMesa without shared-glapi,
# since doing that causes OSMesa to miss the OpenGL symbols.
# See e.g. https://bugs.launchpad.net/ubuntu/+source/mesa/+bug/1066599
# -Anssi 12/2012

pushd build-osmesa
%configure2_5x \
	--enable-osmesa \
	--disable-dri \
	--disable-glx \
	--disable-egl \
	--disable-shared-glapi \
	--without-gallium-drivers
popd

%make
%make -C build-osmesa

%install
%makeinstall_std -C build-osmesa
%makeinstall_std

# FIXME: strip will likely break the hardlink
# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p %{buildroot}%{_libdir}/mesa
pushd %{buildroot}%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

# .so files are not needed by vdpau
rm -f %{buildroot}%{_libdir}/vdpau/libvdpau_*.so

# .la files are not needed by mesa
find %{buildroot} -name '*.la' -exec rm {} \;

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so


%files
%doc docs/COPYING docs/README.*
%config(noreplace) %{_sysconfdir}/drirc

%files -n %{dridrivers}
%doc docs/COPYING

%files -n %{dridrivers}-radeon
%_libdir/dri/r?00_dri.so
%_libdir/dri/radeon_dri.so
%_libdir/dri/radeonsi_dri.so
%_libdir/gallium-pipe/pipe_r?00.so
%_libdir/gallium-pipe/pipe_radeonsi.so
%_libdir/libXvMCr?00.so.*
#% _libdir/libllvmradeon*.so

%files -n %{dridrivers}-vmwgfx
%_libdir/dri/vmwgfx_dri.so
%_libdir/gallium-pipe/pipe_vmwgfx.so

%ifnarch %arm
%files -n %{dridrivers}-intel
%if ! %{with bootstrap}
%{_libdir}/xorg/modules/drivers/i915_drv.so
%endif
%_libdir/dri/i9?5_dri.so
%_libdir/gallium-pipe/pipe_i915.so
%endif

%files -n %{dridrivers}-nouveau
%_libdir/dri/nouveau*_dri.so
%_libdir/gallium-pipe/pipe_nouveau.so
%_libdir/libXvMCnouveau.so.*

%files -n %{dridrivers}-swrast
%_libdir/dri/swrast_dri.so
%_libdir/gallium-pipe/pipe_swrast.so
%_libdir/libXvMCsoftpipe.so.*

%ifarch %arm
%files -n %{dridrivers}-freedreno
%{_libdir}/dri/kgsl_dri.so
%endif

%if ! %{with bootstrap}
%files xorg-drivers

%files xorg-drivers-radeon
%_libdir/xorg/modules/drivers/r?00g_drv.so
%_libdir/xorg/modules/drivers/radeonsi_drv.so

%files xorg-drivers-nouveau
%_libdir/xorg/modules/drivers/nouveau2_drv.so
%endif

%files -n %{libdricore}
%{_libdir}/libdricore%{version}.so.%{dricoremajor}*

%files -n %{libosmesa}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{devosmesa}
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if %{with va}
%files -n %{libvadrivers}
%{_libdir}/va/lib*.so*
%endif

%files -n %{libgl}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*
%dir %_libdir/dri
%dir %_libdir/gallium-pipe

%if %{with egl}
%files -n %{libegl}
%doc docs/COPYING
%{_libdir}/libEGL.so.%{eglmajor}*
%dir %{_libdir}/egl
%if !%{with wayland}
# st_GL, built only when shared glapi is not enabled
%{_libdir}/egl/st_GL.so
%endif
%{_libdir}/egl/egl_gallium.so
%endif

%files -n %{libglapi}
%{_libdir}/libglapi.so.%{glapimajor}*

%if ! %{with bootstrap}
%files -n %{libxatracker}
%{_libdir}/libxatracker.so.%{xatrackermajor}*
%endif

%files -n %{libglesv1}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libopenvg}
%{_libdir}/libOpenVG.so.%{openvgmajor}*

%if %{with opencl}
%files -n %{libcl}
%_libdir/libOpenCL.so.%{clmajor}*
%endif

%if %{with wayland}
%files -n %{libgbm}
%{_libdir}/libgbm.so.%{gbmmajor}*
%{_libdir}/gbm/gbm_*.so

%files -n %{libwaylandegl}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}*
%endif

%files -n %{devgl}
%doc docs/COPYING
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%{_libdir}/libXvMC*.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files common-devel
# meta devel pkg

%if %{with egl}
%files -n %{devegl}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc
%endif

%files -n %{devglapi}
%{_libdir}/libglapi.so

%files -n %{devdricore}
%{_libdir}/libdricore%{version}.so

#vdpau enblaed
%if %{with vdpau}
%files -n %{_lib}vdpau-driver-nouveau
%{_libdir}/vdpau/libvdpau_nouveau.so.*

%files -n %{_lib}vdpau-driver-r300
%{_libdir}/vdpau/libvdpau_r300.so.*

%files -n %{_lib}vdpau-driver-r600
%{_libdir}/vdpau/libvdpau_r600.so.*

%files -n %{_lib}vdpau-driver-radeonsi
%{_libdir}/vdpau/libvdpau_radeonsi.so.*

%files -n %{_lib}vdpau-driver-softpipe
%{_libdir}/vdpau/libvdpau_softpipe.so.*
%endif

%if ! %{with bootstrap}
%files -n %{devxatracker}
%{_libdir}/libxatracker.so
%{_includedir}/xa_*.h
%{_libdir}/pkgconfig/xatracker.pc
%endif

%files -n %{devglesv1}
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{devglesv2}
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{devglesv3}
%{_includedir}/GLES3

%files -n %{devopenvg}
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_libdir}/pkgconfig/vg.pc

%if %{with opencl}
%files -n %{devcl}
%_includedir/CL
%_libdir/libOpenCL.so
%endif

%if %{with wayland}
%files -n %{devgbm}
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc

%files -n %{devwaylandegl}
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif


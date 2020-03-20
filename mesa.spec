# (cg) Cheater...
%define Werror_cflags %{nil}

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

# We disable LTO because of a compile error in the Intel Vulkan driver
# last seen with Mesa 19.2.0-rc1 and (interestingly) both gcc 9.2 and clang 9.0-rc2
# Use BFD as ith LLD this errors occurs ld: error: TLS attribute mismatch: _glapi_tls_Dispatch
# -fno-strict-aliasing is added because of numerous warnings, strict
# aliasing might generate broekn code.
%global optflags %{optflags} -O3 -fno-strict-aliasing -fuse-ld=gold
%global ldflags %{ldflags} -fno-strict-aliasing

%define git %{nil}
%define git_branch %(echo %{version} |cut -d. -f1-2)

# (tpg) starting version 11.1.1 this may fully support OGL 4.1
%define opengl_ver 4.5

%define relc %{nil}

%ifarch %{riscv}
%bcond_without gcc
%bcond_with opencl
%else
%bcond_with gcc
%bcond_without opencl
%endif

%bcond_with bootstrap
%bcond_without vdpau
%bcond_without va
%bcond_without glvnd
%bcond_without egl
%ifarch %{ix86} %{x86_64}
%bcond_without intel
%else
%bcond_with intel
%endif
# Sometimes it's necessary to disable r600 while bootstrapping
# an LLVM change (such as the r600 -> AMDGPU rename)
%bcond_without r600

%if "%{relc}" != ""
%define vsuffix -rc%{relc}
%else
%define vsuffix %{nil}
%endif

%define osmesamajor 8
%define libosmesa %mklibname osmesa %{osmesamajor}
%define devosmesa %mklibname osmesa -d

%define eglmajor 0
%define eglname EGL_mesa
%define libegl %mklibname %{eglname} %{eglmajor}
%define devegl %mklibname %{eglname} -d

%define glmajor 0
%define glname GLX_mesa
%define libgl %mklibname %{glname} %{glmajor}
%define devgl %mklibname GL -d

%define devvulkan %mklibname vulkan-intel -d

%define glesv1major 1
%define glesv1name GLESv1_CM
%define libglesv1 %mklibname %{glesv1name} %{glesv1major}
%define devglesv1 %mklibname %{glesv1name} -d

%define glesv2major 2
%define glesv2name GLESv2
%define libglesv2 %mklibname %{glesv2name}_ %{glesv2major}
%define devglesv2 %mklibname %{glesv2name} -d

%define devglesv3 %mklibname glesv3 -d

%define d3dmajor 1
%define d3dname d3dadapter9
%define libd3d %mklibname %{d3dname} %{d3dmajor}
%define devd3d %mklibname %{d3dname} -d

%define glapimajor 0
%define glapiname glapi
%define libglapi %mklibname %{glapiname} %{glapimajor}
%define devglapi %mklibname %{glapiname} -d

%define dridrivers %mklibname dri-drivers
%define vdpaudrivers %mklibname vdpau-drivers

%define gbmmajor 1
%define gbmname gbm
%define libgbm %mklibname %{gbmname} %{gbmmajor}
%define devgbm %mklibname %{gbmname} -d

%define xatrackermajor 2
%define xatrackername xatracker
%define libxatracker %mklibname %xatrackername %{xatrackermajor}
%define devxatracker %mklibname %xatrackername -d

%define swravxmajor 0
%define swravxname swravx
%define libswravx %mklibname %swravxname %{swravxmajor}

%define swravx2major 0
%define swravx2name swravx2
%define libswravx2 %mklibname %swravx2name %{swravx2major}

%define clmajor 1
%define clname mesaopencl
%define libcl %mklibname %clname %clmajor
%define devcl %mklibname %clname -d

%define mesasrcdir %{_prefix}/src/Mesa/
%define driver_dir %{_libdir}/dri

%define short_ver %(if [ `echo %{version} |cut -d. -f3` = "0" ]; then echo %{version} |cut -d. -f1-2; else echo %{version}; fi)

Summary:	OpenGL %{opengl_ver} compatible 3D graphics library
Name:		mesa
Version:	20.0.2
%if "%{relc}%{git}" == ""
Release:	1
%else
%if "%{relc}" != ""
%if "%{git}" != ""
Release:	%{?relc:0.rc%{relc}}.0.%{git}.1
%else
Release:	%{?relc:0.rc%{relc}}.1
%endif
%else
Release:	%{?git:0.%{git}.}1
%endif
%endif
Group:		System/Libraries
License:	MIT
Url:		http://www.mesa3d.org
%if "%{git}" != ""
Source0:	%{name}-%{git_branch}-%{git}.tar.xz
%else
Source0:	https://mesa.freedesktop.org/archive/mesa-%{version}%{vsuffix}.tar.xz
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install
Source100:	%{name}.rpmlintrc

%define dricoremajor 1
%define dricorename dricore
%define devdricore %mklibname %{dricorename} -d
%define libdricore %mklibname %{dricorename} 9

Obsoletes:	%{libdricore} < %{EVRD}
Obsoletes:	%{devdricore} < %{EVRD}
Obsoletes:	%{name}-xorg-drivers < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-radeon < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-nouveau < %{EVRD}

# https://bugs.freedesktop.org/show_bug.cgi?id=74098
#Patch1:		mesa-10.2-clang-compilefix.patch
#Patch3:		mesa-19.0.0-rc2-more-ARM-drivers.patch
Patch1:		mesa-19.2.3-arm32-buildfix.patch
Patch2:		mesa-20.0.0-rc1-amd-non-x86.patch
%ifarch %{ix86}
Patch4:		mesa-19.2.0-rc3-32bit-buildfix.patch
%endif
%ifarch %{armx} riscv64
Patch5:		mesa-19.2.0-rc3-meson-radeon-arm-riscv.patch
%endif
# https://gitlab.freedesktop.org/mesa/mesa/merge_requests/3449
Patch6:		https://gitlab.freedesktop.org/mesa/mesa/merge_requests/3449.patch
# fedora patches
#Patch15:	mesa-9.2-hardware-float.patch

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

# Mandriva & Mageia patches

# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'
#Patch201:	0201-revert-fix-glxinitializevisualconfigfromtags-handling.patch
#Patch202:	riscv64.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=110783
# https://gitlab.freedesktop.org/mesa/mesa/merge_requests/1084
#Patch203:	https://gitlab.freedesktop.org/mesa/mesa/merge_requests/1084.diff

# Direct3D patchset -- https://wiki.ixit.cz/d3d9
#
# git clone git://anongit.freedesktop.org/git/mesa/mesa
# git remote add ixit https://github.com/iXit/Mesa-3D
# git fetch ixit
# git checkout -b d3d9 ixit/master
# git rebase origin/master
# git format-patch origin/master
# ( for i in 00*.patch; do PN=`echo $i |cut -b1-4 |sed 's,^0*,,g'`; echo Patch$((PN+1000)): $i; done ) >patchlist
# Currently empty -- current D3D9 bits have been merged into 10.4.0-rc1
# Leaving the infrastructure in place for future updates.

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	gccmakedep
BuildRequires:	libxml2-python
BuildRequires:	makedepend
BuildRequires:	meson
BuildRequires:	lm_sensors-devel
BuildRequires:	llvm-devel >= 3.3
BuildRequires:	pkgconfig(expat)
BuildRequires:	elfutils-devel
%ifarch %{ix86}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	python-mako >= 0.8.0
BuildRequires:	pkgconfig(libdrm) >= 2.4.56
BuildRequires:	pkgconfig(libudev) >= 186
%if %{with glvnd}
BuildRequires:	pkgconfig(libglvnd)
%endif
%ifnarch %{armx} %{riscv}
# needed only for intel binaries
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(x11) >= 1.3.3
BuildRequires:	pkgconfig(xdamage) >= 1.1.1
BuildRequires:	pkgconfig(xext) >= 1.1.1
BuildRequires:	pkgconfig(xfixes) >= 4.0.3
BuildRequires:	pkgconfig(xi) >= 1.3
BuildRequires:	pkgconfig(xmu) >= 1.0.3
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xt) >= 1.0.5
BuildRequires:	pkgconfig(xxf86vm) >= 1.1.0
BuildRequires:	pkgconfig(xshmfence) >= 1.1
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xcb-dri3)
BuildRequires:	pkgconfig(xcb-present)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xvmc)
#BuildRequires:	pkgconfig(valgrind)
# for libsupc++.a
BuildRequires:	stdc++-static-devel
# (tpg) with openssl a steam crashes
# Program received signal SIGSEGV, Segmentation fault.
# 0xf63db8d5 in OPENSSL_ia32_cpuid () from /lib/libcrypto.so.1.0.0
# crypto is needed for shader cache which uses the SHA-1
# (tpg) strting from 2019-04-15 and openssl-1.1.1b-5 this is fixed
BuildRequires:	pkgconfig(libssl) >= 1.1.1b-5
%if %{with opencl}
BuildRequires:	pkgconfig(libclc)
BuildRequires:	clang-devel
BuildRequires:	clang
%endif
BuildRequires:	pkgconfig(xvmc)
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau) >= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva) >= 0.31.0
%endif
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-protocols) >= 1.8

# package mesa
Requires:	libGL.so.1%{_arch_tag_suffix}

%description
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.

%package -n %{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Requires:	%{dridrivers}-swrast = %{EVRD}
%ifnarch %{riscv}
Requires:	%{dridrivers}-virtio = %{EVRD}
%endif
%ifnarch %{armx} %{riscv}
%if %{with r600}
Requires:	%{dridrivers}-radeon = %{EVRD}
%endif
%ifarch %{ix86} %{x86_64}
Requires:	%{dridrivers}-intel = %{EVRD}
%endif
Requires:	%{dridrivers}-nouveau = %{EVRD}
%endif
%ifarch %{armx}
Requires:	%{dridrivers}-freedreno = %{EVRD}
Requires:	%{dridrivers}-vc4 = %{EVRD}
Requires:	%{dridrivers}-v3d = %{EVRD}
Requires:	%{dridrivers}-etnaviv = %{EVRD}
Requires:	%{dridrivers}-tegra = %{EVRD}
Requires:	%{dridrivers}-lima = %{EVRD}
Requires:	%{dridrivers}-panfrost = %{EVRD}
Requires:	%{dridrivers}-kmsro = %{EVRD}
%endif
Provides:	dri-drivers = %{EVRD}
Obsoletes:	%{_lib}XvMCgallium1 < %{EVRD}

%description -n %{dridrivers}
DRI and XvMC drivers.

%package -n %{dridrivers}-radeon
Summary:	DRI Drivers for AMD/ATI Radeon graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
Conflicts:	libva-vdpau-driver < 17.3.0

%description -n %{dridrivers}-radeon
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets

%package -n %{dridrivers}-vmwgfx
Summary:	DRI Drivers for VMWare guest OS
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-vmwgfx
DRI and XvMC drivers for VMWare guest Operating Systems.

%ifarch %{ix86} %{x86_64}
%package -n %{dridrivers}-intel
Summary:	DRI Drivers for Intel graphics chipsets
Group:		System/Libraries
Conflicts:	libva-vdpau-driver < 17.3.0
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
Suggests:	libvdpau-va-gl

%description -n %{dridrivers}-intel
DRI and XvMC drivers for Intel graphics chipsets
%endif

%package -n %{dridrivers}-nouveau
Summary:	DRI Drivers for NVIDIA graphics chipsets using the Nouveau driver
Group:		System/Libraries
Conflicts:	libva-vdpau-driver < 17.3.0
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-nouveau
DRI and XvMC drivers for Nvidia graphics chipsets

%package -n %{dridrivers}-swrast
Summary:	DRI Drivers for software rendering
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
Obsoletes:	%{libswravx} < %{EVRD}
Obsoletes:	%{libswravx2} < %{EVRD}

%description -n %{dridrivers}-swrast
Generic DRI driver using CPU rendering

%package -n %{dridrivers}-virtio
Summary:	DRI Drivers for virtual environments
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-virtio
Generic DRI driver for virtual environments.

%ifarch %{armx} %{riscv}
%package -n %{dridrivers}-freedreno
Summary:	DRI Drivers for Adreno graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-freedreno
DRI and XvMC drivers for Adreno graphics chipsets

%package -n %{dridrivers}-vc4
Summary:	DRI Drivers for Broadcom VC4 graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-vc4
DRI and XvMC drivers for Broadcom VC4 graphics chips

%package -n %{dridrivers}-v3d
Summary:	DRI Drivers for Broadcom VC5 graphics chipsets
Group:		System/Libraries

%description -n %{dridrivers}-v3d
DRI and XvMC drivers for Broadcom VC5 graphics chips

%package -n %{dridrivers}-etnaviv
Summary:	DRI Drivers for Vivante graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-etnaviv
DRI and XvMC drivers for Vivante graphics chips

%package -n %{dridrivers}-tegra
Summary:	DRI Drivers for Tegra graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-tegra
DRI and XvMC drivers for Tegra graphics chips

%package -n %{dridrivers}-lima
Summary:	DRI Drivers for Mali Utgard devices
Group:		System/Libraries

%description -n %{dridrivers}-lima
DRI drivers for Mali Utgard devices

%package -n %{dridrivers}-panfrost
Summary:	DRI Drivers for Mali Midgard and Bifrost devices
Group:		System/Libraries

%description -n %{dridrivers}-panfrost
DRI drivers for Mali Midgard and Bifrost devices

%package -n %{dridrivers}-kmsro
Summary:	DRI Drivers for KMS-only devices
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
%rename %{dridrivers}-pl111
%rename %{dridrivers}-imx

%description -n %{dridrivers}-kmsro
DRI and XvMC drivers for KMS renderonly layer devices
%endif

%package -n %{libosmesa}
Summary:	Mesa offscreen rendering library
Group:		System/Libraries

%description -n %{libosmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n %{devosmesa}
Summary:	Development files for libosmesa
Group:		Development/C
Requires:	%{libosmesa} = %{version}-%{release}

%description -n %{devosmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%package -n %{libgl}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Suggests:	%{dridrivers} >= %{version}-%{release}
Obsoletes:	%{_lib}mesagl1 < %{version}-%{release}
Requires:	%{_lib}udev1
Requires:	%{_lib}GL1%{?_isa}
Provides:	mesa-libGL%{?_isa} = %{EVRD}
Requires:	%mklibname GL 1
%if %{with glvnd}
Requires:	libglvnd-GL
%endif
%define oldglname %mklibname gl 1
%rename %oldglname

%description -n %{libgl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GL and GLX parts.

%package -n %{devgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
%ifarch armv7hl
# This will allow to install proprietary libGL library for ie. imx
Requires:	libGL.so.1%{_arch_tag_suffix}
# This is to prevent older version of being installed to satisfy dependency
Conflicts:	%{libgl} < %{version}-%{release}
%else
Requires:	%{libgl} = %{version}-%{release}
%endif
%if %{with glvnd}
Requires:	pkgconfig(libglvnd)
%endif
# GL/glext.h uses KHR/khrplatform.h
Requires:	%{devegl}  = %{EVRD}
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{version}-%{release}
%define oldlibgl %mklibname gl -d
%rename %oldlibgl

%description -n %{devgl}
This package contains the headers needed to compile Mesa programs.

%package -n %{devvulkan}
Summary:	Development files for the Intel Vulkan driver
Group:		Development/C
Requires:	pkgconfig(vulkan)
Provides:	vulkan-intel-devel = %{EVRD}

%description -n %{devvulkan}
This package contains the headers needed to compile applications
that use Intel Vulkan driver extras

%if %{with egl}
%package -n %{libegl}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0
Provides:	mesa-libEGL%{?_isa} = %{EVRD}
%if %{with glvnd}
Requires:	libglvnd-egl
%endif
%define oldegl %mklibname egl 1
%rename %oldegl

%description -n %{libegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
EGL parts.

%package -n %{devegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Provides:	egl-devel = %{version}-%{release}
Requires:	%{libegl} = %{version}-%{release}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{version}-%{release}
%define olddevegl %mklibname egl -d
%rename %olddevegl

%description -n %{devegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
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

%package -n %{libswravx}
Summary:	AVX Software rendering library for Mesa
Group:		System/Libraries

%description -n %{libswravx}
AVX Software rendering library for Mesa

%package -n %{libswravx2}
Summary:	AVX2 Software rendering library for Mesa
Group:		System/Libraries

%description -n %{libswravx2}
AVX2 Software rendering library for Mesa

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
Requires:	%{libglesv1}
%if %{with glvnd}
Requires:	libglvnd-GLESv1_CM
# For libGLESv1_CM.so symlink
Requires:	pkgconfig(libglvnd)
%endif
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{version}-%{release}

%description -n %{devglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%package -n %{libglesv2}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0
%if %{with glvnd}
# For libGLESv2.so symlink
Requires:	pkgconfig(libglvnd)
%endif

%description -n %{libglesv2}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%package -n %{devglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2}
%if %{with glvnd}
Requires:	libglvnd-GLESv2
%endif
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

%package -n %{libd3d}
Summary:	Mesa Gallium Direct3D 9 state tracker
Group:		System/Libraries

%description -n %{libd3d}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides Direct3D 9 support.

%package -n %{devd3d}
Summary:	Development files for Direct3D 9 libs
Group:		Development/C
Requires:	%{libd3d} = %{version}-%{release}
Provides:	d3d-devel = %{EVRD}

%description -n %{devd3d}
This package contains the headers needed to compile Direct3D 9 programs.

%if %{with opencl}
%package -n %{libcl}
Summary:	Mesa OpenCL libs
Group:		System/Libraries
Provides:	mesa-libOpenCL = %{EVRD}
Provides:	mesa-opencl = %{EVRD}

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
Provides:	%{clname}-devel = %{version}-%{release}
Provides:	mesa-libOpenCL-devel = %{EVRD}
Provides:	mesa-opencl-devel = %{EVRD}

%description -n %{devcl}
Development files for the OpenCL library
%endif

%if %{with vdpau}
%package -n %{vdpaudrivers}
Summary:	Mesa VDPAU drivers
Group:		System/Libraries
Requires:	%{dridrivers} = %{EVRD}
%ifnarch %{armx} %{riscv}
Requires:	%{_lib}vdpau-driver-nouveau
Requires:	%{_lib}vdpau-driver-r300
Requires:	%{_lib}vdpau-driver-radeonsi
%if %{with r600}
Requires:	%{_lib}vdpau-driver-r600
%endif
%endif
Requires:	%{_lib}vdpau-driver-softpipe
Provides:	vdpau-drivers = %{EVRD}

%description -n %{vdpaudrivers}
VDPAU drivers.

%package -n %{_lib}vdpau-driver-nouveau
Summary:	VDPAU plugin for nouveau driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-nouveau
This packages provides a VPDAU plugin to enable video acceleration
with the nouveau driver.

%package -n %{_lib}vdpau-driver-r300
Summary:	VDPAU plugin for r300 driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-r300
This packages provides a VPDAU plugin to enable video acceleration
with the r300 driver.

%package -n %{_lib}vdpau-driver-r600
Summary:	VDPAU plugin for r600 driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-r600
This packages provides a VPDAU plugin to enable video acceleration
with the r600 driver.

%package -n %{_lib}vdpau-driver-radeonsi
Summary:	VDPAU plugin for radeonsi driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-radeonsi
This packages provides a VPDAU plugin to enable video acceleration
with the radeonsi driver.

%package -n %{_lib}vdpau-driver-softpipe
Summary:	VDPAU plugin for softpipe driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-softpipe
This packages provides a VPDAU plugin to enable video acceleration
with the softpipe driver.
%endif

%if %{with egl}
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
%endif

%package common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{devgl} = %{version}-%{release}
Requires:	%{devegl} = %{version}-%{release}
Requires:	%{devglapi} = %{version}-%{release}
%if ! %{with glvnd}
Requires:	%{devglesv1} = %{version}-%{release}
Requires:	%{devglesv2} = %{version}-%{release}
%endif
Suggests:	%{devd3d} = %{version}-%{release}
%if %{with glvnd}
Requires:	pkgconfig(libglvnd)
Requires:	pkgconfig(glesv1_cm)
Requires:	pkgconfig(glesv2)
%endif

%description common-devel
Mesa common metapackage devel.

%package tools
Summary:	Tools for debugging Mesa drivers
Group:		Development/Tools

%description tools
Tools for debugging Mesa drivers.

%prep
%if "%{git}" != ""
%autosetup -p1 -n %{name}-%{git_branch}-%{git}
%else
%autosetup -p1 -n mesa-%{version}%{vsuffix}
%endif
chmod +x %{SOURCE5}

# this is a hack for S3TC support. r200_screen.c is symlinked to
# radeon_screen.c in git, but is its own file in the tarball.
cp -f src/mesa/drivers/dri/{radeon,r200}/radeon_screen.c || :

%build
%if %{with gcc}
export CC=gcc
export CXX=g++
%else
%global ldflags %{ldflags} -fuse-ld=gold
%endif

if ! %meson \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Ddri-drivers=auto \
	-Dgallium-drivers=auto \
%if %{with opencl}
	-Dgallium-opencl=icd \
%else
	-Dgallium-opencl=disabled \
%endif
	-Dgallium-va=true \
	-Dgallium-vdpau=true \
	-Dgallium-xa=true \
	-Dgallium-xvmc=true \
	-Dgallium-nine=true \
	-Dglx=auto \
	-Dplatforms=auto \
	-Dvulkan-drivers=auto \
	-Dxlib-lease=auto \
	-Dosmesa=gallium \
%if %{with glvnd}
	-Dglvnd=true \
%endif
	-Ddri3=true \
	-Degl=true \
	-Dgbm=true \
	-Dgles1=true \
	-Dgles2=true \
	-Dglx-direct=true \
	-Dllvm=true \
	-Dlmsensors=true \
	-Dopengl=true \
	-Dshader-cache=true \
	-Dshared-glapi=true \
	-Dshared-llvm=true \
	-Dswr-arches=avx,avx2,knl,skx \
	-Dselinux=false \
	-Dbuild-tests=false \
	-Dtools=all; then

	cat build/meson-logs/meson-log.txt >/dev/stderr
fi

%ninja_build -C build/

%install
%ninja_install -C build/

%if %{with glvnd}
rm -rf	%{buildroot}%{_includedir}/GL/gl.h \
	%{buildroot}%{_includedir}/GL/glcorearb.h \
	%{buildroot}%{_includedir}/GL/glext.h \
	%{buildroot}%{_includedir}/GL/glx.h \
	%{buildroot}%{_includedir}/GL/glxext.h \
	%{buildroot}%{_includedir}/EGL/eglext.h \
	%{buildroot}%{_includedir}/EGL/egl.h \
	%{buildroot}%{_includedir}/EGL/eglplatform.h \
	%{buildroot}%{_includedir}/KHR \
	%{buildroot}%{_includedir}/GLES \
	%{buildroot}%{_includedir}/GLES2 \
	%{buildroot}%{_includedir}/GLES3 \
	%{buildroot}%{_libdir}/pkgconfig/egl.pc \
	%{buildroot}%{_libdir}/pkgconfig/gl.pc
%endif

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

%if %{with opencl}
# FIXME workaround for OpenCL headers not being installed
if [ -e %{buildroot}%{_includedir}/CL/opencl.h ]; then
    echo OpenCL headers are being installed correctly now. Please remove the workaround.
    exit 1
else
    cp -af include/CL %{buildroot}%{_includedir}/
fi
%endif

# .so files are not needed by vdpau
rm -f %{buildroot}%{_libdir}/vdpau/libvdpau_*.so

%if %{with glvnd}
# We get those from libglvnd
rm -f %{buildroot}%{_libdir}/libGLESv1_CM.so* %{buildroot}%{_libdir}/libGLESv2.so*
%endif

# .la files are not needed by mesa
find %{buildroot} -name '*.la' |xargs rm -f

%if ! %{with glvnd}
# Used to be present in 19.0.x, and some packages rely on it
cat >%{buildroot}%{_libdir}/pkgconfig/glesv1_cm.pc <<'EOF'
Name: glesv1_cm
Description: Mesa OpenGL ES 1.1 CM library
Version: %{version}
Libs: -lGLESv1_CM
Libs.private: -lpthread -pthread -lm -ldl
EOF
cat >%{buildroot}%{_libdir}/pkgconfig/glesv2.pc <<'EOF'
Name: glesv2
Description: Mesa OpenGL ES 2.0 library
Version: %{version}
Libs: -lGLESv2
Libs.private: -lpthread -pthread -lm -ldl
EOF

# Used to be present in 19.1.x, and some packages rely on it
cat >%{buildroot}%{_libdir}/pkgconfig/egl.pc <<'EOF'
prefix=%{_prefix}
libdir=${prefix}/%{_libdir}
includedir=${prefix}/include
Name: egl
Description: Mesa EGL Library
Version: %{version}
Requires.private: x11, xext, xdamage >=  1.1, xfixes, x11-xcb, xcb, xcb-glx >=  1.8.1, xcb-dri2 >=  1.8, xxf86vm, libdrm >=  2.4.75
Libs: -L${libdir} -lEGL
Libs.private: -lpthread -pthread -lm -ldl
Cflags: -I${includedir}
EOF
%endif

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

# (tpg) remove wayland files as they are now part of wayland package
rm -rf %{buildroot}%{_libdir}/libwayland-egl.so*
rm -rf %{buildroot}%{_libdir}/pkgconfig/wayland-egl.pc

%files
%doc docs/README.*
%{_datadir}/drirc.d

%files -n %{dridrivers}

%files -n %{dridrivers}-radeon
%{_libdir}/dri/r?00_dri.so
%{_libdir}/dri/radeon_dri.so
%{_libdir}/libXvMCgallium.so
%{_libdir}/libXvMCr?00.so
%{_libdir}/dri/radeonsi_dri.so
%{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_r?00.so
%endif
%if %{with r600}
%if %{with va}
%{_libdir}/dri/r600_drv_video.so
%endif
%if %{with va}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_radeonsi.so
%endif
%endif

%ifarch %{ix86} %{x86_64}
%files -n %{dridrivers}-vmwgfx
%{_libdir}/dri/vmwgfx_dri.so
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_vmwgfx.so
%endif

%files -n %{dridrivers}-intel
%{_libdir}/dri/i9?5_dri.so
%{_libdir}/dri/iris_dri.so
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif

%files -n %{dridrivers}-nouveau
%{_libdir}/dri/nouveau*_dri.so
%{_libdir}/libXvMCnouveau.so
%if %{with va}
%{_libdir}/dri/nouveau_drv_video.so
%endif
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_nouveau.so
%endif

%files -n %{dridrivers}-swrast
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/kms_swrast_dri.so
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_swrast.so
%endif

%ifnarch %{riscv}
%files -n %{dridrivers}-virtio
%{_libdir}/dri/virtio_gpu_dri.so
%endif

%ifarch %{armx}
%files -n %{dridrivers}-freedreno
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%{_libdir}/libfreedreno_noop_drm_shim.so
%if %{with opencl}
%{_libdir}/gallium-pipe/pipe_msm.so
%endif

%files -n %{dridrivers}-vc4
%{_libdir}/dri/vc4_dri.so

%files -n %{dridrivers}-v3d
%{_libdir}/dri/v3d_dri.so
%{_libdir}/libv3d_noop_drm_shim.so

%files -n %{dridrivers}-etnaviv
%{_libdir}/dri/etnaviv_dri.so
%{_libdir}/libetnaviv_noop_drm_shim.so

%files -n %{dridrivers}-tegra
%{_libdir}/dri/tegra_dri.so

%files -n %{dridrivers}-lima
%{_bindir}/lima_compiler
%{_bindir}/lima_disasm
%{_libdir}/dri/lima_dri.so
%{_libdir}/gallium-pipe/pipe_kmsro.so


%files -n %{dridrivers}-panfrost
%{_libdir}/dri/panfrost_dri.so

%files -n %{dridrivers}-kmsro
%{_libdir}/dri/armada-drm_dri.so
%{_libdir}/dri/exynos_dri.so
%{_libdir}/dri/hx8357d_dri.so
%{_libdir}/dri/ili9???_dri.so
%{_libdir}/dri/imx-drm_dri.so
%{_libdir}/dri/imx-dcss_dri.so
%{_libdir}/dri/ingenic-drm_dri.so
%{_libdir}/dri/mcde_dri.so
%{_libdir}/dri/meson_dri.so
%{_libdir}/dri/mi0283qt_dri.so
%{_libdir}/dri/mxsfb-drm_dri.so
%{_libdir}/dri/pl111_dri.so
%{_libdir}/dri/repaper_dri.so
%{_libdir}/dri/rockchip_dri.so
%{_libdir}/dri/st7586_dri.so
%{_libdir}/dri/st7735r_dri.so
%{_libdir}/dri/stm_dri.so
%{_libdir}/dri/sun4i-drm_dri.so
%endif

%files -n %{libosmesa}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{devosmesa}
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files -n %{libgl}
%if %{with glvnd}
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libGLX_mesa.so.0*
%endif
%dir %{_libdir}/dri
%if %{with opencl}
%dir %{_libdir}/gallium-pipe
%endif

%if %{with egl}
%files -n %{libegl}
%{_libdir}/libEGL_mesa.so.%{eglmajor}*
%endif

%files -n %{libglapi}
%{_libdir}/libglapi.so.%{glapimajor}*

%if ! %{with bootstrap}
%files -n %{libxatracker}
%{_libdir}/libxatracker.so.%{xatrackermajor}*
%endif

%if 0
%files -n %{libglesv1}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2}
%{_libdir}/libGLESv2.so.%{glesv2major}*
%endif

%files -n %{libd3d}
%dir %{_libdir}/d3d
%{_libdir}/d3d/d3dadapter9.so.%{d3dmajor}*

%if %{with opencl}
%files -n %{libcl}
%{_sysconfdir}/OpenCL
%{_libdir}/libMesaOpenCL.so.%{clmajor}*
%endif

%if %{with egl}
%files -n %{libgbm}
%{_libdir}/libgbm.so.%{gbmmajor}*
%endif

%files -n %{devgl}
%if ! %{with glvnd}
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glcorearb.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_libdir}/pkgconfig/gl.pc
%endif
%if %{with glvnd}
%{_libdir}/libGLX_mesa.so
%endif
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files common-devel
# meta devel pkg

%if %{with egl}
%files -n %{devegl}
%if ! %{with glvnd}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/pkgconfig/egl.pc
%else
%{_includedir}/EGL/eglextchromium.h
%{_includedir}/EGL/eglmesaext.h
%endif
%{_libdir}/libEGL_mesa.so
%endif

%files -n %{devglapi}
%{_libdir}/libglapi.so

#vdpau enblaed
%if %{with vdpau}
%files -n %{vdpaudrivers}

%files -n %{_lib}vdpau-driver-nouveau
%{_libdir}/vdpau/libvdpau_nouveau.so.*

%files -n %{_lib}vdpau-driver-r300
%{_libdir}/vdpau/libvdpau_r300.so.*

%if %{with r600}
%files -n %{_lib}vdpau-driver-r600
%{_libdir}/vdpau/libvdpau_r600.so.*

%files -n %{_lib}vdpau-driver-radeonsi
%{_libdir}/vdpau/libvdpau_radeonsi.so.*
%endif

%files -n %{_lib}vdpau-driver-softpipe
%endif

%if ! %{with bootstrap}
%files -n %{devxatracker}
%{_libdir}/libxatracker.so
%{_includedir}/xa_*.h
%{_libdir}/pkgconfig/xatracker.pc
%endif

%if ! %{with glvnd}
%files -n %{devglesv1}
%{_includedir}/GLES
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{devglesv2}
%{_includedir}/GLES2
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{devglesv3}
%{_includedir}/GLES3
%endif

%files -n %{devd3d}
%{_includedir}/d3dadapter
%{_libdir}/d3d/d3dadapter9.so
%{_libdir}/pkgconfig/d3d.pc

%if %{with opencl}
%files -n %{devcl}
%{_includedir}/CL
%{_libdir}/libMesaOpenCL.so
%endif

%if %{with egl}
%files -n %{devgbm}
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc
%endif

%ifarch %{ix86} %{x86_64}
%files -n %{devvulkan}
%{_includedir}/vulkan/vulkan_intel.h
%endif

%files tools
%ifarch %{ix86} %{x86_64}
%{_bindir}/aubinator
%{_bindir}/aubinator_error_decode
%{_bindir}/aubinator_viewer
%{_bindir}/i965_asm
%{_bindir}/i965_disasm
%{_bindir}/intel_dump_gpu
%{_bindir}/intel_error2aub
%{_bindir}/intel_sanitize_gpu
%{_libexecdir}/libintel_dump_gpu.so
%{_libexecdir}/libintel_sanitize_gpu.so
%endif
%ifarch %{armx}
%{_bindir}/etnaviv_compiler
%{_bindir}/ir3_compiler
%endif
%{_bindir}/glsl_compiler
%{_bindir}/glsl_test
%{_bindir}/nouveau_compiler
%{_bindir}/spirv2nir
%{_bindir}/xvmc_bench
%{_bindir}/xvmc_blocks
%{_bindir}/xvmc_context
%{_bindir}/xvmc_rendering
%{_bindir}/xvmc_subpicture
%{_bindir}/xvmc_surface

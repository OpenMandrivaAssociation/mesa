# (cg) Cheater...
%define Werror_cflags %{nil}

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

# LTOing Mesa takes insane amounts of RAM :/
# So you may want to disable it for anything
# but final builds...
#define _disable_lto 1

# Mesa is used by wine and steam
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# -fno-strict-aliasing is added because of numerous warnings, strict
# aliasing might generate broken code.
# (tpg) imho -g3 here is for someone who is developing graphics drivers
# or trying to pin point a specific issue. Nobody install debug symbols by default
%ifarch %{aarch64}
# In LLVM 18.0.0-rc1, O3 on aarch64 results in a build failure
%global optflags %{optflags} -O2 -fno-strict-aliasing -g1 -flto=thin
%else
%global optflags %{optflags} -O3 -fno-strict-aliasing -g1 -flto=thin
%endif
%global build_ldflags %{build_ldflags} -fno-strict-aliasing -flto=thin -Wl,--undefined-version

#define git 20240114
%define git_branch main
#define git_branch %(echo %{version} |cut -d. -f1-2)
%define relc 3

%ifarch %{riscv}
%bcond_with gcc
%bcond_with opencl
%else
%bcond_with gcc
%bcond_without opencl
%endif

%bcond_without rust
%bcond_without rusticl
%bcond_without vdpau
%bcond_without va
%bcond_without egl
%ifarch %{ix86} %{x86_64}
%bcond_without intel
%else
%bcond_with intel
%endif
# aubinator_viewer (part of Intel bits) requires gtk
# which in turn requires mesa, breaking bootstrapping
%bcond_with aubinatorviewer
# Sometimes it's necessary to disable r600 while bootstrapping
# an LLVM change (such as the r600 -> AMDGPU rename)
%bcond_without r600

%define vsuffix %{?relc:-rc%{relc}}%{!?relc:%{nil}}

%define eglmajor 0
%define eglname EGL_mesa
%define libegl %mklibname %{eglname} %{eglmajor}
%define devegl %mklibname %{eglname} -d
%define lib32egl lib%{eglname}%{eglmajor}
%define dev32egl lib%{eglname}-devel

%define glmajor 0
%define glname GLX_mesa
%define libgl %mklibname %{glname} %{glmajor}
%define devgl %mklibname GL -d
%define lib32gl lib%{glname}%{glmajor}
%define dev32gl libGL-devel

%define devvulkan %mklibname vulkan-intel -d
%define dev32vulkan libvulkan-intel-devel

%define glesv1major 1
%define glesv1name GLESv1_CM
%define libglesv1 %mklibname %{glesv1name} %{glesv1major}
%define devglesv1 %mklibname %{glesv1name} -d
%define lib32glesv1 lib%{glesv1name}%{glesv1major}
%define dev32glesv1 lib%{glesv1name}-devel

%define glesv2major 2
%define glesv2name GLESv2
%define libglesv2 %mklibname %{glesv2name}_ %{glesv2major}
%define devglesv2 %mklibname %{glesv2name} -d
%define lib32glesv2 lib%{glesv2name}_%{glesv2major}
%define dev32glesv2 lib%{glesv2name}-devel

%define devglesv3 %mklibname glesv3 -d
%define dev32glesv3 libglesv3-devel

%define dridrivers %mklibname dri-drivers
%define vdpaudrivers %mklibname vdpau-drivers
%define dridrivers32 libdri-drivers

%define gbmmajor 1
%define gbmname gbm
%define libgbm %mklibname %{gbmname} %{gbmmajor}
%define devgbm %mklibname %{gbmname} -d
%define lib32gbm lib%{gbmname}%{gbmmajor}
%define dev32gbm lib%{gbmname}-devel

%define swravxmajor 0
%define swravxname swravx
%define libswravx %mklibname %swravxname %{swravxmajor}
%define lib32swravx lib%{swravxname}%{swravxmajor}

%define swravx2major 0
%define swravx2name swravx2
%define libswravx2 %mklibname %swravx2name %{swravx2major}
%define lib32swravx2 lib%{swravx2name}%{swravx2major}

%define librusticl %mklibname RusticlOpenCL

# This has been removed in 25.0, but we still need to
# do the macro definitions so we can obsolete the packages
%define glapimajor 0
%define glapiname glapi
%define libglapi %mklibname %{glapiname} %{glapimajor}
%define devglapi %mklibname %{glapiname} -d
%define lib32glapi lib%{glapiname}%{glapimajor}
%define dev32glapi lib%{glapiname}-devel

%define mesasrcdir %{_prefix}/src/Mesa/
%define driver_dir %{_libdir}/dri

%define short_ver %(if [ $(echo %{version} |cut -d. -f3) = "0" ]; then echo %{version} |cut -d. -f1-2; else echo %{version}; fi)

Summary:	OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library
Name:		mesa
Version:	25.2.0
Release:	%{?relc:0.rc%{relc}.}%{?git:0.%{git}.}1
Group:		System/Libraries
License:	MIT
Url:		https://www.mesa3d.org
%if 0%{?git:1}
%if "%{git_branch}" == "panthor" || "%{git_branch}" == "panfrost"
Source0:	https://gitlab.freedesktop.org/panfrost/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
%else
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{git_branch}/mesa-%{git_branch}.tar.bz2#/mesa-%{git }.tar.bz2
%endif
%else
Source0:	https://mesa.freedesktop.org/archive/mesa-%{version}%{vsuffix}.tar.xz
%endif
Source100:	%{name}.rpmlintrc

%define dricoremajor 1
%define dricorename dricore
%define devdricore %mklibname %{dricorename} -d
%define libdricore %mklibname %{dricorename} 9
%define dev32dricore lib%{dricorename}-devel
%define lib32dricore lib%{dricorename}9

Obsoletes:	%{libdricore} < %{EVRD}
Obsoletes:	%{devdricore} < %{EVRD}
Obsoletes:	%{name}-xorg-drivers < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-radeon < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-nouveau < %{EVRD}

# Dropped in 25.1
%define xatrackermajor 2
%define xatrackername xatracker
%define libxatracker %mklibname %xatrackername %{xatrackermajor}
%define devxatracker %mklibname %xatrackername -d
%define lib32xatracker lib%{xatrackername}%{xatrackermajor}
%define dev32xatracker lib%{xatrackername}-devel
Obsoletes:	%{libxatracker} < %{EVRD}
Obsoletes:	%{devxatracker} < %{EVRD}
%if %{with compat32}
Obsoletes:	%{lib32xatracker} < %{EVRD}
Obsoletes:	%{dev32xatracker} < %{EVRD}
%endif
%define d3dmajor 1
%define d3dname d3dadapter9
%define libd3d %mklibname %{d3dname} %{d3dmajor}
%define devd3d %mklibname %{d3dname} -d
%define lib32d3d lib%{d3dname}%{d3dmajor}
%define dev32d3d lib%{d3dname}-devel
Obsoletes:	%{libd3d} < %{EVRD}
Obsoletes:	%{devd3d} < %{EVRD}
%if %{with compat32}
Obsoletes:	%{lib32d3d} < %{EVRD}
Obsoletes:	%{dev32d3d} < %{EVRD}
%endif

# Without this patch, the OpenCL ICD calls into MesaOpenCL,
# which for some reason calls back into the OpenCL ICD instead
# of calling its own function by the same name.
# (Probably related to -Bsymbolic/-Bsymbolic-functions)
#Patch0:		mesa-20.1.1-fix-opencl.patch
# Use llvm-config to detect llvm, since the newer method
# finds /usr/lib64/libLLVM-17.so even for 32-bit builds
Patch1:		mesa-23.1-x86_32-llvm-detection.patch
# Fix intel-vk build with clang 16 and gcc 13
#Patch2:		mesa-23.1-intel-vk-compile.patch
# find opencl-c-base.h even when crosscompiling
Patch3:		mesa-24.1-find-opencl-c-base.h.patch
Patch4:		mesa-23.3.0-rc4-panfrost-enable-gl3-by-default.patch
# Not used in the spec; this is a test case to verify patch0
# is still needed. If this code works without the patch, the
# patch can be removed. If it crashes/takes forever (infinite
# loop), the patch is still needed.
Source50:	test.c

#Patch1:		mesa-19.2.3-arm32-buildfix.patch
#Patch2:		mesa-20.3.4-glibc-2.33.patch
Patch5:		mesa-20.3.0-meson-radeon-arm-riscv-ppc.patch

# FIXME is there a better way to teach meson about
# rust cruft?
#Patch6:		mesa-rustdeps.patch

Patch7:		mesa-24-llvmspirv-detection.patch
Patch8:		mesa-buildsystem-improvements.patch
Patch9:		mesa-24.0-llvmspirvlib-version-check.patch
#Patch10:	mesa-24.0.2-buildfix32.patch
###FIXME Patch11:	enable-vulkan-video-decode.patch
#Patch12:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31950.patch
Patch13:	mesa-25.2-llvm-21.patch
Patch14:	mesa-25.2-aarch64-compile.patch

# Panthor -- https://gitlab.freedesktop.org/bbrezillon/mesa.git
# Currently no patches required

# From upstream
# [currently nothing]

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libxml2-python
BuildRequires:	meson
BuildRequires:	lm_sensors-devel
BuildRequires:	cmake(LLVM)
BuildRequires:	pkgconfig(LLVMSPIRVLib)
BuildRequires:	pkgconfig(expat)
BuildRequires:	elfutils-devel
%ifarch %{ix86}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	python
BuildRequires:	python%{pyver}dist(ply)
BuildRequires:	python%{pyver}dist(pyyaml)
BuildRequires:	python%{pyver}dist(mako) >= 0.8.0
%ifarch %{arm} %{armx} %{riscv}
# For etnaviv
BuildRequires:	python%{pyver}dist(pycparser)
%endif
BuildRequires:	pkgconfig(libdrm) >= 2.4.56
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(libglvnd)
%ifnarch %{armx} %{riscv}
%if %{with aubinatorviewer}
# needed only for intel binaries
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
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
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(valgrind)
# for libsupc++.a
BuildRequires:	stdc++-static-devel
BuildRequires:	cmake(Polly)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(libunwind)
%if %{with opencl}
BuildRequires:	pkgconfig(libclc)
BuildRequires:	libclc-amdgcn
BuildRequires:	libclc-spirv
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(OpenCLHeaders)
BuildRequires:	cmake(OpenCLICDLoader)
BuildRequires:	clang
%endif
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau) >= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva) >= 0.31.0
%endif
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-protocols) >= 1.8
BuildRequires:	glslang

%if %{with rusticl}
BuildRequires:	rust
BuildRequires:	rust-bindgen-cli
BuildRequires:	cbindgen
%endif

%if %{with rust}
BuildRequires:	rust
BuildRequires:	crate(proc-macro2)
BuildRequires:	crate(quote)
BuildRequires:	crate(syn)
BuildRequires:	crate(unicode-ident)
BuildRequires:	crate(paste)
BuildRequires:	crate(rustc-hash)
# For etnaviv
BuildRequires:	crate(indexmap)
%endif

# package mesa
Requires:	libGL.so.1%{_arch_tag_suffix}

%if %{with compat32}
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXdamage)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXmu)
BuildRequires:	devel(libXt)
BuildRequires:	devel(libXxf86vm)
BuildRequires:	devel(libxshmfence)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libxcb-dri3)
BuildRequires:	devel(libxcb-present)
BuildRequires:	devel(libXv)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libsensors)
BuildRequires:	libsensors.so.5
BuildRequires:	devel(libLLVM)
BuildRequires:	devel(libclang)
BuildRequires:	devel(libzstd)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libelf)
BuildRequires:	libunwind-nongnu-devel
BuildRequires:	devel(libva)
BuildRequires:	devel(libz)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libvdpau)
BuildRequires:	devel(libOpenGL)
BuildRequires:	devel(libGLdispatch)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libatomic)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libSPIRV-Tools-shared)
BuildRequires:	devel(libvulkan)
BuildRequires:	libLLVMSPIRVLib-devel
BuildRequires:	libLLVMSPIRVLib-static-devel
%endif

%description
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.

%package -n %{dridrivers}
Summary:	Mesa DRI and Vulkan drivers
Group:		System/Libraries
%rename		%{dridrivers}-swrast
Conflicts:	%{dridrivers}-swrast <= 22.0.0-0.rc2.1
%ifnarch %{riscv}
%rename		%{dridrivers}-virtio
Conflicts:	%{dridrivers}-virtio <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-vmwgfx
Conflicts:	%{dridrivers}-vmwgfx <= 22.0.0-0.rc2.1
%endif
%ifnarch %{armx} %{riscv}
%if %{with r600}
%rename		%{dridrivers}-radeon
Conflicts:	%{dridrivers}-radeon <= 22.0.0-0.rc2.1
%endif
%ifarch %{ix86} %{x86_64}
Suggests:	libvdpau-va-gl
%rename		%{dridrivers}-intel
Conflicts:	%{dridrivers}-intel <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-iris
Conflicts:	%{dridrivers}-iris <= 22.0.0-0.rc2.1
%endif
%rename		%{dridrivers}-nouveau
Conflicts:	%{dridrivers}-nouveau <= 22.0.0-0.rc2.1
%endif
%ifarch %{armx}
%rename		%{dridrivers}-freedreno
Conflicts:	%{dridrivers}-freedreno <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-vc4
Conflicts:	%{dridrivers}-vc4 <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-v3d
Conflicts:	%{dridrivers}-v3d <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-etnaviv
Conflicts:	%{dridrivers}-etnaviv <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-tegra
Conflicts:	%{dridrivers}-tegra <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-lima
Conflicts:	%{dridrivers}-lima <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-panfrost
Conflicts:	%{dridrivers}-panfrost <= 22.0.0-0.rc2.1
%rename		%{dridrivers}-kmsro
Conflicts:	%{dridrivers}-kmsro <= 22.0.0-0.rc2.1
%endif
# Old OM package
Provides:	dri-drivers = %{EVRD}
# Fedora naming, compat Provides: needed to make the
# zoom RPM install
Provides:	mesa-dri-drivers = %{EVRD}
Requires:	vulkan-loader
Obsoletes:	%{_lib}XvMCgallium1 <= 22.0.0-0.rc2.1

%description -n %{dridrivers}
DRI and Vulkan drivers.

%ifarch %{armx} %{riscv}
%package -n freedreno-tools
Summary:	Tools for debugging the Freedreno graphics driver
Requires:	%{dridrivers} = %{EVRD}

%description -n freedreno-tools
Tools for debugging the Freedreno graphics driver.
%endif

%package -n %{libgl}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Suggests:	%{dridrivers} >= %{EVRD}
Obsoletes:	%{_lib}mesagl1 < %{EVRD}
Requires:	%{_lib}udev1
Requires:	%{_lib}GL1%{?_isa}
Provides:	mesa-libGL%{?_isa} = %{EVRD}
Requires:	%mklibname GL 1
Requires:	libglvnd-GL%{?_isa}
%define oldglname %mklibname gl 1
%rename %oldglname
Obsoletes:	%{libglapi} < %{EVRD}

%description -n %{libgl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GL and GLX parts.

%package -n %{devgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
%ifarch armv7hl
# This will allow to install proprietary libGL library for ie. imx
Requires:	libGL.so.1%{_arch_tag_suffix}
# This is to prevent older version of being installed to satisfy dependency
Conflicts:	%{libgl} < %{EVRD}
%else
Requires:	%{libgl} = %{EVRD}
%endif
Requires:	pkgconfig(libglvnd)
# GL/glext.h uses KHR/khrplatform.h
Requires:	%{devegl}  = %{EVRD}
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{EVRD}
Obsoletes:	%{devglapi} < %{EVRD}
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
that use Intel Vulkan driver extras.

%if %{with egl}
%package -n %{libegl}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0
Provides:	mesa-libEGL%{?_isa} = %{EVRD}
Requires:	libglvnd-egl%{?_isa}
%define oldegl %mklibname egl 1
%rename %oldegl

%description -n %{libegl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
EGL parts.

%package -n %{devegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Provides:	egl-devel = %{EVRD}
Requires:	%{libegl} = %{EVRD}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{EVRD}
%define olddevegl %mklibname egl -d
%rename %olddevegl

%description -n %{devegl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
EGL development parts.
%endif

%package -n %{libswravx}
Summary:	AVX Software rendering library for Mesa
Group:		System/Libraries

%description -n %{libswravx}
AVX Software rendering library for Mesa.

%package -n %{libswravx2}
Summary:	AVX2 Software rendering library for Mesa
Group:		System/Libraries

%description -n %{libswravx2}
AVX2 Software rendering library for Mesa.

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
Requires:	libglvnd-GLESv1_CM%{?_isa}
# For libGLESv1_CM.so symlink
Requires:	pkgconfig(libglvnd)
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{EVRD}

%description -n %{devglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%package -n %{libglesv2}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0
# For libGLESv2.so symlink
Requires:	pkgconfig(libglvnd)

%description -n %{libglesv2}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%package -n %{devglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2}
Requires:	libglvnd-GLESv2%{?_isa}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{EVRD}

%description -n %{devglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%package -n %{devglesv3}
Summary:	Development files for glesv3 libs
Group:		Development/C
# there is no pkgconfig
Provides:	glesv3-devel = %{EVRD}

%description -n %{devglesv3}
This package contains the headers needed to compile OpenGL ES 3 programs.

%if %{with compat32}
%package -n %{dridrivers32}
Summary:	Mesa DRI and Vulkan drivers (32-bit)
Group:		System/Libraries
%rename		%{dridrivers32}-swrast
Conflicts:	%{dridrivers32}-swrast <= 22.0.0-0.rc2.1
%if %{with r600}
%rename		%{dridrivers32}-radeon
Conflicts:	%{dridrivers32}-radeon <= 22.0.0-0.rc2.1
%endif
%rename		%{dridrivers32}-intel
Conflicts:	%{dridrivers32}-intel <= 22.0.0-0.rc2.1
%rename		%{dridrivers32}-iris
Conflicts:	%{dridrivers32}-iris <= 22.0.0-0.rc2.1
%rename		%{dridrivers32}-nouveau
Conflicts:	%{dridrivers32}-nouveau <= 22.0.0-0.rc2.1
%rename		libvdpau-drivers
Requires:	libvulkan1

%description -n %{dridrivers32}
DRI and Vulkan drivers.

%package -n %{lib32gl}
Summary:	Files for Mesa (GL and GLX libs) (32-bit)
Group:		System/Libraries
Suggests:	%{dridrivers32} >= %{EVRD}
Obsoletes:	%{lib32glapi} < %{EVRD}

%description -n %{lib32gl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GL and GLX parts.

%package -n %{dev32gl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib) (32-bit)
Group:		Development/C
Requires:	devel(libGL)
Requires:	%{dev32egl} = %{EVRD}
Requires:	%{devgl} = %{EVRD}
Obsoletes:	%{dev32glapi} < %{EVRD}

%description -n %{dev32gl}
This package contains the headers needed to compile Mesa programs.

%package -n %{lib32gbm}
Summary:	Files for Mesa (gbm libs) (32-bit)
Group:		System/Libraries

%description -n %{lib32gbm}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%package -n %{dev32gbm}
Summary:	Development files for Mesa (gbm libs) (32-bit)
Group:		Development/C
Requires:	%{devgbm} = %{EVRD}
Requires:	%{lib32gbm} = %{EVRD}

%description -n %{dev32gbm}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.

%package -n %{lib32egl}
Summary:	Files for Mesa (EGL libs) (32-bit)
Group:		System/Libraries
Requires:	libglvnd-egl%{?_isa}

%description -n %{lib32egl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
EGL parts.

%package -n %{dev32egl}
Summary:	Development files for Mesa (EGL libs) (32-bit)
Group:		Development/C
Requires:	%{lib32egl} = %{EVRD}
Requires:	%{devegl} = %{EVRD}

%description -n %{dev32egl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
EGL development parts.
%endif

%if %{with rusticl}
%package -n %{librusticl}
Summary:	Mesa Rusticl OpenCL libs
Group:		System/Libraries
Provides:	mesa-rusticl = %{EVRD}
Requires:	libclc-spirv
Recommends:	%{_lib}OpenCL
%define clmajor 1
%define clname mesaopencl
%define libcl %mklibname %clname %clmajor
%define devcl %mklibname %clname -d
%define lib32cl lib%{clname}%{clmajor}
%define dev32cl lib%{clname}-devel
Obsoletes: %{libcl} < %{EVRD}
Obsoletes: %{devcl} < %{EVRD}
%if %{with compat32}
Obsoletes: %{lib32cl} < %{EVRD}
Obsoletes: %{dev32cl} < %{EVRD}
%endif

%description -n %{librusticl}
Open Computing Language (OpenCL) is a framework for writing programs that
execute across heterogeneous platforms consisting of central processing units
(CPUs), graphics processing units (GPUs), DSPs and other processors.

Rusticl is an implementation of OpenCL.
%endif

%if %{with vdpau}
%package -n %{vdpaudrivers}
Summary:	Mesa VDPAU drivers
Group:		System/Libraries
Requires:	%{dridrivers} >= %{EVRD}
%ifnarch %{armx} %{riscv}
%rename		%{_lib}vdpau-driver-nouveau
Conflicts:	%{_lib}vdpau-driver-nouveau <= 22.0.0-0.rc2.1
%rename		%{_lib}vdpau-driver-r300
Conflicts:	%{_lib}vdpau-driver-r300 <= 22.0.0-0.rc2.1
%rename		%{_lib}vdpau-driver-radeonsi
Conflicts:	%{_lib}vdpau-driver-radeonsi <= 22.0.0-0.rc2.1
%if %{with r600}
%rename		%{_lib}vdpau-driver-r600
Conflicts:	%{_lib}vdpau-driver-r600 <= 22.0.0-0.rc2.1
%endif
%endif
%rename		%{_lib}vdpau-driver-softpipe
Conflicts:	%{_lib}vdpau-driver-softpipe <= 22.0.0-0.rc2.1
Provides:	vdpau-drivers = %{EVRD}
Requires:	%{_lib}vdpau1

%description -n %{vdpaudrivers}
VDPAU drivers.
%endif

%if %{with egl}
%package -n %{libgbm}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries

%description -n %{libgbm}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%package -n %{devgbm}
Summary:	Development files for Mesa (gbm libs)
Group:		Development/C
Requires:	%{libgbm} = %{EVRD}

%description -n %{devgbm}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.
%endif

%package common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{devgl} = %{EVRD}
Requires:	%{devegl} = %{EVRD}
Requires:	pkgconfig(libglvnd)
Requires:	pkgconfig(glesv1_cm)
Requires:	pkgconfig(glesv2)

%description common-devel
Mesa common metapackage devel.

%package tools
Summary:	Tools for debugging Mesa drivers
Group:		Development/Tools

%description tools
Tools for debugging Mesa drivers.

%prep
%autosetup -p1 -n mesa-%{?git:%{git_branch}}%{!?git:%{version}%{vsuffix}}

%build
%if %{with gcc}
export CC=gcc
export CXX=g++
%endif

%if %{with rust}
%define cargo_registry /usr/share/cargo/registry
export MESON_PACKAGE_CACHE_DIR="%{cargo_registry}/"
# So... Meson can't actually find them without tweaks
%define inst_crate_nameversion() %(basename %{cargo_registry}/%{1}-*)
%define rewrite_wrap_file() sed -e "/source.*/d" -e "s/%{1}-.*/%{inst_crate_nameversion %{1}}/" -i subprojects/%{1}.wrap
 
%rewrite_wrap_file proc-macro2
%rewrite_wrap_file quote
%rewrite_wrap_file syn
%rewrite_wrap_file unicode-ident
%rewrite_wrap_file paste
%rewrite_wrap_file rustc-hash
# Rust dependencies of Nouveau...
# Nouveau doesn't use cargo, so we probably have to do this manually?
mkdir rustdeps
rustc --crate-name paste --edition=2021 /usr/share/cargo/registry/unicode-ident-*/src/lib.rs --crate-type lib --emit=dep-info,metadata,link --out-dir $(pwd)/rustdeps -Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now

rustc --crate-name unicode_ident --edition=2021 /usr/share/cargo/registry/unicode-ident-*/src/lib.rs --crate-type lib --emit=dep-info,metadata,link --out-dir $(pwd)/rustdeps -Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now

rustc --crate-name proc_macro2 --edition=2021 /usr/share/cargo/registry/proc-macro2-*/src/lib.rs --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debug-assertions=off --cfg 'feature="default"' --cfg 'feature="proc-macro"' --out-dir $(pwd)/rustdeps -L dependency=$(pwd)/rustdeps --extern unicode_ident=$(pwd)/rustdeps/libunicode_ident.rmeta --cap-lints warn -Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now --cap-lints=warn --cfg wrap_proc_macro

rustc --crate-name quote --edition=2018 /usr/share/cargo/registry/quote-*/src/lib.rs --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debug-assertions=off --cfg 'feature="default"' --cfg 'feature="proc-macro"' --out-dir $(pwd)/rustdeps -L dependency=$(pwd)/rustdeps --extern proc_macro2=$(pwd)/rustdeps/libproc_macro2.rmeta --cap-lints warn -Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now --cap-lints=warn

rustc --crate-name syn --edition=2021 /usr/share/cargo/registry/syn-*/src/lib.rs --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debug-assertions=off --cfg 'feature="default"' --cfg 'feature="proc-macro"' --cfg 'feature="parsing"' --cfg 'feature="full"' --cfg 'feature="derive"' --cfg 'feature="printing"' --out-dir $(pwd)/rustdeps -L dependency=$(pwd)/rustdeps --extern proc_macro2=$(pwd)/rustdeps/libproc_macro2.rmeta --extern unicode_ident=$(pwd)/rustdeps/libunicode_ident.rmeta --extern quote=$(pwd)/rustdeps/libquote.rmeta --cap-lints warn -Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Clink-arg=-Wl,-z,relro -Clink-arg=-Wl,-z,now --cap-lints=warn
%endif


%if %{with compat32}
cat >llvm-config <<EOF
#!/bin/sh
/usr/bin/llvm-config "\$@" |sed -e 's,lib64,lib,g'
EOF
chmod +x llvm-config
export PATH="$(pwd):${PATH}"

cat >i686.cross <<EOF
[binaries]
pkgconfig = 'pkg-config'
cmake = 'cmake'
llvm-config = '$(pwd)/llvm-config'

[host_machine]
system = 'linux'
cpu_family = 'x86'
cpu = 'i686'
endian = 'little'
EOF

# vulkan-drivers intentionally doesn't include nouveau for now, since
# that would require a 32-bit rust crosscompiler.
# Let's just hope anything that is old enough to be 32-bit also
# predates vulkan!
# for opencl-c-base.h
export CC="%{__cc} -I%{_libdir}/clang/$(clang --version |head -n1 |cut -d' ' -f2 |cut -d. -f1)/include"
if ! %meson32 \
	-Dgallium-mediafoundation=disabled \
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	--cross-file=i686.cross \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dglx=auto \
	-Dplatforms=wayland,x11 \
	-Dvulkan-layers=device-select,overlay \
	-Dvulkan-drivers=amd,intel,intel_hasvk,swrast \
	-Dvulkan-beta=true \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dxlib-lease=auto \
	-Dandroid-libbacktrace=disabled \
	-Dvalgrind=disabled \
	-Dglvnd=enabled \
	-Dgallium-va=enabled \
	-Dgallium-vdpau=enabled \
	-Dgallium-drivers=auto,crocus \
	-Degl=enabled \
	-Dgbm=enabled \
	-Dgles1=disabled \
	-Dgles2=enabled \
	-Dglx-direct=true \
	-Dllvm=enabled \
	-Dlmsensors=enabled \
	-Dopengl=true \
	-Dshader-cache=enabled \
	-Dshared-glapi=enabled \
	-Dshared-llvm=enabled \
	-Dselinux=false \
	-Dbuild-tests=false \
	-Dintel-rt=disabled \
	-Dtools=""; then

	cat build32/meson-logs/meson-log.txt >/dev/stderr
fi
unset CC

%ninja_build -C build32/
rm llvm-config
%endif

# FIXME keep in sync with with_tools=all definition from meson.build
TOOLS="drm-shim,dlclose-skip,glsl,nir,nouveau"
%ifarch %{armx}
# FIXME add etnaviv again once the rust dependencies of etnaviv's
# tools can be sorted out -- currently we package them, but the meson
# files can't find them
# Fortunately the driver itself hasn't been infested with rust yet
TOOLS="$TOOLS,freedreno,lima,panfrost,imagination"
%endif
%ifarch %{ix86} %{x86_64}
%if %{with intel}
TOOLS="$TOOLS,intel"
%if %{with aubinatorviewer}
TOOLS="$TOOLS,intel-ui"
%endif
%endif
%endif

%if %{cross_compiling}
# We need to use a HOST compatible llvm-config... While technically wrong-ish,
# target llvm-config is for the target architecture...
cat >llvm-config <<EOF
#!/bin/sh
%{_bindir}/llvm-config "\$@" |sed -e 's,-I/usr/include ,,;s,-isystem/usr/include ,,;s,-L/usr/lib64 ,,'
EOF
chmod +x llvm-config
cp %{_datadir}/meson/toolchains/%{_target_platform}.cross cross.cross
sed -i -e "/binaries/allvm-config = '$(pwd)/llvm-config'" cross.cross
%endif

if ! %meson \
%if %{cross_compiling}
	--cross-file=cross.cross \
	-Dvalgrind=disabled \
%endif
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dandroid-libbacktrace=disabled \
%if %{cross_compiling}
	-Dgallium-drivers=swrast,r300,r600,svga,radeonsi,nouveau,zink \
	-Dvulkan-drivers=swrast,virtio \
%else
%ifarch %{armx}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,freedreno,etnaviv,tegra,vc4,v3d,lima,panfrost,zink \
	-Dvulkan-drivers=auto,broadcom,freedreno,panfrost,virtio,imagination-experimental \
%else
%ifarch %{riscv}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,etnaviv,zink \
	-Dvulkan-drivers=auto,virtio,imagination-experimental \
%else
	-Dgallium-drivers=auto,crocus,zink \
	-Dvulkan-drivers=auto,virtio,intel,intel_hasvk \
%endif
%endif
%endif
%ifarch %{x86_64}
	-Dintel-clc=enabled \
%endif
%if %{with rusticl}
	-Dgallium-rusticl=true \
%endif
	-Dgallium-extra-hud=true \
	-Dgallium-va=enabled \
	-Dgallium-vdpau=enabled \
	-Dgallium-mediafoundation=disabled \
	-Dglx=dri \
	-Dplatforms=wayland,x11 \
	-Degl-native-platform=wayland \
	-Dvulkan-layers=device-select,overlay \
	-Dvulkan-beta=true \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec,av1dec,av1enc,vp9dec \
	-Dxlib-lease=auto \
	-Dglvnd=enabled \
	-Degl=enabled \
	-Dgbm=enabled \
	-Dgles1=disabled \
	-Dgles2=enabled \
	-Dglx-direct=true \
	-Dllvm=enabled \
	-Dlmsensors=enabled \
	-Dopengl=true \
	-Dshader-cache=enabled \
	-Dshared-glapi=enabled \
	-Dshared-llvm=enabled \
	-Dselinux=false \
	-Dbuild-tests=false \
%ifarch %{x86_64}
	-Dintel-rt=enabled \
%else
	-Dintel-rt=disabled \
%endif
	-Dtools="$TOOLS"; then

	cat build/meson-logs/meson-log.txt >/dev/stderr
fi

%ninja_build -C build/

%install
%if %{with compat32}
%ninja_install -C build32/
%endif
%ninja_install -C build/

# We get those from libglvnd
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
	%{buildroot}%{_libdir}/pkgconfig/gl.pc \
	%{buildroot}%{_libdir}/libGLESv1_CM.so* \
	%{buildroot}%{_libdir}/libGLESv2.so*

# Useless, static lib without headers [optional because it's Intel specific]
[ -e %{buildroot}%{_libdir}/libgrl.a ] && rm %{buildroot}%{_libdir}/libgrl.a

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

# .so files are not needed by vdpau
rm -f %{buildroot}%{_libdir}/vdpau/libvdpau_*.so

# .la files are not needed by mesa
find %{buildroot} -name '*.la' |xargs rm -f

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

# (tpg) remove wayland files as they are now part of wayland package
rm -rf %{buildroot}%{_libdir}/libwayland-egl.so*
rm -rf %{buildroot}%{_libdir}/pkgconfig/wayland-egl.pc

%files
%doc docs/README.*
%{_datadir}/drirc.d

%files -n %{dridrivers}
%{_libdir}/libgallium-*.so
%{_libdir}/dri/*.so
%ifarch %{armx}
%{_libdir}/libpowervr_rogue.so
%endif
%{_libdir}/lib*_noop_drm_shim.so
# vulkan stuff
%{_libdir}/libVkLayer_*.so
%{_datadir}/vulkan/implicit_layer.d/*.json
%{_bindir}/mesa-overlay-control.py
%{_datadir}/vulkan/explicit_layer.d/*.json
%{_libdir}/libvulkan_*.so
%{_datadir}/vulkan/icd.d/*_icd.*.json

%ifarch %{armx}
%files -n freedreno-tools
%{_bindir}/afuc-asm
%{_bindir}/afuc-disasm
%{_bindir}/cffdump
%{_bindir}/computerator
%{_bindir}/crashdec
%{_bindir}/fdperf
%{_datadir}/freedreno
%endif

%files -n %{libgl}
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libGLX_mesa.so.0*
%dir %{_libdir}/dri

%if %{with egl}
%files -n %{libegl}
%{_libdir}/libEGL_mesa.so.%{eglmajor}*
%endif

%if %{with rusticl}
%files -n %{librusticl}
%{_sysconfdir}/OpenCL/vendors/rusticl.icd
%{_libdir}/libRusticlOpenCL.so*
%endif

%if %{with egl}
%files -n %{libgbm}
%{_libdir}/libgbm.so.%{gbmmajor}*
%{_libdir}/gbm
%endif

%files -n %{devgl}
%{_libdir}/libGLX_mesa.so
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files common-devel
# meta devel pkg

%if %{with egl}
%files -n %{devegl}
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglext_angle.h
%{_libdir}/libEGL_mesa.so
%endif

#vdpau enabled
%if %{with vdpau}
%files -n %{vdpaudrivers}
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau*.so.*
%endif

%if %{with egl}
%files -n %{devgbm}
%{_includedir}/gbm.h
%{_includedir}/gbm_backend_abi.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc
%endif

%ifarch %{ix86} %{x86_64}
%files -n %{devvulkan}
%endif

%files tools
%ifarch %{ix86} %{x86_64}
%{_bindir}/aubinator
%{_bindir}/aubinator_error_decode
%if %{with aubinatorviewer}
%{_bindir}/aubinator_viewer
%endif
%{_bindir}/executor
%{_bindir}/intel_error2hangdump
%{_bindir}/intel_hang_replay
%{_bindir}/intel_dev_info
%{_bindir}/intel_dump_gpu
%{_bindir}/intel_error2aub
%{_bindir}/intel_measure.py
%{_bindir}/intel_sanitize_gpu
%{_bindir}/intel_stub_gpu
%{_bindir}/intel_monitor
%{_bindir}/brw_asm
%{_bindir}/brw_disasm
%{_bindir}/elk_asm
%{_bindir}/elk_disasm
%{_libexecdir}/libintel_dump_gpu.so
%{_libexecdir}/libintel_sanitize_gpu.so
%endif
%{_bindir}/nv_mme_dump
%{_bindir}/nv_push_dump
%ifarch %{armx}
%{_bindir}/generate_rd
%{_bindir}/panfrostdump
%{_bindir}/panfrost_texfeatures
%{_bindir}/rddecompiler
%{_bindir}/replay
%{_bindir}/lima_disasm
%endif
%{_bindir}/glsl_compiler
%{_bindir}/spirv2nir
%{_libdir}/libdlclose-skip.so

%if %{with compat32}
%files -n %{lib32egl}
%{_prefix}/lib/libEGL_mesa.so.%{eglmajor}*

%files -n %{dev32egl}
%{_prefix}/lib/libEGL_mesa.so

%files -n %{lib32gl}
%{_prefix}/lib/libGLX_mesa.so.0*
%dir %{_prefix}/lib/dri

%files -n %{dev32gl}
%{_prefix}/lib/pkgconfig/dri.pc
%{_prefix}/lib/libGLX_mesa.so

%files -n %{lib32gbm}
%{_prefix}/lib/libgbm.so.*

%files -n %{dev32gbm}
%{_prefix}/lib/libgbm.so
%{_prefix}/lib/gbm
%{_prefix}/lib/pkgconfig/gbm.pc

%files -n %{dridrivers32}
%{_prefix}/lib/libgallium-*.so
%{_prefix}/lib/dri/*.so
%{_prefix}/lib/libVkLayer_*.so
%{_prefix}/lib/libvulkan_*.so
%{_prefix}/lib/vdpau/libvdpau_*.so*
%endif

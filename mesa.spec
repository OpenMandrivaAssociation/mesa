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
#define relc 2

%ifarch %{riscv}
%bcond_with gcc
%bcond_with opencl
%else
%bcond_with gcc
%bcond_without opencl
%endif

%bcond_without rust
%bcond_without rusticl
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
%define libegl %mklibname %{eglname}
%define oldlibegl %mklibname %{eglname} %{eglmajor}
%define devegl %mklibname %{eglname} -d
%define lib32egl %mklib32name %{eglname}
%define oldlib32egl %mklib32name %{eglname} %{eglmajor}
%define dev32egl %mklib32name %{eglname} -d

%define glmajor 0
%define glname GLX_mesa
%define libgl %mklibname %{glname}
%define oldlibglx %mklibname %{glname} %{glmajor}
%define devgl %mklibname GL -d
%define lib32gl %mklib32name %{glname}
%define oldlib32glx %mklib32name %{glname} %{glmajor}
%define dev32gl libGL-devel

%define devvulkan %mklibname vulkan-intel -d
%define dev32vulkan libvulkan-intel-devel

%define glesv1major 1
%define glesv1name GLESv1_CM
%define libglesv1 %mklibname %{glesv1name}
%define devglesv1 %mklibname %{glesv1name} -d
%define lib32glesv1 %mklib32name %{glesv1name}
%define dev32glesv1 %mklib32name %{glesv1name} -d

%define glesv2major 2
%define glesv2name GLESv2
%define libglesv2 %mklibname %{glesv2name}
%define devglesv2 %mklibname %{glesv2name} -d
%define lib32glesv2 %mklib32name %{glesv2name}
%define dev32glesv2 %mklib32name %{glesv2name} -d

%define devglesv3 %mklibname glesv3 -d
%define dev32glesv3 libglesv3-devel

%define dridrivers %mklibname dri-drivers
%define dridrivers32 %mklib32name dri-drivers
%define libgallium %mklibname gallium
%define lib32gallium %mklib32name gallium

%define gbmmajor 1
%define gbmname gbm
%define libgbm %mklibname %{gbmname}
%define oldlibgbm %mklibname %{gbmname} %{gbmmajor}
%define devgbm %mklibname %{gbmname} -d
%define lib32gbm %mklib32name %{gbmname}
%define oldlib32gbm %mklib32name %{gbmname} %{gbmmajor}
%define dev32gbm %mklib32name %{gbmname} -d

%define swravxmajor 0
%define swravxname swravx
%define libswravx %mklibname %swravxname
%define lib32swravx %mklib32name %{swravxname}

%define swravx2major 0
%define swravx2name swravx2
%define libswravx2 %mklibname %swravx2name
%define lib32swravx2 %mklib32name %{swravx2name}

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
Version:	26.2.1
Release:	%{?relc:0.rc%{relc}.}%{?git:0.%{git}.}4
Group:		System/Libraries
License:	MIT
Url:		https://www.mesa3d.org
%if 0%{?git:1}
%if "%{git_branch}" == "panthor" || "%{git_branch}" == "panfrost"
Source0:	https://gitlab.freedesktop.org/panfrost/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
%else
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{git_branch}/mesa-%{git_branch}.tar.bz2#/mesa-%{git}.tar.bz2
%endif
%else
Source0:	https://mesa.freedesktop.org/archive/mesa-%{version}%{vsuffix}.tar.xz
%endif
# 3rd party libraries that need to be built inside mesa (mostly rust mess that
# doesn't support proper libraries).
Source1:	mesa-subprojects.tar.zst
# Use this to generate/refresh Source1 (not used inside the spec, just kept
# here for reference) [run from this directory]
Source2:	download-subprojects
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
# RADV already enables Vulkan video by default on VCN2+ (Mesa 25+).
# ANV still gates decode behind ANV_DEBUG=video-decode; default it on.
Patch11:	enable-vulkan-video-decode.patch
#Patch12:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/31950.patch
Patch13:	mesa-26.0-missing-include.patch
Patch14:	mesa-25.2-aarch64-compile.patch
# LLVM 23 moved libclc into the clang resource dir and dropped libclc.pc.
# Based on draft mesa!40601 (completed for packaging: optional pkg-config +
# per-triple spirv{32,64}-unknown-unknown/libclc.spv paths).
Patch15:	mesa-26.2-llvm23-libclc.patch
# gen_private.h uses std::size_t without including <cstddef>; fails 32-bit builds
# where transitive includes do not pull it in.
Patch16:	mesa-26.2-gen-private-cstddef.patch
# LLVM 23 ObjectLinkingLayer creator takes a memory manager and returns Expected<>
Patch17:	mesa-26.2-llvm23-orc-jitlink.patch
# Cross: use host mesa_clc/vtn_bindgen2, but still install target copies.
Patch18:	mesa-26.2-install-target-clc.patch
# Build each Gallium pipe driver as a real *_dri.so that ELF-links libgallium
# instead of one megadriver containing every vendor.
Patch19:	mesa-split-gallium-drivers.patch

# Panthor -- https://gitlab.freedesktop.org/bbrezillon/mesa.git
# Currently no patches required

# From upstream

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
BuildRequires:	pkgconfig(libdisplay-info)
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
#BuildRequires:	pkgconfig(libclc)
BuildRequires:	libclc-amdgcn
BuildRequires:	libclc-spirv
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(OpenCLHeaders)
BuildRequires:	cmake(OpenCLICDLoader)
BuildRequires:	clang
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

# package mesa
Requires:	libGL.so.1%{_arch_tag_suffix}

%if %{with compat32} || %{cross_compiling}
BuildRequires:	%{name}-buildtools = %{version}
%endif

%if %{with compat32}
BuildRequires:	cross-i686-openmandriva-linux-gnu-binutils
BuildRequires:	cross-i686-openmandriva-linux-gnu-clang
BuildRequires:	cross-i686-openmandriva-linux-gnu-gcc
BuildRequires:	cross-i686-openmandriva-linux-gnu-libc
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
BuildRequires:	libdisplay-info
BuildRequires:	devel(libdisplay-info)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libelf)
BuildRequires:	libunwind-nongnu-devel
BuildRequires:	devel(libva)
BuildRequires:	devel(libz)
BuildRequires:	devel(libexpat)
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

%package -n %{libgallium}
Summary:	Mesa Gallium shared core (state tracker, NIR, util)
Group:		System/Libraries

%description -n %{libgallium}
Shared Mesa Gallium core used by the per-vendor *_dri.so drivers.

%package -n %{dridrivers}
Summary:	Mesa DRI/Vulkan common files
Group:		System/Libraries
# Old OM package
Provides:	dri-drivers = %{EVRD}
# Fedora naming, compat Provides: needed to make the
# zoom RPM install
Provides:	mesa-dri-drivers = %{EVRD}
Requires:	%{libgallium} = %{EVRD}
Requires:	vulkan-loader
Requires:	%{libgl} = %{EVRD}
%if %{with egl}
Requires:	%{libegl} = %{EVRD}
%endif
Requires:	%{dridrivers}-swrast = %{EVRD}
Requires:	%{dridrivers}-zink = %{EVRD}
%ifnarch %{riscv}
Recommends:	%{dridrivers}-virtio = %{EVRD}
Recommends:	%{dridrivers}-vmwgfx = %{EVRD}
%endif
%ifnarch %{armx} %{riscv}
%if %{with r600}
Recommends:	%{dridrivers}-radeon = %{EVRD}
%endif
%ifarch %{ix86} %{x86_64}
Recommends:	%{dridrivers}-intel = %{EVRD}
Recommends:	%{dridrivers}-iris = %{EVRD}
%endif
Recommends:	%{dridrivers}-nouveau = %{EVRD}
%endif
%ifarch %{armx}
Recommends:	%{dridrivers}-freedreno = %{EVRD}
Recommends:	%{dridrivers}-vc4 = %{EVRD}
Recommends:	%{dridrivers}-v3d = %{EVRD}
Recommends:	%{dridrivers}-etnaviv = %{EVRD}
Recommends:	%{dridrivers}-tegra = %{EVRD}
Recommends:	%{dridrivers}-lima = %{EVRD}
Recommends:	%{dridrivers}-panfrost = %{EVRD}
Recommends:	%{dridrivers}-kmsro = %{EVRD}
%endif
Obsoletes:	%{_lib}XvMCgallium1 <= 22.0.0-0.rc2.1
Obsoletes:	vdpau-drivers < %{EVRD}

%description -n %{dridrivers}
Common Mesa DRI/Vulkan bits (loader stub, layers). Hardware drivers
are in %{dridrivers}-* subpackages so unused vendors can be omitted.

%package -n %{dridrivers}-swrast
Summary:	Mesa software rasterizers (llvmpipe, softpipe, lavapipe)
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-swrast
Gallium software rasterizers and the lavapipe Vulkan ICD.

%package -n %{dridrivers}-zink
Summary:	Mesa Zink OpenGL-on-Vulkan driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-zink
Zink Gallium driver (OpenGL on top of Vulkan).

%ifnarch %{riscv}
%package -n %{dridrivers}-virtio
Summary:	Mesa virtio-GPU DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-virtio
virtio-GPU Gallium and Vulkan drivers.

%package -n %{dridrivers}-vmwgfx
Summary:	Mesa VMware SVGA DRI driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-vmwgfx
VMware SVGA Gallium driver.
%endif

%ifnarch %{armx} %{riscv}
%if %{with r600}
%package -n %{dridrivers}-radeon
Summary:	Mesa AMD/Radeon DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-radeon
radeonsi/r600/r300 Gallium drivers and RADV.
%endif
%ifarch %{ix86} %{x86_64}
%package -n %{dridrivers}-intel
Summary:	Mesa Intel DRI and Vulkan drivers (crocus, i915, hasvk)
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-intel
crocus/i915 Gallium drivers and ANV hasvk.

%package -n %{dridrivers}-iris
Summary:	Mesa Intel Iris DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-iris
Iris Gallium driver and ANV.
%endif
%package -n %{dridrivers}-nouveau
Summary:	Mesa Nouveau DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-nouveau
Nouveau Gallium driver and NVK.
%endif

%ifarch %{armx}
%package -n %{dridrivers}-freedreno
Summary:	Mesa Freedreno DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-freedreno
Freedreno Gallium and Vulkan drivers.

%package -n %{dridrivers}-vc4
Summary:	Mesa VC4 DRI driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-vc4
Broadcom VC4 Gallium driver.

%package -n %{dridrivers}-v3d
Summary:	Mesa V3D DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-v3d
Broadcom V3D Gallium and Vulkan drivers.

%package -n %{dridrivers}-etnaviv
Summary:	Mesa Etnaviv DRI driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-etnaviv
Etnaviv Gallium driver.

%package -n %{dridrivers}-tegra
Summary:	Mesa Tegra DRI driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-tegra
Tegra Gallium driver.

%package -n %{dridrivers}-lima
Summary:	Mesa Lima DRI driver
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-lima
Lima Gallium driver.

%package -n %{dridrivers}-panfrost
Summary:	Mesa Panfrost DRI and Vulkan drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-panfrost
Panfrost Gallium and Vulkan drivers.

%package -n %{dridrivers}-kmsro
Summary:	Mesa kmsro display-only DRI drivers
Group:		System/Libraries
Requires:	%{libgallium} = %{EVRD}

%description -n %{dridrivers}-kmsro
kmsro display-controller Gallium drivers.
%endif

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
%rename %{oldlibglx}
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
%rename %{oldlibegl}

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
%package -n %{lib32gallium}
Summary:	Mesa Gallium shared core (32-bit)
Group:		System/Libraries

%description -n %{lib32gallium}
Shared Mesa Gallium core used by the per-vendor 32-bit *_dri.so drivers.

%package -n %{dridrivers32}
Summary:	Mesa DRI/Vulkan common files (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}
Requires:	libvulkan1
Requires:	%{lib32gl} = %{EVRD}
%if %{with egl}
Requires:	%{lib32egl} = %{EVRD}
%endif
Requires:	%{dridrivers32}-swrast = %{EVRD}
Requires:	%{dridrivers32}-zink = %{EVRD}
%if %{with r600}
Recommends:	%{dridrivers32}-radeon = %{EVRD}
%endif
Recommends:	%{dridrivers32}-intel = %{EVRD}
Recommends:	%{dridrivers32}-iris = %{EVRD}
Recommends:	%{dridrivers32}-nouveau = %{EVRD}
Recommends:	%{dridrivers32}-virtio = %{EVRD}
Recommends:	%{dridrivers32}-vmwgfx = %{EVRD}

%description -n %{dridrivers32}
Common 32-bit Mesa DRI/Vulkan bits. Hardware drivers are in
%{dridrivers32}-* subpackages.

%package -n %{dridrivers32}-swrast
Summary:	Mesa software rasterizers (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-swrast
32-bit Gallium software rasterizers and lavapipe.

%package -n %{dridrivers32}-zink
Summary:	Mesa Zink OpenGL-on-Vulkan driver (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-zink
32-bit Zink Gallium driver.

%if %{with r600}
%package -n %{dridrivers32}-radeon
Summary:	Mesa AMD/Radeon DRI and Vulkan drivers (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-radeon
32-bit radeonsi/r600/r300 and RADV.
%endif

%package -n %{dridrivers32}-intel
Summary:	Mesa Intel DRI and Vulkan drivers (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-intel
32-bit crocus/i915 and ANV hasvk.

%package -n %{dridrivers32}-iris
Summary:	Mesa Intel Iris DRI and Vulkan drivers (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-iris
32-bit Iris and ANV.

%package -n %{dridrivers32}-nouveau
Summary:	Mesa Nouveau DRI and Vulkan drivers (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-nouveau
32-bit Nouveau and NVK.

%package -n %{dridrivers32}-virtio
Summary:	Mesa virtio-GPU DRI driver (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-virtio
32-bit virtio-GPU Gallium driver.

%package -n %{dridrivers32}-vmwgfx
Summary:	Mesa VMware SVGA DRI driver (32-bit)
Group:		System/Libraries
Requires:	%{lib32gallium} = %{EVRD}

%description -n %{dridrivers32}-vmwgfx
32-bit VMware SVGA Gallium driver.

%package -n %{lib32gl}
Summary:	Files for Mesa (GL and GLX libs) (32-bit)
Group:		System/Libraries
Suggests:	%{dridrivers32} >= %{EVRD}
%rename %{oldlib32glx}
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
%rename %{oldlib32gbm}

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
%rename %{oldlib32egl}

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

%if %{with egl}
%package -n %{libgbm}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries
%rename %{oldlibgbm}

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

%package buildtools
Summary:	Mesa build tools needed for crosscompiling mesa
Group:		Development/Tools

%description buildtools
Mesa build tools needed for crosscompiling mesa.

%files buildtools
%{_bindir}/vtn_bindgen2
%{_bindir}/mesa_clc

%prep
%autosetup -p1 -a1 -n mesa-%{?git:%{git_branch}}%{!?git:%{version}%{vsuffix}}

%build
%if %{with gcc}
export CC=gcc
export CXX=g++
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
export CC="%{__cc} -m32 -I%{_libdir}/clang/$(clang --version |head -n1 |cut -d' ' -f2 |cut -d. -f1)/include -isystem %{_includedir}"
export CXX="%{__cxx} -m32 -I%{_libdir}/clang/$(clang --version |head -n1 |cut -d' ' -f2 |cut -d. -f1)/include -isystem %{_includedir}"
export LDFLAGS="-m32 -L%{_prefix}/lib"
if ! %meson32 \
	-Dgallium-mediafoundation=disabled \
	-Dmicrosoft-clc=disabled \
	-Dmesa-clc=system \
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
	-Dgallium-split-drivers=true \
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
unset CXX
unset LDFLAGS

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
	-Dmesa-clc=system \
	-Dvalgrind=disabled \
	-Ddisplay-info=disabled \
%endif
	-Dmicrosoft-clc=disabled \
	-Dinstall-mesa-clc=true \
	-Dshared-llvm=enabled \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dandroid-libbacktrace=disabled \
%if %{cross_compiling}
	-Dgallium-drivers=llvmpipe,softpipe,r300,r600,svga,radeonsi,nouveau,zink \
	-Dvulkan-drivers=virtio \
%else
%ifarch %{armx}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,freedreno,etnaviv,tegra,vc4,v3d,lima,panfrost,zink \
	-Dvulkan-drivers=auto,broadcom,freedreno,panfrost,virtio,imagination \
%else
%ifarch %{riscv}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,etnaviv,zink \
	-Dvulkan-drivers=auto,virtio,imagination \
%else
	-Dgallium-drivers=auto,crocus,zink \
	-Dvulkan-drivers=auto,virtio,intel,intel_hasvk \
%endif
%endif
%endif
%if %{with rusticl}
	-Dgallium-rusticl=true \
%endif
	-Dgallium-extra-hud=true \
	-Dgallium-split-drivers=true \
	-Dgallium-va=enabled \
	-Dgallium-mediafoundation=disabled \
	-Dglx=dri \
	-Dplatforms=wayland,x11 \
	-Degl-native-platform=x11 \
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

# .la files are not needed by mesa
find %{buildroot} -name '*.la' |xargs rm -f

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

# (tpg) remove wayland files as they are now part of wayland package
rm -rf %{buildroot}%{_libdir}/libwayland-egl.so*
rm -rf %{buildroot}%{_libdir}/pkgconfig/wayland-egl.pc

# Fix perms
chmod 0755 %{buildroot}%{_bindir}/mesa-overlay-control.py


%files
%doc docs/README.*
%{_datadir}/drirc.d

%files -n %{libgallium}
%{_libdir}/libgallium-*.so

%files -n %{dridrivers}
%dir %{_libdir}/dri
%{_libdir}/dri/libdril_dri.so
# kmsro panel aliases (libdril stubs) on desktop too
%optional %{_libdir}/dri/apple_dri.so
%optional %{_libdir}/dri/armada-drm_dri.so
%optional %{_libdir}/dri/exynos_dri.so
%optional %{_libdir}/dri/gm12u320_dri.so
%optional %{_libdir}/dri/hdlcd_dri.so
%optional %{_libdir}/dri/hx8357d_dri.so
%optional %{_libdir}/dri/ili9163_dri.so
%optional %{_libdir}/dri/ili9225_dri.so
%optional %{_libdir}/dri/ili9341_dri.so
%optional %{_libdir}/dri/ili9486_dri.so
%optional %{_libdir}/dri/imx-dcss_dri.so
%optional %{_libdir}/dri/imx-drm_dri.so
%optional %{_libdir}/dri/imx-lcdif_dri.so
%optional %{_libdir}/dri/ingenic-drm_dri.so
%optional %{_libdir}/dri/kirin_dri.so
%optional %{_libdir}/dri/komeda_dri.so
%optional %{_libdir}/dri/mali-dp_dri.so
%optional %{_libdir}/dri/mcde_dri.so
%optional %{_libdir}/dri/mediatek_dri.so
%optional %{_libdir}/dri/meson_dri.so
%optional %{_libdir}/dri/mi0283qt_dri.so
%optional %{_libdir}/dri/mxsfb-drm_dri.so
%optional %{_libdir}/dri/panel-mipi-dbi_dri.so
%optional %{_libdir}/dri/pl111_dri.so
%optional %{_libdir}/dri/rcar-du_dri.so
%optional %{_libdir}/dri/repaper_dri.so
%optional %{_libdir}/dri/rockchip_dri.so
%optional %{_libdir}/dri/rzg2l-du_dri.so
%optional %{_libdir}/dri/ssd130x_dri.so
%optional %{_libdir}/dri/st7586_dri.so
%optional %{_libdir}/dri/st7735r_dri.so
%optional %{_libdir}/dri/sti_dri.so
%optional %{_libdir}/dri/stm_dri.so
%optional %{_libdir}/dri/sun4i-drm_dri.so
%optional %{_libdir}/dri/udl_dri.so
%optional %{_libdir}/dri/vkms_dri.so
%optional %{_libdir}/dri/zynqmp-dpsub_dri.so
%{_libdir}/libVkLayer_*.so
%{_datadir}/vulkan/implicit_layer.d/*.json
%{_bindir}/mesa-overlay-control.py
%{_datadir}/vulkan/explicit_layer.d/*.json
%ifarch %{armx} %{riscv}
%optional %{_libdir}/libvulkan_imagination.so
%optional %{_datadir}/vulkan/icd.d/powervr_icd.*.json
%optional %{_datadir}/vulkan/icd.d/imagination_icd.*.json
%endif

%files -n %{dridrivers}-swrast
%{_libdir}/dri/swrast_dri.so
%optional %{_libdir}/dri/kms_swrast_dri.so
%optional %{_libdir}/libvulkan_lvp.so
%optional %{_datadir}/vulkan/icd.d/lvp_icd.*.json

%files -n %{dridrivers}-zink
%{_libdir}/dri/zink_dri.so

%ifnarch %{riscv}
%files -n %{dridrivers}-virtio
%{_libdir}/dri/virtio_gpu_dri.so
%optional %{_libdir}/dri/virtio_gpu_drv_video.so
%optional %{_libdir}/libvulkan_virtio.so
%optional %{_datadir}/vulkan/icd.d/virtio_icd.*.json

%files -n %{dridrivers}-vmwgfx
%{_libdir}/dri/vmwgfx_dri.so
%endif

%ifnarch %{armx} %{riscv}
%if %{with r600}
%files -n %{dridrivers}-radeon
%{_libdir}/dri/radeonsi_dri.so
%optional %{_libdir}/dri/r300_dri.so
%optional %{_libdir}/dri/r600_dri.so
%optional %{_libdir}/dri/radeonsi_drv_video.so
%optional %{_libdir}/dri/r600_drv_video.so
%optional %{_libdir}/libvulkan_radeon.so
%optional %{_datadir}/vulkan/icd.d/radeon_icd.*.json
%optional %{_libdir}/libamdgpu_noop_drm_shim.so
%optional %{_libdir}/libradeon_noop_drm_shim.so
%endif
%ifarch %{ix86} %{x86_64}
%files -n %{dridrivers}-intel
%optional %{_libdir}/dri/crocus_dri.so
%optional %{_libdir}/dri/i915_dri.so
%optional %{_libdir}/libvulkan_intel_hasvk.so
%optional %{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%optional %{_libdir}/libintel_noop_drm_shim.so

%files -n %{dridrivers}-iris
%{_libdir}/dri/iris_dri.so
%optional %{_libdir}/libvulkan_intel.so
%optional %{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif
%files -n %{dridrivers}-nouveau
%{_libdir}/dri/nouveau_dri.so
%optional %{_libdir}/dri/nouveau_drv_video.so
%optional %{_libdir}/libvulkan_nouveau.so
%optional %{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%optional %{_libdir}/libnouveau_noop_drm_shim.so
%endif

%ifarch %{armx}
%files -n %{dridrivers}-freedreno
%{_libdir}/dri/msm_dri.so
%optional %{_libdir}/dri/kgsl_dri.so
%optional %{_libdir}/libvulkan_freedreno.so
%optional %{_datadir}/vulkan/icd.d/freedreno_icd.*.json

%files -n %{dridrivers}-vc4
%{_libdir}/dri/vc4_dri.so

%files -n %{dridrivers}-v3d
%{_libdir}/dri/v3d_dri.so
%optional %{_libdir}/libvulkan_broadcom.so
%optional %{_datadir}/vulkan/icd.d/broadcom_icd.*.json

%files -n %{dridrivers}-etnaviv
%{_libdir}/dri/etnaviv_dri.so

%files -n %{dridrivers}-tegra
%{_libdir}/dri/tegra_dri.so

%files -n %{dridrivers}-lima
%{_libdir}/dri/lima_dri.so

%files -n %{dridrivers}-panfrost
%{_libdir}/dri/panfrost_dri.so
%optional %{_libdir}/dri/panthor_dri.so
%optional %{_libdir}/libvulkan_panfrost.so
%optional %{_datadir}/vulkan/icd.d/panfrost_icd.*.json

%files -n %{dridrivers}-kmsro
%{_libdir}/dri/kmsro_dri.so
%endif

%ifarch %{armx}
%files -n freedreno-tools
%{_bindir}/cffdump
%{_bindir}/computerator
%{_bindir}/crashdec
%{_bindir}/fdperf
%{_bindir}/qrisc-asm
%{_bindir}/qrisc-disasm
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
%{_bindir}/gentool
%{_bindir}/intel_error2hangdump
%{_bindir}/intel_hang_replay
%{_bindir}/intel_dev_info
%{_bindir}/intel_dump_gpu
%{_bindir}/intel_error2aub
%{_bindir}/intel_measure.py
%{_bindir}/intel_sanitize_gpu
%{_bindir}/intel_stub_gpu
%{_bindir}/intel_monitor
%{_bindir}/mda
# brw_asm/brw_disasm removed upstream in favor of elk_* (intel compiler split)
%{_bindir}/elk_asm
%{_bindir}/elk_disasm
%{_libexecdir}/libintel_dump_gpu.so
%{_libexecdir}/libintel_sanitize_gpu.so
%endif
%optional %{_bindir}/nv_mme_dump
%optional %{_bindir}/nv_mme_method_dumper
%optional %{_bindir}/nv_push_dump
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

%files -n %{lib32gallium}
%{_prefix}/lib/libgallium-*.so

%files -n %{dridrivers32}
%dir %{_prefix}/lib/dri
%{_prefix}/lib/dri/libdril_dri.so
%optional %{_prefix}/lib/dri/apple_dri.so
%optional %{_prefix}/lib/dri/armada-drm_dri.so
%optional %{_prefix}/lib/dri/exynos_dri.so
%optional %{_prefix}/lib/dri/gm12u320_dri.so
%optional %{_prefix}/lib/dri/hdlcd_dri.so
%optional %{_prefix}/lib/dri/hx8357d_dri.so
%optional %{_prefix}/lib/dri/ili9163_dri.so
%optional %{_prefix}/lib/dri/ili9225_dri.so
%optional %{_prefix}/lib/dri/ili9341_dri.so
%optional %{_prefix}/lib/dri/ili9486_dri.so
%optional %{_prefix}/lib/dri/imx-dcss_dri.so
%optional %{_prefix}/lib/dri/imx-drm_dri.so
%optional %{_prefix}/lib/dri/imx-lcdif_dri.so
%optional %{_prefix}/lib/dri/ingenic-drm_dri.so
%optional %{_prefix}/lib/dri/kirin_dri.so
%optional %{_prefix}/lib/dri/komeda_dri.so
%optional %{_prefix}/lib/dri/mali-dp_dri.so
%optional %{_prefix}/lib/dri/mcde_dri.so
%optional %{_prefix}/lib/dri/mediatek_dri.so
%optional %{_prefix}/lib/dri/meson_dri.so
%optional %{_prefix}/lib/dri/mi0283qt_dri.so
%optional %{_prefix}/lib/dri/mxsfb-drm_dri.so
%optional %{_prefix}/lib/dri/panel-mipi-dbi_dri.so
%optional %{_prefix}/lib/dri/pl111_dri.so
%optional %{_prefix}/lib/dri/rcar-du_dri.so
%optional %{_prefix}/lib/dri/repaper_dri.so
%optional %{_prefix}/lib/dri/rockchip_dri.so
%optional %{_prefix}/lib/dri/rzg2l-du_dri.so
%optional %{_prefix}/lib/dri/ssd130x_dri.so
%optional %{_prefix}/lib/dri/st7586_dri.so
%optional %{_prefix}/lib/dri/st7735r_dri.so
%optional %{_prefix}/lib/dri/sti_dri.so
%optional %{_prefix}/lib/dri/stm_dri.so
%optional %{_prefix}/lib/dri/sun4i-drm_dri.so
%optional %{_prefix}/lib/dri/udl_dri.so
%optional %{_prefix}/lib/dri/vkms_dri.so
%optional %{_prefix}/lib/dri/zynqmp-dpsub_dri.so
%optional %{_prefix}/lib/libVkLayer_*.so

%files -n %{dridrivers32}-swrast
%{_prefix}/lib/dri/swrast_dri.so
%optional %{_prefix}/lib/dri/kms_swrast_dri.so
%optional %{_prefix}/lib/libvulkan_lvp.so

%files -n %{dridrivers32}-zink
%{_prefix}/lib/dri/zink_dri.so

%if %{with r600}
%files -n %{dridrivers32}-radeon
%{_prefix}/lib/dri/radeonsi_dri.so
%optional %{_prefix}/lib/dri/r300_dri.so
%optional %{_prefix}/lib/dri/r600_dri.so
%optional %{_prefix}/lib/dri/radeonsi_drv_video.so
%optional %{_prefix}/lib/dri/r600_drv_video.so
%optional %{_prefix}/lib/libvulkan_radeon.so
%endif

%files -n %{dridrivers32}-intel
%optional %{_prefix}/lib/dri/crocus_dri.so
%optional %{_prefix}/lib/dri/i915_dri.so
%optional %{_prefix}/lib/libvulkan_intel_hasvk.so

%files -n %{dridrivers32}-iris
%{_prefix}/lib/dri/iris_dri.so
%optional %{_prefix}/lib/libvulkan_intel.so

%files -n %{dridrivers32}-nouveau
%{_prefix}/lib/dri/nouveau_dri.so
%optional %{_prefix}/lib/dri/nouveau_drv_video.so
%optional %{_prefix}/lib/libvulkan_nouveau.so

%files -n %{dridrivers32}-virtio
%{_prefix}/lib/dri/virtio_gpu_dri.so
%optional %{_prefix}/lib/dri/virtio_gpu_drv_video.so

%files -n %{dridrivers32}-vmwgfx
%{_prefix}/lib/dri/vmwgfx_dri.so
%endif

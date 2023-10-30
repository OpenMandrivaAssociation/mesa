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
%global optflags %{optflags} -O3 -fno-strict-aliasing -g1 -flto=thin
%global build_ldflags %{build_ldflags} -fno-strict-aliasing -flto=thin -Wl,--undefined-version

#define git 20230824
#define git_branch %(echo %{version} |cut -d. -f1-2)

#define relc 3

%ifarch %{riscv}
%bcond_with gcc
%bcond_with opencl
%else
%bcond_with gcc
%bcond_without opencl
%endif

%bcond_with bootstrap
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

%define osmesamajor 8
%define libosmesa %mklibname osmesa %{osmesamajor}
%define devosmesa %mklibname osmesa -d
%define lib32osmesa libosmesa%{osmesamajor}
%define dev32osmesa libosmesa-devel

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

%define d3dmajor 1
%define d3dname d3dadapter9
%define libd3d %mklibname %{d3dname} %{d3dmajor}
%define devd3d %mklibname %{d3dname} -d
%define lib32d3d lib%{d3dname}%{d3dmajor}
%define dev32d3d lib%{d3dname}-devel

%define glapimajor 0
%define glapiname glapi
%define libglapi %mklibname %{glapiname} %{glapimajor}
%define devglapi %mklibname %{glapiname} -d
%define lib32glapi lib%{glapiname}%{glapimajor}
%define dev32glapi lib%{glapiname}-devel

%define dridrivers %mklibname dri-drivers
%define vdpaudrivers %mklibname vdpau-drivers
%define dridrivers32 libdri-drivers

%define gbmmajor 1
%define gbmname gbm
%define libgbm %mklibname %{gbmname} %{gbmmajor}
%define devgbm %mklibname %{gbmname} -d
%define lib32gbm lib%{gbmname}%{gbmmajor}
%define dev32gbm lib%{gbmname}-devel

%define xatrackermajor 2
%define xatrackername xatracker
%define libxatracker %mklibname %xatrackername %{xatrackermajor}
%define devxatracker %mklibname %xatrackername -d
%define lib32xatracker lib%{xatrackername}%{xatrackermajor}
%define dev32xatracker lib%{xatrackername}-devel

%define swravxmajor 0
%define swravxname swravx
%define libswravx %mklibname %swravxname %{swravxmajor}
%define lib32swravx lib%{swravxname}%{swravxmajor}

%define swravx2major 0
%define swravx2name swravx2
%define libswravx2 %mklibname %swravx2name %{swravx2major}
%define lib32swravx2 lib%{swravx2name}%{swravx2major}

%define clmajor 1
%define clname mesaopencl
%define libcl %mklibname %clname %clmajor
%define devcl %mklibname %clname -d
%define lib32cl lib%{clname}%{clmajor}
%define dev32cl lib%{clname}-devel

%define mesasrcdir %{_prefix}/src/Mesa/
%define driver_dir %{_libdir}/dri

%define short_ver %(if [ $(echo %{version} |cut -d. -f3) = "0" ]; then echo %{version} |cut -d. -f1-2; else echo %{version}; fi)

Summary:	OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library
Name:		mesa
Version:	23.2.1
Release:	%{?relc:0.rc%{relc}.}%{?git:0.%{git}.}1
Group:		System/Libraries
License:	MIT
Url:		http://www.mesa3d.org
%if 0%{?git:1}
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
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
%define dev32dricore lib%{dricorename}-devel
%define lib32dricore lib%{dricorename}9

Obsoletes:	%{libdricore} < %{EVRD}
Obsoletes:	%{devdricore} < %{EVRD}
Obsoletes:	%{name}-xorg-drivers < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-radeon < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-nouveau < %{EVRD}

# Without this patch, the OpenCL ICD calls into MesaOpenCL,
# which for some reason calls back into the OpenCL ICD instead
# of calling its own function by the same name.
Patch0:		mesa-20.1.1-fix-opencl.patch
# Use llvm-config to detect llvm, since the newer method
# finds /usr/lib64/libLLVM-17.so even for 32-bit builds
Patch1:		mesa-23.1-x86_32-llvm-detection.patch
# Fix intel-vk build with clang 16 and gcc 13
Patch2:		mesa-23.1-intel-vk-compile.patch
# Not used in the spec; this is a test case to verify patch0
# is still needed. If this code works without the patch, the
# patch can be removed. If it crashes/takes forever (infinite
# loop), the patch is still needed.
Source50:	test.c

#Patch1:		mesa-19.2.3-arm32-buildfix.patch
#Patch2:		mesa-20.3.4-glibc-2.33.patch
Patch5:		mesa-20.3.0-meson-radeon-arm-riscv-ppc.patch

# Fix clover with new LLVM versions
Patch6:		https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/24879.patch
Patch7:		https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/13449.patch

# fedora patches
#Patch15:	mesa-9.2-hardware-float.patch

Patch8:		mesa-buildsystem-improvements.patch

# Make VirtualBox great again
# Broken by commit 2569215f43f6ce71fb8eb2181b36c6cf976bce2a
Patch10:	mesa-22.3-make-vbox-great-again.patch

# Fix LLVM 17 support
Patch20:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/25536.patch
# Adapt Patch20 to work with 23.2 branch
Patch21:	backport-25536.patch

# Panthor -- based on v10+panthor branch of https://gitlab.freedesktop.org/panfork/mesa.git
Patch100:	0001-panfrost-Abstract-some-kernel-driver-operations.patch
Patch101:	0002-panfrost-Use-the-kmod-abstraction.patch
Patch102:	0003-panfrost-Introduce-a-PAN_BO_SHAREABLE-flag.patch
Patch103:	0004-panvk-Pass-the-PAN_BO_SHAREABLE-when-relevant.patch
Patch104:	0005-panfrost-Keep-original-BO-flags-when-linearizing-a-r.patch
Patch105:	0006-panfrost-Flag-BO-shareable-when-appropriate.patch
Patch106:	0007-panfrost-Add-a-flag-to-create-uncached-GPU-mappings.patch
Patch107:	0008-panfrost-Create-scanout-kmsro-buffer-when-shared.patch
Patch108:	0009-panfrost-Add-a-backend-for-the-Panthor-kernel-driver.patch
Patch109:	0010-panfrost-Add-a-library-to-help-building-CSF-streams.patch
Patch110:	0011-panfrost-genxml-Add-missing-Progress-increment-field.patch
Patch111:	0012-panfrost-genxml-Fix-Last-First-Heap-Chunk-field-posi.patch
Patch112:	0013-panfrost-Move-pan_afbc_compression_mode-to-pan_cs.c-.patch
Patch113:	0014-panfrost-v10-support.patch
Patch114:	0015-panfrost-do-not-open-code-panfrost_has_fragment_job.patch
Patch115:	0016-panfrost-consult-draws-instead-of-draw_count.patch
Patch116:	0017-panfrost-factor-out-ceu_vt_start-from-panfrost_emit_.patch
Patch117:	0018-panfrost-Rename-panfrost_vtable-context_init.patch
Patch118:	0019-panfrost-Add-arch-specific-context-init-cleanup-hook.patch
Patch119:	0020-panfrost-Move-the-queue-heap-initialization-to-pan_c.patch
Patch120:	0021-panfrost-Add-a-panfrost_context_reinit-helper-and-us.patch
Patch121:	0022-panfrost-Set-the-heap-context-only-once-at-context-c.patch
Patch122:	0023-panfrost-Move-the-heap-descriptor-creation-to-panfro.patch
Patch123:	0024-panfrost-run-clang-format.patch
Patch124:	0025-fixup-panfrost-Abstract-some-kernel-driver-operation.patch
Patch125:	0026-panfrost-return-error-from-panthor_kmod_bo_get_sync_.patch
Patch126:	0027-panfrost-handle-errors-in-panthor_kmod_bo_get_sync_p.patch
Patch127:	0028-panfrost-debug_printf-on-unlikely-errors.patch
Patch128:	0029-fixup-panfrost-Abstract-some-kernel-driver-operation.patch
Patch129:	0030-fixup-panfrost-debug_printf-on-unlikely-errors.patch
Patch130:	0031-panfrost-Fix-gnu-empty-initializer-warning.patch
Patch131:	0032-fixup-panfrost-v10-support.patch
Patch132:	0033-Revert-panfrost-consult-draws-instead-of-draw_count.patch
Patch133:	0034-fixup-panfrost-v10-support.patch
Patch134:	0035-panfrost-Set-batch-any_compute-true-any-time-we-issu.patch
# Doesn't apply and isn't relevant outside of gitlab CI anyway
#Patch135:	0036-panfrost-Add-kmod-changes-to-CI-trigger.patch
Patch136:	0037-panfrost-kmod-Add-locking-to-panfrost_kmod_vm-va_to_.patch
Patch137:	0038-panfrost-Add-spec-egl-1.4-egl-ext_egl_image_storage-.patch
Patch138:	0039-panfrost-Create-a-dedicated-hook-for-batch-ending-cl.patch
Patch139:	0040-panfrost-introduce-and-use-PAN_USE_CSF.patch
Patch140:	0041-panfrost-Add-JOBX-wrappers-to-simplify-jm_-vs-csf_-h.patch
Patch141:	0042-panfrost-merge-top-level-draw-functions.patch
Patch142:	0043-panfrost-reuse-panfrost_launch_xfb-for-v10.patch
Patch143:	0044-panfrost-merge-panfrost_direct_draw-functions.patch
Patch144:	0045-panfrost-clean-up-index_size-logic.patch
Patch145:	0046-panfrost-Inline-panfrost_emit_heap_set.patch
Patch146:	0047-panfrost-Use-JOBX-for-the-context_-init-cleanup-hook.patch
Patch147:	0048-panfrost-Use-JOBX-for-emit_batch_end.patch
Patch148:	0049-panfrost-Use-JOBX-for-tiler-heap-desc-emission.patch
Patch149:	0050-panfrost-s-panfrost_emit_shader_regs-csf_emit_shader.patch
Patch150:	0051-panfrost-Use-JOBX-for-init_batch.patch
Patch151:	0052-panfrost-Rename-panfrost_start_tiling-and-use-JOBX.patch
Patch152:	0053-panfrost-Provide-CSF-JM-specific-emit_fragment_job-h.patch
Patch153:	0054-panfrost-Use-JOBX-for-job-backend-specific-launch_xf.patch
Patch154:	0055-panfrost-Deduplicate-panfrost_launch_grid.patch
Patch155:	0056-panfrost-Move-vertex_count-calculation-out-of-panfro.patch
Patch156:	0057-panfrost-Move-job-backend-specific-bits-out-of-panfr.patch
Patch157:	0058-panfrost-Allocate-the-temporary-geometry-buffer-once.patch
Patch158:	0059-panfrost-Set-any_compute-true-in-the-panfrost_launch.patch
Patch159:	0060-panfrost-Move-draw_count-increment-to-jm-csf-_emit_d.patch
Patch160:	0061-panfrost-Prepare-uniform-buffers-in-panfrost_launch_.patch
Patch161:	0062-panfrost-Use-a-1-task-increment-in-csf_launch_xfb.patch
Patch162:	0063-panfrost-Make-CS-decoding-more-robust.patch
Patch163:	0064-panfrost-Move-occlusion_query-init-out-of-the-if-fs_.patch

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
BuildRequires:	python%{pyver}dist(mako) >= 0.8.0
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
BuildRequires:	(devel(libLLVM-17) or devel(libLLVM-16))
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

# This is intentionally packaged separately and not installed by default
# until https://gitlab.freedesktop.org/mesa/mesa/-/issues/8106 gets fixed.
%package -n %{dridrivers}-zink
Summary:	OpenGL driver that emits Vulkan calls
Requires:	%{dridrivers} = %{EVRD}

%description -n %{dridrivers}-zink
OpenGL driver that emits Vulkan calls

This allows OpenGL applictions to run on hardware that
has only a Vulkan driver.

%ifarch %{armx} %{riscv}
%package -n freedreno-tools
Summary:	Tools for debugging the Freedreno graphics driver
Requires:	%{dridrivers} = %{EVRD}

%description -n freedreno-tools
Tools for debugging the Freedreno graphics driver.
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
Requires:	%{libosmesa} = %{EVRD}

%description -n %{devosmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

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

%package -n %{libglapi}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%description -n %{libglapi}
This package provides the glapi shared library used by gallium.

%package -n %{devglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Requires:	%{libglapi} = %{EVRD}
Obsoletes:	%{_lib}glapi0-devel < %{EVRD}

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
Requires:	%{libxatracker} = %{EVRD}

%description -n %{devxatracker}
This package contains the headers needed to compile programs against
the xatracker shared library.
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
Requires:	%{libd3d} = %{EVRD}
Provides:	d3d-devel = %{EVRD}

%description -n %{devd3d}
This package contains the headers needed to compile Direct3D 9 programs.

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

%description -n %{lib32gl}
Mesa is an OpenGL 4.6+ and ES 3.1+ compatible 3D graphics library.
GL and GLX parts.

%package -n %{dev32gl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib) (32-bit)
Group:		Development/C
Requires:	devel(libGL)
Requires:	%{dev32egl} = %{EVRD}
Requires:	%{devgl} = %{EVRD}

%description -n %{dev32gl}
This package contains the headers needed to compile Mesa programs.

%package -n %{lib32glapi}
Summary:	Files for mesa (glapi libs) (32-bit)
Group:		System/Libraries

%description -n %{lib32glapi}
This package provides the glapi shared library used by gallium.

%package -n %{dev32glapi}
Summary:	Development files for glapi libs (32-bit)
Group:		Development/C
Requires:	%{devglapi} = %{EVRD}
Requires:	%{lib32glapi} = %{EVRD}

%description -n %{dev32glapi}
This package contains the headers needed to compile programs against
the glapi shared library.

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

%package -n %{lib32xatracker}
Summary:	Files for mesa (xatracker libs) (32-bit)
Group:		System/Libraries

%description -n %{lib32xatracker}
This package provides the xatracker shared library used by gallium.

%package -n %{dev32xatracker}
Summary:	Development files for xatracker libs (32-bit)
Group:		Development/C
Requires:	%{lib32xatracker} = %{EVRD}
Requires:	%{devxatracker} = %{EVRD}

%description -n %{dev32xatracker}
This package contains the headers needed to compile programs against
the xatracker shared library.

%package -n %{lib32osmesa}
Summary:	Mesa offscreen rendering library (32-bit)
Group:		System/Libraries

%description -n %{lib32osmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n %{dev32osmesa}
Summary:	Development files for libosmesa (32-bit)
Group:		Development/C
Requires:	%{lib32osmesa} = %{EVRD}
Requires:	%{devosmesa} = %{EVRD}

%description -n %{dev32osmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%package -n %{lib32d3d}
Summary:	Mesa Gallium Direct3D 9 state tracker (32-bit)
Group:		System/Libraries

%description -n %{lib32d3d}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides Direct3D 9 support.

%package -n %{dev32d3d}
Summary:	Development files for Direct3D 9 libs
Group:		Development/C
Requires:	%{devd3d} = %{EVRD}
Requires:	%{lib32d3d} = %{EVRD}

%description -n %{dev32d3d}
This package contains the headers needed to compile Direct3D 9 programs.

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

%package -n %{lib32cl}
Summary:	Mesa OpenCL libs (32-bit)
Group:		System/Libraries
Recommends:	libOpenCL

%description -n %{lib32cl}
Open Computing Language (OpenCL) is a framework for writing programs that
execute across heterogeneous platforms consisting of central processing units
(CPUs), graphics processing units (GPUs), DSPs and other processors.

OpenCL includes a language (based on C99) for writing kernels (functions that
execute on OpenCL devices), plus application programming interfaces (APIs) that
are used to define and then control the platforms. OpenCL provides parallel
computing using task-based and data-based parallelism. OpenCL is an open
standard maintained by the non-profit technology consortium Khronos Group.
It has been adopted by Intel, Advanced Micro Devices, Nvidia, and ARM Holdings.

%package -n %{dev32cl}
Summary:	Development files for OpenCL libs (32-bit)
Group:		Development/Other
Requires:	%{lib32cl} = %{EVRD}
Requires:	%{devcl} = %{EVRD}
Requires:	opencl-headers

%description -n %{dev32cl}
Development files for the OpenCL library.
%endif

%if %{with opencl}
%package -n %{libcl}
Summary:	Mesa OpenCL libs
Group:		System/Libraries
Provides:	mesa-libOpenCL = %{EVRD}
Provides:	mesa-opencl = %{EVRD}
Recommends:	%{_lib}OpenCL

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
Requires:	%{libcl} = %{EVRD}
Provides:	%{clname}-devel = %{EVRD}
Provides:	mesa-libOpenCL-devel = %{EVRD}
Provides:	mesa-opencl-devel = %{EVRD}
Requires:	opencl-headers
Recommends:	cmake(OpenCLICDLoader)

%description -n %{devcl}
Development files for the OpenCL library
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
Requires:	%{devglapi} = %{EVRD}
Suggests:	%{devd3d} = %{EVRD}
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
%autosetup -p1 -n mesa-%{?git:%{git}}%{!?git:%{version}%{vsuffix}}
chmod +x %{SOURCE5}

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

if ! %meson32 \
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	--cross-file=i686.cross \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dglx=auto \
	-Dplatforms=wayland,x11 \
	-Dvulkan-layers=device-select,overlay \
	-Dvulkan-drivers=auto \
	-Dvulkan-beta=true \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dxlib-lease=auto \
	-Dosmesa=true \
	-Dandroid-libbacktrace=disabled \
	-Dvalgrind=disabled \
	-Dglvnd=true \
%if %{with opencl}
	-Dgallium-opencl=icd \
	-Dopencl-spirv=true \
%else
	-Dgallium-opencl=disabled \
%endif
	-Dgallium-va=enabled \
	-Dgallium-vdpau=enabled \
	-Dgallium-xa=enabled \
	-Dgallium-nine=true \
	-Dgallium-drivers=auto,crocus \
	-Ddri3=enabled \
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
	-Dtools=""; then

	cat build32/meson-logs/meson-log.txt >/dev/stderr
fi

%ninja_build -C build32/
rm llvm-config
%endif

# FIXME keep in sync with with_tools=all definition from meson.build
TOOLS="drm-shim,dlclose-skip,glsl,nir,nouveau"
%ifarch %{armx}
TOOLS="$TOOLS,etnaviv,freedreno,lima,panfrost,imagination"
%endif
%ifarch %{ix86} %{x86_64}
%if %{with intel}
TOOLS="$TOOLS,intel"
%if %{with aubinatorviewer}
TOOLS="$TOOLS,intel-ui"
%endif
%endif
%endif

if ! %meson \
	-Dmicrosoft-clc=disabled \
	-Dshared-llvm=enabled \
	-Db_ndebug=true \
	-Dc_std=c11 \
	-Dcpp_std=c++17 \
	-Dandroid-libbacktrace=disabled \
%ifarch %{armx}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,freedreno,etnaviv,tegra,vc4,v3d,kmsro,lima,panfrost,zink \
%else
%ifarch %{riscv}
	-Dgallium-drivers=auto,r300,r600,svga,radeonsi,etnaviv,kmsro,zink \
%else
	-Dgallium-drivers=auto,crocus,zink \
%endif
%endif
%ifarch %{x86_64}
	-Dintel-clc=enabled \
%endif
%if %{with opencl}
	-Dgallium-opencl=icd \
	-Dopencl-spirv=true \
%else
	-Dgallium-opencl=disabled \
%endif
	-Dgallium-va=enabled \
	-Dgallium-vdpau=enabled \
	-Dgallium-xa=enabled \
	-Dgallium-nine=true \
	-Dglx=dri \
	-Dplatforms=wayland,x11 \
	-Degl-native-platform=wayland \
	-Dvulkan-layers=device-select,overlay \
%ifarch %{armx}
	-Dvulkan-drivers=auto,broadcom,freedreno,panfrost,virtio,imagination-experimental \
%else
%ifarch %{riscv}
	-Dvulkan-drivers=auto,virtio,imagination-experimental \
%else
	-Dvulkan-drivers=auto,virtio \
%endif
%endif
	-Dvulkan-beta=true \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dxlib-lease=auto \
	-Dosmesa=true \
	-Dglvnd=true \
	-Ddri3=enabled \
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
%ifarch %{armx}
%{_bindir}/lima_compiler
%{_bindir}/lima_disasm
%endif
%{_libdir}/dri/*.so
%exclude %{_libdir}/dri/zink_dri.so
%ifarch %{armx} %{riscv}
%{_libdir}/libpowervr_rogue.so
%endif
%if %{with opencl}
%{_libdir}/gallium-pipe/*.so
%endif
%{_libdir}/lib*_noop_drm_shim.so
# vulkan stuff
%{_libdir}/libVkLayer_*.so
%{_datadir}/vulkan/implicit_layer.d/*.json
%{_bindir}/mesa-overlay-control.py
%{_datadir}/vulkan/explicit_layer.d/*.json
%{_libdir}/libvulkan_*.so
%{_datadir}/vulkan/icd.d/*_icd.*.json

%files -n %{dridrivers}-zink
%{_libdir}/dri/zink_dri.so

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

%files -n %{libosmesa}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{devosmesa}
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files -n %{libgl}
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libGLX_mesa.so.0*
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

%files -n %{devglapi}
%{_libdir}/libglapi.so

#vdpau enblaed
%if %{with vdpau}
%files -n %{vdpaudrivers}
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau*.so.*
%endif

%if ! %{with bootstrap}
%files -n %{devxatracker}
%{_libdir}/libxatracker.so
%{_includedir}/xa_*.h
%{_libdir}/pkgconfig/xatracker.pc
%endif

%files -n %{devd3d}
%{_includedir}/d3dadapter
%{_libdir}/d3d/d3dadapter9.so
%{_libdir}/pkgconfig/d3d.pc

%if %{with opencl}
%files -n %{devcl}
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
%endif

%files tools
%ifarch %{ix86} %{x86_64}
%{_bindir}/aubinator
%{_bindir}/aubinator_error_decode
%if %{with aubinatorviewer}
%{_bindir}/aubinator_viewer
%endif
%{_bindir}/i965_asm
%{_bindir}/i965_disasm
%{_bindir}/intel_dev_info
%{_bindir}/intel_dump_gpu
%{_bindir}/intel_error2aub
%{_bindir}/intel_sanitize_gpu
%{_bindir}/intel_stub_gpu
%{_libexecdir}/libintel_dump_gpu.so
%{_libexecdir}/libintel_sanitize_gpu.so
%endif
%ifarch %{armx}
%{_bindir}/etnaviv_compiler
%{_bindir}/panfrostdump
%{_bindir}/panfrost_texfeatures
%{_bindir}/rddecompiler
%{_bindir}/replay
%endif
%{_bindir}/glsl_compiler
%{_bindir}/glsl_test
%{_bindir}/nouveau_compiler
%{_bindir}/spirv2nir
%{_libdir}/libdlclose-skip.so

%if %{with compat32}
%files -n %{lib32d3d}
%dir %{_prefix}/lib/d3d
%{_prefix}/lib/d3d/d3dadapter9.so.%{d3dmajor}*

%files -n %{dev32d3d}
%{_prefix}/lib/d3d/d3dadapter9.so
%{_prefix}/lib/pkgconfig/d3d.pc

%files -n %{lib32egl}
%{_prefix}/lib/libEGL_mesa.so.%{eglmajor}*

%files -n %{dev32egl}
%{_prefix}/lib/libEGL_mesa.so

%files -n %{lib32gl}
%{_prefix}/lib/libGLX_mesa.so.0*
%dir %{_prefix}/lib/dri
%dir %{_prefix}/lib/gallium-pipe

%files -n %{dev32gl}
%{_prefix}/lib/pkgconfig/dri.pc
%{_prefix}/lib/libGLX_mesa.so

%files -n %{lib32cl}
%{_prefix}/lib/libMesaOpenCL.so.*

%files -n %{dev32cl}
%{_prefix}/lib/libMesaOpenCL.so

%files -n %{lib32osmesa}
%{_prefix}/lib/libOSMesa.so.%{osmesamajor}*

%files -n %{dev32osmesa}
%{_prefix}/lib/libOSMesa.so
%{_prefix}/lib/pkgconfig/osmesa.pc

%files -n %{lib32xatracker}
%{_prefix}/lib/libxatracker.so.*

%files -n %{dev32xatracker}
%{_prefix}/lib/libxatracker.so
%{_prefix}/lib/pkgconfig/xatracker.pc

%files -n %{lib32gbm}
%{_prefix}/lib/libgbm.so.*

%files -n %{dev32gbm}
%{_prefix}/lib/libgbm.so
%{_prefix}/lib/pkgconfig/gbm.pc

%files -n %{lib32glapi}
%{_prefix}/lib/libglapi.so.*

%files -n %{dev32glapi}
%{_prefix}/lib/libglapi.so

%files -n %{dridrivers32}
%{_prefix}/lib/dri/*.so
%{_prefix}/lib/gallium-pipe/*.so
%{_prefix}/lib/libVkLayer_*.so
%{_prefix}/lib/libvulkan_*.so
%{_prefix}/lib/vdpau/libvdpau_*.so*
%endif

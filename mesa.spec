# (cg) Cheater...
%define Werror_cflags %nil

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define build_plf 0

%define with_hardware 1

%define git 0
%define git_branch 9.0
%define with_hardware 1

%define opengl_ver 3.0

%define relc	0

%bcond_without vdpau
%bcond_with va
%bcond_without wayland

%if %{relc}
%define vsuffix -rc%{relc}
%else
%define vsuffix %nil
%endif

%define eglmajor		1
%define eglname			egl
%define libeglname		%mklibname %{eglname} %{eglmajor}
%define develegl		%mklibname %{eglname} -d

%define glmajor			1
%define glname			gl
%define libglname		%mklibname %{glname} %{glmajor}
%define develgl			%mklibname %{glname} -d

%define glesv1major		1
%define glesv1name		glesv1
%define libglesv1name		%mklibname %{glesv1name}_ %{glesv1major}
%define develglesv1		%mklibname %{glesv1name} -d

%define glesv2major		2
%define glesv2name		glesv2
%define libglesv2name		%mklibname %{glesv2name}_ %{glesv2major}
%define develglesv2		%mklibname %{glesv2name} -d

%define openvgmajor		1
%define openvgname		openvg
%define libopenvgname		%mklibname %{openvgname} %{openvgmajor}
%define developenvg		%mklibname %{openvgname} -d

%define glapimajor		0
%define glapiname		glapi
%define libglapiname		%mklibname %{glapiname} %{glapimajor}
%define develglapi		%mklibname %{glapiname} -d

%define dridrivers		%mklibname dri-drivers

%define dricoremajor		1
%define dricorename		dricore
%define libdricorename		%mklibname %{dricorename} %{dricoremajor}
%define develdricore		%mklibname %{dricorename} -d

%define gbmmajor		1
%define gbmname			gbm
%define libgbmname		%mklibname %{gbmname} %{gbmmajor}
%define develgbm		%mklibname %{gbmname} -d

%define waylandeglmajor		1
%define waylandeglname		wayland-egl
%define libwaylandeglname	%mklibname %{waylandeglname} %{waylandeglmajor}
%define develwaylandegl		%mklibname %{waylandeglname} -d

%define libvadrivers		%mklibname libva-drivers

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i915,i965,nouveau,r200,radeon,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"r200,radeon,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i915,i965,r200,radeon,swrast"
%define	dri_drivers_alpha	"r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,radeon,swrast"
%define dri_drivers_mipsel	"r200,radeon"
%define dri_drivers_arm		"swrast"
%ifarch	%{arm}
%define	dri_drivers		%{expand:%{dri_drivers_arm}}
%else
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}
%endif

%define short_ver 9.0.1

Name:		mesa
Version:	9.0.1
%if %relc
%if %git
Release:	0.rc%relc.0.%git.1
%else
Release:	0.rc%relc.1
%endif
%else
%if %git
Release:	0.%git.6.1
%else
Release:	1
%endif
%endif
Summary:	OpenGL 3.0 compatible 3D graphics library
Group:		System/Libraries

License:	MIT
URL:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git_branch}-%{git}.tar.bz2
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/MesaLib-%{short_ver}%{vsuffix}.tar.bz2
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install

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

# Patches "liberated" from Fedora:
# Patches from ChromiumOS
Patch901: 0901-gallium-only-link-static-archives-between-ld-start-e.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	llvm-devel
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	makedepend
BuildRequires:	x11-proto-devel >= 7.3
BuildRequires:	libxml2-python
BuildRequires:	pkgconfig(libdrm) >= 2.4.21
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(xfixes)	>= 4.0.3
BuildRequires:	pkgconfig(xt)		>= 1.0.5
BuildRequires:	pkgconfig(xmu)		>= 1.0.3
BuildRequires:	pkgconfig(x11)		>= 1.3.3
BuildRequires:	pkgconfig(xdamage)	>= 1.1.1
BuildRequires:	pkgconfig(xext)		>= 1.1.1
BuildRequires:	pkgconfig(xxf86vm)	>= 1.1.0
BuildRequires:	pkgconfig(xi)		>= 1.3
BuildRequires:	pkgconfig(xorg-server)	>= 1.11.0
BuildRequires:	pkgconfig(xvmc)
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau)	>= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva)	>= 0.31.0
%endif
%if %{with wayland}
BuildRequires:	wayland-devel
%endif

# package mesa
Requires:	%{libglname} = %{version}-%{release}

#------------------------------------------------------------------------------

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Conflicts:	%{_lib}MesaGL1 < 7.7-5
%rename %{_lib}dri-drivers-experimental

%package -n	%{libdricorename}
Summary:	Shared library for DRI drivers
Group:		System/Libraries

%package -n	%{libvadrivers}
Summary:	Mesa libVA video acceleration drivers
Group:		System/Libraries

%package -n	%{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Provides:	libmesa%{glname} = %{version}-%{release}
Requires:	%{dridrivers} >= %{version}-%{release}
%if %{build_plf}
Requires:	%mklibname txc-dxtn
%endif
Obsoletes:	%{_lib}mesagl1 < %{version}-%{release}

%package -n	%{develgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{libglname} = %{version}-%{release}
Provides:	libmesa%{glname}-devel = %{version}-%{release}
Provides:	mesa%{glname}-devel = %{version}-%{release}
Provides:	GL-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{version}-%{release}

%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0

%package -n	%{develegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libeglname} = %{version}-%{release}
Provides:	lib%{eglname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{version}-%{release}

%package -n %{libglapiname}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%package -n %{develglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Obsoletes:	%{_lib}glapi0-devel < %{version}-%{release}

%package -n	%{develdricore}
Summary:	Development files for DRI core
Group:		Development/C
Requires:	%{libdricorename} = %{version}-%{release}
Provides:	lib%{dricorename}-devel = %{version}-%{release}
Provides:	%{dricorename}-devel = %{version}-%{release}

%package -n %{libglesv1name}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1 < 8.0

%package -n %{develglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1name} = %{version}-%{release}
Provides:	lib%{glesv1name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{version}-%{release}

%package -n %{libglesv2name}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0

%package -n %{develglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2name} = %{version}-%{release}
Provides:	lib%{glesv2name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{version}-%{release}

%package -n %{libopenvgname}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaopenvg1 < 8.0

%package -n %{developenvg}
Summary:	Development files vor OpenVG libs
Group:		Development/C
Requires:	%{libopenvgname} = %{version}-%{release}
Provides:	lib%{openvgname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaopenvg1-devel < 8.0

%if %{with wayland}
%package -n %{libgbmname}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries

%package -n %{develgbm}
Summary:	Development files for Mesa (gbm libs)
Group:		Development/C
Requires:	%{libgbmname} = %{version}-%{release}
Provides:	lib%{gbmname}-devel = %{version}-%{release}
Provides:	%{gbmname}-devel = %{version}-%{release}

%package -n %{libwaylandeglname}
Summary:	Files for Mesa (Wayland EGL libs)
Group:		System/Libraries

%package -n %{develwaylandegl}
Summary:	Development files for Mesa (Wayland EGL libs)
Group:		Development/C
Requires:	%{libwaylandeglname} = %{version}-%{release}
Provides:	lib%{waylandeglname}-devel = %{version}-%{release}
Provides:	%{waylandeglname}-devel = %{version}-%{release}
%endif

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{develgl} = %{version}-%{release}
Requires:	%{develegl} = %{version}-%{release}
Requires:	%{develglapi} = %{version}-%{release}
Requires:	%{develglesv1} = %{version}-%{release}
Requires:	%{develglesv2} = %{version}-%{release}

#------------------------------------------------------------------------------

%description
Mesa is an OpenGL 3.0 compatible 3D graphics library.

%if %{build_plf}
This package is in the restricted repository because it enables some
OpenGL extentions that are covered by software patents.
%endif

%description -n %{dridrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
DRI drivers.

%description -n %{libdricorename}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
DRI core part.

%description -n %{libvadrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
libVA drivers for video acceleration

%description common-devel
Mesa common metapackage devel

%description -n %{libeglname}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL parts.

%description -n %{develegl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
EGL development parts.

%description -n %{libglname}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
GL and GLX parts.

%description -n %{develgl}
Mesa is an OpenGL 3.0 compatible 3D graphics library.

This package contains the headers needed to compile Mesa programs.

%description -n %{libglapiname}
This package provides the glapi shared library used by gallium.

%description -n %{develglapi}
This package contains the headers needed to compile programs against
the glapi shared library.

%description -n %{develdricore}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.

This package contains the headers needed to compile DRI drivers.

%description -n %{libglesv1name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%description -n %{develglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%description -n %{libglesv2name}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%description -n %{develglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%description -n %{libopenvgname}
OpenVG is a royalty-free, cross-platform API that provides a low-level hardware
acceleration interface for vector graphics libraries such as Flash and SVG.

%description -n %{developenvg}
Development files for OpenVG library.

%if %{with wayland}
%description -n %{libgbmname}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%description -n %{develgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.

%description -n %{libwaylandeglname}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform parts.

%description -n %{develwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform development parts.
%endif

#------------------------------------------------------------------------------

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

%build
# fix build - TODO: should this be fixed in llvm somehow, or maybe the library
# symlinks should be moved to %{_libdir}? -Anssi 08/2012
export LDFLAGS="-L%{_libdir}/llvm"

# Replacing --disable-glx-tls with --enable-glx-tls
# below would be good - but unfortunately it seems to
# break the nvidia binary-only driver.
%configure2_5x \
	--with-dri-driverdir=%{driver_dir} \
	--with-dri-drivers="%{dri_drivers}" \
	--enable-shared-dricore \
	--enable-egl \
	--enable-dri \
	--enable-glx \
	--enable-xorg \
	--enable-xa \
	--enable-xvmc \
%if %{with wayland}
	--with-egl-platforms=x11,wayland,drm \
	--enable-gbm \
	--enable-shared-glapi \
%endif
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
	--enable-gles1 \
	--enable-gles2 \
	--enable-openvg \
	--enable-gallium-egl \
	--disable-glx-tls \
	--enable-gallium-g3dvl \
%if %{with_hardware}
	--with-gallium-drivers=r300,r600,radeonsi,nouveau,swrast \
   	--enable-gallium-llvm \
%else
   	--disable-gallium-llvm \
   	--with-gallium-drivers=swrast \
%endif
%if %{build_plf}
   	--enable-texture-float
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p %{buildroot}%{_libdir}/mesa
pushd %{buildroot}%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so

#------------------------------------------------------------------------------

%files
%doc docs/COPYING docs/README.*
%config(noreplace) %{_sysconfdir}/drirc

%files -n %{dridrivers}
%ifnarch ppc64
%dir %{_libdir}/dri
# (blino) new mesa 8.1 and 9.0 build system seems to use a static libglsl
#%{_libdir}/dri/libglsl.so
%{_libdir}/dri/*_dri.so
%{_libdir}/libXvMCnouveau.so.*
%{_libdir}/libXvMCr300.so.*
%{_libdir}/libXvMCr600.so.*
%{_libdir}/libXvMCsoftpipe.so.*
%if %{with vdpau}
%{_libdir}/vdpau/libvdpau_nouveau.so*
%{_libdir}/vdpau/libvdpau_r300.so*
%{_libdir}/vdpau/libvdpau_r600.so*
%{_libdir}/vdpau/libvdpau_radeonsi.so*
%{_libdir}/vdpau/libvdpau_softpipe.so*
%endif
%{_libdir}/xorg/modules/drivers/nouveau2_drv.so
%{_libdir}/xorg/modules/drivers/r300_drv.so
%{_libdir}/xorg/modules/drivers/r600g_drv.so
%{_libdir}/xorg/modules/drivers/radeonsi_drv.so
%endif

%files -n %{libdricorename}
%{_libdir}/libdricore%{version}.so.%{dricoremajor}
%{_libdir}/libdricore%{version}.so.%{dricoremajor}.*

%if %{with va}
%files -n %{libvadrivers}
%{_libdir}/va/lib*.so*
%endif

%files -n %{libglname}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*

%files -n %{libeglname}
%{_libdir}/libEGL.so.%{eglmajor}*
%dir %{_libdir}/egl
%if !%{with wayland}
%{_libdir}/egl/st_GL.so
%endif
%{_libdir}/egl/egl_gallium.so

%files -n %{libglapiname}
%{_libdir}/libglapi.so.%{glapimajor}*

%files -n %{libglesv1name}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2name}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libopenvgname}
%{_libdir}/libOpenVG.so.%{openvgmajor}*

%if %{with wayland}
%files -n %{libgbmname}
%{_libdir}/libgbm.so.%{gbmmajor}
%{_libdir}/libgbm.so.%{gbmmajor}.*
%{_libdir}/gbm/gbm_*.so
%{_libdir}/gbm/pipe_*.so

%files -n %{libwaylandeglname}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}.*
%endif

%files -n %{develgl}
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%{_libdir}/libXvMC*.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files common-devel
# meta devel pkg

%files -n %{develegl}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc

%files -n %{develglapi}
%{_libdir}/libglapi.so

%files -n %{develdricore}
%{_libdir}/libdricore%{version}.so

%files -n %{develglesv1}
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{develglesv2}
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{developenvg}
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_libdir}/pkgconfig/vg.pc

%if %{with wayland}
%files -n %{develgbm}
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc

%files -n %{develwaylandegl}
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif

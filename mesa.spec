# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define build_plf 0
%define with_hardware 1

%define git		0
%define relc	0

%bcond_without vdpau
%bcond_without va

%if %{relc}
%define vsuffix -rc%{relc}
%else
%define vsuffix	%nil
%endif

%define eglmajor		1
%define eglname			egl
%define libeglname		%mklibname %{eglname} %{eglmajor}
%define develegl		%mklibname %{eglname} -d

%define glmajor			1
%define glname			gl
%define libglname		%mklibname %{glname} %{glmajor}
%define develgl			%mklibname %{glname} -d

%define glumajor		1
%define gluname			glu
%define libgluname		%mklibname %{gluname} %{glumajor}
%define develglu		%mklibname %{gluname} -d

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

%define xatrackermajor		1
%define xatrackername		xatracker
%define libxatrackername	%mklibname %xatrackername %xatrackermajor
%define develxatracker		%mklibname %xatrackername -d

%define dridrivers		%mklibname dri-drivers

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

Name:		mesa
Version: 	8.0.3
%if %relc
%if %git
Release:	0.rc%relc.0.%git.1
%else
Release:	0.rc%relc.1
%endif
%else
%if %git
Release:	0.%git.1
%else
Release:	2
%endif
%endif
Summary:	OpenGL 3.0 compatible 3D graphics library
Group:		System/Libraries

License:	MIT
URL:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git}.tar.bz2
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%version/MesaLib-%{version}%{vsuffix}.tar.bz2
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

# Patches "liberated" from Fedora:
# http://cvs.fedoraproject.org/viewvc/rpms/mesa/devel/
# git format-patch --start-number 300 mdv-cherry-picks..mdv-redhat

# Mandriva & Mageia patches
Patch900: 0900-Mips-support.patch
Patch901: Mesa-8.0.1-libva-0.32.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:  llvm-devel
BuildRequires:	expat-devel		>= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	makedepend
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libxml2-python
BuildRequires:	pkgconfig(libdrm)	>= 2.4.21
BuildRequires:  pkgconfig(libudev)
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

# package mesa
Requires:	%{libglname} = %{version}-%{release}

#------------------------------------------------------------------------------

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Conflicts:	%{_lib}MesaGL1 < 7.7-5
%rename %{_lib}dri-drivers-experimental
# Lives in %_libdir/dri, but should be provided
# nevertheless...
%if "%_lib" != "lib"
Provides:	libdricore.so()(64bit)
Provides:	libglsl.so()(64bit)
%else
Provides:	libdricore.so
Provides:	libglsl.so
%endif

%package -n	%libvadrivers
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
Obsoletes:	%{_lib}mesagl1

%package -n	%{develgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{libglname} = %{version}-%{release}
Provides:	libmesa%{glname}-devel = %{version}-%{release}
Provides:	mesa%{glname}-devel = %{version}-%{release}
Provides:	GL-devel
Obsoletes:	%{_lib}mesagl1-devel

%package -n	%{libgluname}
Summary:	Files for Mesa (GLU libs)
Group:		System/Libraries
Provides:	libmesa%{gluname} = %{version}-%{release}
Obsoletes:	%{_lib}mesaglu1

%package -n	%{develglu}
Summary:	Development files for GLU libs
Group:		Development/C
Requires:	%{libgluname} = %{version}-%{release}
Provides:	libmesa%{gluname}-devel = %{version}-%{release}
Provides:	mesa%{gluname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}mesaglu1-devel

%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1

%package -n	%{develegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libeglname} = %{version}-%{release}
Provides:	lib%{eglname}-devel
Obsoletes:	%{_lib}mesaegl1-devel

%package -n %{libglapiname}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%package -n %{develglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Obsoletes:	%{_lib}glapi0-devel

%package -n %libxatrackername
Summary:	Files for mesa (xatracker libs)
Group:		System/Libraries

%package -n %develxatracker
Summary:	Development files for xatracker libs
Group:		Development/C

%package -n %{libglesv1name}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1

%package -n %{develglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1name} = %{version}-%{release}
Provides:	lib%{glesv1name}-devel
Obsoletes:	%{_lib}mesaglesv1_1-devel

%package -n %{libglesv2name}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2

%package -n %{develglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2name} = %{version}-%{release}
Provides:	lib%{glesv2name}-devel
Obsoletes:	%{_lib}mesaglesv2_2-devel

%package -n %{libopenvgname}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaopenvg1

%package -n %{developenvg}
Summary:	Development files vor OpenVG libs
Group:		Development/C
Requires:	%{libopenvgname} = %{version}-%{release}
Provides:	lib%{openvgname}-devel
Obsoletes:	%{_lib}mesaopenvg1-devel

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	%{develegl} = %{version}
Requires:	%{develglapi} = %{version}
Requires:	%develxatracker = %version
Requires:	%{develglu} = %{version}
Requires:	freeglut-devel
Requires:	%{develgl} = %{version}
Requires:	%{develglesv1} = %{version}
Requires:	%{develglesv2} = %{version}

#------------------------------------------------------------------------------

%description
Mesa is an OpenGL 3.0 compatible 3D graphics library.
%if %{build_plf}

This package is in the "tainted" section because it enables some
OpenGL extentions that are covered by software patents.
%endif

%description -n %{dridrivers}
Mesa is an OpenGL 3.0 compatible 3D graphics library.
DRI drivers.

%description -n %libvadrivers
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

%description -n %{libgluname}
GLU is the OpenGL Utility Library.
It provides a number of functions upon the base OpenGL library to provide
higher-level drawing routines from the more primitive routines provided by
OpenGL.

%description -n %{develglu}
This package contains the headers needed to compile programs with GLU.

%description -n %{libglapiname}
This package provides the glapi shared library used by gallium.

%description -n %{develglapi}
This package contains the headers needed to compile programs against
the glapi shared library.

%description -n %libxatrackername
This package provides the xatracker shared library used by gallium.

%description -n %develxatracker
This package contains the headers needed to compile programs against
the xatracker shared library.

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

#------------------------------------------------------------------------------

%prep
%if %{git}
%setup -qn mesa-%{git}
%else
%setup -qn Mesa-%{version}%{vsuffix}
%endif

%apply_patches
chmod +x %{SOURCE5}

# Needed after vaapi 0.32 support patch
autoconf

%build
#%if %{git}
#./autogen.sh -v
#%endif

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
	--with-gallium-drivers=svga,i915,r300,r600,nouveau,swrast \
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

%files -n %{dridrivers}
%ifnarch ppc64
%dir %{_libdir}/dri
%{_libdir}/dri/libdricore.so
%{_libdir}/dri/libglsl.so
%{_libdir}/dri/*_dri.so
%_libdir/libXvMCnouveau.so.*
%_libdir/libXvMCr300.so.*
%_libdir/libXvMCr600.so.*
%_libdir/libXvMCsoftpipe.so.*
%if %{with vdpau}
%_libdir/vdpau/libvdpau_nouveau.so*
%_libdir/vdpau/libvdpau_r300.so*
%_libdir/vdpau/libvdpau_r600.so*
%_libdir/vdpau/libvdpau_softpipe.so*
%endif
%_libdir/xorg/modules/drivers/modesetting_drv.so
%_libdir/xorg/modules/drivers/nouveau2_drv.so
%_libdir/xorg/modules/drivers/r300_drv.so
%_libdir/xorg/modules/drivers/r600g_drv.so
%endif

%if %{with va}
%files -n %libvadrivers
%_libdir/va/lib*.so*
%endif

%files -n %{libglname}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*

%files -n %{libgluname}
%{_libdir}/libGLU.so.%{glumajor}*

%files -n %{libeglname}
%{_libdir}/libEGL.so.%{eglmajor}*
%dir %{_libdir}/egl
%{_libdir}/egl/st_GL.so
%{_libdir}/egl/egl_gallium.so

%files -n %{libglapiname}
%{_libdir}/libglapi.so.%{glapimajor}*

%files -n %libxatrackername
%_libdir/libxatracker.so.%{xatrackermajor}*

%files -n %{libglesv1name}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2name}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libopenvgname}
%{_libdir}/libOpenVG.so.%{openvgmajor}*

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
%_libdir/libXvMC*.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files -n %{develglu}
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%files common-devel
# meta devel pkg

%files -n %{develegl}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc

%files -n %{develglapi}
%{_libdir}/libglapi.so

%files -n %develxatracker
%_libdir/libxatracker.so
%_includedir/xa_*.h
%_libdir/pkgconfig/xatracker.pc

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


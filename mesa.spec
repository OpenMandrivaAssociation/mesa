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

# 00f9e4... is the merge-base of main and v10+panthor
%define git 78058a2a156e37217210a9dbd07cf471a98d4baf
%define git_branch panthor

%define relc 1

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
Version:	23.3.0
Release:	%{?relc:0.rc%{relc}.}%{?git:0.%{git}.}5
Group:		System/Libraries
License:	MIT
Url:		http://www.mesa3d.org
%if 0%{?git:1}
%if "%{git_branch}" == "panthor" || "%{git_branch}" == "panfrost"
Source0:	https://gitlab.freedesktop.org/panfrost/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
%else
Source0:	https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{git}/mesa-%{git}.tar.bz2
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

# Bring the v10+panthor tree up to -rc1
Patch0:		0001-docs-fix-linkcheck.patch
Patch1:		0002-docs-update-a-few-links-to-https.patch
Patch2:		0003-docs-update-anchor-for-link.patch
Patch3:		0004-docs-update-link-to-git-wiki.patch
Patch4:		0005-docs-link-to-upstream-etnaviv.patch
Patch5:		0006-docs-apply-some-trivial-redirects.patch
Patch6:		0007-docs-use-doc-role-when-linking-to-lists-article.patch
Patch7:		0008-docs-keep-up-with-intels-ever-moving-documentation.patch
Patch8:		0009-docs-mark-some-redirects-as-allowed.patch
Patch9:		0010-docs-only-link-to-old-docs-from-html.patch
Patch10:	0011-docs-use-html_static_path-for-static-files.patch
Patch11:	0012-pvr-fix-mipmap-size-calculation-for-bc-formats.patch
Patch12:	0013-pvr-Fix-cubemap-layer-stride.patch
Patch13:	0014-anv-implement-INTEL_DEBUG-reemit.patch
Patch14:	0015-anv-add-missing-workaround-handling-in-simple-shader.patch
Patch15:	0016-anv-fix-a-couple-of-missing-input-for-3DSTATE_RASTER.patch
Patch16:	0017-anv-flag-3DSTATE_RASTER-as-dirty-after-simple-shader.patch
Patch17:	0018-pvr-Use-the-render-passes-attachments-array-to-setup.patch
Patch18:	0019-pvr-Adjust-EOT-PBE-state-to-account-for-the-iview-s-.patch
Patch19:	0020-i915-Re-clang-format-and-enforce-it-in-CI.patch
Patch20:	0021-i915-Print-the-relevant-counts-vs-limits-when-throwi.patch
Patch21:	0022-i915-Don-t-log-I915_DEBUG-fs-output-for-blit-shaders.patch
Patch22:	0023-i915-Save-fragment-program-compile-error-messages-in.patch
Patch23:	0024-i915-Do-a-test-compile-at-glLinkShader-time.patch
Patch24:	0025-i915-Make-exceeding-tex-indirect-count-fatal.patch
Patch25:	0026-i915-Use-nir_group_loads-to-reduce-texture-indirecti.patch
Patch26:	0027-nir-fix-several-crashes-in-nir_lower_tex.patch
Patch27:	0028-egl-don-t-set-ForceSoftware-for-all-zink-loading.patch
Patch28:	0029-zink-error-at-handle-export-on-missing-EXT_image_drm.patch
Patch29:	0030-gbm-delete-some-zink-handling.patch
Patch30:	0031-iris-Lock-bufmgr-lock-before-call-vma_free-in-error-.patch
Patch31:	0032-iris-Nuke-useless-flags-from-iris_fine_fence_new.patch
Patch32:	0033-vulkan-runtime-add-internal-parameter-to-vk_spirv_to.patch
Patch33:	0034-nir-lower_int64-respect-rounding-mode-when-casting-t.patch
Patch34:	0035-intel-compiler-round-f2f16-correctly-for-RTNE-case.patch
Patch35:	0036-util-add-double_to_float16-helpers.patch
Patch36:	0037-nir-round-f2f16-_rtne-_rtz-correctly-for-constant-ex.patch
Patch37:	0038-ci-crocus-Generalize-the-drawarrays-vertex-count-fla.patch
Patch38:	0039-ci-zink-Skip-3-minute-long-glx-visuals-timeouts.patch
Patch39:	0040-ci-zink-Skip-dmat-34-op-tests-in-general-as-well.patch
Patch40:	0041-ci-crocus-Disable-flaky-unvanquished-ultra-trace.patch
Patch41:	0042-venus-remove-redundant-bo-roundtrip-and-add-more-doc.patch
Patch42:	0043-venus-track-VkPhysicalDeviceMemoryProperties-instead.patch
Patch43:	0044-venus-refactor-vn_device_memory-to-prepare-for-async.patch
Patch44:	0045-venus-make-device-memory-alloc-async.patch
Patch45:	0046-ac-radeonsi-move-ps-arg-pos_fixed_pt-to-ac_shader_ar.patch
Patch46:	0047-aco-do-not-eliminate-final-exec-write-when-p_end_wit.patch
Patch47:	0048-aco-remove-p_end_with_regs-from-needs_exact.patch
Patch48:	0049-aco-add-ps-prolog-generation-for-radeonsi.patch
Patch49:	0050-aco-handle-ps-outputs-from-radeonsi.patch
Patch50:	0051-aco-add-create_fs_end_for_epilog-for-radeonsi.patch
Patch51:	0052-aco-radv-remove-unused-ps-epilog-info-fields.patch
Patch52:	0053-aco-radv-rename-ps-epilog-info-inputs-to-colors.patch
Patch53:	0054-aco-simplify-export_fs_mrt_color.patch
Patch54:	0055-aco-radv-add-radeonsi-spec-ps-epilog-code.patch
Patch55:	0056-aco-compact-ps-expilog-color-export-for-radeonsi.patch
Patch56:	0057-aco-radv-radeonsi-pass-spi-ps-input-ena-and-addr.patch
Patch57:	0058-aco-do-not-fix_exports-when-program-has-epilog.patch
Patch58:	0059-aco-fix-assertion-fail-when-program-contains-empty-b.patch
Patch59:	0060-aco-create-exit-block-for-p_end_with_regs-to-branch-.patch
Patch60:	0061-aco-wait-memory-ops-done-before-go-to-next-shader-pa.patch
Patch61:	0062-radeonsi-reduce-sgpr-count-for-scratch_offset-when-a.patch
Patch62:	0063-radeonsi-init-spi_ps_input_addr-for-part-mode-ps.patch
Patch63:	0064-radeonsi-extract-si_prolog_get_internal_binding_slot.patch
Patch64:	0065-radeonsi-extract-si_get_ps_prolog_args-to-be-shared-.patch
Patch65:	0066-ac-radeonsi-remove-unused-ps-prolog-key-fields.patch
Patch66:	0067-radeonsi-add-ps-prolog-shader-part-build.patch
Patch67:	0068-radeonsi-extract-si_get_ps_epilog_args-to-be-shared-.patch
Patch68:	0069-radeonsi-fill-aco-shader-info-for-ps-part.patch
Patch69:	0070-radeonsi-add-ps-epilog-shader-part-build.patch
Patch70:	0071-radeonsi-enable-aco-compile-for-part-mode-ps.patch
Patch71:	0072-lavapipe-fix-some-whitespace-in-advance-of-other-cha.patch
Patch72:	0073-lavapipe-fix-subresource-layers-asserts.patch
Patch73:	0074-lavapipe-support-host-image-copying-on-compressed-te.patch
Patch74:	0075-llvmpipe-don-t-create-texture-functions-for-planar-t.patch
Patch75:	0076-lavapipe-don-t-emit-blit-src-dst-for-subsampled-form.patch
Patch76:	0077-llvmpipe-don-t-support-planar-formats-for-buffers.patch
Patch77:	0078-lavapipe-convert-sampler-to-use-vk-base-class.patch
Patch78:	0079-lavapipe-cleanup-copy-code-to-use-a-local-region-var.patch
Patch79:	0080-lavapipe-start-introducing-planes-structure.patch
Patch80:	0081-lavapipe-allocate-image-and-image-view-planes.patch
Patch81:	0082-lavapipe-handle-planes-in-copies.patch
Patch82:	0083-lavapipe-handle-planes-in-get-image-sub-resource.patch
Patch83:	0084-lavapipe-add-descriptor-sets-bindings-for-planar-ima.patch
Patch84:	0085-lavapipe-handle-planes-in-texture-lowering.patch
Patch85:	0086-lavapipe-expose-planar-ycbcr-formats-and-new-ycbcr-f.patch
Patch86:	0087-radv-fix-IB-alignment.patch
Patch87:	0088-lima-pp-Do-not-use-union-undefined-behaviour.patch
Patch88:	0089-nir-Add-trivial-nir_src_-getters.patch
Patch89:	0090-nir-Use-set_parent_instr-internally.patch
Patch90:	0091-nir-Use-getters-for-nir_src-parent_.patch
Patch91:	0092-nir-Assert-the-nir_src-union-is-used-safely.patch
Patch92:	0093-nir-Use-a-tagged-pointer-for-nir_src-parents.patch
Patch93:	0094-tu-Fix-stale-tu_render_pass_attachment-store_stencil.patch
Patch94:	0095-tu-Zero-init-tu_render_pass-and-tu_subpass-for-dynam.patch
Patch95:	0096-ci-etnaviv-update-ci-expectation.patch
Patch96:	0097-ci-etnaviv-allow-failure-on-failing-test.patch
Patch97:	0098-zink-use-warn_missing_feature-for-missing-modifier-s.patch
Patch98:	0099-ci-traces-upload-only-missing-trace-images.patch
Patch99:	0100-ci-traces-keep-images-for-every-job-except-the-perfo.patch
Patch100:	0101-ci-traces-rename-upload-function-to-reflect-it-works.patch
Patch101:	0102-docs-vulkan-fixup-some-typos.patch
Patch102:	0103-nir-Add-ACCESS_CAN_SPECULATE.patch
Patch103:	0104-ir3-Set-CAN_SPECULATE-before-opt_preamble.patch
Patch104:	0105-ir3-Model-cost-of-phi-nodes-for-opt_preamble.patch
Patch105:	0106-nir-opt_preamble-Walk-cf_list-manually.patch
Patch106:	0107-nir-opt_preamble-Preserve-IR-when-replacing-phis.patch
Patch107:	0108-nir-opt_preamble-Unify-foreach_use-logic.patch
Patch108:	0109-nir-opt_preamble-Move-phis-for-movable-if-s.patch
Patch109:	0110-nir-opt_preamble-Respect-ACCESS_CAN_SPECULATE.patch
Patch110:	0111-freedreno-ci-Minetest.patch
Patch111:	0112-radv-fix-destroying-GDS-OA-BOs.patch
Patch112:	0113-radv-allocate-only-1-GDS-OA-counter-for-gfx10-NGG-st.patch
Patch113:	0114-ac-nir-only-consider-overflow-for-valid-feedback-buf.patch
Patch114:	0115-zink-fix-wording-of-warning.patch
Patch115:	0116-dri-Remove-__driDriverExtensions-leftovers.patch
Patch116:	0117-zink-ci-remove-42-tests-from-the-zink-radv-polaris10.patch
Patch117:	0118-pvr-fix-attachments-segfault-in-pvr_is_stencil_store.patch
Patch118:	0119-pvr-fix-allocation-size-of-clear-colour-consts-share.patch
Patch119:	0120-pvr-change-a-few-places-to-use-PVR_DW_TO_BYTES.patch
Patch120:	0121-pvr-fix-setup-of-load-op-unresolved-msaa-mask.patch
Patch121:	0122-pvr-emit-PPP-state-when-vis_test-dirty-bit-is-set.patch
Patch122:	0123-rusticl-memory-fix-potential-use-after-free-in-clEnq.patch
Patch123:	0124-lavapipe-docs-update-ycbcr-extension-enables.patch
Patch124:	0125-zink-apply-ZINK_DEBUG-quiet-to-all-missing-feature-w.patch
Patch125:	0126-zink-set-ZINK_DEBUG-quiet-for-polaris-jobs.patch
Patch126:	0127-lavapipe-don-t-block-begin-end-cmdbuf-pipeline-barri.patch
Patch127:	0128-radeonsi-disable-disk-cache-when-use-aco.patch
Patch128:	0129-nir-load_libclc-fix-libclc-memory-leak.patch
Patch129:	0130-ci-b2c-move-to-the-shiny-new-gfx-ci-ci-tron-repo.patch
Patch130:	0131-ci-b2c-use-latest-mesa-trigger-image.patch
Patch131:	0132-nvk-Advertise-more-inline-uniform-block-limits.patch
Patch132:	0133-nvk-Emit-MME_DMA_SYSMEMBAR-before-indirect-draw-disp.patch
Patch133:	0134-nvk-Set-max-descriptors-to-2-20-for-most-descriptor-.patch
Patch134:	0135-nvk-Reset-descriptor-pool-allocator-when-all-sets-ar.patch
Patch135:	0136-nil-format-Use-A-for-alpha-blend.patch
Patch136:	0137-nil-format-Advertise-R10G10B10A2_UINT-texture-buffer.patch
Patch137:	0138-nvk-Disable-depth-or-stencil-tests-when-unbound.patch
Patch138:	0139-nvk-Always-emit-at-least-one-color-attachment.patch
Patch139:	0140-nvk-Improve-address-space-and-buffer-size-limits.patch
Patch140:	0141-pvr-Fix-MRT-index-in-PBE-state.patch
Patch141:	0142-pvr-Fix-pbe_emit-assert.patch
Patch142:	0143-pvr-Fix-OOB-access-of-pbe_-cs-reg-_words.patch
Patch143:	0144-pvr-Order-tile-buffer-EOT-emits-to-be-last.patch
Patch144:	0145-pvr-Fix-subpass-sample-count-on-ds-attachment-only.patch
Patch145:	0146-pvr-Refactor-subpass-ds-and-sample-count-setup.patch
Patch146:	0147-pvr-Fix-SPM-load-shader-sample-rate.patch
Patch147:	0148-pvr-Fix-PPP_SCREEN-sizes.patch
Patch148:	0149-tu-Disable-preamble-push-consts-when-they-are-not-us.patch
Patch149:	0150-pvr-Switch-to-common-pipeline-cache-implementation.patch
Patch150:	0151-pvr-Use-vk_sampler-base.patch
Patch151:	0152-pvr-Clean-up-fix-sampler-border-color-support.patch
Patch152:	0153-etnaviv-fix-read-staging-buffer-leak.patch
Patch153:	0154-Revert-ci-etnaviv-allow-failure-on-failing-test.patch
Patch154:	0155-vulkan-bump-headers-registry-to-1.3.267.patch
Patch155:	0156-anv-rename-primary-in-container-in-ExecuteCommands.patch
Patch156:	0157-anv-add-support-for-VK_EXT_nested_command_buffer.patch
Patch157:	0158-intel-genxml-fix-3DSTATE_3D_MODE-length-to-align-wit.patch
Patch158:	0159-anv-ensure-that-FCV_CCS_E-fast-clears-are-properly-t.patch
Patch159:	0160-anv-enable-FCV-for-Gen12.5.patch
Patch160:	0161-aco-fix-LdsDirectVMEMHazard-WaW-with-the-wrong-waitc.patch
Patch161:	0162-aco-only-mitigate-VcmpxExecWARHazard-when-necessary.patch
Patch162:	0163-aco-fix-s_setreg-hazards.patch
Patch163:	0164-aco-consider-exec_hi-in-reads_exec.patch
Patch164:	0165-aco-resolve-all-possible-hazards-at-the-end-of-shade.patch
Patch165:	0166-aco-tests-test-that-hazards-are-resolved-at-the-end-.patch
Patch166:	0167-radv-ci-update-list-of-expected-failures-on-RAVEN.patch
Patch167:	0168-radv-ci-update-list-of-flakes-for-VANGOGH.patch
Patch168:	0169-radv-ci-update-list-of-flakes-for-STONEY.patch
Patch169:	0170-spirv-Don-t-use-libclc-for-rotate.patch
Patch170:	0171-ir3-Fix-values-of-wrmask-not-being-compatible-with-i.patch
Patch171:	0172-frontends-va-Add-High-Quality-preset-mode.patch
Patch172:	0173-radeonsi-vcn-Add-High-Quality-encoding-preset-for-AV.patch
Patch173:	0174-ac-surface-add-astc-block-size-to-bpe_to_format-func.patch
Patch174:	0175-mesa-make-astc_decoder.glsl-vk-compatible.patch
Patch175:	0176-util-move-ASTCLutHolder-from-mesa-main-to-util.patch
Patch176:	0177-vulkan-formats-zink-move-vk_format_from_pipe_format-.patch
Patch177:	0178-vulkan-runtime-add-compute-astc-decoder-helper-funct.patch
Patch178:	0179-vulkan-add-3D-texture-support-for-compute-astc-decod.patch
Patch179:	0180-radv-integrate-meta-astc-compute-decoder-to-radv.patch
Patch180:	0181-tu-Count-a-whole-push-consts-range-in-constlen-for-P.patch
Patch181:	0182-anv-simplify-push-descriptors.patch
Patch182:	0183-ci-traces-always-export-piglit-EXTRA_ARGS.patch
Patch183:	0184-ci-ci_run_n_monitor-print-stress-test-results-per-jo.patch
Patch184:	0185-ci-ci_run_n_monitor-simplify-with-defaultdict.patch
Patch185:	0186-ci-ci_run_n_monitor-merge-print_job_status_change-wi.patch
Patch186:	0187-ci-ci_run_n_monitor-make-target-mandatory.patch
Patch187:	0188-ci-ci_run_n_monitor-merge-enable_job-with-retry_job.patch
Patch188:	0189-ci-ci_run_n_monitor-simplify-enable-cancel-logic-in-.patch
Patch189:	0190-ci-ci_run_n_monitor-allow-user-project-in-project.patch
Patch190:	0191-ci-ci_run_n_monitor-limit-repetitions-on-stress.patch
Patch191:	0192-venus-enable-Vulkan-1.3-for-Android-13-and-above.patch
Patch192:	0193-mesa-st-ignore-StencilSampling-if-stencil-not-part-o.patch
Patch193:	0194-radv-disable-primitive-restart-for-non-indexed-draws.patch
Patch194:	0195-vulkan-Add-vk_subpass_dependency_is_fb_local-helper.patch
Patch195:	0196-tu-Use-common-vk_subpass_dependency_is_fb_local.patch
Patch196:	0197-pvr-Don-t-merge-subpasses-on-framebuffer-global-depe.patch
Patch197:	0198-radv-enable-radv_disable_aniso_single_level-true-for.patch
Patch198:	0199-amd-llvm-aco-radv-implement-NGG-streamout-with-GDS_S.patch
Patch199:	0200-radv-mark-GDS-as-needed-for-XFB-queries-with-NGG-str.patch
Patch200:	0201-radv-skip-GDS-allocation-for-NGG-streamout-on-GFX11.patch
Patch201:	0202-anv-Enable-transfer-queue-only-on-ACM-platforms.patch
Patch202:	0203-ci-add-a630-trace-flakes.patch
Patch203:	0204-anv-fixup-spirv-cap-for-ImageReadWithoutFormat-on-Gf.patch
Patch204:	0205-ci-Uprev-virglrenderer.patch
Patch205:	0206-r600-sfn-Handle-load_global_constant.patch
Patch206:	0207-nir-opt_phi_precision-Work-with-libraries.patch
Patch207:	0208-nir-legalize_16bit_sampler_srcs-Use-instr_pass.patch
Patch208:	0209-nir-print-Handle-KERNEL.patch
Patch209:	0210-nir-lower_io-Use-load_global_constant-for-OpenCL.patch
Patch210:	0211-nir-opt_algebraic-Reduce-int64.patch
Patch211:	0212-zink-shrink-vectors-during-optimization.patch
Patch212:	0213-nir-print-Decode-system-values-in-the-variable-decla.patch
Patch213:	0214-ci-zink-Add-a-TGL-flake-that-s-showed-up-in-nightlie.patch
Patch214:	0215-ci-radeonsi-Drop-an-xfail-for-vangogh.patch
Patch215:	0216-anv-batch-Check-if-batch-already-has-an-error-in-anv.patch
Patch216:	0217-anv-batch-Assert-that-extend_cb-is-non-NULL-if-the-b.patch
Patch217:	0218-intel-dev-Add-0x56ba-0x56bd-DG2-PCI-IDs.patch
Patch218:	0219-nir-opt_algebraic-Optimize-LLVM-booleans.patch
Patch219:	0220-intel-Prepare-implementation-of-Wa_18019816803-and-W.patch
Patch220:	0221-Revert-intel-fs-limit-register-flag-interaction-of-F.patch
Patch221:	0222-include-dri_interface.h-restore-define-mistakenly-re.patch
Patch222:	0223-freedreno-rddecompiler-Use-fd_dev_gen-to-pass-gpu_id.patch
Patch223:	0224-freedreno-rddecompiler-Decompile-repeated-IBs.patch
Patch224:	0225-rusticl-kernel-Fix-creation-from-programs-not-built-.patch
Patch225:	0226-isaspec-fix-isaspec-build-error-in-aosp.patch
Patch226:	0227-Revert-ci-lima-farm-is-down-disable-for-now.patch
Patch227:	0228-pvr-Don-t-pass-pvr_physical_device-when-only-device-.patch
Patch228:	0229-pvr-Minor-refactor-of-pvr_device.c.patch
Patch229:	0230-pvr-Use-common-physical-device-properties.patch
Patch230:	0231-ci-etnaviv-move-failure-to-flake.patch
Patch231:	0232-radv-ci-tighten-the-vkcts-navi21-timeouts.patch
Patch232:	0233-zink-ci-tighten-the-zink-radv-vangogh-timeouts.patch
Patch233:	0234-r600-sfn-don-t-remove-texture-sources-by-using-the-e.patch
Patch234:	0235-r600-drop-egcm_load_index_reg.patch
Patch235:	0236-meson-add-wayland-protocols-from-meson-wrapdb.patch
Patch236:	0237-zink-ci-remove-expected-failures-that-are-skipped-fo.patch
Patch237:	0238-ci_run_n_monitor-dependency-jobs-must-always-be-star.patch
Patch238:	0239-docs-update-etnaviv-extensions.patch
Patch239:	0240-rusticl-memory-fix-potential-use-after-free-in-clEnq.patch
Patch240:	0241-blorp-Use-the-correct-miptail-start-LOD-for-surfaces.patch
Patch241:	0242-broadcom-cle-clif-common-simulator-add-7.1-version-o.patch
Patch242:	0243-broadcom-simulator-reset-CFG7-for-compute-dispatch-i.patch
Patch243:	0244-broadcom-cle-update-the-packet-definitions-for-new-g.patch
Patch244:	0245-broadcom-common-retrieve-V3D-revision-number.patch
Patch245:	0246-broadcom-common-add-some-common-v71-helpers.patch
Patch246:	0247-broadcom-qpu-add-comments-on-waddr-not-used-on-V3D-7.patch
Patch247:	0248-broadcom-qpu-set-V3D-7.x-names-for-some-waddr-aliasi.patch
Patch248:	0249-broadcom-compiler-rename-small_imm-to-small_imm_b.patch
Patch249:	0250-broadcom-compiler-add-small_imm-a-c-d-on-v3d_qpu_sig.patch
Patch250:	0251-broadcom-qpu-add-v71-signal-map.patch
Patch251:	0252-broadcom-qpu-define-v3d_qpu_input-use-on-v3d_qpu_alu.patch
Patch252:	0253-broadcom-qpu-add-raddr-on-v3d_qpu_input.patch
Patch253:	0254-broadcom-qpu-defining-shift-mask-for-raddr_c-d.patch
Patch254:	0255-broadcom-commmon-add-has_accumulators-field-on-v3d_d.patch
Patch255:	0256-broadcom-qpu-add-qpu_writes_rf0_implicitly-helper.patch
Patch256:	0257-broadcom-qpu-add-pack-unpack-support-for-v71.patch
Patch257:	0258-broadcom-compiler-update-node-temp-translation-for-v.patch
Patch258:	0259-broadcom-compiler-phys-index-depends-on-hw-version.patch
Patch259:	0260-broadcom-compiler-don-t-favor-select-accum-registers.patch
Patch260:	0261-broadcom-vir-implement-is_no_op_mov-for-v71.patch
Patch261:	0262-broadcom-compiler-update-vir_to_qpu-set_src-for-v71.patch
Patch262:	0263-broadcom-qpu_schedule-add-process_raddr_deps.patch
Patch263:	0264-broadcom-qpu-update-disasm_raddr-for-v71.patch
Patch264:	0265-broadcom-qpu-return-false-on-qpu_writes_accumulatorX.patch
Patch265:	0266-broadcom-compiler-add-support-for-varyings-on-nir-to.patch
Patch266:	0267-broadcom-compiler-payload_w-is-loaded-on-rf3-for-v71.patch
Patch267:	0268-broadcom-qpu_schedule-update-write-deps-for-v71.patch
Patch268:	0269-broadcom-compiler-update-register-classes-to-not-inc.patch
Patch269:	0270-broadcom-compiler-implement-reads-writes-too-soon-ch.patch
Patch270:	0271-broadcom-compiler-implement-read-stall-check-for-v71.patch
Patch271:	0272-broadcom-compiler-add-a-v3d71_qpu_writes_waddr_expli.patch
Patch272:	0273-broadcom-compiler-prevent-rf2-3-usage-in-thread-end-.patch
Patch273:	0274-broadcom-qpu-add-new-ADD-opcodes-for-FMOV-MOV-in-v71.patch
Patch274:	0275-broadcom-qpu-fix-packing-unpacking-of-fmov-variants-.patch
Patch275:	0276-broadcom-qpu-implement-switch-rules-for-fmin-fmax-fa.patch
Patch276:	0277-broadcom-compiler-make-vir_write_rX-return-false-on-.patch
Patch277:	0278-broadcom-compiler-rename-vir_writes_rX-to-vir_writes.patch
Patch278:	0279-broadcom-compiler-only-handle-accumulator-classes-if.patch
Patch279:	0280-broadcom-compiler-don-t-assign-rf0-to-temps-across-i.patch
Patch280:	0281-broadcom-compiler-CS-payload-registers-have-changed-.patch
Patch281:	0282-broadcom-compiler-don-t-schedule-rf0-writes-right-af.patch
Patch282:	0283-broadcom-compiler-allow-instruction-merges-in-v71.patch
Patch283:	0284-broadcom-qpu-add-MOV-integer-packing-unpacking-varia.patch
Patch284:	0285-broadcom-qpu-fail-packing-on-unhandled-mul-pack-unpa.patch
Patch285:	0286-broadcom-compiler-generalize-check-for-shaders-using.patch
Patch286:	0287-broadcom-compiler-v71-isn-t-affected-by-double-round.patch
Patch287:	0288-broadcom-compiler-update-one-TMUWT-restriction-for-v.patch
Patch288:	0289-broadcom-compiler-update-ldunif-ldvary-comment-for-v.patch
Patch289:	0290-broadcom-compiler-update-payload-registers-handling-.patch
Patch290:	0291-broadcom-compiler-update-peripheral-access-restricti.patch
Patch291:	0292-broadcom-qpu-add-packing-for-fmov-on-ADD-alu.patch
Patch292:	0293-broadcom-compiler-handle-rf0-flops-storage-restricti.patch
Patch293:	0294-broadcom-compiler-enable-ldvary-pipelining-on-v71.patch
Patch294:	0295-broadcom-compiler-try-to-use-ldunif-a-instead-of-ldu.patch
Patch295:	0296-broadcom-compiler-don-t-assign-rf0-to-temps-that-con.patch
Patch296:	0297-broadcom-compiler-convert-mul-to-add-when-needed-to-.patch
Patch297:	0298-broadcom-compiler-implement-small-immediates-for-v71.patch
Patch298:	0299-broadcom-compiler-update-thread-end-restrictions-for.patch
Patch299:	0300-broadcom-compiler-update-ldvary-thread-switch-delay-.patch
Patch300:	0301-broadcom-compiler-lift-restriction-for-branch-msfign.patch
Patch301:	0302-broadcom-compiler-start-allocating-from-RF-4-in-V7.x.patch
Patch302:	0303-broadcom-compiler-validate-restrictions-after-TLB-Z-.patch
Patch303:	0304-broadcom-compiler-lift-restriction-on-vpmwt-in-last-.patch
Patch304:	0305-broadcom-compiler-fix-up-copy-propagation-for-v71.patch
Patch305:	0306-broadcom-qpu-new-packing-conversion-v71-instructions.patch
Patch306:	0307-broadcom-compiler-don-t-allocate-spill-base-to-rf0-i.patch
Patch307:	0308-broadcom-compiler-improve-allocation-for-final-progr.patch
Patch308:	0309-broadcom-compiler-don-t-assign-registers-to-unused-n.patch
Patch309:	0310-broadcom-compiler-only-assign-rf0-as-last-resort-in-.patch
Patch310:	0311-v3dv-meson-add-v71-hw-generation.patch
Patch311:	0312-v3dv-expose-V3D-revision-number-in-device-name.patch
Patch312:	0313-v3dv-device-handle-new-rpi5-device-bcm2712.patch
Patch313:	0314-v3dv-emit-TILE_BINNING_MODE_CFG-and-TILE_RENDERING_M.patch
Patch314:	0315-v3dv-cmd_buffer-emit-TILE_RENDERING_MODE_CFG_RENDER_.patch
Patch315:	0316-v3dvx-cmd_buffer-emit-CLEAR_RENDER_TARGETS-for-v71.patch
Patch316:	0317-v3dv-cmd_buffer-emit-CLIPPER_XY_SCALING-for-v71.patch
Patch317:	0318-v3dv-uniforms-update-VIEWPORT_X-Y_SCALE-uniforms-for.patch
Patch318:	0319-v3dv-cmd_buffer-just-don-t-fill-up-early-z-fields-fo.patch
Patch319:	0320-v3dv-default-vertex-attribute-values-are-gen-dependa.patch
Patch320:	0321-v3dv-pipeline-default-vertex-attributes-values-are-n.patch
Patch321:	0322-v3dv-pipeline-handle-GL_SHADER_STATE_RECORD-changed-.patch
Patch322:	0323-v3dv-setup-render-pass-color-clears-for-any-format-b.patch
Patch323:	0324-v3dv-setup-TLB-clear-color-for-meta-operations-in-v7.patch
Patch324:	0325-v3dv-fix-up-texture-shader-state-for-v71.patch
Patch325:	0326-v3dv-handle-new-texture-state-transfer-functions-in-.patch
Patch326:	0327-v3dv-implement-noop-job-for-v71.patch
Patch327:	0328-v3dv-handle-render-pass-global-clear-for-v71.patch
Patch328:	0329-v3dv-GFX-1461-does-not-affect-V3D-7.x.patch
Patch329:	0330-broadcom-compiler-update-thread-end-restrictions-val.patch
Patch330:	0331-v3dv-handle-early-Z-S-clears-for-v71.patch
Patch331:	0332-v3dv-handle-RTs-with-no-color-targets-in-v71.patch
Patch332:	0333-v3dv-no-specific-separate_segments-flag-for-V3D-7.1.patch
Patch333:	0334-v3dv-don-t-convert-floating-point-border-colors-in-v.patch
Patch334:	0335-v3dv-handle-Z-clipping-in-v71.patch
Patch335:	0336-v3dv-add-support-for-TFU-jobs-in-v71.patch
Patch336:	0337-v3dv-make-v3dv_viewport_compute_xform-depend-on-the-.patch
Patch337:	0338-v3dv-fix-depth-clipping-then-Z-scale-is-too-small-in.patch
Patch338:	0339-v3d-add-v71-hw-generation.patch
Patch339:	0340-v3d-emit-TILE_BINNING_MODE_CFG-and-TILE_RENDERING_MO.patch
Patch340:	0341-v3d-TILE_RENDERING_MODE_CFG_RENDER_TARGET_PART1.patch
Patch341:	0342-v3d-emit-CLEAR_RENDER_TARGETS-for-v71.patch
Patch342:	0343-v3d-just-don-t-fill-up-early-z-fields-for-CFG_BITS-f.patch
Patch343:	0344-v3d-emit-CLIPPER_XY_SCALING-for-v71.patch
Patch344:	0345-v3d-no-specific-separate_segments-flag-for-V3D-7.1.patch
Patch345:	0346-v3d-default-vertex-attributes-values-are-not-needed-.patch
Patch346:	0347-v3d-uniforms-update-VIEWPORT_X-Y_SCALE-uniforms-for-.patch
Patch347:	0348-v3d-handle-new-texture-state-transfer-functions-in-v.patch
Patch348:	0349-v3d-handle-new-TEXTURE_SHADER_STATE-v71-YCbCr-fields.patch
Patch349:	0350-v3d-setup-render-pass-color-clears-for-any-format-bp.patch
Patch350:	0351-v3d-GFX-1461-does-not-affect-V3D-7.x.patch
Patch351:	0352-v3d-don-t-convert-floating-point-border-colors-in-v7.patch
Patch352:	0353-v3d-handle-Z-clipping-in-v71.patch
Patch353:	0354-v3d-add-support-for-TFU-blit-in-v71.patch
Patch354:	0355-v3d-v3dv-fix-texture-state-array-stride-packing-for-.patch
Patch355:	0356-v3d-v3dv-support-up-to-8-render-targets-in-v7.1.patch
Patch356:	0357-v3d-v3dv-don-t-use-max-internal-bpp-for-tile-sizing-.patch
Patch357:	0358-v3dv-implement-depthBounds-support-for-v71.patch
Patch358:	0359-v3d-v3dv-propagate-NaNs-bits-in-shader-state-records.patch
Patch359:	0360-v3dv-use-new-texture-shader-state-rb_swap-and-revers.patch
Patch360:	0361-v3dv-fix-color-write-mask-for-v3d-7.x.patch
Patch361:	0362-v3d-v3dv-fix-depth-bias-for-v3d-7.x.patch
Patch362:	0363-v3d-v3dv-fix-compute-for-V3D-7.1.6.patch
Patch363:	0364-broadcom-add-performance-counters-for-V3D-7.x.patch
Patch364:	0365-broadcom-simulator-add-per-hw-version-calls.patch
Patch365:	0366-v3dv-expose-fullDrawIndexUint32-in-V3D-7.x.patch
Patch366:	0367-v3dv-expose-depthClamp-in-V3D-7.x.patch
Patch367:	0368-v3dv-expose-scalarBlockLayout-on-V3D-7.x.patch
Patch368:	0369-doc-features-update-after-last-v3d-changes.patch
Patch369:	0370-ci-add-half-life-2-freedreno-flake.patch
Patch370:	0371-zink-always-clamp-shader-stage-in-descriptor-handlin.patch
Patch371:	0372-zink-implement-get_compute_state_info.patch
Patch372:	0373-zink-copy-has_variable_shared_mem-cs-property.patch
Patch373:	0374-zink-pass-entire-pipe_grid_info-into-zink_program_up.patch
Patch374:	0375-zink-refactor-spec-constant-handling.patch
Patch375:	0376-zink-variable-shared-mem-support.patch
Patch376:	0377-zink-support-more-nir-opcodes.patch
Patch377:	0378-zink-make-spirv_builder_emit_-op-compatible-with-spe.patch
Patch378:	0379-zink-add-set_global_binding.patch
Patch379:	0380-zink-support-samplers-with-unnormalized_coords.patch
Patch380:	0381-zink-implement-remaining-pack-ops-via-bitcast.patch
Patch381:	0382-zink-fix-RA-textures.patch
Patch382:	0383-zink-fix-load-store-scratch-offsets.patch
Patch383:	0384-zink-eliminate-samplers-from-no-sampler-CL-texops.patch
Patch384:	0385-rusticl-mesa-screen-device-add-driver_name.patch
Patch385:	0386-rusticl-enable-zink.patch
Patch386:	0387-pipe-loader-allow-to-load-multiple-zink-devices.patch
Patch387:	0388-anv-update-batch-chaining-to-Gfx9-commands.patch
Patch388:	0389-radv-drirc-rename-radv_require_-etc2-astc.patch
Patch389:	0390-anv-remove-unused-field-from-anv_image_view.patch
Patch390:	0391-anv-add-anv_image_view_-init-finish.patch
Patch391:	0392-anv-support-image-views-with-surface-state-stream.patch
Patch392:	0393-anv-add-anv_push_descriptor_set_-init-finish.patch
Patch393:	0394-anv-support-alternative-push-descriptor-sets.patch
Patch394:	0395-anv-add-anv_descriptor_set_write.patch
Patch395:	0396-anv-add-anv_cmd_buffer_-save-restore-_state.patch
Patch396:	0397-anv-add-anv_is_format_emulated.patch
Patch397:	0398-anv-add-a-hidden-plane-for-emulated-formats.patch
Patch398:	0399-anv-decompress-on-upload-for-emulated-formats.patch
Patch399:	0400-anv-fix-up-image-views-for-emulated-formats.patch
Patch400:	0401-anv-fix-up-blit-src-for-emulated-formats.patch
Patch401:	0402-anv-advertise-emulated-formats.patch
Patch402:	0403-anv-add-support-for-vk_require_astc-driconf.patch
Patch403:	0404-nvk-Always-set-pixel_min-max_Z-to-CLAMP.patch
Patch404:	0405-rusticl-bump-rustc-version-to-1.66.patch
Patch405:	0406-rusticl-mesa-nir-mark-more-methods-as-mut.patch
Patch406:	0407-rusticl-mesa-nir-Mark-NirShader-and-NirPrintfInfo-as.patch
Patch407:	0408-rusticl-mesa-mark-PipeResource-as-Send-and-Sync.patch
Patch408:	0409-rusticl-mesa-mark-PipeTransfer-as-Send.patch
Patch409:	0410-rusticl-cl-mark-_cl_image_desc-as-Send-and-Sync.patch
Patch410:	0411-rusticl-queue-get-rid-of-pointless-Option-around-our.patch
Patch411:	0412-rusticl-queue-make-it-Sync.patch
Patch412:	0413-rusticl-kernel-get-rid-of-Arcs-in-KernelDevStateVari.patch
Patch413:	0414-ci-ci_marge_queue.py.patch
Patch414:	0415-rusticl-memory-use-get_mut-instead-of-lock-in-drop.patch
Patch415:	0416-fix-clover-warning-ignoring-return-value-of-int-posi.patch
Patch416:	0417-mesa-Introduce-MESA_texture_const_bandwidth.patch
Patch417:	0418-mesa-Implement-MESA_texture_const_bandwidth.patch
Patch418:	0419-freedreno-Add-PIPE_CAP_HAS_CONST_BW-support.patch
Patch419:	0420-panfrost-Add-PIPE_CAP_HAS_CONST_BW-support.patch
Patch420:	0421-iris-Add-PIPE_CAP_HAS_CONST_BW-support.patch
Patch421:	0422-radeonsi-Add-PIPE_CAP_HAS_CONST_BW-support.patch
Patch422:	0423-zink-implement-PIPE_COMPUTE_CAP_MAX_COMPUTE_UNITS.patch
Patch423:	0424-zink-sync-queue-access-for-vkQueueWaitIdle.patch
Patch424:	0425-rusticl-Rename-XyzCB-aliases-to-FuncXyzCB.patch
Patch425:	0426-rusticl-add-structs-to-hold-the-C-callbacks.patch
Patch426:	0427-rusticl-use-CreateContextCB.patch
Patch427:	0428-rusticl-use-DeleteContextCB.patch
Patch428:	0429-rusticl-use-EventCB.patch
Patch429:	0430-rusticl-use-MemCB.patch
Patch430:	0431-rusticl-use-ProgramCB.patch
Patch431:	0432-rusticl-use-SVMFreeCb.patch
Patch432:	0433-rusticl-Make-EventSig-take-ownership-of-its-environm.patch
Patch433:	0434-rusticl-add-a-safe-abstraction-to-execute-a-DeleteCo.patch
Patch434:	0435-rusticl-add-a-safe-abstraction-to-execute-an-EventCB.patch
Patch435:	0436-rusticl-add-a-safe-abstraction-to-execute-a-MemCB.patch
Patch436:	0437-rusticl-add-a-safe-abstraction-to-execute-an-SVMFree.patch
Patch437:	0438-rusticl-add-a-safe-abstraction-to-execute-a-CreateCo.patch
Patch438:	0439-rusticl-add-a-safe-abstraction-to-execute-a-ProgramC.patch
Patch439:	0440-rusticl-api-drop-a-few-include-paths.patch
Patch440:	0441-rusticl-api-remove-cl_closure-macro.patch
Patch441:	0442-rusticl-mark-the-fields-of-callback-structs-private.patch
Patch442:	0443-rusticl-drop-an-allow-dead_code-marker.patch
Patch443:	0444-rusticl-core-don-t-take-a-lock-while-dropping-Contex.patch
Patch444:	0445-mesa-enable-NV_texture_barrier-in-GLES2-again.patch
Patch445:	0446-zink-implement-load_global_constant.patch
Patch446:	0447-zink-properly-emit-PhysicalStorageBufferAddresses-ca.patch
Patch447:	0448-freedreno-Fix-field-size-of-A6XX_TEX_CONST-3-.ARRAY_.patch
Patch448:	0449-nir-lower_mem_access_bit_sizes-fix-invalid-shift-bit.patch
Patch449:	0450-rusticl-device-restrict-1Dbuffer-images-for-RGB-and-.patch
Patch450:	0451-rusticl-memory-use-PIPE_BUFFER-for-IMAGE1D_BUFFER-im.patch
Patch451:	0452-rusticl-format-disable-all-sRGB-formats.patch
Patch452:	0453-util-xmlconfig-add-an-env-var-for-overriding-drirc-s.patch
Patch453:	0454-meson-add-src-util-to-the-drirc-search-path.patch
Patch454:	0455-util-xmlconfig-drop-driInjectDataDir-now-that-DRIRC_.patch
Patch455:	0456-util-xmlconfig-inline-datadir.patch
Patch456:	0457-docs-relnotes-remove-cruft-from-end-of-lines.patch
Patch457:	0458-docs-ci-escape-at-symbols.patch
Patch458:	0459-docs-relnotes-escape-some-at-symbols.patch
Patch459:	0460-bin-gen_release_notes-escape-at-symbols.patch
Patch460:	0461-vulkan-wsi-wayland-Fix-detection-of-tearing-control-.patch
Patch461:	0462-nvk-Use-nouveau_ws_bo_unmap-instead-of-munmap.patch
Patch462:	0463-nvk-Free-the-disk-cache.patch
Patch463:	0464-nvk-Add-an-nvk_shader_finish-helper.patch
Patch464:	0465-nvk-Handle-unbinding-images-and-buffers.patch
Patch465:	0466-nvk-Clean-up-the-disk-cache-on-physical-device-creat.patch
Patch466:	0467-vulkan-wsi-Allow-for-larger-linear-images.patch
Patch467:	0468-r600-sfn-Don-t-override-a-chgr-pinning-during-copy-p.patch
Patch468:	0469-r600-sfn-When-simplifying-src-vec4-pinnings-also-che.patch
Patch469:	0470-frontends-va-config-report-max-width-and-height-for-.patch
Patch470:	0471-ac-gpu_info-split-ib_alignment-as-ip-type-.ib_alignm.patch
Patch471:	0472-ac-gpu_info-move-ib_pad_dw_mask-into-ip.patch
Patch472:	0473-ac-gpu_info-drop-the-hack-unifying-all-IB-alignments.patch
Patch473:	0474-ac-gpu_info-conservatively-decrease-IB-alignment-and.patch
Patch474:	0475-ac-gpu_info-set-gfx-and-compute-IB-padding-to-only-8.patch
Patch475:	0476-winsys-amdgpu-properly-pad-the-IB-in-amdgpu_submit_g.patch
Patch476:	0477-winsys-amdgpu-correctly-pad-noop-IBs-for-RADEON_NOOP.patch
Patch477:	0478-winsys-amdgpu-pad-gfx-and-compute-IBs-with-only-1-NO.patch
Patch478:	0479-anv-workaround-Gfx11-with-optimized-state-emission.patch
Patch479:	0480-radv-rt-Reject-hits-within-10ULP-of-previous-hits-in.patch
Patch480:	0481-anv-advertise-VK_KHR_global_priority_queue.patch
Patch481:	0482-docs-Mention-meson-devenv-in-the-pre-install-test-in.patch
Patch482:	0483-ac-gpu_info-don-t-allow-register-shadowing-with-SR-I.patch
Patch483:	0484-radeonsi-disable-register-shadowing-without-SR-IOV-t.patch
Patch484:	0485-winsys-amdgpu-don-t-send-CP_GFX_SHADOW-chunk-if-shad.patch
# doesn't apply, irrelevant outside of CI
#Patch485:	0486-radeonsi-ci-update-gfx1100-results.patch
Patch486:	0487-intel-clc-avoid-using-spirv-linker.patch
Patch487:	0488-virgl-Fix-logic-for-reporting-PIPE_MIRROR_CLAMP.patch
Patch488:	0489-anv-don-t-flush_llc-on-gen9.patch
Patch489:	0490-u_trace-generate-tracepoint-index-parameter-in-perfe.patch
Patch490:	0491-u_trace-generate-tracepoint-name-array-in-perfetto-h.patch
Patch491:	0492-intel-ds-provide-names-for-different-events-of-a-tim.patch
Patch492:	0493-broadcom-qpu-Remove-duplicate-variable-opcode.patch
Patch493:	0494-etnaviv-use-correct-blit-box-sizes-when-copying-reso.patch
Patch494:	0495-etnaviv-zero-shared-TS-metadata-block.patch
Patch495:	0496-anv-fix-debug-string-for-PC-flush.patch
Patch496:	0497-nir-split-FLOAT_CONTROLS_SIGNED_ZERO_INF_NAN_PRESERV.patch
Patch497:	0498-nir-algebraic-use-only-signed_zero_preserve_-for-add.patch
Patch498:	0499-anv-set-ComputeMode.PixelAsyncComputeThreadLimit-4.patch
Patch499:	0500-nvk-Add-a-nvk_cmd_buffer_dirty_render_pass-helper.patch
Patch500:	0501-nvk-Re-sort-device-features.patch
Patch501:	0502-nvk-Implement-VK_EXT_depth_bias_control.patch
Patch502:	0503-venus-properly-expose-KHR_external_fence-sempahore_f.patch
Patch503:	0504-loader-rename-loader_open_render_node-to-loader_open.patch
Patch504:	0505-loader-add-driver-list-as-parameter-in-loader_open_r.patch
Patch505:	0506-pipe-loader-add-pipe_loader_get_compatible_render_ca.patch
Patch506:	0507-dri-add-queryCompatibleRenderOnlyDeviceFd-to-__DRI_M.patch
### Patches verified to be ok until here
# FIXME should be ported, clashes with Panthor addition
#Patch507:	0508-kmsro-try-to-use-only-compatible-render-capable-devi.patch
# FIXME with these, Rock 5B uses llvmpipe rather than panthor
Patch508:	0509-loader-add-loader_is_device_render_capable.patch
#Patch509:	0510-egl-drm-get-compatible-render-only-device-fd-for-kms.patch
#Patch510:	0511-egl-error-out-if-we-can-t-find-an-EGLDevice-in-_eglF.patch
Patch511:	0512-iris-Support-parameter-queries-for-main-planes.patch
Patch512:	0513-zink-add-some-checks-to-determine-whether-queue-is-i.patch
Patch513:	0514-zink-don-t-destroy-any-simple_mtx_t-objects-during-s.patch
Patch514:	0515-zink-don-t-destroy-uninitialized-disk-cache-thread.patch
Patch515:	0516-zink-reorder-glsl_type_singleton_init_or_ref-call.patch
Patch516:	0517-zink-use-screen-destructor-for-creation-fails.patch
Patch517:	0518-zink-fix-readback_present-locking.patch
Patch518:	0519-zink-add-automatic-swapchain-readback-using-heuristi.patch
Patch519:	0520-lavapipe-VK_EXT_nested_command_buffer.patch
Patch520:	0521-i915-Make-I915_DEBUG-fs-log-shaders-that-fail-to-lin.patch
Patch521:	0522-nir-Flatten-ifs-with-discards-in-nir_opt_peephole_se.patch
Patch522:	0523-glsl-Remove-lower_discard.patch
Patch523:	0524-mesa-don-t-pass-Infs-to-the-shader-via-gl_Fog.scale.patch
Patch524:	0525-util-improve-BITFIELD_MASK-and-BITFIELD64_MASK-on-cl.patch
Patch525:	0526-llvmpipe-Compile-a-nop-texture-function-for-unsuppor.patch
Patch526:	0527-nvk-Enable-VK_EXT_load_store_op_none.patch
Patch527:	0528-radv-rt-Use-nir_shader_instructions_pass-for-lower_r.patch
Patch528:	0529-radeonsi-Fix-plane-size-in-si_copy_multi_plane_textu.patch
Patch529:	0530-nvk-Advertise-VK_KHR_workgroup_memory_explicit_layou.patch
Patch530:	0531-anv-reuse-local-variable-for-gfx-state.patch
Patch531:	0532-anv-track-render-targets-render-area-changes-separat.patch
Patch532:	0533-nvk-Implement-VK_EXT_image_sliced_view_of_3d.patch
Patch533:	0534-nvk-Advertise-VK_EXT_primitive_topology_list_restart.patch
Patch534:	0535-ci-update-CTS-to-vulkan-cts-1.3.7.0.patch
Patch535:	0536-ci-bump-the-number-of-tests-per-group-from-500-to-50.patch
Patch536:	0537-ci-bump-DEQP_FRACTION-for-some-jobs.patch
Patch537:	0538-zink-ignore-unacquired-swapchain-images-during-end-o.patch
Patch538:	0539-radeonsi-ci-update-the-runner-for-new-build-scripts.patch
Patch539:	0540-radeonsi-ci-enable-GTF-tests-in-the-runner.patch
Patch540:	0541-radeonsi-ci-enable-GLES-CTS-in-the-runner.patch
# Doesn't apply (and is irrelevant outside of CI)
#Patch541:	0542-radeonsi-ci-update-failures-and-flakes.patch
Patch542:	0543-pvr-Enable-VK_EXT_scalar_block_layout.patch
Patch543:	0544-pvr-Enable-KHR_image_format_list.patch
Patch544:	0545-pvr-Enable-VK_KHR_uniform_buffer_standard_layout.patch
Patch545:	0546-frontends-va-Implement-vaMapBuffer2.patch
Patch546:	0547-ac-gpu_info-Add-some-SDMA-related-information.patch
Patch547:	0548-ac-Clarify-SDMA-opcode-defines.patch
Patch548:	0549-ac-Add-amd_ip_type-argument-to-ac_parse_ib-and-ac_pa.patch
Patch549:	0550-ac-Rename-ac_do_parse_ib-to-parse_pkt3_ib.patch
Patch550:	0551-ac-Print-IP-type-for-IBs.patch
Patch551:	0552-ac-Add-rudimentary-implementation-of-printing-SDMA-I.patch
Patch552:	0553-asahi-flush-denorms-on-exact-fmin-fmax.patch
Patch553:	0554-venus-Sync-protocol-for-VK_EXT_graphics_pipeline_lib.patch
Patch554:	0555-venus-Erase-pViewports-and-pScissors-in-fewer-cases.patch
Patch555:	0556-venus-Fix-crash-when-VkGraphicsPipelineCreateInfo-la.patch
Patch556:	0557-venus-Fix-subpass-attachments.patch
Patch557:	0558-venus-Drop-incorrectly-used-always-true-pipeline-var.patch
Patch558:	0559-venus-Use-VkImageAspectFlags-in-vn_subpass.patch
Patch559:	0560-venus-Add-enum-vn_pipeline_type.patch
Patch560:	0561-venus-Renames-for-VkGraphicsPipelineCreateInfo-fixes.patch
Patch561:	0562-venus-Refactor-pipeline-fixup-into-two-stages.patch
Patch562:	0563-venus-Do-pipeline-fixes-for-VK_EXT_graphics_pipeline.patch
Patch563:	0564-venus-Enable-VK_EXT_graphics_pipeline_library-behind.patch
Patch564:	0565-nir-lower_fragcolor-preserve-location_frac.patch
Patch565:	0566-zink-update-pointer-for-GPL-pipeline-cache-entry-for.patch
Patch566:	0567-zink-fix-legacy-depth-texture-rewriting-for-single-c.patch
Patch567:	0568-ci-zink-Only-test-half-of-piglit-pre-merge-on-anv.patch
Patch568:	0569-ci-Stop-doing-internal-retries-in-bare-metal.patch
Patch569:	0570-ci-bare-metal-Drop-the-2-vs-1-exit-code-from-poe_run.patch
Patch570:	0571-ci-bare-metal-Default-our-boards-to-a-20-minute-time.patch
Patch571:	0572-ci-iris-Drop-parallel-on-kbl-piglit-to-2.patch
Patch572:	0573-ci-freedreno-Fold-a630_egl-into-a630_gl.patch
Patch573:	0574-ci-freedreno-Move-skqp-testing-to-a618.patch
Patch574:	0575-ci-zink-Cut-zink-lvp-coverage-in-half.patch
Patch575:	0576-anv-don-t-uninitialize-bvh_bo_pool-is-not-initialize.patch
Patch576:	0577-ci-freedreno-Generalize-the-implicit_unmap-timeouts.patch
Patch577:	0578-anv-uninitialize-queues-before-utrace.patch
Patch578:	0579-nvk-Advertise-VK_EXT_attachment_feedback_loop_layout.patch
Patch579:	0580-features-Mark-VK_EXT_attachment_feedback_loop_layout.patch
Patch580:	0581-nvk-Re-arrange-Vulkan-1.2-features-to-match-the-head.patch
Patch581:	0582-nvk-Advertise-shaderOutputLayer-and-shaderOutputView.patch
Patch582:	0583-nvk-Enable-descriptorIndexing.patch
Patch583:	0584-nvk-Implement-VK_EXT_dynamic_rendering_unused_attach.patch
Patch584:	0585-radv-Rename-SDMA-file-to-radv_sdma.c.patch
Patch585:	0586-radv-Use-const-device-argument-in-radv_sdma_copy_buf.patch
Patch586:	0587-radv-Use-const-on-vi_alpha_is_on_msb-arguments.patch
Patch587:	0588-radv-Only-call-si_cp_dma_wait_for_idle-on-GFX-and-AC.patch
Patch588:	0589-radv-Move-radv_cp_wait_mem-to-radv_cs.h-and-add-queu.patch
Patch589:	0590-radv-Refactor-WRITE_DATA-helper-function.patch
Patch590:	0591-radv-Use-new-WRITE_DATA-helper-in-more-places.patch
Patch591:	0592-radv-Add-queue-family-argument-to-some-functions.patch
Patch592:	0593-radv-Wait-for-bottom-of-pipe-in-ACE-gang-wait-postam.patch
Patch593:	0594-radeonsi-Add-perfetto-support-in-radeonsi.patch
Patch594:	0595-radeonsi-Add-u_trace-init-code-in-radeonsi.patch
Patch595:	0596-radeonsi-Add-tracepoints-in-radeonsi-driver.patch
Patch596:	0597-egl-unify-dri2_egl_display-creation.patch
Patch597:	0598-egl-init-dri3-version-info-during-screen-creation.patch
Patch598:	0599-egl-glx-don-t-load-non-sw-zink-without-dri3-support.patch
Patch599:	0600-egl-add-automatic-zink-fallback-loading-between-hw-a.patch
Patch600:	0601-glx-add-automatic-zink-fallback-loading-between-hw-a.patch
Patch601:	0602-ci-don-t-set-GALLIUM_DRIVER-for-zink.patch
Patch602:	0603-egl-wayland-only-add-more-registry-listeners-for-har.patch
Patch603:	0604-svga-ignore-sampler-view-resource-if-not-used-by-sha.patch
Patch604:	0605-venus-Fix-Wmaybe-uninitialized.patch
Patch605:	0606-venus-set-lvp-queries-as-saturate-on-overflow.patch
Patch606:	0607-frontends-va-Add-profile-param-when-querying-PIPE_VI.patch
Patch607:	0608-d3d12-Upgrade-to-D3D12-Agility-SDK-1.611-Video-inter.patch
Patch608:	0609-d3d12-Fixes-AV1-tx_mode_support-reporting-and-unsupp.patch
Patch609:	0610-d3d12-Video-Decode-Wait-for-GPU-completion-before-de.patch
Patch610:	0611-d3d12-Do-not-destroy-codec-when-destroying-video-buf.patch
Patch611:	0612-d3d12-AV1-encode-Add-lower-resolution-fallback-check.patch
Patch612:	0613-d3d12-AV1-encode-add-fallback-for-app-passing-unsupp.patch
Patch613:	0614-d3d12-AV1-Encode-Fix-VAConfigAttribEncMaxRefFrames-r.patch
Patch614:	0615-frontend-va-Add-support-for-VAConfigAttribEncMaxTile.patch
Patch615:	0616-d3d12-Add-support-for-PIPE_VIDEO_CAP_ENC_MAX_TILE_RO.patch
Patch616:	0617-d3d12-Allocate-d3d12_video_buffer-with-higher-alignm.patch
Patch617:	0618-amd-common-update-addrlib-for-gfx11.5.patch
Patch618:	0619-amd-common-add-registers-for-gfx11.5.patch
Patch619:	0620-ac-nir-extract-must_wait_attr_ring-helper.patch
Patch620:	0621-amd-radeonsi-Add-code-to-enable-gfx11.5.patch
Patch621:	0622-amd-common-update-DCC-for-gfx11.5.patch
Patch622:	0623-radeonsi-vcn-set-jpeg-reg-version-for-gfx-1150.patch
Patch623:	0624-ci_run_n_monitor-Poll-mesa-mesa-and-user-mesa-for-pi.patch
Patch624:	0625-glx-Delete-support-for-GLX_OML_swap_method.patch
Patch625:	0626-ci-drop-skip-for-glx-swap-copy.patch
Patch626:	0627-dri-Drop-a-duplicate-mesa-vs-pipe-format-table.patch
Patch627:	0628-Revert-etnaviv-use-correct-blit-box-sizes-when-copyi.patch
Patch628:	0629-anv-move-generation-shader-return-instruction-to-las.patch
Patch629:	0630-anv-fix-generated-draws-gl_DrawID-with-more-than-819.patch
Patch630:	0631-anv-extract-out-draw-call-generation.patch
Patch631:	0632-anv-identify-internal-shader-in-NIR.patch
Patch632:	0633-anv-avoid-MI-commands-to-copy-draw-indirect-count.patch
Patch633:	0634-anv-move-generation-batch-fields-to-a-sub-struct.patch
Patch634:	0635-util-glsl2spirv-add-ability-to-pass-defines.patch
Patch635:	0636-anv-factor-out-host-gpu-internal-shaders-interfaces.patch
Patch636:	0637-anv-index-indirect-data-buffer-with-absolute-offset.patch
Patch637:	0638-anv-add-ring-buffer-mode-to-generated-draw-optimizat.patch
Patch638:	0639-anv-merge-gfx9-11-indirect-draw-generation-shaders.patch
Patch639:	0640-anv-document-the-draw-indirect-optimization-ring-mod.patch
Patch640:	0641-pvr-Implement-VK_KHR_external_fence.patch
Patch641:	0642-pvr-Implement-VK_KHR_external_semaphore.patch
Patch642:	0643-pvr-Enable-VK_KHR_bind_memory2-extension.patch
Patch643:	0644-pvr-Implement-VK_EXT_texel_buffer_alignment.patch
Patch644:	0645-pvr-Implement-VK_EXT_host_query_reset.patch
Patch645:	0646-frontends-va-Fix-locking-in-vlVaBeginPicture.patch
Patch646:	0647-zink-wrap-shared-memory-blocks-in-a-struct.patch
Patch647:	0648-zink-properly-alias-shared-memory.patch
Patch648:	0649-mesa-add-GL_APPLE_sync-support.patch
Patch649:	0650-ci-marge_queue-add-missing-python-dateutils-to-requi.patch
Patch650:	0651-ci-venus-mark-more-flaky-tests-after-recent-cts-upre.patch
Patch651:	0652-svga-Make-surfaces-shareable-at-creation.patch
Patch652:	0653-svga-Unify-gmr-and-mob-surface-pool-managers.patch
Patch653:	0654-ci-freedreno-fix-copy-paste-causing-a618_gl-being-ru.patch
Patch654:	0655-radeonsi-fixes-compilaton-error-when-perfetto-is-dis.patch
Patch655:	0656-ci-freedreno-disable-Adreno-660-Vulkan-pre-merge.patch
Patch656:	0657-ci-ci_run_n_monitor-keep-monitoring-if-a-job-is-stil.patch
Patch657:	0658-ci-b2c-change-artifacts-path-to-match-baremetal-and-.patch
Patch658:	0659-pvr-Only-setup-the-bgobj-to-load-if-we-have-a-load_o.patch
Patch659:	0660-etnaviv-drm-Be-able-to-mark-end-of-context-init.patch
Patch660:	0661-etnaviv-Skip-empty-cmd-streams.patch
Patch661:	0662-zink-fix-zink_destroy_screen-for-early-screen-creati.patch
Patch662:	0663-freedreno-drm-virtio-Use-MESA_TRACE_SCOPE-instead-of.patch
Patch663:	0664-tu-Use-MESA_TRACE_SCOPE-instead-of-_BEGIN-_END.patch
Patch664:	0665-aux-tc-Use-MESA_TRACE_SCOPE-instead-of-_BEGIN-_END.patch
Patch665:	0666-venus-Change-the-only-occurrence-of-VN_TRACE_BEGIN-E.patch
Patch666:	0667-util-Avoid-the-use-of-MESA_TRACE_BEGIN-END.patch
Patch667:	0668-util-perf-Remove-the-tracing-categories.patch
Patch668:	0669-util-Remove-MESA_TRACE_BEGIN-END.patch
Patch669:	0670-docs-ci-Drop-old-instructions-for-farm-disabling.patch
Patch670:	0671-docs-ci-Add-some-links-in-the-CI-docs-to-how-to-trac.patch
Patch671:	0672-radv-rra-Recognize-LPDDR-memory.patch
Patch672:	0673-radv-rmv-Recognize-LPDDR-memory.patch
Patch673:	0674-intel-Return-a-bool-from-intel_aux_map_add_mapping.patch
Patch674:	0675-anv-Move-scope-of-CCS-binding-determination.patch
Patch675:	0676-anv-Allocate-space-for-aux-map-CCS-in-image-bindings.patch
Patch676:	0677-anv-Wrap-aux-surface-image-binding-queries.patch
Patch677:	0678-anv-Refactor-CCS-disabling-at-image-bind-time.patch
Patch678:	0679-anv-Place-images-into-the-aux-map-when-safe-to-do-so.patch
Patch679:	0680-anv-Loosen-anv_bo_allows_aux_map.patch
Patch680:	0681-anv-Meet-CCS-alignment-reqs-with-dedicated-allocs.patch
Patch681:	0682-anv-Delete-implicit-CCS-code.patch
Patch682:	0683-intel-isl-Add-scores-for-GEN12_RC_CCS-and-MTL_RC_CCS.patch
Patch683:	0684-radv-skip-zero-sized-memcpy.patch
Patch684:	0685-ac-nir-fix-out-of-bounds-access-in-ac_nir_export_pos.patch
Patch685:	0686-radv-fix-signed-integer-overflow.patch
Patch686:	0687-spirv-Expose-stage-enum-conversion-in-vtn_private.h.patch
Patch687:	0688-spirv-Change-spirv2nir-to-use-the-shorter-shader-nam.patch
Patch688:	0689-spirv-List-entry-points-in-spirv2nir-when-unsure-wha.patch
Patch689:	0690-spirv-Let-spirv2nir-find-out-the-shader-to-use.patch
Patch690:	0691-intel-Sync-xe_drm.h.patch
Patch691:	0692-anv-Switch-Xe-KMD-vm-bind-to-sync.patch
Patch692:	0693-glsl-Remove-int64-div-mod-lowering.patch
Patch693:	0694-llvmpipe-Set-nir_lower_dround_even.patch
Patch694:	0695-nir-Add-nir_lower_dsign-as-64-bit-fsign-lowering.patch
Patch695:	0696-glsl-Retire-dround-lowering.patch
Patch696:	0697-amd-common-add-missing-stuff-for-gfx11.5.patch
Patch697:	0698-amd-radeonsi-add-missing-stuff-for-gfx11.5.patch
Patch698:	0699-zink-only-increment-image_rebind_counter-on-image-ex.patch
Patch699:	0700-zink-check-for-sampler-view-existence-during-zink_re.patch
Patch700:	0701-radeonsi-add-more-documentation-for-dpbb-debug-env-v.patch
Patch701:	0702-docs-remove-document-for-unused-variable-dfsm-from-A.patch
Patch702:	0703-radeonsi-correct-old-comment-in-si_emit_framebuffer_.patch
Patch703:	0704-radeonsi-In-gfx6_init_gfx_preamble_state-use-gfx_lev.patch
Patch704:	0705-radeonsi-add-radeonsi-to-GL_RENDERER-string.patch
Patch705:	0706-radv-set-ENABLE_PING_PONG_BIN_ORDER-for-GFX11.5.patch
Patch706:	0707-radv-initialize-video-decoder-for-GFX11.5.patch
Patch707:	0708-Revert-radv-pre-init-surface-info.patch
Patch708:	0709-anv-cleanup-includes.patch
Patch709:	0710-ac-gpu_info-query-the-maximum-number-of-IBs-per-subm.patch
Patch710:	0711-ci-marge_queue-add-pretty_dutation.patch
Patch711:	0712-ci-ci_run_n_monitor-print-job-duration-time.patch
Patch712:	0713-nir-Add-AMD-cooperative-matrix-intrinsics.patch
Patch713:	0714-aco-Add-WMMA-instructions.patch
Patch714:	0715-aco-Make-RA-understand-WMMA-instructions.patch
Patch715:	0716-radv-Don-t-transparently-use-wave32-with-cooperative.patch
Patch716:	0717-radv-Add-cooperative-matrix-lowering.patch
Patch717:	0718-radv-Expose-VK_KHR_cooperative_matrix.patch
Patch718:	0719-Revert-radv-fix-finding-shaders-by-PC.patch
Patch719:	0720-radv-fix-missing-predicate-bit-for-WRITE_DATA-helper.patch
Patch720:	0721-radv-Simplify-gang-CS-and-semaphore-initialization.patch
Patch721:	0722-radv-Allow-gang-submit-use-cases-other-than-task-sha.patch
Patch722:	0723-radv-Slightly-refactor-gang-semaphore-functions.patch
Patch723:	0724-radv-Add-gang-follower-semaphore-functions.patch
Patch724:	0725-v3d-vc4-ci-add-new-fails-timeout.patch
Patch725:	0726-radeonsi-vcn-disable-tmz-ctx-buffer-for-VCN_2_2_0.patch
Patch726:	0727-anv-turn-off-non-zero-fast-clears-for-CCS_E.patch
Patch727:	0728-anv-selectively-enable-FCV-optimization-for-DG2.patch
Patch728:	0729-ac-gpu_info-fix-querying-the-maximum-number-of-IBs-p.patch
Patch729:	0730-intel-compiler-Don-t-emit-calls-to-validate-in-relea.patch
Patch730:	0731-nir-improve-ms_cross_invocation_output_access-with-l.patch
Patch731:	0732-aco-nir-add-export_row_amd-intrinsic.patch
Patch732:	0733-ac-nir-add-row-parameter-to-helpers.patch
Patch733:	0734-ac-nir-remove-dead-code.patch
Patch734:	0735-ac-nir-refactor-mesh-vertex-primitive-export.patch
Patch735:	0736-ac-nir-implement-mesh-shader-gs_fast_launch-2.patch
Patch736:	0737-ac-nir-optimize-mesh-shader-local_invocation_index.patch
Patch737:	0738-radv-implement-mesh-shader-gs_fast_launch-2.patch
Patch738:	0739-ac-nir-add-emit_ms_outputs-helper.patch
Patch739:	0740-ac-nir-radv-pass-workgroup-size-to-ac_nir_lower_ngg_.patch
Patch740:	0741-ac-nir-implement-mesh-shader-multi-row-export.patch
Patch741:	0742-radv-implement-mesh-shader-multi-row-export.patch
Patch742:	0743-radv-enable-mesh-shader-gs_fast_launch-2-and-multi-r.patch
Patch743:	0744-nir-Add-a-nir_ssa_def_all_uses_are_fsat-helper.patch
Patch744:	0745-nir-Add-convert_alu_types-to-divergence-analysis.patch
Patch745:	0746-nir-lower_tex-Add-a-lower_txd_clamp-option.patch
Patch746:	0747-nir-Add-a-load_sysval_nv-intrinsic.patch
Patch747:	0748-nir-Add-NV-specific-texture-opcodes.patch
Patch748:	0749-nir-Add-an-load_barycentric_at_offset_nv-intrinsic.patch
Patch749:	0750-nir-Add-a-range-to-most-I-O-intrinsics.patch
Patch750:	0751-nir-Add-NVIDIA-specific-I-O-intrinsics.patch
Patch751:	0752-nir-Add-NVIDIA-specific-geometry-shader-opcodes.patch
Patch752:	0753-radv-Support-SDMA-in-radv_cs_write_data_head.patch
Patch753:	0754-radv-Support-SDMA-in-radv_cp_wait_mem.patch
Patch754:	0755-radv-Support-SDMA-in-si_cs_emit_write_event_eop.patch
Patch755:	0756-anv-prep-for-gen9-astc-workaround.patch
Patch756:	0757-anv-add-gen9-astc-workaround.patch
Patch757:	0758-frontends-va-Parse-H264-SPS-for-max_num_reorder_fram.patch
Patch758:	0759-util-vl-Fix-vl_rbsp-parser-with-bitstreams-without-e.patch
Patch759:	0760-frontends-va-Fix-parsing-packed-headers-without-emul.patch
Patch760:	0761-radeonsi-vcn-Add-encode-support-for-H264-B-frames.patch
Patch761:	0762-ci_run_n_monitor-Always-resolve-rev-arguments-for-lo.patch
Patch762:	0763-compiler-types-Flip-wrapping-of-type-contains-predic.patch
Patch763:	0764-compiler-types-Flip-wrapping-of-array-related-functi.patch
Patch764:	0765-compiler-types-Flip-wrapping-of-cmat-related-functio.patch
Patch765:	0766-compiler-types-Flip-wrapping-of-CL-related-functions.patch
Patch766:	0767-compiler-types-Flip-wrapping-of-size-related-functio.patch
Patch767:	0768-compiler-types-Flip-wrapping-of-struct-related-funct.patch
Patch768:	0769-compiler-types-Flip-wrapping-of-interface-related-fu.patch
Patch769:	0770-compiler-types-Flip-wrapping-of-layout-related-funct.patch
Patch770:	0771-compiler-types-Flip-wrapping-of-record_compare.patch
Patch771:	0772-compiler-types-Flip-wrapping-of-get_instance.patch
Patch772:	0773-compiler-types-Flip-wrapping-of-texture-sampler-imag.patch
Patch773:	0774-compiler-types-Flip-wrapping-of-various-get-instance.patch
Patch774:	0775-compiler-types-Flip-wrapping-of-get-row-column-type-.patch
Patch775:	0776-compiler-types-Flip-wrapping-of-remaining-non-trivia.patch
Patch776:	0777-compiler-types-Flip-wrapping-of-remaining-small-data.patch
Patch777:	0778-compiler-types-Flip-wrapping-of-numeric-type-convers.patch
Patch778:	0779-compiler-types-Move-remaining-code-from-nir_types-to.patch
Patch779:	0780-rusticl-Add-bindings-for-glsl_vector_type.patch
Patch780:	0781-compiler-types-Add-more-glsl_contains_-functions-and.patch
Patch781:	0782-compiler-types-Add-glsl_get_mul_type-and-use-it-in-C.patch
Patch782:	0783-compiler-types-Add-glsl_type_compare_no_precision-an.patch
Patch783:	0784-compiler-types-Add-glsl_type_uniform_locations-and-u.patch
Patch784:	0785-compiler-types-Add-glsl_get_std430_array_stride-and-.patch
Patch785:	0786-compiler-types-Add-glsl_get_explicit_-functions-and-.patch
Patch786:	0787-compiler-types-Implement-glsl_type-field_type-in-ter.patch
Patch787:	0788-compiler-types-Add-glsl_simple_explicit_type-and-sim.patch
Patch788:	0789-compiler-types-Add-remaining-type-extraction-functio.patch
Patch789:	0790-compiler-types-Use-C-instead-of-C-constants-for-buil.patch
Patch790:	0791-compiler-types-Remove-usages-of-C-members-in-glsl_ty.patch
Patch791:	0792-compiler-types-Annotate-extern-C-only-once-in-glsl_t.patch
Patch792:	0793-compiler-types-Rename-glsl_types.cpp-to-glsl_types.c.patch
Patch793:	0794-compiler-types-Remove-warnings-about-potential-fallt.patch
Patch794:	0795-compiler-types-Move-comments-and-reorganize-declarat.patch
Patch795:	0796-intel-dev-expand-existing-fix-for-all-gfx12-with-sma.patch
Patch796:	0797-ci-Bump-PyYAML-to-6.0.1.patch
Patch797:	0798-etnaviv-Don-t-leak-disk_cache.patch
Patch798:	0799-anv-fixup-32bit-build-of-internal-shaders.patch
# FIXME disabled because it needs 0509-0511
#Patch799:	0800-egl-fix-leaking-drmDevicePtr-in-_eglFindDevice.patch
Patch800:	0801-panfrost-Fix-error-in-comment.patch
Patch801:	0802-panfrost-Add-methods-to-determine-slice-and-body-ali.patch
Patch802:	0803-panfrost-Add-method-to-get-size-of-AFBC-subblocks.patch
Patch803:	0804-panfrost-Precalculate-stride-and-nr-of-blocks-for-AF.patch
Patch804:	0805-panfrost-Add-panfrost_batch_write_bo.patch
Patch805:	0806-panfrost-Make-panfrost_resource_create_with_modifier.patch
# FIXME these clash with Panthor
#Patch806:	0807-panfrost-Split-out-internal-of-panfrost_launch_grid.patch
#Patch807:	0808-panfrost-Add-infrastructure-for-internal-AFBC-comput.patch
#Patch808:	0809-panfrost-Add-method-to-get-size-of-AFBC-superblocks-.patch
#Patch809:	0810-panfrost-Add-support-for-AFBC-packing.patch
Patch810:	0811-panfrost-Legalize-resource-when-attaching-to-a-batch.patch
Patch811:	0812-panfrost-Don-t-force-constant-modifier-after-convert.patch
# FIXME clashes with Panthor
#Patch812:	0813-panfrost-Add-debug-flag-to-force-packing-of-AFBC-tex.patch
#Patch813:	0814-panfrost-Add-some-debug-utility-methods-for-resource.patch
#Patch814:	0815-panfrost-Add-env-variable-for-max-AFBC-packing-ratio.patch
Patch815:	0816-zink-Fix-SyntaxWarning-in-zink_extensions-script.patch
Patch816:	0817-radv-remove-outdated-RADV_DEBUG-vmfaults-support.patch
Patch817:	0818-amd-update-amdgpu_drm.h.patch
Patch818:	0819-amd-add-has_gpuvm_fault_query.patch
Patch819:	0820-radv-amdgpu-add-support-quering-the-last-GPUVM-fault.patch
Patch820:	0821-radv-query-and-report-the-last-GPUVM-fault-with-RADV.patch
Patch821:	0822-radv-report-the-last-GPUVM-fault-when-a-device-lost-.patch
Patch822:	0823-docs-features-remove-empty-lines-confusing-mesamatri.patch
Patch823:	0824-nir-trivialize_registers-Handle-obscure-load-hazard.patch
Patch824:	0825-nir-serialize-fix-signed-integer-overflow.patch
Patch825:	0826-nir-lower_shader_calls-skip-zero-sized-qsort.patch
Patch826:	0827-util-skip-zero-sized-SHA1Update.patch
Patch827:	0828-zink-use-weston-for-anv-ci.patch
Patch828:	0829-zink-blow-up-broken-xservers-more-reliably.patch
Patch829:	0830-zink-delete-some-dead-modifier-handling.patch
Patch830:	0831-ci-skip-implicit-modifier-piglits-for-zink.patch
Patch831:	0832-v3dv-fix-confusing-nomenclature-about-DRM-nodes.patch
Patch832:	0833-anv-fix-uninitialized-use-of-compute-initialization-.patch
Patch833:	0834-VERSION-bump-for-rc1.patch

# Without this patch, the OpenCL ICD calls into MesaOpenCL,
# which for some reason calls back into the OpenCL ICD instead
# of calling its own function by the same name.
Patch1000:	mesa-20.1.1-fix-opencl.patch
# Use llvm-config to detect llvm, since the newer method
# finds /usr/lib64/libLLVM-17.so even for 32-bit builds
Patch1001:	mesa-23.1-x86_32-llvm-detection.patch
# Fix intel-vk build with clang 16 and gcc 13
Patch1002:	mesa-23.1-intel-vk-compile.patch
# Not used in the spec; this is a test case to verify patch0
# is still needed. If this code works without the patch, the
# patch can be removed. If it crashes/takes forever (infinite
# loop), the patch is still needed.
Source50:	test.c

#Patch1:		mesa-19.2.3-arm32-buildfix.patch
#Patch2:		mesa-20.3.4-glibc-2.33.patch
Patch1003:	mesa-20.3.0-meson-radeon-arm-riscv-ppc.patch

Patch1004:	mesa-buildsystem-improvements.patch

# Make VirtualBox great again
# Broken by commit 2569215f43f6ce71fb8eb2181b36c6cf976bce2a
Patch1005:	mesa-22.3-make-vbox-great-again.patch

# Fix LLVM 17 support
#Patch1006:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/25536.patch
# Adapt Patch20 to work with 23.2 branch
#Patch1007:	backport-25536.patch

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

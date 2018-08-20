;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;            Copyright (C) 1994, Alias Research, Inc.                        ;
;                                                                            ;
;    These coded instructions,  statements and  computer programs contain    ;
;    unpublished information proprietary to Alias Research, Inc.  and are    ;
;    protected by the Canadian and US Federal copyright law. They may not    ;
;    be disclosed to third parties  or copied  or duplicated, in whole or    ;
;    in part,  without the prior written consent of Alias Research,  Inc.    ;
;                                                                            ;
; Unpublished-rights reserved under the Copyright Laws of the United States. ;
;                                                                            ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;---------------------------------------------------------
;;			MAIN MENU
;;---------------------------------------------------------

	(ui-symbol 'shelf_extras_tab 'CML_MAIN)
	(ui-string "shelf_extras_tab"  "Shelf Extras")
	(ui-string "shelf_extras_tab_attr"  "Shelf Extras")
	(ui-menu "shelf_extras_tab"
		(list 'select           "ma_menu" '0)
		(list 'label_string     "shelf_extras_tab")
		(list 'attribute_string "shelf_extras_tab_attr")
	)
	(ui-level-add-menu "al_extras_palette" 'shelf_extras_tab  )

	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_blank")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_blank_vert")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_blank_horz")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_braceleft")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_braceright")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_spacerdag")
	(ui-menu-add-entry "shelf_extras_tab" "ma_extras_studio")


;; Curve networks Level

(ui-menu "mo_cnet_tools"
	(list 'label_string 	'mo_cnet_tools)
	(list 'attribute_string 'mo_cnet_tools)
)

(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_pick)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_new)

(ui-submenu "mo_cnet_continuity_sub")
	(ui-submenu-add-entry "mo_cnet_continuity_sub"		'mo_cnet_pos_continuity)
	(ui-submenu-add-entry "mo_cnet_continuity_sub"		'mo_cnet_tan_continuity)
;	(ui-submenu-add-entry "mo_cnet_continuity_sub"		'mo_cnet_curve_continuity)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_continuity_sub)

(ui-submenu "mo_cnet_add_sub")
	(ui-submenu-add-entry "mo_cnet_add_sub"		'mo_cnet_add)
	(ui-submenu-add-entry "mo_cnet_add_sub"		'mo_cnet_subtract)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_add_sub)

;(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_implied)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_analyze)

(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_map_shape)
(ui-submenu "mo_cnet_add_control_sub")
	(ui-submenu-add-entry "mo_cnet_add_control_sub"		'mo_cnet_add_control)
	(ui-submenu-add-entry "mo_cnet_add_control_sub"		'mo_cnet_del_control)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_add_control_sub)

(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_pin)
(ui-submenu "mo_cnet_weight_sub")
	(ui-submenu-add-entry "mo_cnet_weight_sub"		'mo_cnet_unit_weight)
	(ui-submenu-add-entry "mo_cnet_weight_sub"		'mo_cnet_multi_weight)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_weight_sub)

(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_lock)
(ui-submenu "mo_cnet_region_sub")
	(ui-submenu-add-entry "mo_cnet_region_sub"		'mo_cnet_region_high)
	(ui-submenu-add-entry "mo_cnet_region_sub"		'mo_cnet_region_medium)
	(ui-submenu-add-entry "mo_cnet_region_sub"		'mo_cnet_region_low)
(ui-menu-add-entry "mo_cnet_tools"		'mo_cnet_region_sub)

(ui-level-add-menu "mo_curve_networks_palette" 'mo_cnet_tools)



;; Blend curve level

(ui-string "mo_blend_crv_tools"      "BlendCrv Tools")
(ui-string "mo_blend_crv_delete"     "Constraint Edits")
(ui-string "mo_blend_crv_toggle"     "Constraint Interpolation Direction")
(ui-string "mo_blend_crv_continuity" "Constraint Continuity")
(ui-string "mo_blend_crv_direction"  "Constraint Direction Type")
(ui-string "mo_blend_crv_extension"  "Constraint Curvature Type")
(ui-string "mo_blend_crv_degree"     "Curve Degree")
(ui-string "mo_blend_crv_parameter"  "Curve Knot Spacing")
(ui-string "mo_blend_crv_pt_master_slave"  "Swap Master Slave")

(ui-menu "mo_blend_crv_tools"
	(list 'label_string 	'mo_blend_crv_tools)
	(list 'attribute_string 'mo_blend_crv_tools)
)

(ui-menu-add-entry "mo_blend_crv_tools"		"mp_blend_crv_create")
(ui-menu-add-entry "mo_blend_crv_tools"		"mp_blend_crv_edit")
(ui-menu-add-entry "mo_blend_crv_tools"     "mp_blend_crv_edit_tangent")
(ui-menu-add-entry "mo_blend_crv_tools"     "mp_blend_crv_planarize")
(ui-menu-add-entry "mo_blend_crv_tools"     "mp_blend_crv_pt_dissociate")
(ui-menu-add-entry "mo_blend_crv_tools"     "mp_blend_crv_pt_make_master")

(ui-submenu "mo_blend_crv_toggle")
	(ui-submenu-add-entry "mo_blend_crv_toggle"	"mp_blend_crv_toggle_loc")
	(ui-submenu-add-entry "mo_blend_crv_toggle"	"mp_blend_crv_toggle_xyz")
	(ui-submenu-add-entry "mo_blend_crv_toggle"	"mp_blend_crv_toggle_geom")
(ui-menu-add-entry "mo_blend_crv_tools"		"mo_blend_crv_toggle")

(ui-submenu "mo_blend_crv_direction")
    (ui-submenu-add-entry "mo_blend_crv_direction" "mp_blend_crv_direction_ray")
    (ui-submenu-add-entry "mo_blend_crv_direction" "mp_blend_crv_direction_parallel")
(ui-menu-add-entry "mo_blend_crv_tools" "mo_blend_crv_direction")

(ui-submenu "mo_blend_crv_continuity")
    (ui-submenu-add-entry "mo_blend_crv_continuity" "mp_blend_crv_G0")
    (ui-submenu-add-entry "mo_blend_crv_continuity" "mp_blend_crv_G1")
    (ui-submenu-add-entry "mo_blend_crv_continuity" "mp_blend_crv_G2")
    (ui-submenu-add-entry "mo_blend_crv_continuity" "mp_blend_crv_G3")
    (ui-submenu-add-entry "mo_blend_crv_continuity" "mp_blend_crv_G4")
(ui-menu-add-entry "mo_blend_crv_tools"     "mo_blend_crv_continuity")

(ui-submenu "mo_blend_crv_extension")
    (ui-submenu-add-entry "mo_blend_crv_extension" "mp_blend_crv_direction_geometric")
    (ui-submenu-add-entry "mo_blend_crv_extension" "mp_blend_crv_direction_parametric")
(ui-menu-add-entry "mo_blend_crv_tools" "mo_blend_crv_extension")

(ui-submenu "mo_blend_crv_degree")
    (ui-submenu-add-entry "mo_blend_crv_degree"   "mp_blend_crv_degree_1")
    (ui-submenu-add-entry "mo_blend_crv_degree"   "mp_blend_crv_degree_2")
    (ui-submenu-add-entry "mo_blend_crv_degree"   "mp_blend_crv_degree_3")
    (ui-submenu-add-entry "mo_blend_crv_degree"   "mp_blend_crv_degree_5")
    (ui-submenu-add-entry "mo_blend_crv_degree"   "mp_blend_crv_degree_7")
(ui-menu-add-entry "mo_blend_crv_tools"     "mo_blend_crv_degree")

(ui-submenu "mo_blend_crv_parameter")
    (ui-submenu-add-entry "mo_blend_crv_parameter" "mp_blend_crv_param_chord")
    (ui-submenu-add-entry "mo_blend_crv_parameter" "mp_blend_crv_param_uniform")
(ui-menu-add-entry "mo_blend_crv_tools" "mo_blend_crv_parameter")

(ui-level-add-menu "mo_blend_curve_palette" "mo_blend_crv_tools")



;; File ----------------------------------------------------
	(ui-menu "al_file"
		(list 'select "mp_menu" 0)
		(list 'label_string "al_file_title")
		(list 'attribute_string "al_file_attribute")
	)

;; Alias FreeForm Surfacing Interface to SDRC I-DEAS Master Series.

	(ui-submenu "al_sdrc_ffs_sub" )
		(ui-submenu-add-entry "al_sdrc_ffs_sub" "mp_file_ffs_quit_no_save" );
		(ui-submenu-add-entry "al_sdrc_ffs_sub" "mp_file_ffs_quit_save" );
		(ui-submenu-add-entry "al_sdrc_ffs_sub" "mp_file_ffs_tmp_save" );
	(ui-menu-add-entry "al_file"    	"al_sdrc_ffs_sub")

	(ui-menu-add-entry "al_file"      "mp_file_new")		; New


	(ui-menu-add-separator "al_file")
	(ui-menu-add-entry "al_file"      "al_file_stage")		; Open

	(ui-submenu "al_recentfiles_sub"        )
		(ui-submenu-add-entry "al_recentfiles_sub" "mp_file_recentfiles_clear" );
		(ui-submenu-add-separator "al_recentfiles_sub")
	(ui-menu-add-entry "al_file"        "al_recentfiles_sub")

	(ui-menu-add-entry "al_file"      "mp_file_stageset")	; OpenStageset
	(ui-menu-add-separator "al_file")

;;  vault
    (ui-string "al_vault_sub"    		"Vault Server" )
    (ui-submenu "al_vault_sub" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_connect" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_open" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_checkout" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_checkin" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_cancel_checkout" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_disconnect" )
        (ui-submenu-add-entry "al_vault_sub" "mp_launch_standalone_vault" )
        (ui-submenu-add-entry "al_vault_sub" "mp_vault_options" )

	(if (ui-symbol-true "mo_vault_enabled")
    	(ui-menu-add-entry "al_file"      "al_vault_sub")
	)
	(if (ui-symbol-true "mo_vault_enabled")
		(ui-menu-add-separator "al_file")
	)

	(if (ui-symbol-true "mo_file_enable_disk_save" )
 		(begin
			(ui-menu-add-entry "al_file"      "mp_file_save_all")	; Save
			(ui-menu-add-entry "al_file"      "mp_file_save_all_as"); Save as
		)
	)
	(ui-menu-add-entry "al_file"      "mp_file_save_stageset"); Save Stageset


	(ui-menu-add-entry "al_file"      "mp_file_save_chkpnt"); Save Check Point

	(ui-menu-add-separator "al_file")

	(ui-submenu "al_import_sub" )
		(ui-submenu-add-entry "al_import_sub" "mp_file_retrieve" );
		(ui-submenu-add-entry "al_import_sub" "LoadReference" );
		(ui-submenu-add-entry "al_import_sub" "cd_file_retrieve_cloud" );
		(ui-submenu-add-entry "al_import_sub" "mp_file_cmm" );
		(ui-submenu-add-entry "al_import_sub" "al_file_retrieve_anim" );
		(ui-submenu-add-separator "al_import_sub")

;; Import of StudioPaint should not be supported anymore
;;		(ui-submenu-add-entry "al_import_sub" "mp_file_imp_paint" );
		(ui-submenu-add-entry "al_import_sub" "mp_file_image" );
		(ui-submenu-add-entry "al_import_sub" "mp_file_import_canvas" )
		(ui-submenu-add-entry "al_import_sub" "mp_file_subdiv" )

	(ui-menu-add-entry "al_file"    	"al_import_sub")

;;  Export menu. Used to export items. In other words specific save types
    (ui-submenu "al_export_types_sub"        )
		(ui-submenu-add-entry "al_export_types_sub"     "mp_file_save_active")
		(ui-submenu-add-separator "al_export_types_sub")

		(ui-submenu-add-entry "al_export_types_sub"		"al_file_save_sdl")
		(ui-submenu-add-entry "al_export_types_sub"		"al_file_save_anim")
		(ui-submenu-add-entry "al_export_types_sub"		"al_file_save_part")
		(ui-submenu-add-separator "al_export_types_sub")
		(ui-submenu-add-entry "al_export_types_sub" 	"mp_file_stl")
		(ui-submenu-add-entry "al_export_types_sub" 	"mp_file_stl14")
		(ui-submenu-add-entry "al_export_types_sub" 	"mp_file_slc")
		(ui-submenu-add-entry "al_export_types_sub" 	"mp_file_rp")
		(ui-submenu-add-separator "al_export_types_sub")

		(ui-submenu-add-entry "al_export_types_sub"    	"mp_file_screen")
		(ui-submenu-add-entry "al_export_types_sub"    	"mp_file_current_window")
		(ui-submenu-add-entry "al_export_types_sub"    	"mp_file_illustrator")

		(ui-submenu-add-separator "al_export_types_sub")
		(ui-submenu-add-entry "al_export_types_sub" "mp_file_export_image_layer" )
		(ui-submenu-add-entry "al_export_types_sub"    	"mp_file_make_picture")
		(ui-submenu-add-separator "al_export_types_sub")
		(ui-submenu-add-entry "al_export_types_sub"		"al_file_triangle")

    (ui-menu-add-entry "al_file"    	"al_export_types_sub")
	(ui-menu-add-separator "al_file")

    (ui-menu-add-entry "al_file"    	"mp_file_send_to_fusion")
	(ui-menu-add-entry "al_file"    	"mp_file_send_to_maya")
	(ui-menu-add-entry "al_file"    	"mp_file_send_to_showcase")
	(ui-menu-add-entry "al_file"    	"mp_file_send_to_vred")
	(ui-menu-add-entry "al_file"    	"mp_file_send_to_sketchbook")

	(ui-menu-add-separator "al_file")
	(ui-submenu "al_iman_sub" )
		(ui-submenu-add-entry "al_iman_sub" "al_iman_open" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_importAssembly");
;;		(if (ui-symbol-true	"aw_gm_de2009")
;;		  ( begin
;;			(ui-submenu-add-entry "al_iman_sub" "al_iman_paste_open" );
;;			(ui-submenu-add-entry "al_iman_sub" "al_iman_paste_importAssembly");
;;		  )
;;		)
		(ui-submenu-add-separator "al_iman_sub");
		(ui-submenu-add-entry "al_iman_sub" "al_iman_assembly_lister" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_components_import" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_save" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_save_as" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_save_active_as" );
;;		(ui-submenu-add-entry "al_iman_sub" "al_iman_check_out" );
;;		(ui-submenu-add-entry "al_iman_sub" "al_iman_check_in" );
;; disabled for bug 396196
;;		(ui-submenu-add-entry "al_iman_sub" "al_iman_check_out_cancel" );
;;		(ui-submenu-add-entry "al_iman_sub" "al_iman_prefs" );
		(ui-submenu-add-entry "al_iman_sub" "al_iman_login" );
	(ui-menu-add-entry "al_file"  "al_iman_sub")

	(ui-menu-add-separator "al_file")

	(ui-menu-add-entry "al_file" "mp_file_referencemanager")

	(ui-menu-add-separator "al_file")

	(ui-menu-add-entry "al_file"    "mp_file_plot" );
	(ui-menu-add-entry "al_file"    "mp_file_print_preview");

    (ui-menu-add-entry "al_file"    "mp_file_new_print_preview");

   	(ui-menu-add-separator "al_file")

	(ui-menu-add-entry "al_file" 	"mp_file_pix" )

	(ui-submenu	"al_image_ref_sub")
		(ui-submenu-add-entry 	"al_image_ref_sub"	"mp_ImageRefList");
		(ui-submenu-add-entry	"al_image_ref_sub"	"mp_file_extract_image_refs"); Extract Image References
	(ui-menu-add-entry	"al_file"	"al_image_ref_sub")


	;;	aw_fod_ext_apps will be set to true if the user
	;;	wants to override the focus on design effort to remove that feature
	;;	otherwise display the menu item and no option box.
	(if (ui-symbol-true "aw_fod_ext_apps" )
		(ui-menu-add-entry "al_file"        "mp_file_extrn")
	)

	(ui-menu-add-separator "al_file")
	(ui-menu-add-entry "al_file"        "mp_file_exit")

;; Edit ----------------------------------------------------
	(ui-menu "al_edit"
		(list 'select "mp_menu" 0)
		(list 'label_string "al_edit_title")
		(list 'attribute_string "al_edit_attribute")
	)
	(ui-menu-add-entry "al_edit"        "al_undo")
    (ui-menu-add-entry "al_edit"        "al_redo")

    (ui-menu-add-entry "al_edit"        "m_menu_reinvoke")

	(ui-menu-add-separator "al_edit")

	(ui-menu-add-entry "al_edit"        "mp_cut_object")
	(ui-menu-add-entry "al_edit"        "mp_copy_object")
	(ui-menu-add-entry "al_edit"        "mp_paste_object")



	(ui-menu-add-separator "al_edit")
	(ui-menu-add-entry "al_edit"        "mp_cut_image")
	(ui-menu-add-entry "al_edit"        "mp_copy_image")
	(ui-menu-add-entry "al_edit"        "mp_paste_image_plane")

	(ui-menu-add-separator "al_edit")

	(ui-submenu			  "al_edit_duplicate")
		(ui-submenu-add-entry "al_edit_duplicate"        "mp_object_tools_copy")
		(ui-submenu-add-entry "al_edit_duplicate"        "ap_mirror")
        (ui-submenu-add-entry "al_edit_duplicate"        "mp_object_tools_duplicate_reference")

	(ui-menu-add-entry "al_edit"    	"al_edit_duplicate")

	(ui-menu-add-separator "al_edit")
	(ui-menu-add-entry "al_edit" 	"mp_objmod_ungroup")
	(ui-menu-add-entry "al_edit" 	"mp_objmod_group")
	(ui-menu-add-entry "al_edit"  	"mp_expand_instances")



;;Delete ----------------------------------------------------
	(ui-menu "al_delete"
		(list 'select "mp_menu" 3)
		(list 'label_string "al_delete_title")
		(list 'attribute_string "al_delete_attribute")
	)
	(ui-menu-add-entry "al_delete"	"mp_delete_active")

	(ui-menu-add-separator "al_delete")

	(ui-menu-add-entry "al_delete"      	"mp_delete_trimhist")
	(ui-menu-add-entry "al_delete"       	"mo_del_all_locators")
	(ui-menu-add-entry "al_delete"			"mo_del_guidelines")
	(ui-menu-add-entry "al_delete"			"mp_delete_model")

	(ui-menu-add-separator "al_delete")

	(ui-submenu "paint_delete")

    (ui-submenu-add-entry "paint_delete" "m_paint_delete_canvasesfromcp")
    (ui-submenu-add-entry "paint_delete" "m_paint_delete_canvases")
	(ui-submenu-add-entry "paint_delete"        "m_menu_deletelayer")
	(ui-submenu-add-entry "paint_delete" "m_paint_delete_all_masks")
	(ui-submenu-add-separator "paint_delete")
	(ui-submenu-add-entry "paint_delete"     "rp_clear_sketch")

	(ui-menu-add-entry "al_delete"    	"paint_delete")
	(ui-menu-add-entry "al_delete"      "mp_delete_image")

;; Add sub menus for rendering functionality
	(ui-menu-add-entry "al_delete"      "mp_delete_projtxt")

;; Add sub menus for animation functionality
	(ui-submenu "animation_delete")
  	(ui-submenu-add-entry "animation_delete" 		"al_delete_sel_handles")
	(ui-submenu-add-entry "animation_delete"      "al_delete_channels")
   	(ui-submenu-add-entry "animation_delete"      "al_delete_action")
	(ui-submenu-add-entry "animation_delete"      "mp_delete_constraint")
	(ui-submenu-add-separator "animation_delete")
	(ui-menu-add-entry "al_delete"    	"animation_delete")

	(ui-menu-add-separator "al_delete")

	(ui-menu-add-entry "al_delete"      "mp_delete_windows")
	(ui-menu-add-entry "al_delete"      "mp_delete_node")



;;Layouts ---------------------------------------------------
	(ui-menu "mp_window"
		(list 'select "mp_menu" 6)
		(list 'label_string "al_layouts_title")
		(list 'attribute_string "al_layouts_attribute")
	)

	(ui-submenu  "windows_all_sub" )
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all7")
		(ui-submenu-add-entry "windows_all_sub"     "mp_window_all")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all6")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all5")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all10")
		(ui-submenu-add-entry "windows_all_sub"     "mp_window_all8")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all9")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all4")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all3")
		(ui-submenu-add-entry "windows_all_sub"		"mp_window_all2")
	(ui-menu-add-entry "mp_window" "windows_all_sub")

	(ui-menu-add-entry "mp_window"      "mp_window_perspect")

	(ui-menu-add-entry "mp_window"      "mp_window_front")
	(ui-menu-add-entry "mp_window"      "mp_window_back")
	(ui-menu-add-entry "mp_window"      "mp_window_right")
	(ui-menu-add-entry "mp_window"      "mp_window_left")
	(ui-menu-add-entry "mp_window"      "mp_window_top")
	(ui-menu-add-entry "mp_window"      "mp_window_bottom")
	(ui-menu-add-entry "mp_window"      "mp_window_2d_paint")
	(ui-menu-add-entry "mp_window"      "mp_window_new")
	(ui-menu-add-entry "mp_window"      "mp_window_reopen")
	(ui-menu-add-entry "mp_window"      "mp_fullscreen")
	(ui-submenu  "windows_load_save" )
		(ui-submenu-add-entry "windows_load_save"     "mp_layout_save")
		(ui-submenu-add-entry "windows_load_save"     "mp_layout_retrieve")
	(ui-menu-add-entry "mp_window" "windows_load_save")

;;ObjDisplay ----------------------------------------------
	(ui-menu "mp_objdisplay"
		(list 'select "mp_menu" 7)
		(list 'label_string "al_object_display_title")
		(list 'attribute_string "al_object_display_attribute")
	)
	(ui-menu-add-entry "mp_objdisplay"     "mp_display_control")
	(ui-menu-add-separator "mp_objdisplay")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_visible")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_invisible")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_toggleVisibility")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_hideunselected")

	(ui-menu-add-separator "mp_objdisplay")

	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_tgltemplate")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_tglbound")

	(ui-menu-add-separator "mp_objdisplay")

	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_curvepre")
	(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_symbology")

	(if (ui-symbol-true "aw_fod_objdisplay_simpdisp" )
		(ui-menu-add-entry "mp_objdisplay"  "mp_objdisplay_tglsimpdisp")
	)

	(ui-menu-add-separator "mp_objdisplay")
	(ui-menu-add-entry "mp_objdisplay"  "mp_diagshade_editor")
	(ui-menu-add-entry "mp_objdisplay"  "mp_diagshade_light_control")


;;Display Tools --------------------------------------------
	(ui-menu "mp_display"
		(list 'select "mp_menu" 8)
		(list 'label_string "al_display_tools_title")
		(list 'attribute_string "al_display_tools_attribute")
	)

;; Display window toggles
	(ui-menu-add-entry "mp_display" "mp_display_titlebar")
	(ui-menu-add-entry "mp_display" "mp_window_sync")
	(ui-menu-add-separator "mp_display")

	(ui-menu-add-entry "mp_display" "mp_display_shade_options")
	(ui-menu-add-entry "mp_display" "mp_display_hiddenLine")
	(ui-menu-add-separator "mp_display")

	(ui-submenu "window_antialias_sub")
		(ui-submenu-add-entry "window_antialias_sub" "mw_antialias_lines")
		(ui-submenu-add-entry "window_antialias_sub" "mw_antialias_surfaces")
	(ui-menu-add-entry "mp_display" "window_antialias_sub")

	(ui-menu-add-entry "mp_display" "mw_transparency")

	(ui-menu-add-entry "mp_display" "mw_xray_controls")

	(ui-menu-add-separator "mp_display")

	(ui-menu-add-entry "mp_display" "mw_visibility")
	(ui-submenu "window_toggles_sub")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_model")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_controls")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_pivots")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_grid")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_guidelines")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_locators")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_construction_objects")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_canvases")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_lights")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_textures")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_cameras")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_image_planes")
		(ui-submenu-add-entry "window_toggles_sub" "mw_toggle_clouds")
	(ui-menu-add-entry "mp_display" "window_toggles_sub")
;;	(ui-menu-add-entry "mp_display" "mw_toggle_nonproportional")

;;Windows --------------------------------------------------
	(ui-menu "mp_windows_menu"
		(list 'select "mp_menu" 9)
		(list 'label_string "Windows")
	)

	(ui-submenu "information_sub")
		(ui-submenu-add-entry "information_sub" "mp_info_window")
		(ui-submenu-add-entry "information_sub"	"mp_layerstats_info")
		(ui-submenu-add-entry "information_sub"	"mp_layers_category_editor")
		(ui-submenu-add-entry "information_sub" "mp_deviation_table")
		(ui-submenu-add-entry "information_sub" "mp_command_history")

	(ui-submenu "editor_sub")
		(ui-submenu-add-entry "editor_sub" "m_menu_constructionplanelister")
		(ui-submenu-add-entry "editor_sub" "m_menu_paintlayerlister")
		(ui-submenu-add-entry "editor_sub" "ma_ControlPanelEditor")
		(ui-submenu-add-entry "editor_sub" "mp_window_stage")
		(ui-submenu-add-entry "editor_sub" "mp_objmod_camera")
		(ui-submenu-add-entry "editor_sub" "mp_cross_section_manager")

;; This function is generally useless but we need it to be in some level
;; so we can copy it to creat swatches on the shelf. So we'll hide it in
;; this more obscure area.
(ui-menu-add-entry "al_special_useful" "pa_color")


	(ui-menu-add-entry "mp_windows_menu" "mp_ToolBox")
	(ui-menu-add-entry "mp_windows_menu" "mp_ToolShelf")
	(ui-menu-add-entry "mp_windows_menu"  "ma_togglecontrolpanel")
	(ui-menu-add-separator  "mp_windows_menu")
	(ui-menu-add-entry "mp_windows_menu" "information_sub")
	(ui-menu-add-entry "mp_windows_menu" "editor_sub")
	(ui-menu-add-entry "mp_windows_menu" "mp_window_objectlister")
	(ui-menu-add-entry "mp_windows_menu" "mp_ToolBookMark")




;;Grid ----------------------------------------------------
	(ui-menu "mp_grid"
		(list 'select "mp_menu" 4)
		(list 'label_string "al_grid_title")
		(list 'attribute_string "al_grid_attribute")
	)

   	(ui-menu-add-entry "mp_grid"	"mo_point_create")
	(ui-menu-add-entry "mp_grid"	"mo_lseg_create")
	(ui-menu-add-entry "mp_grid"	"mo_plane_create")


	(ui-menu-add-entry "mp_grid"    "mp_grid_setconst")
	(ui-menu-add-entry "mp_grid"    "mp_grid_tglconst")
	(ui-menu-add-entry "mp_grid"    "mp_grid_reset")

;;Animation ---------------------------------------------
	(ui-menu "ap_animwinds"
		(list 'select "ap_menu" 'A_ANIMWINDS)
		(list 'label_string "al_anim_wins_title")
		(list 'attribute_string "al_anim_wins_attribute")
	)

	(ui-submenu			  "al_edit_keyframe")
	(ui-submenu-add-entry "al_edit_keyframe"   "ap_animwinds_keyframe")
	(ui-submenu-add-entry "al_edit_keyframe"   "ap_animwinds_autokey")
	(ui-submenu-add-separator "al_edit_keyframe")
	(ui-submenu-add-entry "al_edit_keyframe"        "ap_cut_keyframes")
	(ui-submenu-add-entry "al_edit_keyframe"        "ap_copy_keyframes")
	(ui-submenu-add-entry "al_edit_keyframe"        "ap_paste_keyframes")
	(ui-submenu-add-separator "al_edit_keyframe")
	(ui-menu-add-entry "ap_animwinds"    	"al_edit_keyframe")

;; This is a submenu with animation pick functionality
 	(ui-submenu			  "anim_pick")
	(ui-submenu-add-entry "anim_pick" 		"mp_pick_joint")
	(ui-submenu-add-entry "anim_pick" 		"mp_pick_ik_handle")
	(ui-submenu-add-entry "anim_pick"    "mp_pick_sel_handle")
	(ui-submenu-add-entry "anim_pick" "mp_pick_cluster")
	(ui-submenu-add-separator "anim_pick")
	(ui-menu-add-entry "ap_animwinds"    	"anim_pick")

;; This is a submenu with animation IK functionality
	(ui-submenu			  "al_edit_ik")
	(ui-submenu-add-entry "al_edit_ik" "mp_object_tools_skeleton")
	(ui-submenu-add-separator  "al_edit_ik")
	(ui-submenu-add-entry "al_edit_ik" "mp_objmod_addikhandle")
	(ui-submenu-add-entry "al_edit_ik" "mp_objmod_setrestp")
	(ui-submenu-add-entry "al_edit_ik" "mp_objmod_assumerestp")
	(ui-submenu-add-separator  "al_edit_ik")
	(ui-submenu-add-entry "al_edit_ik"	"ap_animwinds_runik")
	(ui-submenu-add-separator  "al_edit_ik")
	(ui-submenu-add-entry 	"al_edit_ik"	"edit_ik_onoff")
	(ui-menu-add-entry "ap_animwinds" "al_edit_ik")

;; This is a submenu with animation creation functionality
	(ui-submenu			  "animation_create")
	(ui-submenu-add-entry "animation_create" "mp_sel_handle_create")
	(ui-submenu-add-entry "animation_create" "mp_objmod_create_cluster")
	(ui-submenu-add-entry "animation_create" "mp_objmod_create_set")
	(ui-submenu-add-separator  "animation_create")
	(ui-submenu-add-entry "animation_create" "ap_timetools_twarp")
	(ui-submenu-add-entry "animation_create" "ap_timetools_cycles")
	(ui-submenu-add-entry "animation_create" "ap_timetools_tscale")
	(ui-menu-add-entry "ap_animwinds" "animation_create")

;; This is a submenu with animation edit functionality
	(ui-submenu	"animation_edit")

	(ui-submenu-add-separator  "animation_edit")
	(ui-submenu-add-entry "animation_edit"        "ap_copy_channels")
	(ui-submenu-add-entry "animation_edit"        "ap_copy_skeleton")
	(ui-submenu-add-separator  "animation_edit")

	(ui-submenu-add-entry 	"animation_edit"	"edit_cstr_onoff")
	(ui-submenu-add-separator  "animation_edit")

	(ui-submenu-add-separator  "animation_edit")

	(ui-menu-add-entry "ap_animwinds" "animation_edit")

;; This is a submenu with animation editor functionality
	(ui-submenu	"animation_editors")
	(ui-submenu-add-entry "animation_editors"   "ap_animwinds_action")
	(ui-submenu-add-separator  "animation_editors")
	(ui-submenu-add-entry "animation_editors"   "ap_timetools_preview")
	(ui-submenu-add-entry "animation_editors"   "ap_animwinds_param")
	(ui-submenu-add-separator  "animation_editors")
	(ui-submenu-add-entry "animation_editors" "mp_objmod_deform")
	(ui-submenu-add-entry "animation_editors" "mp_expression_win")
	(ui-submenu-add-entry "animation_editors" "mp_objmod_skeleton")
	(ui-submenu-add-entry "animation_editors" "mp_objmod_edit_cluster")
	(ui-submenu-add-separator  "animation_editors")
	(ui-submenu-add-entry "animation_editors" "mp_set_lister")
	(ui-submenu-add-entry "animation_editors" "mp_objmod_edit_set")
	(ui-submenu-add-separator  "animation_editors")
	(ui-submenu-add-entry "animation_editors"	"mp_animstats_info")
	(ui-submenu-add-entry "animation_editors"	"mp_animinfo_info")
	(ui-menu-add-entry "ap_animwinds" "animation_editors")

;; This is a submenu with animation tool functionality
	(ui-submenu	"animation_tools")
	(ui-submenu-add-entry "animation_tools" "ap_animwinds_motion")
	(ui-submenu-add-entry "animation_tools" "ap_animwinds_keyshape")
	(ui-submenu-add-separator  "animation_tools")
	(ui-submenu-add-entry "animation_tools" "ap_timetools_poseanim")
	(ui-submenu-add-entry "animation_tools" "mp_xform_autofly")
	(ui-submenu-add-separator  "animation_tools")
	(ui-submenu-add-entry "animation_tools"		'mp_objmod_addconst)
	(ui-submenu-add-entry "animation_tools"		'mp_objmod_createconst)
	(ui-submenu-add-entry "animation_tools"		'mp_objmod_editconst)
	(ui-submenu-add-separator  "animation_tools")
	(ui-submenu-add-entry "animation_tools" "mp_object_tools_jack")
	(ui-submenu-add-separator  "animation_tools")
	(ui-submenu-add-entry "animation_tools" "mp_sel_handle_move")
	(ui-submenu-add-entry "animation_tools"  "mp_objdisplay_linestl")
	(ui-menu-add-entry "ap_animwinds" "animation_tools")

;; This is a submenu with animation display functionality
	(ui-submenu	"al_animation_show")
	(ui-submenu-add-entry "al_animation_show" "ap_timetools_frame")
	(ui-submenu-add-entry "al_animation_show"   "ap_timetools_playback")
	(ui-submenu-add-entry "al_animation_show"   "ap_timetools_slider")
	(ui-submenu-add-separator  "al_animation_show")
	(ui-submenu-add-entry "al_animation_show"     "mp_display_skeleton")
	(ui-submenu-add-entry "al_animation_show"     "mp_display_sel_handles")
	(ui-submenu-add-entry "al_animation_show"     "mp_display_ik_handles")
	(ui-submenu-add-entry "al_animation_show"     "mp_display_constraints")

	(if (ui-symbol-true "using_nt_os" )
        (begin
          (ui-submenu-add-separator  "al_animation_show")
          (ui-submenu-add-entry "al_animation_show"   "ap_timetools_flipbook")))

	(ui-menu-add-entry	  "ap_animwinds"		  "al_animation_show")

	;;	aw_fod_dynamics will be set to true if the user
	;;	wants to override the focus on design effort to remove that feature
	;;	otherwise display the menu item and no option box.
	(if (ui-symbol-true "aw_fod_dynamics" )
		(ui-menu-add-entry "ap_animwinds"	"ap_animwinds_dynamics")
	)
	(ui-menu-add-entry "ap_animwinds"	"mp_xform_turntbl")

;; Display rendering toggles - used to be in the DisplayToggles menu
;; the only tool on it is fod'd, but it doesn't really fit on the
;; WindowDisplay menu, so moving it here.
	(ui-submenu           "mp_display_render_sub")
	(ui-submenu-add-entry "mp_display_render_sub" "mp_display_particle")
	(ui-menu-add-entry    "ap_animwinds"          "mp_display_render_sub")


;;Render ---------------------------------------------------

	(ui-menu "rp_render"
		(list 'select "mp_menu" 12)
		(list 'label_string "al_rendering_title")
		(list 'attribute_string "al_rendering_attribute")
	)

	(ui-menu-add-entry "rp_render"      "rp_render_global")

;; Insert multi-lister in the rendering menu
	(ui-submenu "mlist_sub")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_all")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_picked")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_shaders")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_lights")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_glows")
	(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_particles")
	(if (ui-symbol-true "aw_fod_dynamics" )
		(begin
 			(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_forces")
 			(ui-submenu-add-entry "mlist_sub" "mp_objmod_multilist_deformations")
		)
	)
	(ui-submenu-add-separator "mlist_sub")
	(ui-submenu-add-entry "mlist_sub"  "mp_multilist_edit")
	(ui-menu-add-entry "rp_render" "mlist_sub")

	(ui-submenu "render_editors_sub")
	(ui-submenu-add-entry "render_editors_sub" "mp_objmod_render")
	(ui-submenu-add-entry "render_editors_sub" "rp_light_link")
	(ui-menu-add-entry "rp_render" "render_editors_sub")

	(ui-menu-add-separator "rp_render")

	(ui-menu-add-entry "rp_render"      "rp_direct_render")
	(ui-menu-add-entry "rp_render"      "rp_render_render")
	(ui-menu-add-entry "rp_render"      "rp_render_qtvr")
	(ui-menu-add-entry "rp_render"      "rp_render_movie")
	(ui-menu-add-entry "rp_render"    	"rp_render_shading_control")

	(ui-menu-add-separator "rp_render")

	(ui-submenu "render_occlusion_sub")
	(ui-submenu-add-entry "render_occlusion_sub" "rp_bake_occlusion")
	(ui-submenu-add-entry "render_occlusion_sub" "rp_del_occlusion")
	(ui-submenu-add-entry "render_occlusion_sub" "rp_tgl_occlusion")
	(ui-menu-add-entry "rp_render" "render_occlusion_sub")

	(ui-submenu-add-entry "rp_render" "mp_objmod_render")

;;	lights submenu
	(ui-submenu "rp_light_sub"          )
		(ui-submenu-add-entry "rp_light_sub" "rp_light_point")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_spot")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_dir")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_ambient")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_area")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_volume")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_linear")
		(ui-submenu-add-entry "rp_light_sub" "rp_light_defaults")

	(ui-menu-add-entry "rp_render"   "rp_light_sub")

   ;; Projective texture primitives submenu
    	(ui-submenu "mo_object_projprims")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projplanar")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projconcentric")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projtriplanar")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projspherical")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projball")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projcylindrical")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projcubic")
	    	(ui-submenu-add-entry "mo_object_projprims" "mp_object_projcamera")
			(ui-menu-add-entry "rp_render" "mo_object_projprims")

	;; Add place texture projection menu entry
	(ui-menu-add-entry "rp_render"		"mp_object_placeprojtxt")

;;Utilities ----------------------------------------------------
	(ui-menu "al_goto"
		(list 'select "mp_menu" 11)
		(list 'label_string "al_goto_title")
		(list 'attribute_string "al_goto_attribute")
	)

	(ui-menu-add-separator "al_goto")

   	(ui-menu-add-entry "al_goto"        "m_menu_pim")
   	(ui-menu-add-entry "al_goto"        "m_menu_manageprefs")
    (ui-menu-add-entry "al_goto"        "m_menu_appman")
    (ui-menu-add-entry "al_goto"        "m_menu_remote_control")

	(ui-submenu  "al_goto_sbd_sub" )
		(ui-submenu-add-entry "al_goto_sbd_sub" "mp_window_sbd")

		(ui-submenu-add-separator "al_goto_sbd_sub")

		(ui-submenu-add-entry "al_goto_sbd_sub"  "mp_objdisplay_comprssbd")
		(ui-submenu-add-entry "al_goto_sbd_sub"  "mp_objdisplay_expandsbd")
	(ui-menu-add-entry	"al_goto"	"al_goto_sbd_sub")

	(ui-submenu  "command_stepper_sub" )
		(ui-submenu-add-entry "command_stepper_sub" 	"ma_cs_edit")
		(ui-submenu-add-entry "command_stepper_sub"		"ma_cs_forward")
		(ui-submenu-add-entry "command_stepper_sub"		"ma_cs_backward")
		(ui-submenu-add-entry "command_stepper_sub"		"ma_cs_restart")
	(ui-menu-add-entry "al_goto"    	"command_stepper_sub")

	(ui-submenu  "licensing_sub" )
		(ui-submenu-add-entry "licensing_sub" 	"ma_license_borrow")
		(ui-submenu-add-entry "licensing_sub"	"ma_license_return")
		(ui-submenu-add-entry "licensing_sub"	"ma_license_show_info")
	(ui-menu-add-entry "al_goto"    	"licensing_sub")

   (ui-submenu  "sys_info_check_sub" )
		(ui-submenu-add-entry "sys_info_check_sub" 	"mp_window_sysinfocheck")
		(ui-submenu-add-entry "sys_info_check_sub"		"mp_window_sysinfolog")
	(ui-menu-add-entry "al_goto"    	"sys_info_check_sub")

	(ui-menu-add-entry "al_goto"        	"m_menu_studiopaint")
	(ui-menu-add-entry "al_goto"		"ma_envtools_errlog" )
	(ui-menu-add-separator "al_goto")

    (ui-menu-add-entry "al_goto"        "m_menu_script_editor")
    (ui-menu-add-entry "al_goto"    "mp_file_trace")

;;Help ----------------------------------------------------

	(ui-menu "al_help"
		(list 'select "mp_menu" 13)
		(list 'label_string "al_help_title")
		(list 'attribute_string "al_help_attribute")
	)

		(ui-menu-add-entry "al_help"        "al_online_docs")

	(ui-menu-add-separator "al_help")

		(ui-menu-add-entry "al_help"        "al_wiki_help")
		(ui-menu-add-entry "al_help"        "al_learning_movies")
		(ui-menu-add-entry "al_help"        "al_tutorials")
		(ui-menu-add-entry "al_help"        "al_whats_new_shelf")
		(ui-menu-add-entry "al_help"        "al_whats_new")
		(ui-menu-add-entry "al_help"        "al_sample_files")
		(ui-menu-add-entry "al_help"        "m_menu_cmd_search")
		(ui-menu-add-entry "al_help"        "al_function_help")
		(ui-menu-add-entry "al_help"        "al_current_tool_help")
		(ui-menu-add-entry "al_help"        "al_keymap_help")

	(ui-menu-add-separator "al_help")

		(ui-menu-add-entry "al_help"        "al_report_problem")
		(ui-menu-add-entry "al_help"        "al_suggest_feature")
		(ui-menu-add-entry "al_help"        "al_visit_ideastation")
        (ui-menu-add-entry "al_help"        "al_desktop_analytics")
		(ui-menu-add-entry "al_help"        "al_support_center")

	(ui-menu-add-separator "al_help")

		(ui-menu-add-entry "al_help"        "al_sustainable_design")
		(ui-menu-add-entry "al_help"        "al_net_community")
        (ui-menu-add-entry "al_help"        "al_app_store")
		(ui-menu-add-entry "al_help"        "al_net_store")

	(ui-menu-add-separator "al_help")

		(ui-menu-add-entry "al_help"        "ma_envtools_info")


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	(ui-menu "al_shotgun"
		(list 'select "mp_menu" 13)
		(list 'label_string "al_shotgun_title")
		(list 'attribute_string "al_shotgun_attribute")
	)
        
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;        

;;---------------------------------------------------------
;;			TOOL PALETTE SECTION
;;---------------------------------------------------------

;;Pick ----------------------------------------------------
	(ui-menu "mp_pick"
		(list 'select "mp_menu" 0)
		(list 'label_string "al_pick_title")
		(list 'attribute_string "al_pick_attribute")
	)

	(ui-menu-add-entry "mp_pick"        "mp_pick_nothing")
	(ui-submenu "point_types_sub"       )
		(ui-submenu-add-entry "point_types_sub" "mp_pick_cv")
		(ui-submenu-add-entry "point_types_sub" "mp_pick_hull")
		(ui-submenu-add-entry "point_types_sub" "mp_pick_blend_point")

	(ui-menu-add-entry "mp_pick"        "mp_pick_object")
	(ui-menu-add-entry "mp_pick"        "mp_pick_component")
	(ui-menu-add-entry "mp_pick" 		"mp_pick_template")
    (ui-menu-add-entry "mp_pick"        "mo_pick_reference")

	(ui-menu-add-entry "mp_pick" 	"mp_pick_editpt")
	(ui-menu-add-entry "mp_pick"  	"point_types_sub")

	(ui-submenu "obj_types_sub"         )
		(ui-submenu-add-entry "obj_types_sub" "mp_pick_surfcrv")
		(ui-submenu-add-entry "obj_types_sub" "mp_cloudtool_pickCloud")
		(ui-submenu-add-entry "obj_types_sub" "mp_pick_image")
		(ui-submenu-add-entry "obj_types_sub" "mp_pick_all")
		(ui-submenu-add-entry "obj_types_sub" "mo_pick_byshader")

	(ui-menu-add-entry "mp_pick"    "obj_types_sub")

	(ui-menu-add-entry  "mp_pick" "mo_pick_locator")

    (ui-menu-add-entry "mp_pick" "mo_pick_visible")
    (ui-menu-add-entry "mp_pick" "mo_pick_chain")
    (ui-menu-add-entry "mp_pick" "mo_pick_surface_chain")


;;Xform --------------------------------------------------
	(ui-menu "mp_xform"
		(list 'select "mp_menu" 1)
		(list 'label_string "al_xform_title")
		(list 'attribute_string "al_xform_attribute")
	)

;; (ui-function "mp_testFunc_m"
;;     (list 'command              "testFunc_M" )
;;     (list 'label_string         "testFunc_M")
;;     (list 'attribute_string     "TF_mom")
;;     (list 'option_function      "o_testFunc_M")
;;     (list 'symbols  'tMf_val1
;;                     'tMf_val2
;;     )
;; )
;; (ui-function "mp_testFunc"
;;     (list 'command              "testFunc" )
;;     (list 'label_string         "testFunc")
;;     (list 'attribute_string     "TF")
;;     (list 'option_function      "o_testFunc")
;;     (list 'symbols  'tf_val1
;;                     'tf_val2
;;     )
;; )
;; (ui-function "mp_testFunc2"
;;     (list 'command              "testFunc2" )
;;     (list 'label_string         "testFunc2")
;;     (list 'attribute_string     "TF2")
;;     (list 'option_function      "o_testFunc2")
;;     (list 'symbols  'tf_val1
;;                     'tf_val2
;;     )
;; )

;; (ui-menu-add-entry "mp_xform"       "mp_testFunc2")
;; (ui-menu-add-entry "mp_xform"       "mp_testFunc")
;; (ui-menu-add-entry "mp_xform"       "mp_testFunc_m")

	(ui-menu-add-entry "mp_xform"       "mp_xform_move")
	(ui-menu-add-entry "mp_xform"       "mp_xform_rotate")

	(ui-submenu "scale_types_sub"       )
;		(ui-submenu-add-entry "scale_types_sub" "mp_xform_scale")
;		(ui-submenu-add-entry "scale_types_sub" "mp_xform_npscale")
;	(ui-menu-add-entry "mp_xform"   "scale_types_sub")

	(ui-menu-add-entry "mp_xform" "mp_xform_scale")
	(ui-menu-add-entry "mp_xform" "mp_xform_npscale")
	(ui-menu-add-entry "mp_xform"       "mp_xform_transform")

    (ui-symbol "noOp_sub" 0 )
	(ui-submenu "noOp_sub")
	    (ui-submenu-add-entry "noOp_sub"       "mp_xform_noOp_tool")
	    (ui-submenu-add-entry "noOp_sub"       "mp_xform_noOp_window")
    (ui-menu-add-entry "mp_xform" "noOp_sub")

    (ui-submenu "prop_mod_types_sub")
        (ui-submenu-add-entry "prop_mod_types_sub"   "mp_xform_pmod")
        (ui-submenu-add-entry "prop_mod_types_sub"   "mp_xform_move_cv_normal")
        (ui-submenu-add-entry "prop_mod_types_sub"   "mp_xform_rot_scale")
    (ui-menu-add-entry "mp_xform" "prop_mod_types_sub")

	(ui-submenu "pivot_types_sub"       )
		(ui-submenu-add-entry "pivot_types_sub" "mp_xform_pivot")
		(ui-submenu-add-entry "pivot_types_sub" "mp_xform_center_pivot")
		(ui-submenu-add-entry "pivot_types_sub" "mp_xform_lclaxes")
	(ui-menu-add-entry "mp_xform"   "pivot_types_sub")

	(ui-menu-add-entry "mp_xform"  	"mp_objmod_zero")

    (ui-submenu "duplicate_place_sub"       )
        (ui-submenu-add-entry "duplicate_place_sub" "mp_duplicate_place_toolBox")
          (ui-submenu-add-entry "duplicate_place_sub" "mp_place_tool")
    (ui-menu-add-entry "mp_xform"  	"duplicate_place_sub")

	(ui-submenu "array_types_sub")
		(ui-submenu-add-entry "array_types_sub" "mp_xform_arraytool")
		(ui-submenu-add-entry "array_types_sub" "mp_xform_patharray")
		(ui-submenu-add-entry "array_types_sub" "mp_xform_surfacearray")
	(ui-menu-add-entry "mp_xform"   "array_types_sub")

;;Curves ------------------------------------------------
	(ui-menu "mp_crvtools"
		(list 'select "mp_menu" 3)
		(list 'label_string "al_curve_tools_title")
		(list 'attribute_string "al_curve_tools_attribute")
	)

	(ui-string "curve_create_sub" "Create")
	(ui-submenu "curve_create_sub" )
		(ui-submenu-add-entry "curve_create_sub" "mp_crvtools_dupcrv")
		(ui-submenu-add-entry "curve_create_sub"    "mp_crvtools_combinecrv")
		(ui-submenu-add-entry "curve_create_sub" "mp_crvtools_fillet")
		(ui-submenu-add-entry "curve_create_sub" "mp_crvtools_freeform_curve")
	(ui-menu-add-entry "mp_crvtools" "curve_create_sub")

	(ui-submenu "modify_types_sub"      )
		(ui-submenu-add-entry "modify_types_sub" "mp_crvtools_addpts")
		(if (ui-symbol-true "aw_fod_adjust_weight" )
			(ui-submenu-add-entry "modify_types_sub" "mp_crvtools_weight")
		)
		(if (ui-symbol-true "aw_fod_cv_multiplicity" )
			(ui-submenu-add-entry "modify_types_sub" "mp_crvtools_multiply")
		)

		(ui-submenu-add-entry 	"modify_types_sub" 	"mp_crvtools_adjint")
		(ui-submenu-add-entry 	"modify_types_sub"  "mp_crvtools_transfcrv")
		(ui-submenu-add-entry 	"modify_types_sub" 	"mp_crvtools_stretch")
	(ui-menu-add-entry "mp_crvtools" "modify_types_sub")

	(ui-submenu "mo_cut_funcs" )
		(ui-submenu-add-entry "mo_cut_funcs" "mp_crvtools_delseg")
		(ui-submenu-add-entry "mo_cut_funcs" "mo_break_infl")
	(ui-menu-add-entry "mp_crvtools" "mo_cut_funcs" )

	(ui-menu-add-entry "mp_crvtools"   	"mp_crvtools_rebuildcrv")
	(ui-menu-add-entry "mp_crvtools"    "mp_crvtools_projtan")
	(ui-menu-add-entry "mp_crvtools"  	"mp_crvtools_crvplanar")
	(ui-menu-add-entry "mp_crvtools"  	"mp_crvtools_crvsection")
	(ui-menu-add-entry "mp_crvtools"	"mp_crvtools_fitcrvtocos")
	(ui-menu-add-entry "mp_crvtools"  	"mp_crvtools_sortsections")
    (ui-menu-add-entry "mp_crvtools"    "mp_crvtools_reverse")
    (ui-menu-add-entry "mp_crvtools"    "mp_crvtools_cosfittest")


; Curve Create ----------------------------------------
  	(ui-menu "al_curvetoolbox"
       (list 'label_string        "al_crvtoolbox_title")
       (list 'attribute_string    "al_crvtoolbox_attribute")
   	)

	(ui-submenu "mo_crv_prims" )
		(ui-submenu-add-entry "mo_crv_prims" "mp_object_tools_circle")
		(ui-submenu-add-entry "mo_crv_prims" "mo_sweeps")
	(ui-menu-add-entry "al_curvetoolbox" "mo_crv_prims" )

	(ui-submenu "mo_curve_funcs" )
		(ui-submenu-add-entry "mo_curve_funcs" "mo_curve_cvs")
		(ui-submenu-add-entry "mo_curve_funcs" "mo_curve_eps")
		;;	aw_fod_curve_sketch will be set to true if the user
		;;	wants to override the focus on design effort to remove that feature
		;;	otherwise display the menu item and no option box.
		(if (ui-symbol-true "aw_fod_curve_sketch" )
			(ui-submenu-add-entry "mo_curve_funcs" "mo_curve_sketch")
		)
		(ui-submenu-add-entry "mo_curve_funcs" "mo_sketch_curve")
	(ui-menu-add-entry "al_curvetoolbox" "mo_curve_funcs" )

	(ui-menu-add-entry "al_curvetoolbox" "mp_blend_crv_toolbox" )
	(ui-menu-add-entry "al_curvetoolbox" "mp_keypoint_curve_toolbox" )

	(ui-submenu "curve_types_sub"       )
		(ui-submenu-add-entry "curve_types_sub" "mp_crvtools_newcrvsurf")
		;;	aw_fod_auto_trace will be set to true if the user
		;;	wants to override the focus on design effort to remove that feature
		;;	otherwise display the menu item and no option box.
		(if (ui-symbol-true "aw_fod_auto_trace" )
			(ui-submenu-add-entry "curve_types_sub" "mp_crvtools_autotrace")
		)

	(ui-menu-add-entry "al_curvetoolbox" "curve_types_sub")

	(ui-menu-add-entry "al_curvetoolbox"  "mp_object_tools_text")

    	(ui-menu-add-entry "al_curvetoolbox" "mo_text")


;;ObjectCreate--------------------------------------------
;;	(ui-menu "al_object_create"
;;		(list 'label_string "al_object_create_title")
;;		(list 'attribute_string "al_object_create_attribute")
;;	)

;;    (ui-submenu "mo_text" )
;;		(ui-submenu-add-entry "mo_text"   "mp_object_tools_text")
;;	(ui-menu-add-entry "al_object_create" "mo_text")

;;    (ui-submenu "mo_object_primitives" )
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_sphere")
;;      (ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_torus")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_circle")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cylinder")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cone")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cube")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_plane")
;;		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_jack")
;;	(ui-menu-add-entry "al_object_create" "mo_object_primitives")

;;	lights submenu
;;	(ui-submenu "rp_light_sub"          )
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_point")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_spot")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_dir")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_ambient")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_area")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_volume")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_linear")
;;		(ui-submenu-add-entry "rp_light_sub" "rp_light_defaults")
;;	(ui-menu-add-entry "al_object_create"   "rp_light_sub")

;;	deformation submenu
;;	(ui-submenu "rp_deform_sub"          )
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_bulge_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_twist_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_taper_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_ripple_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_rock_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_mangle_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_wave_deform")
;;		(ui-submenu-add-entry "rp_deform_sub" "rp_swirl_deform")
;;	(ui-menu-add-entry "al_object_create"   "rp_deform_sub")

    ;; Projective texture primitives submenu
;;    (ui-submenu "mo_object_projprims")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projplanar")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projconcentric")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projtriplanar")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projspherical")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projball")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projcylindrical")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projcubic")
;;	    (ui-submenu-add-entry "mo_object_projprims" "mp_object_projcamera")
;;		(ui-menu-add-entry "al_object_create" "mo_object_projprims")

;;Surfaces ----------------------------------------------
	(ui-menu "mp_buildsurf"
		(list 'select "mp_menu" 4)
		(list 'label_string "al_build_surface_title")
		(list 'attribute_string "al_build_surface_attribute")
		(list 'popup "Modeling/mo_build_surf_menu.p.scm")
	)

    	(ui-submenu "mo_object_primitives" )
		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_sphere")
        	(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_torus")
		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cylinder")
		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cone")
		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_cube")
		(ui-submenu-add-entry "mo_object_primitives" "mp_object_tools_plane")
	(ui-menu-add-entry "mp_buildsurf" "mo_object_primitives")

	(ui-submenu "planar_surf_sub")
		(ui-submenu-add-entry "planar_surf_sub" "mp_buildsurf_plansrf")
		(ui-submenu-add-entry "planar_surf_sub" "mp_buildsurf_bevel")
	(ui-menu-add-entry "mp_buildsurf"   "planar_surf_sub")

	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_revolve")

	(ui-submenu "skin_types_sub")
		(ui-submenu-add-entry "skin_types_sub" "mp_buildsurf_vsrskin")
		(ui-submenu-add-entry "skin_types_sub" "mp_buildsurf_skin")
	(ui-menu-add-entry "mp_buildsurf" "skin_types_sub")

	(ui-submenu "sweep_types_sub"       )
		(ui-submenu-add-entry "sweep_types_sub" "mp_buildsurf_rail")
		(ui-submenu-add-entry "sweep_types_sub" "mp_buildsurf_extrude")
		(ui-submenu-add-entry "sweep_types_sub" "ap_animwinds_sweep")
		(ui-submenu-add-entry "sweep_types_sub" "mp_buildsurf_profile")
	(ui-menu-add-entry "mp_buildsurf" "sweep_types_sub")

	(ui-submenu "boundary_types_sub"    )
		(ui-submenu-add-entry "boundary_types_sub" "mp_buildsurf_square")

		(if (ui-symbol-true "aw_fod_buildsurf_boundary" )
			(ui-submenu-add-entry "boundary_types_sub" "mp_buildsurf_boundary")
		)

		(ui-submenu-add-entry "boundary_types_sub" "mp_buildsurf_nsided")
		(ui-submenu-add-entry "boundary_types_sub" "mp_buildsurf_multiblend")
	(ui-menu-add-entry "mp_buildsurf" "boundary_types_sub")

	(ui-submenu "fillet_types_sub" )
		(ui-submenu-add-entry "fillet_types_sub" "mp_buildsurf_filletsrf")
		(ui-submenu-add-entry "fillet_types_sub" "mp_buildsurf_symmetric_fillet")
	(ui-menu-add-entry "mp_buildsurf" "fillet_types_sub")

	(ui-submenu "blend_types_sub" )
		(ui-submenu-add-entry "blend_types_sub" "mp_buildsurf_freeformblend")
		(ui-submenu-add-entry "blend_types_sub" "mp_buildsurf_profileblend")
		(if (ui-symbol-true "aw_fod_surface_blend" )
			(ui-submenu-add-entry "blend_types_sub" "mp_buildsurf_blendsrf")
		)
	(ui-menu-add-entry "mp_buildsurf" "blend_types_sub")

	(ui-submenu "rolled_edge_types_sub" )
		(ui-submenu-add-entry "rolled_edge_types_sub" "mp_buildsurf_filletflange")
		(ui-submenu-add-entry "rolled_edge_types_sub" "mp_buildsurf_tube")
		(ui-submenu-add-entry "rolled_edge_types_sub" "mp_object_tools_tub_offset")
		(ui-submenu-add-entry "rolled_edge_types_sub" "mp_buildsurf_panelgap")
	(ui-menu-add-entry "mp_buildsurf" "rolled_edge_types_sub")

	(ui-submenu "round_types_sub" )
		(ui-submenu-add-entry "round_types_sub" "mp_buildsurf_msf_round")
		(ui-submenu-add-entry "round_types_sub" "mp_buildsurf_roundengine")
		(if (ui-symbol-true "aw_fod_round90" )
			(ui-submenu-add-entry "round_types_sub" "mp_buildsurf_roundsrf")
		)
	(ui-menu-add-entry "mp_buildsurf" "round_types_sub")

	(ui-submenu "draft_types_sub" )
		(ui-submenu-add-entry "draft_types_sub"   "mp_buildsurf_draft")
	(ui-menu-add-entry "mp_buildsurf" "draft_types_sub")

	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_network")
	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_combine")
	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_ballcorner")
	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_tubesurface")
	(ui-menu-add-entry "mp_buildsurf"   "mp_buildsurf_autostitch")
    (ui-menu-add-entry "mp_buildsurf"	"mp_buildsurf_quicksurface")


;;ObjTools -----------------------------------------------
	(ui-menu "mp_objtools"
		(list 'select "mp_menu" 2)
		(list 'label_string "al_object_tools_title")
		(list 'attribute_string "al_object_tools_attribute")
	)

	(ui-submenu "attach_types_sub"      )
		(ui-submenu-add-entry "attach_types_sub" "mp_object_tools_attach")
		(ui-submenu-add-entry "attach_types_sub" "mp_object_tools_detach")
	(ui-menu-add-entry "mp_objtools" "attach_types_sub")

	(ui-menu-add-entry "mp_objtools"    "mp_object_tools_insert")
	(ui-menu-add-entry "mp_objtools"    "mp_object_tools_extend")
	(ui-menu-add-entry "mp_objtools" "mp_object_tools_make_symmetric")


	(ui-submenu "align_types_sub"      )
		(ui-submenu-add-entry "align_types_sub"    "mp_object_tools_align_nova")
		(ui-submenu-add-entry "align_types_sub"    "mp_object_tools_align")
		(ui-submenu-add-entry "align_types_sub"    "mp_object_tools_symalign")
	(ui-menu-add-entry "mp_objtools" "align_types_sub")

	(ui-menu-add-entry "mp_objtools"    "mp_object_tools_ch_offset")




;; Deformation toolbox start **************************************************

(ui-menu "df_tooltab"
    (list 'label_string     "df_tooltab_str" )
	(list 'attribute_string "df_tooltab_attr" )
)
(ui-level-add-menu "al_deformation_toolbox"   "df_tooltab" )

(ui-menu-add-entry "df_tooltab" "al_TransformerRig")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigFlexible")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigRigid")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigFreeModifier")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigPreDefinedModifier")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigConstraint")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigClamper")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigRemoveFromRig")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigRevert")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigCommit")
(ui-menu-add-entry "df_tooltab" "al_TransformerRigOpenPickMaskCBox")

(ui-menu "dfl_tooltab"
    (list 'label_string     "dfl_tooltab_str" )
	(list 'attribute_string "dfl_tooltab_attr" )
)
(ui-level-add-menu "al_deformation_lattice_toolbox"   "dfl_tooltab" )
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRig")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigToggleEngage")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigSplitEdge")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigSimplify")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigCenterPivot")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigClearSelection")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigConstraint")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigRevert")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigCommit")
(ui-menu-add-entry "dfl_tooltab" "al_LatticeRigOpenPickMaskCBox")

(ui-menu "dft_tooltab"
    (list 'label_string     "dft_tooltab_str" )
	(list 'attribute_string "dft_tooltab_attr" )
)
(ui-level-add-menu "al_deformation_twist_toolbox"   "dft_tooltab" )
(ui-menu-add-entry "dft_tooltab" "al_TwistRig")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigAddAngles")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigRemoveAngles")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigChangeAxisOrientation")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigReferenceOtherTwist")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigUnrefTwist")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigRevert")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigCommit")
(ui-menu-add-entry "dft_tooltab" "al_TwistRigOpenPickMaskCBox")

(ui-menu "dfb_tooltab"
    (list 'label_string     "dfb_tooltab_str" )
	(list 'attribute_string "dfb_tooltab_attr" )
)
(ui-level-add-menu "al_deformation_bend_toolbox"   "dfb_tooltab" )
(ui-menu-add-entry "dfb_tooltab" "al_BendRig")
(ui-menu-add-entry "dfb_tooltab" "al_BendChangeAxisOrientation")
(ui-menu-add-entry "dfb_tooltab" "al_BendRigRevert")
(ui-menu-add-entry "dfb_tooltab" "al_BendRigCommit")
(ui-menu-add-entry "dfb_tooltab" "al_BendRigOpenPickMaskCBox")

(ui-menu "dfc_tooltab"
    (list 'label_string     "dfc_tooltab_str" )
	(list 'attribute_string "dfc_tooltab_attr" )
)
(ui-level-add-menu "al_deformation_conform_toolbox"   "dfc_tooltab" )
(ui-menu-add-entry "dfc_tooltab" "al_ConformRig")
(ui-menu-add-entry "dfc_tooltab" "al_ConformRigChangeContactPoint")
(ui-menu-add-entry "dfc_tooltab" "al_ConformRigRevert")
(ui-menu-add-entry "dfc_tooltab" "al_ConformRigCommit")
(ui-menu-add-entry "dfc_tooltab" "al_ConformRigOpenPickMaskCBox")

(ui-menu "dffs_tooltab"
    (list 'label_string     "dffs_tooltab_str" )
	(list 'attribute_string "dffs_tooltab_attr" )
)
(ui-level-add-menu "al_feature_snap_toolbox"   "dffs_tooltab" )
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnap")
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnapRevert")
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnapCommit")
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnapPickPNormal")
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnapClearPNormal")
(ui-menu-add-entry "dffs_tooltab" "al_FeatureSnapOpenPickMaskCBox")

(ui-menu "dffp_tooltab"
    (list 'label_string     "dffp_tooltab_str" )
	(list 'attribute_string "dffp_tooltab_attr" )
)
(ui-level-add-menu "al_duplicate_place_toolbox"   "dffp_tooltab" )
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlace")
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlaceRevert")
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlaceCommit")
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlacePickPNormal")
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlaceClearPNormal")
(ui-menu-add-entry "dffp_tooltab" "al_DuplicatePlaceOpenPickMaskCBox")

(ui-submenu	"mp_deformation_sub")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_deform_toolBox")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_deform_lattice_toolBox")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_deform_twist_toolBox")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_deform_bend_toolBox")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_deform_conform_toolBox")
(ui-submenu-add-entry "mp_deformation_sub"       "mp_feature_snap_toolBox")

(ui-menu-add-entry	"mp_objtools"		"mp_deformation_sub")

;; The rest of the ObjectEdit tools

	(ui-menu-add-entry "mp_objtools"	"mp_object_tools_objecteditor")
	(ui-menu-add-entry "mp_objtools"    "mp_object_tools_smooth")
	(ui-menu-add-entry "mp_objtools"    "mp_object_tools_close")

	(if (ui-symbol-true "aw_fod_tools_bspline")
		(ui-menu-add-entry "mp_objtools" "mp_object_tools_bspline")
	)

	(if (not (ui-symbol-true "using_nt_os" ))
		(ui-menu-add-entry "mp_objtools"  	"mp_objmod_ultra_64")
	)
	(ui-menu-add-entry "mp_objtools"    "mp_objmod_comment")
	(ui-menu-add-entry "mp_objtools"  "mp_objdisplay_patchpre")

	(ui-menu-add-entry "mp_objtools"  "mp_multilist_edit")
	(ui-menu-add-entry "mp_objtools"  "mp_query_geom")
	(ui-menu-add-entry "mp_objtools"  "mp_object_tools_vsrsmooth")

;;Sid Paint tools ----------------------------------------------------
		;; define the default paint tool selection
		(ui-symbol "mp_paint"                   0)
	;; define the items inside the paint tool tab
	(ui-menu "mp_paint"
;;				(list 'select "mp_menu" 3)
		(list 'label_string "al_paint_title")
		(list 'attribute_string "al_paint_attribute")
	)

	(ui-submenu "mp_paint_pencil_sub"      )
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_default")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_round")

	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_black")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_white")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_red")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_blue")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_green")
	(ui-submenu-add-entry "mp_paint_pencil_sub" "mp_paint_pencil_2B_yellow")

	(ui-menu-add-entry "mp_paint" "mp_paint_pencil_sub" )

	(ui-submenu "mp_paint_marker_sub"      )
	(ui-submenu-add-entry "mp_paint_marker_sub"    "mp_paint_marker_ink")
	(ui-submenu-add-entry "mp_paint_marker_sub"    "mp_paint_marker_fine")
	(ui-submenu-add-entry "mp_paint_marker_sub"    "mp_paint_marker_broad")
	(ui-menu-add-entry "mp_paint" "mp_paint_marker_sub")

	(ui-submenu "mp_paint_airbrush_sub"      )
	(ui-submenu-add-entry "mp_paint_airbrush_sub"    "mp_paint_airbrush_soft")
	(ui-submenu-add-entry "mp_paint_airbrush_sub"    "mp_paint_airbrush_med2")
	(ui-menu-add-entry "mp_paint" "mp_paint_airbrush_sub")

	(ui-submenu "mp_paint_pastel_sub"      )
	(ui-submenu-add-entry "mp_paint_pastel_sub"    "mp_paint_pastel_soft")
	(ui-menu-add-entry "mp_paint" "mp_paint_pastel_sub")

	(ui-submenu "mp_paint_solidbrush_sub"      )
	(ui-submenu-add-entry "mp_paint_solidbrush_sub"    "mp_paint_solidbrush_felt")
	(ui-submenu-add-entry "mp_paint_solidbrush_sub"    "mp_paint_solidbrush_large2")
	(ui-menu-add-entry "mp_paint" "mp_paint_solidbrush_sub")

	(ui-submenu "mp_paint_eraser_sub"      )
	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_softbrush")
	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_hardbrush")
	(ui-submenu-add-entry "mp_paint_eraser_sub" "m_menu_paintclearimage")

	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_solidbrush_fine")
	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_solidbrush_small")
	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_solidbrush_medium")
	(ui-submenu-add-entry "mp_paint_eraser_sub" "mp_paint_eraser_solidbrush_large")


	(ui-menu-add-entry "mp_paint" "mp_paint_eraser_sub" )

	(ui-submenu "mp_paint_effectbrush_sub"      )
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_sharpenbrush")
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_blurbrush")
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_smearbrush")
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_clonebrush")
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_dodgebrush")
	(ui-submenu-add-entry "mp_paint_effectbrush_sub"    "mp_paint_burnbrush")
	(ui-menu-add-entry "mp_paint" "mp_paint_effectbrush_sub")

	(ui-menu-add-entry "mp_paint" "mp_paint_floodfill" )

	(ui-menu-add-entry "mp_paint" "mp_paint_picklayer")

	(ui-submenu "mp_paint_select_sub"      )
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_magicwand" )
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_poly")
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_lasso")
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_rect")
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_circle")
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_ellipse")
	(ui-submenu-add-entry "mp_paint_select_sub" "m_menu_tglselectionmask")
	(ui-submenu-add-entry "mp_paint_select_sub" "m_menu_paintinvertselmask")
	(ui-submenu-add-entry "mp_paint_select_sub" "m_menu_paintclearselection")
	(ui-submenu-add-entry "mp_paint_select_sub" "mp_paint_marquee_transform" )
	(ui-menu-add-entry "mp_paint" "mp_paint_select_sub" )

	(ui-submenu "mp_paint_makeshape_sub" )
	(ui-submenu-add-entry "mp_paint_makeshape_sub" "mp_paint_makeshapeoutline")
	(ui-submenu-add-entry "mp_paint_makeshape_sub" "mp_paint_makeshape_mask")
	(ui-submenu-add-entry "mp_paint_makeshape_sub" "mp_paint_makeshape_stencil")

	(ui-menu-add-entry "mp_paint" "mp_paint_makeshape_sub")

	(ui-submenu "mp_paint_textImage_sub"      )
	(ui-submenu-add-entry "mp_paint_textImage_sub" "mp_paint_textImage")
	(ui-menu-add-entry "mp_paint" "mp_paint_textImage_sub" )

	(ui-submenu "mp_paint_symmetry_sub" )
	(ui-submenu-add-entry "mp_paint_symmetry_sub" "mp_paint_symmetry")
	(ui-submenu-add-entry "mp_paint_symmetry_sub" "mp_paint_symmetry_toggle")
	(ui-menu-add-entry "mp_paint" "mp_paint_symmetry_sub" )

	(ui-submenu "mp_paint_color_sub"      )
	(ui-submenu-add-entry "mp_paint_color_sub" "m_menu_coloreditor")
	(ui-menu-add-entry "mp_paint" "mp_paint_color_sub" )

;; End of new image tool bar section

	(ui-submenu "mp_paint_text_sub"      )
	(ui-submenu-add-entry "mp_paint_text_sub" "mp_paint_textImage")
	(ui-menu-add-entry "mp_paint" "mp_paint_text_sub" )


;;SurfTools----------------------------------------------
	(ui-menu "mp_srftools"
		(list 'select "mp_menu" 6)
		(list 'label_string "al_surface_tools_title")
		(list 'attribute_string "al_surface_tools_attribute")
	)

	(ui-submenu "create_COS_types_sub"  )
		(ui-submenu-add-entry "create_COS_types_sub" "mp_srftools_project")
		(ui-submenu-add-entry "create_COS_types_sub" "mp_srftools_intersect")
		(ui-submenu-add-entry "create_COS_types_sub" "mp_srftools_geomap")
	(ui-menu-add-entry "mp_srftools" "create_COS_types_sub")

	(ui-submenu "trim_types_sub"        )
		(ui-submenu-add-entry "trim_types_sub" "mp_srftools_trim_tool")
		(ui-submenu-add-entry "trim_types_sub" "mp_srftools_trim")
		(ui-submenu-add-entry "trim_types_sub" "mp_srftools_trimdiv")
		(ui-submenu-add-entry "trim_types_sub" "mp_srftools_untrim")
		(ui-submenu-add-entry "trim_types_sub" "mp_srftools_trim_convert")
	(ui-menu-add-entry "mp_srftools" "trim_types_sub")

	(ui-submenu "stitch_types_sub"      )
		(ui-submenu-add-entry "stitch_types_sub" "mp_srftools_sh_stitch")
		(ui-submenu-add-entry "stitch_types_sub" "mp_srftools_sh_unstitch")
	(ui-menu-add-entry "mp_srftools" "stitch_types_sub")

	(ui-submenu "solid_types_sub"       )
			(ui-submenu-add-entry "solid_types_sub" "mp_srftools_sh_subtract")
			(ui-submenu-add-entry "solid_types_sub" "mp_srftools_sh_intersect")
			(ui-submenu-add-entry "solid_types_sub" "mp_srftools_sh_union")
;;  	    (ui-submenu-add-entry "solid_types_sub" "mp_srftools_sh_rebuild")
	(ui-menu-add-entry "mp_srftools" "solid_types_sub")

	(if (ui-symbol-true "aw_fod_srftools_alignmesh" )
		(ui-menu-add-entry "mp_srftools"  "mp_srftools_alignmsh")
	)

    (ui-menu-add-entry "mp_srftools"    "mp_srftools_alignhull")
	(ui-menu-add-entry "mp_srftools"    "mp_srftools_hullplanarize")
	(ui-menu-add-entry "mp_srftools"    "mp_srftools_rebuild")
	(ui-menu-add-entry "mp_srftools"    "mp_srftools_claymate")
	(if (ui-symbol-true "aw_fod_global_deformation" )
    	(ui-menu-add-entry "mp_srftools"    "mp_defSpace")
	)

	(ui-menu-add-entry "mp_srftools"    "mp_srftools_fitscan")
	(ui-menu-add-entry "mp_srftools"    "mp_srftools_newfitscan")
    (ui-menu-add-entry "mp_srftools"	"mp_srftools_refitsurfaces") 
	(ui-menu-add-entry "mp_srftools"    "mp_srftools_srf_align")

;	(ui-submenu "vector_types_sub"      )
;		(ui-submenu-add-entry "vector_types_sub" "mp_srftools_movevect")
;		(ui-submenu-add-entry "vector_types_sub" "mp_srftools_winvect")
;	(ui-menu-add-entry "mp_srftools" "vector_types_sub")

	(ui-submenu "normal_tools")
		(ui-submenu-add-entry "normal_tools"  "mp_objmod_orient_visual_normals")
		(ui-submenu-add-entry "normal_tools"  "mp_objmod_orient_geometric_normals")
		(ui-submenu-add-entry "normal_tools"  "mp_objmod_unifynormals")
		(ui-submenu-add-entry "normal_tools"  "mp_srftools_reverse_normal")
		(ui-submenu-add-entry "normal_tools"  "mp_srftools_reverse_uv")
	(ui-menu-add-entry "mp_srftools"	"normal_tools")

	(ui-menu-add-entry "mp_srftools"  	"mp_srftools_nurbstobez")

;; Mesh Tools -------------------------------------------------

    (ui-string "al_mesh_title_str" "Mesh")
    (ui-string "al_mesh_attribute_str" "mesh")
	(ui-menu "al_mesh"
		(list 'label_string "al_mesh_title_str")
		(list 'attribute_string "al_mesh_attribute_str")
	)


	; strings for the submenus
    (ui-string "al_mesh_tess_sub"               "Mesh Tessellation")
	(ui-string "al_mesh_curves_sub"				"Mesh Curves")
	(ui-string "al_mesh_partitioning_sub"		"Mesh Partitioning")
	(ui-string "al_mesh_cleanup_sub"			"Mesh Cleanup")

    ; all the mesh tools now...here we go
    (ui-submenu "al_mesh_tess_sub")
        (ui-submenu-add-entry "al_mesh_tess_sub" "al_mesh_NurbsToMesh")
        (ui-submenu-add-entry "al_mesh_tess_sub" "al_mesh_CloudToMesh")
        (ui-submenu-add-entry "al_mesh_tess_sub" "al_mesh_DispMapToMesh")
    (ui-menu-add-entry "al_mesh" "al_mesh_tess_sub")

    (ui-submenu "al_mesh_partitioning_sub")
		(ui-submenu-add-entry "al_mesh_partitioning_sub" "al_mesh_MeshSubset")
		(ui-submenu-add-entry "al_mesh_partitioning_sub" "al_mesh_MeshMerge")
		(ui-submenu-add-entry "al_mesh_partitioning_sub" "al_mesh_MeshCut")
	(ui-menu-add-entry "al_mesh" "al_mesh_partitioning_sub")

	(ui-submenu "al_mesh_curves_sub")
        (ui-submenu-add-entry "al_mesh_curves_sub" "al_mesh_MeshProjectCurve")
        (ui-submenu-add-entry "al_mesh_curves_sub" "al_mesh_MeshProjectNormal")
        (ui-submenu-add-entry "al_mesh_curves_sub" "al_mesh_MeshIntersect")
		(ui-submenu-add-entry "al_mesh_curves_sub" "al_mesh_MeshFeatureCurves")
        (ui-submenu-add-entry "al_mesh_curves_sub" "al_mesh_MeshBoundaries")
    (ui-menu-add-entry "al_mesh" "al_mesh_curves_sub")

    (ui-submenu "al_mesh_cleanup_sub")
		(ui-submenu-add-entry "al_mesh_cleanup_sub" "al_mesh_MeshSmooth")
		(ui-submenu-add-entry "al_mesh_cleanup_sub" "al_mesh_MeshReduce")
		(ui-submenu-add-entry "al_mesh_cleanup_sub" "al_mesh_MeshHoleFill")
		(ui-submenu-add-entry "al_mesh_cleanup_sub" "al_mesh_MeshBridge")
		(ui-submenu-add-entry "al_mesh_cleanup_sub" "al_mesh_MeshMergeVertices")
	(ui-menu-add-entry "al_mesh" "al_mesh_cleanup_sub")

	(ui-menu-add-entry "al_mesh" "al_mesh_MeshRepair")

    (ui-menu-add-entry "al_mesh" "al_mesh_MeshCollar")

    (ui-menu-add-entry "al_mesh" "al_mesh_MeshOffset")
    (ui-menu-add-entry "al_mesh" "al_mesh_MeshStitch")

    (ui-menu-add-entry "al_mesh" "al_mesh_MeshReverseNormals")

    (ui-menu-add-entry "al_mesh" "al_mesh_MeshFlatten")

    (ui-menu-add-entry "al_mesh" "al_mesh_MeshAlignment")
    (ui-menu-add-entry "al_mesh" "al_mesh_MeshSharpen")
    (ui-menu-add-entry "al_mesh" "al_mesh_MeshPatch")

;;Cameras Control (Views)-------------------------------------------------
	(ui-menu "mp_views"
		(list 'select "mp_menu" 5)
		(list 'label_string "al_cameras_title")
		(list 'attribute_string "al_cameras_attribute")
	)

	(ui-submenu "camera_world_movements_types_sub" )
		(ui-submenu-add-entry "camera_world_movements_types_sub" "mp_views_tumble")
		(ui-submenu-add-entry "camera_world_movements_types_sub" "mp_views_track")
		(ui-submenu-add-entry "camera_world_movements_types_sub" "mp_views_dolly")
		(ui-submenu-add-entry "camera_world_movements_types_sub" "mp_views_multiview")
	(ui-menu-add-entry "mp_views"   "camera_world_movements_types_sub")

	(ui-submenu "camera_local_movements_types_sub" )
		(ui-submenu-add-entry "camera_local_movements_types_sub" "mp_views_twist")
		(ui-submenu-add-entry "camera_local_movements_types_sub" "mp_views_elevation")
		(ui-submenu-add-entry "camera_local_movements_types_sub" "mp_views_pitch")
	(ui-menu-add-entry "mp_views"	"camera_local_movements_types_sub")

	(ui-menu-add-entry "mp_views"      "mp_views_zoom")
	(ui-menu-add-entry "mp_views"      "mp_views_look")
	(ui-menu-add-entry "mp_views"      "mp_views_set_nonproportional")
	(ui-menu-add-entry "mp_views"      "mp_views_toggle_nonproportional")
	(ui-menu-add-entry "mp_views"      "mp_views_previous")
	(ui-menu-add-entry "mp_views"      "mp_views_reset")
    (ui-menu-add-entry "mp_views"	   "mp_views_tglStereo")
    (ui-menu-add-entry "mp_views"	   "mp_tgl_lens_style")


	(ui-menu-add-entry 	"mp_views"      	"mp_views_camera")
;;	(ui-menu-add-entry 	"mp_views"      	"mp_window_clone")


	(ui-menu-add-entry "mp_views"      "mp_window_clip")
	(ui-menu-add-entry "mp_views"      "mp_match_3point")

	(ui-submenu "one2one_sub" )
		(ui-submenu-add-entry "one2one_sub" "mp_one2one_calibrate")
		(ui-submenu-add-entry "one2one_sub" "mp_one2one_toggle")
	(ui-menu-add-entry "mp_views" "one2one_sub")
	(ui-menu-add-entry "mp_views" "mp_views_view_flip")
	(ui-menu-add-entry "mp_views" "mp_views_view_both")

;;Locators----------------------------------------------
	(ui-menu "al_locate"
		(list 'label_string 	"al_locate_title")
		(list 'attribute_string "al_locate_attribute")
	)

	(ui-menu-add-entry  "al_locate" "mo_move_locator")
	(ui-menu-add-entry  "al_locate" "mo_locator_annotate")

	(ui-submenu			"al_locate_measurement_sub" )
		(ui-submenu-add-entry  "al_locate_measurement_sub" 	"mo_locator_dist")
		(ui-submenu-add-entry  "al_locate_measurement_sub" 	"mo_locator_angle")
		(ui-submenu-add-entry  "al_locate_measurement_sub" 	"mo_locator_radius")
		(ui-submenu-add-entry  "al_locate_measurement_sub" 	"mo_locator_diameter")
		(ui-submenu-add-entry  "al_locate_measurement_sub"    	"mp_evaltool_arclength")
	(ui-menu-add-entry  "al_locate" "al_locate_measurement_sub")

	(ui-submenu 	"al_locate_deviation_sub" )
        (ui-submenu-add-entry  "al_locate_deviation_sub" "mo_locator_closest_point")


		(ui-submenu-add-entry  "al_locate_deviation_sub" "mo_locator_deviation")

		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_minmax_deviation)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_minmax_srf_srf_deviation)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_minmax_crv_srf_deviation)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_minmax_mesh_srf_deviation)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
							            		"mo_locator_cloud_minmax")
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_min_distance)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_measure_to_plane)
		(ui-submenu-add-entry  "al_locate_deviation_sub"
										'mo_locator_angular_deviation)
	(ui-menu-add-entry  "al_locate" "al_locate_deviation_sub")

;    obsolete
;    (ui-menu-add-entry  "al_locate" "mo_locator_curveprop")
    (ui-menu-add-entry  "al_locate" "mo_locator_curvecurvature")


;;EvalTools----------------------------------------------
	(ui-menu "mp_evaltool"
		(list 'select "mp_menu" 14)
		(list 'label_string "al_evaluation_tools_title")
		(list 'attribute_string "al_evaluation_tools_attribute")
	)

;;	(ui-menu-add-entry "mp_evaltool"    "mp_evaltool_tglcrvcrv")


	(ui-submenu "curvature_sub"         )
		(ui-submenu-add-entry "curvature_sub" "mp_evaltool_srfcont")
		(ui-submenu-add-entry "curvature_sub" "mp_evaltool_crvcont")
	(ui-menu-add-entry "mp_evaltool" "curvature_sub")

    (ui-submenu "surf_eval_sub"         )
        (ui-submenu-add-entry "surf_eval_sub" "mp_evaltool_highlights")
        (ui-submenu-add-entry "surf_eval_sub" "mp_evaltool_curvature")
        (ui-submenu-add-entry "surf_eval_sub" "mp_evaltool_contour")
        (ui-submenu-add-entry "surf_eval_sub" "mp_evaltool_horizon")
    (ui-menu-add-entry "mp_evaltool" "surf_eval_sub")

	(ui-menu-add-entry "mp_evaltool"    "mp_evaltool_dyn_xsect")
    (ui-menu-add-entry "mp_evaltool"    "mp_evaltool_light_tunnel")

	(ui-submenu "surf_curv_sub"         )
		(ui-submenu-add-entry "surf_curv_sub" "mp_evaltool_surfcrv")
		(ui-submenu-add-entry "surf_curv_sub" "mp_evaltool_scrvparam")
	(ui-menu-add-entry "mp_evaltool" "surf_curv_sub")

	(ui-submenu "highlight_sub"         )
		(ui-submenu-add-entry "highlight_sub" "mp_evaltool_highlight")
		(ui-submenu-add-entry "highlight_sub" "mp_evaltool_highparam")
	(ui-menu-add-entry "mp_evaltool" "highlight_sub")

	(ui-menu-add-entry "mp_evaltool"    "mp_evaltool_minmaxcrv")

	;;	aw_fod_mass_prop will be set to true if the user
	;;	wants to override the focus on design effort to remove that feature
	;;	otherwise display the menu item and no option box.
	(if (ui-symbol-true "aw_fod_mass_prop" )
;		(ui-menu-add-entry "mp_evaltool"    "mp_evaltool_mass")
		(ui-menu-add-entry "mp_evaltool"	"mp_evaltool_mass_new")

	)


	; Model Check tool.  Will be moved later.
	(ui-menu-add-entry "mp_evaltool"      "mp_check_model")

	; Deviation Map tool.
	(ui-menu-add-entry "mp_evaltool" "mp_evaltool_deviation")

	; Contact Analysis tool.
	(ui-menu-add-entry "mp_evaltool" "mp_evaltool_contactanalysis")

	; Dynamic Measurement tool
	(ui-menu-add-entry "mp_evaltool" "mp_evaltool_dynamicmeasurement")

	; Pedestrian Protection tool.
	(ui-menu-add-entry "mp_evaltool" "mp_evaltool_pedestrian_protection")

	; Live Scan tool.
	(ui-menu-add-entry "mp_evaltool" "mp_evaltool_livescan")

;;SID Image Tools ------------------------------------------
	(ui-menu "sid_imagetools"
		(list 'select "mp_menu" 15)
		(list 'label_string "al_sid_image_tools_title")
		(list 'attribute_string "al_sid_image_tools_attribute")
	)

	(ui-menu-add-entry "sid_imagetools"	 "m_menu_newcanvas" )
    (ui-menu-add-entry "sid_imagetools"  "m_menu_addpaint")
    (ui-menu-add-entry "sid_imagetools"  "m_menu_newoverlay")

	(ui-menu-add-separator "sid_imagetools")

    (ui-menu-add-entry "sid_imagetools" "m_menu_resize_canvas")
    (ui-menu-add-entry "sid_imagetools" "m_menu_cropcanvas")
	(ui-menu-add-separator "sid_imagetools")

    (ui-menu-add-entry "sid_imagetools"     "rp_render_sketch")

;;Effects --------------------------------------------------


	(ui-string "al_effects_tools_title" "Paint Edit")
	(ui-string "al_effects_tools_attribute" "paint edit")

	(ui-string "al_effects_transform_sub"	"Modify Layer")
	(ui-string "al_effects_color_correct_sub" "Color Correction")
	(ui-string "al_effects_layer_effect_sub" "Layer Effect")
	(ui-string "al_effects_layer_op_sub" "Layer Operation")

	(ui-menu "mp_effects_menu"
		(list 'select "mp_menu" 44)
		(list 'label_string "al_effects_tools_title")
		(list 'attribute_string "al_effects_tools_attribute")
	)

	(ui-submenu		"al_effects_transform_sub")
		(ui-submenu-add-entry "al_effects_transform_sub" "mp_paint_image_transform" )
		(ui-submenu-add-entry "al_effects_transform_sub" "m_paint_h_flip_layer")
		(ui-submenu-add-entry "al_effects_transform_sub" "m_paint_v_flip_layer")
	(ui-menu-add-entry	"mp_effects_menu"	"al_effects_transform_sub")

	(ui-menu-add-entry "mp_effects_menu" "mp_paint_image_deform" )
	(ui-menu-add-entry "mp_effects_menu" "mp_paint_makeshape_warp")

	(ui-menu-add-separator "mp_effects_menu")

	(ui-submenu		"al_effects_color_correct_sub")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_image_color_editor" )
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_bri_ctr_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_sat_val_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "m_paint_dodge_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "m_paint_burn_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_colorbalance_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_colorreplace_layer")
		(ui-submenu-add-entry "al_effects_color_correct_sub" "mp_paint_colorreplace_hsl_layer")
	(ui-menu-add-entry	"mp_effects_menu"	"al_effects_color_correct_sub")


	(ui-menu-add-entry "mp_effects_menu" "sid_imagetools_coloradjust")
	(ui-menu-add-separator "mp_effects_menu")

	(ui-submenu		"al_effects_layer_effect_sub")
		(ui-submenu-add-entry "al_effects_layer_effect_sub" "m_paint_sharpen_layer")
		(ui-submenu-add-entry "al_effects_layer_effect_sub" "m_paint_blur_layer")
	(ui-menu-add-entry	"mp_effects_menu"	"al_effects_layer_effect_sub")

	(ui-submenu		"al_effects_layer_op_sub")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_newlayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_newmasklayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_newstencillayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_newlayerfolder")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_duplicatelayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_mergelayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_mergevisiblelayer")
		(ui-submenu-add-entry "al_effects_layer_op_sub" "m_menu_mergealllayers")

	(ui-menu-add-entry	"mp_effects_menu"	"al_effects_layer_op_sub")



;;PtCloud Tools----------------------------------------------
	(ui-menu "al_cloudtoolbox"
	        (list 'label_string     'al_cloud_tools_title)
		(list 'attribute_string 'al_cloud_tools_attribute)
        )
	(ui-menu-add-entry "al_cloudtoolbox" 'mp_cloudtool_pickBox)

; Curve menu
;    (ui-submenu "cloud_crv_sub")
;        (ui-submenu-add-entry "cloud_crv_sub" 'mp_cloudtool_crvProject)
;	(ui-menu-add-entry "al_cloudtoolbox" 'cloud_crv_sub)
    (ui-menu-add-entry "al_cloudtoolbox" 'mp_cloudtool_crvProject)

; Surf menu
    (ui-submenu "cloud_surf_sub")
            (ui-submenu-add-entry "cloud_surf_sub" 'mp_cloudtool_quick_surfs)
            (ui-submenu-add-entry "cloud_surf_sub" 'mp_cloudtool_create_surfs)
            (ui-submenu-add-entry "cloud_surf_sub" 'mp_cloudtool_create_surfsCorners)
	(ui-menu-add-entry "al_cloudtoolbox" 'cloud_surf_sub)
	(ui-menu-add-entry "al_cloudtoolbox" 'mp_cloudtool_mergeClouds)
	(ui-menu-add-entry "al_cloudtoolbox" 'mp_cloudtool_tesselate)

;;Preferences -------------------------------------------------
	(ui-menu "al_envtools"
		(list 'select           "ma_menu" 'M_ENVTOOLS)
		(list 'label_string     "al_envtools_title")
		(list 'attribute_string "al_envtools_attribute")
	)

 	(ui-submenu "al_workflow"
		(list 'available (ui-eq "workflows_available" #t))
	)
	(ui-menu-add-entry "al_envtools"    "al_workflow")

	(ui-submenu  "interface_sub" )
		(ui-submenu-add-entry "interface_sub"  "ma_envtools_hotkeys")
		(ui-submenu-add-entry "interface_sub"  "ma_envtools_clutchkeys")
		(ui-submenu-add-entry "interface_sub"    "ma_mmedit_window")
		(ui-submenu-add-entry "interface_sub"  "ma_envtools_shotkeys")
		(ui-submenu-add-entry "interface_sub"  "ma_envtools_tile")
		(ui-submenu-add-entry "interface_sub"    "ma_extras_window")
		(ui-submenu-add-entry "interface_sub"  "ma_envtools_colors")

	(ui-submenu "menu_sub" )
		(ui-submenu-add-entry "menu_sub"    "m_menu_short")
		(ui-submenu-add-entry "menu_sub"    "m_menu_long")
	(ui-menu-add-entry "al_envtools"    "menu_sub")
	(ui-menu-add-entry "al_envtools"    "interface_sub")

	(ui-menu-add-separator	"al_envtools")

	(ui-menu-add-entry "al_envtools"    "ma_envtools_config")

	(ui-menu-add-entry "al_envtools"    "ma_envtools_selection")

	(ui-menu-add-entry "al_envtools" 	"mp_objmod_update")
	(ui-menu-add-entry "al_envtools"    "mp_construction_options")
	(ui-menu-add-separator	"al_envtools")

;;	(ui-submenu  "user_options_sub" )
;;		(ui-submenu-add-entry "user_options_sub"    "ma_save_opt_restore")
;;		(ui-submenu-add-entry "user_options_sub"    "ma_save_opt_save")

;;	(ui-menu-add-entry "al_envtools"    "user_options_sub")

	(ui-submenu  "prefs_sub" )
	    (ui-submenu-add-entry "prefs_sub"  "ma_envtools_savepref")
	    (ui-submenu-add-entry "prefs_sub"  "ma_envtools_importprefset")
	    (ui-submenu-add-entry "prefs_sub"  "ma_envtools_exportprefset")


	(ui-menu-add-entry "al_envtools"    "prefs_sub")


;;Layers ---------------------------------------------------
	(ui-menu "ma_layers"
		(list 'select           "ma_menu" '0)
		(list 'label_string     "ma_layers_title")
		(list 'attribute_string "ma_layers_attribute")
	)

	(ui-submenu  "layer_select" )
		(ui-submenu-add-entry "layer_select"    "ma_layerpickobjects")
		(ui-submenu-add-entry "layer_select"    "ma_layerselbyobj")
		(ui-submenu-add-entry "layer_select"    "ma_layerselall")
		(ui-submenu-add-entry "layer_select"    "ma_layerselrange")
	(ui-menu-add-separator "ma_layers")

	(ui-submenu  "layer_states" )
		(ui-submenu-add-entry "layer_states"    "ma_layersetpickable")
		(ui-submenu-add-entry "layer_states"    "ma_layersetsnapable")
		(ui-submenu-add-entry "layer_states"    "ma_layersetinactive")

	(ui-submenu  "layer_delete" )
		(ui-submenu-add-entry "layer_delete"    "ma_layerdelete")
		(ui-submenu-add-entry "layer_delete"    "ma_layerdelunassigned")
		(ui-submenu-add-entry "layer_delete"    "ma_layerdelduplicate")

	(ui-submenu  "layer_visibility" )
		(ui-submenu-add-entry "layer_visibility"    "ma_layermakevisible")
		(ui-submenu-add-entry "layer_visibility"    "ma_layermakeinvisible")

	(ui-submenu  "layer_symmetric" )
		(ui-submenu-add-entry "layer_symmetric"    "ma_layermakesymmetric")
		(ui-submenu-add-entry "layer_symmetric"    "ma_layermakeunsymmetric")
		(ui-submenu-add-entry "layer_symmetric"    "ma_layersetsymmplane")
		(ui-submenu-add-entry "layer_symmetric"    "ma_layercreatesymmgeometry")

	(ui-submenu  "layer_jtmrg_symmetric" )
		(ui-submenu-add-entry "layer_jtmrg_symmetric"    "ma_layerjtmrgsymmgeometry")
		(ui-submenu-add-entry "layer_jtmrg_symmetric"    "ma_layerjtunmrgsymmgeometry")

;;		(ui-submenu  "layer_animatibility" )
;;			(ui-submenu-add-entry "layer_animatibility"    "ma_layeranimon")
;;			(ui-submenu-add-entry "layer_animatibility"    "ma_layeranimoff")


	(ui-menu-add-entry "ma_layers"    "ma_layernew")
	(ui-menu-add-entry "ma_layers"    "ma_layernew_folder")
	(ui-menu-add-entry "ma_layers"    "layer_select")
	(ui-menu-add-entry "ma_layers"    "layer_states")
	(ui-menu-add-entry "ma_layers"    "layer_delete")
	(ui-menu-add-entry "ma_layers"    "layer_visibility")
	(ui-menu-add-entry "ma_layers"    "layer_symmetric")
	(if (ui-symbol-true "aw_want_GM_jtopen" )
		(ui-menu-add-entry "ma_layers"    "layer_jtmrg_symmetric")
	)

;;
;;	THESE HAVE BEEN REMOVED IN BLACKSHEEP.
;;
;;	(ui-menu-add-entry "ma_layers"    "layer_animatibility")
;;	(ui-menu-add-entry "ma_layers"    "ma_layersetconstruct")
;;	(ui-menu-add-entry "ma_layers"    "ma_layerassign")
    (ui-menu-add-entry "ma_layers"    "ma_layerrandomcolor")

	(ui-menu-add-entry "ma_layers"    "ma_layerundo")
	(ui-menu-add-separator "ma_layers")
	(ui-menu-add-entry "ma_layers"    "ma_tgllayers")
	(ui-menu-add-entry "ma_layers"    "ma_layerlist")
;	(ui-menu-add-separator "ma_layers")
	(ui-menu-add-entry "ma_layers"    "ma_layertglempty")
; The name_number tool has been removed from the code and has been added
; as an option inside General Preferences.
;	(ui-menu-add-entry "ma_layers"    "ma_layer_name_number")

;;============================================================= LEVEL DEFINES


(ui-symbol "al_bkactions" 1)
(ui-menu "al_bkactions"
	(list 'label_string 		"VariantActions")
	(list 'attribute_string 	"varaction")
	(list 'common )
	(list 'fixed )
)
(ui-menu-add-entry "al_bkactions" "mp_views_delete_bookmark")
(ui-menu-add-entry "al_bkactions" "mp_views_set_bookmark")
(ui-menu-add-entry "al_bkactions" "mp_views_prev_bookmark")
(ui-menu-add-entry "al_bkactions" "mp_views_next_bookmark")
(ui-menu-add-entry "al_bkactions" "mp_views_toggleCameraBookmark")
(ui-menu-add-entry "al_bkactions" "mp_views_publish_bookmark")

(ui-symbol "al_bkdefault" 2 )
(ui-menu "al_bkdefault"
	(list 'label_string 		"Variants")
	(list 'attribute_string 	"variant")
)

(ui-level-add-menu "al_bookmarks"  "al_bkdefault")
(ui-level-add-menu "al_bookmarks"  "al_bkactions")

(ui-level-add-menu "al_menu_bar"        "al_file")
(ui-level-add-menu "al_menu_bar"        "al_edit")
(ui-level-add-menu "al_menu_bar"        "al_delete")
(ui-level-add-menu "al_menu_bar"        "mp_window")
(ui-level-add-menu "al_menu_bar"        "mp_objdisplay")
(ui-level-add-menu "al_menu_bar"        "mp_display")
(ui-level-add-menu "al_menu_bar"       	"ma_layers")
(ui-level-add-menu "al_menu_bar"        "sid_imagetools")
(ui-level-add-menu "al_menu_bar"        "rp_render")
(ui-level-add-menu "al_menu_bar"        "ap_animwinds")
(ui-level-add-menu "al_menu_bar"        "mp_windows_menu")
(ui-level-add-menu "al_menu_bar"        "al_envtools")
;;(ui-level-add-menu "al_menu_bar"    	"al_workflow")
(ui-level-add-menu "al_menu_bar"        "al_goto")
(ui-level-add-menu "al_menu_bar"        "al_shotgun")
(ui-level-add-menu "al_menu_bar"        "al_help")

(ui-level-add-menu "al_action_menu_bar"        "aw_listmode")
(ui-level-add-menu "al_action_menu_bar"        "aw_edit")
(ui-level-add-menu "al_action_menu_bar"        "aw_curvetools")
(ui-level-add-menu "al_action_menu_bar"        "aw_pick")
(ui-level-add-menu "al_action_menu_bar"        "aw_xform")
(ui-level-add-menu "al_action_menu_bar"        "aw_views")
(ui-level-add-menu "al_action_menu_bar"        "aw_disptools")
(ui-level-add-menu "al_action_menu_bar"        "aw_actiontools")
(ui-level-add-menu "al_action_menu_bar"        "aw_tangenttype")
(ui-level-add-menu "al_action_menu_bar"        "aw_preferences")

; This menu is for the Reference Manager
(ui-level-add-menu "al_reference_menu_bar" "al_ref_file_menu")
(ui-level-add-menu "al_reference_menu_bar" "al_ref_edit_menu")
(ui-level-add-menu "al_reference_menu_bar" "al_ref_view_menu")
(ui-level-add-menu "al_reference_menu_bar" "al_ref_filter_menu")

;; New modeBox tools

	(ui-symbol "mp_modeBoxtools"     (ui-symbol-reference "MP_LOCATE"))
	(ui-menu "mp_modeBoxtools"
		(list 'label_string "al_evaluation_tools_title")
		(list 'attribute_string "al_evaluation_tools_attribute")
	)

	(ui-shelf-entry  "mb_moveCV_D" "moveCV"
		(ui-new-symbol "mo_movecv_mode"		0 )
		(ui-new-symbol "mo_movecv_pickhull"	0 )
		(ui-new-symbol "mo_movecv_x"		#t )
		(ui-new-symbol "mo_movecv_y"		#t )
		(ui-new-symbol "mo_movecv_z"		#t )
		(ui-new-symbol "mo_movecv_n"		#t )
		(ui-new-symbol "mo_movecv_u"		#t )
		(ui-new-symbol "mo_movecv_v"		#t )
		(ui-new-symbol "mo_use_stepsize"	#f )
		(ui-new-symbol "mo_lock_stepsize"	#f )
		(ui-new-symbol "mo_stepsize"		0.01 )
		(ui-new-symbol "mo_mouse_warp"	1)
        (ui-new-symbol "mo_mouse_warp_index"    0 )
        (ui-new-symbol "mo_mouse_warps" (list 1.0 5.0 10.0 50.0 ))
		(ui-new-symbol "mo_pick_size"	    4)
		(ui-new-symbol "mo_proxy_display"	0 )
		(ui-new-symbol "mo_movecv_xf_mode"	0 )
		(ui-new-symbol "mo_movecv_pmod_mode" 0 )
		(ui-new-symbol "mo_movecv_falloff_type" 0 )
		(ui-new-symbol "mo_movecv_pmod_ufalloff" 1.0 )
		(ui-new-symbol "mo_movecv_pmod_vfalloff" 1.0 )
		(ui-new-symbol "mo_movecv_pmod_uprec" 0 )
		(ui-new-symbol "mo_movecv_pmod_vprec" 0 )
		(ui-new-symbol "mo_movecv_pmod_usucc" 0 )
		(ui-new-symbol "mo_movecv_pmod_vsucc" 0 )
	)

	(ui-shelf-entry  "locScansurfDev_D" "scansurf_deviation" )
	(ui-shelf-entry  "EvaltoolXsect_D" "CrossSectionManager" )
	(ui-shelf-entry  "locCrvcurvat_D" "mbCurveCurvature" )

   (ui-shelf-entry  "mb_moveCV_M" "moveCV" )
	(ui-shelf-entry  "locScansurfDev_M" "scansurf_deviation" )
	(ui-shelf-entry  "EvaltoolXsect_M" "CrossSectionManager" )
	(ui-shelf-entry  "locCrvcurvat_M" "mbCurveCurvature" )

;; Diagnostic Tools
   (ui-shelf-entry  "mb_DiagnosticShade_MultiColor_D" "DiagnosticShade_MultiColor" )
   (ui-shelf-entry  "mb_DiagnosticShade_RandomColor_D" "DiagnosticShade_RandomColor" )
   (ui-shelf-entry  "mb_DiagnosticShade_CurvatureEvaluation_D" "DiagnosticShade_CurvatureEvaluation" )
   (ui-shelf-entry  "mb_DiagnosticShade_IsoAngle_D" "DiagnosticShade_IsoAngle" )
   (ui-shelf-entry  "mb_DiagnosticShade_Zebra_D" "DiagnosticShade_Zebra"  )
   (ui-shelf-entry  "mb_DiagnosticShade_SurfaceEvaluation_D" "DiagnosticShade_SurfaceEvaluation" )
   (ui-shelf-entry  "mb_DiagnosticShade_UserDefinedTexture_D" "DiagnosticShade_UserDefinedTexture" )
   (ui-shelf-entry  "mb_DiagnosticShade_LightTunnel_D" "DiagnosticShade_LightTunnel" )
   (ui-shelf-entry  "mb_DiagnosticShade_ClayAO_D" "DiagnosticShade_ClayAO" )
   (ui-shelf-entry  "mb_DiagnosticShade_SaddleHightlight_D" "DiagnosticShade_SaddleHightlight" )
   (ui-shelf-entry  "mb_DiagnosticShade_VREDNurbsRT_D" "DiagnosticShade_VREDNurbsRT" )
   (ui-shelf-entry  "mb_DiagnosticShade_ShadeOff_D" "DiagnosticShade_ShadeOff" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState1_D" "DiagnosticShade_VisState1" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState2_D" "DiagnosticShade_VisState2" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState3_D" "DiagnosticShade_VisState3" )
   (ui-shelf-entry  "mb_DiagnosticShade_FileState_D" "DiagnosticShade_FileState" )

   (ui-shelf-entry  "mb_DiagnosticShade_MultiColor_M" "DiagnosticShade_MultiColor" )
   (ui-shelf-entry  "mb_DiagnosticShade_RandomColor_M" "DiagnosticShade_RandomColor" )
   (ui-shelf-entry  "mb_DiagnosticShade_CurvatureEvaluation_M" "DiagnosticShade_CurvatureEvaluation" )
   (ui-shelf-entry  "mb_DiagnosticShade_IsoAngle_M" "DiagnosticShade_IsoAngle" )
   (ui-shelf-entry  "mb_DiagnosticShade_Zebra_M" "DiagnosticShade_Zebra"  )
   (ui-shelf-entry  "mb_DiagnosticShade_SurfaceEvaluation_M" "DiagnosticShade_SurfaceEvaluation" )
   (ui-shelf-entry  "mb_DiagnosticShade_UserDefinedTexture_M" "DiagnosticShade_UserDefinedTexture" )
   (ui-shelf-entry  "mb_DiagnosticShade_VREDNurbsRT_M" "DiagnosticShade_VREDNurbsRT" )
   (ui-shelf-entry  "mb_DiagnosticShade_SaddleHightlight_M" "DiagnosticShade_SaddleHightlight" )
   (ui-shelf-entry  "mb_DiagnosticShade_VREDNurbsRT_M" "DiagnosticShade_VREDNurbsRT" )
   (ui-shelf-entry  "mb_DiagnosticShade_ShadeOff_M" "DiagnosticShade_ShadeOff" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState1_M" "DiagnosticShade_VisState1" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState2_M" "DiagnosticShade_VisState2" )
   (ui-shelf-entry  "mb_DiagnosticShade_VisState3_M" "DiagnosticShade_VisState3" )
   (ui-shelf-entry  "mb_DiagnosticShade_FileState_M" "DiagnosticShade_FileState" )

   (ui-shelf-entry "mp_paint_newcanvas"	"NewCanvas")


(ui-level-add-menu "al_toolbox"         "mp_pick")
(ui-level-add-menu "al_toolbox"         "mp_xform")
;; Sid paint tools
(ui-level-add-menu "al_toolbox"         "mp_paint")

(ui-level-add-menu "al_toolbox"        "mp_effects_menu")


(ui-level-add-menu "al_toolbox"         "al_curvetoolbox")
(ui-level-add-menu "al_toolbox"         "mp_crvtools")
(ui-level-add-menu "al_toolbox"         "mp_objtools")
(ui-level-add-menu "al_toolbox"         "mp_buildsurf")
(ui-level-add-menu "al_toolbox"         "mp_srftools")

(ui-level-add-menu "al_toolbox"        "al_mesh")

(ui-level-add-menu "al_toolbox"         "mp_views")
(ui-level-add-menu "al_toolbox"         "mp_grid")
(ui-level-add-menu "al_toolbox"       	"al_locate")
(ui-level-add-menu "al_toolbox"         "mp_evaltool")
(ui-level-add-menu "al_toolbox"         'al_cloudtoolbox)

;;--------------------------------------------
(ui-string "al_window_view_title" "View")
(ui-string "al_window_view_attribute" "View")
(ui-menu "al_window_view"
	(list 'select "mp_menu" 20)
	(list 'label_string "al_window_view_title")
	(list 'attribute_string "al_window_view_attribute")
)
(ui-menu-add-entry "al_window_view" "mp_views_persp_camera")

;; render panel

(ui-shelf-entry  "mb_toggleShade" "TglShade" )
(ui-shelf-entry  "mb_toggleModel" "TglModel" )
(ui-shelf-entry  "mb_MLister" "MlistAll" )

(ui-menu "mo_keypoint_curve_tools"
	(list 'label_string "KeypntCrv Tools")
	(list 'attribute_string "kpcrv tbox")
)

(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_circle")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_ellipse")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_rectangle")

(ui-string "mo_arc_funcs" 			"Arcs")
(ui-string "mo_line_funcs" 			"Lines")
(ui-string "mo_linetan_funcs" 		"Line Tangent & Perp")
(ui-string "mo_kpcut_funcs" 		"Break & Join")

(ui-submenu "mo_arc_funcs" )
	(ui-submenu-add-entry "mo_arc_funcs" "mo_arc_threepoint")
	(ui-submenu-add-entry "mo_arc_funcs" "mo_arc_twopoint")
	(ui-submenu-add-entry "mo_arc_funcs" "mo_arc_tan_to_crv")
	(ui-submenu-add-entry "mo_arc_funcs" "mo_arc_concentric")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_arc_funcs" )

(ui-submenu "mo_line_funcs" )
	(ui-submenu-add-entry "mo_line_funcs" "mo_line_twopoint")
	(ui-submenu-add-entry "mo_line_funcs" "mo_line_poly")
	(ui-submenu-add-entry "mo_line_funcs" "mo_line_parallel")
	(ui-submenu-add-entry "mo_line_funcs" "mo_line_at_angle")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_line_funcs" )

(ui-submenu "mo_linetan_funcs" )
	(ui-submenu-add-entry "mo_linetan_funcs" "mo_line_tan_to_curve")
	(ui-submenu-add-entry "mo_linetan_funcs" "mo_line_tan_fromto_curve")
	(ui-submenu-add-entry "mo_linetan_funcs" "mo_line_perp_fromto_curve")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_linetan_funcs" )

(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_linearc")

(ui-submenu "mo_kpcut_funcs" )
	(ui-submenu-add-entry "mo_kpcut_funcs" "mo_break_curves")
	(ui-submenu-add-entry "mo_kpcut_funcs" "mo_join_curves")
(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_kpcut_funcs" )


(ui-menu-add-entry "mo_keypoint_curve_tools" "mo_drag_keypoints")

(ui-level-add-menu "mo_keypoint_curve_palette" "mo_keypoint_curve_tools")


(ui-symbol "xs_new" 0 )
(ui-menu "xs_new"
	(list 'select "xs_new" 8)
	(list 'label_string 'xs_new_str )
	(list 'attribute_string 'xs_new_attr_str )
)
;;(ui-menu-add-entry "xs_new" "mo_axis_sections" )
;;
(ui-menu-add-entry "xs_new" "xs_new_axis_incremental" )

(ui-symbol "xs_new_axis_discrete" 0 )
(ui-submenu "xs_new_axis_discrete" )
	(ui-submenu-add-entry "xs_new_axis_discrete" "xs_new_axis_discrete_x")
	(ui-submenu-add-entry "xs_new_axis_discrete" "xs_new_axis_discrete_y")
	(ui-submenu-add-entry "xs_new_axis_discrete" "xs_new_axis_discrete_z")
(ui-menu-add-entry "xs_new" "xs_new_axis_discrete" )


(ui-menu-add-entry "xs_new" "xs_new_picked_reference" )
(ui-menu-add-entry "xs_new" "xs_new_planar" )
(ui-menu-add-entry "xs_new" "xs_new_true" )

(ui-symbol "xs_delete" 0 )
(ui-menu "xs_delete"
	(list 'select "xs_delete" 8)
	(list 'label_string 'xs_delete_str )
	(list 'attribute_string 'xs_delete_attr_str )
)
(ui-menu-add-entry "xs_delete" "xs_delete_selected" )
(ui-menu-add-entry "xs_delete" "xs_delete_all" )

(ui-symbol "xs_tools" 0 )
(ui-menu "xs_tools"
	(list 'select "xs_tools" 8)
	(list 'label_string 'xs_tools_str )
	(list 'attribute_string 'xs_tools_attr_str )
)
(ui-menu-add-entry "xs_tools" "xs_promote_selected" )


(ui-level-add-menu "xsec_menu_bar"        "xs_new")
(ui-level-add-menu "xsec_menu_bar"        "xs_delete")
(ui-level-add-menu "xsec_menu_bar"        "xs_tools")

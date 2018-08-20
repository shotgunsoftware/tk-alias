;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                            ;
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

; New version of Vars files

(ui-symbol "mp_file"                    (ui-symbol-reference "MP_RETRIEVE"))
(ui-symbol "mp_objtools"                (ui-symbol-reference "MP_PRIMITIVE"))
(ui-symbol "mp_crvtools"                (ui-symbol-reference "MP_NEWCRV"))
(ui-symbol "mp_buildsurf"               (ui-symbol-reference "MP_BOUNDARY"))
(ui-symbol "mp_pick"                    (ui-symbol-reference "MP_OBJECT"))
(ui-symbol "mp_xform"                   (ui-symbol-reference "MP_MOVE"))
(ui-symbol "mp_objmod"                  (ui-symbol-reference "MP_GROUP"))
(ui-symbol "mp_grid"                    (ui-symbol-reference "MP_GRIDSPACING"))
(ui-symbol "mp_delete"                  (ui-symbol-reference "MP_DELACT"))
(ui-symbol "mp_views"                   (ui-symbol-reference "MP_TUMBLE"))
(ui-symbol "mp_window"                  (ui-symbol-reference "MP_ALL"))
(ui-symbol "mp_objdisplay"              (ui-symbol-reference "MP_VISIBLE"))
(ui-symbol "mp_objdisplay"              (ui-symbol-reference "MP_TGLSIMPDISP"))
(ui-symbol "mp_display"                 (ui-symbol-reference "MP_QUICK"))
(ui-symbol "mp_srftools"                (ui-symbol-reference "MP_TRIM"))
(ui-symbol "mp_evaltool"                (ui-symbol-reference "MP_LOCATE"))
(ui-symbol "mp_goto"                    (ui-symbol-reference "CML_MAIN"))
(ui-symbol "m_menu"                     (ui-symbol-reference "CML_MAIN"))
(ui-symbol "al_cloudtoolbox"            (ui-symbol-reference "M_UNUSED"))
(ui-symbol "al_workflow"				(ui-symbol-reference "M_UNUSED"))
;; New (v7) menu symbols

(ui-symbol "al_file"                    (ui-symbol-reference "MP_RETRIEVE"))
(ui-symbol "al_edit"                    (ui-symbol-reference "MP_COPY"))
(ui-symbol "al_delete"                  (ui-symbol-reference "MP_DELACT"))
(ui-symbol "al_objmod"                  (ui-symbol-reference "MP_GROUP"))
(ui-symbol "al_objtools"                (ui-symbol-reference "MP_PRIMITIVE"))
(ui-symbol "al_crvtools"                (ui-symbol-reference "MP_NEWCRV"))
(ui-symbol "al_buildsurf"               (ui-symbol-reference "MP_BOUNDARY"))
(ui-symbol "al_pick"                    (ui-symbol-reference "MP_OBJECT"))
(ui-symbol "al_xform"                   (ui-symbol-reference "MP_MOVE"))
(ui-symbol "al_objmod"                  (ui-symbol-reference "MP_GROUP"))
(ui-symbol "al_grid"                    (ui-symbol-reference "MP_GRIDSPACING"))
(ui-symbol "al_delete"                  (ui-symbol-reference "MP_DELACT"))
(ui-symbol "al_views"                   (ui-symbol-reference "MP_TUMBLE"))
(ui-symbol "al_window"                  (ui-symbol-reference "MP_ALL"))
(ui-symbol "mp_effects_menu"            (ui-symbol-reference "MP_EFFECTS"))
(ui-symbol "al_objdisplay"              (ui-symbol-reference "MP_VISIBLE"))
(ui-symbol "al_objdisplay"              (ui-symbol-reference "MP_TGLSIMPDISP"))
(ui-symbol "al_display"                 (ui-symbol-reference "MP_QUICK"))
(ui-symbol "al_srftools"                (ui-symbol-reference "MP_TRIM"))
(ui-symbol "al_evaltool"                (ui-symbol-reference "MP_LOCATE"))
(ui-symbol "al_goto"                    (ui-symbol-reference "CML_MAIN"))
(ui-symbol "al_help"                    (ui-symbol-reference "M_ONLINEDOCS"))
(ui-symbol "al_shotgun"                 (ui-symbol-reference "M_ONLINEDOCS"))
(ui-symbol "al_polytools"               (ui-symbol-reference "MP_OPEN_POLYTOOL"))
(ui-symbol "al_polyedit"                (ui-symbol-reference "MP_OPEN_POLYTOOL"))
(ui-symbol "al_polydisp_edit"           (ui-symbol-reference "MP_OPEN_POLYTOOL"))
(ui-symbol "al_mesh"                    0)
(ui-symbol "al_curvetoolbox"            (ui-symbol-reference "MP_DRAFT_EDITOR"))
(ui-symbol "al_object_create"           (ui-symbol-reference "MP_PRIMITIVE"))
(ui-symbol "al_locate"           		(ui-symbol-reference "MP_MOVE_LOCATOR"))
(ui-symbol "al_special_display"   		(ui-symbol-reference "M_UNUSED"))
(ui-symbol "al_special_workspace"   	0 )
(ui-symbol "al_special_anim"   			(ui-symbol-reference "M_UNUSED"))
(ui-symbol "al_special_construction"	(ui-symbol-reference "M_UNUSED"))
(ui-symbol "mo_cnet_tools"   			(ui-symbol-reference "M_UNUSED"))
(ui-symbol "mo_blend_crv_tools"			(ui-symbol-reference "M_UNUSED"))
(ui-symbol "mo_keypoint_curve_tools"	(ui-symbol-reference "M_UNUSED"))
(ui-symbol "mo_blend_crv_command"       "BlendCurveEditTangent")

(ui-symbol "mo_current_win"             (ui-symbol-reference "MO_PERSP") UI_SYMBOL_GROUP_NOSAVE )
(ui-symbol "mo_current_cam_is_persp"    #f UI_SYMBOL_GROUP_NOSAVE )


(ui-symbol "al_anim_tools"              (ui-symbol-reference "AP_PLAYBACK"))
(ui-symbol "al_anim_actions"            (ui-symbol-reference "AP_SETPARAM"))

(ui-symbol "al_render_actions"          (ui-symbol-reference "RP_GLOBALPARAMS"))
(ui-symbol "al_lights"                  (ui-symbol-reference "RP_LIGHT_POINT"))
(ui-symbol "al_shader"                  (ui-symbol-reference "RP_SHADER_LISTALL"))

(ui-symbol "al_envtools"                (ui-symbol-reference "MA_EDIT_ALIAS_PREFS"))
(ui-symbol "ma_layers"                  (ui-symbol-reference "CML_MAIN"))
(ui-symbol "sid_imagetools"             (ui-symbol-reference "CML_MAIN"))

(ui-symbol "mp_windows_menu"            (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_new_windows"             (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_curve_locator_menu"      (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_edit_menu"               (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_ToolShelf"               (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_ToolBox"                 (ui-symbol-reference "CML_MAIN"))
(ui-symbol "mp_ToolBookMark"            (ui-symbol-reference "CML_MAIN"))
(ui-symbol "al_cloudtoolbox"            (ui-symbol-reference "M_UNUSED"))


(ui-symbol "aps_shelves"         #t)
(ui-symbol "aps_mmenus"          #t)
(ui-symbol "aps_userOptions"     #t)
(ui-symbol "aps_userColors"      #t)
(ui-symbol "aps_generalPrefs"    #t)
(ui-symbol "aps_hotKeys"         #t)
(ui-symbol "aps_menus"           #t)
(ui-symbol "aps_constrPresets"   #t)

; store options file types -- wire, data transfer

(ui-symbol "mo_store_type"              (ui-symbol-reference "MO_WIRE"))
(ui-symbol "mo_wire_file_data"          (ui-symbol-reference "MO_FILE_DATA_ALL"))
(ui-symbol "mo_filter_file_data"        (ui-symbol-reference "MO_FILE_DATA_ALL"))

(ui-symbol "mo_wire_bake"				#f)
(ui-symbol "mo_wire_bake_installed_images" #f)

(ui-symbol "mo_wire_studioviewer"       #f)
(ui-symbol "mo_spf_format"              (ui-symbol-reference "MO_SPF_BINARY"))
(ui-symbol "mo_spf_type_tags"           #f)

; N.B. Since the following wdl variables are not set from an option box anymore,
; the 'temp' variables should eventually be removed.
; store options data transfer formats -- wire, iges, des, vda, dxf, dwg

(ui-symbol "mo_file_format"             (ui-symbol-reference "MO_WIRE"))
(ui-symbol "mo_iges_option_0"           (ui-symbol-reference "MO_IGES_BSPLINE"))
(ui-symbol "mo_iges_option_1"           (ui-symbol-reference "MO_PRESERVE_SURF"))
(ui-symbol "mo_iges_option_2"           (ui-symbol-reference "MO_TRIMMED_SURF"))
(ui-symbol "mo_des_option"              (ui-symbol-reference "MO_METRIC"))
(ui-symbol "mo_des_scan_data"           #f)
(ui-symbol "mo_step_option"             (ui-symbol-reference "MO_STEP_AP214"))
(ui-symbol "mo_step_option_1"           (ui-symbol-reference "MO_STEP_HYBRID"))
(ui-symbol "mo_step_option_2"           (ui-symbol-reference "MO_STEP_PARAMETER"))
(ui-symbol "mo_step_option_3"           (ui-symbol-reference "MO_SHELLS_ONLY"))
(ui-symbol "mo_step_option_keepmultiknots" #t)
(ui-symbol "mo_iges_store_scale"        1.0)
(ui-symbol "mo_vdais_store_scale"       1.0)
(ui-symbol "mo_c4_store_scale"          1.0)
(ui-symbol "mo_jamais_store_scale"      1.0)
(ui-symbol "mo_vdafs_store_scale"       1.0)
(ui-symbol "mo_vdafs_store_layer"       #f)
(ui-symbol "mo_des_store_scale"         1.0)
(ui-symbol "mo_styleguide_store_scale"  1.0)
(ui-symbol "mo_render_store_scale"      1.0)
(ui-symbol "mo_inventor_store_scale"    1.0)
(ui-symbol "mo_inventor_opt"            #f)
(ui-symbol "mo_inventor_in_units"	(ui-symbol-reference "MO_DT_CENTIMETERS"))
(ui-symbol "mo_iges_import_log_file"   #f)
(ui-symbol "mo_iges_export_log_file"   #f)
(ui-symbol "mo_iges_include_comments"   #f)
(ui-symbol "mo_vdais_include_comments"  #f)
(ui-symbol "mo_c4_include_comments"     #f)
(ui-symbol "mo_jamais_include_comments" #f)
(ui-symbol "mo_vdafs_include_comments"  #f)
(ui-symbol "mo_cai_include_comments"    #f)

(ui-symbol "mo_iges_significant_digits" 	12)
(ui-symbol "mo_vdais_significant_digits" 	12)
(ui-symbol "mo_c4_significant_digits"   	12)
(ui-symbol "mo_jamais_significant_digits"	 12)
(ui-symbol "mo_iges_units"          (ui-symbol-reference "MO_IGES_MODEL"))
(ui-symbol "mo_c4_units"            (ui-symbol-reference "MO_IGES_MILLIMETERS"))
(ui-symbol "mo_jamais_units"        (ui-symbol-reference "MO_IGES_MILLIMETERS"))
(ui-symbol "mo_render_out_units"    (ui-symbol-reference "MO_DT_INCHES"))
(ui-symbol "mo_inventor_out_units"  (ui-symbol-reference "MO_DT_METERS"))
(ui-symbol "mo_render_in_units"     (ui-symbol-reference "MO_DT_INCHES"))
(ui-symbol "mo_ug_units"            (ui-symbol-reference "MO_UG_MILLIMETERS"))

(ui-symbol "mo_step_file_extension"     ".stp")
(ui-symbol "mo_iges_file_extension"     ".igs")
(ui-symbol "mo_vdais_file_extension"    ".igs")
(ui-symbol "mo_jamais_file_extension"   ".igs")
(ui-symbol "mo_vdafs_file_extension"    ".vda")
(ui-symbol "mo_des_file_extension"      ".des")
(ui-symbol "mo_render_file_extension"   ".slp")

(ui-symbol "mo_iges_version"            (ui-symbol-reference "MO_IGES_V53"))

(ui-symbol "mo_ug_collaboration"        #f)
(ui-symbol "mo_ug_distance"             #f)
(ui-symbol "mo_ug_distance_value"       0.01)

(ui-symbol "mo_iges_retrieve_annotation" 	#f)
(ui-symbol "mo_vdais_retrieve_annotation" 	#f)
(ui-symbol "mo_c4_retrieve_annotation"  	#f)
(ui-symbol "mo_jamais_retrieve_annotation"	#f)


(ui-symbol "mo_iges_comments"           "")
(ui-symbol "mo_vdais_comments"          "")
(ui-symbol "mo_vdafs_comments"          "")
(ui-symbol "mo_c4_comments"             "")
(ui-symbol "mo_jamais_comments"         "")
(ui-symbol "mo_cai_comments"            "")

(ui-symbol "mo_iges_hdr_author"         "")
(ui-symbol "mo_iges_hdr_organization"   "")
(ui-symbol "mo_iges_hdr_prod_id_from_sender" "")
(ui-symbol "mo_iges_hdr_prod_id_for_receiver" "")


(ui-symbol "mo_cai_hdr_shortcomment"   "")
(ui-symbol "mo_cai_hdr_organization"   "")
(ui-symbol "mo_cai_hdr_company"        "")
(ui-symbol "mo_cai_hdr_authorization"  "")
(ui-symbol "mo_cai_hdr_author"         "")


(ui-symbol "mo_step_hdr_author"           "")
(ui-symbol "mo_step_hdr_organisation"     "")
(ui-symbol "mo_step_hdr_authorisation"    "")
(ui-symbol "mo_step_cc_person_last"       "")
(ui-symbol "mo_step_cc_person_first"      "")
(ui-symbol "mo_step_cc_person_id"         "")
(ui-symbol "mo_step_cc_organisation_id"   "")
(ui-symbol "mo_step_cc_organisation_name" "")
(ui-symbol "mo_step_cc_organisation_desc" "")
(ui-symbol "mo_step_cc_product_id"        "")
(ui-symbol "mo_step_cc_product_name"      "")
(ui-symbol "mo_step_cc_product_desc"      "")
(ui-symbol "mo_step_cc_po_role"          (ui-symbol-reference "MO_STEPCC_DESIGN_SUPPLIER"))
(ui-symbol "mo_step_cc_security_class"   (ui-symbol-reference "MO_STEPCC_UNCLASSIFIED"))
(ui-symbol "mo_step_cc_datetime_role"    (ui-symbol-reference "MO_STEPCC_CREATION_DATE"))
(ui-symbol "mo_step_cc_approval_role"    (ui-symbol-reference "MO_STEPCC_APPROVED"))

(ui-symbol "mo_vdais_hdr_sendfirm"      "")
(ui-symbol "mo_vdais_hdr_contact"       "")
(ui-symbol "mo_vdais_hdr_phone"         "")
(ui-symbol "mo_vdais_hdr_address"       "")
(ui-symbol "mo_vdais_hdr_project"       "")
(ui-symbol "mo_vdais_hdr_prjref"        "")
(ui-symbol "mo_vdais_hdr_variant"       "")
(ui-symbol "mo_vdais_hdr_confid"        "")
(ui-symbol "mo_vdais_hdr_valid"         "")
(ui-symbol "mo_vdais_hdr_rfirm"         "")
(ui-symbol "mo_vdais_hdr_rname"         "")

(ui-symbol "mo_vdafs_hdr_sendfirm"      "")
(ui-symbol "mo_vdafs_hdr_contact"       "")
(ui-symbol "mo_vdafs_hdr_phone"         "")
(ui-symbol "mo_vdafs_hdr_address"       "")
(ui-symbol "mo_vdafs_hdr_project"       "")
(ui-symbol "mo_vdafs_hdr_prjref"        "")
(ui-symbol "mo_vdafs_hdr_variant"       "")
(ui-symbol "mo_vdafs_hdr_confid"        "")
(ui-symbol "mo_vdafs_hdr_valid"         "")
(ui-symbol "mo_vdafs_hdr_rfirm"         "")
(ui-symbol "mo_vdafs_hdr_rname"         "")

(ui-symbol "mo_c4_hdr_sendsite"         "")
(ui-symbol "mo_c4_hdr_partno"           "")
(ui-symbol "mo_c4_hdr_clevel"           "")
(ui-symbol "mo_c4_hdr_pname"            "")
(ui-symbol "mo_c4_hdr_style"            "")
(ui-symbol "mo_c4_hdr_designer"         "")
(ui-symbol "mo_c4_hdr_translator"       "")
(ui-symbol "mo_c4_hdr_rsite"            "")
(ui-symbol "mo_c4_hdr_receiver"         "")
(ui-symbol "mo_c4_hdr_rfax"             "")

(ui-symbol "mo_ug_hdr_sendsite"         "")
(ui-symbol "mo_ug_hdr_partno"           "")
(ui-symbol "mo_ug_hdr_clevel"           "")
(ui-symbol "mo_ug_hdr_pname"            "")
(ui-symbol "mo_ug_hdr_style"            "")
(ui-symbol "mo_ug_hdr_designer"         "")
(ui-symbol "mo_ug_hdr_translator"       "")
(ui-symbol "mo_ug_hdr_rsite"            "")
(ui-symbol "mo_ug_hdr_receiver"         "")
(ui-symbol "mo_ug_hdr_rfax"             "")

(ui-symbol "mo_ug_healing"          (ui-symbol-reference "MO_UG_BREP_0"))
(ui-symbol "mo_ug_check-thicken"        #f)
(ui-symbol "mo_ug_thicken-amount"        3.0)
(ui-symbol "mo_ug_export_categories"            #f)
(ui-symbol "mo_ug_export_facets"                #f)
(ui-symbol "mo_ug_keep_multiknots"              #t)
(ui-symbol "mo_ug_parameterizePlane"            #f)
(ui-symbol "mo_ug_export_nurbs"					#t)
(ui-symbol "mo_ug_export_curves"				#t)
(ui-symbol "mo_ug_export_points"				#f)
(ui-symbol "mo_ug_export_splitG1"				#f)
(ui-symbol "mo_ug_export_useFixedTol"			#t)
(ui-symbol "mo_ug_file_version"    (ui-symbol-reference "MO_NX_29"))

(ui-symbol "mo_jamais_hdr_author"               "")
(ui-symbol "mo_jamais_hdr_organization"         "")
(ui-symbol "mo_jamais_hdr_prod_id_from_sender"  "")
(ui-symbol "mo_jamais_hdr_prod_id_for_receiver" "")

(ui-symbol "mo_granite_im_stitch"          #t)
(ui-symbol "mo_granite_im_import_curves"   #f)
(ui-symbol "mo_granite_im_import_quilts"   #f)
(ui-symbol "mo_granite_im_use_ptc_fitter"  #f)
(ui-symbol "mo_granite_im_trim_method"     (ui-symbol-reference "MO_GR_TRIM_2D"))
(ui-symbol "mo_granite_ex_thicken"         #f)
(ui-symbol "mo_granite_ex_thickness"      3.0)
(ui-symbol "mo_granite_ex_collaborate"     #f)
(ui-symbol "mo_granite_ex_use_granite_v2"  #f)
(ui-symbol "mo_granite_ex_save_version"    (ui-symbol-reference "MO_GRANITE_V9"))

(ui-symbol "mo_openjt_im_meshes"			#t)
(ui-symbol "mo_openjt_im_breps"				#t)
(ui-symbol "mo_openjt_im_curves"			#t)
(ui-symbol "mo_openjt_im_merge_vertices"	#f)
(ui-symbol "mo_openjt_im_merge_tol"			0.0001)

(ui-symbol "edit_pt_option"	1)
(ui-symbol "chord_option"	1)
(ui-symbol "ff_fillet_option"	1)

;; vault symbols
;(ui-symbol "mo_vault_enabled" 0)
(ui-symbol "mo_vault_auth_type" #f)
(ui-symbol "mo_vault_autoconnect" #f)
(ui-symbol "mo_vault_server_machine" "")
(ui-symbol "mo_vault_server" "")
(ui-symbol "mo_vault_user" "")
(ui-symbol "mo_vault_location" "")
(ui-symbol "mo_vault_folder_id" 0)
(ui-symbol "mo_vault_checkout_on_open" #f)
(ui-symbol "mo_vault_openDialog" "")  ;; open dialog state as an xml
(ui-symbol "mo_vault_keepCheckedOut" #f)
(ui-symbol "mo_vault_candd_onCheckin" #f)
(ui-symbol "mo_vault_connected" #f)
(ui-symbol "mo_vault_checkedOut" 0)  ;; 0 = not in vault
                                     ;; 1 = checked out
									 ;; 2 - checked in
(ui-symbol "mo_vault_checkInDialog" "")  ;; checkin dialog state as an xml
(ui-symbol "mo_vault_embed_images" #t)
(ui-symbol "mo_vault_visualize" #t)
(ui-symbol "mo_vault_client_loc" "")
;; end vault symbols

(ui-symbol "mo_iman_check_out"       #t)
(ui-symbol "mo_iman_check_in"        #f)
(ui-symbol "aw_iman_password"        "")
;(ui-symbol "aw_iman_userid"          ""); we save these stuff in AliasPrefs.scm
;(ui-symbol "aw_iman_autologin"       1 ); we will want try autologin
;(ui-symbol "aw_iman_userdata0" 0)
;(ui-symbol "aw_iman_userdata1" 0)
;(ui-symbol "aw_iman_userdata2" 0)
;(ui-symbol "aw_iman_userdata3" 0)
;(ui-symbol "aw_iman_userdata4" 0)
;(ui-symbol "aw_iman_userdata5" 0)
;(ui-symbol "aw_iman_userdata6" 0)
;(ui-symbol "aw_iman_userdata7" 0)
;(ui-symbol "mo_iman_asm_lister_x"		 0)
;(ui-symbol "mo_iman_asm_lister_y"		 0)
;(ui-symbol "mo_iman_asm_lister_h"		 400)
;(ui-symbol "mo_iman_asm_lister_w"		 800)
(ui-symbol "aw_iman_volume"          "")
(ui-symbol "aw_iman_server"          "sun-mcai")
(ui-symbol "aw_iman_database"        "")
(ui-symbol "aw_iman_rev_rules"		 "Latest Working")
(ui-symbol "aw_iman_item_types"		 "CORP_Criteria, 0,")
(ui-symbol "mo_iman_rev_rule"		 0)
(ui-symbol "mo_iman_usePasteOpen"	 1)
(ui-symbol "mo_iman_show_icon"		 0)
(ui-symbol "mo_iman_itemtype_prefix"		 1)
(ui-symbol "mo_iman_prefer_asm"		 1)
(ui-symbol "mo_iman_item_type"		 0)
;;(ui-symbol "mo_iman_relationship"		 3)
(ui-symbol "mo_iman_relationship_wire"		 3)
(ui-symbol "mo_iman_relationship_ug"		 3)
(ui-symbol "mo_iman_relationship_jt"		 11)
;;(ui-symbol "mo_iman_dataset_type"		 0)
(ui-symbol "mo_iman_dataset_type_wire"		 0)
(ui-symbol "mo_iman_dataset_type_ug"		 2)
(ui-symbol "mo_iman_dataset_type_jt"		 5)
(ui-symbol "mo_iman_baseline"				 0)
(ui-symbol "mo_iman_baseline_template"		 "")
(ui-symbol "mo_iman_baseline_template"		 "")
(ui-symbol "mo_iman_newItemName"		 "")
(ui-symbol "mo_iman_checkout_reason" " ")
(ui-symbol "mo_iman_find_itemid"	 " ")
(ui-symbol "mo_iman_del_unused_layers"			1)
(ui-symbol "mo_iman_auto_query_elapse"			15)

(ui-symbol "mo_obj_normals"   					#t)
(ui-symbol "mo_obj_object_groups"				#t)
(ui-symbol "mo_obj_smooth_groups" 				#t)
(ui-symbol "mo_obj_cluster"   					#t)
(ui-symbol "mo_obj_set"   						#t)
(ui-symbol "mo_obj_face"       (ui-symbol-reference "MO_FACE_TO_TRIMMED_SURF"))
(ui-symbol "mo_obj_tesselate"   				#f)
(ui-symbol "mo_obj_tesselation_tol" 	0.1)
(ui-symbol "mo_obj_store_units"      (ui-symbol-reference "MO_DT_CENTIMETERS"))
(ui-symbol "mo_obj_store_scale"      1.0)
(ui-symbol "mo_obj_include_comments" #t)
(ui-symbol "mo_obj_comments"         "")
(ui-symbol "mo_obj_keep_nrm" 		 #t)
(ui-symbol "mo_obj_vtx_group" (ui-symbol-reference "MO_VTX_GRP_SET"))
(ui-symbol "mo_obj_retrieve_units"   (ui-symbol-reference "MO_DT_CENTIMETERS"))
(ui-symbol "mo_obj_retrieve_scale"   1.0)
(ui-symbol "mo_obj_merge_vertices"   #t)
(ui-symbol "mo_obj_merge_with_pos_nrm" (ui-symbol-reference "MO_POSITION"))
(ui-symbol "mo_obj_merge_tol_vertices" 0.0001)
(ui-symbol "mo_obj_merge_tol_nrm_vertices" 1)

(ui-symbol "mo_edf_retrieve_want_groups" #t)
(ui-symbol "mo_edf_retrieve_want_log" #f)
(ui-symbol "mo_edf_retrieve_want_log_txt_extension" #f)
(ui-symbol "mo_edf_retrieve_want_log_redirect" #f)
(ui-symbol "mo_edf_retrieve_log_redirect_path" "")

(ui-symbol "mo_edf_store_want_groups" #t)
(ui-symbol "mo_edf_store_layer_order_method" 0)
(ui-symbol "mo_edf_store_want_log" #f)
(ui-symbol "mo_edf_store_want_log_txt_extension" #f)
(ui-symbol "mo_edf_store_want_log_redirect" #f)
(ui-symbol "mo_edf_store_log_redirect_path" "")

(ui-symbol "mo_stl_merge_vertices"      #f)
(ui-symbol "mo_stl_merge_tol_vertices"  0.0001)

(ui-symbol "mo_cmm_useexistingscan"     #f)
(ui-symbol "mo_cmm_showdeviation"       #f)
(ui-symbol "mo_cmm_devacceptdist"      0.1)
(ui-symbol "mo_cmm_devrampdist"        1.0)
(ui-symbol "mo_cmm_filterpoints"        #t)
(ui-symbol "mo_cmm_filtersize"			1.0)
(ui-symbol "mo_cmm_vertextol"			0.0)
(ui-symbol "mo_cmm_groupingtol"			0.2)
(ui-symbol "mo_cmm_limitedgelength"		#f)
(ui-symbol "mo_cmm_maxedgelength"		.5)
(ui-symbol "mo_cmm_maxholeedges"		30)

(ui-symbol "mo_exportSTL_format"        1)
(ui-symbol "mo_exportSTL_tolerance"     0.01)

(ui-symbol "mo_exportRP_fileFormat"    1)
(ui-symbol "mo_exportRP_format"        1)
(ui-symbol "mo_exportRP_stitchTolerance" 0.01)
(ui-symbol "mo_exportRP_tolerance"     0.01)
(ui-symbol "mo_exportRP_maxEdgeLength" 0.5)
(ui-symbol "mo_exportRP_flipNormals"   #f)
(ui-symbol "mo_exportRP_createWallThickness" #f)
(ui-symbol "mo_exportRP_wallThickness" 0.2)

; The following wdl variables are not used in any option box, but they are
; necessary to keep the values of the DT options when the user saves an option
; file.

(ui-symbol "mo_iges_vendor_default"     "Default")
(ui-symbol "mo_vdais_vendor_default"    "Default")
(ui-symbol "mo_vdais_option_0"        (ui-symbol-reference "MO_IGES_BSPLINE"))
(ui-symbol "mo_vdais_option_1"        (ui-symbol-reference "MO_PRESERVE_SURF"))
(ui-symbol "mo_vdais_option_2"        (ui-symbol-reference "MO_TRIMMED_SURF"))
(ui-symbol "mo_c4_option_1"           (ui-symbol-reference "MO_PRESERVE_SURF"))
(ui-symbol "mo_jamais_option_0"       (ui-symbol-reference "MO_IGES_BSPLINE"))
(ui-symbol "mo_jamais_option_1"       (ui-symbol-reference "MO_PRESERVE_SURF"))
(ui-symbol "mo_iges_rebuild_geometry"   #f)
(ui-symbol "mo_iges_dt_rebuild_tol"     0.01)
(ui-symbol "mo_vdais_rebuild_geometry"  #f)
(ui-symbol "mo_vdais_dt_rebuild_tol"    0.01)
(ui-symbol "mo_c4_rebuild_geometry"     #f)
(ui-symbol "mo_c4_dt_rebuild_tol"       0.01)
(ui-symbol "mo_jamais_rebuild_geometry" #f)
(ui-symbol "mo_jamais_dt_rebuild_tol"   0.01)
(ui-symbol "mo_vdafs_rebuild_geometry"  #f)
(ui-symbol "mo_vdafs_dt_rebuild_tol"    0.01)
(ui-symbol "mo_iges_store_layer_or_set"   (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_vdais_store_layer_or_set"  (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_c4_store_layer_or_set"     (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_jamais_store_layer_or_set" (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_dbview_tol" 0.1)
(ui-symbol "mo_dbview_tesselate" #f)
(ui-symbol "mo_dbview_ascii_binary" (ui-symbol-reference "MO_DBVIEW_BIN"))
(ui-symbol "mo_eai_organize_first"   (ui-symbol-reference "MO_EAI_BY_SHADER"))
(ui-symbol "mo_eai_organize_second"		#f)
(ui-symbol "mo_eai_organize_sort"		#f)
(ui-symbol "mo_eai_multi_file"         #t)
(ui-symbol "mo_eai_export_curves"      #f)
(ui-symbol "mo_eai_export_symmetry"    0)
(ui-symbol "mo_eai_export_lights"      #t)
(ui-symbol "mo_eai_export_shaders"     #t)
(ui-symbol "mo_eai_export_textures"    #t)
(ui-symbol "mo_eai_export_cameras"     #f); turned off at GM's request on 16 Oct 2006.
(ui-symbol "mo_eai_export_invisible"   #f)
(ui-symbol "mo_eai_export_templated"   #f)
(ui-symbol "mo_eai_verbose"            #t)
(ui-symbol "mo_eai_sew_faces"          #f)
(ui-symbol "mo_eai_sew_faces_tol"      0.01)
; (ui-symbol "mo_eai_sew_tolerance"    0.01)
(ui-symbol "mo_eai_scale"             1.0)
(ui-symbol "mo_eai_image_resolution"  128)
(ui-symbol "mo_eai_option"          (ui-symbol-reference "MO_EAI_USE_1LOD"))
(ui-symbol "mo_eai_option_1"        (ui-symbol-reference "MO_EAI_USER_DEF"))
(ui-symbol "mo_eai_config_file" "config.cfg")
(ui-symbol "mo_eai_tri_strip_optimization"    #t)
(ui-symbol "mo_eai_chordal_relative"    1)
(ui-symbol "mo_eai_angular_value"     20.0)
(ui-symbol "mo_eai_min_int_angle"     10.0)
(ui-symbol "mo_eai_chordal_value"      5.0)
(ui-symbol "mo_eai_max_aspect_ratio"   4.0)
(ui-symbol "mo_eai_edge_length"       15.0)
(ui-symbol "mo_eai_tesselate_all"      3)
(ui-symbol "mo_eai_geometry_type"		0)
(ui-symbol "mo_eai_brep_type"			0)
(ui-symbol "mo_eai_tess_type"			2)
;(ui-symbol "mo_eai_tesselation_exp_brep"      0)
(ui-symbol "mo_eai_tesselation_tol" 	0.1)
(ui-symbol "mo_eai_tesselation_tol1" 	0.25)
(ui-symbol "mo_eai_tesselation_tol2" 	1.0)
(ui-symbol "mo_eai_tesselation_lod" 	1)
(ui-symbol "mo_jt_import_log_option"   (ui-symbol-reference "MO_JT_IMPORT_NO_LOGFILE"))
(ui-symbol "mo_jt_import_brep_tess_pref"   (ui-symbol-reference "MO_JT_IMPORT_BREP_PREF"))
(ui-symbol "mo_jt_import_config_file"  "")
(ui-symbol "mo_jt_import_meshes" 		#t)
(ui-symbol "mo_jt_import_breps" 		#t)
(ui-symbol "mo_jt_import_curves" 		#t)

(ui-symbol "mo_sat_retrieve_want_log"            #f)
(ui-symbol "mo_sat_retrieve_want_optimization" 	 #f)
(ui-symbol "mo_sat_store_want_log"               #f)
(ui-symbol "mo_sat_store_want_binary"            #f)
(ui-symbol "mo_sat_store_version"                (ui-symbol-reference "MO_SAT_V70"))

; store options -- store select

(ui-symbol "mo_store_select_scope"      (ui-symbol-reference "MO_SAVE_ACTIVE_AS"))
(ui-symbol "mo_store_select_anim"       #t)
(ui-symbol "mo_store_select_model"      #t)
(ui-symbol "mo_store_select_attributes" #t)

; Toggle Windows Title Bar options
(ui-symbol "mo_tgl_titlebar_options"        (ui-symbol-reference "MO_CUR_WIND"))

; debugging options -- DBG,DUMP options

(ui-symbol "mo_dbg_flag_1"              #f)
(ui-symbol "mo_dbg_flag_2"              #f)
(ui-symbol "mo_dbg_flag_3"              #f)
(ui-symbol "mo_dbg_flag_4"              #f)
(ui-symbol "mo_dbg_float"               1.0)
(ui-symbol "mo_dbg_int"                 -1)


; debugging utilities

(ui-symbol "mo_dbg_util_func"           (ui-symbol-reference "MP_HIGH_GEOM"))


; tt store options

(ui-symbol "mo_tt_store_exact"          #f)
(ui-symbol "mo_tt_store_transform"      #t)

; checkpoints options

(ui-symbol "checkpoints_frequency"		    10 );
(ui-symbol "checkpoints_maxfiles"		    10 );
(ui-symbol "checkpoints_maxdisk"		    100 );
(ui-symbol "checkpoints_autosave_toggle"    #f );
(ui-symbol "checkpoints_autosave"		    #f );
(ui-symbol "checkpoints_varify"			    #f );
(ui-symbol "checkpoints_sortBy"			    2 );
(ui-symbol "checkpoints_clrOnExit"		    #f );

; Stageset Save Options

(ui-symbol "stageset_prompt_for_stage_save"			#f );


; retrieve options

(ui-symbol "mo_stage_style"				  0)
(ui-symbol "mo_wire_keep_renderGlobals"  #t)
(ui-symbol "mo_wire_keep_unitsTolerances" #t)
(ui-symbol "mo_wire_keepwin"            #t)
(ui-symbol "mo_wire_keepshaders"            #t)
(ui-symbol "mo_wire_keeplights"            #t)
(ui-symbol "mo_wire_keep_layers"	    #t)
(ui-symbol "mo_wire_keep_bookmarks"	    #t)
(ui-symbol "mo_wire_as_reference"       #f)
(ui-symbol "mo_filter_keepwin"          #t)
(ui-symbol "mo_wire_keepcam"            #t)
(ui-symbol "mo_filter_keepcam"          #t)
(ui-symbol "mo_wire_keepanim"           #t)
(ui-symbol "mo_filter_keepanim"         #t)
(ui-symbol "mo_wire_keepbackground"     #t)
(ui-symbol "mo_filter_keepbackground"   #t)
(ui-symbol "mo_iges_retrieve_scale"     1.0)
(ui-symbol "mo_vdais_retrieve_scale"    1.0)
(ui-symbol "mo_c4_retrieve_scale"       1.0)
(ui-symbol "mo_jamais_retrieve_scale"   1.0)
(ui-symbol "mo_vdafs_retrieve_scale"    1.0)
(ui-symbol "mo_des_retrieve_scale"      1.0)
(ui-symbol "mo_styleguide_retrieve_scale" 1.0)
(ui-symbol "mo_epsf_retrieve_scale"     1.0)
(ui-symbol "mo_illustrator_retrieve_scale" 1.0)
(ui-symbol "mo_render_retrieve_scale"   1.0)
(ui-symbol "mo_inventor_retrieve_scale" 1.0)
(ui-symbol "mo_render_keep_normals"   	#t)
(ui-symbol "mo_render_merge_vertices"   #t)
(ui-symbol "mo_inventor_merge_vertices" #t)
(ui-symbol "mo_render_merge_with_pos_nrm" (ui-symbol-reference "MO_POS_NRM"))
(ui-symbol "mo_render_merge_tol_vertices" 0.0001)
(ui-symbol "mo_inventor_merge_tol_vertices" 0.0001)
(ui-symbol "mo_render_merge_tol_nrm_vertices" 1)
(ui-symbol "mo_iges_group_ret"          #f)
(ui-symbol "mo_vdais_group_ret"         #f)
(ui-symbol "mo_c4_group_ret"            #f)
(ui-symbol "mo_jamais_group_ret"        #f)
(ui-symbol "mo_vdafs_group_ret"         #f)
(ui-symbol "mo_dwf_export_curves"          #f)
(ui-symbol "mo_dwf_export_symmetry"        0)
(ui-symbol "mo_dwf_tess_limit_length"      #f)
(ui-symbol "mo_dwf_tess_max_edge_length"   10.0)
(ui-symbol "mo_dwf_tess_chordal_deviation" 0.01)
(ui-symbol "mo_dwf_tess_type"              0)
(ui-symbol "mo_autocad_keepCrvs_dwg"    #t)
(ui-symbol "mo_autocad_keepCrvs_dxf"    #t)
(ui-symbol "mo_autocad_splitG1_dwg"     #f)
(ui-symbol "mo_autocad_splitG1_dxf"     #f)
(ui-symbol "mo_autocad_version_dwg"     (ui-symbol-reference "MO_ACAD_2013"))
(ui-symbol "mo_autocad_version_dxf"     (ui-symbol-reference "MO_ACAD_2013"))
(ui-symbol "mo_adsk_inventor_import_nurbs"     #t)
(ui-symbol "mo_adsk_inventor_import_meshes"    #f)
(ui-symbol "mo_des_group_ret"           #f)
(ui-symbol "mo_styleguide_group_ret"    #f)
(ui-symbol "mo_epsf_group_ret"          #f)
(ui-symbol "mo_illustrator_group_ret"   #f)
(ui-symbol "mo_render_group_ret"        #f)
(ui-symbol "mo_inventor_group_ret"      #f)
(ui-symbol "mo_step_stitch_ret"         #t)
(ui-symbol "mo_step_shrink_ret"         #f)
(ui-symbol "mo_ug_stitch_ret"           #t)
(ui-symbol "mo_ug_shrink_ret"           #f)
(ui-symbol "mo_iges_coalesce_srf_ret"   #f)
(ui-symbol "mo_vdais_coalesce_srf_ret"  #f)
(ui-symbol "mo_jamais_coalesce_srf_ret" #f)
(ui-symbol "mo_vdafs_coalesce_srf_ret"  #f)
(ui-symbol "mo_iges_trim_to_surf"       #f)
(ui-symbol "mo_vdais_trim_to_surf"      #t)
(ui-symbol "mo_c4_trim_to_surf"         #t)
(ui-symbol "mo_jamais_trim_to_surf"     #t)
(ui-symbol "mo_create_new_stage"        #f)
(ui-symbol "mo_vdafs_option_0" (ui-symbol-reference "MO_STEP_PARAMETER"))
(ui-symbol "mo_vdafs_retrieve_layer"    #f)
(ui-symbol "mo_cai_view_file_info"      #f)
(ui-symbol "mo_cai_import_extended_log" #f)
(ui-symbol "mo_cai_export_extended_log" #f)
(ui-symbol "mo_ug_import_dimAsLabel"    #f)
(ui-symbol "mo_ug_import_layerSelect"   #f)
(ui-symbol "mo_ug_import_selectedLayers"    "1-256")
(ui-symbol "mo_iman_nx_import_dimAsLabel"    #f)
(ui-symbol "mo_iman_nx_import_layerSelect"   #f)
(ui-symbol "mo_iman_nx_import_selectedLayers"  "1-256")
(ui-symbol "mo_ug_import_categories"    #f)
(ui-symbol "mo_ug_import_facets"        #f)
(ui-symbol "mo_ug_import_nurbs"			#t)
(ui-symbol "mo_ug_import_curves"		#t)
(ui-symbol "mo_ug_import_points"		#f)
(ui-symbol "mo_ug_import_log_opt" (ui-symbol-reference "MO_UG_NOLOG"))
(ui-symbol "mo_ug_export_log_opt" (ui-symbol-reference "MO_UG_NOLOG"))
(ui-symbol "mo_cai_import_browse_log"   #f)
(ui-symbol "mo_cai_export_browse_log"   #f)
(ui-symbol "mo_iges_option_3"         (ui-symbol-reference "MO_IGES_PREFERENCE"))
(ui-symbol "mo_c4_option_2"           (ui-symbol-reference "MO_STEP_PARAMETER"))
(ui-symbol "mo_vdais_option_3"        (ui-symbol-reference "MO_STEP_PARAMETER"))
(ui-symbol "mo_jamais_option_2"       (ui-symbol-reference "MO_STEP_PARAMETER"))
(ui-symbol "mo_iges_retrieve_layer_or_set"   (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_vdais_retrieve_layer_or_set"  (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_c4_retrieve_layer_or_set"     (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_jamais_retrieve_layer_or_set" (ui-symbol-reference "MO_LAYER"))
(ui-symbol "mo_iges_scan_data"         #f)
(ui-symbol "mo_vdafs_scan_data"        #f)
(ui-symbol "mo_catv4_auto_stitch"        #t)
(ui-symbol "mo_catv4_shrink_surface"     #f)
(ui-symbol "mo_catv4_import_invisible"   #f)
(ui-symbol "mo_catv4_import_infinite"    #f)
(ui-symbol "mo_catv4_import_curves"      #t)
(ui-symbol "mo_catv4_import_points"      #t)
(ui-symbol "mo_catv4_import_meshes"      #t)
(ui-symbol "mo_catv4_import_log_file"    (ui-symbol-reference "MO_CATV4_NOLOG"))
(ui-symbol "mo_catv5_auto_stitch"        #t)
(ui-symbol "mo_catv5_shrink_surface"     #f)
(ui-symbol "mo_catv5_import_as_const"    #t)
(ui-symbol "mo_catv5_invisible_datum"    #f)
(ui-symbol "mo_catv5_import_invisible"   #f)
(ui-symbol "mo_catv5_import_nurbs"       #t)
(ui-symbol "mo_catv5_import_cloud_data"  #t)
(ui-symbol "mo_catv5_import_weld_data"   #t)
(ui-symbol "mo_catv5_import_meshes"      #f)
(ui-symbol "mo_catv5_preserve_color"     #t)
(ui-symbol "mo_catv5_merge_vertices"     #f)
(ui-symbol "mo_catv5_merge_tol"      0.0001)
(ui-symbol "mo_catv5_param_space_curves" #t)
(ui-symbol "mo_catv5_infinite_object"    #f)
(ui-symbol "mo_catv5_import_log_file"   (ui-symbol-reference "MO_CATV5_NOLOG"))
(ui-symbol "mo_catv5_export_log_file"   (ui-symbol-reference "MO_CATV5_NOLOG"))
(ui-symbol "mo_catv5_import_by_layer"    #t)
(ui-symbol "mo_catv5_export_by_layer"    #t)
(ui-symbol "mo_catv5_import_empty_layer" #t)
(ui-symbol "mo_catv5_export_empty_layer" #t)
(ui-symbol "mo_catv5_export_cons"        #t)
(ui-symbol "mo_catv5_export_meshes"      #t)
(ui-symbol "mo_catv5_export_symmetry"    #f)
(ui-symbol "mo_catv5_divide_periodic"    #t)
(ui-symbol "mo_catv5_divide_multi_knots" #f)
(ui-symbol "mo_catv5_stitch_shell"       #t)
(ui-symbol "mo_catv5_stitch_tol"         0.001)
(ui-symbol "mo_catv5_stitch_close"       #f)
(ui-symbol "mo_catv5_stitch_open"        #t)
(ui-symbol "mo_catv5_stitch_keep"        #f)
(ui-symbol "mo_catv5_check_connexity"    #t)
(ui-symbol "mo_catv5_check_tangency"     #f)
(ui-symbol "mo_catv5_simplify_result"    #f)
(ui-symbol "mo_catv5_suppress_erronous"  #f)
(ui-symbol "mo_catv5_angular_threshold"  #f)
(ui-symbol "mo_catv5_angular_tol"        0.5)
(ui-symbol "mo_catv5_healing"            #f)
(ui-symbol "mo_catv5_heal_close"         #t)
(ui-symbol "mo_catv5_heal_keep"          #f)
(ui-symbol "mo_catv5_continuity_type"    #f)
(ui-symbol "mo_catv5_merge_distance"     0.001)
(ui-symbol "mo_catv5_distance_objective" 0.001)
(ui-symbol "mo_catv5_tangency_angle"     0.5)
(ui-symbol "mo_catv5_tangency_objective" 0.5)
(ui-symbol "mo_catv5_export_invisible"   #t)
(ui-symbol "mo_catv5_file_release"       (ui-symbol-reference "MO_CATV5_REL_24"))

(ui-symbol "mo_fbx_retrieve_want_log"           #f)
(ui-symbol "mo_fbx_retrieve_want_optimization"  #f)
(ui-symbol "mo_fbx_retrieve_want_curves"        #t)
(ui-symbol "mo_fbx_retrieve_want_bookmarks"     #t)
(ui-symbol "mo_fbx_retrieve_want_lights"        #t)
(ui-symbol "mo_fbx_retrieve_want_cameras"       #t)
(ui-symbol "mo_fbx_retrieve_want_shaders"       #t)
(ui-symbol "mo_fbx_retrieve_want_divide_periodic" #f)
(ui-symbol "mo_fbx_retrieve_want_z_axis"        #t)
(ui-symbol "mo_fbx_store_want_log"              #f)
(ui-symbol "mo_fbx_store_want_curves"           #t)
(ui-symbol "mo_fbx_store_want_symmetry"         #t)
(ui-symbol "mo_fbx_store_want_instances"        #t)
(ui-symbol "mo_fbx_store_want_bookmarks"        #t)
(ui-symbol "mo_fbx_store_want_lights"           #t)
(ui-symbol "mo_fbx_store_want_cameras"          #t)
(ui-symbol "mo_fbx_store_want_shaders"          #t)
(ui-symbol "mo_fbx_store_want_divide_periodic"  #t)
(ui-symbol "mo_fbx_store_want_z_axis"           #t)
(ui-symbol "mo_fbx_store_want_ascii_file"       #f)
(ui-symbol "mo_fbx_store_file_version"          (ui-symbol-reference "MO_FBX_2016"))
(ui-symbol "mo_fbx_store_trim_curve_type"       1)
(ui-symbol "mo_fbx_store_want_tessellation"     #f)
(ui-symbol "mo_fbx_store_tess_type"             1)
(ui-symbol "mo_fbx_store_tess_tolerance"        0.01)

(ui-symbol "mo_iges_atf_retrieve_want_log"               #f)
(ui-symbol "mo_iges_atf_retrieve_want_optimization"      #f)
(ui-symbol "mo_iges_atf_retrieve_want_annotation"        #f)
(ui-symbol "mo_iges_atf_retrieve_want_parametric"        #f)
(ui-symbol "mo_iges_atf_retrieve_want_construction"      #f)
(ui-symbol "mo_iges_atf_retrieve_want_nested_group"      #t)
(ui-symbol "mo_iges_atf_retrieve_want_curve_as_wire"     #t)
(ui-symbol "mo_iges_atf_retrieve_want_unbounded_plane_as_wp" #f)
(ui-symbol "mo_iges_atf_retrieve_want_transformation_as_wp"  #f)
(ui-symbol "mo_iges_atf_retrieve_want_shrink_surface"        #f)
(ui-symbol "mo_iges_atf_retrieve_want_scan_data"         #f)
(ui-symbol "mo_iges_atf_store_want_log"                  #f)
(ui-symbol "mo_iges_atf_store_want_layer"                #t)
(ui-symbol "mo_iges_atf_store_want_group_brep"           #t)
(ui-symbol "mo_iges_atf_store_want_group_hierarchy"      #t)
(ui-symbol "mo_iges_atf_store_want_curve_asm_conversion" #t)
(ui-symbol "mo_iges_atf_store_shell_type"                (ui-symbol-reference "MO_SOLID_SOLID"))
(ui-symbol "mo_iges_atf_store_surface_type"              (ui-symbol-reference "MO_TRIMMED_SURF"))
(ui-symbol "mo_iges_atf_store_as_nurbs"                  (ui-symbol-reference "MO_NURBS"))
(ui-symbol "mo_iges_atf_store_tolerance"                 0.001)
(ui-symbol "mo_iges_atf_store_scale"                     1.000)
(ui-symbol "mo_iges_atf_store_units"                     (ui-symbol-reference "MO_IGES_MODEL"))
(ui-symbol "mo_iges_atf_store_file_extension"            ".igs")

(ui-symbol "mo_nx_atf_retrieve_want_log"                                 #f)
(ui-symbol "mo_nx_atf_retrieve_want_optimization"                        #f)
(ui-symbol "mo_nx_atf_retrieve_facets"                                   #f)
(ui-symbol "mo_nx_atf_retrieve_associative_meshes"                       #f)
(ui-symbol "mo_nx_atf_retrieve_nurbs"                                    #t)
(ui-symbol "mo_nx_atf_retrieve_curves"                                   #t)
(ui-symbol "mo_nx_atf_retrieve_points"                                   #t)
(ui-symbol "mo_nx_atf_retrieve_invisibles"                               #t)
(ui-symbol "mo_nx_atf_retrieve_keep_topology"                            #t)
(ui-symbol "mo_nx_atf_retrieve_shrink_surfaces"                          #f)
(ui-symbol "mo_nx_atf_retrieve_split_periodic"                           #f)
(ui-symbol "mo_nx_atf_retrieve_simplify_primitives"                      #t)
(ui-symbol "mo_nx_atf_retrieve_enable_simplification"                    #f)
(ui-symbol "mo_nx_atf_retrieve_enable_healing"                           #t)
(ui-symbol "mo_nx_atf_retrieve_enable_edge_split_and_merge"              #t)
(ui-symbol "mo_nx_atf_retrieve_enable_face_split_and_merge"              #t)
(ui-symbol "mo_nx_atf_retrieve_preserve_surface_parameterization"        #t)
(ui-symbol "mo_nx_atf_retrieve_merge_faces"                              #f)
(ui-symbol "mo_nx_atf_retrieve_empty_layers"                             #f)
(ui-symbol "mo_nx_atf_retrieve_categories"                               #t)
(ui-symbol "mo_nx_atf_retrieve_empty_categories"                         #f)
(ui-symbol "mo_nx_atf_retrieve_map_category_name_to_layer"               #f)
(ui-symbol "mo_nx_atf_retrieve_want_attributes_in_sub_assembly"          #t)
(ui-symbol "mo_nx_atf_retrieve_want_category_all_files"                  #f)
(ui-symbol "mo_nx_atf_retrieve_tolerance"                             0.001)
(ui-symbol "mo_nx_atf_retrieve_dimensions"                               #f)
(ui-symbol "mo_nx_atf_retrieve_dimAsLabel"                               #f)
(ui-symbol "mo_nx_atf_retrieve_layerSelect"                              #f)
(ui-symbol "mo_nx_atf_retrieve_selectedLayers"                      "1-256")

(ui-symbol "mo_nx_atf_store_want_log"                                    #f)
(ui-symbol "mo_nx_atf_store_facets"                                      #t)
(ui-symbol "mo_nx_atf_store_nurbs"                                       #t)
(ui-symbol "mo_nx_atf_store_nurbs"                                       #t)
(ui-symbol "mo_nx_atf_store_points"                                      #t)
(ui-symbol "mo_nx_atf_store_invisibles"                                  #t)
(ui-symbol "mo_nx_atf_store_templates"                                   #f)
(ui-symbol "mo_nx_atf_store_keep_topology"                               #t)
(ui-symbol "mo_nx_atf_store_keep_topology"                               #t)
(ui-symbol "mo_nx_atf_store_layers"                                      #t)
(ui-symbol "mo_nx_atf_store_empty_layers"                                #f)
(ui-symbol "mo_nx_atf_store_categories"                                  #t)
(ui-symbol "mo_nx_atf_store_empty_categories"                            #f)
(ui-symbol "mo_nx_atf_store_layer_symmetry"                              #t)
(ui-symbol "mo_nx_atf_store_instances"                                   #t)
(ui-symbol "mo_nx_atf_store_simplify_primitives"                         #f)
(ui-symbol "mo_nx_atf_store_split_periodic"                              #f)
(ui-symbol "mo_nx_atf_store_split_g1_breaks"                             #f)
(ui-symbol "mo_nx_atf_store_parameterized_planes"                        #t)
(ui-symbol "mo_nx_atf_store_want_tessellation"                           #f)
(ui-symbol "mo_nx_atf_store_tessellation_type"                            1)
(ui-symbol "mo_nx_atf_store_tessellation_tolerance"                    0.01)
(ui-symbol "mo_nx_atf_store_file_version"  (ui-symbol-reference "MO_NX_29"))
(ui-symbol "mo_nx_atf_store_units"                                        0)
(ui-symbol "mo_nx_atf_store_cdf_path"                                    "")
;(ui-symbol "mo_nx_atf_store_cdf_path"                            "cdf.txt")
(ui-symbol "mo_nx_atf_store_convertLayerToCategory"                      #f)
(ui-symbol "mo_nx_atf_store_zeroTransform"                               #t)

(ui-symbol "mo_inventor_atf_retrieve_want_log"                           #f)
(ui-symbol "mo_inventor_atf_retrieve_want_optimization"                  #f)
(ui-symbol "mo_inventor_atf_retrieve_bodies" (ui-symbol-reference "MO_PRECISE_GEOMETRY"))
(ui-symbol "mo_inventor_atf_retrieve_meshes"                             #f)
(ui-symbol "mo_inventor_atf_retrieve_face_meshes"                        #f)
(ui-symbol "mo_inventor_atf_retrieve_nurbs"                              #t)
(ui-symbol "mo_inventor_atf_retrieve_curves"                             #t)
(ui-symbol "mo_inventor_atf_retrieve_points"                             #t)
(ui-symbol "mo_inventor_atf_retrieve_invisibles"                         #t)
(ui-symbol "mo_inventor_atf_retrieve_keep_topology"                      #t)
(ui-symbol "mo_inventor_atf_retrieve_shrink_surfaces"                    #f)
(ui-symbol "mo_inventor_atf_retrieve_split_periodic"                     #f)

(ui-symbol "mo_step_atf_retrieve_want_log"                               #f)
(ui-symbol "mo_step_atf_retrieve_want_optimization"                      #f)
(ui-symbol "mo_step_atf_retrieve_meshes"                                 #t)
(ui-symbol "mo_step_atf_retrieve_nurbs"                                  #t)
(ui-symbol "mo_step_atf_retrieve_curves"                                 #t)
(ui-symbol "mo_step_atf_retrieve_points"                                 #t)
(ui-symbol "mo_step_atf_retrieve_invisibles"                             #t)
(ui-symbol "mo_step_atf_retrieve_keep_topology"                          #t)
(ui-symbol "mo_step_atf_retrieve_shrink_surfaces"                        #f)
(ui-symbol "mo_step_atf_retrieve_split_periodic"                         #f)

(ui-symbol "mo_catiav5_atf_retrieve_want_log"                            #f)
(ui-symbol "mo_catiav5_atf_retrieve_want_optimization"                   #f)
(ui-symbol "mo_catiav5_atf_retrieve_meshes"                              #f)
(ui-symbol "mo_catiav5_atf_retrieve_nurbs"                               #t)
(ui-symbol "mo_catiav5_atf_retrieve_curves"                              #t)
(ui-symbol "mo_catiav5_atf_retrieve_points"                              #t)
(ui-symbol "mo_catiav5_atf_retrieve_invisibles"                          #f)
(ui-symbol "mo_catiav5_atf_retrieve_infinites"                           #f)
(ui-symbol "mo_catiav5_atf_retrieve_cloud_data"                          #t)
(ui-symbol "mo_catiav5_atf_retrieve_weld_data"                           #t)
(ui-symbol "mo_catiav5_atf_retrieve_keep_topology"                       #t)
(ui-symbol "mo_catiav5_atf_retrieve_shrink_surfaces"                     #f)
(ui-symbol "mo_catiav5_atf_retrieve_split_periodic"                      #f)
(ui-symbol "mo_catiav5_atf_retrieve_color_meshes"                        #t)
(ui-symbol "mo_catiav5_atf_retrieve_merge_vertices"                      #f)
(ui-symbol "mo_catiav5_atf_retrieve_merge_vertices_tol"              0.0001)
(ui-symbol "mo_catiav5_atf_retrieve_geometric_sets"                      #t)
(ui-symbol "mo_catiav5_atf_retrieve_want_annotation"                     #t)

(ui-symbol "mo_catiav4_atf_retrieve_want_log"                            #f)
(ui-symbol "mo_catiav4_atf_retrieve_want_optimization"                   #f)
(ui-symbol "mo_catiav4_atf_retrieve_meshes"                              #t)
(ui-symbol "mo_catiav4_atf_retrieve_nurbs"                               #t)
(ui-symbol "mo_catiav4_atf_retrieve_curves"                              #t)
(ui-symbol "mo_catiav4_atf_retrieve_points"                              #t)
(ui-symbol "mo_catiav4_atf_retrieve_invisibles"                          #f)
(ui-symbol "mo_catiav4_atf_retrieve_infinites"                           #f)
(ui-symbol "mo_catiav4_atf_retrieve_keep_topology"                       #t)
(ui-symbol "mo_catiav4_atf_retrieve_shrink_surfaces"                     #f)
(ui-symbol "mo_catiav4_atf_retrieve_split_periodic"                      #f)

(ui-symbol "mo_stl_atf_retrieve_want_log"                                #f)
(ui-symbol "mo_stl_atf_retrieve_colors"                                  #t)
(ui-symbol "mo_stl_atf_retrieve_color_schema"                             0)
(ui-symbol "mo_stl_atf_retrieve_units"                                    1)
(ui-symbol "mo_stl_atf_retrieve_merge_vertices"                          #f)
(ui-symbol "mo_stl_atf_retrieve_merge_vertices_tol"                  0.0001)

(ui-symbol "mo_jt_atf_retrieve_want_log"                                 #f)
(ui-symbol "mo_jt_atf_retrieve_want_optimization"                        #f)
(ui-symbol "mo_jt_atf_retrieve_meshes"                                   #t)
(ui-symbol "mo_jt_atf_retrieve_nurbs"                                    #t)
(ui-symbol "mo_jt_atf_retrieve_curves"                                   #t)
(ui-symbol "mo_jt_atf_retrieve_points"                                   #t)
(ui-symbol "mo_jt_atf_retrieve_keep_topology"                            #t)
(ui-symbol "mo_jt_atf_retrieve_shrink_surfaces"                          #f)
(ui-symbol "mo_jt_atf_retrieve_split_periodic"                           #f)
(ui-symbol "mo_jt_atf_retrieve_lod"                                       0)
(ui-symbol "mo_jt_atf_retrieve_merge_vertices"                           #f)
(ui-symbol "mo_jt_atf_retrieve_merge_vertices_tol"                   0.0001)

(ui-symbol "mo_granite_atf_retrieve_want_log"                            #f)
(ui-symbol "mo_granite_atf_retrieve_want_optimization"                   #f)
(ui-symbol "mo_granite_atf_retrieve_nurbs"                               #t)
(ui-symbol "mo_granite_atf_retrieve_quilts"                              #t)
(ui-symbol "mo_granite_atf_retrieve_curves"                              #t)
(ui-symbol "mo_granite_atf_retrieve_points"                              #t)
(ui-symbol "mo_granite_atf_retrieve_invisibles"                          #t)
(ui-symbol "mo_granite_atf_retrieve_keep_topology"                       #t)
(ui-symbol "mo_granite_atf_retrieve_shrink_surfaces"                     #f)
(ui-symbol "mo_granite_atf_retrieve_split_periodic"                      #f)
(ui-symbol "mo_granite_atf_retrieve_construction_planes"                 #f)

(ui-symbol "mo_solidworks_atf_retrieve_want_log"                         #f)
(ui-symbol "mo_solidworks_atf_retrieve_want_optimization"                #f)
(ui-symbol "mo_solidworks_atf_retrieve_nurbs"                            #t)
(ui-symbol "mo_solidworks_atf_retrieve_curves"                           #t)
(ui-symbol "mo_solidworks_atf_retrieve_points"                           #t)
(ui-symbol "mo_solidworks_atf_retrieve_invisibles"                       #t)
(ui-symbol "mo_solidworks_atf_retrieve_keep_topology"                    #t)
(ui-symbol "mo_solidworks_atf_retrieve_shrink_surfaces"                  #f)
(ui-symbol "mo_solidworks_atf_retrieve_split_periodic"                   #f)

; Plot options
; The following wdl variables are not used in any option box, but they are
; necessary to keep the values of the Plot options when the user saves an option
; file.

;(ui-symbol "mo_plot_scope"              (ui-symbol-reference "MO_PLOT_ALL"))
;(ui-symbol "mo_plot_border"             #t)
;(ui-symbol "mo_plot_auto_model_scale"   #f)
;(ui-symbol "mo_plot_xoffset"            0)
;(ui-symbol "mo_plot_yoffset"            0)

;(ui-symbol "mo_plot_output"             0) ; PL_OUTPUT_FILE = 0, PL_OUTPUT_PLOTTER = 1
;(ui-symbol "mo_plot_hidline"            #f)
;(ui-symbol "mo_plot_units"              "cm")
;(ui-symbol "mo_plot_position"           (ui-symbol-reference "MO_PLOT_RELATIVE"))
;(ui-symbol "mo_plot_center"             0)
;(ui-symbol "mo_plot_rotate"             0)
;(ui-symbol "mo_plot_scale"              1.0)
;(ui-symbol "mo_plot_plotter_type"       0)
;(ui-symbol "mo_plot_standards"          0)
;(ui-symbol "mo_plot_paper_size"         1)
;(ui-symbol "mo_plot_xcorrection"        1.0)
;(ui-symbol "mo_plot_ycorrection"        1.0)
;(ui-symbol "mo_plot_model_scale"		1.0)
;(ui-symbol "mo_plot_model_scale_mode_xcenter"	0.5)
;(ui-symbol "mo_plot_model_scale_mode_ycenter"	0.5)
;(ui-symbol "mo_plot_all_papers"			#t)
;(ui-symbol "mo_plot_fit_to_paper"		#f)
;(ui-symbol "mo_plot_arrow_size_cm"		0.4)
;(ui-symbol "mo_plot_grids"				#t)
;(ui-symbol "mo_plot_hpgl_plotter_type"	"default")
;(ui-symbol "mo_plot_postscript_plotter_type"	"default")
;(ui-symbol "mo_plot_paper_type"			"A4H")

;(ui-symbol "mo_plot_number_paper_x"		1)
;(ui-symbol "mo_plot_number_paper_y"		1)
;(ui-symbol "mo_plot_ll_window_wname"	(ui-symbol-reference "MO_LEFT))
;(ui-symbol "mo_plot_lr_window_wname"	(ui-symbol-reference "MO_BACK"))
;(ui-symbol "mo_plot_ul_window_wname"	(ui-symbol-reference "MO_TOP"))
;(ui-symbol "mo_plot_ur_window_wname"	(ui-symbol-reference "MO_NO_WINDOW"))
;(ui-symbol "mo_plot_banner_alignment"	(ui-symbol-reference "MO_BOTTOM"))
;(ui-symbol "mo_plot_destination"        " ")
;(ui-symbol "mo_plot_format"				0)
;(ui-symbol "mo_plot_colour"				0)
;(ui-symbol "mo_plot_font_size"			10)

;RSE new symbols for print preview
;(ui-symbol "mo_printplot_scope"              (ui-symbol-reference "MO_PLOT_ALL"))
;(ui-symbol "mo_printplot_border"             #t)
;(ui-symbol "mo_printplot_auto_model_scale"   #f)
;(ui-symbol "mo_printplot_xoffset"            0)
;(ui-symbol "mo_printplot_yoffset"            0)

;(ui-symbol "mo_printplot_output"             0) ; PL_OUTPUT_FILE = 0, PL_OUTPUT_PLOTTER = 1
;(ui-symbol "mo_printplot_hidline"            #f)
;(ui-symbol "mo_printplot_units"              "cm")
;(ui-symbol "mo_printplot_position"           (ui-symbol-reference "MO_PLOT_MODE_MODEL_SCALE"))
;(ui-symbol "mo_printplot_center"             0)
;(ui-symbol "mo_printplot_rotate"             0)
;(ui-symbol "mo_printplot_scale"              1.0)
;(ui-symbol "mo_printplot_plotter_type"       0)
;(ui-symbol "mo_printplot_paper_size"         1)
;(ui-symbol "mo_printplot_xcorrection"        1.0)
;(ui-symbol "mo_printplot_ycorrection"        1.0)
;(ui-symbol "mo_printplot_model_scale"		1.0)
;(ui-symbol "mo_printplot_model_scale_mode_xcenter"	0.5)
;(ui-symbol "mo_printplot_model_scale_mode_ycenter"	0.5)
;(ui-symbol "mo_printplot_all_papers"			#t)
;(ui-symbol "mo_printplot_fit_to_paper"		#f)
;(ui-symbol "mo_printplot_arrow_size_cm"		0.4)
;(ui-symbol "mo_printplot_grids"				#t)
(ui-symbol "mo_printplot_hpgl_plotter_type"	"default")
(ui-symbol "mo_printplot_postscript_plotter_type"	"default")
(ui-symbol "mo_printplot_standards"          1)
(ui-symbol "mo_printplot_paper_type"			"A4V")
;(ui-symbol "mo_printplot_standards"          1)
(ui-symbol "mo_printplot_paper_type"			"A4")

;(ui-symbol "mo_printplot_number_paper_x"		1)
;(ui-symbol "mo_printplot_number_paper_y"		1)

(ui-symbol "mo_printplot_ll_window_wname_1"	(ui-symbol-reference "MO_BACK"))

(ui-symbol "mo_printplot_ll_window_wname_4"	(ui-symbol-reference "MO_LEFT"))
(ui-symbol "mo_printplot_lr_window_wname_4"	(ui-symbol-reference "MO_BACK"))
(ui-symbol "mo_printplot_ul_window_wname_4"	(ui-symbol-reference "MO_TOP"))
(ui-symbol "mo_printplot_ur_window_wname_4"	(ui-symbol-reference "MO_PERSP"))

(ui-symbol "mo_printplot_ll_window_wname_3"	(ui-symbol-reference "MO_LEFT"))
(ui-symbol "mo_printplot_lr_window_wname_3"	(ui-symbol-reference "MO_BACK"))
(ui-symbol "mo_printplot_ul_window_wname_3"	(ui-symbol-reference "MO_TOP"))
(ui-symbol "mo_printplot_ur_window_wname_3"	(ui-symbol-reference "MO_NO_WINDOW"))

;added by divakar for 1st angle an 3rd angle view
(ui-symbol "mo_printplot_ll_window_wname_firstangle"	(ui-symbol-reference "MO_TOP"))
(ui-symbol "mo_printplot_lr_window_wname_firstangle"	(ui-symbol-reference "MO_NO_WINDOW"))
(ui-symbol "mo_printplot_ul_window_wname_firstangle"	(ui-symbol-reference "MO_BACK"))
(ui-symbol "mo_printplot_ur_window_wname_firstangle"	(ui-symbol-reference "MO_LEFT"))

(ui-symbol "mo_printplot_ll_window_wname_thirdangle"	(ui-symbol-reference "MO_LEFT"))
(ui-symbol "mo_printplot_lr_window_wname_thirdangle"	(ui-symbol-reference "MO_BACK"))
(ui-symbol "mo_printplot_ul_window_wname_thirdangle"	(ui-symbol-reference "MO_NO_WINDOW"))
(ui-symbol "mo_printplot_ur_window_wname_thirdangle"	(ui-symbol-reference "MO_TOP"))

(ui-symbol "mo_printplot_bookmark"		0)
(ui-symbol "mo_print_mode"              0)

;(ui-symbol "mo_printplot_banner_alignment"	(ui-symbol-reference "MO_BOTTOM"))
;(ui-symbol "mo_printplot_destination"        " ")
;(ui-symbol "mo_printplot_format"				0)
;(ui-symbol "mo_printplot_colour"				0)
;(ui-symbol "mo_printplot_font_size"			10)

(ui-symbol "mo_newprint_printer_name"                    "")
(ui-symbol "mo_newprint_paper_size"                      "")
(ui-symbol "mo_newprint_output_style"                     0)
(ui-symbol "mo_newprint_show_background"                 #f)
(ui-symbol "mo_newprint_show_grid"                       #t)
(ui-symbol "mo_newprint_show_model"                      #t)
(ui-symbol "mo_newprint_show_canvases"                   #t)
(ui-symbol "mo_newprint_show_locators"                   #t)
(ui-symbol "mo_newprint_show_construction_objects"       #t)
(ui-symbol "mo_newprint_render_hidden_lines"             #f)
(ui-symbol "mo_newprint_show_curves"                     #t)
(ui-symbol "mo_newprint_show_surfaces"                   #t)
(ui-symbol "mo_newprint_show_cvs"						 #t)
(ui-symbol "mo_newprint_is_portrait"                     #t)
(ui-symbol "mo_newprint_destination_is_printer"          #t)
(ui-symbol "mo_newprint_size_width"                   792.0)
(ui-symbol "mo_newprint_size_height"                  612.0)
(ui-symbol "mo_newprint_dpi"                          300.0)
(ui-symbol "mo_newprint_scale"                          1.0)
(ui-symbol "mo_newprint_left_margin"                    0.0)
(ui-symbol "mo_newprint_right_margin"                   0.0)               
(ui-symbol "mo_newprint_top_margin"                     0.0)
(ui-symbol "mo_newprint_bottom_margin"                  0.0)
(ui-symbol "mo_newprint_interior_margin"                0.0)
(ui-symbol "mo_newprint_copies"                           1)
(ui-symbol "mo_newprint_line_width"                       1.0)
(ui-symbol "mo_newprint_placement_unit"                   0)
(ui-symbol "mo_newprint_margin_unit"                      0)
(ui-symbol "mo_newprint_x_offset"                       0.0)
(ui-symbol "mo_newprint_y_offset"                       0.0)
(ui-symbol "mo_newprint_x_align"                          1)
(ui-symbol "mo_newprint_y_align"                          1)
(ui-symbol "mo_newprint_window_aspect"                   #f)
(ui-symbol "mo_newprint_color_mode"                      #f)
(ui-symbol "mo_newprint_scale_option"                     1)
(ui-symbol "mo_newprint_win_x"                           0)
(ui-symbol "mo_newprint_win_y"                           0)
(ui-symbol "mo_newprint_win_w"                           -1)
(ui-symbol "mo_newprint_win_h"                           -1)
(ui-symbol "mo_newprint_show_window_borders"             #t)
(ui-symbol "mo_newprint_mod_conflicting_colours"         #f)
(ui-symbol "mo_newprint_show_margin_borders"             #t)

; Output Options
(ui-symbol  "tf_Output_Printer" 1)
(ui-symbol  "tf_Output_Format" 0)
(ui-symbol  "tf_Output_Colour" 1)
(ui-symbol  "tf_Output_PrintQuality" 0)
(ui-symbol  "tf_Output_PlotterType" 0)
;(ui-symbol "tf_Output_Appearence"
(ui-symbol  "tf_Output_Range" 1)
(ui-symbol  "tf_Output_Frompage" 1)
(ui-symbol  "tf_Output_Topage" 1)
(ui-symbol  "tf_Output_NoofCopies" 1)
;(ui-symbol "tf_Output_Str"
(ui-symbol  "tf_Printer_Name" "")
(ui-symbol  "tf_Printer_Name_Sys" "")

(ui-symbol  "tf_Printer_Name_1" "")
(ui-symbol  "tf_Printer_Name_2" "")
(ui-symbol  "tf_Printer_Name_3" "")
(ui-symbol  "tf_Printer_Name_4" "")
(ui-symbol  "tf_Printer_Name_5" "")

;(ui-symbol  "tf_Printer_Index" 0)

; Paper Options
(ui-symbol  "tf_Paper_Type" 0)

(ui-symbol  "tf_Paper_Standard" 1)
;1
(ui-symbol  "tf_Paper_sizeAnsi" 0)
;9
(ui-symbol  "tf_Paper_sizeIso" 0)
;5
(ui-symbol  "tf_Paper_sizeArch" 0)
;1
(ui-symbol  "tf_Paper_sizeOther" 0)

(ui-symbol  "tf_Paper_RollfeedWidth_cm" 254.00)
(ui-symbol  "tf_Paper_RollfeedHeight_cm" 254.00)
(ui-symbol  "tf_Paper_RollfeedWidth_in" 100.00)
(ui-symbol  "tf_Paper_RollfeedHeight_in" 100.00)
(ui-symbol  "tf_Paper_Orientation" 0)
(ui-symbol  "tf_Paper_Rotate" 2)
(ui-symbol  "tf_Paper_Interactive" 0)

; Border Options
(ui-symbol  "tf_Border_Cropmarks" 0)
;(ui-symbol  "tf_Border_Regmarks"
(ui-symbol  "tf_Border_DrawBorder" 1)
(ui-symbol  "tf_Border_DrawRuler" 0)
(ui-symbol  "tf_Border_DrawGrid" 1)
(ui-symbol  "tf_Border_Thickness_mm" 0.5)
(ui-symbol  "tf_Border_Topmargin_mm" 5)
(ui-symbol  "tf_Border_Botmargin_mm" 5)
(ui-symbol  "tf_Border_Ltmargin_mm" 5)
(ui-symbol  "tf_Border_Rtmargin_mm" 5)

(ui-symbol  "tf_Border_Title" "")
(ui-symbol  "tf_Border_Name" "")
(ui-symbol  "tf_Border_Company" "")
(ui-symbol  "tf_Border_Date" "")
(ui-symbol  "tf_Border_Number" "")
(ui-symbol  "tf_Border_Scale" "1:1")
(ui-symbol  "tf_Border_Notes" "")
(ui-symbol  "tf_Border_FileName" "")
(ui-symbol  "tf_Border_DrawTitleBox" 1)

; Object Options
(ui-symbol  "tf_Object_Objects" 0)
(ui-symbol  "tf_Object_Viewingtype" 1)
(ui-symbol  "tf_Object_ScaleFactorType" 1)
(ui-symbol  "tf_Object_Screen_Scale" 1.0)
(ui-symbol  "tf_Object_Model_Scale" 1.0)

(ui-symbol  "tf_Object_Str" "1:1")

; Draw Options
;(ui-symbol  "tf_Draw_Linecolor"
;(ui-symbol  "tf_Draw_Dimline"
(ui-symbol  "tf_Grid_Thickness_mm" 0.025)
(ui-symbol  "tf_Draw_FilledArrow" 0)
(ui-symbol  "tf_Draw_ArrowWidth_mm" 2)
(ui-symbol  "tf_Draw_ArrowLength_mm" 4)
(ui-symbol  "tf_Draw_LocatorWidth_mm" 0.2)
(ui-symbol  "tf_Draw_LayerWidth_mm" 0.2)

; Print/plot Font Settings
(ui-symbol  "tf_TBoxFont.fontsize" 10)
(ui-symbol  "tf_LocFont.override" #f)
(ui-symbol  "tf_LocFont.fontsize" 10)
(ui-symbol  "tf_GridFont.override" #f)
(ui-symbol  "tf_GridFont.fontsize" 10)

; Border Options for inch slider
(ui-symbol  "tf_Border_Topmargin_in" 0.197)
(ui-symbol  "tf_Border_Botmargin_in" 0.197)
(ui-symbol  "tf_Border_Ltmargin_in"  0.197)
(ui-symbol  "tf_Border_Rtmargin_in"  0.197)

; Draw options for inch slider
(ui-symbol  "tf_Grid_Thickness_in"  0.025)
(ui-symbol  "tf_Draw_ArrowWidth_in"  0.110)
(ui-symbol  "tf_Draw_ArrowLength_in" 0.354)
(ui-symbol  "tf_Draw_LocatorWidth_in" 0.007)
(ui-symbol  "tf_Draw_LayerWidth_in" 0.007)
(ui-symbol  "tf_Border_Thickness_in" 0.002)

(ui-symbol  "tf_Draw_LocatorColor_ValR" 0)
(ui-symbol  "tf_Draw_LocatorColor_ValG" 0)
(ui-symbol  "tf_Draw_LocatorColor_ValB" 0)

; Layout Options
;(ui-symbol  "tf_Layout_Objectpos"
(ui-symbol  "tf_Layout_Style" 2)
(ui-symbol  "tf_Layout_Syncview" 1)
(ui-symbol  "tf_Layout_MatchPaperBorder" 1)
(ui-symbol  "tf_View_CMYK" 0)

; Hidden Line Plot Options
(ui-symbol  "tf_HiddenLine_enabled" #f)
(ui-symbol  "tf_HiddenLine_tess_useExisting" #t)
(ui-symbol  "tf_HiddenLine_tess_type" 0)
(ui-symbol  "tf_HiddenLine_tess_tolerance" 0.01)
(ui-symbol  "tf_HiddenLine_tess_limitEdgeLength" #f)
(ui-symbol  "tf_HiddenLine_tess_maxEdgeLength" 1.0)

; Image Print Options
(ui-symbol  "tf_ImagePrint_orient" 1)
(ui-symbol  "tf_ImagePrint_top" 0.5)
(ui-symbol  "tf_ImagePrint_left" 0.5)
(ui-symbol  "tf_ImagePrint_width" 11.5)
(ui-symbol  "tf_ImagePrint_height" 8.0)
(ui-symbol  "tf_ImagePrint_fitToPage" #t)
(ui-symbol  "tf_ImagePrint_center" #t)

(ui-symbol "mo_image_mode"              (ui-symbol-reference "MO_MODE_RGB"))
(ui-symbol "mo_image_mask"              (ui-symbol-reference "MO_MASK_OFF"))
(ui-symbol "mo_image_depth_type"        (ui-symbol-reference "MO_DEPTH_OFF"))
(ui-symbol "mo_image_depth"             1.0)
(ui-symbol "mo_image_crop"              #f)
(ui-symbol "mo_image_dim"               #f)
(ui-symbol "mo_image_rgb_mult"          0.55)
(ui-symbol "mo_image_rgb_offset"        0.55)
(ui-symbol "mo_image_size"				(ui-symbol-reference "MO_IMAGE_SIZE_FIT"))
(ui-symbol "mo_image_horizontal"		(ui-symbol-reference "MO_IMAGE_HORIZONTAL"))
(ui-symbol "mo_image_vertical"			(ui-symbol-reference "MO_IMAGE_VERTICAL"))
(ui-symbol "mo_image_aspect_ratio"		(ui-symbol-reference "MO_IMAGE_ASPECT_FIXED"))

; make picture options (SID)

(ui-symbol "mo_imagelayer_file_type"    (ui-symbol-reference "MO_FILETYPE_TIFF"))
(ui-symbol "mo_imagelayer_resize"       #f)
(ui-symbol "mo_imagelayer_limit_size"   #f)
(ui-symbol "mo_imagelayer_max_x"        1280)
(ui-symbol "mo_imagelayer_max_y"        1024)
(ui-symbol "mo_imagelayer_q_factor"     90)
(ui-symbol "mo_imagelayer_q_level"      (ui-symbol-reference "MO_Q_HIGH"))
(ui-symbol "mo_makepicture_blendBkgd"   #t)
(ui-symbol "mo_makepicture_masktoimage" #f)


; SLA options

(ui-symbol "mp_slc_command"         	"ExportSLC")
(ui-symbol "mo_slc_target"             (ui-symbol-reference "MO_INCHES"))
(ui-symbol "mo_slc_model_type"         (ui-symbol-reference "MO_SLC_TYPE_PART"))
(ui-symbol "mo_slc_auto_range"     		#t)
(ui-symbol "mo_slc_display"             #f)
(ui-symbol "mo_slc_step_z"    	      0.01)
(ui-symbol "mo_slc_start_z"          -10.0)
(ui-symbol "mo_slc_end_z"             10.0)

; Showcaseout options

(ui-symbol "mo_showcaseout_tess_setting"            0 )
(ui-symbol "mo_showcaseout_geometry"  (ui-symbol-reference "MO_SAVE_ALL_AS"))
(ui-symbol "mo_showcaseout_bake_ao"                 #t)
(ui-symbol "mo_showcaseout_replace_materials"       #t)
(ui-symbol "mo_showcaseout_replace_material_map"    "")
(ui-symbol "mo_showcaseout_visual_style"            3)
(ui-symbol "mo_showcaseout_convert_bookmarks"       #t)
(ui-symbol "mo_showcaseout_convert_env"                 #t)
(ui-symbol "mo_showcaseout_ground_plane"            1)
(ui-symbol "mo_showcaseout_environment"             0)
(ui-symbol "mo_showcaseout_center_env"              #t)

; VRED options
(ui-symbol "mo_vredout_geometry"            (ui-symbol-reference "MO_SAVE_ALL_AS"))
(ui-symbol "mo_vredout_keep_nurbs"          #t)
(ui-symbol "mo_vredout_chord_deviation"     0.075)
(ui-symbol "mo_vredout_normal_tolerance"    10.0)
(ui-symbol "mo_vredout_max_chord_length"    100.0)
(ui-symbol "mo_vredout_enable_stitching"    #t)
(ui-symbol "mo_vredout_stitching_tolerance" 0.1)
(ui-symbol "mo_vredout_merge_geometries"    #t)
(ui-symbol "mo_vredout_want_new_scene"      #t)
(ui-symbol "mo_vredout_translator_ui"       0)

; primitive options

(ui-symbol "mo_prim_type" 			(ui-symbol-reference "MO_SPHERE"))
(ui-symbol "mo_prim_geometry_type" 	(ui-symbol-reference "MO_BSPLINE"))
(ui-symbol "mo_prim_caps" 			(ui-symbol-reference "MO_TWO_CAPS"))
(ui-symbol "mo_sections" 			8)
(ui-symbol "mo_sweep" 				360.0)
(ui-symbol "mo_ratio"               0.4)

; Sphere options

(ui-symbol "mo_prim_sphere_type"    (ui-symbol-reference "MO_PRIM_SPH_NURBS"))
(ui-symbol "mo_sphere_geometry_type" 	(ui-symbol-reference "MO_BSPLINE"))
(ui-symbol "mo_sphere_sections"			8)
(ui-symbol "mo_sphere_sweep" 			360.0)

; Torus options

(ui-symbol "mo_torus_sweep"            360.0)
(ui-symbol "mo_torus_axis_ratio"       0.2)
(ui-symbol "mo_torus_major_radius"	   0.4)
(ui-symbol "mo_torus_minor_radius"	   0.1)
(ui-symbol "mo_torus_radius_abs"	   1)

; Ellipse options

(ui-symbol "mo_ellipse_sweep"           360.0)
(ui-symbol "mo_ellipse_axis_ratio"      0.5)
(ui-symbol "mo_ellipse_build_method"   (ui-symbol-reference "MO_ELLIPSE_DEFINE_SEMIMAJOR"))

; Circle options

(ui-symbol "mo_circle_periodic_degree"  5)
(ui-symbol "mo_circle_periodic_spans"   12)
(ui-symbol "mo_circle_sweep" 			360.0)

(ui-symbol "mo_circle_periodic_mode"   #t)
(ui-symbol "mo_circle_degree"           5)
(ui-symbol "mo_circle_spans"            1)
(ui-symbol "mo_circle_temp"            16)
(ui-symbol "mo_circle_segments"         1)

(ui-symbol "mo_keypoint_circle_degree" 6)
(ui-symbol "mo_keypoint_circle_spans"  1)

; Arc tools options

(ui-symbol "mo_arc3Point_degree"                6)
(ui-symbol "mo_arc3Point_spans"                 1)
(ui-symbol "mo_arc3Point_temp"                 16)

(ui-symbol "mo_arc2Point_degree"                6)
(ui-symbol "mo_arc2Point_spans"                 1)
(ui-symbol "mo_arc2Point_temp"                 16)

(ui-symbol "mo_arcConcentric_degree"            6)
(ui-symbol "mo_arcConcentric_spans"             1)
(ui-symbol "mo_arcConcentric_temp"             16)

(ui-symbol "mo_arcTangent_degree"               6)
(ui-symbol "mo_arcTangent_spans"                1)
(ui-symbol "mo_arcTangent_temp"                16)

; Line tools options

(ui-symbol "mo_keypoint_line2Point_degree"      1)
(ui-symbol "mo_keypoint_lineParallel_degree"    1)
(ui-symbol "mo_keypoint_linePoly_degree"        1)
(ui-symbol "mo_keypoint_lineAngle_degree"       1)
(ui-symbol "mo_keypoint_linePerp_degree"        1)
(ui-symbol "mo_keypoint_linePerp_type"          1)
(ui-symbol "mo_keypoint_linePerp_mode"          1)

; Cylinder options

(ui-symbol "mo_cylinder_degree" 		3)
(ui-symbol "mo_cylinder_caps" 			(ui-symbol-reference "MO_TWO_CAPS"))
(ui-symbol "mo_cylinder_sections"			8)
(ui-symbol "mo_cylinder_sweep" 			360.0)

; Cone options

(ui-symbol "mo_cone_degree" 			3)
(ui-symbol "mo_cone_caps" 			(ui-symbol-reference "MO_ONE_CAP"))
(ui-symbol "mo_cone_sections"			8)
(ui-symbol "mo_cone_sweep" 				360.0)

; Cube options
(ui-symbol "mo_cube_geometry_type" 		(ui-symbol-reference "MO_BSPLINE"))

; Plane options
(ui-symbol "mo_plane_geometry_type" 	(ui-symbol-reference "MO_BSPLINE"))

; Projective texture options
(ui-symbol "projtxt_projtype"			(ui-symbol-reference "PTXT_PLANAR"))

; planar proj options
(ui-symbol "projtxt_planarCenter"		0)
(ui-symbol "projtxt_editOnCreate.planar" 0)
(ui-symbol "projtxt_snapBox.planar"		0)
(ui-symbol "projtxt_drawBox.planar"			#f)
(ui-symbol "projtxt_uniformSnap.planar"		#f)

; concentric proj options
(ui-symbol "projtxt_editOnCreate.conc"		0)
(ui-symbol "projtxt_snapBox.conc"			0)
(ui-symbol "projtxt_drawBox.conc"			#f)
(ui-symbol "projtxt_uniformSnap.conc"		#f)

; triplanar proj options
(ui-symbol "projtxt_editOnCreate.tri"		0)
(ui-symbol "projtxt_snapBox.tri"			0)
(ui-symbol "projtxt_drawBox.tri"			#f)
(ui-symbol "projtxt_uniformSnap.tri"		#f)

; sphere proj options
(ui-symbol "projtxt_editOnCreate.sph"		0)
(ui-symbol "projtxt_snapBox.sph"			0)
(ui-symbol "projtxt_drawBox.sph"			#f)
(ui-symbol "projtxt_uniformSnap.sph"		#f)

; ball proj options
(ui-symbol "projtxt_editOnCreate.ball"		0)
(ui-symbol "projtxt_snapBox.ball"			0)
(ui-symbol "projtxt_drawBox.ball"			#f)
(ui-symbol "projtxt_uniformSnap.ball"		#f)

; cylindrical proj options
(ui-symbol "projtxt_editOnCreate.cyl"		0)
(ui-symbol "projtxt_snapBox.cyl"			0)
(ui-symbol "projtxt_drawBox.cyl"			#f)
(ui-symbol "projtxt_uniformSnap.cyl"		#f)

; cubic proj options
(ui-symbol "projtxt_editOnCreate.cub"		0)
(ui-symbol "projtxt_snapBox.cub"			0)
(ui-symbol "projtxt_drawBox.cub"			#f)
(ui-symbol "projtxt_uniformSnap.cub"		#f)

; camera proj options
(ui-symbol "projtxt_editOnCreate.camera"	0)

(ui-symbol "projtxt_cameraSnap"			#t)

; ungroup options

(ui-symbol "mo_ungroup_method"   (ui-symbol-reference "MO_UNGROUP_DELETE"))
(ui-symbol "mo_ungroup_compensate" #t)


; group options

(ui-symbol "mo_group_compensate"        #t)
(ui-symbol "mo_group_under"             #t)


; set creation options

(ui-symbol "mo_set_type"				(ui-symbol-reference "MO_SET_MULTI"))

; cluster creation options

(ui-symbol "mo_cluster_type"			(ui-symbol-reference "MO_CLUSTER_EXCLUSIVE"))

; pick object options

(ui-symbol "mo_pick_layered_object"     #f)

(ui-symbol "mo_pick_lights"             #t)
(ui-symbol "mo_pick_scans"              #t)
(ui-symbol "mo_pick_faces"              #t)
(ui-symbol "mo_pick_curves"             #t)
(ui-symbol "mo_pick_surfaces"           #t)
(ui-symbol "mo_pick_shells"             #t)
(ui-symbol "mo_pick_constr_obj"			#t)
(ui-symbol "mo_pick_others"             #t)
(ui-symbol "mo_pick_meshes"             #t)
(ui-symbol "mo_pick_disp_pt"            #t) ; obsolete
(ui-symbol "mo_pick_disp_vec"           #t) ; obsolete
(ui-symbol "mo_pick_disp_plane"         #t) ; obsolete

(ui-symbol "mo_pick_disp_measure"       #t)
(ui-symbol "mo_pick_disp_deviation"     #t)
(ui-symbol "mo_pick_disp_other"         #t)

; pick component options
(ui-symbol "mo_pick_all"                #t)
(ui-symbol "mo_pick_surface_type"		 2)

; pick by name options

(ui-symbol "mo_pickname_active"         #f)
(ui-symbol "mo_pickname_string"         "sets")

; pick image plane options
(ui-symbol "mo_pick_image_function"     "PickImagePlane")

; pick reference options
(ui-symbol "mo_pick_reference_level" 1)
(ui-symbol "mo_pick_reference_curves" #t)
(ui-symbol "mo_pick_reference_surfaces" #t)
(ui-symbol "mo_pick_reference_shells" #t)
(ui-symbol "mo_pick_reference_meshes" #t)

; pick curve on surface options
(ui-symbol "mo_pick_cos_visual"		#t)
(ui-symbol "mo_pick_cos_geometry"	#t)

; ungroup options

(ui-symbol "mo_ungrp_type"              (ui-symbol-reference "MO_GROUP_HIER"))


; light options

(ui-symbol "mo_light_type"              (ui-symbol-reference "MO_POINT"))
(ui-symbol "mo_decay"                   1)
(ui-symbol "mo_lightr"                  255)
(ui-symbol "mo_lightg"                  255)
(ui-symbol "mo_lightb"                  255)
(ui-symbol "mo_intensity"               1.0)
(ui-symbol "mo_dropoff"                 20.0)
(ui-symbol "mo_cutoff"                  90.0)
(ui-symbol "mo_light_dirx"              0)
(ui-symbol "mo_light_diry"              0)
(ui-symbol "mo_light_dirz"              0)


; copy options

(ui-symbol "mo_copy_function"           "ModelCopyGroupOn")

(ui-symbol "mo_copy_geom_type"          (ui-symbol-reference "MO_AS_COPY"))
(ui-symbol "mo_cpynumber"               1)
(ui-symbol "mo_xlatex"                  0.0)
(ui-symbol "mo_xlatey"                  0.0)
(ui-symbol "mo_xlatez"                  0.0)
(ui-symbol "mo_rotatex"                 0.0)
(ui-symbol "mo_rotatey"                 0.0)
(ui-symbol "mo_rotatez"                 0.0)
(ui-symbol "mo_scalex"                  1.0)
(ui-symbol "mo_scaley"                  1.0)
(ui-symbol "mo_scalez"                  1.0)
(ui-symbol "mo_cpgroup"                 #t)
(ui-symbol "mo_copy_geom_mode"                  (ui-symbol-reference "MO_COPY_GEOM_MODE_FRACTIONAL"))
(ui-symbol "mo_copy_geom_vectoru"               1.0)
(ui-symbol "mo_copy_geom_vectorv"               0.0)
(ui-symbol "mo_copy_geom_distance"              1.0)
(ui-symbol "mo_copy_xyz_or_uv_space"                    (ui-symbol-reference "MO_COPY_XYZ_SPACE"))
(ui-symbol "mo_copy_geom_dir"			(ui-symbol-reference "MO_COPY_GEOM_MODE_AUTO_DIR"))


; NOTE : if mo_copy_geom_type = 'MO_AS_INST, mo_cpygroup MUST be #t
; close options

(ui-symbol "mo_insert_knots"            #f)
(ui-symbol "mo_close_fudge"             50)
(ui-symbol "mo_close_save_shape"        #f)

; insert options

(ui-symbol "mo_insert_type"				1)

; extend default options

(ui-symbol "mo_extend_type"             (ui-symbol-reference "MO_EXTEND_TYPE_CUBIC"))
(ui-symbol "mo_extend_merge"            #t)
(ui-symbol "mo_extend_length"           0.0)
(ui-symbol "mo_extend_percent"          0.0)
(ui-symbol "mo_extend_chain"            #f)
(ui-symbol "mo_extend_method"			1)

; reverse direction options

(ui-symbol "mo_reverse_dir"             (ui-symbol-reference "MO_REV_U"))


; edit surface normals options

(ui-symbol "srfnorm_all_intersections"  #f)

; edit surface normals options

(ui-symbol "srfuvs_reverse_dir"        (ui-symbol-reference "MO_REV_U"))
(ui-symbol "srfuvs_all_intersections"  #f)

; fair (smooth) options

(ui-symbol "mo_smooth_method"           (ui-symbol-reference "MO_KNOT_REMOVAL"))
(ui-symbol "mo_smooth_axis"             (ui-symbol-reference "MO_SMOOTH_ALL"))
(ui-symbol "mo_smooth_direction"        (ui-symbol-reference "MO_SMOOTH_BOTH"))
(ui-symbol "mo_cont_startu"             (ui-symbol-reference "MO_SMOOTH_CONT_G1"))
(ui-symbol "mo_cont_endu"               (ui-symbol-reference "MO_SMOOTH_CONT_G1"))
(ui-symbol "mo_cont_startv"             (ui-symbol-reference "MO_SMOOTH_CONT_G1"))
(ui-symbol "mo_cont_endv"               (ui-symbol-reference "MO_SMOOTH_CONT_G1"))


; end tangent options

(ui-symbol "mo_start_u_tan"             (ui-symbol-reference "MO_STATIC"))
(ui-symbol "mo_start_v_tan"             (ui-symbol-reference "MO_STATIC"))
(ui-symbol "mo_end_u_tan"               (ui-symbol-reference "MO_STATIC"))
(ui-symbol "mo_end_v_tan"               (ui-symbol-reference "MO_STATIC"))


; Offset options  -- will be obsolete soon

(ui-symbol "mo_offset_connect_breaks"   1)
(ui-symbol "mo_offset_loop_cutting"     #t)
(ui-symbol "mo_offset_arc_radius"       0.0)
(ui-symbol "mo_offset_plane"            (ui-symbol-reference "MO_OFFSET_PLANE_ACTIVE"))
(ui-symbol "mo_offset_cos_distance_domain" (ui-symbol-reference "MO_OFFSET_COS_WORLD"))
(ui-symbol "mo_offset_subdiv"           5.0)


; bevel options

(ui-symbol "mo_bevel_depth"             0.1)
(ui-symbol "mo_bevel_width"             0.1)
(ui-symbol "mo_bevel_result_depth"      1.0)
(ui-symbol "mo_bevel_both_sides"        #t)
(ui-symbol "mo_bevel_front_cap"         #t)
(ui-symbol "mo_bevel_back_cap"          #t)
(ui-symbol "mo_bevel_keep_originals"    #t)
(ui-symbol "mo_bevel_connect_circular"  #t)


; fillet options

(ui-symbol "mo_ff_constrn"              (ui-symbol-reference "MO_FF_CONSTRN_CIRC"))

(ui-symbol "mo_ff_calculate" (ui-symbol-reference "MO_FF_CALC_KNEE_RATIO"))

(ui-symbol "mo_ff_radius"           10.0)

(ui-symbol "mo_ff_knee_ratio"           1.0)
(ui-symbol "mo_ff_lead_radius" (ui-symbol-reference 'mo_ff_radius))

(ui-symbol "mo_ff_blend"                #f)
(ui-symbol "mo_ff_type"                 (ui-symbol-reference "MO_FF_TYPE_BLEND"))
(ui-symbol "mo_ff_trim"                 #f)
(ui-symbol "mo_ff_history"              #t)

(if (ui-check-option "advancedmodeling_module" )
	(ui-symbol "mo_ff_continuity"       #t)
	(ui-symbol "mo_ff_continuity"       #f)
)

; curve fillet options (same command, but different defaults,
; which can be stored separately)

(ui-symbol "mo_crv_ff_constrn" (ui-symbol-reference "MO_FF_CONSTRN_CIRC"))
(ui-symbol "mo_crv_ff_calculate" (ui-symbol-reference "MO_FF_CALC_KNEE_RATIO"))
(ui-symbol "mo_crv_ff_type"    (ui-symbol-reference "MO_FF_TYPE_BLEND"))

(ui-symbol "mo_crv_ff_radius"           10.0)

(ui-symbol "mo_crv_ff_knee_ratio"           1.0)
(ui-symbol "mo_crv_ff_lead_radius" (ui-symbol-reference 'mo_crv_ff_radius))

(ui-symbol "mo_crv_ff_blend"   #f)
(ui-symbol "mo_crv_ff_trim"    #t)
(ui-symbol "mo_crv_ff_history" #t)
(if (ui-check-option "advancedmodeling_module" )
	(ui-symbol "mo_crv_ff_continuity"       #t)
	(ui-symbol "mo_crv_ff_continuity"       #f)
)

; fillet options

(ui-symbol "mo_fillet_radius"           10000)
(ui-symbol "mo_fillet_tolrnc"           10)
(ui-symbol "mo_flt_profile_dist"        2000)
(ui-symbol "mo_fillet_autopos"          #f)
(ui-symbol "mo_fillet_pos"              #t)
(ui-symbol "mo_fillet_trim"             #f)
;
; fillet curve options

(ui-symbol "mo_curve_fillet_constr_method"			1)
(ui-symbol "mo_curve_fillet_section_type"			2)
(ui-symbol "mo_curve_fillet_curvature_side"			0)

(ui-symbol "mo_curve_fillet_chordal_type"			1)

(ui-symbol "mo_curve_fillet_chordal_length"			1.0)
(ui-symbol "mo_curve_fillet_outer_radius"			1.0)
(ui-symbol "mo_curve_fillet_center_radius"			0.5)
(ui-symbol "mo_curve_fillet_form_factor"			1.0)
(ui-symbol "mo_curve_fillet_parameter_type"			1)
(ui-symbol "mo_curve_fillet_form_factor_version"	2014)

(ui-symbol "mo_curve_fillet_explicit_control"		#f)
(ui-symbol "mo_curve_fillet_degree"					5)
(ui-symbol "mo_curve_fillet_spans"					1)

(ui-symbol "mo_curve_fillet_fillet_plane_type"		0)
(ui-symbol "mo_curve_fillet_fillet_plane_name"		"")
(ui-symbol "mo_curve_fillet_fillet_plane_presets"	2)
(ui-symbol "mo_curve_fillet_fillet_plane_refresh"	0)
(ui-symbol "mo_curve_fillet_fillet_plane_save"		0)
(ui-symbol "mo_curve_fillet_fillet_plane_create"	0)

(ui-symbol "mo_curve_fillet_create_history"			#t)
(ui-symbol "mo_curve_fillet_auto_recalc"			#f)
(ui-symbol "mo_curve_fillet_trim_type"				0)
(ui-symbol "mo_curve_fillet_continuity_check"		#f)
(ui-symbol "mo_curve_fillet_debug_geometry"			#f)
(ui-symbol "mo_curve_fillet_curvature_comb"			#f)

; fillet surface options

(ui-symbol "mo_fillet_srf_constr_method"			(ui-symbol-reference 'MO_FILLET_SRF_CONSTR_TYPE_CONSTANT))
(ui-symbol "mo_fillet_srf_surface_type"				(ui-symbol-reference 'MO_FILLET_SRF_MULTIPLE_SURFACES))
(ui-symbol "mo_fillet_srf_radius_type"			    (ui-symbol-reference 'MO_FILLET_SRF_SECTION_TYPE_G1TANGENT))

(ui-symbol "mo_fillet_srf_variable_mode"		    #f)
(ui-symbol "mo_fillet_srf_chordal_type"				(ui-symbol-reference 'MO_FILLET_SRF_CHORDAL_TYPE_CHORDAL_DISTANCE))

(ui-symbol "mo_fillet_srf_curvature_in_bias"		0)
(ui-symbol "mo_fillet_srf_curvature_toggle"			0)

(if (ui-check-option "advancedmodeling_module" )
        (begin
			(ui-symbol "mo_fillet_srf_radius"			1.0)
			(ui-symbol "mo_fillet_srf_chord_distance"	1.0)
			(ui-symbol "mo_fillet_srf_lead_radius"		1.0)
        )

		(ui-symbol "mo_fillet_srf_radius"				 1.0)
		(ui-symbol "mo_fillet_srf_chord_distance"		 1.0)
		(ui-symbol "mo_fillet_srf_lead_radius"			 1.0)
)

(ui-symbol "mo_fillet_srf_single_span"			  #f)
(ui-symbol "mo_fillet_srf_explicit_control"		  #f)
(ui-symbol "mo_fillet_srf_u_degree"				   5)
(ui-symbol "mo_fillet_srf_v_degree"				   3)
(ui-symbol "mo_fillet_srf_uniform_spans"		   0)
(ui-symbol "mo_fillet_srf_max_num_spans"		 100)
(ui-symbol "mo_fillet_srf_num_uniform_spans"	   1)
(ui-symbol "mo_fillet_srf_parameter_type"		   1)
(ui-symbol "mo_fillet_srf_lead_type"			   1)
(ui-symbol "mo_fillet_srf_knee_ratio"			 1.0)
(ui-symbol "mo_fillet_srf_bias"					  #f)
(ui-symbol "mo_fillet_srf_bias_factor"			 0.0)
(ui-symbol "mo_fillet_srf_use_central_K"		  #f)
(ui-symbol "mo_fillet_srf_central_K_radius"		 0.5)
(ui-symbol "mo_fillet_srf_central_K_ratio"		 0.5)
(ui-symbol "mo_fillet_srf_start_edge_flow"		   1)
(ui-symbol "mo_fillet_srf_interior_flow"		   5)
(ui-symbol "mo_fillet_srf_end_edge_flow"		   1)

(ui-symbol "mo_fillet_srf_primary_clip" #f )
(ui-symbol "mo_fillet_srf_primary_clip_start" 0.0)
(ui-symbol "mo_fillet_srf_primary_clip_end" 1.0)
(ui-symbol "mo_fillet_srf_secondary_clip" #f )
(ui-symbol "mo_fillet_srf_secondary_clip_start" 0.0)
(ui-symbol "mo_fillet_srf_secondary_clip_end" 1.0)

(ui-symbol "mo_fillet_srf_create_history"		  #t)
(ui-symbol "mo_fillet_srf_auto_recalc"			  #f)
(ui-symbol "mo_fillet_srf_trim_type"			  (ui-symbol-reference 'MO_FILLET_SRF_TRIM_TYPE_AUTOMATIC))
(ui-symbol "mo_fillet_srf_continuity_check"		  #f)
(ui-symbol "mo_fillet_srf_curvature_comb"		  #f)
(ui-symbol "mo_fillet_srf_short_edge_tol"      0.001)
(ui-symbol "mo_fillet_srf_is_G3_curvature"		  #f)
(ui-symbol "mo_fillet_srf_center_radius"		0.5)
(ui-symbol "mo_fillet_srf_form_factor"			0.5)
(ui-symbol "mo_fillet_srf_form_factor_version"	2014)
(ui-symbol "mo_fillet_srf_use_minimum_radius"	#f)
(ui-symbol "mo_fillet_srf_minimum_radius"		3.14)

; freeform fillet options

(ui-symbol "mo_freeform_blend_constr_method"			(ui-symbol-reference 'MO_FILLET_SRF_CONSTR_TYPE_FREEFORM))
(ui-symbol "mo_freeform_blend_surface_type"		(ui-symbol-reference 'MO_FILLET_SRF_MULTIPLE_SURFACES))
(ui-symbol "mo_freeform_blend_section_type"			(ui-symbol-reference 'MO_FILLET_SRF_SECTION_TYPE_G1CIRCULAR))
(ui-symbol "mo_freeform_blend_Aside_continuity"			(ui-symbol-reference 'MO_FILLET_SRF_TANGENT_CONTINUITY))
(ui-symbol "mo_freeform_blend_Bside_continuity"			(ui-symbol-reference 'MO_FILLET_SRF_TANGENT_CONTINUITY))

(ui-symbol "mo_freeform_blend_curvature_in_bias"	   0)
(ui-symbol "mo_freeform_blend_curvature_toggle"		   0)

(ui-symbol "mo_freeform_blend_single_span"			  #f)
(ui-symbol "mo_freeform_blend_explicit_control"		  #f)
(ui-symbol "mo_freeform_blend_u_degree"				   5)
(ui-symbol "mo_freeform_blend_max_num_spans"		 100)
(ui-symbol "mo_freeform_blend_lead"					  #f)
(ui-symbol "mo_freeform_blend_knee_ratio"			 1.0)
(ui-symbol "mo_freeform_blend_bias_factor"			 0.0)
(ui-symbol "mo_freeform_blend_use_central_K"		  #f)
(ui-symbol "mo_freeform_blend_central_K_ratio"		 0.5)
(ui-symbol "mo_freeform_blend_form_factor" 1.0)
(ui-symbol "mo_freeform_blend_form_factor_version" 2014)
(ui-symbol "mo_freeform_blend_center_radius" 0.5)

(if (ui-check-option "coremodeling_module" )
	(ui-symbol "mo_freeform_blend_start_edge_flow"		3)
	(ui-symbol "mo_freeform_blend_start_edge_flow"		1)
)
(ui-symbol "mo_freeform_blend_interior_flow"		   5)
(if (ui-check-option "coremodeling_module" )
	(ui-symbol "mo_freeform_blend_end_edge_flow"		3)
	(ui-symbol "mo_freeform_blend_end_edge_flow"		1)
)
(ui-symbol "mo_freeform_blend_primary_clip" #f)
(ui-symbol "mo_freeform_blend_primary_clip_start" 0.0)
(ui-symbol "mo_freeform_blend_primary_clip_end" 1.0)
(ui-symbol "mo_freeform_blend_secondary_clip" #f)
(ui-symbol "mo_freeform_blend_secondary_clip_start" 0.0)
(ui-symbol "mo_freeform_blend_secondary_clip_end" 1.0)
(ui-symbol "mo_freeform_blend_is_G3_curvature"		  #f)
(ui-symbol "mo_freeform_blend_symmetric"			  #f)
(ui-symbol "mo_freeform_blend_symmetric_continuity"	  1)
(ui-symbol "mo_freeform_blend_symmetric_vdegree"	  3)
(ui-symbol "mo_freeform_blend_symmetric_peak"		  #f)


(ui-symbol "mo_freeform_blend_auto_recalc"			  #f)
(ui-symbol "mo_freeform_blend_continuity_check"		  #f)
(ui-symbol "mo_freeform_blend_curvature_comb"		  #f)
(ui-symbol "mo_freeform_blend_short_edge_tol"	   0.001)
(ui-symbol "mo_freeform_blend_shape_slider"			 1.0)
(ui-symbol "mo_freeform_blend_shape_sliderB"		 1.0)
(ui-symbol "mo_freeform_blend_pick_chain"			  #f)
(ui-symbol "mo_freeform_blend_shape_lock"			  #t)
(ui-symbol "mo_freeform_blend_use_form_factor_math"	  #f)

(ui-symbol "mo_freeform_blend_range_primary"	           #f)
(ui-symbol "mo_freeform_blend_range_secondary"          #f)
(ui-symbol "mo_freeform_blend_range_primary_start"	     0.0)
(ui-symbol "mo_freeform_blend_range_primary_end"		  1.0)
(ui-symbol "mo_freeform_blend_range_secondary_start"	  0.0)
(ui-symbol "mo_freeform_blend_range_secondary_end"		  1.0)

(ui-symbol "mo_freeform_blend_prop_crown"			  #f)
(ui-symbol "mo_freeform_blend_prop_crown_val"		 0.0)
(ui-symbol "mo_freeform_blend_prop_crown_flip"		  #f)

; profile blend options

(ui-symbol "mo_profile_blend_surface_type"		(ui-symbol-reference 'MO_FILLET_SRF_MULTIPLE_SURFACES))
(ui-symbol "mo_profile_blend_continuityA"			   1)
(ui-symbol "mo_profile_blend_continuityB"			   1)

(ui-symbol "mo_profile_blend_single_span"			  #f)
(ui-symbol "mo_profile_blend_interior_edge_align"	  #f)
(ui-symbol "mo_profile_blend_explicit_control"		  #f)
(ui-symbol "mo_profile_blend_u_degree"				   5)
(ui-symbol "mo_profile_blend_max_num_spans"			 100)

(ui-symbol "mo_profile_blend_auto_recalc"			  #f)
(ui-symbol "mo_profile_blend_continuity_check"		  #f)
(ui-symbol "mo_profile_blend_short_edge_tol"	   0.001)
(ui-symbol "mo_profile_blend_pick_chain"			  #f)

; Deformation
(ui-symbol "mo_deformation_pick_ptDisp"               #f)
(ui-symbol "mo_deformation_pick_mesh"                 #t)
(ui-symbol "mo_deformation_pick_isoParam"             #f)
(ui-symbol "mo_deformation_pick_trimEdge"             #f)
(ui-symbol "mo_deformation_pick_COS"                  #f)
(ui-symbol "mo_deformation_pick_curve"                #t)
(ui-symbol "mo_deformation_pick_surfaces"             #t)
(ui-symbol "mo_deformation_pick_group"                #f)
(ui-symbol "mo_deformation_pick_chain"                #f)
(ui-symbol "mo_deformation_pick_object"               #f)

; fillet flange
(ui-symbol "mo_fillet_flange_wall_type"				   1)
(ui-symbol "mo_fillet_flange_flange_angle"			 0.0)
(ui-symbol "mo_fillet_flange_draft_angle"			 0.0)
(ui-symbol "mo_fillet_flange_wall_flip"				  #f)
(ui-symbol "mo_fillet_flange_radius"				 1.0)
(ui-symbol "mo_fillet_flange_flip"					  #f)
(ui-symbol "mo_fillet_flange_section_type"			(ui-symbol-reference 'MO_FILLET_SRF_SECTION_TYPE_G1CIRCULAR))
(ui-symbol "mo_fillet_flange_parameter_type"		   1)
(ui-symbol "mo_fillet_flange_center_radius"			 0.5)
(ui-symbol "mo_fillet_flange_form_factor_version"	 2014)
(ui-symbol "mo_fillet_flange_form_factor"			 0.5)
(ui-symbol "mo_fillet_flange_surface_type"			(ui-symbol-reference 'MO_FILLET_SRF_MULTIPLE_SURFACES))
(ui-symbol "mo_fillet_flange_single_span"			  #f)
(ui-symbol "mo_fillet_flange_short_edge_tol"       0.001)
(ui-symbol "mo_fillet_flange_explicit_control"	      #f)
(ui-symbol "mo_fillet_flange_degree"				   5)
(ui-symbol "mo_fillet_flange_v_degree"				   5)
(ui-symbol "mo_fillet_flange_max_spans"				 100)
(ui-symbol "mo_fillet_flange_create_flange"			  #t)
(ui-symbol "mo_fillet_flange_ext_type"				   0)
(ui-symbol "mo_fillet_flange_ext_distance"			 1.0)
(ui-symbol "mo_fillet_flange_ext_explicit_control"	  #f)
(ui-symbol "mo_fillet_flange_ext_degree"			   5)
(ui-symbol "mo_fillet_flange_ext_max_spans"			 100)
(ui-symbol "mo_fillet_flange_sweep_angle"			90.0)
(ui-symbol "mo_fillet_flange_parting_line_angle"	 0.0)
(ui-symbol "mo_fillet_flange_variable_param"		   0)
(ui-symbol "mo_fillet_flange_auto_trim"				  #f)
(ui-symbol "mo_fillet_flange_continuity_check"		  #f)
(ui-symbol "mo_fillet_flange_auto_recalc"			  #f)
(ui-symbol "mo_fillet_flange_show_wall"				  #f)
(ui-symbol "mo_fillet_flange_extend_start"			  #f)
(ui-symbol "mo_fillet_flange_extend_end"			  #f)
(ui-symbol "mo_fillet_flange_pick_chain"			  #f)
(ui-symbol "mo_fillet_flange_pull_vect_name"          "")
(ui-symbol "mo_fillet_flange_pull_vect_presets"        2)
(ui-symbol "mo_fillet_flange_pull_vect_create"         0)
(ui-symbol "mo_fillet_flange_pull_vect_save"           0)
(ui-symbol "mo_fillet_flange_pull_vect_create"         0)
(ui-symbol "mo_fillet_flange_partline_vector_name"    "")
(ui-symbol "mo_fillet_flange_partline_vector_presets"  2)
(ui-symbol "mo_fillet_flange_partline_vector_refresh"  0)
(ui-symbol "mo_fillet_flange_partline_vector_save"     0)
(ui-symbol "mo_fillet_flange_partline_vector_create"   0)
(ui-symbol "mo_fillet_flange_range"           #f)
(ui-symbol "mo_fillet_flange_range_start"     0.0)
(ui-symbol "mo_fillet_flange_range_end"       1.0)

; tube
(ui-symbol "mo_tube_radius"							 1.0)
(ui-symbol "mo_tube_flip"							  #f)
(ui-symbol "mo_tube_surface_type"					   1)
(ui-symbol "mo_tube_section_type"					(ui-symbol-reference 'MO_FILLET_SRF_SECTION_TYPE_G1CIRCULAR))
(ui-symbol "mo_tube_parameter_type"					   1)
(ui-symbol "mo_tube_form_factor_version"			2014)
(ui-symbol "mo_tube_center_radius"					 0.5)
(ui-symbol "mo_tube_form_factor"					 0.5)
(ui-symbol "mo_tube_single_span"					  #f)
(ui-symbol "mo_tube_short_edge_tol"				   0.001)
(ui-symbol "mo_tube_explicit_control"				  #f)
(ui-symbol "mo_tube_degree"							   5)
(ui-symbol "mo_tube_v_degree"						   5)
(ui-symbol "mo_tube_max_spans"						 100)
(ui-symbol "mo_tube_create_flange"					  #t)
(ui-symbol "mo_tube_ext_type"						   0)
(ui-symbol "mo_tube_ext_distance"					 1.0)
(ui-symbol "mo_tube_ext_flip"						  #f)
(ui-symbol "mo_tube_ext_explicit_control"			  #f)
(ui-symbol "mo_tube_ext_degree"						   5)
(ui-symbol "mo_tube_ext_max_spans"					 100)
(ui-symbol "mo_tube_sweep_angle"					90.0)
(ui-symbol "mo_tube_parting_line_angle"				 0.0)
(ui-symbol "mo_tube_variable_param"					   0)
(ui-symbol "mo_tube_continuity_check"				  #f)
(ui-symbol "mo_tube_auto_recalc"					  #f)
(ui-symbol "mo_tube_pick_chain"						  #f)
(ui-symbol "mo_tube_partline_vect_name"               "")
(ui-symbol "mo_tube_partline_vect_presets"             2)
(ui-symbol "mo_tube_partline_vect_refresh"             0)
(ui-symbol "mo_tube_partline_vect_save"                0)
(ui-symbol "mo_tube_partline_vect_create"              0)
(ui-symbol "mo_tube_range"					  #f)
(ui-symbol "mo_tube_range_start"			  0.0)
(ui-symbol "mo_tube_range_end"			  1.0)

; VSR Skin
(ui-symbol "mo_vsrskin_proportional_crown"			  #f)
(ui-symbol "mo_vsrskin_proportional_crown_val"		 0.0)
(ui-symbol "mo_vsrskin_proportional_crown_flip"		  #f)
(ui-symbol "mo_vsrskin_multi_srf"					   2)
(ui-symbol "mo_vsrskin_create_bezier"				  #f)
(ui-symbol "mo_vsrskin_explicit_control"			  #f)
(ui-symbol "mo_vsrskin_degree_u"					   3)
(ui-symbol "mo_vsrskin_degree_v"					   3)
(ui-symbol "mo_vsrskin_spans_u"						 100)
(ui-symbol "mo_vsrskin_spans_v"						   1)
(ui-symbol "mo_vsrskin_tolerance"				   0.001)
(ui-symbol "mo_vsrskin_topology"					   2)
(ui-symbol "mo_vsrskin_flow_ctrl_begin"				4)
(ui-symbol "mo_vsrskin_flow_ctrl_end"				   4)
(ui-symbol "mo_vsrskin_trim"						  #f)
(ui-symbol "mo_vsrskin_history"						  #t)
(ui-symbol "mo_vsrskin_auto_recalc"					  #t)
(ui-symbol "mo_vsrskin_chain_select"				  #f)
(ui-symbol "mo_vsrskin_deviation"					  #t)
(ui-symbol "mo_vsrskin_continuity_check"			  #t)

; Nurbs to Bezier
(ui-symbol "mo_nurbs_to_bezier_all"					   0)
(ui-symbol "mo_nurbs_to_bezier_keep_originals"		  #t)

; Surface Array

(ui-symbol "mo_surfacearr_rngstart"					        0.0)
(ui-symbol "mo_surfacearr_rngend"				            1.0)
(ui-symbol "mo_surfacearr_rngstart_2"					    1.0)
(ui-symbol "mo_surfacearr_rngend_2"				            1.0)
(ui-symbol "mo_surfacearr_rngdummy_0"						0.0)
(ui-symbol "mo_surfacearr_rngdummy_1"						0.0)
(ui-symbol "mo_surfacearr_nposoff"				   	        0.0)
(ui-symbol "mo_surfacearr_uposoff"			  	            0.0)
(ui-symbol "mo_surfacearr_vposoff"				            0.0)
(ui-symbol "mo_surfacearr_xrotoff"				      	    0.0)
(ui-symbol "mo_surfacearr_yrotoff"			  	            0.0)
(ui-symbol "mo_surfacearr_zrotoff"                          0.0)
(ui-symbol "mo_surfacearr_specify_1"					      1)
(ui-symbol "mo_surfacearr_number_1"					          3)
(ui-symbol "mo_surfacearr_spacing_1"					   10.0)
(ui-symbol "mo_surfacearr_scalefactor_1"                    1.0)
(ui-symbol "mo_surfacearr_enablerotation_1"					#f)
(ui-symbol "mo_surfacearr_xincrementalrotationaloffset_1"   0.0)
(ui-symbol "mo_surfacearr_yincrementalrotationaloffset_1"   0.0)
(ui-symbol "mo_surfacearr_zincrementalrotationaloffset_1"   0.0)
(ui-symbol "mo_surfacearr_incroffset_1"						0.0)
(ui-symbol "mo_surfacearr_specify_2"					      1)
(ui-symbol "mo_surfacearr_number_2"					          3)
(ui-symbol "mo_surfacearr_spacing_2"					   10.0)
(ui-symbol "mo_surfacearr_scalefactor_2"                    1.0)
(ui-symbol "mo_surfacearr_enablerotation_2"					 #f)
(ui-symbol "mo_surfacearr_xincrementalrotationaloffset_2"   0.0)
(ui-symbol "mo_surfacearr_yincrementalrotationaloffset_2"   0.0)
(ui-symbol "mo_surfacearr_zincrementalrotationaloffset_2"   0.0)
(ui-symbol "mo_surfacearr_incroffset_2"						0.0)
(ui-symbol "mo_surfacearr_autoupdate"				         #t)
(ui-symbol "mo_surfacearr_createhistory"  			    	 #t)
(ui-symbol "mo_surfacearr_rangefit_1"				         #t)
(ui-symbol "mo_surfacearr_rangefit_2"				         #f)
(ui-symbol "mo_surfacearr_orientnormals"			          2)
(ui-symbol "mo_surfacearr_chainselect"				         #f)
(ui-symbol "mo_surfacearr_rangemanips"				         #t)
(ui-symbol "mo_surfacearr_stagger_1"  				         #f)
(ui-symbol "mo_surfacearr_stagger_2"  				         #f)
(ui-symbol "mo_surfacearr_uvdirection"						  2)
(ui-symbol "mo_surfacearr_direction"  				          0)

; Stitch Gen
(ui-symbol "mo_stitchgen_specify"					     0)
(ui-symbol "mo_stitchgen_number"					    10)
(ui-symbol "mo_stitchgen_spacing"					  10.0)
(ui-symbol "mo_stitchgen_rngstart"					   0.0)
(ui-symbol "mo_stitchgen_rngend"				       1.0)
(ui-symbol "mo_stitchgen_xposoff"				   	   0.0)
(ui-symbol "mo_stitchgen_yposoff"			  	       0.0)
(ui-symbol "mo_stitchgen_zposoff"				       0.0)
(ui-symbol "mo_stitchgen_xrotoff"				   	   0.0)
(ui-symbol "mo_stitchgen_yrotoff"			  	       0.0)
(ui-symbol "mo_stitchgen_zrotoff"                      0.0)
(ui-symbol "mo_stitchgen_scalefactor"                  1.0)
(ui-symbol "mo_stitchgen_xincrementalrotationaloffset" 0.0)
(ui-symbol "mo_stitchgen_yincrementalrotationaloffset" 0.0)
(ui-symbol "mo_stitchgen_zincrementalrotationaloffset" 0.0)
(ui-symbol "mo_stitchgen_autoupdate"				    #t)
(ui-symbol "mo_stitchgen_createhistory"  				#t)
(ui-symbol "mo_stitchgen_rangefit"					    #f)
(ui-symbol "mo_stitchgen_orientnormals"				     2)
(ui-symbol "mo_stitchgen_chainselect"				    #f)
(ui-symbol "mo_stitchgen_rangemanips"				    #t)

; Array
(ui-symbol "mo_arraytool_mode"					 	   0)
(ui-symbol "mo_arraytool_plane"					 	   0)
(ui-symbol "mo_arraytool_dimx"					 	   5)
(ui-symbol "mo_arraytool_dimy"					 	   5)
(ui-symbol "mo_arraytool_spacingx"					10.0)
(ui-symbol "mo_arraytool_spacingy"					10.0)
(ui-symbol "mo_arraytool_spacingr"					72.0)
(ui-symbol "mo_arraytool_posoffx"					 0.0)
(ui-symbol "mo_arraytool_posoffy"					 0.0)
(ui-symbol "mo_arraytool_posoffr"					 0.0)
(ui-symbol "mo_arraytool_scalex"					 1.0)
(ui-symbol "mo_arraytool_scaley"					 1.0)
(ui-symbol "mo_arraytool_staggerx"					   0)
(ui-symbol "mo_arraytool_staggery"					   0)
(ui-symbol "mo_arraytool_mirrorx"					  #f)
(ui-symbol "mo_arraytool_mirrory"					  #f)
(ui-symbol "mo_arraytool_autoupdate"				  #t)
(ui-symbol "mo_arraytool_createhistory"				  #t)
(ui-symbol "mo_arraytool_growradial"				  #f)
(ui-symbol "mo_arraytool_scalepos"					  #f)
(ui-symbol "mo_arraytool_fittocircle"                 #f)
(ui-symbol "mo_arraytool_rotateduplicates"            #f)
(ui-symbol "mo_arraytool_centeroriginal"			  #t)

; VSR Smooth
(ui-symbol "mo_vsrsmooth_smoothing_factor"			 0.2)
(ui-symbol "mo_vsrsmooth_edge_influence"			 0.0)
(ui-symbol "mo_vsrsmooth_partial_undo"				 1.0)
(ui-symbol "mo_vsrsmooth_fixed_edges"				  #f)
(ui-symbol "mo_vsrsmooth_smooth_u"					  #t)
(ui-symbol "mo_vsrsmooth_smooth_v"					  #t)
(ui-symbol "mo_vsrsmooth_deviation"					  #t)
(ui-symbol "mo_vsrsmooth_proxy_display"				  #t)
(ui-symbol "mo_vsrsmooth_keep_originals"			  #f)

; Quick surface
(ui-symbol "mo_quicksrf_creationmode"				   0)
(ui-symbol "mo_quicksrf_u_degree"					   3)
(ui-symbol "mo_quicksrf_v_degree"					   3)
(ui-symbol "mo_quicksrf_smooth"					  	  #f)
(ui-symbol "mo_quicksrf_smoothfactor"				 0.2)
(ui-symbol "mo_quicksrf_selectionmode"				   0)
(ui-symbol "mo_quicksrf_normalangle"				 3.0)
(ui-symbol "mo_quicksrf_minradiuslimit"				 0.5)
(ui-symbol "mo_quicksrf_pickradius"					  25)
(ui-symbol "mo_quicksrf_pickvisible"				  #t)
(ui-symbol "mo_quicksrf_autoupdate"					  #f)
(ui-symbol "mo_quicksrf_history"					  #t)
(ui-symbol "mo_quicksrf_deviation"					  #f)
(ui-symbol "mo_quicksrf_deviationscale"				 1.0)
(ui-symbol "mo_quicksrf_deviationsamples"			  25)
(ui-symbol "mo_quicksrf_deviationswapuv"			  #f)


; symmetry plane align options
(ui-symbol "mo_symalign_project_bndy"   #t)


; refit surfaces
(ui-symbol "mo_refitsrfs_mindegree"         1)
(ui-symbol "mo_refitsrfs_smoothfactor"    0.2)
(ui-symbol "mo_refitsrfs_direction"				1)
(ui-symbol "mo_refitsrfs_history"				  #t)
(ui-symbol "mo_refitsrfs_autoupdate"			  #f)
(ui-symbol "mo_refitsrfs_keep_originals"		  #f)
(ui-symbol "mo_refitsrfs_deviationscale"  1.0)


; align options

(ui-symbol "mo_align_history"           #t)
(ui-symbol "mo_align_continuity_check"  #f)
(ui-symbol "mo_align_explicit_control"  #f)
(ui-symbol "mo_align_auto_recalc"       #t)
(ui-symbol "mo_align_insert_at_param"   #f)
(ui-symbol "mo_align_skews_allowed"     #f)
(ui-symbol "mo_align_partial_joins"     0)
(ui-symbol "mo_align_modify_interior_allowed" 0)
(ui-symbol "mo_align_attach_hardness"   1)
(ui-symbol "mo_align_continuity"        1)
(ui-symbol "mo_align_modify_type"       1)
(ui-symbol "mo_align_intersection_type" 0)
(ui-symbol "mo_align_interp_int_from_ends" #f)
(ui-symbol "mo_align_interp_int_from_ends2" #f)
(ui-symbol "mo_align_se_controls" #f)
(ui-symbol "mo_align_alignment_type"    0)
(ui-symbol "mo_align_alignment_type_start" 0)
(ui-symbol "mo_align_alignment_type_end"   0)
(ui-symbol "mo_align_dirAlignVector" 0.0 0.0 1.0)
(ui-symbol "mo_align_dirAlignPreset" 2)
(ui-symbol "mo_align_continuity_check_same" #t)
(ui-symbol "mo_align_continuity_check_type" 2)
(ui-symbol "mo_align_item1_g1_scale" 1.0)
(ui-symbol "mo_align_item1_g1_scale_end" 1.0)
(ui-symbol "mo_align_item1_g1_skew0" 0.0)
(ui-symbol "mo_align_item1_g1_skew1" 0.0)
(ui-symbol "mo_align_item1_g2_scale" 0.0)
(ui-symbol "mo_align_item1_g2_scale_end" 0.0)
(ui-symbol "mo_align_item1_g2_skew0" 0.0)
(ui-symbol "mo_align_item1_g2_skew1" 0.0)
(ui-symbol "mo_align_item1_cv_rows_affected" 0)
(ui-symbol "mo_align_item1_decay" 1.0)
(ui-symbol "mo_align_item1_degreeSync" #f)
(ui-symbol "mo_align_item1_num_manip" 0)
(ui-symbol "mo_align_item2_g1_scale" 1.0)
(ui-symbol "mo_align_item2_g1_scale_end" 1.0)
(ui-symbol "mo_align_item2_g1_skew0" 0.0)
(ui-symbol "mo_align_item2_g1_skew1" 0.0)
(ui-symbol "mo_align_item2_g2_scale" 0.0)
(ui-symbol "mo_align_item2_g2_scale_end" 0.0)
(ui-symbol "mo_align_item2_g2_skew0" 0.0)
(ui-symbol "mo_align_item2_g2_skew1" 0.0)
(ui-symbol "mo_align_item2_cv_rows_affected" 0)
(ui-symbol "mo_align_item2_decay" 1.0)
(ui-symbol "mo_align_item2_degreeSync" #f)
(ui-symbol "mo_align_item2_num_manip" 2)
(ui-symbol "mo_align_lock_position_row" #f)
(ui-symbol "mo_align_lock_tangent_row" #f)

; the following options are no longer used by align
(ui-symbol "mo_align_alignmode_C0"      (ui-symbol-reference "MO_MODIFY_FIRST"))
(ui-symbol "mo_align_alignmode_G1"      (ui-symbol-reference "MO_MODIFY_FIRST"))
(ui-symbol "mo_align_alignmode_G2"      (ui-symbol-reference "MO_MODIFY_FIRST"))
(ui-symbol "mo_align_align_by_project"  #f)
(ui-symbol "mo_align_keep_orig"         #f)
(ui-symbol "mo_align_tangent_scaling"   #f)
(ui-symbol "mo_align_mod_type"          (ui-symbol-reference "MO_ALIGN_FIX_END"))
(ui-symbol "mo_align_snap_mode"         (ui-symbol-reference "MO_MODIFY_FIRST"))
(ui-symbol "mo_align_align_mode"        (ui-symbol-reference "MO_MODIFY_FIRST"))

; align mesh options

(ui-symbol "mo_align_mesh_modify_mode"  (ui-symbol-reference "MO_ALIGN_MESH_MODIFY_BOUNDARY"))
(ui-symbol "mo_align_mesh_c0_tolerance" 0.1)
(ui-symbol "mo_align_mesh_keep_orig"    #t)

; align hull options
(ui-symbol "mo_align_hull_c0_tolerance" 0.1)
(ui-symbol "mo_align_hull_percentage"	100.0)
(ui-symbol "mo_align_hull_keep_orig"    #f)
(ui-symbol "mo_align_hull_lock_u"		#f)
(ui-symbol "mo_align_hull_lock_v"       #f)
(ui-symbol "mo_align_hull_modify_mode"	1)

; hull planarize options
(ui-symbol "mo_hull_planarize_type" 3)
(ui-symbol "mo_hull_planarize_vector_select_method" 4)
(ui-symbol "mo_hull_planarize_view_based" #t)
(ui-symbol "mo_hull_planarize_iterations" #t)
(ui-symbol "mo_hull_planarize_include_edges" #f)
(ui-symbol "mo_hull_planarize_calculate_deviation" #f)
(ui-symbol "mo_hull_planarize_proxy_display" #f)

; attach options

(ui-symbol "mo_attach_keep_orig"        #f)
(ui-symbol "mo_attach_insert_knots"     #f)
(ui-symbol "mo_attach_insert_pos"       0.1)
(ui-symbol "mo_attach_mod_type"         (ui-symbol-reference "MO_FILLET"))
(ui-symbol "mo_fillet_bias"             0.5)
(ui-symbol "mo_seam_weight"             10000)

; undo-attach options

(ui-symbol "mo_attach_undo_ok"          #f)


; detach options

(ui-symbol "mo_detach_keep"             #f)
(ui-symbol "mo_detach_interactive"      #f)


; new curve options

(ui-symbol "mo_create_guidelines"		#f)
(ui-symbol "mo_newcrv_pick_chooser"		#f)
(ui-symbol "mo_construct_mode"          (ui-symbol-reference "MO_CV"))
(ui-symbol "mo_knot_spacing"            (ui-symbol-reference "MO_UNIFORM"))
(ui-symbol "mo_cvs_knot_spacing"        (ui-symbol-reference "MO_UNIFORM"))
(ui-symbol "mo_eps_knot_spacing"        (ui-symbol-reference "MO_CHORD_LENGTH"))
(ui-symbol "mo_sketch_knot_spacing"     (ui-symbol-reference "MO_CHORD_LENGTH"))
(ui-symbol "mo_sketch_tolerance"        3.00000)
(ui-symbol "mo_sketch_max_spans"        2)
(ui-symbol "mo_beep_mode"               #f)
(ui-symbol "mo_geometry_type"           (ui-symbol-reference "MO_BSPLINE"))
(ui-symbol "mo_geom_degree"             (ui-symbol-reference "MO_THREE"))
(ui-symbol "mo_addcv_preprocess"        #t)
(ui-symbol "mo_initial_new_curve"       #f)
(ui-symbol "mo_addcv_domain"            (ui-symbol-reference "MO_ADDCV_WORLD"))
(ui-symbol "newcrv.progressive_degree"	#t)
(ui-symbol "mo_newcrv_cvs_pivot"        (ui-symbol-reference "MO_CRV_PIVOT_FIRST_CV"))
(ui-symbol "mo_newcrv_eps_pivot"        (ui-symbol-reference "MO_CRV_PIVOT_FIRST_CV"))
(ui-symbol "mo_newcrv_sketch_pivot"     (ui-symbol-reference "MO_CRV_PIVOT_FIRST_CV"))
(ui-symbol "mo_newcrv_blend_pivot"      (ui-symbol-reference "MO_CRV_PIVOT_FIRST_CV"))
(ui-symbol "mo_sketchcurve_pivot"       (ui-symbol-reference "MO_CRV_PIVOT_FIRST_CV"))
(ui-symbol "mo_sketchcurve_type"	    1)
(ui-symbol "mo_sketchcurve_degree"	    3)
(ui-symbol "mo_sketchcurve_maxspans"    10)
(ui-symbol "mo_sketchcurve_tolerance"   3.0)


; new curve on surface options

(ui-symbol "mo_cos_construct_mode"      (ui-symbol-reference "MO_EDIT_PT"))
(ui-symbol "mo_cos_geometry_type"       (ui-symbol-reference "MO_BSPLINE"))
(ui-symbol "mo_cos_knot_spacing"        (ui-symbol-reference "MO_CHORD_LENGTH"))


; blending curve options

(ui-symbol "mo_blend_curve_degree"      5)
(ui-symbol "mo_blend_curve_knot_spacing" (ui-symbol-reference "MO_UNIFORM"))
(ui-symbol "mo_blend_curve_auto_align"     #t)
(ui-symbol "mo_blend_curve_curve_continuity" 2)

; curve stretch options
(ui-symbol "stretch.numpoints"	2)
(ui-symbol "stretch.floating_knot"	#f)
(ui-symbol "stretch.preserve_shape"	#t)
; (ui-symbol "stretch.only_rock"	#f)

; duplicate curve options

(ui-symbol "mo_dupl_fit"                (ui-symbol-reference "MO_FIT_OFF"))
(ui-symbol "mo_dupl_interactive"        #f)
(ui-symbol "mo_dupl_fit_tol"            0.01)
(ui-symbol "mo_dpl_end_condition"       (ui-symbol-reference "MO_END_CUBIC"))
(ui-symbol "mo_dpl_knot_spacing"        (ui-symbol-reference "MO_CHORD_LENGTH"))

; fitcurve to COS

(ui-symbol "mo_fitcurve_curvename"      "fit curve")
(ui-symbol "mo_fitcurve_curvature"      #f)
(ui-symbol "mo_fitcurve_deviation"      #t)
(ui-symbol "mo_fitcurve_spans"          1)
(ui-symbol "mo_fitcurve_degree"         3)
(ui-symbol "mo_fitcurve_modify_COS"     0)
(ui-symbol "mo_fitcurve_COS_tolerance"  0.001)
(ui-symbol "mo_fitcurve_history"        #t)


; COS fit test tool

(ui-symbol "mo_cosfittest_mode"			0 )
(ui-symbol "mo_cosfittest_tol"			0.001 )
(ui-symbol "mo_cosfittest_maxSpans"		100 )
(ui-symbol "mo_cosfittest_degree"		3 )
(ui-symbol "mo_cosfittest_spans"		1 )
(ui-symbol "mo_cosfittest_segOption"	0 )
(ui-symbol "mo_cosfittest_fitMethod"	0 )
(ui-symbol "mo_cosfittest_chordalInfl"	0.0 )
(ui-symbol "mo_cosfittest_surfUVInfl"	0.0 )
(ui-symbol "mo_cosfittest_autoUpdate"	#t )
(ui-symbol "mo_cosfittest_curvature"	#t )
(ui-symbol "mo_cosfittest_deviation"	#t )
(ui-symbol "mo_cosfittest_chainSelect"	#f )

; adjust intersection options

(ui-symbol "mo_modificn"                (ui-symbol-reference "MO_MODIFICN_GLOBAL"))
(ui-symbol "mo_intpt"                   (ui-symbol-reference "MO_INTPT_VIEW"))
(ui-symbol "mo_segseln"                 (ui-symbol-reference "MO_SEGSELN_AUTO"))
(ui-symbol "mo_startmod"                (ui-symbol-reference "MO_STARTMOD_TANFIXED"))
(ui-symbol "mo_endmod"                  (ui-symbol-reference "MO_ENDMOD_TANFIXED"))
(ui-symbol "mo_keeporig"                (ui-symbol-reference "MO_KEEPORIG_OFF"))


; Merge vertices options

(ui-symbol "mo_merge_verts_tol"         0.0001)


; Rebuild curve options

(ui-symbol "mo_rebuild_crv_whichOne"    0)
(ui-symbol "mo_rebuild_crv_duplReduce"  #f)
(ui-symbol "mo_rebuild_crv_typeDuplicate" (ui-symbol-reference "MO_REBUILD_CRV_TYPE_NO_REBUILD"))
(ui-symbol "mo_rebuild_crv_typeRebuild" (ui-symbol-reference "MO_REBUILD_CRV_TYPE_REDUCE"))

(ui-symbol "mo_rebuild_crv_tol"     0.1)



(ui-symbol "mo_rebuild_crv_spansChangeCVs" #f)
(ui-symbol "mo_rebuild_crv_spansNum"    3)
(ui-symbol "mo_rebuild_crv_spansRelative" (ui-symbol-reference "MO_REBUILD_CRV_SPANS_RELATIVE"))
(ui-symbol "mo_rebuild_crv_spansMax"    3)
(ui-symbol "mo_rebuild_crv_spansFact"   5.0)
(ui-symbol "mo_rebuild_crv_changeDegree" #f)
(ui-symbol "mo_rebuild_crv_degree"      3)
(ui-symbol "mo_rebuild_crv_autoRecalc"  #f)
(ui-symbol "mo_rebuild_crv_smoothing"   #f)
(ui-symbol "mo_rebuild_crv_interactive" #f)
(ui-symbol "mo_rebuild_crv_originals"   #t)
(ui-symbol "mo_rebuild_crv_MinMaxDev"   #f)
(ui-symbol "mo_rebuild_crv_history"     #f)
(ui-symbol "mo_rebuild_crv_chain_select" #f)

; curve planar options

(ui-symbol "mo_crv_planar_plane_type"   (ui-symbol-reference "MO_CRV_PLANAR_BEST_PROJECT"))
(ui-symbol "mo_crv_planar_axis_type"    (ui-symbol-reference "MO_CRV_PLANAR_AXIS_XY"))
(ui-symbol "mo_crv_planar_lock_ends"	#t)
(ui-symbol "mo_crv_planar_originals"	#t)
(ui-symbol "mo_crv_planar_create_plane"	#f)

; curve section options

(ui-symbol "mo_crvSection_mode"   		(ui-symbol-reference "MO_CRV_SECTION_MODE_TRIM"))
(ui-symbol "mo_crvSection_slice_type"   (ui-symbol-reference "MO_CRV_SECTION_INTERPOLATE"))
(ui-symbol "mo_crvSection_criterion"    (ui-symbol-reference "MO_CRV_SECTION_CRIT_GEOM"))

; composite curve options

(ui-symbol "mo_auto_direction"          (ui-symbol-reference "MO_AUTODIR_ON"))
(ui-symbol "mo_comb_create_history"     #t)


; fit bspline options

(ui-symbol "mo_end_condition"           (ui-symbol-reference "MO_END_CUBIC"))
(ui-symbol "mo_fit_type"                (ui-symbol-reference "MO_CUBIC_FIT"))
(ui-symbol "mo_fit_tol"                 0.01)
(ui-symbol "mo_chord_h_ratio"           #f)
(ui-symbol "mo_val_chord_h_ratio"       10.0)
(ui-symbol "mo_fit_knot_spacing"        (ui-symbol-reference "MO_CHORD_LENGTH"))

(ui-symbol "mo_fit_start_utan_x"        1.0)
(ui-symbol "mo_fit_start_utan_y"        0.0)
(ui-symbol "mo_fit_start_utan_z"        0.0)

(ui-symbol "mo_fit_end_utan_x"          -1.0)
(ui-symbol "mo_fit_end_utan_y"          0.0)
(ui-symbol "mo_fit_end_utan_z"          0.0)

(ui-symbol "mo_fit_start_vtan_x"        1.0)
(ui-symbol "mo_fit_start_vtan_y"        0.0)
(ui-symbol "mo_fit_start_vtan_z"        0.0)

(ui-symbol "mo_fit_end_vtan_x"          -1.0)
(ui-symbol "mo_fit_end_vtan_y"          0.0)
(ui-symbol "mo_fit_end_vtan_z"          0.0)


; weight options

(ui-symbol "mo_weight_increment"        3)


; autotrace options

(ui-symbol "mo_autotrace_threshold"     32)
(ui-symbol "mo_autotrace_stepsize"      5.0)
(ui-symbol "mo_autotrace_resample"      #t)
(ui-symbol "mo_autotrace_smooth"        #t)
(ui-symbol "mo_autotrace_fixcorner"     #f)


; boundary options

(ui-symbol "mo_tolerance"               1000000)
(ui-symbol "mo_bound_type"              (ui-symbol-reference "MO_COONS"))
(ui-symbol "mo_prim_blender"            (ui-symbol-reference "MO_PRIMB_CUBIC"))
(ui-symbol "mo_sec_blender"             (ui-symbol-reference "MO_SECB_CUBIC"))
(ui-symbol "mo_bcurve1"                 #f)
(ui-symbol "mo_bcurve2"                 #f)
(ui-symbol "mo_bcurve3"                 #f)
(ui-symbol "mo_bcurve4"                 #f)
(ui-symbol "mo_bkeep_profiles"          #t)
(ui-symbol "mo_bound_create_history"    #t)


; patch options

(ui-symbol "mo_patch_tol"               50000)
(ui-symbol "mo_patch_type"              (ui-symbol-reference "MO_PARAM_BASED"))
(ui-symbol "mo_patch_subdiv"            1)
(ui-symbol "mo_patch_geom_type"         (ui-symbol-reference "MO_CUBIC_PATCH"))
(ui-symbol "mo_pcurve1"                 #f)
(ui-symbol "mo_pcurve2"                 #f)
(ui-symbol "mo_pkeep_profiles"          #t)
(ui-symbol "mo_patch_create_history"    #t)
(ui-symbol "mo_p_single_surface"        #t)

; multi-surface draft

(ui-symbol "mo_draft_type"				   0)
(ui-symbol "mo_draft_surface_type"		   1)
(ui-symbol "mo_draft_flange_angle"		 0.0)
(ui-symbol "mo_draft_draft_angle"		 0.0)
(ui-symbol "mo_draft_height"			 1.0)
(ui-symbol "mo_draft_angle_calc"		   0)
(ui-symbol "mo_draft_length_mode"		   0)
(ui-symbol "mo_draft_flange_from_curve"	  #f)
(ui-symbol "mo_draft_from_curve_mode"	   0)
(ui-symbol "mo_draft_to_surface"		  #f)
(ui-symbol "mo_draft_radial_orient"		  #f)
(ui-symbol "mo_draft_radial_refit"		  #t)
(ui-symbol "mo_draft_orientation_vector"  #f)
(ui-symbol "mo_draft_modify_range"		  #f)
(ui-symbol "mo_draft_range_start"		 0.0)
(ui-symbol "mo_draft_range_end"			 1.0)
(ui-symbol "mo_draft_flip"				  #f)
(ui-symbol "mo_draft_surface_type"		   1)
(ui-symbol "mo_draft_single_span"		  #f)
(ui-symbol "mo_draft_crown"				  #f)
(ui-symbol "mo_draft_crown_flip"		  #f)
(ui-symbol "mo_draft_crown_type"		   0)
(ui-symbol "mo_draft_crown_value"		 0.0)
(ui-symbol "mo_draft_explicit_control"	  #f)
(ui-symbol "mo_draft_degree"			   5)
(ui-symbol "mo_draft_vDegree"			   1)
(ui-symbol "mo_draft_max_spans"			 100)
(ui-symbol "mo_draft_exact_spans"		   1)
(ui-symbol "mo_draft_segmentation"         0)
(ui-symbol "mo_draft_fitting_method"       0)
(ui-symbol "mo_draft_hybrid_infl"        0.0)
(ui-symbol "mo_draft_variable_param"	   0)
(ui-symbol "mo_draft_continuity_check"	  #f)
(ui-symbol "mo_draft_auto_recalc"		  #f)
(ui-symbol "mo_draft_pick_chain"		  #f)
(ui-symbol "mo_draft_pull_vect_name"      "")
(ui-symbol "mo_draft_pull_vect_presets"    2)
(ui-symbol "mo_draft_pull_vect_refresh"    0)
(ui-symbol "mo_draft_pull_vect_save"       0)
(ui-symbol "mo_draft_pull_vect_create"     0)
(ui-symbol "mo_draft_pull_vector" 0.0 0.0 1.0)
(ui-symbol "mo_draft_orient_vect_name"    "")
(ui-symbol "mo_draft_orient_vect_presets"  2)
(ui-symbol "mo_draft_orient_vect_refresh"  0)
(ui-symbol "mo_draft_orient_vect_save"     0)
(ui-symbol "mo_draft_orient_vect_create"   0)
(ui-symbol "mo_draft_orient_vector" 0.0 0.0 1.0)
(ui-symbol "mo_draft_double_sided"		  #f)
(ui-symbol "mo_draft_single_surface"	  #f)
(ui-symbol "mo_draft_pick_isoParam"	      #t)
(ui-symbol "mo_draft_pick_curve"	      #t)
(ui-symbol "mo_draft_pick_trimEdge"	      #t)
(ui-symbol "mo_draft_pick_COS"	          #t)
(ui-symbol "mo_draft_intersect_flanges"	  #f)
(ui-symbol "mo_draft_miter_mode"		   1)
(ui-symbol "mo_draft_inter_continuity_check" #f)
(ui-symbol "mo_draft_tangent_angle_maximum" 30.0)

; extrude & revolve options

(ui-symbol "mo_keep_extrud_profiles"    #t)
(ui-symbol "mo_extrude_create_history"  #t)
(ui-symbol "mo_extrudepivot"            (ui-symbol-reference "MO_EXTRUDEPATH"))
(ui-symbol "mo_extrudetype"             (ui-symbol-reference "MO_EXTRUDETUBE"))

(ui-symbol "mo_extrudecaps"         (ui-symbol-reference "MO_EXTRUDECAPS0"))

; skin options

(ui-symbol "mo_skin_U_knot_spacing"       (ui-symbol-reference "MO_UNIFORM"))
(ui-symbol "mo_skin_V_knot_spacing"       (ui-symbol-reference "MO_CHORD_LENGTH"))
(ui-symbol "mo_keep_profiles"           #t)
(ui-symbol "mo_skin_extrapolate"        #t)
(ui-symbol "mo_skin_subdiv"             1)
(ui-symbol "mo_skin_mode"               (ui-symbol-reference "MO_SKIN_EXACT"))
(ui-symbol "mo_skintype"                (ui-symbol-reference "MO_SKINOPEN"))
(ui-symbol "mo_skin_geom_type"          (ui-symbol-reference "MO_CUBIC_SKIN"))
(ui-symbol "mo_skin_rebuild"     		#f)
(ui-symbol "mo_skin_create_history"     #t)
(ui-symbol "mo_skin_auto_recalc"        #t)


;  surfmod options

(ui-symbol "mo_surfmod_offset_do_it"    #f)
(ui-symbol "mo_surfmod_keep_originals"  #t)
(ui-symbol "mo_surfmod_make_set"        #t)
(ui-symbol "mo_surfmod_min_mod_tol"     0.0)
(ui-symbol "mo_surfmod_max_mod_tol"     10000.0)
(ui-symbol "mo_surfmod_num_subdiv"      0.0)
(ui-symbol "mo_surfmod_eval_method"     (ui-symbol-reference "AS_SURFMOD_EVAL_OFF"))
(ui-symbol "mo_surfmod_target_check_pts" 3)
(ui-symbol "mo_surfmod_working_check_pts" 3)
(ui-symbol "mo_surfmod_target_sampling" #f)
(ui-symbol "mo_surfmod_working_sampling" #f)
(ui-symbol "mo_surfmod_internal_value"  0.0)
(ui-symbol "mo_surfmod_boundaries_only" #f)
(ui-symbol "mo_surfmod_region_cutoff"   0.0)
(ui-symbol "mo_surfmod_auto_recalc"     1)
(ui-symbol "mo_surfmod_tangent_lock"    0)


; surface rebuild options (in the control box, not the option box)

(ui-symbol "mo_srf_rebuild_type"        3)
(ui-symbol "mo_srf_rebuild_tolerance" 0.1)



(ui-symbol "mo_srf_rebuild_tangency"    0.1)
(ui-symbol "mo_srf_rebuild_direction"   2)
(ui-symbol "mo_srf_rebuild_changeCVs"   #f)
(ui-symbol "mo_srf_rebuild_spansNumU"   3)
(ui-symbol "mo_srf_rebuild_spansNumV"   3)
(ui-symbol "mo_srf_rebuild_relativeSpans" 1)
(ui-symbol "mo_srf_rebuild_spansMaxU"   5)
(ui-symbol "mo_srf_rebuild_spansMaxV"   5)
(ui-symbol "mo_srf_rebuild_spansFactU"  3.0)
(ui-symbol "mo_srf_rebuild_spansFactV"  3.0)
(ui-symbol "mo_srf_rebuild_changeDegree" #f)
(ui-symbol "mo_srf_rebuild_degreeU"     3)
(ui-symbol "mo_srf_rebuild_degreeV"     3)
(ui-symbol "mo_srf_rebuild_autoRecalc"  #f)
(ui-symbol "mo_srf_rebuild_keepOriginals" #t)
(ui-symbol "mo_srf_rebuild_measureDev" #f)
(ui-symbol "mo_srf_rebuild_MinMaxDev"  #f)
(ui-symbol "mo_srf_rebuild_history"     #f)

; Shading Control Tool

(ui-symbol "mo_sct_show_viz_panel"     #t)
(ui-symbol "mo_sct_show_shader_lister"  #f)
(ui-symbol "mo_sct_max_current_view"   #f)
(ui-symbol "mo_sct_use_fullscreen"	   #f)
(ui-symbol "mo_sct_hide_main_menu"	   #t)
(ui-symbol "mo_sct_hide_title_bar"	   #t)
(ui-symbol "mo_sct_hide_palette"	   #t)

; revolve options

(ui-symbol "mo_revolvecaps"             (ui-symbol-reference "MO_REVOLVECAPS2"))
(ui-symbol "mo_revolve_axis"            0)
(ui-symbol "mo_revolve_vector_name"     "")
(ui-symbol "mo_revolve_vector_refresh"  0)
(ui-symbol "mo_revolve_vector_save"     0)
(ui-symbol "mo_revolve_vector_create"	0)
(ui-symbol "mo_revolve_axes"            (ui-symbol-reference "MO_REV_LOCAL"))
(ui-symbol "mo_revolve_surface_type"	0)
(ui-symbol "mo_revolve_sideglass_mode"	0)
(ui-symbol "mo_revolve_geometry_type"   5)
(ui-symbol "mo_revolve_periodic"		#f)
(ui-symbol "mo_revsections"             1)
(ui-symbol "mo_revolve_degree_periodic" 5)
(ui-symbol "mo_revolve_spans_periodic"  12)
(ui-symbol "mo_revolve_barrel_degree"   5)
(ui-symbol "mo_degrees"                 360.0)
(ui-symbol "mo_revolve_pitch"			0.0)
(ui-symbol "mo_revolve_segments"		1)
(ui-symbol "mo_revolve_per_segment"		360.0)
(ui-symbol "mo_revolve_barrel_rot_st"   0.0)
(ui-symbol "mo_revolve_barrel_rot_ed"   0.0)
(ui-symbol "mo_revolve_barrel_crv_st"   0.0)
(ui-symbol "mo_revolve_barrel_crv_ed"   0.0)
(ui-symbol "mo_revolve_helix_rot_st"    0.0)
(ui-symbol "mo_revolve_helix_rot_ed"    0.0)
(ui-symbol "mo_revolve_chain_select"    #f)
(ui-symbol "mo_revolve_cont_check"      #t)
(ui-symbol "mo_revolve_history"         #t)
(ui-symbol "mo_revolve_auto_recalc"     #t)

; Xform->unxform options

(ui-symbol "mo_xform_undo_ok"           #f)
(ui-symbol "al_undo_ok"           		#f)
(ui-symbol "al_redo_ok"           		#f)

; Xform->transform options
(ui-symbol "transform_move_active"      #t)
(ui-symbol "transform_rotate_active"    #t)
(ui-symbol "transform_scale_active"     #t)

; noOp
(ui-symbol "noOp_editor_image_path"      " ")
(ui-symbol "noOp_hotspot_image_path"      " ")
(ui-symbol "noOp_window_image_path"      " ")
(ui-symbol "noOp_window_name"           "Window")

; Xform->rotate options

(ui-symbol "mo_global_rotate"           (ui-symbol-reference "MO_ROTATE_GLOBAL"))

; Xform->translate options

(ui-symbol "mo_global_translate"        #t)
(ui-symbol "mo_use_stepsize"   #f )				;; if we should use step size in move cv tool.
(ui-symbol "mo_lock_stepsize"   #f )

; Xform->set local axes options

(ui-symbol "mo_set_lcl_axes_method"     (ui-symbol-reference "MO_LCL_AXES_INTERACTIVE"))

; Xform->rotational scale options

(ui-symbol "mo_rot_scale_input"        1)


; pivot options

(ui-symbol "mo_rot_pivot"               #t)
(ui-symbol "mo_scale_pivot"             #t)
(ui-symbol "mo_pivot_and_sel_hdl"       #t)

; center pivot options
(ui-symbol "mo_center_rot_pivot"        #t);
(ui-symbol "mo_center_scale_pivot"      #t);

; ObjMod->add constraint options

(ui-symbol "mo_constraint_on_uv"       #f)
(ui-symbol "mo_ik_constraint"           (ui-symbol-reference "MO_IK_CONSTR_POINT"))
(ui-symbol "mo_ik_aim_axis"             (ui-symbol-reference "MO_IK_X"))
(ui-symbol "mo_ik_up_axis"              (ui-symbol-reference "MO_IK_Y"))
(ui-symbol "mo_ik_weight"               2.0)

; ObjMod->create constraint options

(ui-symbol "mo_create_constraint_p"		 #t)
(ui-symbol "mo_create_constraint_o"		 #f)
(ui-symbol "mo_create_constraint_jack"	 #f)
(ui-symbol "mo_create_constraint_handle" #t)
(ui-symbol "mo_create_constraint_weight" 1.0)

; ObjMod->rest_pose_options

(ui-symbol "mo_restpose_hierarchy"		(ui-symbol-reference "MO_RESTPOSE_HIER_BELOW"))
(ui-symbol "mo_restpose_joint"			(ui-symbol-reference "MO_RESTPOSE_JOINT_USED"))
(ui-symbol "mo_restpose_pose"			(ui-symbol-reference "MO_RESTPOSE_ROTATE"))

; ObjMod->assume_pose_options
(ui-symbol "mo_assumepose_restpose"		#t)
(ui-symbol "mo_assumepose_hierarchy"	(ui-symbol-reference "MO_RESTPOSE_HIER_BELOW"))
(ui-symbol "mo_assumepose_joint"		(ui-symbol-reference "MO_RESTPOSE_JOINT_USED"))
(ui-symbol "mo_assumepose_pose"			(ui-symbol-reference "MO_RESTPOSE_ROTATE"))

; Edit->ik_onoff_options
(ui-symbol "mo_ikonoff_active"			#t)
(ui-symbol "mo_ikonoff_hier"			(ui-symbol-reference "MO_IK_ONOFF_HIER_NONE"))
(ui-symbol "mo_ikonoff_type_sc"			#t)
(ui-symbol "mo_ikonoff_type_mc"			#t)
(ui-symbol "mo_ikonoff_type_sp"			#t)
(ui-symbol "mo_ikonoff_cmd"				(ui-symbol-reference "MO_IK_ONOFF_CMD_TGL"))

; Edit->constraint_onoff_options
(ui-symbol "mo_constr_onoff_active"		#t)
(ui-symbol "mo_constr_onoff_hier"		(ui-symbol-reference "MO_CSTR_ONOFF_HIER_NONE"))
(ui-symbol "mo_constr_onoff_side"		(ui-symbol-reference "MO_CSTR_ONOFF_SIDE_SRC"))
(ui-symbol "mo_constr_onoff_pnt"		#t)
(ui-symbol "mo_constr_onoff_ori"		#t)
(ui-symbol "mo_constr_onoff_aim"		#t)

(ui-symbol "mo_constr_onoff_cmd"		(ui-symbol-reference "MO_CSTR_ONOFF_CMD_TGL"))

; ObjMod->add ik handle options

(ui-symbol "mo_addikhandle_solver"		(ui-symbol-reference "MO_ADD_IKHANDLE_SINGLE"))
(ui-symbol "mo_addikhandle_control"		(ui-symbol-reference "MO_ADDIK_CONTROL_TRANS"))
(ui-symbol "mo_addikhandle_plane_ctrl"	(ui-symbol-reference "MO_ADDIK_LOCAL_PLANE"))
(ui-symbol "mo_addikhandle_set_rest"		#f)
(ui-symbol "mo_addikhandle_weight_type" (ui-symbol-reference "MO_IK_WEIGHT_STICKY"))
(ui-symbol "mo_addikhandle_weight"			1.0)
(ui-symbol "mo_addikhandle_create_ee"		#f)
(ui-symbol "mo_addikhandle_goal"		(ui-symbol-reference "MO_ADD_IKHANDLE_POSITION"))

(ui-symbol "mo_addsphandle_pos_type"	(ui-symbol-reference "MO_ADDSP_POS_PARAM"))
(ui-symbol "mo_addsphandle_twst_type"	(ui-symbol-reference "MO_ADDSP_TWST_LINEAR"))
(ui-symbol "mo_addsphandle_twist_root"		#t)
(ui-symbol "mo_addsphandle_create_curve"	#f)
(ui-symbol "mo_addsphandle_snap_curve"		#t)
(ui-symbol "mo_addsphandle_plus_rhandle"	#t)

; move CV normal options

(ui-symbol "mo_cv_normal_scale" 0.025)




; xform reset options

(ui-symbol "mo_reset_pivots"            #t)


; proportional modification options

(ui-symbol "mp_pmod_command"            "PropMove")
(ui-symbol "mp_pmod_com"            "PropMove")
(ui-symbol "mo_pmod_type"               (ui-symbol-reference "MO_BOW"))
(ui-symbol "mo_pmod_move_mode"          0)
(ui-symbol "mo_pmod_udegree"            1.0)
(ui-symbol "mo_pmod_vdegree"            1.0)
(ui-symbol "mo_pmod_uprec"              0)
(ui-symbol "mo_pmod_vprec"              0)
(ui-symbol "mo_pmod_usucc"              0)
(ui-symbol "mo_pmod_vsucc"              0)
(ui-symbol "mo_pmod_poly_byst"			#t)
(ui-symbol "mo_pmod_poly_uprec"         1.0)
(ui-symbol "mo_pmod_poly_vprec"         1.0)
(ui-symbol "mo_pmod_poly_usucc"         1.0)
(ui-symbol "mo_pmod_poly_vsucc"         1.0)
(ui-symbol "mo_pmod_poly_edge_inc"      #t)
(ui-symbol "mo_pmod_poly_tround"		#t)
(ui-symbol "mo_pmod_poly_tdegree"       1.0)
(ui-symbol "mo_pmod_poly_tlevels"       5)
(ui-symbol "mo_pmod_poly_t_byvertex"    #t)

; mass property options

(ui-symbol "mo_volume"                  #t)
(ui-symbol "mo_surf_area"               #t)
(ui-symbol "mo_centroid"                #t)
(ui-symbol "mo_moment"                  #t)
(ui-symbol "mo_1st_moment"              #t)
(ui-symbol "mo_2nd_moment"              #t)

; mass property v.14 options
(ui-symbol "mo_mp_volume"				#t)
(ui-symbol "mo_mp_surf_area"			#t)
(ui-symbol "mo_mp_centroid"				#t)
(ui-symbol "mo_mp_1st_moment"			#t)
(ui-symbol "mo_mp_2nd_moment"			#t)
(ui-symbol "mo_mp_centroid_point"		#f)


; show stats options

(ui-symbol "mo_stats_interact"          (ui-symbol-reference "MO_STATSKEEP"))
(ui-symbol "mo_stats_transparency"      #f)

; construction presets

(ui-symbol "mo_vendor_default"          "User Defined" UI_SYMBOL_GROUP_UNITS)

; linear dimension options

(ui-symbol "mo_ldimen_defined_state"    #f UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_ldimen_number"           1)

(ui-symbol "mo_lmu_distance"            (ui-symbol-reference "MO_MILLIMETERS")
		   UI_SYMBOL_GROUP_UNITS)



(ui-symbol "mo_lsu_distance"            (ui-symbol-reference "MO_MILLIMETERS")
	 UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_lpu_distance"            (ui-symbol-reference "MO_MILLIMETERS")
	 UI_SYMBOL_GROUP_UNITS)

(ui-symbol "mo_scaling_lmu"             1.0 UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_scaling_lsu"             1.0 UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_scaling_lpu"             1.0 UI_SYMBOL_GROUP_UNITS)

(ui-symbol "mo_linear_update_grids"     #f)


; angular dimension options

(ui-symbol "mo_adimen_defined_state"    #f UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_adimen_number"           1)
(ui-symbol "mo_amu_angle"               (ui-symbol-reference "MO_ANG_DEGREES")
		   UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_asu_angle"               (ui-symbol-reference "MO_ANG_MINUTES")
		   UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_apu_angle"               (ui-symbol-reference "MO_ANG_SECONDS")
		   UI_SYMBOL_GROUP_UNITS)

(ui-symbol "mo_scaling_amu"             1.0 UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_scaling_asu"             1.0 UI_SYMBOL_GROUP_UNITS)
(ui-symbol "mo_scaling_apu"             1.0 UI_SYMBOL_GROUP_UNITS)


; tolerance table options
; Note: these values should be kept the same as those defined in
;	Modeling/stats/tolerance.c
; tolerances are stored in wire files, hence the specification of a group is
; given.

(ui-symbol "mo_tol_crv_fit"             0.01  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_continuity_gap"      0.01  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_continuity_angle"    0.1   UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_curvature"           0.1   UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_checkpoints"         5     UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_maxsurfspans"        100   UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_trim_crv_fit"        0.001 UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_cos_gap"             0.1   UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_vertex"              0.01  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_modeling_mode"           0     UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_allow_rationals"         #f    UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_allow_rat_primitives"        #f    UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_allow_rat_fillets_rounds"    #f    UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_allow_rat_curves_surfaces"   #f    UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_topological_G0"      0.02  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_topological_G1"      30.0  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_topological_G2"      1.0  UI_SYMBOL_GROUP_TOLERANCES)
(ui-symbol "mo_tol_auto_recalc"   #f)
(ui-symbol "mo_tol_disable_unused" #f)

; Default Modeling font properties

(ui-symbol "mo_font_default.fontsize" 'MO_FONT_FONTSIZE_DEFAULT)

; Modeling Text scaling modes and settings

(ui-symbol "mo_font.textScaleActive"     #f)
(ui-symbol "mo_font.userTextScaleActive" #f)
(ui-symbol "mo_font.userTextScaleFactor"  1.0)

; Adjacent surface checker options

(ui-symbol "checker.checkwhat" 'MO_CHECKER_FIND_G2)
(ui-symbol "checker.arc_stepsize"	0.1)
(ui-symbol "checker.steptype"	'MO_CHECKER_PARAM_STEP)
(ui-symbol "checker.persistence" #t)
(ui-symbol "checker.check_interior"	#f)
(ui-symbol "checker.show_maxLabels"	#f)
(ui-symbol "checker.show_edgeLabels" #f)
(ui-symbol "checker.show_comb" #f)
(ui-symbol "checker.auto_scale" #t)
(ui-symbol "checker.scaleX" 1.0)
(ui-symbol "checker.scaleY" 1.0)
(ui-symbol "checker.scaleZ" 1.0)

; tangent plane evaluation options

(ui-symbol "mo_taneval_ovlptol"         0.01)
(ui-symbol "mo_taneval_checkpoints"     10)
(ui-symbol "mo_taneval_continuity_angle" 0.1)
(ui-symbol "mo_taneval_init_scale"      10.0)
(ui-symbol "mo_taneval_curvature_check" #t)
(ui-symbol "mo_taneval_locator_persistance" #t)
(ui-symbol "mo_taneval_locator_simple" #f)
(ui-symbol "mo_taneval_init_t_scale"      10.0)
(ui-symbol "mo_taneval_init_c_scale"      5.0)
(ui-symbol "mo_taneval_crv_cont_display"     4)


; curve tangent projection options

(ui-symbol "mo_tanproj_init_scale"      1.0)
(ui-symbol "mo_tanproj_init_rotation"   0)
(ui-symbol "mo_tanproj_modify_range"    4)
(ui-symbol "mo_tanproj_keeporig"        (ui-symbol-reference "MO_TANPROJ_KEEPORIG_OFF"))
(ui-symbol "mo_tanproj_create_history"  #t)
(ui-symbol "mo_tanproj_tangent_angle"    0.0)


; values below are current linear/angular dimension units, and cannot be
; changed from the tolerance table option box

(ui-symbol "mo_tol_lin_unit"            (ui-symbol-reference "mo_lmu_distance"))
(ui-symbol "mo_tol_ang_unit"            (ui-symbol-reference "mo_amu_angle"))


; measure options

(ui-symbol "mo_measure_type"            (ui-symbol-reference "MO_LINEAR_DISTANCE"))
(ui-symbol "mo_arc_error"               10)


; volume options

(ui-symbol "mo_volume_type"             (ui-symbol-reference "MO_SOLID"))
(ui-symbol "mo_volume_boundary"         #f)
(ui-symbol "mo_volume_axis"             (ui-symbol-reference "MO_VOLUME_AXIS_Z"))
(ui-symbol "mo_volume_min_bound"        -1.0)
(ui-symbol "mo_volume_max_bound"        1.0)
(ui-symbol "mo_volume_thickness"        0.5)
(ui-symbol "mo_volume_precision"        16)
(ui-symbol "mo_volume_tolerance"        0.001)

(ui-symbol "mo_mp_volume_type"			(ui-symbol-reference "MO_SOLID"))
(ui-symbol "mo_mp_volume_thickness"		0.5)
(ui-symbol "mo_mp_volume_tolerance"		0.01)
(ui-symbol "mo_mp_moment_axis"			(ui-symbol-reference "MO_VOLUME_AXIS_X"))

; surface-mesh, mesh-mesh, and surface-surface deviation tool options
(ui-symbol "mo_dev_acceptable_distance" 0.1)
(ui-symbol "mo_dev_ramp_distance" 1.0)
(ui-symbol "mo_dev_identical_ramp" #f)
(ui-symbol "mo_dev_use_bands" #f)
(ui-symbol "mo_dev_tool_type" 0)

; contact analysis tool options
(ui-symbol "mo_contact_sphere_radius" 10.0)
(ui-symbol "mo_contact_curvature_radius" 0.1)
(ui-symbol "mo_contact_continuity_angle_tolerance" 0.0)

; Live scan
(ui-symbol "mo_livescan_resolution"			0.05)
(ui-symbol "mo_livescan_devacceptdist"      0.1)
(ui-symbol "mo_livescan_devrampdist"        1.0)
(ui-symbol "mo_livescan_transparency"		0.5)
(ui-symbol "mo_livescan_originpoint"		0.0 0.0 0.0)
(ui-symbol "mo_livescan_xpoint"				0.1 0.0 0.0)
(ui-symbol "mo_livescan_3point"				0.0 0.1 0.0)
(ui-symbol "mo_livescan_offset"				0.0 0.0 0.0)

; set coord options

(ui-symbol "mo_coordinate_sys"          (ui-symbol-reference "MO_WORLD_COORD"))


; set construction plane options

;(ui-symbol "mo_construct_type"         (ui-symbol-reference "MO_ORTHOGRAPHIC"))




; grid spacing options

(ui-symbol "mo_grdspace_by_move"        #f)
(ui-symbol "mo_grdmesh"             10.0)



(ui-symbol "mo_grid_labels"             #f)
(ui-symbol "mo_grddots"                 1)
(ui-symbol "mo_grid_all_windows"        #t)
(ui-symbol "mo_interactive_grid_all_windows"        #t)
(ui-symbol "mo_set_grid_all_windows"        #t)
(ui-symbol "mo_tgl_grid_options"        (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_set_grid_value"        (ui-symbol-reference 'mo_grdmesh))
(ui-symbol "mo_grid_label_font_override" #f)
(ui-symbol "mo_grid_label_fontsize"     'MO_FONT_FONTSIZE_DEFAULT)

; diagnostic Light options
(ui-symbol "mo_diag_light_show_name"		#f)

; construction point options
(ui-symbol "mo_cpoint_show_name"		#f)

; construction vector options
(ui-symbol "mo_lseg_show_name"			#f)

; construction plane options

(ui-symbol "mo_cplane_window"           #f )
(ui-symbol "mo_cplane_show_name"		#t )
(ui-symbol "mo_cplane_creation_type"	1)
(ui-symbol "mo_cplane_scale_handle"     #f)
(ui-symbol "mo_cplane_plane_handle"     #t)
(ui-symbol "mo_cplane_reflect_handle"   #t)
(ui-symbol "mo_cplane_rotate_handle"    #t)

; manipulator options

(ui-symbol "mo_manipulator_window"           #f)
(ui-symbol "mo_manipulator_free"             #t)
(ui-symbol "mo_manipulator_show_name"        #t)
(ui-symbol "mo_manipulator_scale_handle"     #t)
(ui-symbol "mo_manipulator_plane_handle"     #t)
(ui-symbol "mo_manipulator_reflect_handle"   #t)
(ui-symbol "mo_manipulator_rotate_handle"    #t)
(ui-symbol "mo_manipulator_explicit_func_end" #f)

; snap mode toggle vars

(ui-symbol "mo_magmode"                 #f)
(ui-symbol "mo_snapgrid"                #f)
(ui-symbol "mo_snapcrv"                 #f)
(ui-symbol "mo_snap_curve_end"			#f)
(ui-symbol "mo_snap_curve_mid"			#f)
(ui-symbol "mo_snap_curve_intersection"	#f)

; perspective window grid options
(ui-symbol "mo_persp_grid_extent"       320.0)

; grid set options

(ui-symbol "mo_cpc_interactive"         (ui-symbol-reference "MO_GRID_OBJECT"))
(ui-symbol "mp_create_construction_plane" "OBJPlane")
(ui-symbol "mp_cpc_exec"                (ui-symbol-reference "POP"))


; rotate construction plane options

(ui-symbol "mo_cp_rot_x"                0)
(ui-symbol "mo_cp_rot_y"                0)
(ui-symbol "mo_cp_rot_z"                0)
(ui-symbol "mo_originx"                 0.0)
(ui-symbol "mo_originy"                 0.0)
(ui-symbol "mo_originz"                 0.0)
(ui-symbol "mo_axis1_x"                 1.0)
(ui-symbol "mo_axis1_y"                 0.0)
(ui-symbol "mo_axis1_z"                 0.0)
(ui-symbol "mo_axis2_x"                 0.0)
(ui-symbol "mo_axis2_y"                 1.0)
(ui-symbol "mo_axis2_z"                 0.0)


; grid previous options

(ui-symbol "mo_grdprev"                 (ui-symbol-reference "MO_CUR_WIND"))


; grid reset options

(ui-symbol "mo_grdreset"                (ui-symbol-reference "MO_CUR_WIND"))


; delete video (image) options

(ui-symbol "mo_del_image_options"       (ui-symbol-reference "MO_ALL_WIND"))

; delete proj texture objects
(ui-symbol "mo_delprojtxt_all"	#f)
(ui-symbol "mo_delprojtxt_parent" #t)
(ui-symbol "mo_delprojtxt_parent_wobj" #f)

; delete windows options

(ui-symbol "mo_delwind"                 (ui-symbol-reference "MO_DELWIN_CURRENT"))


; delete all  options

(ui-symbol "mo_delshaders"              #t)
(ui-symbol "mo_dellights"               #t)

; delete all locators options
(ui-symbol "mo_dellocators_no_invisiable"              #t)
(ui-symbol "mo_dellocators_no_reference"               #t)
(ui-symbol "mo_dellocators_active"                     #f)

; delete constraints options

(ui-symbol "mo_del_constraints_hier"    #f)
(ui-symbol "mo_del_constraints_target"  (ui-symbol-reference "MO_DEL_CONSTRA_ALL"))
(ui-symbol "mo_del_constraints_type"    (ui-symbol-reference "MO_DEL_CONSTRA_TYPE_ALL"))


; delete selection handles options

(ui-symbol "mo_delselhandle_active"		#t)
(ui-symbol "mo_delselhandle_hier"		#f)

; delete guidelines options

(ui-symbol "de_guidelines_user_display_toggle"	#t)

; delete null nodes options
(ui-symbol "mo_delnull_cluster"			#f)

; views options

(ui-symbol "mo_eyex"                    0.0)
(ui-symbol "mo_eyey"                    0.0)
(ui-symbol "mo_eyez"                    0.0)
(ui-symbol "mo_viewx"                   0.0)
(ui-symbol "mo_viewy"                   0.0)
(ui-symbol "mo_viewz"                   0.0)
(ui-symbol "mo_upx"                     0.0)
(ui-symbol "mo_upy"                     0.0)
(ui-symbol "mo_upz"                     0.0)
(ui-symbol "mo_zoom"                    40.0)
(ui-symbol "mo_tumble_centre_type"      (ui-symbol-reference "MO_WORLD_POINT"))
(ui-symbol "mo_world_point_x"           0.0)
(ui-symbol "mo_world_point_y"           0.0)
(ui-symbol "mo_world_point_z"           0.0)

(ui-symbol "mo_persp_gain"              10.0)



(ui-symbol "mo_scaling"                 (ui-symbol-reference "MO_PROPORTIONAL"))
(ui-symbol "mo_lookat_frame"            #t)
(ui-symbol "mo_lookat_exclude_lights"	#f)
(ui-symbol "mo_lookat_exclude_textures"	#f)
(ui-symbol "mo_lookat_include_animation_rendering_objects"	#t)
(ui-symbol "mo_lookat_include_symmetric_objects"	#t)
(ui-symbol "mo_lookat_ground_relative"            #f)
(ui-symbol "mo_window_sync"				#t)
(ui-symbol "mo_window_zoom_locked"		#f)
(ui-symbol "mo_window_one2one"			#f)
(ui-symbol "mo_dolly.auto.zoom"         #t)


; views->turntable options

(ui-symbol "mo_trntbl_axis"             (ui-symbol-reference "REVOLVE_Z"))
(ui-symbol "mo_trntbl_dir"              (ui-symbol-reference "MO_TRNTBL_POS"))
(ui-symbol "mo_trntbl_pivot"            (ui-symbol-reference "MO_TRNTBL_CENTER_OF_BBOX"))
(ui-symbol "mo_trntbl_rate"             60.0)
(ui-symbol "mo_trntbl_file"             #f)

; View Flip /Both options

(ui-symbol "mo_view_flip_axis"          (ui-symbol-reference "MO_VIEW_FLIP_XZ"))


; windows->default  options

(ui-symbol "mo_windef"                  (ui-symbol-reference "MO_WINDEF_RESTORE"))


; newwin options

(ui-symbol "mo_newwin"                  (ui-symbol-reference "MO_FRONT"))
(ui-symbol "mo_newwin_showgrid"			#t)

; fullscreen options
(ui-symbol	"fullscreen.hidemainmenu"		#t)
(ui-symbol	"fullscreen.hidetitle"			#t)
(ui-symbol	"fullscreen.hidewindows"		#t)
(ui-symbol	"fullscreen.hideembedded"		#f)

; reopen option

(ui-symbol "mo_windreopen"              (ui-symbol-reference "MO_ALLAYERS"))


; tgl skeleton options
(ui-symbol "mo_tgl_skl_window"          (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_ikhandles"           #f)
(ui-symbol "mo_tgl_constraints"         #f)

; tgl constraints options
(ui-symbol "mo_tgl_constr_window"       (ui-symbol-reference "MO_ALL_WIND"))

; tgl ik handles options
(ui-symbol "mo_tgl_ik_han_window"       (ui-symbol-reference "MO_ALL_WIND"))

; tgl particle option
(ui-symbol "mo_tgl_part_window"         (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_part_display"        (ui-symbol-reference "MO_PSYS_LINE"))

; visible options

(ui-symbol "mp_visible_command"         "VisibleAll")
(ui-symbol "mo_visible_scope"           (ui-symbol-reference "MO_VISIBLE_ALL"))
(ui-symbol "mo_visible_objects"         #t)
(ui-symbol "mo_visible_locators"        #t)

; symbology (line style) options

(ui-symbol "mo_symbology_objects"       (ui-symbol-reference "MO_SYMBOLOGY_ACTIVE"))
(ui-symbol "mo_symbology_display"       (ui-symbol-reference "MO_SYMBOLOGY_SOLID"))

; surface style options

(ui-symbol "mo_surfstyle_boundary"		(ui-symbol-reference "MO_LINEWIDTH_DOUBLE"))
(ui-symbol "mo_surfstyle_interior"		(ui-symbol-reference "MO_SURFSTYLE_DASHED"))
(ui-symbol "mo_surfstyle_vhull"		    (ui-symbol-reference "MO_SURFSTYLE_SOLID"))
(ui-symbol "mo_surfstyle_hull_width"    (ui-symbol-reference "MO_LINEWIDTH_SINGLE"))
(ui-symbol "mo_surface_cv_icon"			-1)

; curve style options

(ui-symbol "mo_curve_line_width"		(ui-symbol-reference "MO_LINEWIDTH_SINGLE"))
(ui-symbol "mo_curve_hull_width"		(ui-symbol-reference "MO_LINEWIDTH_SINGLE"))
(ui-symbol "mo_curve_cv_icon"			-1)
(ui-symbol "mo_curve_ep_icon"			-1)

; scan data style options

(ui-symbol "mo_scandata_icon"			-1)
(ui-symbol "mo_blendpoint_icon_style"	 1)
(ui-symbol "mo_scandata_lines"			#t)
(ui-symbol "mo_scandata_showlines"		#t)
(ui-symbol "mo_scandata_linestyle"		 0)
(ui-symbol "mo_symmetry_linestyle"		 1)

; symmetry style options
(ui-symbol "mo_symmetry_linestyle"		 1)

; visual curve style options
(ui-symbol "mo_visual_curve_line_width"  (ui-symbol-reference "MO_LINEWIDTH_SINGLE"))

;
; Default curve precision values
;


; xsection options

(ui-symbol "mo_xsection_type"			0)
(ui-symbol "mo_xsection_start"			-10.0 -10.0 -10.0)
(ui-symbol "mo_xsection_end"			10.0 10.0 10.0)
(ui-symbol "mo_xsection_step"			1.0 1.0 1.0)
(ui-symbol "mo_xsection_create_section_data"	#t)
(ui-symbol "mo_xsection_section_data_tol"       0.01)

(ui-symbol "mo_xsection_parallel_mode"  #t)
(ui-symbol "mo_xsection_usage_x"        #t)
(ui-symbol "mo_xsection_usage_y"        #t)
(ui-symbol "mo_xsection_usage_z"        #t)
(ui-symbol "mo_xsection_event_x"        (ui-symbol-reference "XSEC_INVALID_AXIS" ))
(ui-symbol "mo_xsection_event_y"        (ui-symbol-reference "XSEC_INVALID_AXIS" ))
(ui-symbol "mo_xsection_event_z"        (ui-symbol-reference "XSEC_INVALID_AXIS" ))
(ui-symbol "mo_xsection_rebuild"        #f)
(ui-symbol "mo_xsection_history"        #t)
(ui-symbol "mo_xsection_auto_range"     #t)
(ui-symbol "mo_xsection_auto_range_x"   #t)
(ui-symbol "mo_xsection_auto_range_y"   #t)
(ui-symbol "mo_xsection_auto_range_z"   #t)
(ui-symbol "mo_xsection_variable_step"     #f)
(ui-symbol "mo_xsection_polyline"		#t)
(ui-symbol "mo_xsection_curvature_x"		#f)
(ui-symbol "mo_xsection_curvature_y"		#f)
(ui-symbol "mo_xsection_curvature_z"		#f)
(ui-symbol "mo_xsection_event_curvature_x"		(ui-symbol-reference "XSEC_INVALID_AXIS" ))
(ui-symbol "mo_xsection_event_curvature_y"		(ui-symbol-reference "XSEC_INVALID_AXIS" ))
(ui-symbol "mo_xsection_event_curvature_z"		(ui-symbol-reference "XSEC_INVALID_AXIS" ))
;; obsolete variable
(ui-symbol "mo_xsection_update_axis"		(ui-symbol-reference "XSEC_INVALID_AXIS" ))
;; obsolete variable
(ui-symbol "mo_xsection_update_value"		#f)

(ui-symbol "mo_xsection_start_x"    -500.0)
(ui-symbol "mo_xsection_start_y"    -500.0)
(ui-symbol "mo_xsection_start_z"    -500.0)
(ui-symbol "mo_xsection_end_x"      500.0)
(ui-symbol "mo_xsection_end_y"      500.0)
(ui-symbol "mo_xsection_end_z"      500.0)
(ui-symbol "mo_xsection_step_x"     10.0)
(ui-symbol "mo_xsection_step_y"     10.0)
(ui-symbol "mo_xsection_step_z"     10.0)

; For use with radial sections
(ui-symbol "mo_xsection_center_x"        0.0)
(ui-symbol "mo_xsection_center_y"        0.0)
(ui-symbol "mo_xsection_center_z"        0.0)
(ui-symbol "mo_xsection_radial_sections" 10)
(ui-symbol "mo_xsection_pick_chain"      #f)

(ui-symbol "mo_xsection_promote_type"  0)
(ui-symbol "mo_xsection_sort_sections"   #t)
(ui-symbol "mo_xsection_merge_sections"  #t)
(ui-symbol "mo_xsection_promote_tol"  0.01)

; For the xsection group editor
(ui-symbol "mo_xsection_group_group_name" "My XSections" )
(ui-symbol "mo_xsection_group_usePicked" #t )
(ui-symbol "mo_xsection_group_lockCurvature" #f )
(ui-symbol "mo_xsection_group_use_x" #t )
(ui-symbol "mo_xsection_group_use_y" #t )
(ui-symbol "mo_xsection_group_use_z" #t )
(ui-symbol "mo_xsection_group_auto_range" #t )
(ui-symbol "mo_xsection_group_start" -500.0 -500.0 -500.0 )
(ui-symbol "mo_xsection_group_end" 500.0 500.0 500.0 )
(ui-symbol "mo_xsection_group_step" 10.0 10.0 10.0 )
(ui-symbol "mo_xsection_group_store_as_default" #f )
(ui-symbol "mo_xsection_group_numCurvatureSamples" 20 )

(ui-symbol "mo_xsection_axis_discrete_location" 0.0 )
(ui-symbol "mo_xsection_axis_buttons" "Buttons" )

; For the UI function required by radial visual cross sections
(ui-symbol "mo_radXSec_num_planes" 10)
(ui-symbol "mo_radXSec_chain" #f)

; For the UI function required by planar visual cross sections
(ui-symbol "mo_planarXSec_num_planes" 1)
(ui-symbol "mo_planarXSec_step" 10.0)
(ui-symbol "mo_planarXSec_mirror_planes" #f)

; For the UI function required by picked reference visual cross sections
(ui-symbol "mo_refXSec_num_planes" "0")

(ui-symbol "mo_xsection_apply_global" #f)

; patch precision option

(ui-symbol "mo_patch_precision"         (ui-symbol-reference "MO_PREC_BOTH"))

; hull precision option

(ui-symbol "mo_hull_precision_udefault" 1)
(ui-symbol "mo_hull_precision_vdefault" 1)


; display objects options for Hide unselected
(ui-symbol "hideunselected.camera"		0)
(ui-symbol "hideunselected.light"		0)
(ui-symbol "hideunselected.texture"		0)

; display objects options for subdivision

(ui-symbol "mo_sbdv_funct"              (ui-symbol-reference "MO_SBDV_LOADVARS"))
(ui-symbol "mo_sbdv_edit"               (ui-symbol-reference "MO_SBDV_ACTOBJ"))

(ui-symbol "mo_gsbdv_type"              (ui-symbol-reference "MO_SBDV_NONADAPT"))
(ui-symbol "mo_gsbdv_min"               2)
(ui-symbol "mo_gsbdv_max"               16)
(ui-symbol "mo_gsbdv_thresh"            00960)
(ui-symbol "mo_gsbdv_u"                 4)
(ui-symbol "mo_gsbdv_v"                 4)

(ui-symbol "mo_osbdv_type"              (ui-symbol-reference "MO_SBDV_NONADAPT"))
(ui-symbol "mo_osbdv_min"               2)
(ui-symbol "mo_osbdv_max"               16)
(ui-symbol "mo_osbdv_thresh"            00960)
(ui-symbol "mo_osbdv_u"                 4)
(ui-symbol "mo_osbdv_v"                 4)


; display modes options

(ui-symbol "mo_tgl_lights_options"      (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_textures_options"    (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_pivots_options"      (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_selection_handles_options" (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_selection_handles_label" #t)
(ui-symbol "mo_tgl_seleHdl_label_state_change" #f)
(ui-symbol "mo_tgl_cull_options"        (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_cull_on"             #t)
(ui-symbol "mo_tgl_cull_style"          (ui-symbol-reference "MO_TGL_CULL_FACE"))
(ui-symbol "mo_tgl_cull_color_on"		#f)
(ui-symbol "mo_tgl_cull_color_style"	(ui-symbol-reference "MO_TGL_PCOLOR_WIRE"))
(ui-symbol "mo_tgl_cull_filled_option"	(ui-symbol-reference "MO_TGL_PCOLOR_ZBUF"))
(ui-symbol "mo_tgl_cull_uv_on"          #f)
(ui-symbol "mo_tgl_cull_topo_on"        #f)
(ui-symbol "mo_tgl_cull_pgon_sel_on"    #f)
(ui-symbol "mo_tgl_cull_edge_affected_off" #t)
(ui-symbol "mo_tgl_cull_pts_only_on"	#f)
(ui-symbol "mo_tgl_cull_state_change"	#f)
(ui-symbol "mo_tgl_cull_showstats"	#f)
(ui-symbol "mo_tgl_cull_showstats.instances" #t)
(ui-symbol "mo_tgl_cull_showstats.templates" #f)
(ui-symbol "mo_tgl_cull_showstats.warn_vcount" 0)
(ui-symbol "mo_tgl_cull_showstats.warn_pcount" 0)

(ui-symbol "mo_tgl_lcl_axes_options"    #f)
(ui-symbol "mo_tgl_single_chain_opt"	#t)
(ui-symbol "mo_tgl_axes_state_change"   #f)
(ui-symbol "mo_tgl_ikhan_state_change"  #f)
(ui-symbol "mo_tgl_model_options"       (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_tgl_model_include_cv"	#t)
(ui-symbol "mo_tgl_tv_options"          (ui-symbol-reference "MO_TGL_TV"))
(ui-symbol "mo_tgl_camera_options"      (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_disp_frustrum_options"   (ui-symbol-reference "MO_FRUSTRUM_HALF"))
(ui-symbol "mo_tgl_frustrum_state_change" #f)
(ui-symbol "mo_tgl_image_options"       (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_imagedisplay_type"       #t)
(ui-symbol "mo_tgl_canvas_options"      (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mo_canvasdisplay_type"      0)
(ui-symbol "mo_disp_object"             (ui-symbol-reference "MO_PICKED_OBJECTS"))
(ui-symbol "mo_tgl_shade_display"       (ui-symbol-reference "MO_TGL_SHADE_CONT"))
(ui-symbol "mo_tglshade_display_tesselation" #f )
(ui-symbol "mo_tgl_shade_options"       #t )

(ui-symbol "diag_shade_tess_limit_edge_length" #f)
(ui-symbol "diag_shade_tess_max_edge_length" 10.0)

(ui-symbol "mo_shade_auto_update"		#t)
(ui-symbol "mo_shade_self_shadows"		#f)
(ui-symbol "mo_shade_force_shader"	1)
(ui-symbol "mo_tglshade_use_fileSyms"      #f)
(ui-symbol "mo_tglshade_tess_flavor" (ui-symbol-reference "MO_TGLSHADE_ARUBA_TESSELATOR"))
(ui-symbol "mo_tglshade_tess_preset" 'MO_TGLSHADE_TESS_PRESET_HIGH)
(ui-symbol "mo_tglshade_tess_limit_edge_length" #f)
(ui-symbol "mo_tglshade_enable_gp" #f)
(ui-symbol "mo_tglshade_enable_lt" #f)
(ui-symbol "mo_tglshade_tess_max_edge_length" 10.0)
(ui-symbol "mo_tglshade_default_shading" 'DN_SHADE_MULTI_COLOR)
(ui-symbol "mo_tglshade_default_texturing" 'MO_TGLSHADE_TEXTURE1)
(ui-symbol "mo_tglshade_clearcoat"      #t)
(ui-symbol "mo_tglshade_texture_res"    'MO_TGLSHADE_TEXTURE_HIGH)
(ui-symbol "mo_tglshade_shadow_style"    1)
(ui-symbol "mo_tglshade_shadow_blur"	 0.0)
(ui-symbol "mo_tglshade_shadow_position" 1)
(ui-symbol "mo_tglshade_shadows"		#f)
(ui-symbol "mo_tglshade_groundplane"			#f)
(ui-symbol "mo_tglshade_groundplaneoutline"		#f)
(ui-symbol "mo_tglshade_groundplanereflection"		#f)
(ui-symbol "mo_tglshade_groundplanereflectivity"		0.50)
(ui-symbol "mo_tglshade_groundplanedepthreflectivity"	50000.00)
(ui-symbol "mo_tglshade_groundplaneblurreflection"		0.00)
(ui-symbol "mo_tglshade_groundplanedepthinterval"		0.00)
(ui-symbol "mo_tglshade_depth_of_field"		#f)
(ui-symbol "mo_tglshade_shaderglow"		#f)
(ui-symbol "mo_tglshade_shaderglow_quality"		0.5)
(ui-symbol "mo_tglshade_optimizegroundplanereflection"		#f)
(ui-symbol "mo_tglshade_optimizeshaderglow"		#f)
(ui-symbol "mo_use_optimize_selfshadows_on_tumble" #f)
(ui-symbol "mo_diagnostic_lighting_ambient"			0.5)
(ui-symbol "mo_diagnostic_lighting_diffuse"			0.5)
(ui-symbol "mo_antialias_is_line_on"			#t)
(ui-symbol "mo_antialias_is_surface_on"			#f)
(ui-symbol "mo_antialias_single_line_width"		0.5)
(ui-symbol "mo_antialias_double_line_width"		1.0)
(ui-symbol "mo_antialias_quality"		4)
(ui-symbol "mo_antialias_samples"		16)
(ui-symbol "mo_antialias_radius"		1.0)
(ui-symbol "mo_tglshade_shadow_transparency"       0.25)
(ui-symbol "mo_tglshade_shadow_plane_Z"            0.0)
(ui-symbol "mo_tglshade_shadow_plane_auto"            #t)
(ui-symbol "ir_tglshade_tol"            0.01)
(ui-symbol "mo_tglshade_lighting"       'MO_TGLSHADE_DEFAULT_LITE)
(ui-symbol "mo_tglshade_light_tunnel" #f )
(ui-symbol "mo_tglshade_light_lock"		#f)  ;obsolete -- replaced by mo_dshade_cameraLinkLight with inverse logic
(ui-symbol "mo_tglshade_windows_only"   #t)
(ui-symbol "mo_tglshade_objects_only"   #t)
(ui-symbol "mo_tglshade_layeredshaders"	#t)
(ui-symbol "mo_tglshade_show_background" #f)
(ui-symbol "mo_tglshade_reflect_background" #t)
(ui-symbol "mo_tglshade_groundplaneshadows" #f)
(ui-symbol "mo_tglshade_pinch_model" #f)
(ui-symbol "mo_hiddenLine_all_windows" #f)
(ui-symbol "mo_hiddenLine_no_silhouettes_on_tumble" #t)
(ui-symbol "mo_hiddenLine_use_existing" #t)
(ui-symbol "mo_hiddenLine_tess_type" (ui-symbol-reference "MO_TGLSHADE_ARUBA_TESSELATOR") )
(ui-symbol "mo_hiddenLine_tolerance" 0.01)
(ui-symbol "mo_hiddenLine_limit_edge_length" #f)
(ui-symbol "mo_hiddenLine_max_edge_length" 10.0)
(ui-symbol "mo_diagnosticshade_lighting" 'MO_TGLSHADE_DEFAULT_LITE)
(ui-symbol "mo_diagnosticshade_light_quality" 2)
(ui-symbol "mo_diagnosticshade_reflections" #f)
(ui-symbol "mo_diagnosticshade_environment" 0)
(ui-symbol "mo_diagnosticshade_reflectivity" 0.5)
(ui-symbol "mo_diagnosticshade_texture_map_type" 5 )
(ui-symbol "mo_diagnosticshade_has_texture_lighting" #t)

(ui-symbol "mo_diag_shade_layered_shade_type"	 'DN_SHADE_NONE)
(ui-symbol "mo_diag_shade_layered_srf_eval_type" 8)
(ui-symbol "mo_diag_shade_layered_transp" 0.80)
(ui-symbol "mo_diag_shade_layered_texture_scale" 1.00)
(ui-symbol "mo_diag_shade_layered_lighting_ambient" 0.50)
(ui-symbol "mo_diag_shade_layered_lighting_diffuse" 0.50)

(ui-symbol "mo_diag_shade_light_tunnel_visible"          #t)
(ui-symbol "mo_diag_shade_light_tunnel_band_color"       255.0 255.0 255.0)
(ui-symbol "mo_diag_shade_light_tunnel_number_of_bands"  10)
(ui-symbol "mo_diag_shade_light_tunnel_intensity"        1.0)
(ui-symbol "mo_diag_shade_light_tunnel_band_width"       0.2)
(ui-symbol "mo_diag_shade_light_tunnel_band_fringe"      0.0)
(ui-symbol "mo_diag_shade_light_tunnel_length"           1000.0)
(ui-symbol "mo_diag_shade_light_tunnel_radius"           100.0)
(ui-symbol "mo_diag_shade_light_tunnel_rotation"         0.0 0.0 0.0)
(ui-symbol "mo_diag_shade_light_tunnel_translation"      0.0 0.0 0.0)

(ui-symbol "mo_diag_shade_layered_stripe_texture_type" 'MO_DYNSHADE_STRIPE_TEXTURE_HORIZ_BW)
(ui-symbol "mo_diagnosticshade_zebraColor1"      0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_zebraColor2"      255.0 255.0 255.0)
(ui-symbol "mo_diagnosticshade_zebraThickness"      1.0)

(ui-symbol "mo_diagnosticshade_clayColor"              126.0 97.0 75.0)
(ui-symbol "mo_diagnosticshade_clayConcentration"      0.3)
(ui-symbol "mo_diagnosticshade_clayContrast"           1.0)
(ui-symbol "mo_diagnosticshade_clayEnabled"            #t)

(ui-symbol "mo_diagnosticshade_saddle_lockeye"       #f)
(ui-symbol "mo_diagnosticshade_saddle_color1"        255.0 255.0 255.0)
(ui-symbol "mo_diagnosticshade_saddle_color2"        0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_saddle_vec"           0.0 0.0 1.0)
(ui-symbol "mo_diagnosticshade_saddle_numbands"      8)
(ui-symbol "mo_diagnosticshade_saddle_thickness"     0.01)
(ui-symbol "mo_diagnosticshade_saddle_sharpness"     0.5)

(ui-symbol "mo_diagnosticshade_layered_saddle_lockeye"       #f)
(ui-symbol "mo_diagnosticshade_layered_saddle_color1"        255.0 255.0 255.0)
(ui-symbol "mo_diagnosticshade_layered_saddle_color2"        0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_layered_saddle_vec"           0.0 0.0 1.0)
(ui-symbol "mo_diagnosticshade_layered_saddle_numbands"      8)
(ui-symbol "mo_diagnosticshade_layered_saddle_thickness"     0.01)
(ui-symbol "mo_diagnosticshade_layered_saddle_sharpness"     0.5 )

(ui-symbol "mo_shade_geom_all"     #t)
(ui-symbol "mo_tglshade_speed"          #t)  ;obsolete
(ui-symbol "mo_tglshade_speed_textures" #t)
(ui-symbol "mo_tglshade_speed_prelight" 1)
(ui-symbol "mo_tglshade_tol"            0.01)
(ui-symbol "mo_tglshade_tess"           #f)
(ui-symbol "mo_tglshade_lighting.kind"  'MO_TGLSHADE_LIGHTING_DEFAULT)
(ui-symbol "mo_tglshade_light_intensity"       0.7)
(ui-symbol "mo_tglshade_material_shininess"    0.1)
(ui-symbol "mo_tglshade_material_red"   204.0)
(ui-symbol "mo_tglshade_material_green" 204.0)
(ui-symbol "mo_tglshade_material_blue"  204.0)
(ui-symbol "mo_tglshade_poffset"        #t)
(ui-symbol "mo_diagshade_texture_lock" #f)
(ui-symbol "mo_tglshade_texture_scale"  1.000)

(ui-symbol "mo_diagnosticshade_multicolor_transp"         0.0)
(ui-symbol "mo_diagnosticshade_random_transp"             0.0)
(ui-symbol "mo_diagnosticshade_isoangle_transp"           0.0)
(ui-symbol "mo_diagnosticshade_zebra_transp"              0.0)
(ui-symbol "mo_diagnosticshade_surface_eval_transp"       0.0)
(ui-symbol "mo_diagnosticshade_user_texture_transp"       0.0)
(ui-symbol "mo_diagnosticshade_clayAO_transp"             0.0)
(ui-symbol "mo_diagnosticshade_light_tunnel_transp"       0.0)
(ui-symbol "mo_diagnosticshade_saddle_transp"             0.0)

(ui-symbol "mo_tglshade_random_saturation" 0.8)
(ui-symbol "mo_tglshade_user_texture" "")
(ui-symbol "mo_tglshade_curvature_type" 32 )  ;OBOSLETE
(ui-symbol "mo_dynshade_srf_eval_type"	19)  ;Draft Angle
(ui-symbol "dn_curva_band_centre"		0.0)  ;obsolete
(ui-symbol "dn_curva_band_width"		0.0)  ;obsolete
(ui-symbol "dn_radius_band_centre"		1.0e30) ;obsolete
(ui-symbol "dn_radius_band_width"		0.0) ;obsolete
(ui-symbol "dn_radius_threshold"		0.5) ; 5 mm is a good default threshold, used
											 ; by evalviewer as well.
(ui-symbol "dn_radius_threshold_enabled" #f)
(ui-symbol "dn_max_radius_threshold"			1000.0) ; 10 m
(ui-symbol "dn_max_radius_threshold_enabled"	#f)

(ui-symbol "mo_dynshade_tess_type" 'MO_DYNSHADE_TESSELLATOR_ARUBA_FAST)
(ui-symbol "mo_dynshade_stripe_texture_type" 'MO_DYNSHADE_STRIPE_TEXTURE_HORIZ_BW)
(ui-symbol "mo_dynshade_ui_shade_type"	'DN_SHADE_NONE)
(ui-symbol "mo_dynshade_ui_srf_eval_type"	19) ;Draft Angle
(ui-symbol "mo_dynshade_ui_crv_eval_type"	8) ;Principal max curvature

; All settings
(ui-symbol "mo_disp_cv"                 #f)
(ui-symbol "mo_disp_key_point"          #f)
(ui-symbol "mo_disp_blend_point"        #f)
(ui-symbol "mo_disp_edit"               #f)
(ui-symbol "mo_disp_hull"               #f)
(ui-symbol "mo_disp_iso"				#t)
(ui-symbol "mo_disp_iso_u"				#t)
(ui-symbol "mo_disp_iso_v"				#t)
(ui-symbol "mo_disp_trim_cv"            #f)
(ui-symbol "mo_disp_precision"   		0 )

; Active settings
(ui-symbol "mo_disp_active_cv"          #t)
(ui-symbol "mo_disp_active_edit"        #t)
(ui-symbol "mo_disp_active_key_point"   #t)
(ui-symbol "mo_disp_active_blend_point" #t)
(ui-symbol "mo_disp_active_hull"        #t)
(ui-symbol "mo_disp_active_iso"			#t)
(ui-symbol "mo_disp_active_iso_u"		#t)
(ui-symbol "mo_disp_active_iso_v"		#t)
(ui-symbol "mo_disp_active_normal"      #t)
(ui-symbol "mo_disp_active_precision"   0 )

; New crv settings
(ui-symbol "mo_disp_crv_cv"             #t)
(ui-symbol "mo_disp_crv_edit"           #t)
(ui-symbol "mo_disp_crv_hull"           #t)
(ui-symbol "mo_disp_crv_normal"         #f)

; New Blend Crv settings
(if (ui-symbol-true "alias_gm_blend_display" )
   	(begin
	  (ui-symbol "mo_disp_crv_blend_cv"       #t)
	  (ui-symbol "mo_disp_crv_blend_hull"     #t)
	  )

	(ui-symbol "mo_disp_crv_blend_cv"       #f)
	(ui-symbol "mo_disp_crv_blend_hull"     #f)
)
(ui-symbol "mo_disp_crv_blend_edit"     #f)
(ui-symbol "mo_disp_crv_blend_point"    #t)

; New Keypoint Crv settings
(ui-symbol "mo_disp_crv_keypoint_cv"    #f)
(ui-symbol "mo_disp_crv_keypoint_edit"  #f)
(ui-symbol "mo_disp_crv_keypoint_hull"  #f)
(ui-symbol "mo_disp_crv_key_point"      #t)

; New scanline settings
(ui-symbol "mo_disp_scan_cv"            #t)
(ui-symbol "mo_disp_scan_hull"          #t)
(ui-symbol "mo_disp_scan_key_point"     #t)
(ui-symbol "mo_disp_scan_edit"          #t)

; New srf settings
(ui-symbol "mo_disp_srf_cv"             #f)
(ui-symbol "mo_disp_srf_hull"           #f)
(ui-symbol "mo_disp_srf_iso"			#t)
(ui-symbol "mo_disp_srf_iso_u"			#t)
(ui-symbol "mo_disp_srf_iso_v"			#t)
(ui-symbol "mo_disp_srf_precision"  	2 )
(ui-symbol "mo_disp_srf_edit"           #f)
(ui-symbol "mo_disp_srf_key_point"      #f)
(ui-symbol "mo_disp_srf_normal"         #f)

; New poly settings
(ui-symbol "mo_disp_poly_key_point"     #f) ;obsolete
(ui-symbol "mo_disp_poly_hull"          #f) ;obsolete
(ui-symbol "mo_disp_poly_cv"            #t) ;obsolete
(ui-symbol "mo_disp_poly_edit"          #f) ;obsolete
(ui-symbol "mo_disp_poly_normal"		#f)

; Display styles, for polys only
(ui-symbol "mo_disp_normals_override"   0)
(ui-symbol "mo_disp_poly_normal_style"	1)
(ui-symbol "mo_disp_poly_normal_scale"	0.5)
(ui-symbol "mo_disp_poly_alpha_style"   #t)
(ui-symbol "mo_disp_poly_cdepth_style"  0)
(ui-symbol "mo_disp_poly_normal_arrow_style" #t)
(ui-symbol "mo_disp_poly_normal_scale_style" #t)
(ui-symbol "mo_disp_poly_normal_label_style" #f)

; quick wire options

(ui-symbol "mo_qkwire_quality"          30.0)
(ui-symbol "mo_qkwire_all"              #f)

; full contour options

(ui-symbol "mo_contour_type"    (ui-symbol-reference "MO_CONTOUR_UVPATCH"))
(ui-symbol "mo_contour_ret"              #f)
(ui-symbol "mo_contour_all"              #f)
(ui-symbol "mo_uvpatch_precision"          0.0)
(ui-symbol "mo_uvsurface_precision"          5.0)
(ui-symbol "mo_section_colors"              #t)
(ui-symbol "mo_uvcubic_uspacing"          5.0)
(ui-symbol "mo_uvcubic_uoffset"          0.0)
(ui-symbol "mo_uvcubic_vspacing"          5.0)
(ui-symbol "mo_uvcubic_voffset"          0.0)
(ui-symbol "mo_section_xspacing"          1.0)
(ui-symbol "mo_section_yspacing"          1.0)
(ui-symbol "mo_section_zspacing"          1.0)
(ui-symbol "mo_section_xoffset"          0.0)
(ui-symbol "mo_section_yoffset"          0.0)
(ui-symbol "mo_section_zoffset"          0.0)
(ui-symbol "mo_section_x"              #t)
(ui-symbol "mo_section_y"              #t)
(ui-symbol "mo_section_z"              #t)

; face options

(ui-symbol "mo_planar_srf_create_history" #t)
(ui-symbol "mo_planar_srf_chain_select" #t)

; rail options

(ui-symbol "mp_railsrf_command"			"Birail_I")
(ui-symbol "mp_railsrf_com"			    "Birail_I")
(ui-symbol "mo_rail_gencrvs"          1)
(ui-symbol "mo_rail_pathcrvs"         2)
(ui-symbol "mo_rail_sweepmode"        (ui-symbol-reference "MO_BIRAIL_PROPORTIONAL"))
(ui-symbol "mo_rail_swproj"           (ui-symbol-reference "MO_BIRAIL_ACTIVE"))
(ui-symbol "mo_rail_contsgc"          (ui-symbol-reference "MO_BIRAIL_CONT_OFF"))
(ui-symbol "mo_rail_contegc"          (ui-symbol-reference "MO_BIRAIL_CONT_OFF"))
(ui-symbol "mo_rail_contspc"          (ui-symbol-reference "MO_BIRAIL_CONT_OFF"))
(ui-symbol "mo_rail_contepc"          (ui-symbol-reference "MO_BIRAIL_CONT_OFF"))
(ui-symbol "mo_rail_transform"        (ui-symbol-reference "MO_BIRAIL_SCALE"))
(ui-symbol "mo_rail_blend"            #t)
(ui-symbol "mo_rail_blend_value"      0.5)
(ui-symbol "mo_rail_crvseg"           #f)
(ui-symbol "mo_rail_view_vector"      1.0 0.0 0.0)
(ui-symbol "mo_rail_space1_pivot"      0.0 0.0 0.0)
(ui-symbol "mo_rail_space2_pivot"      0.0 0.0 0.0)
(ui-symbol "mo_rail_explicit_control"  #f)
(ui-symbol "mo_rail_srfDegreeGen"  3)
(ui-symbol "mo_rail_srfDegreePath"  3)
(ui-symbol "mo_rail_degreeSync"  #f)
(ui-symbol "mo_rail_continuity_check"  #f)
(ui-symbol "mo_rail_cont_max_iter"    10)
(ui-symbol "mo_rail_explicitSpansGen"  1)
(ui-symbol "mo_rail_explicitSpansPath" 1)
(ui-symbol "mo_rail_rebuild_path1"    #f)
(ui-symbol "mo_rail_rebuild_path2"    #f)
(ui-symbol "mo_rail_rebuild_gen1"     #f)
(ui-symbol "mo_rail_rebuild_genL"     #f)
(ui-symbol "mo_rail_rebuild_genI"     #f)
(ui-symbol "mo_rail_explicit_max_iter" 0)
(ui-symbol "mo_rail_achieved_continuity_check"  #t)
(ui-symbol "mo_rail_surfeval"          (ui-symbol-reference "MO_SWEPT_SURFEVAL_OFF"))
(ui-symbol "mo_rail_pivots"            (ui-symbol-reference "MO_SWEPT_CLOSEST"))
(ui-symbol "mo_rail_fixedcrv"          (ui-symbol-reference "MO_SWEPT_PATH"))
(ui-symbol "mo_rail_scale_xform"       1.0)
(ui-symbol "mo_rail_rotate_xform"      0.0)
(ui-symbol "mo_rail_gen1_pivot"        0.0)
(ui-symbol "mo_rail_gen2_pivot"        0.0)
(ui-symbol "mo_rail_path_pivot1"       0.0)
(ui-symbol "mo_rail_path_pivot2"       0.0)
(ui-symbol "mo_rail_gen1_segment_start"  0.0)
(ui-symbol "mo_rail_gen1_segment_end"  0.0)
(ui-symbol "mo_rail_gen2_segment_start" 0.0)
(ui-symbol "mo_rail_gen2_segment_end" 0.0)
(ui-symbol "mo_rail_path1_segment_start" 0.0)
(ui-symbol "mo_rail_path1_segment_end" 0.0)
(ui-symbol "mo_rail_path2_segment_start" 0.0)
(ui-symbol "mo_rail_path2_segment_end" 0.0)
(ui-symbol "mo_rail_history"           #t)
(ui-symbol "mo_rail_auto_recalc"       #t)
(ui-symbol "mo_rail_xsec_show_previous" #f)
(ui-symbol "mo_rail_boundary_labels"  #t)
(ui-symbol "mo_rail_insert_at_midpoint"  #f)
(ui-symbol "mo_rail_colinear_isoparms"  #f)
(ui-symbol "mo_swept_sweepmode"         (ui-symbol-reference "MO_SWEPT_NATURAL"))
(ui-symbol "mo_rail_colinear_path1"    #f)
(ui-symbol "mo_rail_colinear_path2"    #f)
(ui-symbol "mo_rail_colinear_gen1"     #f)
(ui-symbol "mo_rail_colinear_genL"     #f)

; ball corner surface options
(ui-symbol "mo_ballcorner_pivot_length" 0.7)
(ui-symbol "mo_ballcorner_pivot_length_start" 0.7)
(ui-symbol "mo_ballcorner_pivot_length_end" 0.7)
(ui-symbol "mo_ballcorner_create_history"   #t)
(ui-symbol "mo_ballcorner_auto_recalc"  #t)
(ui-symbol "mo_ballcorner_continuity_check"  #f)
(ui-symbol "mo_ballcorner_max_spans"    10)
(ui-symbol "mo_ballcorner_continuity_type"  0)
(ui-symbol "mo_ballcorner_degree_sides"  3)
(ui-symbol "mo_ballcorner_degree_pivot"  3)
(ui-symbol "mo_ballcorner_spans_sides"  1)
(ui-symbol "mo_ballcorner_spans_pivot"  1)
(ui-symbol "mo_ballcorner_build_surface"  #t)
(ui-symbol "mo_ballcorner_trim_primary"   #t)
(ui-symbol "mo_ballcorner_center_adjust"  #f)
(ui-symbol "mo_ballcorner_center_height"  0.0)
(ui-symbol "mo_ballcorner_explicit_control"  #f)
(ui-symbol "mo_ballcorner_show_helpers"  #f)

; square surface options

(ui-symbol "mo_square_have_surfaces"    #f)
(ui-symbol "mo_square_concrvs"          (ui-symbol-reference "MO_SQUARE_CONCRVS_ON"))
(ui-symbol "mo_square_recon"            (ui-symbol-reference "MO_AUTO_RECON_ON"))
(ui-symbol "mo_square_blendmode"        (ui-symbol-reference "MO_SQUARE_BLENDMODE_LINEAR"))
(ui-symbol "mo_square_boundary_vblend"  0.5)
(ui-symbol "mo_square_boundary_ublend"  0.5)
(ui-symbol "mo_square_influence_factor1"  1.0)
(ui-symbol "mo_square_influence_factor2"  1.0)
(ui-symbol "mo_square_contin_b1"        #f)
(ui-symbol "mo_square_contin_b2"        #f)
(ui-symbol "mo_square_contin_b3"        #f)
(ui-symbol "mo_square_contin_b4"        #f)
(ui-symbol "mo_square_rebuild_b1"       #f)
(ui-symbol "mo_square_rebuild_b2"       #f)
(ui-symbol "mo_square_rebuild_b3"       #f)
(ui-symbol "mo_square_rebuild_b4"       #f)
(ui-symbol "mo_square_colinear_b1"      #f)
(ui-symbol "mo_square_colinear_b2"      #f)
(ui-symbol "mo_square_colinear_b3"      #f)
(ui-symbol "mo_square_colinear_b4"      #f)
(ui-symbol "mo_square_create_history"   #t)
(ui-symbol "mo_square_xsec_keep"        #f)
(ui-symbol "mo_square_xsec_show_previous" #f)
(ui-symbol "mo_square_xsec_draw_mode"   #f)
(ui-symbol "mo_square_cont_max_iter"    10)
(ui-symbol "mo_square_g1_by_project"    #t)
(ui-symbol "mo_square_g2_enhanced"      #f)
(ui-symbol "mo_square_skews_allowed"    #t)
(ui-symbol "mo_square_surfeval"         0)
(ui-symbol "mo_square_xsec_mode"        0)
(ui-symbol "mo_square_dataredn"         (ui-symbol-reference "MO_SQUARE_DATAREDN_OFF"))
(ui-symbol "mo_square_blend"            (ui-symbol-reference "MO_SQUARE_BLEND_ON"))
(ui-symbol "mo_square_tanscale_u"       1.0)
(ui-symbol "mo_square_tanscale_v"       1.0)
(ui-symbol "mo_square_boundary_labels"  #t)
(ui-symbol "mo_square_explicit_control"  #f)
(ui-symbol "mo_square_srfDegreeU"  3)
(ui-symbol "mo_square_srfDegreeV"  3)
(ui-symbol "mo_square_degreeSync"  #f)
(ui-symbol "mo_square_continuity_check"  #f)
(ui-symbol "mo_square_insert_at_midpoint"  #t)
(ui-symbol "mo_square_explicitSpansU"  1)
(ui-symbol "mo_square_explicitSpansV"  1)
(ui-symbol "mo_square_explicit_max_iter" 0)
(ui-symbol "mo_square_cont_extra_passes" 0)

; n-sided surface default options

(ui-symbol "mo_nsided_blendmode"        (ui-symbol-reference "MO_NSIDED_BLENDMODE_CUBIC"))
(ui-symbol "mo_nsided_num_sides"        (ui-symbol-reference "MO_NSIDED_N_SIDES"))
(ui-symbol "mo_nsided_continuity"       (ui-symbol-reference "MO_NSIDED_CONTINUITY_ON"))
(ui-symbol "mo_nsided_rebuild"          (ui-symbol-reference "MO_NSIDED_REBUILD_ON"))
(ui-symbol "mo_nsided_keeporig"         (ui-symbol-reference "MO_NSIDED_KEEPORIG_ON"))

; holeFiller surface default options

(ui-symbol "mo_holeFiller_continuity"     1)
(ui-symbol "mo_holeFiller_rebuild"        #t)
(ui-symbol "mo_holeFiller_max_new_spans"  10)
(ui-symbol "mo_holeFiller_insert_double"  #t)
(ui-symbol "mo_holeFiller_blend_control"  #f)
(ui-symbol "mo_holeFiller_surface_degree" 3)
(ui-symbol "mo_holeFiller_blend_weight"   5)
(ui-symbol "mo_holeFiller_smooth_weight"  5)
(ui-symbol "mo_holeFiller_cubic_c_on_s"   0)
(ui-symbol "mo_holeFiller_map_closest"    #f)

; Curve network editor options

(ui-symbol "mo_cnet_continuity_type"    (ui-symbol-reference "MO_CNET_CONTINUITY_G0"))

; Tube surface options
(ui-symbol "mo_tube_surface_radius"   10.0)
(ui-symbol "mo_tube_surface_pick_chain" #f)
(ui-symbol "mo_tube_surface_single_span" #f)

; Panel Gap
(ui-symbol "mo_panel_gap_wall_type" 1)
(ui-symbol "mo_panel_gap_wall_uses_primary" #t)
(ui-symbol "mo_panel_gap_flange_angle" 0.0)
(ui-symbol "mo_panel_gap_draft_angle" 0.0)
(ui-symbol "mo_panel_gap_wall_flip" #f)
(ui-symbol "mo_panel_gap_wall_vector_name" "")
(ui-symbol "mo_panel_gap_wall_vector_presets" 2)
(ui-symbol "mo_panel_gap_wall_vector_refresh" 0)
(ui-symbol "mo_panel_gap_wall_vector_save" 0)
(ui-symbol "mo_panel_gap_wall_vector_create" 0)

(ui-symbol "mo_panel_gap_form_factor_version" 2014)
(ui-symbol "mo_panel_gap_primary_section_type" 1 )
(ui-symbol "mo_panel_gap_primary_parameter_type" 1)
(ui-symbol "mo_panel_gap_primary_radius" 1.0)
(ui-symbol "mo_panel_gap_primary_center_radius" 0.5)
(ui-symbol "mo_panel_gap_primary_form_factor" 0.5)

(ui-symbol "mo_panel_gap_primary_extension_type" 0)
(ui-symbol "mo_panel_gap_primary_sweep_angle" 90.0)
(ui-symbol "mo_panel_gap_variable_primary" 0)
(ui-symbol "mo_panel_gap_primary_partline_angle" 0.0)
(ui-symbol "mo_panel_gap_create_primary_flange" #t)
(ui-symbol "mo_panel_gap_primary_extension_distance" 1.0)
(ui-symbol "mo_panel_gap_primary_vector_name" "")
(ui-symbol "mo_panel_gap_primary_vector_presets" 2)
(ui-symbol "mo_panel_gap_primary_vector_refresh" 0)
(ui-symbol "mo_panel_gap_primary_vector_save" 0)
(ui-symbol "mo_panel_gap_primary_vector_create" 0)

(ui-symbol "mo_panel_gap_gap_distance" 0.5)
(ui-symbol "mo_panel_gap_gap_flip" #f)
(ui-symbol "mo_panel_gap_variable_gap" #f)
(ui-symbol "mo_panel_gap_center_gap" #f)

(ui-symbol "mo_panel_gap_secondary_section_type" 1)
(ui-symbol "mo_panel_gap_secondary_parameter_type" 1)
(ui-symbol "mo_panel_gap_secondary_radius" 1.0)
(ui-symbol "mo_panel_gap_secondary_center_radius" 0.5)
(ui-symbol "mo_panel_gap_secondary_form_factor" 0.5)

(ui-symbol "mo_panel_gap_secondary_extension_type" 0)
(ui-symbol "mo_panel_gap_secondary_sweep_angle" 90.0)
(ui-symbol "mo_panel_gap_variable_secondary" 0)
(ui-symbol "mo_panel_gap_secondary_partline_angle" 0.0)
(ui-symbol "mo_panel_gap_create_secondary_flange" #t)
(ui-symbol "mo_panel_gap_secondary_extension_distance" 1.0)
(ui-symbol "mo_panel_gap_secondary_vector_name" "")
(ui-symbol "mo_panel_gap_secondary_vector_presets" 2)
(ui-symbol "mo_panel_gap_secondary_vector_refresh" 0)
(ui-symbol "mo_panel_gap_secondary_vector_save" 0)
(ui-symbol "mo_panel_gap_secondary_vector_create" 0)

(ui-symbol "mo_panel_gap_clip_primary" #f )
(ui-symbol "mo_panel_gap_clip_primary_start" 0.0)
(ui-symbol "mo_panel_gap_clip_primary_end" 1.0)
(ui-symbol "mo_panel_gap_clip_secondary" #f )
(ui-symbol "mo_panel_gap_clip_secondary_start" 0.0)
(ui-symbol "mo_panel_gap_clip_secondary_end" 1.0)

(ui-symbol "mo_panel_gap_gap_check" #f)
(ui-symbol "mo_panel_gap_gap_samples" 50)
(ui-symbol "mo_panel_gap_deviation_scale" 1.0)
(ui-symbol "mo_panel_gap_deviation_threshold" 0.01 )
(ui-symbol "mo_panel_gap_continuity_check" #f)
(ui-symbol "mo_panel_gap_closeout_surface" #f)

(ui-symbol "mo_panel_gap_explicit_control" #f)
(ui-symbol "mo_panel_gap_u_degree" 5)
(ui-symbol "mo_panel_gap_v_degree" 5)
(ui-symbol "mo_panel_gap_max_spans" 100)
(ui-symbol "mo_panel_gap_short_edge_tol" 0.001)

(ui-symbol "mo_panel_gap_surface_type" 1)
(ui-symbol "mo_panel_gap_trim_type"
		(ui-symbol-reference 'MO_FILLET_SRF_TRIM_TYPE_AUTOMATIC))
(ui-symbol "mo_panel_gap_single_span" #f)
(ui-symbol "mo_panel_gap_pick_chain" #f)
(ui-symbol "mo_panel_gap_auto_recalc" #f)
(ui-symbol "mo_panel_gap_debug_geometry" #f)
(ui-symbol "mo_panel_gap_create_type" 0)

; Symmetric Fillet options
(ui-symbol "mo_symmetric_fillet_section_type"
		(ui-symbol-reference 'MO_FILLET_SRF_SECTION_TYPE_G1CIRCULAR))

(ui-symbol "mo_symmetric_fillet_form_factor"			0.5)
(ui-symbol "mo_symmetric_fillet_form_factor_version"	2014)

(ui-symbol "mo_symmetric_fillet_curvature_toggle" 0)
(ui-symbol "mo_symmetric_fillet_explicit_control" #f)
(ui-symbol "mo_symmetric_fillet_u_degree" 5)
(ui-symbol "mo_symmetric_fillet_v_degree" 5)
(ui-symbol "mo_symmetric_fillet_max_num_spans" 100)

(ui-symbol "mo_symmetric_fillet_start_edge_flow" 1)
(ui-symbol "mo_symmetric_fillet_interior_flow" 5)
(ui-symbol "mo_symmetric_fillet_end_edge_flow" 1)
(ui-symbol "mo_symmetric_fillet_clip" #f )
(ui-symbol "mo_symmetric_fillet_clip_start" 0.0)
(ui-symbol "mo_symmetric_fillet_clip_end" 1.0)

(ui-symbol "mo_symmetric_fillet_surface_type"
		(ui-symbol-reference 'MO_FILLET_SRF_MULTIPLE_SURFACES))

(ui-symbol "mo_symmetric_fillet_single_span" #f)
(ui-symbol "mo_symmetric_fillet_short_edge_tol" 0.001)

(ui-symbol "mo_symmetric_fillet_trim_type"
		(ui-symbol-reference 'MO_FILLET_SRF_TRIM_TYPE_AUTOMATIC))

(ui-symbol "mo_symmetric_fillet_flip" #f)
(ui-symbol "mo_symmetric_fillet_curvature_comb" #f)
(ui-symbol "mo_symmetric_fillet_continuity_check" #f)
(ui-symbol "mo_symmetric_fillet_auto_recalc" #f)
(ui-symbol "mo_symmetric_fillet_pick_chain" #f)
(ui-symbol "mo_symmetric_fillet_minimum_radius_check" #f)
(ui-symbol "mo_symmetric_fillet_minimum_radius_samples" 50)

(ui-symbol "mo_symmetric_fillet_debug_geometry" #f)
(ui-symbol "mo_symmetric_fillet_create_history" #t)

; Round Options
(ui-symbol "mo_round_trim_type"         (ui-symbol-reference "MO_ROUND_TRIM_TYPE_AUTO"))

(if (ui-check-option "advancedmodeling_module" )
	(ui-symbol "mo_round_continuity"    #t)
	(ui-symbol "mo_round_continuity"    #f)
)

; angular deviation options

(ui-symbol "mo_angular_dev_spacing_type"		  1)
(ui-symbol "mo_angular_dev_num_per_span"		 20)
(ui-symbol "mo_angular_dev_arc_length"			1.0)
(ui-symbol "mo_angular_dev_show_max_labels"		 #t)
(ui-symbol "mo_angular_dev_show_edge_labels"	 #t)
(ui-symbol "mo_angular_dev_show_comb"			 #t)
(ui-symbol "mo_angular_dev_auto_scale"			 #t)
(ui-symbol "mo_angular_dev_comb_scale"			1.0)
(ui-symbol "mo_angular_dev_chain_select"		 #f)

; measure to plane options

(ui-symbol "mo_measure_to_plane_selection_type"	  7)
(ui-symbol "mo_measure_to_plane_show_min"		 #t)
(ui-symbol "mo_measure_to_plane_show_max"		 #t)
(ui-symbol "mo_measure_to_plane_show_mean"		 #t)
(ui-symbol "mo_measure_to_plane_show_comb"		 #t)

; curve curvature options

(ui-symbol "mo_dispmode"                (ui-symbol-reference "MO_DISPMODE_CONTINUOUS"))
(ui-symbol "mo_windows"                 (ui-symbol-reference "MO_WINDOWS_ALL"))
(ui-symbol "mo_plotvalue"               (ui-symbol-reference "MO_PLOTVAL_CRV"))
(ui-symbol "mo_plotscale"               (ui-symbol-reference "MO_DISP_CRVCURVATURE_DRAW_SCALE"))
(ui-symbol "mo_scaletype"               (ui-symbol-reference "MO_SCALETYPE_LINEAR"))
(ui-symbol "mo_crvdisplay"              (ui-symbol-reference "MO_CRVDISPLAY_COMBLINE"))
; new ones...
(ui-symbol "mo_crvinflection"           #f)
(ui-symbol "mo_crvtorsion"              #f)
(ui-symbol "mo_surfrelative"            #f)
(ui-symbol "mo_enableplot"              #f)
(ui-symbol "mo_crvminmax"               #f)
(ui-symbol "mo_crvcurva_auto_scale"     #t)


(ui-symbol "mo_maxcrvlength"        10000.0)



(ui-symbol "mo_crvcurva_enable_radius_threshold"	#f)
(ui-symbol "mo_crvcurva_min_radius_threshold"	(ui-symbol-reference "MO_CRVCURVA_MIN_RADIUS_THRESHOLD"))
(ui-symbol "mo_crvcurva_max_radius_threshold"	(ui-symbol-reference "MO_CRVCURVA_MAX_RADIUS_THRESHOLD"))

(ui-symbol "mo_crvdenval"               20)
(ui-symbol "mb_curva_arc_length_mode"	#t )
(ui-symbol "mb_curva_u_number"			(ui-symbol-reference "MB_CURVA_U_SAMPLE") )
(ui-symbol "mb_curva_v_number"			(ui-symbol-reference "MB_CURVA_V_SAMPLE") )
(ui-symbol "mb_curva_show_min"			#t)
(ui-symbol "mb_curva_show_max"			#f)
(ui-symbol "mb_curva_show_absolute"		#f)
(ui-symbol "mb_curva_show_scale"		#f)
(ui-symbol "mb_curva_show_scale_x"		#f)
(ui-symbol "mb_curva_show_scale_y"		#f)
(ui-symbol "mb_curva_show_scale_z"		#f)
(ui-symbol "mb_curva_draw_scale"		1.0)
(ui-symbol "mb_curva_draw_scale_x"		1.0)
(ui-symbol "mb_curva_draw_scale_y"		1.0)
(ui-symbol "mb_curva_draw_scale_z"		1.0)
(ui-symbol "mb_curva_ramp_draw_scale"	1.0)
(ui-symbol "mb_curva_rad_or_curva"      0)
(ui-symbol "mb_curva_ramp_use_bands"	#f)



; surface evaluate (cos) options
;
(ui-symbol "mo_surface_cos_eval_type" (ui-symbol-reference "MO_SURFACE_COS_EVAL_TYPE_HIGHLIGHTS"))
(ui-symbol "mo_surface_cos_eval_lightOrigin" 0.0 0.0 10.0)
(ui-symbol "mo_surface_cos_eval_lightDirection" 0.0 0.0 1.0)
(ui-symbol "mo_surface_cos_eval_lightCount" 1)
(ui-symbol "mo_surface_cos_eval_lightSpacing" 10.0)
(ui-symbol "mo_surface_cos_eval_lightWidth" 0.0)
(ui-symbol "mo_surface_cos_eval_curvType" (ui-symbol-reference "AM_CRV_GAUSSIAN"))
(ui-symbol "mo_surface_cos_eval_curvValue" 0.0)
(ui-symbol "mo_diagnosticshade_draft_curve_subdDepth" 6)
(ui-symbol "mo_surface_cos_eval_planeOrigin" 0.0 0.0 0.0)
(ui-symbol "mo_surface_cos_eval_planeNormal" 0.0 0.0 1.0)
(ui-symbol "mo_surface_cos_eval_viewInfinite" (ui-symbol-reference "MO_SURFACE_COS_EVAL_VIEW_PERSPECTIVE"))
(ui-symbol "mo_surface_cos_eval_viewPoint" 0.0 0.0 0.0)
(ui-symbol "mo_surface_cos_eval_viewDirection" 0.0 0.0 1.0)
(ui-symbol "mo_diagnosticshade_draft_vector" 0.0 0.0 1.0)
(ui-symbol "mo_diagnosticshade_draft_angle_pos" 1.0)
(ui-symbol "mo_diagnosticshade_draft_angle_pos_tol" 0.0)
(ui-symbol "mo_diagnosticshade_draft_angle_neg" -1.0)
(ui-symbol "mo_diagnosticshade_draft_angle_neg_tol" 0.0)
(ui-symbol "mo_diagnosticshade_draft_angle_pos_on" #t)
(ui-symbol "mo_diagnosticshade_draft_angle_neg_on" #t)
(ui-symbol "mo_diagnosticshade_draft_curve_zeroLineOn" #t)
(ui-symbol "mo_diagnosticshade_draft_curves_only" #f)
(ui-symbol "mo_surface_cos_eval_autoRecalc" #t)
(ui-symbol "mo_surface_cos_eval_history" #t)
(ui-symbol "mo_surface_cos_eval_visual" #f)
(ui-symbol "mo_surface_cos_eval_pullRotation" 0.0 0.0 0.0 )
(ui-symbol "mo_surface_cos_eval_viewRotation" 0.0 0.0 0.0 )
(ui-symbol "mo_surface_cos_eval_lightRotation" 0.0 0.0 0.0 )
(ui-symbol "mo_surface_cos_eval_planeRotation" 0.0 0.0 0.0 )
(ui-symbol "mo_diagnosticshade_draft_curve_tess_tol" 0.001 )
(ui-symbol "mo_surface_cos_eval_shadeSurfaces" #f)
(ui-symbol "mo_diagnosticshade_draft_curve_type" 0)
(ui-symbol "mo_surface_cos_eval_createCurves" #t)
(ui-symbol "mo_surface_cos_eval_pullAngleLinkValues" #f)
(ui-symbol "mo_surface_cos_eval_vector_name" "")
(ui-symbol "mo_surface_cos_eval_vector_presets" 2)
(ui-symbol "mo_surface_cos_eval_vector_refresh" 0)
(ui-symbol "mo_surface_cos_eval_vector_save" 0)


; curvature rendering options

(ui-symbol "mo_curv_active"             #f)
(ui-symbol "mo_curv_autorange"          #f)
(ui-symbol "mo_cupath.windows.rvdowup"           #f)


; highlight rendering options

(ui-symbol "mo_hl_active"               #f)
(ui-symbol "mo_hl_display"              #t)
(ui-symbol "mo_hl_range_set"            #t)
(ui-symbol "mo_hl_bycolour"             #t)
(ui-symbol "mo_hl_adapt"                1.0)
(ui-symbol "mo_hl_windowup"             #f)


; min-max rendering options

(ui-symbol "mo_mm_active"               #f)
(ui-symbol "mo_mm_curvtype"           (ui-symbol-reference "AM_CRV_PRINCMAX"))
(ui-symbol "ro_pixar_shading"           #t)


; Background   	because these values are tested in the modeling menu
;		before the rendering menu has been initialized.

; (ui-symbol "rp_background"            (ui-symbol-reference "RP_COLOR"))
(ui-symbol "rp_background_str"          "color")

(ui-symbol "ro_background_red"          0)
(ui-symbol "ro_background_green"        0)
(ui-symbol "ro_background_blue"         0)


; added by S.Garrett, Mar.22,1987

(ui-symbol "ro_bg_file_by_frame"        1)
(ui-symbol "ro_bg_file_start_frame"     1)
(ui-symbol "ro_bg_file_end_frame"       1)
(ui-symbol "ro_bg_file_appl"            (ui-symbol-reference "RO_SINGLE"))


; animate options

; (ui-symbol "mo_animate_comptype"      (ui-symbol-reference "MO_COMPALL"))
(ui-symbol "mo_animgrid"                #t)
; (ui-symbol "mo_animplayback"          (ui-symbol-reference "MO_ANIMNATURAL"))
; (ui-symbol "mo_animrangefrom"         (ui-symbol-reference "MO_FROMDOPESHEET"))
(ui-symbol "mo_animstartframe"          1)
(ui-symbol "mo_animendframe"            1)
(ui-symbol "mo_animskipby"              1)


; translation type options

; (ui-symbol "mo_transtype"             (ui-symbol-reference "MO_PARAMCRVS"))


; PATH variables

; (ui-symbol "pthp_settan"              (ui-symbol-reference "PTHP_KEYBRD"))
(ui-symbol "pthp_settan_str"            "keybd")

;(ui-symbol "pthp_display"              (ui-symbol-reference "PTHP_BETWEENS"))
(ui-symbol "pthp_display_str"           "btwns")

;(ui-symbol "pthp_move"                 (ui-symbol-reference "PTHP_CV"))
(ui-symbol "pthp_move_str"              "cv")

;(ui-symbol "pthp_tgllock"              (ui-symbol-reference "PTHP_TANLOCK"))
(ui-symbol "pthp_tgllock_str"           "lock")

;(ui-symbol "pthp_views"                (ui-symbol-reference "PTHP_TUMBLE"))
(ui-symbol "pthp_views_str"             "tumble")

;(ui-symbol "pthp_animate"              (ui-symbol-reference "PTHP_ANIMATEOPTS"))
(ui-symbol "pthp_animate_str"           "do it")

;(ui-symbol "ptho_animate"              (ui-symbol-reference "PTHO_IRIS"))

;(ui-symbol "ptho_animate_comptype"     (ui-symbol-reference "PTHO_COMPALL"))


; PARAM variables

;(ui-symbol "parp_settan"               (ui-symbol-reference "PARP_KEYBRD"))
(ui-symbol "parp_settan_str"            "keybd")

;(ui-symbol "parp_tgllock"              (ui-symbol-reference "PARP_TANLOCK"))
(ui-symbol "parp_tgllock_str"           "lock")

;(ui-symbol "parp_views"                (ui-symbol-reference "PARP_TUMBLE"))
(ui-symbol "parp_views_str"             "tumble")

;(ui-symbol "parp_animate"              (ui-symbol-reference "PARP_ANIMATEOPTS"))
(ui-symbol "parp_animate_str"           "do it")

;(ui-symbol "paro_animate"              (ui-symbol-reference "PARO_IRIS"))

;(ui-symbol "paro_animate_comptype"     (ui-symbol-reference "PARO_COMPALL"))


; TIME variables

(ui-symbol "tp_settan"                  (ui-symbol-reference "TP_KEYBRD"))
(ui-symbol "tp_settan_str"              "keybd")

(ui-symbol "tp_tgllock"                 (ui-symbol-reference "TP_TANLOCK"))
(ui-symbol "tp_tgllock_str"             "lock")

(ui-symbol "tp_display"                 (ui-symbol-reference "TP_BETWEENS"))
(ui-symbol "tp_display_str"             "btwns")

(ui-symbol "tp_views"                   (ui-symbol-reference "TP_TUMBLE"))
(ui-symbol "tp_views_str"               "tumble")

(ui-symbol "tp_animate"                 (ui-symbol-reference "TP_ANIMATEOPTS"))
(ui-symbol "tp_animate_str"             "do it")

; (ui-symbol "to_animate"               (ui-symbol-reference "TO_IRIS"))

; (ui-symbol "to_animate_comptype"      (ui-symbol-reference "TO_COMPALL"))


; Trimming Variable Assignment

(ui-symbol "trp_file"                   (ui-symbol-reference "TRP_RETRIEVE"))
(ui-symbol "trp_file_str"               "retrieve")

(ui-symbol "trp_objtools"               (ui-symbol-reference "TRP_ATTACH"))
(ui-symbol "trp_objtools_str"           "attach")

(ui-symbol "trp_crvtools"               (ui-symbol-reference "TRP_ADDCRV"))
(ui-symbol "trp_crvtools_str"           "add")

(ui-symbol "trp_trim"                   (ui-symbol-reference "TRP_PROJECT"))
(ui-symbol "trp_trim_str"               "project")

(ui-symbol "trp_pick"                   (ui-symbol-reference "TRP_OBJECT"))
(ui-symbol "trp_pick_str"               "object")

(ui-symbol "trp_xform"                  (ui-symbol-reference "TRP_MOVE"))
(ui-symbol "trp_xform_str"              "move")

(ui-symbol "trp_locator"                (ui-symbol-reference "TRP_MOVE_LOCATOR"))
(ui-symbol "trp_locator_str"            "move")

(ui-symbol "trp_delete"                 (ui-symbol-reference "TRP_DELACT"))
(ui-symbol "trp_delete_str"             "del act")

; (ui-symbol "trp_views"                (ui-symbol-reference "TRP_TUMBLE"))
(ui-symbol "trp_views_str"              "tumble")

(ui-symbol "trp_close_trim_level"       0)
(ui-symbol "mp_close_model_level"       0)


; attach options

(ui-symbol "tro_attach_mod_type"        (ui-symbol-reference "TRO_ATTACH"))
(ui-symbol "tro_fillet_bias"            50)
(ui-symbol "tro_seam_weight"            10000)


; detach options

(ui-symbol "tro_detach_break"           #t)
(ui-symbol "tro_detach_break_type"      (ui-symbol-reference "TRO_BREAK_AFTER"))
(ui-symbol "tro_detach_keep"            #f)


; curve options

(ui-symbol "tro_sticky_mode"            #f)
(ui-symbol "tro_beep_mode"              #f)

; untrim surface options

(ui-symbol "mo_untrim_last_stage"       #t)

; divide surface options

(ui-symbol "mo_divide_shrink_surface"   #f)


; trim surface options

(ui-symbol "mo_trim_project_history"    #f)
(ui-symbol "mo_trim_project_use_normal" #f)
(ui-symbol "mo_trim_3d_trim"            #f)
(ui-symbol "mo_trim_3d_trim_type"        1)
(ui-symbol "mo_trim_extend"             #f)
(ui-symbol "mo_trim_extend_type"         1)
(ui-symbol "mo_trim_extend_tol"        0.1)
(ui-symbol "mo_trim_show_diagnostics"   #t)
(ui-symbol "mo_trim_pick_chain"         #f)
(ui-symbol "mo_trim_default_trim_type"   1)
(ui-symbol "mo_trim_selector_u_size"   1.0)
(ui-symbol "mo_trim_selector_v_size"   1.0)
(ui-symbol "mo_trim_vector_name"        "")
(ui-symbol "mo_trim_vector_presets"      3)
(ui-symbol "mo_trim_vector_refresh"      0)
(ui-symbol "mo_trim_vector_save"         0)
(ui-symbol "mo_trim_vector_create"		 0)

; trim convert options

(ui-symbol "mo_trim_convert_3d_trim"       #f)
(ui-symbol "mo_trim_convert_3d_trim_type"   1)
(ui-symbol "mo_trim_convert_extend"        #f)
(ui-symbol "mo_trim_convert_extend_type"    1)
(ui-symbol "mo_trim_convert_extend_tol"   0.1)
(ui-symbol "mo_trim_convert_vector_name"   "")
(ui-symbol "mo_trim_convert_vector_presets" 3)
(ui-symbol "mo_trim_convert_vector_refresh" 0)
(ui-symbol "mo_trim_convert_vector_save"    0)
(ui-symbol "mo_trim_convert_vector_create"	0)
(ui-symbol "mo_trim_convert_uspans"				5)
(ui-symbol "mo_trim_convert_vspans"				5)
(ui-symbol "mo_trim_convert_udegree"			3)
(ui-symbol "mo_trim_convert_vdegree"			3)
(ui-symbol "mo_trim_convert_direction"			0)
(ui-symbol "mo_trim_convert_surface_deviation"	0)
(ui-symbol "mo_trim_convert_edge_deviations"	0)
(ui-symbol "mo_trim_convert_keep_originals"		1)
(ui-symbol "mo_trim_convert_auto_recalc"		0)
(ui-symbol "mo_trim_convert_show_diagnostics" #t)
(ui-symbol "mo_trim_convert_selector_u_size" 1.0)
(ui-symbol "mo_trim_convert_selector_v_size" 1.0)


; fit scan options

(ui-symbol "mo_fit_scan_uspans"					1)
(ui-symbol "mo_fit_scan_vspans"					1)
(ui-symbol "mo_fit_scan_udegree"				5)
(ui-symbol "mo_fit_scan_vdegree"				5)
(ui-symbol "mo_fit_scan_smoothness"				0.0)
(ui-symbol "mo_fit_scan_keep_originals"			1)
(ui-symbol "mo_fit_scan_deviations"				0)
(ui-symbol "mo_fit_scan_auto_recalc"			0)
(ui-symbol "mo_fit_scan_direction"				4)
(ui-symbol "mo_fit_scan_proximity"				0.0)

; construction history offset options

(ui-symbol "mo_ch_offset_curve_break"			1)
(ui-symbol "mo_ch_offset_plane"					1)
(ui-symbol "mo_ch_offset_curve_loop_cutting"	#t)
(ui-symbol "mo_ch_offset_offset_autorecalc"		#t)
(ui-symbol "mo_ch_offset_offset_history"		#t)
(ui-symbol "mo_ch_offset_offset_control"		#t)
(ui-symbol "mo_ch_offset_offset_copy_cos"		#t)
(ui-symbol "mo_ch_offset_distance"				1.0)
(ui-symbol "mo_ch_offset_curve_cutting_radius"	0.0)
(ui-symbol "mo_ch_offset_max_spans_factor"		1.0)
(ui-symbol "mo_ch_offset_normal_mode"			0)

; project options

(ui-symbol "tro_proj_projv"             (ui-symbol-reference "TRO_PROJ_PROJV_ACTIVE"))
(ui-symbol "tro_proj_create_trim_history" #t)
(ui-symbol "tro_closest_checkpoints"    1)

; project_and_trim options
(ui-symbol "mo_proj_trim_mode"				 1)
(ui-symbol "mo_proj_trim_enabled"			#f)
(ui-symbol "mo_proj_trim_create"			 1)
(ui-symbol "mo_proj_trim_match_original"	#t)

(ui-symbol "mo_proj_explicit_control" 1)
(ui-symbol "mo_proj_exp_degree" 3)
(ui-symbol "mo_proj_exp_spans" 1)

(ui-symbol "mo_proj_vector_name" "")
(ui-symbol "mo_proj_vector_presets" 3)
(ui-symbol "mo_proj_vector_refresh" 0)
(ui-symbol "mo_proj_vector_save" 0)
(ui-symbol "mo_proj_vector_create" 0)

; intersect options

(ui-symbol "tro_isect_create_cos"       (ui-symbol-reference "TRO_ISECT_CREATE_COS_BOTH"))
(ui-symbol "tro_isect_create_trim_history" #t)

; tubular offset options

(ui-symbol "mo_tubular_offset_trim_type"		(ui-symbol-reference "MO_FILLET_SRF_TRIM_TYPE_CURVES_ON_SURFACE"))
(ui-symbol "mo_tubular_offset_surface"		(ui-symbol-reference "MO_TUBULAR_OFFSET_SURFACE_TUBE"))
(ui-symbol "mo_tubular_offset_surface_type"		1)
(ui-symbol "mo_tubular_offset_single_span"		#f)
(ui-symbol "mo_tubular_offset_span_placement"	1)
(ui-symbol "mo_tubular_offset_h_offset"		   0.0)
(ui-symbol "mo_tubular_offset_v_offset"		   0.0)
(ui-symbol "mo_tubular_offset_flip"				#f)
(ui-symbol "mo_tubular_offset_auto_recalc"		#f)
(ui-symbol "mo_tubular_offset_radius"		  10.0)
(ui-symbol "mo_tubular_offset_pick_chain"		#f)

; uvmapping options

(ui-symbol "tro_uvmap_uaxis"            0)
(ui-symbol "tro_uvmap_vaxis"            1)
(ui-symbol "tro_uvmap_umin"             0.0)
(ui-symbol "tro_uvmap_umax"             1.0)
(ui-symbol "tro_uvmap_vmin"             0.0)
(ui-symbol "tro_uvmap_vmax"             1.0)
(ui-symbol "tro_uvmap_divisions"        10)
(ui-symbol "tro_uvmap_type"             (ui-symbol-reference "TRO_UVMAP_PARAM"))
(ui-symbol "tro_uvmap_create_trim_history" #t)


;
; Shell stuff
;

(ui-symbol "sh_stitch_keep_orig"        #t)
(ui-symbol "sh_unstitch_keep_orig"      #f)
(ui-symbol "sh_intersect_keep_orig"     #t)
(ui-symbol "sh_union_keep_orig"         #t)
(ui-symbol "sh_subtract_keep_orig"      #t)

(ui-symbol "sh_intersect_shrink"     #f)
(ui-symbol "sh_union_shrink"         #f)
(ui-symbol "sh_subtract_shrink"      #f)

(ui-symbol "sh_stitch_detach_single_crv_bnd" #t)
(ui-symbol "sh_stitch_detach_periodic_srfs" #t)

; V14 stitch
(ui-symbol "mo_stitch_use_constropts" #t)
(ui-symbol "mo_stitch_tolerance" 0.02)
(ui-symbol "mo_stitch_keep_originals" #t)
(ui-symbol "mo_stitch_unify_normals" #f)
(ui-symbol "mo_stitch_detach_single_curves" #t)
(ui-symbol "mo_stitch_detach_periodics" #t)

; pivot options

(ui-symbol "tro_rot_pivot"              #t)
(ui-symbol "tro_scale_pivot"            #t)


; proportional modification options

(ui-symbol "tro_pmod_type"              (ui-symbol-reference "TRO_BOW"))
(ui-symbol "tro_pmod_udegree"           100)
(ui-symbol "tro_pmod_vdegree"           100)
(ui-symbol "tro_pmod_uprec"             0)
(ui-symbol "tro_pmod_vprec"             0)
(ui-symbol "tro_pmod_usucc"             0)
(ui-symbol "tro_pmod_vsucc"             0)


; Variables used by new popup initialization function:

(ui-symbol "popup_l"                    0)
(ui-symbol "popup_r"                    0)
(ui-symbol "popup_b"                    0)
(ui-symbol "popup_t"                    0)
(ui-symbol "n_popups"                   0)
(ui-symbol "wider_popups"               0)
(ui-symbol "cell_offset"                0)
(ui-symbol "option_boxes"               0)


; Menu customization stuff:

(ui-symbol "custom_command"             "")


; SCP creation options

(ui-symbol "mo_scpcreate_axis"          (ui-symbol-reference "MO_SCPCREATE_X"))
(ui-symbol "mo_scp_asymm_option"        (ui-symbol-reference "MO_SCP_ASYMM_DELETE"))
(ui-symbol "mo_tmp_scp_asymm_option"    (ui-symbol-reference "MO_SCP_ASYMM_DELETE"))
(ui-symbol "mo_tgl_scp_option"          (ui-symbol-reference "MO_TGL_SCP_INSTANCE"))
(ui-symbol "mo_tmp_tgl_scp_option"      (ui-symbol-reference "MO_TGL_SCP_INSTANCE"))


; File Browser menu defaults

(ui-symbol "lister_display_mode"        4)
(ui-symbol "lister_sort_mode"           1)


; Store and Retreive Filters

(ui-symbol "mo_filter_scope"            1)
(ui-symbol "mo_filter_do_input"         1)
(ui-symbol "mo_filter_do_output"        1)
(ui-symbol "mo_filter_replace"          1)
(ui-symbol "mo_filter_import_suffix"    "")
(ui-symbol "mo_filter_export_method"    "")

(ui-symbol "mo_appl_do_input"           #t)
(ui-symbol "mo_appl_input_scope"        (ui-symbol-reference "MO_PICKED_OBJECTS"))
(ui-symbol "mo_appl_input_file"         "mo_appl_input_file")

(ui-symbol "mo_appl_do_output"          #t)
(ui-symbol "mo_appl_replace_scope"      (ui-symbol-reference "MO_PICKED_OBJECTS"))
(ui-symbol "mo_appl_replace"            #t)
(ui-symbol "mo_appl_output_file"        "mo_appl_output_file")

(ui-symbol "mo_appl_name"               "")


; Update Status options

(ui-symbol "mo_draw_trim_boundaries" #t)
(ui-symbol "mo_draw_trim_boundaries_in_playback" #f)

(ui-symbol "mo_auto_redraw_precision_static" 0)
(ui-symbol "mo_auto_redraw_precision_motion" 0)
(ui-symbol "mo_auto_redraw_precision_update" 0)

(ui-symbol "mo_update_evaluate_expr"    #t)
(ui-symbol "mo_update_evaluate_expr_xform" #f)
(ui-symbol "mo_update_evaluate_expr_playback" #t)
(ui-symbol "mo_update_evaluate_constraint" #t)
(ui-symbol "mo_update_evaluate_constraint_xform" #t)
(ui-symbol "mo_update_evaluate_constraint_playback" #t)
(ui-symbol "mo_update_evaluate_ik" #t)
(ui-symbol "mo_update_evaluate_ik_xform" #t)
(ui-symbol "mo_update_evaluate_ik_postwritesdl" #f)
(ui-symbol "mo_update_evaluate_ik_playback" #t)
(ui-symbol "mo_update_evaluate_constHist" #t)
(ui-symbol "mo_update_evaluate_constHist_xform" #f)
(ui-symbol "mo_update_evaluate_blend_crv_xform" #t)
(ui-symbol "mo_update_evaluate_constHist_playback" #f)
(ui-symbol "mo_update_evaluate_blend_playback" #t)
(ui-symbol "mo_update_evaluate_constHist_round_auto" #f)
(ui-symbol "mo_update_evaluate_displayables" #t)
(ui-symbol "mo_update_evaluate_displayables_xform" #t)
(ui-symbol "mo_update_evaluate_displayables_playback" #t)
(ui-symbol "mo_update_evaluate_actionWindow" #f)
(ui-symbol "mo_update_evaluate_actionWindow_xform" #f)
(ui-symbol "mo_update_evaluate_cluster"    #t)
(ui-symbol "mo_update_evaluate_cluster_xform" #t)
(ui-symbol "mo_update_evaluate_cluster_playback" #t)
(ui-symbol "mo_evaluations_per_update" 1)

(ui-symbol "sm_device_avail"       #f)
;
;; Point cloud options
;
; Cloud retrieve options
(ui-symbol "cd_retrieveNthPts"                          1)
;
; Cloud display options
(ui-symbol "cd_cloud_display_scope"                  0)
(ui-symbol "cd_cloud_display_visible"               #t)
(ui-symbol "cd_cloud_display_still_coarseness"       1)
(ui-symbol "cd_cloud_display_moving_coarseness"      1)

(ui-symbol "cd_cloud_display_polys"                  0)
(ui-symbol "cd_cloud_display_lats"                   0)
(ui-symbol "cd_cloud_display_longs"                  0)
(ui-symbol "cd_cloud_display_latRes"                10)
(ui-symbol "cd_cloud_display_longRes"               10)
(ui-symbol "cd_cloud_display_latMin"                 1)
(ui-symbol "cd_cloud_display_latMax"                 600)
(ui-symbol "cd_cloud_display_longMin"                1)
(ui-symbol "cd_cloud_display_longMax"                600)

(ui-symbol "cd_cloud_display_style"                  0)
(ui-symbol "cd_cloud_display_pt_size"                1)

; Cloud subset options
(ui-symbol "cd_cloud_subset_keep_part"                0)

; Cloud quick surface options
(ui-symbol "cd_surf_numRefines"              3)
(ui-symbol "cd_surf_UGridSpans"              3)
(ui-symbol "cd_surf_VGridSpans"              3)
(ui-symbol "cd_surf_resSurfUdegree"          3)
(ui-symbol "cd_surf_resSurfVdegree"          3)
(ui-symbol "cd_surf_resSurfUSpans"           2)
(ui-symbol "cd_surf_resSurfVSpans"           2)
(ui-symbol "cd_surf_displayRefinementsAs"    0)
(ui-symbol "cd_surf_continuity"              0)
(ui-symbol "cd_surf_dataType"                0)
(ui-symbol "cd_surf_radius"                1.0)

(ui-symbol "cd_surfCreate_tolerance"      0.01)
(ui-symbol "cd_surfCreate_trimmedSurf"      #f)
(ui-symbol "cd_surfCreate_continuity"        0)
(ui-symbol "cd_surfCreate_gfactor"          80)

; Cloud surface creation from corners options
(ui-symbol "cd_surfCorner_tolerance"      0.10)
(ui-symbol "cd_surfCorner_gfactor"          30)

; Cloud crv projection options
(ui-symbol "cd_crvProjectVectorSrc"          0)
(ui-symbol "cd_crvProjectHist"              #t)
(ui-symbol "cd_crvProjectKeepSpans"          1)
(ui-symbol "cd_crvProjectProjMethod"         0)
(ui-symbol "cd_crvProjectMaxIterations"     10)
(ui-symbol "cd_crvProjectProjDirection"      0)

;; layers options

(ui-symbol "ly_current_start_layer"	      1)
(ui-symbol	"ly_merge_mode"			      0)
(ui-symbol	"mo_paste_in_layer"			  0)
(ui-symbol	"mo_paste_layer_name"	      "")
(ui-symbol	"mo_paste_layer_number"	      0)
(ui-symbol	"mo_paste_by_name_or_number"  1)
(ui-symbol	"mo_paste_in_categories"      #t)
(ui-symbol "ly_default_symm_plane_origin_x" 0.0)
(ui-symbol "ly_default_symm_plane_origin_y" 0.0)
(ui-symbol "ly_default_symm_plane_origin_z" 0.0)

(ui-symbol "ly_default_symm_plane_normal_x" 0.0)
(ui-symbol "ly_default_symm_plane_normal_y" 1.0)
(ui-symbol "ly_default_symm_plane_normal_z" 0.0)
(ui-symbol "ly_layers_enabled" #t)

;; random layer options
(ui-symbol "ly_random_include_folders"	      #f)

; variables used by the draft evaluation tool
; may or may not eventually end up in an option box
(ui-symbol  "mo_diagnosticshade_draft_rotation"		0.0 0.0 0.0)
(ui-symbol "mo_disp_draftprop_usampsperspan"  3)
(ui-symbol "mo_disp_draftprop_vsampsperspan"  3)
(ui-symbol "mo_disp_draftprop_ucutlength"  0.0)
(ui-symbol "mo_disp_draftprop_dirvec" 0) ; direction vector or rotation angles?
(ui-symbol "mo_disp_draftprop_parting_line" 1) ; compute the parting line, too ?
(ui-symbol "mo_disp_draftprop_tesselation" 0) ; use the tesselation version?

;; al_displayable window draw mode
(ui-symbol "al_disp_window_draw_mode"	(ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "al_disp_dist_proj_or_true"		1)
(ui-symbol "al_disp_angle_proj_or_true"		1)
(ui-symbol "al_disp_dist_show_prefix"		#f)
(ui-symbol "al_disp_angle_show_prefix"		#f)
(ui-symbol "al_disp_minmax_proj_or_true"		1)

;; minmax meshsrf deviation options
(ui-symbol "mo_deviation_meshsrf_show_min" #t)
(ui-symbol "mo_deviation_meshsrf_show_max" #t)
(ui-symbol "mo_deviation_meshsrf_show_comb" #t)
(ui-symbol "mo_deviation_crvcrv_show_min" #t)
(ui-symbol "mo_deviation_crvcrv_show_max" #t)
(ui-symbol "mo_deviation_crvcrv_show_mean" #f)
(ui-symbol "mo_deviation_crvcrv_show_comb" #t)
(ui-symbol "mo_deviation_crvsrf_show_min" #t)
(ui-symbol "mo_deviation_crvsrf_show_max" #t)
(ui-symbol "mo_deviation_crvsrf_show_mean" #f)
(ui-symbol "mo_deviation_crvsrf_show_comb" #t)
(ui-symbol "mo_deviation_srfsrf_show_min" #t)
(ui-symbol "mo_deviation_srfsrf_show_max" #t)
(ui-symbol "mo_deviation_srfsrf_show_mean" #f)
(ui-symbol "mo_deviation_srfsrf_show_comb" #t)

(ui-symbol "mo_disp_plane_create_num"		0)

; variables used by the draft evaluation tool
; may or may not eventually end up in an option box
(ui-symbol "mo_disp_curveprop_type"  1)
(ui-symbol "mo_disp_curveprop_abs"   0)
(ui-symbol "mo_disp_curveprop_lothresh" -0.5)  ; colouring boundary
(ui-symbol "mo_disp_curveprop_hithresh"  0.5)  ; degrees
(ui-symbol "mo_disp_curveprop_usampsperspan"  3)
(ui-symbol "mo_disp_curveprop_vsampsperspan"  3)
(ui-symbol "mo_disp_curveprop_scale"  1.0)



; combine surface needs a set of tolerances, etc..
(ui-symbol "mo_combine_surfaces_tolerance" 0.01)
(ui-symbol "mo_combine_surfaces_angle_tolerance" 0.0)
(ui-symbol "mo_combine_surfaces_iterate"  #f)
(ui-symbol "mo_combine_surfaces_deg" 3)
(ui-symbol "mo_combine_surfaces_udeg" 3)
(ui-symbol "mo_combine_surfaces_vdeg" 3)
(ui-symbol "mo_combine_surfaces_uspans" 3)
(ui-symbol "mo_combine_surfaces_vspans" 3)

(ui-symbol "mo_tess_default_max_subdiv" 8)

(ui-symbol  "mb_refl_dev_min"	#t )
(ui-symbol  "mb_refl_dev_mean"	#t )
(ui-symbol  "mb_refl_dev_max"	#t )
(ui-symbol  "mb_refl_dev_draw_scale"	1.0 )
(ui-symbol  "mb_dev_precision"	4 )
(ui-symbol  "mb_refl_dev_threshold"	0.1 )
(ui-symbol  "mb_refl_dev_min_threshold"	(ui-symbol-reference "MB_REFL_DEV_MIN_THRESHOLD"))
(ui-symbol  "mb_refl_dev_max_threshold"	(ui-symbol-reference "MB_REFL_DEV_MAX_THRESHOLD"))


(ui-symbol  "mo_dyn_xsec_number"        0)
(ui-symbol  "mo_dyn_xsec_step"          1.0)
(ui-symbol  "mo_dyn_xsec_curva_draw_scale"     1.0)
(ui-symbol  "mo_dyn_xsec_curva_sample_count"   50)
(ui-symbol  "mo_dyn_xsec_history"		#f)
(ui-symbol  "mo_dyn_xsec_visual_clip"   #f)
(ui-symbol  "mo_dyn_xsec_visual_clip_history"   #f)
(ui-symbol  "mo_dyn_xsec_visual_flip"   #f)
(ui-symbol  "mo_dyn_xsec_translate"		0.0 0.0 0.0)
(ui-symbol  "mo_dyn_xsec_rotate"		0.0 0.0 0.0)
(ui-symbol  "mo_dyn_xsec_use_clip_offset"  #f)
(ui-symbol  "mo_dyn_xsec_clip_offset"   10.0)

; Need to have global variable to save the last VRML2 export directory
(ui-symbol "mvrml2.expdir" "" )

(ui-symbol "pickfunc_name" "Object" )

(ui-symbol "mo_sbd_showinvisible" #t )

(ui-symbol "mo_isoangle_curves_only"		#f)
(ui-symbol "mo_isoangle_steps"		2)
(ui-symbol "mo_isoangle_width"		4.0)
(ui-symbol "mo_isoangle_decay"		'MO_ISOANGLE_DEFAULT_SHARPNESS)
(ui-symbol "mo_isoangle_angle"		90.0)
(ui-symbol "mo_isoangle_texture"	(ui-symbol-reference "MO_TEXTURE_ISOANGLE_BW"))
(ui-symbol "mo_isoangle_rotation"	0.0)
(ui-symbol "mo_isoangle_relax"		0.0)
(ui-symbol "mo_isoangle_mode"		0)
(ui-symbol "mo_isoangle_cos_type"		1)
(ui-symbol "mo_isoangle_vec"		0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_isoangle_history"		#t)

(ui-symbol "tf_val1"		0)
(ui-symbol "tf_val2"		2)

(ui-symbol "tMf_val1"		0)
(ui-symbol "tMf_val2"		2)

; deviation table options
(ui-symbol "tf_Output_Str"              "Printing.....")

(ui-symbol "mo_devtable_C0BandStart"     0.0)
(ui-symbol "mo_devtable_C0BandEnd"       1.0e15)
(ui-symbol "mo_devtable_G1BandStart"     0.0)
(ui-symbol "mo_devtable_G1BandEnd"       90.0)
(ui-symbol "mo_devtable_G2BandStart"     0.0)
(ui-symbol "mo_devtable_G2BandEnd"       1.0)

(ui-symbol "defctrl.fromPnt"	0.0 0.0 0.0 )
(ui-symbol "defctrl.toPnt"		0.0 0.0 0.0 )
(ui-symbol "defctrl.dist"		0.0 )
(ui-symbol "defctrl.toU"		0.0 )
(ui-symbol "defctrl.toV"		0.0 )
(ui-symbol "defctrl.FromU"		0.0 )
(ui-symbol "defctrl.FromV"		0.0 )
(ui-symbol "defctrl.extents"	0.0 0.0 0.0 )
(ui-symbol "defctrl.rotation"	0.0 0.0 0.0 )
(ui-symbol "defctrl.fillBox"	#f )
(ui-symbol "defctrl.undodepth"	10 )

; Reset View options

(ui-symbol "mo_reset_view_function" "ResetView")
(ui-symbol "mo_reset_type"		(ui-symbol-reference "MO_RESETVIEW_DEFAULT"))

; new round (round engine)

;; use tighter approximation or not...
(ui-symbol "mo_re_uti"	#t )
(ui-symbol "mo_re_history"	#t )

; direction mode
(ui-symbol "show_direction_mode"	0 )
; Diagnostic Draft but MUST match show_direction_mode above
(ui-symbol "mo_diagnosticshade_draft_disp_vec_or_rot"		0 )

(ui-symbol "mo_sweepsfloat"	0.7 )
(ui-symbol "mo_sweepschoice"	1 )
(ui-symbol "mo_sweepsSiteChoice"	1 )
(ui-symbol "mo_sweepsbool"	1 )
(ui-symbol "mo_sweepsShowNames"	1 )
(ui-symbol "mo_sweepsRGB"	150.0 150.0 150.0 )

; object editor options
(ui-symbol "objecteditor.endpoints" 0)
(ui-symbol "objecteditor.create_history" #f)
	(ui-symbol "objecteditor.simple_mode"	#f)
(ui-symbol "curveeditor.modification_mode" 2)

; model check options
(ui-symbol "mcheck_iActiveGeom" 2)
(ui-symbol "mcheck_iReportAll" 1)
(ui-symbol "mcheck_iMultiknot" 1)
(ui-symbol "mcheck_iPeriodicity" 0)
(ui-symbol "mcheck_iShortEdge" 1)
(ui-symbol "mcheck_iRational" 0)
(ui-symbol "mcheck_iDegree" 0)
(ui-symbol "mcheck_iMultiTrim" 0)
(ui-symbol "mcheck_iMultiSpans" 0)
(ui-symbol "mcheck_iTangentDiscont" 1)
(ui-symbol "mcheck_fShortEdgeTol" 0.01)
(ui-symbol "mcheck_iDegreeAbove" 7)
(ui-symbol "mcheck_iCheckGeomType" 2)
(ui-symbol "mcheck_fMultiknotTol" 0.000001)
(ui-symbol "mcheck_iIdentical" 1)
(ui-symbol "mcheck_fIdenticalTol" 0.01)
(ui-symbol "mcheck_iCG0" 0)
(ui-symbol "mcheck_iCG1" 0)
(ui-symbol "mcheck_iCG2" 0)
(ui-symbol "mcheck_fCGOTol" 0.01)
(ui-symbol "mcheck_fCG1Tol" 0.1)
(ui-symbol "mcheck_fCG2Tol" 0.1)
(ui-symbol "mcheck_iNormalConsistency" 0)
(ui-symbol "mcheck_iVisualNormalConsistency" 0)
(ui-symbol "mcheck_iGeometricNormalConsistency" 0)
(ui-symbol "mcheck_fTopCGOTol" 0.1)
(ui-symbol "mcheck_fTopCG1Tol" 30.0)
(ui-symbol "mcheck_fTopCG2Tol" 1.0)
(ui-symbol "mcheck_iUseConstructionOptionTolerances" 1)
(ui-symbol "mcheck_iUseVDAG2" 0)
(ui-symbol "mcheck_fCG2TolVDA" 0.1)
(ui-symbol "mcheck_iMinCurvatureR" 0)
(ui-symbol "mcheck_fMinCurvatureR" 0.01)
(ui-symbol "mcheck_iWaviness" 0)
(ui-symbol "mcheck_iWavinessDoPerSpan" 1)
(ui-symbol "mcheck_iWavyAllowedPerSpan" 1)
(ui-symbol "mcheck_iWavyAllowedPerBs" 3)
(ui-symbol "mcheck_iNonPlanarCurve" 0)
(ui-symbol "mcheck_iSelfIntersection" 0)
(ui-symbol "mcheck_iIntersectingLoops" 0)
(ui-symbol "mcheck_iMinKnotSeparation" 0)
(ui-symbol "mcheck_iMinSegmentLength" 0)
(ui-symbol "mcheck_iMultiSpansAllowed" 200)
(ui-symbol "mcheck_iMinKnotSeparationExponent" -6)
(ui-symbol "mcheck_fMinSegmentLengthTol" 0.005)
(ui-symbol "mcheck_fIntersectionTol" 0.001)
(ui-symbol "mcheck_findDuplicates"    #t )
(ui-symbol "mcheck_iToleranceSet" -1)
(ui-symbol "mcheck_sToleranceSetName" "")

(ui-symbol "mcheck_f" 1.0)
(ui-symbol "mcheck_tick"    #t )
(ui-symbol "mcheck_int2" 1)
(ui-symbol "mcheck_float2" 1.0)
(ui-symbol "mcheck_tick2"    #t )

(ui-symbol "mcheck_int3" 1)
(ui-symbol "mcheck_float3" 1.0)
(ui-symbol "mcheck_tick3"    #t )


(ui-symbol "sweepsTabPage" "stdPage" )
(ui-symbol "interface_options_TabPage" "interface" )

(ui-symbol "view_bookmark_id" "" )
(ui-symbol "view_bookmark_cycle_time" 2) ; time in seconds
(ui-symbol "view_bookmark_cycle_loopforever" #f) ;
(ui-symbol "view_bookmark_new_visibility" #f) ;
(ui-symbol "view_bookmark_useOnlyCameraMode" #f)

; help menu web links

(ui-symbol "help_report_bug" "http://www.alias.com/cgi-bin/bug_forms/beta/product.cgi?product=StudioTools")
(ui-symbol "help_homepage" "http://www.alias.com/tryalias" )
(ui-symbol "help_resource_center" "http://www.alias.com/community/studio")
(ui-symbol "help_support" "http://www.autodesk.com/aliasstudio-support")

(ui-symbol "help_community" "http://www.alias.com/studiotools/")
(ui-symbol "help_store" "http://www.alias.com/store/")
(ui-symbol "help_tutorials" "")

(ui-symbol "help_report_problem" "http://www.alias.com/studio/bug")
(ui-symbol "help_suggest_feature" "http://www.alias.com/studio/sug")
(ui-symbol "help_try_other_products" "http://www.alias.com/tryalias")

; Mesh Control Panel
(ui-symbol "mo_mesh_quality"	1.0)
(ui-symbol "mo_mesh_density"	1.0)
(ui-symbol "mo_mesh_transparency"	0.0)
(ui-symbol "mo_draw_precision"  0.5)
(ui-symbol "mb_mesh_flat_shaded" 0 )

; MeshFromCloud variables
(ui-symbol "mo_cloudToMesh_estimate" #f)
(ui-symbol "mo_cloudToMesh_estimate_switch" #f)
(ui-symbol "mo_cloudToMesh_vertex_tolerance" 0.0)
(ui-symbol "mo_cloudToMesh_grouping_tolerance" 0.2)
(ui-symbol "mo_cloudToMesh_unify_normals" #t)
(ui-symbol "mo_cloudToMesh_limit_edge_length" #f)
(ui-symbol "mo_cloudToMesh_max_edge_length" .5)
(ui-symbol "mo_cloudToMesh_max_hole_edges" 30)

; MeshFromNurbs variables
(ui-symbol "mo_nurbsToMesh_tess_type" (ui-symbol-reference "MO_TGLSHADE_ARUBA_TESSELATOR"))
(ui-symbol "mo_nurbsToMesh_use_existing" #f)
(ui-symbol "mo_nurbsToMesh_tolerance" 0.1)
(ui-symbol "mo_nurbsToMesh_tessellate_shells" #t)
(ui-symbol "mo_nurbsToMesh_merge_vertices" #t)
(ui-symbol "mo_nurbsToMesh_limit_edge_length" #t)
(ui-symbol "mo_nurbsToMesh_max_edge_length" 5.0)

; MeshFromDispMap variables
(ui-symbol "mo_dispMapToMesh_tolerance" 0.05)
(ui-symbol "mo_dispMapToMesh_dispdetail" 40)
(ui-symbol "mo_dispMapToMesh_use_existing" #f)

; MeshSubset variables
(ui-symbol "mo_meshSubset_selectionMode" 0)
(ui-symbol "mo_meshSubset_invisible" #f)
(ui-symbol "mo_meshSubset_frontSelectionMode" #t)
(ui-symbol "mo_meshSubset_normalAngle" 3.0)
(ui-symbol "mo_meshSubset_pickRadius" 25)

; Mesh offset variables
(ui-symbol "mo_meshOffset_distance" 1.0)
(ui-symbol "mo_meshOffset_outputType" 0)

; Mesh cut variables
(ui-symbol "mo_mesh_cut_intersect_history" #t)

; Mesh Collar variables
(ui-symbol "mo_mesh_collar_width" 2.5)
(ui-symbol "mo_mesh_collar_spans" 1)
(ui-symbol "mo_mesh_collar_periodic" #f)
(ui-symbol "mo_mesh_collar_create_history" #t)
(ui-symbol "mo_mesh_collar_show_surface_deviation" #f)
(ui-symbol "mo_mesh_collar_show_deviation_map" #f)
(ui-symbol "mo_mesh_collar_devmap_autoramp" #f)


; Mesh Repair variables
(ui-symbol "mo_mesh_repair_show_problems" #t)
(ui-symbol "mo_mesh_repair_check_intersect" #f)
(ui-symbol "mo_mesh_repair_check_angles" #f)
(ui-symbol "mo_mesh_repair_arrow_boundaries" #f)

; Mesh Stitch variables
(ui-symbol "mo_mesh_stitch_tolerance" 0.05)

; Mesh Hole Fill variables
(ui-symbol "mo_mesh_holefill_quality" 2)
(ui-symbol "mo_mesh_holefill_maxholesize" 150)

; Mesh Reduce variables
(ui-symbol "mo_mesh_reduce_percentage" 75)
(ui-symbol "mo_mesh_reduce_mode" 2)
(ui-symbol "mo_mesh_reduce_max_deviation" 0.005)
(ui-symbol "mo_mesh_reduce_show_deviation_map" #f )
(ui-symbol "mo_mesh_reduce_devmap_autoramp" #t )

; Mesh Smooth variables
(ui-symbol "mo_mesh_smooth_preserve_features" #t)
(ui-symbol "mo_mesh_smooth_number_iterations" 4)
(ui-symbol "mo_mesh_smooth_fix_boundary_vertices" #t)
(ui-symbol "mo_mesh_smooth_use_maxdeviation" #f)
(ui-symbol "mo_mesh_smooth_maxdeviation" 1.0)
(ui-symbol "mo_mesh_smooth_radius" 0.5)
(ui-symbol "mo_mesh_smooth_show_deviation_map" #f )
(ui-symbol "mo_mesh_smooth_devmap_autoramp" #t )
(ui-symbol "mo_mesh_smooth_selection_mode" 0 )
(ui-symbol "mo_mesh_smooth_normal_angle" 3.0 )
(ui-symbol "mo_mesh_smooth_pick_radius" 25)

; Mesh Flatten options
(ui-symbol "mo_mesh_flatten_keep_orig"    #t )
(ui-symbol "mo_mesh_flatten_plane"        0  )
(ui-symbol "mo_mesh_flatten_flip_x"       #t )
(ui-symbol "mo_mesh_flatten_flip_y"       #f )
(ui-symbol "mo_mesh_flatten_swap"         #t )

; Mesh Theoretical options
(ui-symbol "mo_mesh_theoretical_radius" 2.0 )
(ui-symbol "mo_mesh_theoretical_samples" 20 )
(ui-symbol "mo_mesh_cross_curve_fit" #t )
(ui-symbol "mo_mesh_cross_curve_degree" 3 )
(ui-symbol "mo_mesh_cross_curve_spans" 1 )
(ui-symbol "mo_mesh_cross_curve_output" #f )
(ui-symbol "mo_mesh_cross_curve_distance" 1.0 )
(ui-symbol "mo_mesh_theo_sampling_factor" 0.5 )
(ui-symbol "mo_mesh_theo_curve_rebuild" #f )
(ui-symbol "mo_mesh_theo_curve_degree" 5 )
(ui-symbol "mo_mesh_theo_curve_spans" 2 )
(ui-symbol "mo_mesh_theo_create_theoreticalCurve" #t )
(ui-symbol "mo_mesh_theo_create_featureCurve" #t )
(ui-symbol "mo_mesh_theo_show_featureHelper" #t )
(ui-symbol "mo_mesh_theo_auto_recalc" #f )
(ui-symbol "mo_mesh_theo_show_curvature_map" #t )

; Mesh Sharpen options
(ui-symbol "mo_mesh_sharpen_radius" 1.0 )
(ui-symbol "mo_mesh_sharpen_samples" 20 )
(ui-symbol "mo_mesh_sharpen_cross_curve_distance" 0.5 )
(ui-symbol "mo_mesh_sharpen_sampling_factor" 0.5 )
(ui-symbol "mo_mesh_sharpen_theo_curve_rebuild" #t )
(ui-symbol "mo_mesh_sharpen_theo_curve_degree" 5 )
(ui-symbol "mo_mesh_sharpen_theo_curve_spans" 2 )
(ui-symbol "mo_mesh_sharpen_output_surfaces" #f )
(ui-symbol "mo_mesh_fillet_on" #f )
(ui-symbol "mo_mesh_fillet_type" 0 )
(ui-symbol "mo_mesh_fillet_radius" 0.5 )
(ui-symbol "mo_mesh_fillet_chord_distance" 0.5 )

; Mesh Alignment options
; (ui-symbol "mo_mesh_alignment_keep_orig"    #f )
(ui-symbol "mo_mesh_alignment_mode"    0 )
(ui-symbol "mo_mesh_alignment_iterations"    5 )
(ui-symbol "mo_mesh_alignment_auto_recalc" #f )
(ui-symbol "mo_mesh_alignment_show_deviation_map" #f )
(ui-symbol "mo_mesh_alignment_translate_x"    #t )
(ui-symbol "mo_mesh_alignment_translate_y"    #t )
(ui-symbol "mo_mesh_alignment_translate_z"    #t )
(ui-symbol "mo_mesh_alignment_rotate_x"       #t )
(ui-symbol "mo_mesh_alignment_rotate_y"       #t )
(ui-symbol "mo_mesh_alignment_rotate_z"       #t )
(ui-symbol "mo_mesh_alignment_sampling_percent"  1.0 )
(ui-symbol "mo_mesh_alignment_rotationPivotType" 0 )
(ui-symbol "mo_mesh_alignment_rotationPivotPosition"  0.0 0.0 0.0)
(ui-symbol "mo_mesh_alignment_cullWRTNormAngle"  #t )
(ui-symbol "mo_mesh_alignment_cullNormAngleValue" 30.0 )
(ui-symbol "mo_mesh_alignment_UIcullNormAngleValue" 1 )
(ui-symbol "mo_mesh_alignment_cullWRTMeanDistance" #t )
(ui-symbol "mo_mesh_alignment_cullMeanDistanceFactor"  2.0 )
(ui-symbol "mo_mesh_alignment_UIcullMeanDistanceFactor"  1 )
(ui-symbol "mo_mesh_alignment_sampling_mode"  0 )
(ui-symbol "mo_mesh_alignment_fast_deviation_map"  #f )
(ui-symbol "mo_mesh_alignment_translate_mode" 0 )
(ui-symbol "mo_mesh_alignment_rotate_mode"    0 )
(ui-symbol "mo_mesh_alignment_translate_titleL"  #f )
(ui-symbol "mo_mesh_alignment_translate_titleR"  #f )

; Mesh Patch options
(ui-symbol "mo_mesh_patch_align_patch" #f)
(ui-symbol "mo_mesh_patch_align_tolerance" 0.5)
(ui-symbol "mo_mesh_patch_stitch_patch" #f)
(ui-symbol "mo_mesh_patch_stitch_tolerance" 0.05)
(ui-symbol "mo_mesh_patch_tessellation_size" 1.0)
(ui-symbol "mo_mesh_patch_debug_geometry" #f)

; Text attribute
(ui-symbol "pa_curr_font"	"Arial")
(ui-symbol "pa_text_font"	1)
(ui-symbol "pa_text_style"	1)
(ui-symbol "pa_text_size"  24)
(ui-symbol "pa_text_tracking"  0 )
(ui-symbol "pa_text_underline" #f )
(ui-symbol "pa_text_strikeout" #f )

; Plane Editor attribute
(ui-symbol "plane_show_mode" (ui-symbol-reference "PA_SHOW_PLANE_MODE_ALL"))
(ui-symbol "plane_displaytgl_canvasplane"		#t )
(ui-symbol "plane_displaytgl_annotateplane"		#t )

; Snap

; ShaderTool symbols

(ui-symbol "rp_lib_shaderball_path" "")
(ui-symbol "rp_res_shaderball_entry_name" "")
(ui-symbol "rp_res_shaderball_entry_type" 0)


;
;; Place Tool
;
(ui-symbol "mo_placetool_vec_f1" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_vec_f2" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_vec_f3" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_vec_t1" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_vec_t2" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_vec_t3" 0.0 0.0 1.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_placetool_delete_points" #t)
(ui-symbol "mo_placetool_set_lcl_axis" #t)

; save screen options

(ui-symbol "mo_savescreen_file_type"    (ui-symbol-reference "MO_FILETYPE_TIFF"))
(ui-symbol "mo_savescreen_resize"       #f)
(ui-symbol "mo_savescreen_limit_size"   #f)
(ui-symbol "mo_savescreen_max_x"        1280)
(ui-symbol "mo_savescreen_max_y"        1024)
(ui-symbol "mo_savescreen_q_factor"     90)
(ui-symbol "mo_savescreen_q_level"      (ui-symbol-reference "MO_Q_HIGH"))

; TglStereo options

(ui-symbol "mo_tglstereo_zspace_enabled"       #f)

; save current window options

(ui-symbol "mo_savecurrentwindow_file_type"    (ui-symbol-reference "MO_FILETYPE_TIFF"))
(ui-symbol "mo_savecurrentwindow_resize"       #f)
(ui-symbol "mo_savecurrentwindow_limit_size"   #f)
(ui-symbol "mo_savecurrentwindow_set_aspect"   #f)
(ui-symbol "mo_savecurrentwindow_aspect"       1.0)
(ui-symbol "mo_savecurrentwindow_max_x"        1280.0)
(ui-symbol "mo_savecurrentwindow_max_y"        1024.0)
(ui-symbol "mo_savecurrentwindow_q_factor"     90)
(ui-symbol "mo_savecurrentwindow_q_level"      (ui-symbol-reference "MO_Q_HIGH"))
(ui-symbol "mo_savecurrentwindow_AA_on"        #f)

; save current window options

(ui-symbol "mo_savetoillustrator_geom" 1 )
(ui-symbol "mo_savetoillustrator_max_x" 1280.0)
(ui-symbol "mo_savetoillustrator_max_y" 1024.0)
(ui-symbol "mo_savetoillustrator_scale_from" 1.0)
(ui-symbol "mo_savetoillustrator_scale_to" 1.0)
(ui-symbol "mo_savetoillustrator_scale" 1.0)
(ui-symbol "mo_savetoillustrator_active" 1)
(ui-symbol "mo_savetoillustrator_tol_crv_fit" 0.01)

(ui-symbol "mo_importsubdiv_split" #f)
(ui-symbol "mo_importsubdiv_refit" #t)

; publish bookmark options
(ui-symbol "mo_view_bookmark_publish_all"	   (ui-symbol-reference "MO_BOOKMARK_PUBLISH_SELECTED"))
(ui-symbol "mo_view_bookmark_publish_to"	   (ui-symbol-reference "MO_BOOKMARK_PUBLISH_TO_LOCAL"))
(ui-symbol "mo_view_bookmark_publish_image_type"	(ui-symbol-reference "MO_FILETYPE_JPEG"))
(ui-symbol "mo_view_bookmark_publish_sp"	   (ui-symbol-reference "MO_BOOKMARK_PUBLISH_TO_LOCAL"))
(ui-symbol "mo_view_bookmark_publish_seed"	   #t)


; ObjectLister options
(ui-symbol "ObjectLister_displaymode" 2 )
(ui-symbol "ObjectLister_sortmode" 0 )

(ui-symbol "ObjectLister_displaySymmetryIcon" 1 )
(ui-symbol "ObjectLister_displayLayerBarIcon" 0 )
(ui-symbol "ObjectLister_displayLayerNumIcon" 0 )
(ui-symbol "ObjectLister_displayPickStateIcon" 1 )
(ui-symbol "ObjectLister_displayLayerAnimIcon" 0 )

(ui-symbol "ObjectLister_displaySurfaceObjects" 1 )
(ui-symbol "ObjectLister_displayTrimSurfObjects" 1 )
(ui-symbol "ObjectLister_displayCurveObjects" 1 )
(ui-symbol "ObjectLister_displayCoSObjects" 1 )
(ui-symbol "ObjectLister_displayMeshObjects" 1 )
(ui-symbol "ObjectLister_displayConstructionObjects" 1 )
(ui-symbol "ObjectLister_displayCanvasObjects" 1 )
(ui-symbol "ObjectLister_displayMiscObjects" 1 )

; Curve transform options

(ui-symbol "curveeditor.transf.opt" 0 )

; One to One parameters
(ui-symbol "mo_one2one_length"		2)
(ui-symbol "mo_one2one_userdefined"	10.0)
(ui-symbol "mo_one2one_displayed"	10.0)
(ui-symbol "mo_one2one_scale"		0.0)

; Transformer Rig command options

(ui-symbol "TransformerRig_Type"                  1 )
(ui-symbol "TransformerRig_Influence"             1.0 )
(ui-symbol "TransformerRig_Cull"                  2.0 )
(ui-symbol "TransformerRig_Clamp"                 #t )
(ui-symbol "TransformerRig_ClampRbf"              0 )
(ui-symbol "TransformerRig_MvcWarp"               #f )
(ui-symbol "TransformerRig_AutoRecalc"            #f )
(ui-symbol "TransformerRig_ShowOriginal"          #f )
(ui-symbol "TransformerRig_ShowBoth"              #f )
(ui-symbol "TransformerRig_FittingEffort"         3.0 )
(ui-symbol "TransformerRig_FittingEffortCategory" 2 )
(ui-symbol "TransformerRig_DrawCorrespondence"    #f )
(ui-symbol "TransformerRig_DrawStat"              #t )
(ui-symbol "TransformerRig_CorrespondenceAlpha"   0.25 )
(ui-symbol "TransformerRig_StatType"              1 )
(ui-symbol "TransformerRig_NumSamples"            "---" )
(ui-symbol "TransformerRig_MaxSamples"            1000 )
(ui-symbol "TransformerRig_RefinementMethod"      0 )
(ui-symbol "TransformerRig_Density"               0.5 )
(ui-symbol "TransformerRig_ScaleTangent"          0 )
(ui-symbol "TransformerRig_NurbsWarpMethod"       1 )
(ui-symbol "TransformerRig_FitBoundary"           #t )
(ui-symbol "TransformerRig_MatchRigid"            #t )
(ui-symbol "TransformerRig_MinDegreeExplicit"     3 )
(ui-symbol "TransformerRig_MinDegreeAdaptive"     5 )
(ui-symbol "TransformerRig_MinSpans"              1 )
(ui-symbol "TransformerRig_CvShape"               0.1 )
(ui-symbol "TransformerRig_CvControlA"            0.0 )
(ui-symbol "TransformerRig_CvControlB"            0.0 )
(ui-symbol "TransformerRig_MeshOutput"            #f )
(ui-symbol "TransformerRig_BendScaleToLength"     #f )
(ui-symbol "TransformerRig_KeepOrientation"       #f )
(ui-symbol "TransformerRig_ShrinkTrim"            #f )

; Lattice Rig command options

(ui-symbol "LatticeRig_Type"                  1 )
(ui-symbol "LatticeRig_Influence"             1.0 )
(ui-symbol "LatticeRig_Cull"                  2.0 )
(ui-symbol "LatticeRig_Clamp"                 #t )
(ui-symbol "LatticeRig_ClampRbf"              0 )
(ui-symbol "LatticeRig_MvcWarp"               #f )
(ui-symbol "LatticeRig_AutoRecalc"            #t )
(ui-symbol "LatticeRig_ShowOriginal"          #f )
(ui-symbol "LatticeRig_ShowBoth"              #f )
(ui-symbol "LatticeRig_FittingEffort"         3.0 )
(ui-symbol "LatticeRig_FittingEffortCategory" 2 )
(ui-symbol "LatticeRig_DrawCorrespondence"    #f )
(ui-symbol "LatticeRig_DrawStat"              #t )
(ui-symbol "LatticeRig_CorrespondenceAlpha"   0.25 )
(ui-symbol "LatticeRig_StatType"              1 )
(ui-symbol "LatticeRig_NumSamples"            "---" )
(ui-symbol "LatticeRig_MaxSamples"            1000 )
(ui-symbol "LatticeRig_RefinementMethod"      0 )
(ui-symbol "LatticeRig_Density"               0.5 )
(ui-symbol "LatticeRig_ScaleTangent"          0 )
(ui-symbol "LatticeRig_NurbsWarpMethod"       1 )
(ui-symbol "LatticeRig_FitBoundary"           #t )
(ui-symbol "LatticeRig_MatchRigid"            #t )
(ui-symbol "LatticeRig_MinDegreeExplicit"     3 )
(ui-symbol "LatticeRig_MinDegreeAdaptive"     5 )
(ui-symbol "LatticeRig_MinSpans"              1 )
(ui-symbol "LatticeRig_CvShape"               0.1 )
(ui-symbol "LatticeRig_CvControlA"            0.0 )
(ui-symbol "LatticeRig_CvControlB"            0.0 )
(ui-symbol "LatticeRig_MeshOutput"            #f )
(ui-symbol "LatticeRig_BendScaleToLength"     #f )
(ui-symbol "LatticeRig_KeepOrientation"       #f )
(ui-symbol "LatticeRig_ShrinkTrim"            #f )

; Twist Rig command options

(ui-symbol "TwistRig_Type"                  1 )
(ui-symbol "TwistRig_Influence"             1.0 )
(ui-symbol "TwistRig_Cull"                  2.0 )
(ui-symbol "TwistRig_Clamp"                 #t )
(ui-symbol "TwistRig_ClampRbf"              0 )
(ui-symbol "TwistRig_MvcWarp"               #f )
(ui-symbol "TwistRig_AutoRecalc"            #t )
(ui-symbol "TwistRig_ShowOriginal"          #f )
(ui-symbol "TwistRig_ShowBoth"              #f )
(ui-symbol "TwistRig_FittingEffort"         3.0 )
(ui-symbol "TwistRig_FittingEffortCategory" 2 )
(ui-symbol "TwistRig_DrawCorrespondence"    #f )
(ui-symbol "TwistRig_DrawStat"              #t )
(ui-symbol "TwistRig_CorrespondenceAlpha"   0.25 )
(ui-symbol "TwistRig_StatType"              1 )
(ui-symbol "TwistRig_NumSamples"            "---" )
(ui-symbol "TwistRig_MaxSamples"            1000 )
(ui-symbol "TwistRig_RefinementMethod"      0 )
(ui-symbol "TwistRig_Density"               0.5 )
(ui-symbol "TwistRig_ScaleTangent"          0 )
(ui-symbol "TwistRig_NurbsWarpMethod"       1 )
(ui-symbol "TwistRig_FitBoundary"           #t )
(ui-symbol "TwistRig_MatchRigid"            #t )
(ui-symbol "TwistRig_MinDegreeExplicit"     3 )
(ui-symbol "TwistRig_MinDegreeAdaptive"     5 )
(ui-symbol "TwistRig_MinSpans"              1 )
(ui-symbol "TwistRig_CvShape"               0.1 )
(ui-symbol "TwistRig_CvControlA"            0.0 )
(ui-symbol "TwistRig_CvControlB"            0.0 )
(ui-symbol "TwistRig_MeshOutput"            #f )
(ui-symbol "TwistRig_BendScaleToLength"     #f )
(ui-symbol "TwistRig_KeepOrientation"       #f )
(ui-symbol "TwistRig_ShrinkTrim"            #f )

; Bend Rig command options

(ui-symbol "BendRig_Type"                  1 )
(ui-symbol "BendRig_Influence"             1.0 )
(ui-symbol "BendRig_Cull"                  2.0 )
(ui-symbol "BendRig_Clamp"                 #t )
(ui-symbol "BendRig_ClampRbf"              0 )
(ui-symbol "BendRig_MvcWarp"               #f )
(ui-symbol "BendRig_AutoRecalc"            #t )
(ui-symbol "BendRig_ShowOriginal"          #f )
(ui-symbol "BendRig_ShowBoth"              #f )
(ui-symbol "BendRig_FittingEffort"         3.0 )
(ui-symbol "BendRig_FittingEffortCategory" 2 )
(ui-symbol "BendRig_DrawCorrespondence"    #f )
(ui-symbol "BendRig_DrawStat"              #t )
(ui-symbol "BendRig_CorrespondenceAlpha"   0.25 )
(ui-symbol "BendRig_StatType"              1 )
(ui-symbol "BendRig_NumSamples"            "---" )
(ui-symbol "BendRig_MaxSamples"            1000 )
(ui-symbol "BendRig_RefinementMethod"      0 )
(ui-symbol "BendRig_Density"               0.5 )
(ui-symbol "BendRig_ScaleTangent"          0 )
(ui-symbol "BendRig_NurbsWarpMethod"       1 )
(ui-symbol "BendRig_FitBoundary"           #t )
(ui-symbol "BendRig_MatchRigid"            #t )
(ui-symbol "BendRig_MinDegreeExplicit"     3 )
(ui-symbol "BendRig_MinDegreeAdaptive"     5 )
(ui-symbol "BendRig_MinSpans"              1 )
(ui-symbol "BendRig_CvShape"               0.1 )
(ui-symbol "BendRig_CvControlA"            0.0 )
(ui-symbol "BendRig_CvControlB"            0.0 )
(ui-symbol "BendRig_MeshOutput"            #f )
(ui-symbol "BendRig_BendScaleToLength"     #f )
(ui-symbol "BendRig_KeepOrientation"       #f )
(ui-symbol "BendRig_ShrinkTrim"            #f )

; Conform Rig command options

(ui-symbol "ConformRig_Type"                  1 )
(ui-symbol "ConformRig_Influence"             1.0 )
(ui-symbol "ConformRig_Cull"                  2.0 )
(ui-symbol "ConformRig_Clamp"                 #t )
(ui-symbol "ConformRig_ClampRbf"              0 )
(ui-symbol "ConformRig_MvcWarp"               #f )
(ui-symbol "ConformRig_AutoRecalc"            #t )
(ui-symbol "ConformRig_ShowOriginal"          #f )
(ui-symbol "ConformRig_ShowBoth"              #f )
(ui-symbol "ConformRig_FittingEffort"         3.0 )
(ui-symbol "ConformRig_FittingEffortCategory" 2 )
(ui-symbol "ConformRig_DrawCorrespondence"    #f )
(ui-symbol "ConformRig_DrawStat"              #t )
(ui-symbol "ConformRig_CorrespondenceAlpha"   0.25 )
(ui-symbol "ConformRig_StatType"              1 )
(ui-symbol "ConformRig_NumSamples"            "---" )
(ui-symbol "ConformRig_MaxSamples"            1000 )
(ui-symbol "ConformRig_RefinementMethod"      0 )
(ui-symbol "ConformRig_Density"               0.5 )
(ui-symbol "ConformRig_ScaleTangent"          0 )
(ui-symbol "ConformRig_NurbsWarpMethod"       1 )
(ui-symbol "ConformRig_FitBoundary"           #t )
(ui-symbol "ConformRig_MatchRigid"            #t )
(ui-symbol "ConformRig_MinDegreeExplicit"     3 )
(ui-symbol "ConformRig_MinDegreeAdaptive"     5 )
(ui-symbol "ConformRig_MinSpans"              1 )
(ui-symbol "ConformRig_CvShape"               0.1 )
(ui-symbol "ConformRig_CvControlA"            0.0 )
(ui-symbol "ConformRig_CvControlB"            0.0 )
(ui-symbol "ConformRig_MeshOutput"            #f )
(ui-symbol "ConformRig_BendScaleToLength"     #f )
(ui-symbol "ConformRig_KeepOrientation"       #f )
(ui-symbol "ConformRig_ShrinkTrim"            #f )

; Feature Snap command options

(ui-symbol "FeatureSnap_Type"                  1 )
(ui-symbol "FeatureSnap_Influence"             1.0 )
(ui-symbol "FeatureSnap_Cull"                  2.0 )
(ui-symbol "FeatureSnap_Clamp"                 #t )
(ui-symbol "FeatureSnap_ClampRbf"              0 )
(ui-symbol "FeatureSnap_MvcWarp"               #f )
(ui-symbol "FeatureSnap_AutoRecalc"            #t )
(ui-symbol "FeatureSnap_ShowOriginal"          #f )
(ui-symbol "FeatureSnap_ShowBoth"              #f )
(ui-symbol "FeatureSnap_FittingEffort"         3.0 )
(ui-symbol "FeatureSnap_FittingEffortCategory" 2 )
(ui-symbol "FeatureSnap_DrawCorrespondence"    #f )
(ui-symbol "FeatureSnap_DrawStat"              #t )
(ui-symbol "FeatureSnap_CorrespondenceAlpha"   0.25 )
(ui-symbol "FeatureSnap_StatType"              1 )
(ui-symbol "FeatureSnap_NumSamples"            "---" )
(ui-symbol "FeatureSnap_MaxSamples"            1000 )
(ui-symbol "FeatureSnap_RefinementMethod"      0 )
(ui-symbol "FeatureSnap_Density"               0.5 )
(ui-symbol "FeatureSnap_ScaleTangent"          0 )
(ui-symbol "FeatureSnap_NurbsWarpMethod"       1 )
(ui-symbol "FeatureSnap_FitBoundary"           #t )
(ui-symbol "FeatureSnap_MatchRigid"            #t )
(ui-symbol "FeatureSnap_MinDegreeExplicit"     3 )
(ui-symbol "FeatureSnap_MinDegreeAdaptive"     5 )
(ui-symbol "FeatureSnap_MinSpans"              1 )
(ui-symbol "FeatureSnap_CvShape"               0.1 )
(ui-symbol "FeatureSnap_CvControlA"            0.0 )
(ui-symbol "FeatureSnap_CvControlB"            0.0 )
(ui-symbol "FeatureSnap_MeshOutput"            #f )
(ui-symbol "FeatureSnap_BendScaleToLength"     #f )
(ui-symbol "FeatureSnap_KeepOrientation"       #f )
(ui-symbol "FeatureSnap_ShrinkTrim"            #f )

; Feature Place command options

(ui-symbol "DuplicatePlace_Type"                  1 )
(ui-symbol "DuplicatePlace_Influence"             1.0 )
(ui-symbol "DuplicatePlace_Cull"                  2.0 )
(ui-symbol "DuplicatePlace_Clamp"                 #t )
(ui-symbol "DuplicatePlace_ClampRbf"              1 )
(ui-symbol "DuplicatePlace_MvcWarp"               #f )
(ui-symbol "DuplicatePlace_AutoRecalc"            #t )
(ui-symbol "DuplicatePlace_ShowOriginal"          #f )
(ui-symbol "DuplicatePlace_ShowBoth"              #f )
(ui-symbol "DuplicatePlace_FittingEffort"         3.0 )
(ui-symbol "DuplicatePlace_FittingEffortCategory" 2 )
(ui-symbol "DuplicatePlace_DrawCorrespondence"    #f )
(ui-symbol "DuplicatePlace_DrawStat"              #t )
(ui-symbol "DuplicatePlace_CorrespondenceAlpha"   5. )
(ui-symbol "DuplicatePlace_StatType"              1 )
(ui-symbol "DuplicatePlace_NumSamples"            "---" )
(ui-symbol "DuplicatePlace_MaxSamples"            1000 )
(ui-symbol "DuplicatePlace_RefinementMethod"      0 )
(ui-symbol "DuplicatePlace_Density"               0.5 )
(ui-symbol "DuplicatePlace_ScaleTangent"          0 )
(ui-symbol "DuplicatePlace_NurbsWarpMethod"       1 )
(ui-symbol "DuplicatePlace_FitBoundary"           #t )
(ui-symbol "DuplicatePlace_MatchRigid"            #t )
(ui-symbol "DuplicatePlace_MinDegreeExplicit"     3 )
(ui-symbol "DuplicatePlace_MinDegreeAdaptive"     5 )
(ui-symbol "DuplicatePlace_MinSpans"              1 )
(ui-symbol "DuplicatePlace_CvShape"               0.1 )
(ui-symbol "DuplicatePlace_CvControlA"            0.0 )
(ui-symbol "DuplicatePlace_CvControlB"            0.0 )
(ui-symbol "DuplicatePlace_MeshOutput"            #f )
(ui-symbol "DuplicatePlace_BendScaleToLength"     #f )
(ui-symbol "DuplicatePlace_KeepOrientation"       #f )
(ui-symbol "DuplicatePlace_ShrinkTrim"            #f )

; Window Display options
(ui-symbol "mw_display_mode"          1 )
(ui-symbol "mw_display_scope"         #t )
(ui-symbol "mw_display_model"         #t )
(ui-symbol "mw_display_pivots"        #t )
(ui-symbol "mw_display_grid"          #t )
(ui-symbol "mw_display_guidelines"    #t )
(ui-symbol "mw_display_locators"      #t )
(ui-symbol "mw_display_construction"  #t )
(ui-symbol "mw_display_canvases"      #t )
(ui-symbol "mw_display_lights"        #f )
(ui-symbol "mw_display_textures"      #f )
(ui-symbol "mw_display_cameras"       #f )
(ui-symbol "mw_display_image_planes"  #f )
(ui-symbol "mw_display_clouds"        #t )
(ui-symbol "mw_display_nonproportional" #t )

; Xray Controls options
(ui-symbol "mo_xray_draw_model"           #f )
(ui-symbol "mo_xray_draw_controls"        #t )
(ui-symbol "mo_xray_draw_pivots"          #t )
(ui-symbol "mo_xray_draw_hulls"           #t )
(ui-symbol "mo_xray_draw_key_points"      #t )
(ui-symbol "mo_xray_draw_locators"        #t )
(ui-symbol "mo_xray_draw_visibility"      0.15 )

; Transparency options
(ui-symbol "mw_transparency_controls"           0.0 )
(ui-symbol "mw_transparency_controls_active"    #t )
(ui-symbol "mw_transparency_curves"             0.0 )
(ui-symbol "mw_transparency_curves_active"      #t )
(ui-symbol "mw_transparency_surfaces"           0.0 )
(ui-symbol "mw_transparency_surfaces_active"    #t )
(ui-symbol "mw_transparency_meshes"             0.0 )
(ui-symbol "mw_transparency_meshes_active"      #t )
(ui-symbol "mw_transparency_canvases"           0.0 )
(ui-symbol "mw_transparency_canvases_active"    #t )
(ui-symbol "mw_transparency_locators"           0.0 )
(ui-symbol "mw_transparency_locators_active"    #t )
(ui-symbol "mw_transparency_reference"          0.0 )
(ui-symbol "mw_transparency_reference_active"   #t )

(ui-symbol "mw_toggle_model_wireframe_only"       #f)
(ui-symbol "mw_toggle_model_scope"                (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_pivots_scope"               (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_grid_scope"                 (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_guidelines_scope"           (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_locators_scope"             (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_construction_objects_scope" (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_canvases_scope"             (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_lights_scope"               (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_textures_scope"             (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_cameras_scope"              (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_image_planes_scope"         (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_clouds_scope"               (ui-symbol-reference "MO_ALL_WIND"))
(ui-symbol "mw_toggle_nonproportional_scope"      (ui-symbol-reference "MO_CUR_WIND"))


(ui-symbol "mo_display_controls_transparency"   0.0 )
(ui-symbol "mo_display_curve_transparency"      0.0 )
(ui-symbol "mo_display_surface_transparency"    0.0 )
(ui-symbol "mo_display_canvas_transparency"     0.0 )
(ui-symbol "mo_display_reference_transparency"  0.0 )
(ui-symbol "mo_display_locators_transparency" 	0.0 )

;MSF Round options
(ui-symbol "mo_msfround_default_radius"			10.0)
(ui-symbol "mo_msfround_trim_type"				2)
(ui-symbol "mo_msfround_extend_fillets"			#t)
(ui-symbol "mo_msfround_trim_fillets"			#t)
(ui-symbol "mo_msfround_3feq_corner_type"		2)
(ui-symbol "mo_msfround_3fne_corner_type"		4)
(ui-symbol "mo_msfround_mitred_corner_type"		5)
(ui-symbol "mo_msfround_4sided_corner_type"		8)


(ui-symbol "mo_hardwareParamchoice"		0)
(ui-symbol "mo_list_buttons"		"Copy" )

; Unify Normals Tool
(ui-symbol "mo_unify_normals_type"	0)
(ui-symbol "mo_unify_normals_operation"	(ui-symbol-reference "MO_REV_U"))

; Reference Tools Options

; Note: if you update the conversion tolerance defaults, you should
; also update the defaults in the translator (aliasToRef.cpp).

(ui-symbol "mo_convertRef_use_proj_dir" #t)
(ui-symbol "mo_convertRef_dir" "")
(ui-symbol "mo_convertRef_tol" 0.01) ; see note above!
(ui-symbol "mo_convertRef_tess_type" (ui-symbol-reference "MO_TGLSHADE_ARUBA_TESSELATOR"))
(ui-symbol "mo_convertRef_crv_tol" 0.001) ; see note above!

(ui-symbol "mo_retessRef_tess_type" (ui-symbol-reference "MO_TGLSHADE_ARUBA_TESSELATOR"))
(ui-symbol "mo_retessRef_tol" 0.01)

;AlignNova Options
(ui-symbol "mo_align_nova_autoRecalc"                    #t)
(ui-symbol "mo_align_nova_create_history"                #t)
(ui-symbol "mo_align_nova_slaveSrf_explicit"             #t)
(ui-symbol "mo_align_nova_slaveSrf_udeg"                 3)
(ui-symbol "mo_align_nova_slaveSrf_vdeg"                 3)
(ui-symbol "mo_align_nova_slaveSrf_uspans"               1)
(ui-symbol "mo_align_nova_slaveSrf_vspans"               1)
(ui-symbol "mo_align_nova_continuity"                    0)
(ui-symbol "mo_align_nova_want_continuity_check"         #t)
(ui-symbol "mo_align_nova_specify_continuity_check_type" #f)
(ui-symbol "mo_align_nova_continuity_check_type"         0)
(ui-symbol "mo_align_nova_enable_blending"               #f)
(ui-symbol "mo_align_nova_blending_num_rows_modified"    0)
(ui-symbol "mo_align_nova_blending_decay"                1.0)
(ui-symbol "mo_align_nova_enable_overhang_tolerance"     #f)
(ui-symbol "mo_align_nova_enable_partial"                #f)
(ui-symbol "mo_align_nova_enable_position_influence"     #t)
(ui-symbol "mo_align_nova_enable_directional"            #f)
(ui-symbol "mo_align_nova_vector_constraint"             0)
(ui-symbol "mo_align_nova_crv_srf_alignType"             0)
;(ui-symbol "mo_align_nova_aSlider_G1_value0"             1.0)
;(ui-symbol "mo_align_nova_aSlider_G1_value1"             1.0)
(ui-symbol "mo_align_nova_aSlider_G2_infer"              #f)
(ui-symbol "mo_align_nova_aSlider_G3_infer"              #f)
;(ui-symbol "mo_align_nova_aSlider_G2_value0"             10.0)
;(ui-symbol "mo_align_nova_aSlider_G2_value1"             10.0)
(ui-symbol "mo_align_nova_lock_G1_values"                #f)
(ui-symbol "mo_align_nova_lock_G2_values"                #f)
(ui-symbol "mo_align_nova_project_vector_name"           "")
(ui-symbol "mo_align_nova_project_vector_presets"        3)
;(ui-symbol "mo_align_nova_project_vector_create"         0)
;(ui-symbol "mo_align_nova_project_vector_save"           0)
;(ui-symbol "mo_align_nova_project_vector_create"		  0)
(ui-symbol "mo_align_nova_slave_influence_value"         0.0)
(ui-symbol "mo_align_nova_slave_tangent_balance"         #f)
(ui-symbol "mo_align_nova_SS_align_linked"               #f)
(ui-symbol "mo_align_nova_SS_align0"                     2)
(ui-symbol "mo_align_nova_SS_align1"                     2)
;(ui-symbol "mo_align_nova_SS_skew_angle0"                0.0)
;(ui-symbol "mo_align_nova_SS_skew_angle1"                0.0)
(ui-symbol "mo_align_nova_partial_auto_snap"             99.0)
(ui-symbol "mo_align_nova_proxy_display"                 #f)
(ui-symbol "mo_align_nova_diagnostic_feedback"           #f)
(ui-symbol "mo_align_nova_lock_row0"                     #f)

; Diagnostic Shade Adjust Light Options
(ui-symbol "mo_diagnosticshade_rotateLight_azimuth"      0.0)
(ui-symbol "mo_diagnosticshade_rotateLight_elevation"    0.0)
(ui-symbol "mo_diagnosticshade_lightLinkedToCamera"      #t)
(ui-symbol "mo_diagnosticshade_rotateLight_eye"      0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_rotateLight_view"     0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_rotateLight_up"       0.0 0.0 0.0)
(ui-symbol "mo_diagnosticshade_rotateLight_pivot"    0.0 0.0 0.0)

(ui-symbol "productization_report_autotest"              #f)
(ui-symbol "productization_report_type"	                 1)

; Pedestrian Protection tools
(ui-symbol "mo_pedpro_ground_height" 0.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_pedpro_pedestrian_height" 125.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_pedpro_impact_zone" 60.0 UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_pedpro_auto_recalc" #f UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_pedpro_create_history" #t UI_SYMBOL_GROUP_MISCELLANEOUS)
(ui-symbol "mo_pedpro_samples" 50 UI_SYMBOL_GROUP_MISCELLANEOUS)

(ui-symbol "mo_toggleVisibility_cameras"		#f)
(ui-symbol "mo_toggleVisibility_lights"			#f)
(ui-symbol "mo_toggleVisibility_textures"		#f)
(ui-symbol "mo_toggleVisibility_construction"	#f)
(ui-symbol "using_16x_aa"	#f)

; Profile Tool
(ui-symbol "mo_profile_orientation" 0)
(ui-symbol "mo_profile_target" 1)
(ui-symbol "mo_profile_use_point" #f)
(ui-symbol "mo_profile_profile_orientation" 5) ; agregate of the above symbols.
(ui-symbol "mo_profile_frame_travel" 2)
(ui-symbol "mo_profile_scaling" 0)
(ui-symbol "mo_profile_param" 0.0)

(ui-symbol "mo_profile_surface_location" 1)
(ui-symbol "mo_profile_transition_type" 1)
(ui-symbol "mo_profile_surface_type" 1)
(ui-symbol "mo_profile_single_span" #f)
(ui-symbol "mo_profile_explicit_control" #f)
(ui-symbol "mo_profile_u_degree" 5)
(ui-symbol "mo_profile_v_degree" 5)
(ui-symbol "mo_profile_max_num_spans" 100)
(ui-symbol "mo_profile_short_edge_tol" 0.001)

(ui-symbol "mo_profile_modify_range" #f)
(ui-symbol "mo_profile_range_start" 0.0)
(ui-symbol "mo_profile_range_end" 1.0)
(ui-symbol "mo_profile_target_start" 0.0)
(ui-symbol "mo_profile_target_end" 1.0)

(ui-symbol "mo_profile_preview" #f)
(ui-symbol "mo_profile_preview_param" 0.0)

(ui-symbol "mo_profile_auto_recalc" #f)
(ui-symbol "mo_profile_continuity_check" #f)
(ui-symbol "mo_profile_deviation_check" #f)
(ui-symbol "mo_profile_create_history" #t)
(ui-symbol "mo_profile_match_parameterization" #t)
(ui-symbol "mo_profile_touch_line_type" 0)

(ui-symbol "mo_profile_pick_chain" #t)

; Automotive Stitching
(ui-symbol "mo_auto_stitch_seam_type"			1)
(ui-symbol "mo_auto_stitch_seam_offset"			1.0)
(ui-symbol "mo_auto_stitch_seam_depth"			0.1)
(ui-symbol "mo_auto_stitch_seam_shape"			1.0)
(ui-symbol "mo_auto_stitch_seam_gap"			0.0)
(ui-symbol "mo_auto_stitch_seam_side"			#f)
(ui-symbol "mo_auto_stitch_seam_flip"			#f)
(ui-symbol "mo_auto_stitch_want_clip"			#f)
(ui-symbol "mo_auto_stitch_clip_start"			0.0)
(ui-symbol "mo_auto_stitch_clip_end"			1.0)
(ui-symbol "mo_auto_stitch_want_bulgeA"			#t)
(ui-symbol "mo_auto_stitch_want_bulgeB"			#t)
(ui-symbol "mo_auto_stitch_bulge_size"			0.1)
(ui-symbol "mo_auto_stitch_want_grooveA"		#t)
(ui-symbol "mo_auto_stitch_want_grooveB"		#t)
(ui-symbol "mo_auto_stitch_groove_size"			0.2)
(ui-symbol "mo_auto_stitch_behave"				#f)
(ui-symbol "mo_auto_stitch_want_stitchA"		#t)
(ui-symbol "mo_auto_stitch_want_stitchB"		#t)
(ui-symbol "mo_auto_stitch_stitch_diameter"		0.1)
(ui-symbol "mo_auto_stitch_stitch_length"		1.0)
(ui-symbol "mo_auto_stitch_stitch_spacing"		0.1)
(ui-symbol "mo_auto_stitch_stitch_angle"		0.0)
(ui-symbol "mo_auto_stitch_stitch_tautness"		0.5)
(ui-symbol "mo_auto_stitch_flip_direction"		#f)
(ui-symbol "mo_auto_stitch_flip_stitch"			#f)
(ui-symbol "mo_auto_stitch_quick_stitch"		#t)
(ui-symbol "mo_auto_stitch_trim_stitch"			#t)
(ui-symbol "mo_auto_stitch_start_edge_flow"		1)
(ui-symbol "mo_auto_stitch_interior_flow"		5)
(ui-symbol "mo_auto_stitch_end_edge_flow"		1)
(ui-symbol "mo_auto_stitch_want_jitter"			#f)
(ui-symbol "mo_auto_stitch_stitch_jitter"		0.0)

(ui-symbol "mo_auto_stitch_trim_type"
		(ui-symbol-reference 'MO_FILLET_SRF_TRIM_TYPE_AUTOMATIC))
(ui-symbol "mo_auto_stitch_auto_update"			#f)
(ui-symbol "mo_auto_stitch_pick_chain"			#f)
(ui-symbol "mo_auto_stitch_create_history"		#t)
(ui-symbol "mo_auto_stitch_debug_geometry"		#f)

; some legacy profile symbols.
(ui-symbol "mo_profile_frame_name" "")
(ui-symbol "mo_profile_frame_presets" 2)
(ui-symbol "mo_profile_frame_refresh" 0)
(ui-symbol "mo_profile_frame_save" 0)

(ui-symbol "mo_profile_plane_name" "")
(ui-symbol "mo_profile_plane_presets" 2)
(ui-symbol "mo_profile_plane_refresh" 0)
(ui-symbol "mo_profile_plane_save" 0)
(ui-symbol "mo_profile_orientation" 2)


; Multi Blend surface tool
(ui-symbol "mo_multiblend_chain_select" #t)
(ui-symbol "mo_multiblend_debug_geometry" #f)
(ui-symbol "mo_multiblend_auto_update" #f)
(ui-symbol "mo_multiblend_create_history" #t)
(ui-symbol "mo_multiblend_check_deviation" #f)
(ui-symbol "mo_multiblend_use_star_point" #f)
(ui-symbol "mo_multiblend_star_point_type" 0)
(ui-symbol "mo_multiblend_udegree" 3)
(ui-symbol "mo_multiblend_vdegree" 3)
(ui-symbol "mo_multiblend_split_type" 0)
(ui-symbol "mo_multiblend_cross_variation" #f)
(ui-symbol "mo_multiblend_seam_continuity" 1)
(ui-symbol "mo_multiblend_edge_continuity" 1)
(ui-symbol "mo_multiblend_single_surface" #f)
(ui-symbol "mo_multiblend_inner_curvature_continuity" #f)
(ui-symbol "mo_multiblend_shape_factor" 1.0)
(ui-symbol "mo_multiblend_tolG0" 0.01 )
(ui-symbol "mo_multiblend_tolG1" 0.1 )

; Surface Chain tool
(ui-symbol "mo_surface_chain_continuity" 0)
(ui-symbol "mo_surface_chain_use_tolerances" #f)
(ui-symbol "mo_surface_chain_edge_coincident_tol" 0.001)
(ui-symbol "mo_surface_chain_edge_tangent_tol" 0.1)

(ui-symbol "mo_surface_chain_debug_geometry" #f)

; Surface Align tool
(ui-symbol "mo_surface_align_0_mode" 0)
(ui-symbol "mo_surface_align_1_mode" 0)
(ui-symbol "mo_surface_align_2_mode" 0)
(ui-symbol "mo_surface_align_3_mode" 0)

(ui-symbol "mo_surface_align_0_adopt" #f)
(ui-symbol "mo_surface_align_1_adopt" #f)
(ui-symbol "mo_surface_align_2_adopt" #f)
(ui-symbol "mo_surface_align_3_adopt" #f)

(ui-symbol "mo_surface_align_continuity_check" #f)
(ui-symbol "mo_surface_align_chain_select" #f)
(ui-symbol "mo_surface_align_auto_update" #f)

(ui-symbol "mo_surface_align_0_start" 0.0)
(ui-symbol "mo_surface_align_1_start" 0.0)
(ui-symbol "mo_surface_align_2_start" 0.0)
(ui-symbol "mo_surface_align_3_start" 0.0)

(ui-symbol "mo_surface_align_0_end" 1.0)
(ui-symbol "mo_surface_align_1_end" 1.0)
(ui-symbol "mo_surface_align_2_end" 1.0)
(ui-symbol "mo_surface_align_3_end" 1.0)

(ui-symbol "mo_surface_align_0_invert" #f)
(ui-symbol "mo_surface_align_1_invert" #f)
(ui-symbol "mo_surface_align_2_invert" #f)
(ui-symbol "mo_surface_align_3_invert" #f)

(ui-symbol "mo_surface_align_0_partial" #f)
(ui-symbol "mo_surface_align_1_partial" #f)
(ui-symbol "mo_surface_align_2_partial" #f)
(ui-symbol "mo_surface_align_3_partial" #f)

(ui-symbol "mo_surface_align_0_adapt" #f)
(ui-symbol "mo_surface_align_1_adapt" #f)
(ui-symbol "mo_surface_align_2_adapt" #f)
(ui-symbol "mo_surface_align_3_adapt" #f)

(ui-symbol "mo_surface_align_0_arc" #f)
(ui-symbol "mo_surface_align_1_arc" #f)
(ui-symbol "mo_surface_align_2_arc" #f)
(ui-symbol "mo_surface_align_3_arc" #f)

(ui-symbol "mo_surface_align_0_raise" #f)
(ui-symbol "mo_surface_align_1_raise" #f)
(ui-symbol "mo_surface_align_2_raise" #f)
(ui-symbol "mo_surface_align_3_raise" #f)

(ui-symbol "mo_surface_align_0_force" #f)
(ui-symbol "mo_surface_align_1_force" #f)
(ui-symbol "mo_surface_align_2_force" #f)
(ui-symbol "mo_surface_align_3_force" #f)

(ui-symbol "variant_cycle_time"     0.5 )
(ui-symbol "variantGroup_show_mask" #t )
(ui-symbol "variantGroup_show_name" #t )
(ui-symbol "variantGroup_show_player" #t )

(ui-symbol "mo_freeform_curve_aside_continuity" 1)
(ui-symbol "mo_freeform_curve_bside_continuity" 1)
(ui-symbol "mo_freeform_curve_planar" #f)
(ui-symbol "mo_freeform_curve_blend_type" 0)
(ui-symbol "mo_freeform_curve_shape_lock" #t)
(ui-symbol "mo_freeform_curve_form_factor" 1.0)
(ui-symbol "mo_freeform_curve_aside_shape" 1.0)
(ui-symbol "mo_freeform_curve_bside_shape" 1.0)
(ui-symbol "mo_freeform_curve_auto_recalc" #f)
(ui-symbol "mo_freeform_curve_pick_chain" #f)
(ui-symbol "mo_freeform_curve_aside_alignment" 0)
(ui-symbol "mo_freeform_curve_bside_alignment" 0)
(ui-symbol "mo_freeform_curve_bside_projection" 0)
(ui-symbol "mo_freeform_curve_closest_point" #f)

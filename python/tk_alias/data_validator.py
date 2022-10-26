# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.

import sgtk
from tank_vendor import six
from tank.util import sgre as re

import alias_api
import alias_py.dag_node
import alias_py.layer
import alias_py.pick_list
import alias_py.utils
import alias_py.traverse_dag


class AliasDataValidator(object):
    """
    The Alias Data Validator class provides the data and functionality to validate data in Alias.

    The :meth:`get_validation_data` method returns the default validation rules data set, that drives the
    data validation. Each rule in the validation data includes the necessary information to display the
    validation rule, and the functions to perform the validation check and fix actions for the rule.

    The validation rule check functions are the functions prefixed with :meth:`check_` and the fix functions
    are prefixed with :meth:`fix_`.

    Some rules may not have the full capability of being resolved programatically, and do not have a fix
    function. These rules may define a :meth:`pick_` function that helps to resolve the data errors by first
    selecting the data that requires attention.
    """

    #
    # Alias defaults
    #
    DEFAULT_LAYER_NAME = "DefaultLayer"
    DEFAULT_SHADER_NAME = "DefaultShader"

    def __init__(self):
        """
        Initialize the AliasDataValidator object.
        """

        self._camera_node_types = alias_py.utils.camera_node_types()
        self._light_node_types = alias_py.utils.light_node_types()

    # -------------------------------------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------------------------------------

    def get_validation_data(self):
        """
        Return the validation rule data set that is used to validate Alias data.

        This is the main function of the class. It defines how the Alias data is validated, and
        provides the functions to resolve those data errors in Alias.

        The returned data set is a dictionay mapping of validation rule id to its validation rule data.

        **Default Validation Rule IDs:**

            shader_unused
                Check for shaders that are not assigned to any geometry, and delete them.
            shader_is_vred_compatible:
                Check that shaders are from the Asset Library for compatibility with VRED.
            node_is_null
                Check for null nodes, and delete them.
            node_has_construction_history:
                Check for nodes with construction history, and delete the history.
            node_instances
                Check for node instances, and convert them to geometry.
            node_pivots_at_origin
                Reset rotate and scale pivots to the global origin (absolute).
            node_has_zero_transform
                Check for nodes with non-zero transforms, and apply the zero transform operation.
            node_templates
                Check for tempalted nodes, and delete them.
            cos_unused
                Check for unused COS, and delete them.
            cos_construction_history
                Check for unused COS with construction history, and delete the history.
            curves
                Check for curves, and delete them.
            set_empty
                Check for empty sets, and delete them.
            group_has_single_level_hierarchy
                Check for group nodes that have a group node child, and flatten the group node to a single level by moving all grandchildren to be a child of the top group node.
            layer_is_empty
                Check for empty layers and folders, and delete them.
            layer_has_single_object
                Check for layers that have multiple objects, and move all objects into a single group node in the layer.
            layer_has_single_shader
                Check for layers whose geometry does not all use a single shader.
            layer_symmetry
                Check for layers that have the symmetry property turned on, and turn it off.
            locators
                Check for locators, and delete them.
            references_exist
                for referenced geometry, and delete it.
            metadata
                Check for metadata, and delete it.
            node_dag_top_level
                Top-level DAG nodes must be of one of the specified types: AlGroupNode, AlCurveNode, AlFaceNode, or AlSurfaceNode.
            node_is_not_in_layer
                Only Lights, Cameras, Texture Placements, and Groups can be in the default layer.
            node_is_in_layer
                All Lights, Camera, and Texture Placements must be in the default layer.
            node_layer_matches_parent
                The layer assigned to a node must be the same layer that is assigned to the node's parent.
            node_name_matches_layer
                A node's name must match the name of the layer that is assigned to the node.

        **The Validation Rule data:**

        .. literalinclude:: ../python/tk_alias/data_validator.py
            :language: python
            :linenos:
            :lines: 187-830

        Each validation rule is a dictionary of data that can be used to create a :class:`~tk-multi-data-validation:api.data.ValidationRule`. See the :class:`~tk-multi-data-validation:api.data.ValidationRule` constructor for more details on the dictionary data format it accepts.

        :return: The validation rules data set.
        :rtype: dict
        """

        return {
            "shader_unused": {
                "name": "Delete Unused Shaders",
                "description": """Check: Unused shaders<br/>
                                Fix: Delete. DefaultShader is not affected.""",
                "error_msg": "Found unused shaders",
                "check_func": self.check_shader_unused,
                "fix_func": self.fix_shader_unused,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete unused Shaders.",
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_shader_unused,
                    },
                ],
                "get_kwargs": lambda: {"skip_shaders": [self.DEFAULT_SHADER_NAME]},
                "dependency_ids": [
                    "node_is_null",
                    "node_instances",
                ],
            },
            "shader_is_vred_compatible": {
                "name": "Only Use VRED Shaders",
                "description": """Check: Shaders are from the Asset Library (VRED-compatible)<br/>
                                Fix: You must assign shaders from the Asset Library. DefaultShader is not affected.""",
                "check_func": self.check_shader_is_vred_compatible,
                "error_msg": "Found shader(s) that are incompatible with VRED.",
                "actions": [
                    {
                        "name": "Select All Shader Geometry",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select Shader Geometry",
                        "callback": self.pick_nodes_assigned_to_shaders,
                    },
                ],
                "get_kwargs": lambda: {"skip_shaders": [self.DEFAULT_SHADER_NAME]},
            },
            "node_is_null": {
                "name": "Delete Null Nodes",
                "description": """Check: Null nodes<br/>
                                Action: Delete""",
                "fix_func": self.fix_node_is_null,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all null nodes.",
                "warn_msg": 'This validation does not return a status. To ensure all null nodes are deleted, select "Delete All" or "Fix All."',
                "dependency_ids": [
                    "node_has_construction_history",
                ],
            },
            "node_has_construction_history": {
                "name": "Delete Construction History",
                "description": """Check: Construction history<br/>
                                Action: Delete""",
                "check_func": self.check_node_has_construction_history,
                "fix_func": self.fix_node_has_construction_history,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all construction history from all nodes.",
                "error_msg": "Found node(s) with construction history.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_node_has_construction_history,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "get_kwargs": lambda: {
                    "skip_node_types": [
                        alias_api.AlObjectType.GroupNodeType,
                        alias_api.AlObjectType.CurveNodeType,
                        alias_api.AlObjectType.FaceNodeType,
                        alias_api.AlObjectType.TextureNodeType,
                    ],
                },
            },
            "node_instances": {
                "name": "Convert Instances to Geometry",
                "description": """Check: Instances<br/>
                                Action: Convert to geometry.""",
                "check_func": self.check_node_instances,
                "fix_func": self.fix_node_instances,
                "fix_name": "Expand All",
                "fix_tooltip": "Remove Instances by expanding them.",
                "error_msg": "Instance found.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Expand",
                        "callback": self.fix_node_instances,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": ["node_has_construction_history", "node_is_null"],
            },
            "node_pivots_at_origin": {
                "name": "Reset Pivots to Global Origin",
                "description": """Check: Pivot point coordinates<br/>
                                Fix: Set pivot points to global origin (0, 0, 0). Camera, light, and texture nodes are not affected.""",
                "check_func": self.check_node_pivots_at_origin,
                "fix_func": self.fix_node_pivots_at_origin,
                "fix_name": "Reset All",
                "fix_tooltip": "All pivots will be moved to the origin. Camera, light, and texture nodes are not affected."
                "",
                "error_msg": "Found pivots not set to the origin.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Reset",
                        "callback": self.fix_node_pivots_at_origin,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": ["node_has_construction_history", "node_is_null"],
                "get_kwargs": lambda: {
                    "skip_node_types": [
                        alias_api.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ]
                },
            },
            "node_has_zero_transform": {
                "name": "Zero Transforms",
                "description": """Check: Non-zero transformations<br/>
                                Action: Sets transformations to 0.0 on each node and DAG node. Camera, light, and texture nodes are not affected.""",
                "check_func": self.check_node_has_zero_transform,
                "fix_func": self.fix_node_has_zero_transform,
                "fix_name": "Reset All",
                "fix_tooltip": "Reset all transforms to zero. Camera, light, and texture nodes are not affected."
                "",
                "error_msg": "Found node(s) with non-zero transform.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Reset",
                        "callback": self.fix_node_has_zero_transform,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "get_kwargs": lambda: {
                    "skip_node_types": [
                        alias_api.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ]
                },
                "dependency_ids": ["node_has_construction_history", "node_is_null"],
            },
            "node_is_not_in_layer": {
                "name": "Nodes Must Not Be In DefaultLayer",
                "description": """Check: Only camera, light, texture, and group nodes should be in the DefaultLayer.""",
                "check_func": self.check_node_is_not_in_layer,
                "error_msg": "Found nodes in the default layer that are not allowed.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                        "tooltip": "Select nodes to manually fix data errors.",
                    },
                ],
                "get_kwargs": lambda: {
                    "layer_name": self.DEFAULT_LAYER_NAME,
                    "accept_node_types": [
                        alias_api.AlObjectType.GroupNodeType,
                        alias_api.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ],
                },
                "dependency_ids": ["node_is_null"],
            },
            "node_is_in_layer": {
                "name": "Nodes Must Be In DefaultLayer",
                "description": """Check: All camera, light, and texture nodes must be in the DefaultLayer<br/>
                                Fix: Move all light, camera, and texture nodes to the DefaultLayer.""",
                "check_func": self.check_node_is_in_layer,
                "fix_func": self.fix_node_is_in_layer,
                "fix_name": "Move",
                "fix_tooltip": "Move all lights, cameras, and texture nodes to the DefaultLayer.",
                "error_msg": "Required objects not found in the DefaultLayer.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Move",
                        "callback": self.fix_node_is_in_layer,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "get_kwargs": lambda: {
                    "layer_name": self.DEFAULT_LAYER_NAME,
                    "accept_node_types": [
                        alias_api.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ],
                },
                "dependency_ids": ["node_is_null"],
            },
            "node_name_matches_layer": {
                "name": "Match Layer And Assigned Nodes' Names",
                "description": """Check: Layer and Top Node Names<br/>
                                Fix: Rename top node in layer to match the layer name. DefaultLayer is not affected.""",
                "check_func": self.check_node_name_matches_layer,
                "fix_func": self.fix_node_name_matches_layer,
                "fix_name": "Rename All",
                "fix_tooltip": "Rename Groups to match their respective Layer name.",
                "error_msg": "Found Layer Group name mismatches.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Rename",
                        "callback": self.fix_node_name_matches_layer,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "get_kwargs": lambda: {"skip_layers": [self.DEFAULT_LAYER_NAME]},
                "dependency_ids": ["node_is_in_layer", "node_is_not_in_layer"],
            },
            "node_layer_matches_parent": {
                "name": "Node Layer Matches Parent Layer",
                "description": """Check: Layer assignment<br/>
                                Fix: Re-assign node to the same layer as the parent node layer.""",
                "check_func": self.check_node_layer_matches_parent,
                "fix_func": self.fix_node_layer_matches_parent,
                "fix_name": "Reassign All",
                "fix_tooltip": "Set each node's layer to match its parent's layer.",
                "error_msg": "Found node(s) assigned to layer different than its parent.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Reassign",
                        "callback": self.fix_node_layer_matches_parent,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": [
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                    "group_has_single_level_hierarchy",
                ],
            },
            "node_dag_top_level": {
                "name": "Top-Level DAG Nodes",
                "description": """Check: DAG Top-level Nodes<br/>
                                Fix: DAG top-level nodes must be a group, curve, face, or surface node.""",
                "check_func": self.check_node_dag_top_level,
                "error_msg": "Found nodes in the top level of the DAG that are not allowed.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                        "tooltip": "Select nodes to manually fix data errors.",
                    },
                ],
                "get_kwargs": lambda: {
                    "accept_node_types": [
                        alias_api.AlObjectType.CurveNodeType,
                        alias_api.AlObjectType.FaceNodeType,
                        alias_api.AlObjectType.SurfaceNodeType,
                        alias_api.AlObjectType.GroupNodeType,
                    ],
                },
            },
            "node_templates": {
                "name": "Delete Templates",
                "description": """Check: Templated geometry<br/>
                                Fix: Delete""",
                "check_func": self.check_node_templates,
                "fix_func": self.fix_node_templates,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete nodes that are set as templates.",
                "error_msg": "Found node(s) that are set as templates.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_node_templates,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": ["node_has_construction_history", "node_is_null"],
            },
            "cos_unused": {
                "name": "Delete Unused Curves-on-Surfaces (COS)",
                "description": """Check: Unused curves-on-surfaces (COS)<br/>
                                Fix: Delete""",
                "check_func": self.check_curve_on_surface_unused,
                "fix_func": self.fix_curve_on_surface_unused,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete unused COS.",
                "error_msg": "Found unused COS.",
                "actions": [
                    {
                        "name": "Select All COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                    {
                        "name": "Select All Nodes",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_curve_on_surface_unused,
                    },
                    {
                        "name": "Select COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                    {
                        "name": "Select Nodes",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": [
                    "cos_construction_history",
                    "node_has_construction_history",
                    "node_is_null",
                ],
            },
            "cos_construction_history": {
                "description": "Check for nodes with unused COS with construction history.",
                "name": "Delete Unused Curves-on-Surfaces (COS) Construction History",
                "description": """Check: Unused curves-on-surfaces (COS) with construction history<br/>
                                Fix: Delete construction history for unused COS.""",
                "check_func": self.check_curve_on_surface_construction_history,
                "fix_func": self.fix_curve_on_surface_construction_history,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete construction history for unused curve on surface",
                "error_msg": "Found construction history for unused curve(s) on surface.",
                "actions": [
                    {
                        "name": "Select All COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                    {
                        "name": "Select All Nodes",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_curve_on_surface_unused,
                    },
                    {
                        "name": "Select COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                    {
                        "name": "Select Nodes",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": ["node_has_construction_history"],
            },
            "curves": {
                "name": "Delete Curves",
                "description": """Check: Curves<br/>
                                Fix: Delete""",
                "check_func": self.check_node_curves,
                "fix_func": self.fix_node_curves,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all curves found.",
                "error_msg": "Found curve(s).",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_node_curves,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": ["node_has_construction_history", "node_is_null"],
            },
            "set_empty": {
                "name": "Delete Empty Selection Sets",
                "description": """Check: Empty sets<br/>
                                Fix: Delete""",
                "check_func": self.check_set_empty,
                "fix_func": self.fix_set_empty,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete empty selection sets found.",
                "error_msg": "Found empty selection set(s).",
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_set_empty,
                    },
                ],
                "dependency_ids": [
                    "node_is_null",
                ],
            },
            "group_has_single_level_hierarchy": {
                "name": "Only One Level Per Group",
                "description": """Check: Group hierarchy<br/>
                                Fix: Flatten group nodes to have a single-level hierarchy.""",
                "check_func": self.check_group_has_single_level_hierarchy,
                "fix_func": self.fix_group_has_single_level_hierarchy,
                "fix_name": "Flatten All",
                "fix_tooltip": "Flatten Groups with multiple hierarchy levels.",
                "error_msg": "Found Groups with multiple hierarchy levels.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Flatten",
                        "callback": self.fix_group_has_single_level_hierarchy,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": [
                    "node_is_null",
                    "layer_has_single_object",
                ],
            },
            "layer_is_empty": {
                "name": "Delete Empty Layers and Folders",
                "description": """Check: Empty Layers and Folders<br/>
                                Fix: Delete. DefaultLayer is not affected.""",
                "check_func": self.check_layer_is_empty,
                "fix_func": self.fix_layer_is_empty,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete empty layers and folders",
                "error_msg": "Found empty layers or folders",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_layers,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_layer_is_empty,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_layers,
                    },
                ],
                "get_kwargs": lambda: {"skip_layers": [self.DEFAULT_LAYER_NAME]},
                "dependency_ids": ["node_is_null"],
            },
            "layer_has_single_shader": {
                "name": "Layer Has Single Shader",
                "description": """Check: Layer Members' Shaders""",
                "check_func": self.check_layer_has_single_shader,
                "error_msg": "Found layer(s) using multiple shaders.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_layers,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select Layer",
                        "callback": self.pick_layers,
                    },
                    {
                        "name": "Select Layer Geometry",
                        "callback": self.pick_nodes_assigned_to_layers,
                    },
                ],
                "dependency_ids": [
                    "node_is_null",
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                ],
            },
            "layer_symmetry": {
                "name": "Turn Off (All) Layer Symmetry",
                "description": """Check: Layer Symmetry<br/>
                                Fix: Turn off symmetry on layers. DefaultLayer is not affected.""",
                "check_func": self.check_layer_symmetry,
                "fix_func": self.fix_layer_symmetry,
                "fix_name": "Turn Off All",
                "fix_tooltip": "Turn off symmetry for all Layers and Layer Folders.",
                "error_msg": "Found Layers with symmetry turned on.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_layers,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Turn Off",
                        "callback": self.fix_layer_symmetry,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_layers,
                    },
                ],
                "get_kwargs": lambda: {"skip_layers": [self.DEFAULT_LAYER_NAME]},
            },
            "layer_has_single_object": {
                "name": "Layer Has Single Item",
                "description": """Check: Layer Members<br/>
                                Fix: Move all layer members into a single group node. DefaultLayer is not affected.""",
                "check_func": self.check_layer_has_single_object,
                "fix_func": self.fix_layer_has_single_object,
                "fix_name": "Collapse All",
                "fix_tooltip": "Collapse all layer items into a single group, and rename the group to the name of the layer.",
                "error_msg": "Found layers with more than one item.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_layers,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select Layer",
                        "callback": self.pick_layers,
                    },
                    {
                        "name": "Select Layer Geometry",
                        "callback": self.pick_nodes_assigned_to_layers,
                    },
                ],
                "get_kwargs": lambda: {"skip_layers": [self.DEFAULT_LAYER_NAME]},
                "dependency_ids": [
                    "layer_is_empty",
                    "node_is_null",
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                    "node_has_zero_transform",
                ],
            },
            "locators": {
                "name": "Delete Locators",
                "description": """Check: Locators<br/>
                                Fix: Delete including Annotate locators.""",
                "check_func": self.check_locators,
                "fix_func": self.fix_locators,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete locators",
                "error_msg": "Found locator(s).",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_locators,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_locators,
                    },
                    {
                        "name": "Select",
                        "callback": self.pick_locators,
                    },
                ],
            },
            "metadata": {
                "name": "Delete Metadata",
                "description": "Check: Metadata",
            },
            "references_exist": {
                "name": "Remove Referenced Geometry",
                "description": """Check: Referenced geometry (.wref).<br/>
                                Fix: Delete""",
                "check_func": self.check_refererences_exist,
                "fix_func": self.fix_references_exist,
                "fix_name": "Remove",
                "fix_tooltip": "Remove all referenced geometry.",
                "error_msg": "Found referenced geometry.",
            },
        }

    # -------------------------------------------------------------------------------------------------------
    # Check & Fix Functions
    # -------------------------------------------------------------------------------------------------------
    #   These can be executed directly, but they are meant to be defined as a 'check_func' in the validation
    #   data and executed using the validatino data rule item.
    #
    #   Guidelines to defining a check function:
    #       - Function name should be prefixed with `check_`
    #       - Takes an optional single parameter `fail_fast` which returned immediately once the check fails
    #       - Returns a list of Alias objects
    #
    #   Guidelines to defining a fix function:
    #       - Function name should be prefixed with `fix_`
    #       - Takes an optional single parameter `errors` which are the items intended to be fixed.
    #               The naming of the parameter is important since this is passed from the check function
    #               return value)
    #       - Function may define other parameters but they should be key-word arguments that appear after
    #         the optional `errors` param
    #
    # -------------------------------------------------------------------------------------------------------

    @sgtk.LogManager.log_timing
    def check_shader_unused(self, fail_fast=False, skip_shaders=None):
        """
        Check for unused shaders (shaders that are not assigned to any geometry) in Alias.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param skip_shaders: The specified shaders (by name) will not be checked.
        :type skip_shaders: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_shaders = skip_shaders or []
        unused_shaders = []

        for shader in alias_api.get_shaders():
            if shader.name in skip_shaders:
                continue

            if not shader.is_used():
                if fail_fast:
                    return False
                unused_shaders.append(shader)

        return unused_shaders

    @sgtk.LogManager.log_timing
    def fix_shader_unused(self, errors=None, skip_shaders=None):
        """
        Process all shaders in Alias, or the specified shaders, and delete all unused shaders.

        NOTE that the shaders list in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to see the
        updated shaders list.

        :param errors: (optional) The shaders to process, if None, all shaders will be
            processed. Default=None
        :type errors: str | list<str> | list<AlShader> | list<dict>
        :param skip_shaders: The specified shaders (by name) will not be fixed.
        :type skip_shaders: list<str>
        """

        skip_shaders = skip_shaders or []

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        shaders = errors or alias_api.get_shaders()

        for shader in shaders:
            if isinstance(shader, six.string_types):
                if shader in skip_shaders:
                    continue
                shader = alias_api.get_shader_by_name(shader)
                if not shader:
                    continue
            elif shader.name in skip_shaders:
                continue

            if not shader.is_used():
                shader.delete_object()

    @sgtk.LogManager.log_timing
    def check_shader_is_vred_compatible(self, fail_fast=False, skip_shaders=None):
        """
        Check for non-VRED shaders used in the current stage.

        A non-VRED shader is a shader that is not from the Asset Library (compaitible with VRED). Only shaders
        that are in use will be checked (e.g. if there is a non-VRED shader but is not used, it will not cause
        this check to fail).

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param skip_shaders: The specified shaders (by name) will not be checked.
        :type skip_shaders: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_shaders = skip_shaders or []
        non_vred_shaders = []

        for shader in alias_api.get_shaders():
            if shader.name in skip_shaders:
                continue

            if shader.is_used() and not alias_api.is_copy_of_vred_shader(shader):
                if fail_fast:
                    return False
                non_vred_shaders.append(shader)

        return non_vred_shaders

    @sgtk.LogManager.log_timing
    def fix_node_is_null(self, errors=None):
        """
        Process all nodes in the current stage, or the specified nodes, and delete all null nodes.

        :param errors: (optional) The of nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>

        :raises alias_api.AliasPythonException: if the attempting to delete specific nodes
        """

        if errors is None:
            alias_api.delete_null_nodes()
        else:
            # NOTE we could just delete the list of given nodes, but we cannot determine if a given node is null.
            alias_py.utils.raise_exception(
                "Requires Alias C++ API function to determine if a node is null"
            )

    @sgtk.LogManager.log_timing
    def check_node_has_construction_history(
        self, fail_fast=False, skip_node_types=None
    ):
        """
        Check for nodes with construction history in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool
        :param skip_node_types: The specified node types will not be checked.
        :type skip_node_types: list<alias_api.AlObjectType>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_node_types = skip_node_types or []

        nodes_with_history = alias_py.dag_node.get_nodes_with_construction_history(
            skip_node_types=set(skip_node_types),
        )

        return nodes_with_history

    @sgtk.LogManager.log_timing
    def fix_node_has_construction_history(self, errors=None, skip_node_types=None):
        """
        Process all nodes in the current stage, or the specified of nodes, and delete history from any nodes
        with history.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The nodes to process, if None, all nodes in the current stage will
                       be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        skip_node_types = skip_node_types or []

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        nodes = alias_py.dag_node.get_nodes_with_construction_history(
            nodes=errors,
            skip_node_types=set(skip_node_types),
        )
        for node in nodes:
            alias_api.delete_history(node)

    @sgtk.LogManager.log_timing
    def check_node_instances(self, fail_fast=False):
        """
        Check for instanced nodes in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        return alias_py.dag_node.get_instanced_nodes()

    @sgtk.LogManager.log_timing
    def fix_node_instances(self, errors=None):
        """
        Process all nodes in the current stage, or the list of nodes if provided, and remove all instanced
        nodes.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The list of nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>

        :raises alias_api.AliasPythonException: if a node instance failed to expand
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        nodes = alias_py.dag_node.get_instanced_nodes(errors)

        for node in nodes:
            status = alias_api.expand_instances(node)
            if not alias_py.utils.is_success(status):
                alias_py.utils.raise_exception(
                    "Failed to expand instanced node '{}'".format(node.name), status
                )

    @sgtk.LogManager.log_timing
    def check_node_pivots_at_origin(self, fail_fast=False, skip_node_types=None):
        """
        Check for nodes that do not have their pivots set to the origin.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_node_types = skip_node_types or []

        return alias_py.dag_node.get_nodes_with_non_origin_pivot(
            skip_node_types=set(skip_node_types),
        )

    @sgtk.LogManager.log_timing
    def fix_node_pivots_at_origin(self, errors=None, skip_node_types=None):
        """
        Process all nodes in the current stage, or the specified nodes, and reset their scale and roate
        pivots such that they are centered around the origin.

        NOTE that the pivots Alias may not update automatically, alias_api.redraw_screen() may need to be
        invoked after this function, to see the updated pivots.

        :param errors: (optional) The nodes to process, if None, all nodes in the current stage will
                              be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>

        :raises alias_api.AliasPythonException: if a failed to set a node's pivot to the origin
        """

        skip_node_types = skip_node_types or []

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        nodes = alias_py.dag_node.get_nodes_with_non_origin_pivot(
            nodes=errors,
            skip_node_types=set(skip_node_types),
        )
        center = alias_api.Vec3(0.0, 0.0, 0.0)

        for node in nodes:
            status = node.set_scale_pivot(center)
            if not alias_py.utils.is_success(status):
                alias_py.utils.raise_exception(
                    "Failed to set scale pivot for node '{}'".format(node.name), status
                )

            status = node.set_rotate_pivot(center)
            if not alias_py.utils.is_success(status):
                alias_py.utils.raise_exception(
                    "Failed to set rotate pivot for node '{}'".format(node.name), status
                )

    @sgtk.LogManager.log_timing
    def check_node_has_zero_transform(self, fail_fast=False, skip_node_types=None):
        """
        Check for nodes with non-zero transforms in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool
        :param skip_node_types: The specified node types will not be checked.
        :type skip_node_types: list<alias_api.AlObjectType>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_node_types = skip_node_types or []

        return alias_py.dag_node.get_nodes_with_non_zero_transform(
            skip_node_types=set(skip_node_types),
        )

    @sgtk.LogManager.log_timing
    def fix_node_has_zero_transform(self, errors=None, skip_node_types=None):
        """
        Process all nodes in the current stage, or the specified nodes, and reset all transforms to zero.

        NOTE that the nodes Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated node transforms.

        :param errors: (optional) The nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>

        :raises alias_api.AliasPythonException: if a failed to set a node's transform to zero
        """

        skip_node_types = skip_node_types or []

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if not errors:
            # Optimize the zero transform by first calling the zero transform on all top-level nodes
            # Then get the remaining nodes that do not have zero transform and apply it to those only.
            alias_api.zero_transform_top_level()

        nodes = alias_py.dag_node.get_nodes_with_non_zero_transform(
            nodes=errors,
            skip_node_types=set(skip_node_types),
        )

        if nodes:
            status = alias_api.zero_transform(nodes)
            if not alias_py.utils.is_success(status):
                alias_py.utils.raise_exception(
                    "Failed to apply zero transform to nodes. Returned status:",
                    status,
                )

    @sgtk.LogManager.log_timing
    def check_node_is_not_in_layer(
        self, fail_fast=False, layer_name=None, accept_node_types=None
    ):
        """
        Check that the layer contains only nodes of type in the accepted list.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param layer_name: The layer to check node membership. Default is the default layer in Alias.
        :type layer_name: str
        :param accept_node_types: Only the specified node types are accepted in the layer.
        :type accept_node_types: list<alias_api.AlObjectType>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        layer = alias_api.get_layer_by_name(layer_name)
        if layer is None:
            alias_py.utils.raise_exception("Layer not found '{}'".format(layer_name))

        accept_node_types = accept_node_types or []
        invalid_nodes = []

        # NOTE get_assigned_nodes will not return the group nodes, only leaf nodes assigned to the layer
        nodes = layer.get_assigned_nodes()

        for node in nodes:
            if node.type() not in accept_node_types:
                if fail_fast:
                    return False
                invalid_nodes.append(node)

        return invalid_nodes

    @sgtk.LogManager.log_timing
    def check_node_is_in_layer(
        self, fail_fast=False, layer_name=None, accept_node_types=None
    ):
        """
        Check that the specified node types are in the layer.

        The whole DAG will be traversed to find nodes that are incorrectly placed in a layer that is not the
        specified layer.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool
        :param layer_name: The layer that the specified node types belong to. Default is the default layer in
            Alias.
        :type layer_name: str
        :param accept_node_types: The node types that must only be in the layer.
        :type accept_node_types: list<alias_api.AlObjectType>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        layer = alias_api.get_layer_by_name(layer_name)
        if layer is None:
            alias_py.utils.raise_exception("Layer not found '{}'".format(layer_name))

        # Traverse the DAG to look for nodes that should be in the default layer, but are not.
        accept_node_types = set(accept_node_types or [])
        input_data = alias_api.TraverseDagInputData(
            layer, False, accept_node_types, True
        )
        result = alias_api.search_dag(input_data)

        return result.nodes

    @sgtk.LogManager.log_timing
    def fix_node_is_in_layer(
        self, errors=None, layer_name=None, accept_node_types=None
    ):
        """
        Process all nodes in the current stage, or the specified nodes, and move any nodes found that are of
        the specified node type but not in the specified layer.

        :param errors: (optional) The of nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        :param layer_name: The layer that the specified node types belong to. Default is the default layer in Alias.
        :type layer_name: str
        :param accept_node_types: The node types only accepted in the default layer.
        :type accept_node_types: list<alias_api.AlObjectType>
        """

        layer = alias_api.get_layer_by_name(layer_name)
        if layer is None:
            alias_py.utils.raise_exception("Layer not found '{}'".format(layer_name))

        accept_node_types = accept_node_types or []

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if errors:
            for node in errors:
                if isinstance(node, six.string_types):
                    node = alias_api.find_dag_node_by_name(node)

                if not node:
                    continue

                node_layer = node.layer()
                if (not node_layer or node_layer.name != layer_name) and (
                    not accept_node_types or node.type() in accept_node_types
                ):
                    node.set_layer(layer)

        else:
            # Find nodes that should be in the default layer, but are not.
            input_data = alias_api.TraverseDagInputData(
                layer, False, set(accept_node_types), True
            )
            result = alias_api.search_dag(input_data)

            # Place the nodes into their correct layer
            for node in result.nodes:
                node.set_layer(layer)

    @sgtk.LogManager.log_timing
    def check_node_name_matches_layer(self, fail_fast=False, skip_layers=None):
        """
        Check for naming mismatches between layer and its nodes, for all top-levle nodes in the current stage.

        Each layer should only contain one group (or one surface). This group is named after the layer.
        If groups are found that don't match the name of the layer, an error is thrown.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param skip_layers: The specified layers (by name) will not be checked.
        :type skip_layers: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        invalid_nodes = []
        nodes = alias_api.get_top_dag_nodes()

        for node in nodes:
            layer = node.layer()
            if not layer or (skip_layers and layer.name in skip_layers):
                continue

            # Check the layer and node names match, which means they are the same or the ndoe name is the
            # layer name plus the suffix "#n" where 'n' is a number.
            reg = r"^{}(#?\d)*$".format(layer.name)
            if not re.match(reg, node.name):
                if fail_fast:
                    return False
                invalid_nodes.append(node)

        return invalid_nodes

    @sgtk.LogManager.log_timing
    def fix_node_name_matches_layer(self, errors=None, skip_layers=None):
        """
        Process all nodes in the current stage, or the specified nodes, and rename any nodes that do not
        match its layer.

        :param errors: (optional) The of nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        :param skip_layers: Nodes in the specified layers (by name) will not be fixed.
        :type skip_layers: list<str>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        nodes = errors or alias_api.get_top_dag_nodes()

        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node:
                continue

            node_layer = node.layer()
            if not node_layer:
                continue

            node_layer_name = node_layer.name
            if skip_layers and node_layer_name in skip_layers:
                continue

            reg = r"^{}(#?\d)*$".format(node_layer_name)
            if not re.match(reg, node.name):
                node.name = node_layer_name

    @sgtk.LogManager.log_timing
    def check_node_layer_matches_parent(self, fail_fast=False):
        """
        Check for nodes that do not have the layer as their parent node.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_layer_does_not_match_parent_layer(input_data)

        return result.nodes

    @sgtk.LogManager.log_timing
    def fix_node_layer_matches_parent(self, errors=None):
        """
        Process all nodes in the current stage, or the specified nodes, and ensure that a node's layer is the
        same as its parent node's layer.

        :param errors: (optional) The of nodes to process, if None, all nodes in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if errors:
            for node in errors:
                if isinstance(node, six.string_types):
                    node = alias_api.find_dag_node_by_name(node)

                if not node:
                    continue

                parent_node = node.parent_node()
                if not parent_node:
                    continue

                parent_node_layer = parent_node.layer()
                if not parent_node_layer:
                    continue

                node_layer = node.layer()
                if not node_layer or node_layer.number != parent_node_layer.number:
                    node.set_layer(parent_node_layer)

        else:
            input_data = alias_api.TraverseDagInputData()
            result = alias_api.search_node_layer_does_not_match_parent_layer(input_data)
            for node in result.nodes:
                node.set_layer(node.parent_node().layer())

    @sgtk.LogManager.log_timing
    def check_node_dag_top_level(self, fail_fast=False, accept_node_types=None):
        """
        Check for invalid top-level nodes in the DAG of the current stage.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param accept_node_types: Only the specified node types are accepted in the top level of the DAG.
        :type accept_node_types: list<alias_api.AlObjectType>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        accept_node_types = accept_node_types or []
        invalid_nodes = []
        nodes = alias_api.get_top_dag_nodes()

        for node in nodes:
            if node.type() not in accept_node_types:
                if fail_fast:
                    return False
                invalid_nodes.append(node)

        return invalid_nodes

    @sgtk.LogManager.log_timing
    def check_node_templates(self, fail_fast=False):
        """
        Check for nodes that are set as templates.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        result = alias_api.traverse_dag(alias_py.traverse_dag.node_is_template)
        return result.nodes

    @sgtk.LogManager.log_timing
    def fix_node_templates(self, errors=None):
        """
        Process all nodes in the current stage, or the list of nodes if provided, and delete nodes that are
        set as a template.

        :param errors: The list of nodes to process, if None, all nodes in the current stage will be
            processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        """

        if isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if errors:
            alias_py.dag_node.delete_nodes(errors)

        else:
            result = alias_api.traverse_dag(alias_py.traverse_dag.node_is_template)
            for node in result.nodes:
                node.delete_object()

    @sgtk.LogManager.log_timing
    def check_node_curves(self, fail_fast=False):
        """
        Check for nodes that represent a curve (ie. AlCurveNode objects).

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        # Find all (and only) AlCurveNode objects
        return alias_py.dag_node.get_nodes_by_type(
            [alias_api.AlObjectType.CurveNodeType]
        )

    @sgtk.LogManager.log_timing
    def fix_node_curves(self, errors=None):
        """
        Process all nodes in the current stage, or the list of nodes if provided, and delete all nodes that
        represent a curve.

        :param errors: The list of nodes to process, if None, all nodes in the current stage will be
            processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        """

        if isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if errors:
            alias_py.dag_node.delete_nodes(errors)

        else:
            curve_nodes = alias_py.dag_node.get_nodes_by_type(
                [alias_api.AlObjectType.CurveNodeType]
            )

            for node in curve_nodes:
                node.delete_object()

    @sgtk.LogManager.log_timing
    def check_curve_on_surface_unused(self, fail_fast=False):
        """
        Check for unused curves on surfaces in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        return alias_py.dag_node.get_nodes_with_unused_curves_on_surface()

    @sgtk.LogManager.log_timing
    def fix_curve_on_surface_unused(self, errors=None):
        """
        Process all curves on surface current stage, or the list of curves on surface if provided, and delete
        unused curves on surface.

        :param errors: The list of curves on surface to process, if None, all curves on surface
                              current stage will be processed. Default=None
        :type errors: str | list<str> | list<AlCurveOnSurface> | list<dict>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        unused_curves = alias_py.dag_node.get_unused_curves_on_surface_for_nodes(
            nodes=errors
        )

        for curve in unused_curves:
            curve.delete_object()

    @sgtk.LogManager.log_timing
    def check_curve_on_surface_construction_history(self, fail_fast=False):
        """
        Check for unused curves on surfaces that have construction history in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        unused_cos = alias_py.dag_node.get_unused_curves_on_surface_for_nodes()

        invalid_nodes = []
        for cos in unused_cos:
            if alias_api.has_construction_history(cos):
                invalid_nodes.append(cos.surface().surface_node())

        return invalid_nodes

    @sgtk.LogManager.log_timing
    def fix_curve_on_surface_construction_history(self, errors=None):
        """
        Process all curves on surface current stage, or the list of curves on surface if provided, and delete
        construction history for unused curves on surface.

        :param errors: The list of curves on surface to process, if None, all curves on surface
                              current stage will be processed. Default=None
        :type errors: str | list<str> | list<AlCurveOnSurface> | list<dict>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        unused_cos = alias_py.dag_node.get_unused_curves_on_surface_for_nodes(
            nodes=errors
        )

        for cos in unused_cos:
            if alias_api.has_construction_history(cos):
                alias_api.delete_construction_history(cos)

    @sgtk.LogManager.log_timing
    def check_set_empty(self, fail_fast=False):
        """
        Check for sets that empty.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        empty_sets = []
        alias_set = alias_api.first_set()

        while alias_set:
            if alias_set.is_empty():
                empty_sets.append(alias_set)
            alias_set = alias_set.next_set()

        return empty_sets

    @sgtk.LogManager.log_timing
    def fix_set_empty(self, errors=None):
        """
        Process all sets in the current stage, or the list of sets if provided, and delete all sets that are
        empty.

        :param errors: The list of nodes to process, if None, all nodes in the current stage will be
            processed. Default=None
        :type errors: str | list<str> | list<AlDagNode> | list<dict>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        # The list of specifi set names to delete. Leave empty to delete all sets.
        set_names = []
        if errors:
            for item in errors:
                if isinstance(item, six.string_types):
                    set_names.append(item)
                elif isinstance(item, alias_api.AlSet):
                    set_names.append(item.name)

        alias_set = alias_api.first_set()
        while alias_set:
            if alias_set.is_empty():
                if not set_names or alias_set.name in set_names:
                    alias_set.delete_object()
            alias_set = alias_set.next_set()

        if errors:
            alias_py.dag_node.delete_nodes(errors)

    @sgtk.LogManager.log_timing
    def check_layer_is_empty(self, fail_fast=False, skip_layers=None):
        """
        Check for empty layers and layer folders in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool
        :param skip_layers: The specified layers (by name) will not be checked.
        :type skip_layers: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        skip_layers = set(skip_layers or [])
        include_folders = True
        return alias_api.get_empty_layers(include_folders, skip_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_is_empty(self, errors=None, skip_layers=None):
        """
        Process all layers in the current stage, or the list of layers if provided, and delete all the empty layers and layer
        folders.

        :param layers: (optiona) The layers to process, if None, all layers in the current stage will
                       be processed. Default=None
        :type layers: str | list<str> | list<AlLayer>
        :param skip_layers: The specified layers (by name) will not be fixed.
        :type skip_layers: list<str>
        """

        skip_layers = set(skip_layers or [])
        include_folders = True
        empty_layers = alias_api.get_empty_layers(include_folders, skip_layers)

        # If a list of layers is specified, only delete those layers.
        delete_only = []
        if errors:
            if isinstance(errors, six.string_types):
                errors = [errors]
            elif isinstance(errors, list):
                for i, error_item in enumerate(errors):
                    if isinstance(error_item, dict):
                        errors[i] = error_item["name"]

            for layer in errors:
                if isinstance(layer, six.string_types):
                    delete_only.append(layer)
                else:
                    delete_only.append(layer.name)

        for layer in empty_layers:
            if not delete_only or layer.name in delete_only:
                layer.delete_object()

    @sgtk.LogManager.log_timing
    def check_layer_has_single_shader(self, fail_fast=False):
        """
        Check that all nodes in a layer use the same single shader.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        return alias_api.get_layers_using_multiple_shaders()

    @sgtk.LogManager.log_timing
    def check_layer_symmetry(self, fail_fast=False, skip_layers=None):
        """
        Check for layers with symmetry turned on in the current stage.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param skip_layers: The specified layers (by name) will not be checked.
        :type skip_layers: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        if fail_fast:
            has_symmetric_layers = alias_py.layer.get_symmetric_layers(
                check_exists=True, skip_layers=skip_layers
            )
            return not has_symmetric_layers

        return alias_py.layer.get_symmetric_layers(skip_layers=skip_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_symmetry(self, errors=None, skip_layers=None):
        """
        Process all layers in the current stage, or the specified layers, and turn off symmetry on layers.

        NOTE that the layers in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated layers.

        :param errors: (optional) The layers to process, if None, all layers in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlLayer> | list<dict>
        :param skip_layers: The specified layers (by name) will not be fixed.
        :type skip_layers: list<str>
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        layers = alias_py.layer.get_symmetric_layers(
            layers=errors, skip_layers=skip_layers
        )

        for layer in layers:
            layer.symmetric = False

    @sgtk.LogManager.log_timing
    def check_layer_has_single_object(self, fail_fast=False, skip_layers=None):
        """
        Check for layers that contain more than one top-level node (e.g. layers can only have a single node,
        for multiple nodes, they can have a group node that contains child nodes).

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool
        :param skip_layers: The specified layers (by name) will not be checked.
        :type skip_layers: list<str>

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        invalid_layers = []
        processed_layers = set()
        marked_invalid_layers = set()

        nodes = alias_api.get_top_dag_nodes()

        for node in nodes:
            node_layer = node.layer()
            if not node_layer:
                continue

            node_layer_name = node_layer.name
            if (
                skip_layers and node_layer_name in skip_layers
            ) or node_layer_name in marked_invalid_layers:
                continue

            if node_layer_name in processed_layers:
                if fail_fast:
                    return False
                invalid_layers.append(node_layer)
                marked_invalid_layers.add(node_layer_name)
            else:
                processed_layers.add(node_layer_name)

        return invalid_layers

    @sgtk.LogManager.log_timing
    def fix_layer_has_single_object(self, errors=None, skip_layers=None):
        """
        Process all layers in the current stage, or the list of layers if provided, and place all
        layer's contents into a single group.

        A new group will be created if the layer does not have any group nodes currently.

        NOTE that the layers in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The list of layers to process, if None, all layers in the current
                              stage will be processed. Default=None
        :type errors: str | list<str> | list<AlLayer> | list<dict>
        :param skip_layers: The specified layers (by name) will not be fixed.
        :type skip_layers: list<str>
        """

        # TODO this algorithm to fix the layer could probably be cleaned up and optimized.

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        layers = errors or alias_api.get_layers()

        for layer in layers:
            if isinstance(layer, six.string_types):
                layer = alias_api.get_layer_by_name(layer)

            if not layer:
                continue

            layer_name = layer.name
            if skip_layers and layer_name in skip_layers:
                continue

            group_node = None

            layer_top_level_nodes = []
            layer_group_nodes = []
            for node in alias_api.get_top_dag_nodes():
                if node.layer().name != layer_name:
                    continue

                layer_top_level_nodes.append(node)

                if alias_py.utils.is_group_node(node):
                    layer_group_nodes.append(node)

            if not layer_top_level_nodes:
                # Skip empty layers
                continue

            # first case: no existing group node
            if not layer_group_nodes:
                group_node = alias_api.AlGroupNode()
                status = group_node.create()
                if not alias_py.utils.is_success(status):
                    alias_py.utils.raise_exception(
                        "Failed to create group node for layer", status
                    )

                group_node.name = layer_name
                group_node.set_layer(layer)

            else:
                # second case: only one group node exist
                if len(layer_group_nodes) == 1:
                    group_node = layer_group_nodes[0]

                # third case: many group nodes exist
                else:
                    # try to get the one named after the layer, otherwise use the first one
                    for group in layer_group_nodes:
                        if group.name == layer_name:
                            group_node = group
                            break
                    if not group_node:
                        group_node = layer_group_nodes[0]

            if not group_node:
                raise ValueError("Failed to find group node for layer")

            for node in layer_top_level_nodes:
                if node.name != group_node.name:
                    group_node.add_child_node(node)

    @sgtk.LogManager.log_timing
    def check_group_has_single_level_hierarchy(self, fail_fast=False):
        """
        Check for groups with more than one level of hierarchy in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        return alias_api.get_nesting_groups()

    @sgtk.LogManager.log_timing
    def fix_group_has_single_level_hierarchy(self, errors=None):
        """
        Process all nodes in the current stage, or the specified group nodes, and flatten each node such that
        it only has a single levele of hierarchy (e.g. parent->child but not parent->child->grandchild)

        NOTE that the groups in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The list of group nodes to process, if None, all nodes in the
                              current stage will be processed. Default=None
        :type errors: str | list<str> | list<AlLayer> | list<dict>

        :raises alias_api.AliasPythonException: if failed to flatten all groups
        """

        status = alias_py.utils.success_status()

        if errors:
            if isinstance(errors, six.string_types):
                errors = [errors]
            elif isinstance(errors, list):
                for i, error_item in enumerate(errors):
                    if isinstance(error_item, dict):
                        errors[i] = error_item["name"]

            groups_to_flatten = []
            for group_node in errors:
                if isinstance(group_node, six.string_types):
                    group_node = alias_api.find_dag_node_by_name(group_node)

                if not group_node:
                    continue

                groups_to_flatten.append(group_node)
                flatten_status = alias_api.flatten_group_nodes(groups_to_flatten)
                if flatten_status != alias_py.utils.success_status():
                    status = flatten_status

        else:
            status = alias_api.flatten_group_nodes()

        if not alias_py.utils.is_success(status):
            alias_py.utils.raise_exception("Failed to flatten group nodes", status)

    @sgtk.LogManager.log_timing
    def check_locators(self, fail_fast=False):
        """
        Check for locators in the current stage.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all data errors found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        :rtype: list | bool
        """

        if fail_fast:
            has_locators = alias_py.utils.get_locators(check_exists=True)
            return not has_locators

        return alias_py.utils.get_locators()

    @sgtk.LogManager.log_timing
    def fix_locators(self, errors=None):
        """
        Process all locators in the current stage, or the specified locators, and delete them.

        :param errors: The list of locators to process, if None, all locators in current stage will
                              be processed. Default=None
        :type errors: str | list<str> | list<AlCurveOnSurface> | list<dict>

        :raises alias_api.AliasPythonException: if failed to delete locator object
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        if errors:
            for locator in errors:
                if isinstance(locator, six.string_types):
                    locator = alias_api.get_locator_by_name(locator)

                if locator:
                    status = locator.delete_object()
                    if not alias_py.utils.is_success(status):
                        alias_py.utils.raise_exception(
                            "Failed to delete locator", status
                        )
        else:
            status = alias_api.delete_all_locators()
            if not alias_py.utils.is_success(status):
                alias_py.utils.raise_exception("Failed to delete all locators", status)

    @sgtk.LogManager.log_timing
    def check_refererences_exist(self, fail_fast=False):
        """
        Check for referenced geometry in the current stage.

        :param fail_fast: Not applicable, but keep this param to follow guidelines for check functions.
        :type fail_fast: bool

        :return: A tuple containing:
                    (1) True if the check passed, else False
                    (2) A list pertaining to the data errors found dict with required keys: id, name This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function This will be an empty dict if fail_fast=False
        :rtype: tuple<bool,list,list,dict>
        """

        return alias_api.get_references()

    @sgtk.LogManager.log_timing
    def fix_references_exist(self, errors=None):
        """
        Process all references, or the specificed references, and remove all referneces from the current
        stage.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The list of references to process, if None, all references in the
                              current stage will be processed. Default=None
        :type errors: str | list<str> | list<AlReferenceFile> | list<dict>

        :raises alias_api.AliasPythonException: if failed to remove a reference
        """

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        references = errors or alias_api.get_references()

        for reference in references:
            if isinstance(reference, six.string_types):
                reference = alias_api.get_reference_by_name(reference)

            if reference:
                status = alias_api.remove_reference(reference)
                if not alias_py.utils.is_success(status):
                    alias_py.utils.raise_exception("Failed to remove reference", status)

    # -------------------------------------------------------------------------------------------------------
    # Pick Functions
    # -------------------------------------------------------------------------------------------------------
    #   These can be executed directly, but they are meant to be used as a validation rule item callback
    #   to help fix an invalid item which cannot be automatically fixed.
    #
    #   Guidelines to defining a pick function:
    #       - Function name should be prefixed with `pick_`
    #       - Takes an optional single parameter `errors` which are the items intended to be picked
    #           (the naming of the parameter is important since this is passed from the check function
    #           return value)
    # -------------------------------------------------------------------------------------------------------

    @sgtk.LogManager.log_timing
    def pick_nodes(self, errors=None):
        """
        Pick the nodes.

        :param errors: The node(s) to pick.
        :type errors: str | AlDagNode | list<str> | list<AlDagNode> | list<dict>
        """

        if not errors:
            return

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        alias_py.pick_list.pick_nodes(errors)

    @sgtk.LogManager.log_timing
    def pick_curves_on_surface_from_nodes(self, errors=None):
        """
        Pick the curves on surface.

        :param errors: The node(s) to pick curves on surface from.
        :type errors: str | AlDagNode | list<str> | list<AlDagNode> | list<dict>
        """

        if not errors:
            return

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        alias_py.pick_list.pick_curves_on_surface_from_nodes(errors)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_shaders(self, errors=None):
        """
        Pick the nodes assigned to the shaders.

        :param errors: The shaders to get assigned nodes to pick.
        :type errors: str | list<str> | list<AlShader> | list<dict>
        """

        errors = errors or alias_api.get_shaders()

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        alias_py.pick_list.pick_nodes_assigned_to_shaders(errors)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_layers(self, errors=None):
        """
        Pick the nodes assigned to the layers.

        :param errors: The layers to get assigned ndoes to pick.
        :type errors: str | list<str> | list<AlLayer> | list<dict>
        """

        errors = errors or alias_api.get_layers()

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        alias_py.pick_list.pick_nodes_assigned_to_layers(errors)

    @sgtk.LogManager.log_timing
    def pick_layers(self, errors=None):
        """
        Pick the layers.

        :param errors: The layers to pick.
        :type errors: str | list<str> | list<AlLayer> | list<dict>
        """

        errors = errors or alias_api.get_layers()

        if isinstance(errors, six.string_types):
            errors = [errors]
        elif isinstance(errors, list):
            for i, error_item in enumerate(errors):
                if isinstance(error_item, dict):
                    errors[i] = error_item["name"]

        alias_py.pick_list.pick_layers(errors)

    @sgtk.LogManager.log_timing
    def pick_locators(self, errors=None):
        """
        Pick the locators.

        :param errors: The locators to pick. If None, all locators will be picked.
        :type errors: str | list<str> | list<AlLocator> | list<dict>
        """

        if not errors:
            alias_py.pick_list.pick_locators(None, pick_all=True)

        else:
            if isinstance(errors, six.string_types):
                errors = [errors]
            elif isinstance(errors, list):
                for i, error_item in enumerate(errors):
                    if isinstance(error_item, dict):
                        errors[i] = error_item["name"]

            alias_py.pick_list.pick_locators(errors)

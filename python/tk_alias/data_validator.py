# Copyright (c) 2024 Autodesk Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk Inc.


from typing import TypeVar, List, Union, Optional, Any, Tuple
from .alias_py.al_typing import (
    AlSetList,
    AlDagNodeList,
    AlObjectTypeList,
    AlShaderList,
    AlReferenceFileList,
    AlLocatorList,
    AlLayerList,
    TraverseDagOutputData,
)

import sgtk
from tank.util import sgre as re


# Convenience types
AlDagNodeErrors = TypeVar(
    "AlDagNodeErrors", bool, Tuple[bool, int], List[str], List[dict], AlDagNodeList
)
AlShaderErrors = TypeVar("AlShaderErrors", List[str], List[dict], AlShaderList)
AlLayerErrors = TypeVar("AlLayerErrors", List[str], List[dict], AlLayerList)
AlSetErrors = TypeVar("AlSetErrors", List[str], List[dict], AlSetList)
AlLocatorErrors = TypeVar("AlLocatorErrors", List[str], List[dict], AlLocatorList)


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

    class AliasDataValidatorError(Exception):
        """Base class for AliasDataValidator exceptions."""

    #
    # Alias defaults
    #
    DEFAULT_LAYER_NAME = "DefaultLayer"
    DEFAULT_SHADER_NAME = "DefaultShader"

    def __init__(self, engine):
        """Initialize the AliasDataValidator object."""

        # Use the engine api instead of importing since the module may not be ready to be
        # imported at the time that this class is imported
        self.alias_py = engine.alias_py

        self._camera_node_types = self.alias_py.py_utils.camera_node_types()
        self._light_node_types = self.alias_py.py_utils.light_node_types()

        # The maximum number of errors to return for a validation check. If
        # count exceeds this value, the validation check will only return True
        # or False to indicate if errors were found. This is to help
        # performance of the validation operations.
        self._max_error_count = engine.get_setting(
            # "data_validation_max_error_count", 1000
            "data_validation_max_error_count",
            1000,
        )

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
                "name": "Delete unused shaders",
                "description": """Check: Unused shaders<br/>
                                Fix: Delete. DefaultShader is not affected.""",
                "error_msg": "Found unused shaders",
                "check_func": self.check_shader_unused,
                "fix_func": self.fix_shader_unused,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete unused shaders.",
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_shader_unused,
                    },
                ],
                "get_kwargs": lambda: {"skip_shaders": [self.DEFAULT_SHADER_NAME]},
                "dependency_ids": [
                    "node_instances",
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "shader_is_vred_compatible": {
                "name": "Only use VRED shaders",
                "description": """Check: Shaders are from the Asset Library (VRED-compatible)<br/>
                                Fix: You must assign shaders from the Asset Library. DefaultShader is not affected.""",
                "check_func": self.check_shader_is_vred_compatible,
                "error_msg": "Found shader(s) that are incompatible with VRED.",
                "actions": [
                    {
                        "name": "Select all shader geometry",
                        "callback": self.pick_nodes_assigned_to_shaders,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Select shader geometry",
                        "callback": self.pick_nodes_assigned_to_shaders,
                    },
                ],
                "get_kwargs": lambda: {"skip_shaders": [self.DEFAULT_SHADER_NAME]},
            },
            "node_is_null": {
                "name": "Delete null nodes",
                "description": """Check: Null nodes<br/>
                                Action: Delete""",
                "fix_func": self.fix_node_is_null,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all null nodes.",
                "warn_msg": 'This validation does not return a status. To ensure all null nodes are deleted, select "Delete All" or "Fix All."',
                "dependency_ids": [
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "node_has_construction_history": {
                "name": "Delete construction history",
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
                        self.alias_py.AlObjectType.GroupNodeType,
                        self.alias_py.AlObjectType.CurveNodeType,
                        self.alias_py.AlObjectType.FaceNodeType,
                        self.alias_py.AlObjectType.TextureNodeType,
                    ],
                },
            },
            # NOTE the fix function for Convert Instances will crash in some versions of Alias
            "node_instances": {
                "name": "Convert instances to geometry",
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
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "node_pivots_at_origin": {
                "name": "Reset pivots to global origin",
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
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
                "get_kwargs": lambda: {
                    "skip_node_types": [
                        self.alias_py.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ]
                },
            },
            "node_has_zero_transform": {
                "name": "Zero transforms",
                "description": """Check: Non-zero transformations<br/>
                                Action: Sets transformations to 0.0 on each node and DAG node. Camera, light, and texture nodes are not affected.""",
                "check_func": self.check_node_has_zero_transform,
                "fix_func": self.fix_all_node_has_zero_transform,
                "fix_name": "Reset All",
                "fix_tooltip": "Reset all transforms to zero. Camera, light, and texture nodes are not affected.",
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
                        self.alias_py.AlObjectType.TextureNodeType,
                        self.alias_py.AlObjectType.GroupNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ]
                },
                "dependency_ids": [
                    "node_instances",
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "node_is_not_in_layer": {
                "name": "Specific nodes must not be in the DefaultLayer",
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
                        self.alias_py.AlObjectType.GroupNodeType,
                        self.alias_py.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ],
                },
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "node_is_in_layer": {
                "name": "Specific nodes must be in the DefaultLayer",
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
                        self.alias_py.AlObjectType.TextureNodeType,
                        *self._camera_node_types,
                        *self._light_node_types,
                    ],
                },
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "node_name_matches_layer": {
                "name": "Match layer and assigned nodes' names",
                "description": """Check: Layer and top node names<br/>
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
                "dependency_ids": [
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                    "layer_has_single_object",
                    "node_layer_matches_parent",
                ],
            },
            "node_layer_matches_parent": {
                "name": "Node layer matches parent layer",
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
                "name": "Top-level DAG nodes",
                "description": """Check: DAG top-level nodes<br/>
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
                        self.alias_py.AlObjectType.CurveNodeType,
                        self.alias_py.AlObjectType.FaceNodeType,
                        self.alias_py.AlObjectType.SurfaceNodeType,
                        self.alias_py.AlObjectType.GroupNodeType,
                    ],
                },
            },
            "node_templates": {
                "name": "Delete templates",
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
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "cos_unused": {
                "name": "Delete unused curve-on-surfaces (COS)",
                "description": """Check: Unused curve-on-surfaces (COS)<br/>
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
                        "name": "Select Node",
                        "callback": self.pick_nodes,
                    },
                ],
                "dependency_ids": [
                    "cos_construction_history",
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "cos_construction_history": {
                "name": "Delete unused curve-on-surfaces (COS) construction history",
                "description": """Check: Unused curve-on-surfaces (COS) with construction history<br/>
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
                        "callback": self.fix_curve_on_surface_construction_history,
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
                "name": "Delete curves",
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
                "dependency_ids": ["node_has_construction_history"],
            },
            "set_empty": {
                "name": "Delete empty selection sets",
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
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "group_has_single_level_hierarchy": {
                "name": "Only one level per group",
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
                    "curves",
                    "node_has_construction_history",
                    "layer_has_single_object",
                ],
            },
            "layer_is_empty": {
                "name": "Delete empty layers and layer folders",
                "description": """Check: Empty layers and layer folders<br/>
                                Fix: Delete. DefaultLayer is not affected.""",
                "check_func": self.check_layer_is_empty,
                "fix_func": self.fix_layer_is_empty,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete empty layers and layer folders",
                "error_msg": "Found empty layers or layer folders",
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
                "dependency_ids": [
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                ],
            },
            "layer_has_single_shader": {
                "name": "Layer has single shader",
                "description": """Check: Layer members' shaders""",
                "check_func": self.check_layer_has_single_shader,
                "error_msg": "Found layer(s) using multiple shaders.",
                "actions": [
                    {
                        "name": "Select All",
                        "callback": self.pick_layers,
                    },
                    {
                        "name": "Select Layer Geometry",
                        "callback": self.pick_nodes_assigned_to_layers,
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
                    "curves",
                    "node_has_construction_history",
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                ],
            },
            "layer_symmetry": {
                "name": "Turn off layer symmetry for all layers",
                "description": """Check: Layer symmetry<br/>
                                Fix: Turn off symmetry on all layers. DefaultLayer is not affected.""",
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
                "name": "Layer has single item",
                "description": """Check: Layer members<br/>
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
                    {
                        "name": "Select Layer Geometry",
                        "callback": self.pick_nodes_assigned_to_layers,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Collapse",
                        "callback": self.fix_layer_has_single_object,
                    },
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
                    "node_has_zero_transform",
                    "node_instances",
                    "node_is_null",
                    "curves",
                    "node_has_construction_history",
                    "node_is_in_layer",
                    "node_is_not_in_layer",
                ],
            },
            "locators": {
                "name": "Delete locators",
                "description": """Check: Locators<br/>
                                Fix: Delete including annotate locators.""",
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
                "name": "Delete metadata",
                "description": "Check: Metadata",
            },
            "references_exist": {
                "name": "Remove referenced geometry",
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
    def check_shader_unused(
        self,
        fail_fast: Optional[bool] = False,
        skip_shaders: Optional[List[str]] = None,
    ) -> AlShaderList:
        """
        Check for unused shaders (shaders that are not assigned to any geometry) in Alias.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_shaders: The specified shaders (by name) will not be checked.

        :return: The shaders that are not being used.
        """

        skip_shaders = skip_shaders or []
        shaders = [
            shader
            for shader in self.alias_py.get_shaders()
            if shader.get_name() not in skip_shaders
        ]
        # Perform batch operation to check which shaders are used. This is
        # faster than iterating one by one.
        with self.alias_py.request_context_manager() as manager:
            for shader in shaders:
                shader.is_used()
        # Return the unused shaders based on the manager result
        return [shaders[i] for i, is_used in enumerate(manager.result) if not is_used]

    @sgtk.LogManager.log_timing
    def fix_shader_unused(
        self,
        errors: Optional[Union[str, dict, List[str], List[dict]]] = None,
        skip_shaders: List[str] = None,
    ):
        """
        Process all shaders in Alias, or the specified shaders, and delete all unused shaders.

        When passing the `errors` parameter, the onus is on the caller to ensure
        that the shaders are not in use. This is meant to be used when the
        caller has performed the corresponding check function before calling this
        function, which then it already has the up-to-date list of unused shaders.

        NOTE that the shaders list in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to see the
        updated shaders list.

        :param errors: (optional) The shaders to process, if None, all shaders
            will be processed. If not None, the shaders will not be validated
            that they are unused, and will be deleted regardless. Default is
            None.
        :param skip_shaders: The specified shaders (by name) will not be fixed.
            This will be ignored if the `errors` parameter is not None.
        """

        if errors:
            # Delete the given list of shaders. The onus is on the caller to
            # ensure that the shaders are not in use.
            unused_shaders = self.__parse_errors(errors)
            if self.__is_str_list(unused_shaders):
                unused_shaders = self.alias_py.get_shaders_by_name(unused_shaders)
        else:
            # Find all unused shaders. This will take longer, but ensures that
            # all currently unused shaders are deleted.
            unused_shaders = self.check_shader_unused(skip_shaders=skip_shaders)

        # Delete all the unsused shaders at once
        status = self.alias_py.delete_all(unused_shaders)
        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed delete all unused shaders.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_shader_is_vred_compatible(
        self,
        fail_fast: Optional[bool] = False,
        skip_shaders: Optional[Union[List[str]]] = None,
    ) -> AlShaderList:
        """
        Check for non-VRED shaders used in the current stage.

        A non-VRED shader is a shader that is not from the Asset Library
        (compaitible with VRED). Only shaders that are in use will be checked
        (e.g. if there is a non-VRED shader but is not used, it will not cause
        this check to fail).

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_shaders: The specified shaders (by name) will not be checked.

        :return: The list of shader objects that are incompatible with VRED.
        """

        skip_shaders = skip_shaders or []

        # First, get all the shaders in use
        shaders = [
            shader
            for shader in self.alias_py.get_shaders()
            if shader.get_name() not in skip_shaders
        ]
        # Perform batch operation to check which shaders are used. This is
        # faster than iterating one by one.
        with self.alias_py.request_context_manager() as manager:
            for shader in shaders:
                shader.is_used()
        # Return the unused shaders based on the manager result
        used_shaders = [
            shaders[i] for i, is_used in enumerate(manager.result) if is_used
        ]
        # Perform batch operation to check which shaders are VRED compatible.
        with self.alias_py.request_context_manager() as manager:
            for shader in used_shaders:
                self.alias_py.is_copy_of_vred_shader(shader)
        # Return the incompatible vred shaders based on the manager result
        return [
            used_shaders[i]
            for i, is_compatible in enumerate(manager.result)
            if not is_compatible
        ]

    @sgtk.LogManager.log_timing
    def fix_node_is_null(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Delete all null nodes.

        When passing the `errors` parameter, the onus is on the caller to ensure
        that the nodes are null. This is meant to be used when the caller has
        performed the corresponding check function before calling this function,
        which then it already has the up-to-date list of null nodes.

        :param errors: The nodes to delete, if None, all nodes in the current
            stage will be processed. If passed, the nodes will not be checked
            and will assume to be null and deleted. Default is None.
        """

        if errors is None:
            self.alias_py.delete_null_nodes()
        else:
            # Delete the given list of nodes. The onus is on the caller to
            # ensure that the nodes are null.
            null_nodes = self.__parse_errors(errors)
            if self.__is_str_list(null_nodes):
                status = self.alias_py.delete_dag_nodes_by_name(null_nodes)
            else:
                status = self.alias_py.delete_all(null_nodes)
            if not self.alias_py.py_utils.is_success(status):
                self.alias_py.py_utils.raise_exception(
                    "Failed delete all null nodes.",
                    status,
                )

    @sgtk.LogManager.log_timing
    def check_node_has_construction_history(
        self,
        fail_fast: Optional[bool] = False,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ) -> AlDagNodeList:
        """
        Check for nodes with construction history in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_node_types: The specified node types will not be checked.

        :return: The list of nodes that have construction history.
        """

        skip_node_types_set = set(skip_node_types or [])
        return self.alias_py.py_dag_node.get_nodes_with_construction_history(
            skip_node_types=skip_node_types_set,
        )

    @sgtk.LogManager.log_timing
    def fix_node_has_construction_history(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        skip_node_types: Optional[Union[AlObjectTypeList]] = None,
    ):
        """
        Delete construction history for the specified nodes.

        When passing the `errors` parameter, the onus is on the caller to ensure
        that the nodes have construction history. This is meant to be used when the
        caller has performed the corresponding check function before calling this
        function, which then it already has the up-to-date list of nodes with
        construction history. Nodes given in the `errors` parameter will not be
        checked and will assume to have construction history and be deleted.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated data.

        :param errors: (optional) The nodes to process, if None, all nodes in the current stage will
                       be processed. Default=None
        :param skip_node_types: The specified node types will not be checked.
        """

        skip_node_types_set = set(skip_node_types or [])

        if errors:
            # Assumes the nodes given has history. Onus is on the caller to
            # ensure the nodes have construction history.
            nodes = self.__parse_errors(errors)
            if self.__is_str_list(nodes):
                nodes = self.alias_py.get_dag_nodes_by_name(nodes)
        else:
            nodes = self.alias_py.py_dag_node.get_nodes_with_construction_history(
                nodes=errors,
                skip_node_types=skip_node_types_set,
            )

        self.alias_py.delete_history(nodes)

    @sgtk.LogManager.log_timing
    def check_node_instances(
        self,
        fail_fast: Optional[bool] = False,
    ) -> Union[bool, AlDagNodeList, Tuple[bool, int]]:
        """
        Check for instanced nodes in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: True if the check passes (e.g. no instanced nodes), otherwise
            the list of instanced nodes if the number of instanced nodes is less
            then or equal to the maximum number of nodes allowed to return,
            otherwise a tuple of False and the number of instanced nodes.
        """

        result = self.alias_py.py_dag_node.get_instanced_nodes(return_nodes=False)
        return self.__return_node_result(result)

    @sgtk.LogManager.log_timing
    def fix_node_instances(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Remove instanced nodes.

        When passing the `errors` parameter, the onus is on the caller to ensure
        that the nodes are instanced. This is meant to be used when the caller
        has performed the corresponding check function before calling this
        function, which then it already has the up-to-date list of nodes are
        instanced. Nodes given in the `errors` parameter will not be checked and
        will assume to be instanced and be deleted.

        NOTE that the nodes in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to
        see the updated data.

        :param errors: The list of nodes to process, if None, all nodes in the
            current stage will be processed. Default is None.
        """

        if errors:
            # Assumes the nodes given are instanced. Onus is on the caller to
            # ensure the nodes are instanced.
            nodes = self.__parse_errors(errors)
            if not self.__is_str_list(nodes):
                nodes = [node.get_name() for node in nodes]
            input_data = self.alias_py.TraverseDagInputData(set(nodes), True)

        else:
            input_data = self.alias_py.TraverseDagInputData()

        expand = True
        result = self.alias_py.search_node_is_instance(input_data, expand)
        status = result.status
        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed to expand all node instances.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_node_pivots_at_origin(
        self,
        fail_fast: Optional[bool] = False,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ) -> AlDagNodeList:
        """
        Check for nodes that do not have their pivots set to the origin.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The nodes that do not have their pivots set to the origin.
        """

        skip_node_types_set = set(skip_node_types or [])
        result = self.alias_py.py_dag_node.get_nodes_with_non_origin_pivot(
            skip_node_types=skip_node_types_set, return_nodes=False
        )
        return self.__return_node_result(result)

    @sgtk.LogManager.log_timing
    def fix_node_pivots_at_origin(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ):
        """
        Reset scale and rotate pivots to the origin for the specified nodes.

        NOTE that the pivots Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to
        see the updated pivots.

        :param errors: The nodes to process, if None, all nodes in the current
            stage will be processed. Default is None.
        """

        if errors:
            nodes = self.__parse_errors(errors)
            status = self.alias_py.reset_pivots(nodes)
        else:
            skip_node_types_set = set(skip_node_types or [])
            input_data = self.alias_py.TraverseDagInputData(
                skip_node_types_set,
                False,
            )
            reset = True
            result = self.alias_py.search_node_has_non_origin_pivot(input_data, reset)
            status = result.status

        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed to reset all pivots to origin",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_node_has_zero_transform(
        self,
        fail_fast: Optional[bool] = False,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ) -> AlDagNodeList:
        """
        Check for nodes wtih non-zero transforms.

        Only top-level dag nodes will be returned.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_node_types: The specified node types will not be checked.

        :return: The nodes with non-zero transforms.
        """

        skip_node_types_set = set(skip_node_types or [])
        result = self.alias_py.py_dag_node.get_nodes_with_non_zero_transform(
            skip_node_types=skip_node_types_set, top_level_only=True, return_nodes=False
        )
        return self.__return_node_result(result)

    @sgtk.LogManager.log_timing
    def fix_all_node_has_zero_transform(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ):
        """
        Reset transforms to zero for all nodes.

        :param errors: This param is ignored, though it is required to be
            defiend for this function to be a data validation fix callback.
        :param skip_node_types: This param is ignored, though it is required to
            be defiend for this function to be a data validation fix callback.
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        self.fix_node_has_zero_transform(errors=None)

    @sgtk.LogManager.log_timing
    def fix_node_has_zero_transform(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
    ):
        """
        Reset node transforms to zero.

        NOTE that the nodes Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function,
        to see the updated node transforms.

        :param errors: The nodes to process, if None, all nodes in the current
            stage will be processed. Default is None.
        :param skip_node_types: This param is ignored, though it is required to
            be defiend for this function to be a data validation fix callback.
        """

        if errors:
            nodes = self.__parse_errors(errors)
            if not self.__is_str_list(nodes):
                nodes = [node.get_name() for node in nodes]
            input_data = self.alias_py.TraverseDagInputData(set(nodes), True)
            result = self.alias_py.search_node_has_non_zero_transform(
                input_data,
                top_level_only=False,
                reset=True,
            )
            status = result.status
        else:
            status = self.alias_py.zero_transform_top_level()

        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed to apply zero transform to nodes. Returned status:",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_node_is_not_in_layer(
        self,
        fail_fast: Optional[bool] = False,
        layer_name: Optional[str] = None,
        accept_node_types: Optional[AlObjectTypeList] = None,
    ) -> Union[bool, AlDagNodeList]:
        """
        Check that the layer contains only nodes of type in the accepted list.

        :param fail_fast: Set to True to return immediately as soon as the
            check fails. Set to False to check entire data and return all data
            errors found, and arguments that can be passed to the corresponding
            fix function. Note that when set to False, this function will be
            slower to execute.
        :param layer_name: The layer to check node membership. Default is
            "DefaultLayer".
        :param accept_node_types: Only the specified node types are accepted in
            the layer.

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        """

        layer_name = layer_name or self.DEFAULT_LAYER_NAME
        accept_node_types = accept_node_types or []

        layer = self.alias_py.get_layer_by_name(layer_name)
        if layer is None:
            self.alias_py.py_utils.raise_exception(f"Layer '{layer_name}' not found.")

        # NOTE get_assigned_nodes will not return the group nodes, only leaf
        # nodes assigned to the layer
        nodes = layer.get_assigned_nodes()

        invalid_nodes = []
        for node in nodes:
            if node.get_type() not in accept_node_types:
                if fail_fast:
                    return False
                invalid_nodes.append(node)
        return invalid_nodes

    @sgtk.LogManager.log_timing
    def check_node_is_in_layer(
        self,
        fail_fast: Optional[bool] = False,
        layer_name: Optional[str] = None,
        accept_node_types: Optional[AlObjectTypeList] = None,
        force_return_errors: Optional[bool] = False,
    ) -> AlDagNodeErrors:
        """
        Check that the specified node types are in the layer.

        The whole DAG will be traversed to find nodes that are incorrectly
        placed in a layer that is not the specified layer.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param layer_name: The layer that the specified node types belong to.
            Default is "DefaultLayer".
        :param accept_node_types: The node types that must only be in the layer.
        :param force_return_errors: If True, the function will return the list
            of errors found, else the list of errors will only be returned if
            the number of errors is less than or equal to the maximum number of
            errors allowed to return. Default is False.

        :return: The list of Alias objects that that failed the check.
        """

        layer_name = layer_name or self.DEFAULT_LAYER_NAME
        layer = self.alias_py.get_layer_by_name(layer_name)
        if not layer:
            raise self.AliasDataValidatorError(f"Layer '{layer_name}' not found.")

        accept_node_types = set(accept_node_types or [])

        # Traverse the DAG to look for nodes that should be in the default layer, but are not.
        input_data = self.alias_py.TraverseDagInputData(
            layer, False, accept_node_types, True
        )
        result = self.alias_py.search_dag(input_data)
        return self.__return_node_result(result, force_return_errors)

    @sgtk.LogManager.log_timing
    def fix_node_is_in_layer(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        layer_name: Optional[str] = None,
        accept_node_types: Optional[AlObjectTypeList] = None,
    ):
        """
        Move nodes of the specified node type to the specified layer.

        If the `errors` parameter is not None, the onus is on the caller to
        ensure that the nodes given should be moved to the layer. This is meant
        to be used when the caller has performed the corresponding check function
        before calling this function, which then it already has the up-to-date
        list of nodes that should be moved to the layer. Nodes given in the
        `errors` parameter will not be checked and will assume to be moved to
        the layer.

        :param errors: The nodes to move to the layer, if None, all nodes in the
            will be checked and moved to the layer, if necessary. Default is
            None.
        :param layer_name: The layer that the specified node types belong to.
            Default is "DefaultLayer".
        :param accept_node_types: The node types that must only be in the layer.
        """

        layer_name = layer_name or self.DEFAULT_LAYER_NAME

        if errors:
            nodes = self.__parse_errors(errors)
        else:
            nodes = self.check_node_is_in_layer(
                layer_name=layer_name,
                accept_node_types=accept_node_types,
                force_return_errors=True,
            )

        status = self.alias_py.assign_nodes_to_layer(nodes, layer_name)

        if status == self.alias_py.AlStatusCode.Failure:
            raise self.AliasDataValidatorError(
                "Failed to move all nodes to layer.",
                status,
            )
        elif status == self.alias_py.AlStatusCode.InvalidArgument:
            raise self.AliasDataValidatorError(f"Layer '{layer_name}' not found ")

    @sgtk.LogManager.log_timing
    def check_node_name_matches_layer(
        self, fail_fast: Optional[bool] = False, skip_layers: Optional[List[str]] = None
    ) -> AlDagNodeList:
        """
        Check for naming mismatches between layer and its nodes, for all
        top-level nodes.

        Each layer should only contain one group (or one surface). This group is
        named after the layer. If groups are found that don't match the name of
        the layer, an error is thrown.

        :param fail_fast: Set to True to return immediately as soon as the check
            fails. Set to False to check entire data and return all data errors
            found, and arguments that can be passed to the corresponding fix
            function. Note that when set to False, this function will be slower
            to execute.
        :param skip_layers: The specified layers (by name) will not be checked.

        :return: If fail_fast is True, a bool indicating if the check succeeded
            is returned, else the list of Alias objects that that failed the
            check is returned.
        """

        invalid_nodes = []
        nodes = self.alias_py.get_top_dag_nodes()

        layers = self.alias_py.get_layers(nodes)
        # with self.alias_py.request_context_manager() as manager:
        #     for node in nodes:
        #         node.layer()

        # for i, layer in enumerate(manager.result):
        for i, layer in enumerate(layers):
            if not layer or (skip_layers and layer.get_name() in skip_layers):
                continue

            # Get the node for the layer
            node = nodes[i]

            # Check the layer and node names match, which means they are the same or the ndoe name is the
            # layer name plus the suffix "#n" where 'n' is a number.
            reg = r"^{}(#?\d)*$".format(layer.get_name())
            if not re.match(reg, node.get_name()):
                if fail_fast:
                    return False
                invalid_nodes.append(node)

        return invalid_nodes

    @sgtk.LogManager.log_timing
    def fix_node_name_matches_layer(
        self,
        errors: Optional[AlDagNodeErrors] = None,
        skip_layers: Optional[List[str]] = None,
    ):
        """
        Rename nodes to match their layer.

        If the `errors` parameter is not None, the onus is on the caller to
        ensure that the nodes given should be renamed to match their layer. This
        is meant to be used when the caller has performed the corresponding check
        function before calling this function, which then it already has the
        up-to-date list of nodes that should be renamed. Nodes given in the
        `errors` parameter will not be checked and will assume to be renamed to
        match their layer.

        :param errors: The nodes to rename, if None, all nodes will be checked
            and renamed to match their layer. Default is None.
        :param skip_layers: Nodes in the specified layers (by name) will not be fixed.
        """

        if errors:
            nodes = self.__parse_errors(errors)
            if self.__is_str_list(nodes):
                nodes = self.alias_py.get_dag_nodes_by_name(nodes)
        else:
            nodes = self.check_node_name_matches_layer(
                fail_fast=False, skip_layers=skip_layers
            )

        # Get all layers in at once
        layers = self.alias_py.get_layers(nodes)
        # with self.alias_py.request_context_manager() as manager:
        #     for node in nodes:
        #         node.layer()

        # Rename all nodes at once
        with self.alias_py.request_context_manager():
            # for i, layer in enumerate(manager.result):
            for i, layer in enumerate(layers):
                if not layer:
                    continue
                # Get the node for the layer
                node = nodes[i]
                node_layer_name = layer.get_name()
                reg = r"^{}(#?\d)*$".format(node_layer_name)
                if not re.match(reg, node.get_name()):
                    node.name = node_layer_name

    @sgtk.LogManager.log_timing
    def check_node_layer_matches_parent(
        self,
        fail_fast: Optional[bool] = False,
        force_return_errors: Optional[bool] = False,
    ) -> AlDagNodeErrors:
        """
        Check for nodes that do not have the layer as their parent node.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param force_return_errors: If True, the function will return the list
            of errors found, else the list of errors will only be returned if
            the number of errors is less than or equal to the maximum number of
            errors allowed to return. Default is False.

        :return: The errors found.
        """

        input_data = self.alias_py.TraverseDagInputData()
        result = self.alias_py.search_node_layer_does_not_match_parent_layer(
            input_data, return_parent=True
        )
        return self.__return_node_result(result, force_return_errors)

    @sgtk.LogManager.log_timing
    def fix_node_layer_matches_parent(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Move nodes to the layer of their parent node.

        If the `errors` parameter is not None, the onus is on the caller to
        ensure that the nodes given should be moved to the layer of their parent
        node. This is meant to be used when the caller has performed the
        corresponding check function before calling this function, which then it
        already has the up-to-date list of nodes that should be moved to the
        layer of their parent node. Nodes given in the `errors` parameter will
        not be checked and will assume to be moved to the layer of their parent
        node.

        :param errors: The nodes to move to the layer of their parent node, if
            None, all nodes will be checked and moved to the layer of their
            parent node. Default is None.
        """

        if errors:
            parent_nodes = self.__parse_errors(errors)
        else:
            parent_nodes = self.check_node_layer_matches_parent(
                force_return_errors=True
            )

        status = self.alias_py.move_children_to_parent_layer(parent_nodes)
        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError(
                "Failed to move all nodes to their parent layer.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_node_dag_top_level(
        self,
        fail_fast: Optional[bool] = False,
        accept_node_types: Optional[AlObjectTypeList] = None,
    ) -> Union[bool, AlDagNodeErrors]:
        """
        Check for invalid top-level nodes in the DAG of the current stage.

        :param fail_fast: Set to True to return immediately as soon as the
            check fails. Set to False to check entire data and return all data
            errors found, and arguments that can be passed to the corresponding
            fix function. Note that when set to False, this function will be
            slower to execute.
        :param accept_node_types: Only the specified node types are accepted in
            the top level of the DAG.

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        """

        accept_node_types = accept_node_types or []
        nodes = self.alias_py.get_top_dag_nodes()
        invalid_nodes = []
        for node in nodes:
            if node.get_type() not in accept_node_types:
                if fail_fast:
                    return False
                invalid_nodes.append(node)
        return invalid_nodes

    @sgtk.LogManager.log_timing
    def check_node_templates(
        self,
        fail_fast: Optional[bool] = False,
        force_return_errors: Optional[bool] = False,
    ) -> AlDagNodeErrors:
        """
        Check for nodes that are set as templates.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param force_return_errors: If True, the function will return the list
            of errors found, else the list of errors will only be returned if
            the number of errors is less than or equal to the maximum number of
            errors allowed to return. Default is False.

        :return: The errors found.
        """

        input_data = self.alias_py.TraverseDagInputData()
        result = self.alias_py.search_node_is_template(input_data)
        return self.__return_node_result(result, force_return_errors)

    @sgtk.LogManager.log_timing
    def fix_node_templates(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Delete the specified nodes that are set as templates.

        If `errors` is passed, the onus is on the caller to ensure that the
        nodes are templates. This is meant to be used when the caller has
        performed the corresponding check function before calling this function,
        which then it already has the up-to-date list of nodes that are
        templates. Nodes given in the `errors` parameter will not be checked and
        will assume to be deleted.

        :param errors: The template nodes to delete, if None, all template nodes
            in the current stage will be deleted. Default is None.
        """

        if errors:
            nodes = self.__parse_errors(errors)
        else:
            nodes = self.check_node_templates(force_return_errors=True)

        if self.__is_str_list(nodes):
            status = self.alias_py.delete_dag_nodes_by_name(nodes)
        else:
            status = self.alias_py.delete_all(nodes)

        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed delete all template nodes.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_node_curves(
        self,
        fail_fast: Optional[bool] = False,
        force_return_errors: Optional[bool] = False,
    ) -> AlDagNodeErrors:
        """
        Check for nodes that represent a curve (ie. AlCurveNode objects).

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The errors found.
        """

        result = self.alias_py.py_dag_node.get_nodes_by_type(
            [self.alias_py.AlObjectType.CurveNodeType],
            return_nodes=False,
        )
        return self.__return_node_result(result, force_return_errors)

    @sgtk.LogManager.log_timing
    def fix_node_curves(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Delete the curve nodes.

        If a list of nodes are passed in, they are assumed to represent a curve
        and will be deleted.

        :param errors: The list of nodes to process, if None, all nodes in the
            current stage will be processed. Default is None.
        """

        if errors:
            curve_nodes = self.__parse_errors(errors)
        else:
            curve_nodes = self.check_node_curves(force_return_errors=True)

        if self.__is_str_list(curve_nodes):
            status = self.alias_py.delete_dag_nodes_by_name(curve_nodes)
        else:
            status = self.alias_py.delete_all(curve_nodes)

        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed delete all curve nodes.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_curve_on_surface_unused(
        self,
        fail_fast: Optional[bool] = False,
        force_return_errors: Optional[bool] = False,
    ) -> AlDagNodeErrors:
        """
        Check for unused curves on surfaces in the current stage.

        This check wil return the nodes that contain the unused curves on
        surfaces, as the errors.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The errors found.
        """

        result = self.alias_py.py_dag_node.get_nodes_with_unused_curves_on_surface(
            return_nodes=False
        )
        return self.__return_node_result(result, force_return_errors)

    @sgtk.LogManager.log_timing
    def fix_curve_on_surface_unused(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Delete unused curves on surface for the specified nodes.

        :param errors: The nodes to delete unused curves on surface for. If
            None, all unused curves on surface will be deleted.
        """

        if errors:
            node_names = self.__parse_errors(errors)
            if not self.__is_str_list(node_names):
                node_names = [node.get_name() for node in node_names]
        else:
            node_names = []

        input_data = self.alias_py.TraverseDagInputData(set(node_names), True)
        result = self.alias_py.search_node_unused_curves_on_surface(
            input_data, delete_unused=True
        )
        status = result.status
        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError(
                "Failed to delete all unused curves on surface", status
            )

    @sgtk.LogManager.log_timing
    def check_curve_on_surface_construction_history(
        self, fail_fast: Optional[bool] = False
    ) -> AlDagNodeList:
        """
        Check for unused curves on surfaces that have construction history.

        NOTE: in newer versions of Alias, this check may not be needed if
        validation rule 'node_has_construction_history' is enabled.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The nodes that have unused curves on surface with construction
            history.
        """

        input_data = self.alias_py.TraverseDagInputData()
        result = self.alias_py.search_node_unused_curves_on_surface_with_history(
            input_data
        )
        return self.__return_node_result(result)

    @sgtk.LogManager.log_timing
    def fix_curve_on_surface_construction_history(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Delete construction history of unnused curves on surface.

        If `errors` is provided, only the nodes in the list will have their
        construction history deleted. The onus is on the caller to ensure that
        the nodes are unused curves on surface with construction history. They
        will not be checked, and will assume to be unused curves on surface with
        construction history and be deleted.

        :param errors: The nodes to delete construction history for unused curves
            on surface. If None, all construction history for unused curves on
            surface will be deleted.
        """

        if errors:
            node_names = self.__parse_errors(errors)
            if not self.__is_str_list(node_names):
                node_names = [node.get_name() for node in node_names]
        else:
            node_names = []

        input_data = self.alias_py.TraverseDagInputData(set(node_names), True)
        result = self.alias_py.search_node_unused_curves_on_surface_with_history(
            input_data, delete_unused=True
        )
        status = result.status
        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError(
                "Failed to delete all construction history for unused curves on surface",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_set_empty(self, fail_fast: Optional[bool] = False) -> AlSetList:
        """
        Check for sets that empty.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The empty sets.
        """

        return self.alias_py.get_empty_sets()

    @sgtk.LogManager.log_timing
    def fix_set_empty(
        self,
        errors: Optional[AlSetErrors] = None,
    ):
        """
        Delete all empty sets.

        If `errors` is provided, only the sets in the list will be deleted.
        The onus is on the caller to ensure that the sets are empty. They
        will not be checked, and will assume to be empty and be be deleted.

        :param errors: If provided, these sets will be deleted. If None, all
            empty sets found will be deleted. Default is None.
        """

        if errors:
            empty_sets = self.__parse_errors(errors)
        else:
            empty_sets = self.check_set_empty()

        if self.__is_str_list(empty_sets):
            status = self.alias_py.delete_sets_by_name(set(empty_sets))
        else:
            status = self.alias_py.delete_all(empty_sets)

        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError("Failed to delete all sets", status)

    @sgtk.LogManager.log_timing
    def check_layer_is_empty(
        self, fail_fast: Optional[bool] = False, skip_layers: Optional[List[str]] = None
    ) -> AlLayerList:
        """
        Check for empty layers and layer folders in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_layers: The specified layers (by name) will not be checked.

        :return: The empty layers.
        """

        skip_layers = set(skip_layers or [])
        include_folders = True
        return self.alias_py.get_empty_layers(include_folders, skip_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_is_empty(
        self,
        errors: Optional[AlLayerErrors] = None,
        skip_layers: Optional[List[str]] = None,
    ):
        """
        Process all layers in the current stage, or the list of layers if
        provided, and delete all the empty layers and layer folders.

        :param layers: The layers to process, if None, all layers in the current stage will
            be processed. Default is None.
        :param skip_layers: The specified layers (by name) will not be fixed.
        """

        if errors:
            empty_layers = self.__parse_errors(errors)
        else:
            empty_layers = self.check_layer_is_empty(skip_layers=skip_layers)

        if self.__is_str_list(empty_layers):
            status = empty_layers = self.alias_py.delete_layers_by_name(empty_layers)
        else:
            status = self.alias_py.delete_all(empty_layers)

        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError("Failed to delete all layers", status)

    @sgtk.LogManager.log_timing
    def check_layer_has_single_shader(
        self,
        fail_fast: Optional[bool] = False,
    ) -> AlLayerList:
        """
        Check that all nodes in a layer use the same single shader.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The layers that have more than one shader.
        """

        return self.alias_py.get_layers_using_multiple_shaders()

    @sgtk.LogManager.log_timing
    def check_layer_symmetry(
        self, fail_fast: Optional[bool] = False, skip_layers: Optional[List[str]] = None
    ) -> AlLayerList:
        """
        Check for layers with symmetry turned on in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.
        :param skip_layers: The specified layers (by name) will not be checked.

        :return: The layers with symmetry turned on.
        """

        return self.alias_py.py_layer.get_symmetric_layers(skip_layers=skip_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_symmetry(
        self,
        errors: Optional[AlLayerErrors] = None,
        skip_layers: Optional[List[str]] = None,
    ):
        """
        Process all layers in the current stage, or the specified layers, and
        turn off symmetry on layers.

        NOTE that the layers in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function,
        to see the updated layers.

        :param errors: The layers to process, if None, all layers in the current
            stage will be processed. Default=None
        :param skip_layers: The specified layers (by name) will not be fixed.
        """

        if errors:
            layers = self.__parse_errors(errors)
        else:
            layers = self.check_layer_symmetry(skip_layers=skip_layers)

        status = self.alias_py.set_layer_symmetry(layers, False)
        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed turn off all layer symmetry.",
                status,
            )

    @sgtk.LogManager.log_timing
    def check_layer_has_single_object(
        self,
        fail_fast: Optional[bool] = False,
        skip_layers: Optional[List[str]] = None,
    ) -> Union[AlLayerList, bool]:
        """
        Check for layers that contain more than one top-level node.

        Layers can only have a single node, for multiple nodes, they can have a
        group node that contains child nodes).

        :param fail_fast: Return immediately as soon as the check fails.
        :param skip_layers: The specified layers (by name) will not be checked.

        :return: If `fail_fast` is True, True is returned if the check is
            successful, else False. If `fail_fast` is False, the layers that
            have more than one top-level node are returned.
        """

        invalid_layers = []

        # Get all top dag nodes
        nodes = self.alias_py.get_top_dag_nodes()

        # Get layers for all top dag nodes at once
        with self.alias_py.request_context_manager() as manager:
            for node in nodes:
                node.layer()

        layer_names = [
            layer.get_name()
            for layer in manager.result
            if layer.get_name() not in skip_layers
        ]
        unique_layer_names = set(layer_names)

        # A layer is invalid if it appears more than once in the list of
        # layers, meaning that it has more than one top dag node
        is_valid = len(layer_names) == len(unique_layer_names)
        if fail_fast:
            return is_valid

        if is_valid:
            return []

        for layer_name in unique_layer_names:
            if layer_names.count(layer_name) > 1:
                invalid_layers.append(layer_name)
        return invalid_layers

    @sgtk.LogManager.log_timing
    def fix_layer_has_single_object(
        self,
        errors: Optional[AlLayerErrors] = None,
        skip_layers: Optional[List[str]] = None,
    ):
        """
        Ensure all layers have only a single top-level node.

        The layer contents will be grouped into a single group node if the layer
        has multiple top-level nodes. A new group will be created if the layer
        does not have any group nodes currently.

        NOTE that the layers in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function,
        to see the updated data.

        :param errors: The layers to ensure have only a single top-level node,
            if None, all layers in the current stage will be processed. Default
            is None.
        :param skip_layers: The specified layers (by name) will not be fixed.
            Ignored if `errors` is provided.
        """

        if errors:
            layers = self.__parse_errors(errors)
        else:
            layers = self.check_layer_has_single_object(
                fail_fast=False, skip_layers=skip_layers
            )

        if not self.__is_str_list(layers):
            layers = [layer.get_name() for layer in layers]

        # Get all top-level nodes
        top_level_nodes = self.alias_py.get_top_dag_nodes()

        # Get all layers for the top-level nodes
        with self.alias_py.request_context_manager() as manager:
            for node in top_level_nodes:
                node.layer()

        # Create mapping of layer to all their top-level nodes and group nodes
        layer_top_level_nodes_mapping = {}
        layer_group_nodes_mapping = {}
        for i, layer in enumerate(manager.result):
            layer_name = layer.get_name()
            if layer_name not in layers:
                continue  # Skip it

            node = top_level_nodes[i]
            layer_top_level_nodes_mapping.setdefault(layer_name, []).append(node)
            if self.alias_py.py_utils.is_group_node(node):
                layer_group_nodes_mapping.setdefault(layer_name, []).append(node)

        # Create mapping of layer to its single group node which all other nodes
        # will be moved to
        layers_to_create_group = []
        layer_group_node_mapping = {}
        for layer_name in layers:
            group_node = None
            layer_group_nodes = layer_group_nodes_mapping.get(layer_name, [])
            if not layer_group_nodes:
                # First case: no existing group node - create one
                layers_to_create_group.append(layer_name)
            else:
                # Second case: only one group node exist
                if len(layer_group_nodes) == 1:
                    group_node = layer_group_nodes[0]

                # Third case: more than one group node exists
                else:
                    # Try to get the one named after the layer, otherwise use the first one
                    for group in layer_group_nodes:
                        if group.get_name() == layer_name:
                            group_node = group
                            break
                    if not group_node:
                        group_node = layer_group_nodes[0]

            layer_group_node_mapping[layer_name] = group_node

        # Create new groups all at once
        with self.alias_py.request_context_manager() as manager:
            for layer_name in layers_to_create_group:
                self.alias_py.create_group_for_layer(layer_name, layer_name)
        for i, group_node in enumerate(manager.result):
            layer_name = layers_to_create_group[i]
            layer_group_node_mapping[layer_name] = group_node

        # Finally, move all top-level nodes to the layer's single group node
        with self.alias_py.request_context_manager() as manager:
            for layer_name in layers:
                layer_top_level_nodes = layer_top_level_nodes_mapping[layer_name]
                group_node = layer_group_node_mapping[layer_name]
                if not group_node:
                    raise self.AliasDataValidatorError(
                        "Failed to find group node for layer"
                    )
                children = [
                    node
                    for node in layer_top_level_nodes
                    if node.get_name() != group_node.get_name()
                ]
                # NOTE: if there are many children to add, this will be slow
                # because the Alias API is not optimized for this
                group_node.add_children(children)

        for status in manager.result:
            if not self.alias_py.py_utils.is_success(status):
                raise self.AliasDataValidatorError(
                    "Failed to ensure all layers have only a single top-level node",
                    status,
                )

    @sgtk.LogManager.log_timing
    def check_group_has_single_level_hierarchy(
        self, fail_fast: Optional[bool] = False
    ) -> AlDagNodeList:
        """
        Check for groups with more than one level of hierarchy in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The group nodes that have more than one level of hierarchy.
        """

        return self.alias_py.get_nesting_groups()

    @sgtk.LogManager.log_timing
    def fix_group_has_single_level_hierarchy(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        Flatten each node such that it only has a single levele of hierarchy.

        A node can have a child but not a grandchild.

        NOTE that the groups in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to
        see the updated data.

        :param errors: The group nodes to flatten, if None, all group nodes will
            be checked and flattened. Default is None.
        """

        if errors:
            group_nodes = self.__parse_errors(errors)
            if self.__is_str_list(group_nodes):
                group_nodes = self.alias_py.get_dag_nodes_by_name(group_nodes)
            status = self.alias_py.flatten_group_nodes(group_nodes)
        else:
            status = self.alias_py.flatten_group_nodes()

        if not self.alias_py.py_utils.is_success(status):
            raise self.AliasDataValidatorError("Failed to flatten group nodes", status)

    @sgtk.LogManager.log_timing
    def check_locators(
        self, fail_fast: Optional[bool] = False
    ) -> Union[bool, AlLocatorList]:
        """
        Check for locators in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: If fail_fast is True, a bool indicating if the check succeeded is returned,
            else the list of Alias objects that that failed the check is returned.
        """

        if fail_fast:
            has_locators = self.alias_py.py_utils.get_locators(check_exists=True)
            return not has_locators
        return self.alias_py.get_locators()

    @sgtk.LogManager.log_timing
    def fix_locators(
        self,
        errors: Optional[AlLocatorList] = None,
    ):
        """
        Process all locators in the current stage, or the specified locators,
        and delete them.

        :param errors: The list of locators to process, if None, all locators in
            current stage will be processed. Default is None.
        """

        if errors:
            locators = self.__parse_errors(errors)
            if self.__is_str_list(locators):
                locators = self.alias_py.get_locators()
            self.alias_py.delete_all(locators)
        else:
            status = self.alias_py.delete_all_locators()
            if not self.alias_py.py_utils.is_success(status):
                raise self.AliasDataValidatorError(
                    "Failed to delete all locators", status
                )

    @sgtk.LogManager.log_timing
    def check_refererences_exist(
        self, fail_fast: Optional[bool] = False
    ) -> AlReferenceFileList:
        """
        Check for referenced geometry in the current stage.

        :param fail_fast: DEPRECATED. This parameter is ignored.

        :return: The referenced geometry.
        """

        return self.alias_py.get_references()

    @sgtk.LogManager.log_timing
    def fix_references_exist(
        self,
        errors: Optional[AlReferenceFileList] = None,
    ):
        """
        Process all references, or the specificed references, and remove all
        referneces from the current stage.

        NOTE that the nodes in Alias may not update automatically,
        alias_api.redraw_screen() may need to be invoked after this function, to
        see the updated data.

        :param errors: The list of references to process, if None, all
            references in the current stage will be processed. Default is None.
        """

        if errors:
            references = self.__parse_errors(errors)
            if self.__is_str_list(references):
                references = self.alias_py.get_references_by_name(references)
        else:
            references = self.alias_py.get_references()

        status = self.alias_py.remove_references(references)
        if not self.alias_py.py_utils.is_success(status):
            self.alias_py.py_utils.raise_exception(
                "Failed to remove all references", status
            )

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
    def pick_nodes(self, errors: AlDagNodeErrors = None):
        """
        Pick the nodes.

        If `errors` are not given, nothing is picked.

        :param errors: The node(s) to pick.
        """

        if not errors:
            return

        nodes = self.__parse_errors(errors)
        self.alias_py.py_pick_list.pick_nodes(nodes)

    @sgtk.LogManager.log_timing
    def pick_curves_on_surface_from_nodes(self, errors: AlDagNodeErrors = None):
        """
        Pick the curves on surface.

        If `errors` are not given, nothing is picked.

        :param errors: The nodes to pick curves on surface from.
        """

        if not errors:
            return

        nodes = self.__parse_errors(errors)
        self.alias_py.py_pick_list.pick_curves_on_surface_from_nodes(nodes)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_shaders(
        self,
        errors: AlShaderErrors = None,
    ):
        """
        Pick the nodes assigned to the shaders.

        If `errors` are not given, nothing is picked.

        :param errors: The shaders to get assigned nodes to pick.
        """

        if not errors:
            return

        shaders = self.__parse_errors(errors)
        self.alias_py.py_pick_list.pick_nodes_assigned_to_shaders(shaders)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_layers(
        self,
        errors: AlLayerErrors = None,
    ):
        """
        Pick the nodes assigned to the layers.

        If `errors` are not given, nothing is picked.

        :param errors: The layers to get assigned ndoes to pick.
        """

        if not errors:
            return

        layers = self.__parse_errors(errors)
        self.alias_py.py_pick_list.pick_nodes_assigned_to_layers(layers)

    @sgtk.LogManager.log_timing
    def pick_layers(self, errors: Optional[AlLayerErrors] = None):
        """
        Pick the layers.

        :param errors: The layers to pick.
        """

        if errors:
            layers = self.__parse_errors(errors)
            self.alias_py.py_pick_list.pick_layers(layers=layers)
        else:
            self.alias_py.py_pick_list.pick_layers(pick_all=True)

    @sgtk.LogManager.log_timing
    def pick_locators(self, errors: Optional[AlLocatorErrors] = None):
        """
        Pick the locators.

        :param errors: The locators to pick. If None, all locators will be picked.
        """

        if errors:
            errors = self.__parse_errors(errors)
            self.alias_py.py_pick_list.pick_locators(locators=errors)
        else:
            self.alias_py.py_pick_list.pick_locators(pick_all=True)

    # ------------------------------------------------------------------------------
    # Private helper methods

    def __parse_errors(
        self,
        errors: Any,
    ) -> List[str]:
        """
        Parse the given errors list.

        The errors list is passed to 'fix' functions and are generally a list of
        the objects that have not passed the corresponding 'validate' function.

        This method parses the error list and returns a list of object names
        to work with.

        :return: The parsed errors.
        """

        if not errors:
            return []

        if isinstance(errors, str):
            return [errors]

        if isinstance(errors, dict):
            return [errors.get("name")]

        if isinstance(errors, list):
            object_names = []
            for error in errors:
                if isinstance(error, dict):
                    object_names.append(error.get("name"))
                elif isinstance(error, str):
                    object_names.append(error)
            return object_names

        raise ValueError("Invalid error object list")

    def __is_str_list(
        self,
        values_list: Any,
    ) -> bool:
        """
        Convenience functions to check if the given value is a list of strings.

        Assumes list values are of the same type.
        """

        if not values_list:
            return False
        if not isinstance(values_list, list):
            return False
        return isinstance(values_list[0], str)

    def __return_node_result(
        self,
        result: TraverseDagOutputData,
        force_return_nodes: Optional[bool] = False,
    ) -> Union[bool, AlDagNodeList, Tuple[bool, int]]:
        """
        Return the node result.

        For performance, we will only get the list of error nodes to return
        if the count is less than the threshold, otherwise it will be very
        slow to get and return a large list of nodes.

        :param result: The result to return.
        :param force_return_nodes: If True, the nodes will be returned
            regardless of the count. Default is False.

        :return: The result.
        """

        if force_return_nodes:
            return result.nodes

        invalid_count = result.count
        if invalid_count == 0:
            # No invalid nodes found, return True to indicate success
            return True
        if invalid_count <= self._max_error_count:
            # Safe to get the nodes to return
            return result.nodes
        # Too many invalid nodes, return False and the number of errors to
        # indicate failure
        return (False, invalid_count)

    # ------------------------------------------------------------------------------
    # Deprecated Functions
    # ------------------------------------------------------------------------------
    # These functions are deprecated and will be removed in a future release.

    @sgtk.LogManager.log_timing
    def fix_all_node_has_construction_history(self, errors=None, skip_node_types=None):
        """
        ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_node_has_construction_history` instead.

        Delete construction history for all nodes.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        self.fix_node_has_construction_history(
            errors=None, skip_node_types=skip_node_types
        )

    @sgtk.LogManager.log_timing
    def fix_all_node_instances(self, errors=None):
        """
        ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_node_instances` instead.

        Remove all instanced nodes.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        self.fix_node_instances(errors=None)

    @sgtk.LogManager.log_timing
    def fix_all_node_pivots_at_origin(self, errors=None, skip_node_types=None):
        """
        ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_node_pivots_at_origin` instead.

        Reset scale and rotate pivots to the origin for all nodes.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        self.fix_node_pivots_at_origin(errors=None, skip_node_types=skip_node_types)

    @sgtk.LogManager.log_timing
    def fix_all_node_curves(self, errors=None):
        """
        ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_node_curves` instead.

        Delete all nodes that represent a curve.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        self.fix_node_curves(errors=None)

    @sgtk.LogManager.log_timing
    def fix_all_curve_on_surface_unused(
        self,
        errors: Optional[AlDagNodeErrors] = None,
    ):
        """
        ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_curve_on_surface_unused` instead.

        Delete unused curves on surface for all nodes.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        """

        self.fix_curve_on_surface_unused(errors=None)

    @sgtk.LogManager.log_timing
    def fix_all_curve_on_surface_construction_history(self, errors=None):
        """
         ********** DEPRECATED **********
        WARNING: This function is deprecated and will be removed in a future release.
        Please use `fix_curve_on_surface_construction_history` instead.

        Delete construction history of unnused curves on surface for all nodes.

        :param errors: This param is ignored, though it is required to be defiend for this
            function to be a data validation fix callback.
        :type errors: N/A
        :param skip_node_types: The specified node types will not be fixed.
        :type skip_node_types: list<alias_api.AlObjectType>
        """

        # Call the main fix function but do not pass an errors list to indicate that all nodes
        # should be processed. This will improve performance.
        return self.fix_curve_on_surface_construction_history(errors=None)

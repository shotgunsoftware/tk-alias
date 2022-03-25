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
from .api import dag_node as api_dag_node
from .api import layer as api_layer
from .api import pick_list as api_pick_list
from .api import utils as api_utils


class AliasSceneValidator(object):
    """
    The Alias Scene Validator class provides the data and functionality to validate a scene in Alias.

    The `get_validation_data` method returns the validation rules data set, which drives the scene
    validation. Each rule in the validation data includes the necessary information to display the
    validation rule, and the functions to perform the validation check and fix actions for the rule.

    The validation rule check functions are the functions prefixed with `check_` and the fix functions
    are prefixed with `fix_`.
    """

    class CheckResult(object):
        """
        The result object returned by AliasSceneValidator check functions.
        """

        def __init__(self, is_valid=None, invalid_items=None, args=None, kwargs=None):
            """
            Initialize the result object with the given data.

            :param is_valid: The success status that the check function reported
            :type is_valid: bool
            :param invalid_items: The invalid items the check function found
            :type invalid_items: list
            :param args: The arguments list the check function provided to pass to its corresponding fix function.
            :type args: list
            :param kwargs: The key-word arguments the check function provided to pass to its corresponding fix
                function.
            :type kargs: dict
            """

            if is_valid is None:
                self.is_valid = not invalid_items
            else:
                self.is_valid = is_valid

            invalid_items = invalid_items or []
            self.invalid_items = [
                {"id": item.name, "name": item.name, "type": item.type(),}
                for item in invalid_items
            ]

            self.args = args or []
            self.kwargs = kwargs or {}
            self.kwargs["invalid_items"] = invalid_items

    def __init__(self):
        """
        Initialize the validator and set up the properties required for validaiting an Alias scene.
        """

        bundle = sgtk.platform.current_bundle()

        camera_node_types = api_utils.camera_node_types()
        light_node_types = api_utils.light_node_types()

        # Store the validation data since this is static
        self.__validation_data = self.get_validation_data()

        #
        # TODO make these configurable hook/settings
        #
        self.__default_layer_name = "DefaultLayer"
        self.__default_shader_name = "DefaultShader"

        self.__skip_layers = set(
            bundle.settings.get("skip_layers", [self.__default_layer_name])
        )
        self.__skip_shaders = set(
            bundle.settings.get("skip_shaders", [self.__default_shader_name])
        )

        # Node types to skip when checking for construction history
        self.__skip_node_types_construction_history = set(
            [
                alias_api.AlObjectType.CurveNodeType,
                alias_api.AlObjectType.FaceNodeType,
                alias_api.AlObjectType.TextureNodeType,
            ]
        )
        self.__skip_node_types_construction_history.update(camera_node_types)

        # Node types to skip when checking for zero transforms
        self.__skip_node_types_zero_transform = set(camera_node_types)

        # Node types to allow as top-level DAG nodes
        self.__node_types_allowed_in_dag_top_level = [
            alias_api.AlObjectType.CurveNodeType,
            alias_api.AlObjectType.FaceNodeType,
            alias_api.AlObjectType.SurfaceNodeType,
            alias_api.AlObjectType.GroupNodeType,
        ]

        # Node types to allow in the default layer
        self.__node_types_allowed_in_default_layer = set(
            [
                alias_api.AlObjectType.GroupNodeType,
                alias_api.AlObjectType.TextureNodeType,
            ]
        )
        self.__node_types_allowed_in_default_layer.update(camera_node_types)
        self.__node_types_allowed_in_default_layer.update(light_node_types)

        # Node types that are only allowed to be in the default layer
        self.__node_types_only_in_default_layer = set(
            [alias_api.AlObjectType.TextureNodeType,]
        )
        self.__node_types_only_in_default_layer.update(camera_node_types)
        self.__node_types_only_in_default_layer.update(light_node_types)

    # -------------------------------------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------------------------------------
    #   Data and execute methods
    #
    #   These are the main methods for the AliasSceneValiation class.
    #
    #   The 'get_validation_data' method defines all the validation rules that apply to an Alias scene. The
    #   validation data provides all the necessary info to describe the validation rule, as well as the
    #   'check', 'fix' and individual actions for invalid items found from the validation rule check.
    #
    #   The execute methods are convenience functions to execute a validation rule check or fix by passing
    #   the validation rule id.
    # -------------------------------------------------------------------------------------------------------

    def get_validation_data(self):
        """
        Return the data set containing the validation rules that can be applied to an Alias scene.

        The data is a dictionay mapping of validation rule id to its validation rule data. The following
        validation rules are defined:

            group_has_single_level_hierarchy:
                description: Groups are prohibited from containing more than one level of hierarchy (e.g. a Group 1 can have a group, Group 2, but Group 2 cannot contain another Group)
            layer_is_empty:
                description: Check for empty layers and folders in the scene
            layer_has_single_item:
                description: Layers are prohibited from containing more than one item (e.g. layer should have a single group that contains all geometry)
            layer_has_single_shader:
                description: Layers are prohibited from using multiple shader (e.g. each node in the layer must have the same shader assigned ot it)
            layer_symmetry:
                description: Layers are prohibited from turning on symmetry
            locators:
                description: Check for locators in the scene
            metadata:
                description: Check for metadata
            node_dag_top_level:
                description: Top-level DAG nodes must be of type: AlGroupNode, AlCurveNode, AlFaceNode, AlSurfaceNode. Nodes with parent nodes (non top-level nodes) must have the same layer as its parent node
            node_has_construction_history:
                description: Check for construction history
            node_has_zero_transform:
                description: Check for nodes with non-zero transformations
            node_is_null:
                description": Check for null nodes in the scene
            node_is_not_in_default_layer:
                description: Only allows Lights, Cameras, and Texture Placements are allowed in the default layer
            node_is_in_default_layer:
                description: The required objects (Lights, Cameras, Texture Placements) must be in the default layer
            node_instances:
                description: Instances are prohibited
            node_layer_matches_parent:
                description: A node's layer must be the same as its parent's layer
            node_name_matches_layer:
                description": A node's name must match its assigned layer name
            node_pivots_at_origin:
                description: Reset pivots to the origin (0,0,0)
            node_unused_curves_on_surface:
                description: Check for unused curve on surface nodes in the current scene
            references_exist:
                description: Referenced geometry is prohibited
            shader_is_vred_compatible:
                description: Shaders must be from the Asset Library for compatibility with VRED
            shader_unused:
                description: Check for unused shaders in the scene

        Each validation rule is a dict containing key-values:
            name:
                value: The display name of the validation rule.
                type: str
            description:
                value: Text to describe what the validation rule checks for.
                type: str
            check_func:
                type: function
                value: The function to call to check the validation rule.
            check_name:
                type: str
                value: Short text to describe what the `check_func` does (e.g. "Check").
            fix_func:
                type: function
                value: The function to call to fix the scene data such that the validation rule passes.
            fix_name:
                type: str
                value: Short text to describe what the `fix_func` does (e.g. "Fix").
            fix_tooltip:
                type: str
                value: Detailed text to describe what the `fix_func` does.
            error_msg:
                type: str
                value: Text to display when the validation rule fails.
            actions:
                type: list
                value:
                    type: dict
                    value: An action that can be applied to an all the invalid items that were found after
                        executing `check_func`.
                    required keys:
                        name (str) - The display text for the action
                        callback (function) - The function to call when the action is invoked
                    optional keys:
                        tooltip (str) - Text to display as for the item action's tooltip help messages
            item_actions:
                type: list
                value:
                    type: dict
                    value: An action that can be applied to an "invalid item" that was found after executing
                        `check_func`.
                    required keys:
                        name (str) - The display text for the action
                        callback (function) - The function to call when the action is invoked
                    optional keys:
                        tooltip (str) - Text to display as for the item action's tooltip help messages

        All `check_func` functions should return the following data:
            type: tuple
            value:
                (0) bool - True if the validation check passed, else False
                (1) list - A list containing data pertaining to the invalid items found when running the
                           validation check. The data should be a dict with keys: 'id', 'name', 'type', where
                           'id' is the unique identifier, 'type' is the object type, and 'name' is the
                           display text for the invalid item
                (2) list - An arguments list that can be passed to the check function's corresponding fix
                           function ('fix_func' defined for the validaiton rule)
                (3) dict - A keyword arguments dict that can be passed to hte check function's corresponing
                           fix function ('fix_func' defined for the validation rule)

        :return: The scene validation data.
        :rtype: dict
        """

        return {
            "shader_unused": {
                "name": "Unused Shaders",
                "description": "Check for shaders that are not assigned to any geometry.",
                "error_msg": "Found unused Shaders",
                "check_func": self.check_shader_unused,
                "fix_func": self.fix_shader_unused,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete unused Shaders",
                "item_actions": [
                    {"name": "Delete", "callback": self.fix_shader_unused,},
                ],
            },
            "shader_is_vred_compatible": {
                "name": "VRED Shaders",
                "description": "Shaders must be from the Asset Library for compatibility with VRED.",
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
            },
            "node_is_null": {
                "name": "Null Nodes",
                "description": "Check for null nodes in the scene.",
                "fix_func": self.fix_node_is_null,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all null nodes.",
                "error_msg": "Found null node(s).",
            },
            "node_has_construction_history": {
                "name": "Node Construction History",
                "description": "Check for nodes that have construction history.",
                "check_func": self.check_node_has_construction_history,
                "fix_func": self.fix_node_has_construction_history,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete all construction history from all nodes.",
                "error_msg": "Found node(s) with construction history.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_node_has_construction_history,
                    },
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_instances": {
                "name": "Instances",
                "description": "Instances are prohibited.",
                "check_func": self.check_node_instances,
                "fix_func": self.fix_node_instances,
                "fix_name": "Expand All",
                "fix_tooltip": "Remove Instances by expanding them.",
                "error_msg": "Instance found.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {"name": "Expand", "callback": self.fix_node_instances,},
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_pivots_at_origin": {
                "name": "Reset Pivots",
                "description": "Reset pivots to the origin (0,0,0).",
                "check_func": self.check_node_pivots_at_origin,
                "fix_func": self.fix_node_pivots_at_origin,
                "fix_name": "Reset All",
                "fix_tooltip": "All pivots will be moved to the origin.",
                "error_msg": "Found pivots not set to the origin.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {"name": "Reset", "callback": self.fix_node_pivots_at_origin,},
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_has_zero_transform": {
                "name": "Zero Transforms",
                "description": "Set all transforms to zero (the identity matrix).",
                "check_func": self.check_node_has_zero_transform,
                "fix_func": self.fix_node_has_zero_transform,
                "fix_name": "Reset All",
                "fix_tooltip": "Reset all transforms to zero.",
                "error_msg": "Found node(s) with non-zero transform.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {"name": "Reset", "callback": self.fix_node_has_zero_transform,},
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_is_not_in_default_layer": {
                "name": "Nodes Must Not Be In Default Layer",
                "description": "Only Light, Camera, Texture, and Group nodes can be in the default layer.",
                "check_func": self.check_node_is_not_in_default_layer,
                "error_msg": "Found invalid nodes in the default layer.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                        "tooltip": "Select invalid nodes that must be manually fixed.",
                    },
                ],
            },
            "node_is_in_default_layer": {
                "name": "Nodes Must Be In Default Layer",
                "description": "Lights, Cameras, Texture can only be in the default layer.",
                "check_func": self.check_node_is_in_default_layer,
                "fix_func": self.fix_node_is_in_default_layer,
                "fix_name": "Move",
                "fix_tooltip": "Move all Lights, Cameras, Texture nodes to the default layer.",
                "error_msg": "Required objects not found in the default layer.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {"name": "Move", "callback": self.fix_node_is_in_default_layer,},
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_name_matches_layer": {
                "name": "Match Layer And Assigned Nodes' Names",
                "description": "Layer name must match the name of each node that is assigned to it.",
                "check_func": self.check_node_name_matches_layer,
                "fix_func": self.fix_node_name_matches_layer,
                "fix_name": "Rename All",
                "fix_tooltip": "Rename Groups to match their respective Layer name.",
                "error_msg": "Found Layer Group name mismatches.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {"name": "Rename", "callback": self.fix_node_name_matches_layer,},
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_layer_matches_parent": {
                "name": "Node Layer Matchces Parent Layer",
                "description": "The layer assigned to a node must be the same as the parent node layer.",
                "check_func": self.check_node_layer_matches_parent,
                "fix_func": self.fix_node_layer_matches_parent,
                "fix_name": "Reassign All",
                "fix_tooltip": "Set each node's layer to match its parent's layer.",
                "error_msg": "Found node(s) assigned to layer different than its parent.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {
                        "name": "Reassign",
                        "callback": self.fix_node_layer_matches_parent,
                    },
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "node_dag_top_level": {
                "name": "Top-Level DAG Nodes",
                "description": "DAG top-level nodes must be of type: AlGroupNode, AlCurveNode, AlFaceNode, AlSurfaceNode. Nodes with parent nodes (non top-level nodes) must have the same layer as its parent node.",
                "check_func": self.check_node_dag_top_level,
                "error_msg": "Found invalid nodes in the top level of the DAG.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {
                        "name": "Select",
                        "callback": self.pick_nodes,
                        "tooltip": "Select invalid nodes that must be manually fixed.",
                    },
                ],
            },
            "node_unused_curves_on_surface": {
                "name": "Unused Curve on Surfaces",
                "description": "Check for nodes with unused curves on surfaces in the current scene.",
                "check_func": self.check_node_unused_curves_on_surface,
                "fix_func": self.fix_node_unused_curves_on_surface,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete node's unused curve on surface",
                "error_msg": "Found node(s) with unused curve(s) on surface",
                "actions": [
                    {"name": "Select All Nodes", "callback": self.pick_nodes,},
                    {
                        "name": "Select All COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                ],
                "item_actions": [
                    {
                        "name": "Delete",
                        "callback": self.fix_node_unused_curves_on_surface,
                    },
                    {"name": "Select Nodes", "callback": self.pick_nodes,},
                    {
                        "name": "Select COS",
                        "callback": self.pick_curves_on_surface_from_nodes,
                    },
                ],
            },
            "group_has_single_level_hierarchy": {
                "name": "Only One Level Per Group",
                "description": "Groups are prohibited from containing more than one level of hierarchy (e.g. a Group 1 can have a group, Group 2, but Group 2 cannot contain another Group).",
                "check_func": self.check_group_has_single_level_hierarchy,
                "fix_func": self.fix_group_has_single_level_hierarchy,
                "fix_name": "Flatten All",
                "fix_tooltip": "Flatten Groups with multiple hierarchy levels.",
                "error_msg": "Found Groups with multiple hierarchy levels.",
                "actions": [{"name": "Select All", "callback": self.pick_nodes,},],
                "item_actions": [
                    {
                        "name": "Flatten",
                        "callback": self.fix_group_has_single_level_hierarchy,
                    },
                    {"name": "Select", "callback": self.pick_nodes,},
                ],
            },
            "layer_is_empty": {
                "name": "Empty Layers",
                "description": "Check for empty layers and folders in the scene.",
                "check_func": self.check_layer_is_empty,
                "fix_func": self.fix_layer_is_empty,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete empty layers and folders",
                "error_msg": "Found empty layers or folders",
                "actions": [{"name": "Select All", "callback": self.pick_layers,},],
                "item_actions": [
                    {"name": "Delete", "callback": self.fix_layer_is_empty,},
                    {"name": "Select", "callback": self.pick_layers,},
                ],
            },
            "layer_has_single_shader": {
                "name": "Layer Has Single Shader",
                "description": "All nodes within a layer must use one single shader. Assign one shader to all nodes in the layer or split into multiple layers.",
                "check_func": self.check_layer_has_single_shader,
                "error_msg": "Found layer(s) using multiple shaders.",
                "actions": [{"name": "Select All", "callback": self.pick_layers,},],
                "item_actions": [
                    {"name": "Select Layer", "callback": self.pick_layers,},
                    {
                        "name": "Select Layer Geometry",
                        "callback": self.pick_nodes_assigned_to_layers,
                    },
                ],
            },
            "layer_symmetry": {
                "name": "Layer Symmetry",
                "description": "Layers are prohibited from turning on symmetry.",
                "check_func": self.check_layer_symmetry,
                "fix_func": self.fix_layer_symmetry,
                "fix_name": "Turn Off All",
                "fix_tooltip": "Turn off symmetry for all Layers and Layer Folders.",
                "error_msg": "Found Layers with symmetry turned on.",
                "actions": [{"name": "Select All", "callback": self.pick_layers,},],
                "item_actions": [
                    {"name": "Turn Off", "callback": self.fix_layer_symmetry,},
                    {"name": "Select", "callback": self.pick_layers,},
                ],
            },
            "layer_has_single_item": {
                "name": "Layer Has Single Item",
                "description": "Layers are prohibited from containing more than one item (group hierarchy within a layer is prohibited, and should be flattened).",
                "check_func": self.check_layer_has_single_item,
                "fix_func": self.fix_layer_has_single_item,
                "fix_name": "Collapse All",
                "fix_tooltip": "Collapse all layer items into a single group, and rename the group to the name of the layer.",
                "error_msg": "Found layers with more than one item.",
                "actions": [{"name": "Select All", "callback": self.pick_layers,},],
                "item_actions": [
                    {"name": "Collapse", "callback": self.fix_layer_has_single_item,},
                    {"name": "Select", "callback": self.pick_layers,},
                ],
            },
            "locators": {
                "name": "Locators",
                "description": "Check for locators in the scene.",
                "check_func": self.check_locators,
                "fix_func": self.fix_locators,
                "fix_name": "Delete All",
                "fix_tooltip": "Delete locators",
                "error_msg": "Found locator(s).",
                "actions": [{"name": "Select All", "callback": self.pick_locators,},],
                "item_actions": [
                    {"name": "Delete", "callback": self.fix_locators,},
                    {"name": "Select", "callback": self.pick_locators,},
                ],
            },
            "metadata": {
                "name": "Metadata",
                "description": "Check for nodes with construction metadata.",
            },
            "placeholder": {
                "name": "Placeholder",
                "description": "Just a placeholder to an another manual check.",
            },
            "references_exist": {
                "name": "Referenced Geometry",
                "description": "Referenced geometry is prohibited.",
                "check_func": self.check_refererences_exist,
                "fix_func": self.fix_references_exist,
                "fix_name": "Remove",
                "fix_tooltip": "Remove all referenced geometry in the scene.",
                "error_msg": "Found referenced geometry.",
            },
        }

    def execute_check_action(self, rule_id, *args, **kwargs):
        """
        Execute the Alias scene validation check function.

        :param rule_id: The unique id to get and run the validation check.
        :type rule_id: str
        :param args: The arguments list to pass to the check function.
        :type args: list
        :param kwargs: The key-word arguments dict to pass to the check function.
        :type kwargs: dict

        :return: The return value of the check function. See the `get_validation_data` function doc for more
            details on the check function return value.
        :rtype: tuple(bool,list,list,dict)

        :raises NotImplementedError: if the validation data was not found for the `rule_id`
        """

        data = self.__validation_data.get(rule_id)

        if not data or not data.get("check_func"):
            raise NotImplementedError(
                "{} does not support check action '{}'.".format(
                    self.__class__.__name__
                ),
                rule_id,
            )

        return data["check_func"](*args, **kwargs)

    def execute_fix_action(self, rule_id, *args, **kwargs):
        """
        Execute the Alias scene validation fix function.

        :param rule_id: The unique id to get and run the validation check.
        :type rule_id: str
        :param args: The arguments list to pass to the check function.
        :type args: list
        :param kwargs: The key-word arguments dict to pass to the check function.
        :type kwargs: dict

        :return: The return value of the check function. See the `get_validation_data` function doc for more
            details on the check function return value.
        :rtype: tuple(bool,list,list,dict)

        :raises NotImplementedError: if the validation data was not found for the `rule_id`
        """

        data = self.__validation_data.get(rule_id)

        if not data or not data.get("fix_func"):
            raise NotImplementedError(
                "{} does not support fix action '{}'.".format(self.__class__.__name__),
                rule_id,
            )

        return data["fix_func"](*args, **kwargs)

    # -------------------------------------------------------------------------------------------------------
    # Check & Fix Functions
    # -------------------------------------------------------------------------------------------------------
    #   These can be executed directly, but they are meant to be defined as a 'check_func' in the validation
    #   data and executed using the validatino data rule item.
    #
    #   Guidelines to defining a check function:
    #       - Function name should be prefixed with `check_`
    #       - Takes an optional single parameter `fail_fast` which returned immediately once the check fails
    #       - Returns a ValidationCheckResult object
    #
    #   Guidelines to defining a fix function:
    #       - Function name should be prefixed with `fix_`
    #       - Takes an optional single parameter `invalid_items` which are the items intended to be fixed.
    #               The naming of the parameter is important since this is passed from the check function
    #               return value)
    #
    # -------------------------------------------------------------------------------------------------------

    @sgtk.LogManager.log_timing
    def check_shader_unused(self, fail_fast=False):
        """
        Check for unused shaders (shaders that are not assigned to any geometry) in the current scene.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        unused_shaders = []

        for shader in alias_api.get_shaders():
            if shader.name in self.__skip_shaders:
                continue

            if not shader.is_used():
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                unused_shaders.append(shader)

        return AliasSceneValidator.CheckResult(invalid_items=unused_shaders)

    @sgtk.LogManager.log_timing
    def fix_shader_unused(self, invalid_items=None):
        """
        Process all shaders in the current scene, or the specified shaders, and delete all unused shaders.

        NOTE that the shaders list in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated shaders list.

        :param invalid_items: (optional) The shaders to process, if None, all shaders in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlShader>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        shaders = invalid_items or alias_api.get_shaders()

        for shader in shaders:
            if isinstance(shader, six.string_types):
                if shader in self.__skip_shaders:
                    continue
                shader = alias_api.get_shader_by_name(shader)
                if not shader:
                    continue
            elif shader.name in self.__skip_shaders:
                continue

            if not shader.is_used():
                shader.delete_object()

    @sgtk.LogManager.log_timing
    def check_shader_is_vred_compatible(self, fail_fast=False):
        """
        Check for non-VRED shaders used in the current scene.

        A non-VRED shader is a shader that is not from the Asset Library (compaitible with VRED). Only shaders
        that are in use will be checked (e.g. if there is a non-VRED shader but is not used, it will not cause
        this check to fail).

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        non_vred_shaders = []

        for shader in alias_api.get_shaders():
            if shader.name in self.__skip_shaders:
                continue

            if shader.is_used() and not alias_api.is_copy_of_vred_shader(shader):
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                non_vred_shaders.append(shader)

        return AliasSceneValidator.CheckResult(invalid_items=non_vred_shaders)

    @sgtk.LogManager.log_timing
    def fix_node_is_null(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and delete all null nodes.

        :param invalid_items: (optional) The of nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>

        :raises alias_api.AliasPythonException: if the attempting to delete specific nodes
        """

        if invalid_items is None:
            alias_api.delete_null_nodes()
        else:
            # NOTE we could just delete the list of given nodes, but we cannot determine if a given node is null.
            api_utils.raise_exception(
                "Requires Alias C++ API function to determine if a node is null"
            )

    @sgtk.LogManager.log_timing
    def check_node_has_construction_history(self, fail_fast=False):
        """
        Check for nodes with construction history in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        nodes_with_history = api_dag_node.get_nodes_with_construction_history(
            skip_node_types=self.__skip_node_types_construction_history
        )

        return AliasSceneValidator.CheckResult(invalid_items=nodes_with_history)

    @sgtk.LogManager.log_timing
    def fix_node_has_construction_history(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified of nodes, and delete history from any nodes
        with history.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated scene.

        :param invalid_items: (optional) The nodes to process, if None, all nodes in the current scene will
                       be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        nodes = api_dag_node.get_nodes_with_construction_history(
            nodes=invalid_items,
            skip_node_types=self.__skip_node_types_construction_history,
        )
        for node in nodes:
            alias_api.delete_history(node)

    @sgtk.LogManager.log_timing
    def check_node_instances(self, fail_fast=False):
        """
        Check for instanced nodes in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = api_dag_node.get_instanced_nodes()

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def fix_node_instances(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the list of nodes if provided, and remove all instanced
        nodes.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated scene.

        :param invalid_items: (optional) The list of nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>

        :raises alias_api.AliasPythonException: if a node instance failed to expand
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        nodes = api_dag_node.get_instanced_nodes(invalid_items)

        for node in nodes:
            status = alias_api.expand_instances(node)
            if not api_utils.is_success(status):
                api_utils.raise_exception(
                    "Failed to expand instanced node '{}'".format(node.name), status
                )

    @sgtk.LogManager.log_timing
    def check_node_pivots_at_origin(self, fail_fast=False):
        """
        Check for nodes that do not have their pivots set to the origin.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = api_dag_node.get_nodes_with_non_origin_pivot()

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def fix_node_pivots_at_origin(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and reset their scale and roate
        pivots such that they are centered around the origin.

        NOTE that the pivots Alias may not update automatically, alias_api.redraw_screen() may need to be
        invoked after this function, to see the updated pivots.

        :param invalid_items: (optional) The nodes to process, if None, all nodes in the current scene will
                              be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>

        :raises alias_api.AliasPythonException: if a failed to set a node's pivot to the origin
        """

        # FIXME separate this out into two checks, one for scale and one for rotate?

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        nodes = api_dag_node.get_nodes_with_non_origin_pivot(invalid_items)
        center = alias_api.Vec3(0.0, 0.0, 0.0)

        for node in nodes:
            status = node.set_scale_pivot(center)
            if not api_utils.is_success(status):
                api_utils.raise_exception(
                    "Failed to set scale pivot for node '{}'".format(node.name), status
                )

            status = node.set_rotate_pivot(center)
            if not api_utils.is_success(status):
                api_utils.raise_exception(
                    "Failed to set rotate pivot for node '{}'".format(node.name), status
                )

    @sgtk.LogManager.log_timing
    def check_node_has_zero_transform(self, fail_fast=False):
        """
        Check for nodes with non-zero transforms in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = api_dag_node.get_nodes_with_non_zero_transform(
            skip_node_types=self.__skip_node_types_zero_transform
        )
        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def fix_node_has_zero_transform(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and reset all transforms to zero.

        NOTE that the nodes Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated node transforms.

        :param invalid_items: (optional) The nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>

        :raises alias_api.AliasPythonException: if a failed to set a node's transform to zero
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        nodes = api_dag_node.get_nodes_with_non_zero_transform(
            nodes=invalid_items, skip_node_types=self.__skip_node_types_zero_transform
        )
        for node in nodes:
            status = alias_api.zero_transform(node)
            if not api_utils.is_success(status):
                api_utils.raise_exception(
                    "Failed to apply zero transform to node '{}'".format(node.name),
                    status,
                )

    @sgtk.LogManager.log_timing
    def check_node_is_not_in_default_layer(self, fail_fast=False):
        """
        Check that the default layer contains only nodes of type in the specified list:
            CameraEyeType
            CameraViewType
            CameraUpType
            TextureNodeType
            LightNodeType
            LightLookAtNodeType
            LightUpNodeType

        TODO allow this node type list to be configurable

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        default_layer = alias_api.get_layer_by_name(self.__default_layer_name)
        if default_layer is None:
            # No default layer found, let this check pass
            return AliasSceneValidator.CheckResult(is_valid=True)

        invalid_nodes = []

        # NOTE get_assigned_nodes will not return the group nodes, only leaf nodes assigned to the layer
        nodes = default_layer.get_assigned_nodes()

        for node in nodes:
            if node.type() not in self.__node_types_allowed_in_default_layer:
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                invalid_nodes.append(node)

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def check_node_is_in_default_layer(self, fail_fast=False):
        """
        Check that the specified list of node types are only in the default layer:
            CameraEyeType
            CameraViewType
            CameraUpType
            TextureNodeType
            LightNodeType
            LightLookAtNodeType
            LightUpNodeType

        TODO allow this node type list to be configurable

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        default_layer = alias_api.get_layer_by_name(self.__default_layer_name)
        if default_layer is None:
            # No default layer found, this check fails automatically
            return AliasSceneValidator.CheckResult(is_valid=False)

        input_data = alias_api.TraverseDagInputData(
            default_layer, False, self.__node_types_only_in_default_layer, True
        )
        result = alias_api.search_dag(input_data)

        return AliasSceneValidator.CheckResult(invalid_items=result.nodes)

    @sgtk.LogManager.log_timing
    def fix_node_is_in_default_layer(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and move any nodes to the
        default layer that should be in the default layer.

        :param invalid_items: (optional) The of nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>
        """

        default_layer = alias_api.get_layer_by_name(self.__default_layer_name)
        if default_layer is None:
            return

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        if invalid_items:
            for node in invalid_items:
                if isinstance(node, six.string_types):
                    node = alias_api.find_dag_node_by_name(node)

                if not node:
                    continue

                node_layer = node.layer()
                if not node_layer or node_layer.name != self.__default_layer_name:
                    if node.type() in self.__node_types_only_in_default_layer:
                        node.set_layer(default_layer)

        else:
            input_data = alias_api.TraverseDagInputData(
                default_layer, False, self.__node_types_only_in_default_layer, True
            )
            result = alias_api.search_dag(input_data)

            for node in result.nodes:
                node.set_layer(default_layer)

    @sgtk.LogManager.log_timing
    def check_node_name_matches_layer(self, fail_fast=False):
        """
        Check for naming mismatches between layer and its nodes, for all top-levle nodes in the current scene.

        Each layer should only contain one group (or one surface). This group is named after the layer.
        If groups are found that don't match the name of the layer, an error is thrown.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = []
        nodes = alias_api.get_top_dag_nodes()

        for node in nodes:
            layer = node.layer()
            if not layer or layer.name in self.__skip_layers:
                continue

            # Check the layer and node names match, which means they are the same or the ndoe name is the
            # layer name plus the suffix "#n" where 'n' is a number.
            reg = r"^{}(#?\d)*$".format(layer.name)
            if not re.match(reg, node.name):
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                invalid_nodes.append(node)

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def fix_node_name_matches_layer(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and rename any nodes that do not
        match its layer.

        :param invalid_items: (optional) The of nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        nodes = invalid_items or alias_api.get_top_dag_nodes()

        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node:
                continue

            node_layer = node.layer()
            if not node_layer:
                continue

            node_layer_name = node_layer.name
            if node_layer_name in self.__skip_layers:
                continue

            reg = r"^{}(#?\d)*$".format(node_layer_name)
            if not re.match(reg, node.name):
                node.name = node_layer_name

    @sgtk.LogManager.log_timing
    def check_node_layer_matches_parent(self, fail_fast=False):
        """
        Check for nodes that do not have the layer as their parent node.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_layer_does_not_match_parent_layer(input_data)

        return AliasSceneValidator.CheckResult(invalid_items=result.nodes)

    @sgtk.LogManager.log_timing
    def fix_node_layer_matches_parent(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified nodes, and ensure that a node's layer is the
        same as its parent node's layer.

        :param invalid_items: (optional) The of nodes to process, if None, all nodes in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlDagNode>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        if invalid_items:
            for node in invalid_items:
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
    def check_node_dag_top_level(self, fail_fast=False):
        """
        Check for invalid top-level nodes in the DAG of the current scene.

        Top-level nodes must have a type in the allowed nodes list. Default allowed types:
            CurveNodeType
            FaceNodeType
            SurfaceNodeType
            GroupNodeType

        TODO make this configurable

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = []
        nodes = alias_api.get_top_dag_nodes()

        for node in nodes:
            if node.type() not in self.__node_types_allowed_in_dag_top_level:
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                invalid_nodes.append(node)

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def check_node_unused_curves_on_surface(self, fail_fast=False):
        """
        Check for unused curves on surfaces in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_nodes = api_dag_node.get_nodes_with_unused_curves_on_surface()

        return AliasSceneValidator.CheckResult(invalid_items=invalid_nodes)

    @sgtk.LogManager.log_timing
    def fix_node_unused_curves_on_surface(self, invalid_items=None):
        """
        Process all curves on surface current scene, or the list of curves on surface if provided, and delete
        unused curves on surface.

        :param invalid_items: The list of curves on surface to process, if None, all curves on surface
                              current scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlCurveOnSurface>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        unused_curves = api_dag_node.get_unused_curves_on_surface_for_nodes(
            nodes=invalid_items
        )

        for curve in unused_curves:
            curve.delete_object()

    @sgtk.LogManager.log_timing
    def check_layer_is_empty(self, fail_fast=False):
        """
        Check for empty layers and layer folders in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        include_folders = True
        empty_layers = alias_api.get_empty_layers(include_folders, self.__skip_layers)

        return AliasSceneValidator.CheckResult(invalid_items=empty_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_is_empty(self, invalid_items=None):
        """
        Process all layers in the current scene, or the list of layers if provided, and delete all the empty layers and layer
        folders.

        :param layers: (optiona) The layers to process, if None, all layers in the current scene will
                       be processed. Default=None
        :type layers: str | list<str> | list<AlLayer>
        """

        include_folders = True
        empty_layers = alias_api.get_empty_layers(include_folders, self.__skip_layers)

        # If a list of layers is specified, only delete those layers.
        delete_only = []
        if invalid_items:
            if isinstance(invalid_items, six.string_types):
                invalid_items = [invalid_items]

            for layer in invalid_items:
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

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_layers = alias_api.get_layers_using_multiple_shaders()

        return AliasSceneValidator.CheckResult(invalid_items=invalid_layers)

    @sgtk.LogManager.log_timing
    def check_layer_symmetry(self, fail_fast=False):
        """
        Check for layers with symmetry turned on in the current scene.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        if fail_fast:
            has_symmetric_layers = api_layer.get_symmetric_layers(
                check_exists=True, skip_layers=self.__skip_layers
            )
            return AliasSceneValidator.CheckResult(is_valid=not has_symmetric_layers)

        symmetric_layers = api_layer.get_symmetric_layers(
            skip_layers=self.__skip_layers
        )
        return AliasSceneValidator.CheckResult(invalid_items=symmetric_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_symmetry(self, invalid_items=None):
        """
        Process all layers in the current scene, or the specified layers, and turn off symmetry on layers.

        NOTE that the layers in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated layers.

        :param invalid_items: (optional) The layers to process, if None, all layers in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlLayer>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        layers = api_layer.get_symmetric_layers(
            layers=invalid_items, skip_layers=self.__skip_layers
        )

        for layer in layers:
            layer.symmetric = False

    @sgtk.LogManager.log_timing
    def check_layer_has_single_item(self, fail_fast=False):
        """
        Check for layers that contain more than one top-level node (e.g. layers can only have a single node,
        for multiple nodes, they can have a group node that contains child nodes).

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
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
                node_layer_name in self.__skip_layers
                or node_layer_name in marked_invalid_layers
            ):
                continue

            if node_layer_name in processed_layers:
                if fail_fast:
                    return AliasSceneValidator.CheckResult(is_valid=False)
                invalid_layers.append(node_layer)
                marked_invalid_layers.add(node_layer_name)
            else:
                processed_layers.add(node_layer_name)

        return AliasSceneValidator.CheckResult(invalid_items=invalid_layers)

    @sgtk.LogManager.log_timing
    def fix_layer_has_single_item(self, invalid_items=None):
        """
        Process all layers in the current scene, or the list of layers if provided, and place all
        layer's contents into a single group.

        A new group will be created if the layer does not have any group nodes currently.

        NOTE that the layers in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated scene.

        :param invalid_items: (optional) The list of layers to process, if None, all layers in the current
                              scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlLayer>
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        layers = invalid_items or alias_api.get_layers()

        for layer in layers:
            if isinstance(layer, six.string_types):
                layer = alias_api.get_layer_by_name(layer)

            if not layer:
                continue

            layer_name = layer.name
            group_node = None

            layer_top_level_nodes = []
            layer_group_nodes = []
            for node in alias_api.get_top_dag_nodes():
                if node.layer().name != layer_name:
                    continue

                layer_top_level_nodes.append(node)

                if api_utils.is_group_node(node):
                    layer_group_nodes.append(node)

            # first case: no existing group node
            if not layer_group_nodes:
                group_node = alias_api.AlGroupNode()
                status = group_node.create()
                if not api_utils.is_success(status):
                    api_utils.raise_exception(
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
        Check for groups with more than one level of hierarchy in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        invalid_group_nodes = alias_api.get_nesting_groups()

        return AliasSceneValidator.CheckResult(invalid_items=invalid_group_nodes)

    @sgtk.LogManager.log_timing
    def fix_group_has_single_level_hierarchy(self, invalid_items=None):
        """
        Process all nodes in the current scene, or the specified group nodes, and flatten each node such that
        it only has a single levele of hierarchy (e.g. parent->child but not parent->child->grandchild)

        NOTE that the groups in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated scene.

        :param invalid_items: (optional) The list of group nodes to process, if None, all nodes in the
                              current scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlLayer>

        :raises alias_api.AliasPythonException: if failed to flatten all groups
        """

        status = api_utils.success_status()

        if invalid_items:
            if isinstance(invalid_items, six.string_types):
                invalid_items = [invalid_items]

            groups_to_flatten = []
            for group_node in invalid_items:
                if isinstance(group_node, six.string_types):
                    group_node = alias_api.find_dag_node_by_name(group_node)

                if not group_node:
                    continue

                groups_to_flatten.append(group_node)
                flatten_status = alias_api.flatten_group_nodes(groups_to_flatten)
                if flatten_status != api_utils.success_status():
                    status = flatten_status

        else:
            status = alias_api.flatten_group_nodes()

        if not api_utils.is_success(status):
            api_utils.raise_exception("Failed to flatten group nodes", status)

    @sgtk.LogManager.log_timing
    def check_locators(self, fail_fast=False):
        """
        Check for locators in the current scene.

        :param fail_fast: Set to True to return immediately as soon as the check fails. Set to False to check
                          entire data and return all invalid items found, and arguments that can be passed to
                          the corresponding fix function. Note that when set to False, this function will be
                          slower to execute.
        :type fail_fast: bool

        :return: The check result object containing the data:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: AliasSceneValidation.CheckResult
        """

        if fail_fast:
            has_locators = api_utils.get_locators(check_exists=True)
            return AliasSceneValidator.CheckResult(is_valid=not has_locators)

        locators = api_utils.get_locators()
        return AliasSceneValidator.CheckResult(invalid_items=locators)

    @sgtk.LogManager.log_timing
    def fix_locators(self, invalid_items=None):
        """
        Process all locators in the current scene, or the specified locators, and delete them.

        :param invalid_items: The list of locators to process, if None, all locators in current scene will
                              be processed. Default=None
        :type invalid_items: str | list<str> | list<AlCurveOnSurface>

        :raises alias_api.AliasPythonException: if failed to delete locator object
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        if invalid_items:
            for locator in invalid_items:
                if isinstance(locator, six.string_types):
                    locator = alias_api.get_locator_by_name(locator)

                if locator:
                    status = locator.delete_object()
                    if not api_utils.is_success(status):
                        api_utils.raise_exception("Failed to delete locator", status)
        else:
            status = alias_api.delete_all_locators()
            if not api_utils.is_success(status):
                api_utils.raise_exception("Failed to delete all locators", status)

    @sgtk.LogManager.log_timing
    def check_refererences_exist(self, fail_fast=False):
        """
        Check for referenced geometry in the current scene.

        :param fail_fast: Not applicable
        :type fail_fast: bool

        :return: A tuple containing:
                    (1) True if the check passed, else False
                    (2) A list of data pertaining to the invalid items found
                        dict with required keys: id, name
                        This will be an empty list if fail_fast=False
                    (3) A list of args to pass to the corresponding fix function
                        This will be an empty list if fail_fast=False
                    (4) A dict of kwargs to pass to the corresponding fix function
                        This will be an empty dict if fail_fast=False
        :rtype: tuple<bool,list,list,dict>
        """

        references = alias_api.get_references()

        return AliasSceneValidator.CheckResult(invalid_items=references)

    @sgtk.LogManager.log_timing
    def fix_references_exist(self, invalid_items=None):
        """
        Process all references, or the specificed references, and remove all referneces from the current
        scene.

        NOTE that the nodes in Alias may not update automatically, alias_api.redraw_screen() may need
        to be invoked after this function, to see the updated scene.

        :param invalid_items: (optional) The list of references to process, if None, all references in the
                              current scene will be processed. Default=None
        :type invalid_items: str | list<str> | list<AlReferenceFile>

        :raises alias_api.AliasPythonException: if failed to remove a reference
        """

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        references = invalid_items or alias_api.get_references()

        for reference in references:
            if isinstance(reference, six.string_types):
                reference = alias_api.get_reference_by_name(reference)

            if reference:
                status = alias_api.remove_reference(reference)
                if not api_utils.is_success(status):
                    api_utils.raise_exception("Failed to remove reference", status)

    # -------------------------------------------------------------------------------------------------------
    # Pick Functions
    # -------------------------------------------------------------------------------------------------------
    #   These can be executed directly, but they are meant to be used as a validation rule item callback
    #   to help fix an invalid item which cannot be automatically fixed.
    #
    #   Guidelines to defining a pick function:
    #       - Function name should be prefixed with `pick_`
    #       - Takes an optional single parameter `invalid_items` which are the items intended to be picked
    #           (the naming of the parameter is important since this is passed from the check function
    #           return value)
    # -------------------------------------------------------------------------------------------------------

    @sgtk.LogManager.log_timing
    def pick_nodes(self, invalid_items=None):
        """
        Pick the nodes specified in the invalid_items.

        :param invalid_items: The node(s) to pick.
        :type invalid_items: str | AlDagNode | list<str> | list<AlDagNode>
        """

        if not invalid_items:
            return

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        api_pick_list.pick_nodes(invalid_items)

    @sgtk.LogManager.log_timing
    def pick_curves_on_surface_from_nodes(self, invalid_items=None):
        """
        Pick the curves on surface from the nodes specified in the invalid_items.

        :param invalid_items: The node(s) to pick curves on surface from.
        :type invalid_items: str | AlDagNode | list<str> | list<AlDagNode>
        """

        if not invalid_items:
            return

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        api_pick_list.pick_curves_on_surface_from_nodes(invalid_items)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_shaders(self, invalid_items=None):
        """
        Pick the nodes assigned to the shaders in the invalid items.

        :param invalid_items: The shaders to get assigned nodes to pick.
        :type invalid_items: str | list<str> | list<AlShader>
        """

        invalid_items = invalid_items or alias_api.get_shaders()

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        api_pick_list.pick_nodes_assigned_to_shaders(invalid_items)

    @sgtk.LogManager.log_timing
    def pick_nodes_assigned_to_layers(self, invalid_items=None):
        """
        Pick the nodes assigned to the layers in the invalid items.

        :param invalid_items: The layers to get assigned ndoes to pick.
        :type invalid_items: str | list<str> | list<AlLayer>
        """

        invalid_items = invalid_items or alias_api.get_layers()

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        api_pick_list.pick_nodes_assigned_to_layers(invalid_items)

    @sgtk.LogManager.log_timing
    def pick_layers(self, invalid_items=None):
        """
        Pick the layers in the invalid items.

        :param invalid_items: The layers to pick.
        :type invalid_items: str | list<str> | list<AlLayer>
        """

        invalid_items = invalid_items or alias_api.get_layers()

        if isinstance(invalid_items, six.string_types):
            invalid_items = [invalid_items]

        api_pick_list.pick_layers(invalid_items)

    @sgtk.LogManager.log_timing
    def pick_locators(self, invalid_items=None):
        """
        Pick the locators.

        :param invalid_items: The locators to pick. If None, all locators will be picked.
        :type invalid_items: str | list<str> | list<AlLocator>
        """

        if not invalid_items:
            api_pick_list.pick_locators(None, pick_all=True)

        else:
            if isinstance(invalid_items, six.string_types):
                invalid_items = [invalid_items]

            api_pick_list.pick_locators(invalid_items)

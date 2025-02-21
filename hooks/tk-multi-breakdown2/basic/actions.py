# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook that loads defines all the available actions, broken down by publish type.
"""

import sgtk
from tank import TankError


HookBaseClass = sgtk.get_hook_baseclass()


class AliasBreakdown2Actions(HookBaseClass):
    """
    Hook to define actions for file items in the Breakdown2 App for Alias.

    This uses the same interface as the hooks/tk-mutl-loader2/basic/scene_actions.py
    """

    def __init__(self, *args, **kwargs):
        """Initialize the hook."""

        super().__init__(*args, **kwargs)
        self.alias_py = self.parent.engine.alias_py

    def generate_actions(self, sg_publish_data, actions, ui_area):
        """
        Returns a list of action instances for a particular publish.
        This method is called each time a user clicks a publish somewhere in the UI.
        The data returned from this hook will be used to populate the actions menu for a publish.

        The mapping between Publish types and actions are kept in a different place
        (in the configuration) so at the point when this hook is called, the loader app
        has already established *which* actions are appropriate for this object.

        The hook should return at least one action for each item passed in via the
        actions parameter.

        This method needs to return detailed data for those actions, in the form of a list
        of dictionaries, each with name, params, caption and description keys.

        Because you are operating on a particular publish, you may tailor the output
        (caption, tooltip etc) to contain custom information suitable for this publish.

        The ui_area parameter is a string and indicates where the publish is to be shown.
        - If it will be shown in the main browsing area, "main" is passed.
        - If it will be shown in the details area, "details" is passed.
        - If it will be shown in the history area, "history" is passed.

        Please note that it is perfectly possible to create more than one action "instance" for
        an action! You can for example do scene introspection - if the action passed in
        is "character_attachment" you may for example scan the scene, figure out all the nodes
        where this object can be attached and return a list of action instances:
        "attach to left hand", "attach to right hand" etc. In this case, when more than
        one object is returned for an action, use the params key to pass additional
        data into the run_action hook.

        :param sg_publish_data: Flow Production Tracking data dictionary with all the standard publish fields.
        :param actions: List of action strings which have been defined in the app configuration.
        :param ui_area: String denoting the UI Area (see above).
        :returns List of dictionaries, each with keys name, params, caption and description
        """

        self.logger.debug(
            "Generate actions called for UI element %s. "
            "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_publish_data)
        )

        action_instances = []

        if "remove_reference" in actions:
            action_instances.append(
                {
                    "name": "remove_reference",
                    "params": {"file_item": None},
                    "caption": "Remove File",
                    "description": "This will remove the reference file from the Alias universe.",
                }
            )

        return action_instances

    def execute_action(self, name, params, sg_publish_data):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.

        :param name: Action name string representing one of the items returned by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_publish_data: Flow Production Tracking data dictionary with all the standard publish fields.
        :returns: No return value expected.
        """

        self.logger.debug(
            "Execute action called for action %s. "
            "Parameters: %s. Publish Data: %s" % (name, params, sg_publish_data)
        )

        file_item = params.get("file_item")
        if not file_item:
            raise TankError(
                "Failed to execute action {name}. Missing param 'file_item'.".format(
                    name=name
                )
            )

        path = file_item.get("path")
        if not path:
            raise TankError(
                "Failed to execute action {name}. Missing reference file path in FileItem.".format(
                    name=name
                )
            )

        reference = self.alias_py.get_reference_by_path(path)
        if not reference:
            raise TankError(
                "Failed to execute action {name}. Failed to find Alias reference with path {path}.".format(
                    name=name, path=path
                )
            )

        if name == "remove_reference":
            self.alias_py.remove_reference(reference)

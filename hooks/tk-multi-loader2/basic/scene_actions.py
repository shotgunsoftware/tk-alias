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

import os

import sgtk
from sgtk.platform.qt import QtGui

HookBaseClass = sgtk.get_hook_baseclass()


class AliasActions(HookBaseClass):
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

        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        :param actions: List of action strings which have been defined in the app configuration.
        :param ui_area: String denoting the UI Area (see above).
        :returns List of dictionaries, each with keys name, params, caption and description
        """
        app = self.parent
        app.log_debug(
            "Generate actions called for UI element %s. "
            "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_publish_data)
        )
        engine = app.engine
        operations = engine.operations

        action_instances = []
        try:
            # call base class first
            action_instances += HookBaseClass.generate_actions(
                self, sg_publish_data, actions, ui_area
            )
        except AttributeError:
            # base class doesn't have the method, so ignore and continue
            pass

        if "reference" in actions:
            action_instances.append(
                {
                    "name": "reference",
                    "params": None,
                    "caption": "Create Reference",
                    "description": "This will add the item to the universe as a standard reference.",
                }
            )

        if "import" in actions:
            action_instances.append(
                {
                    "name": "import",
                    "params": None,
                    "caption": "Import into Scene",
                    "description": "This will import the item into the current universe.",
                }
            )

        if "import_as_reference" in actions:
            action_instances.append(
                {
                    "name": "import_as_reference",
                    "params": None,
                    "caption": "Import as Reference",
                    "description": "This will import the item as a reference into the current universe.",
                }
            )

        if "texture_node" in actions:
            action_instances.append(
                {
                    "name": "texture_node",
                    "params": None,
                    "caption": "Import into Scene",
                    "description": "This will import the item into the current universe.",
                }
            )

        if "import_subdiv" in actions and operations.is_subdiv_supported():
            action_instances.append(
                {
                    "name": "import_subdiv",
                    "params": None,
                    "caption": "Import Subdiv file into Scene",
                    "description": "This will import the subdiv item into the current universe.",
                }
            )

        return action_instances

    def execute_action(self, name, params, sg_publish_data):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.

        :param name: Action name string representing one of the items returned by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        :returns: No return value expected.
        """
        app = self.parent
        engine = app.engine
        operations = engine.operations

        app.log_debug(
            "Execute action called for action %s. "
            "Parameters: %s. Publish Data: %s" % (name, params, sg_publish_data)
        )

        # resolve path
        path = self.get_publish_path(sg_publish_data)

        if name == "reference":
            return operations.create_reference(path, standalone=False)

        elif name == "import":
            return operations.import_file(path, create_stage=False, standalone=False)

        elif name == "import_as_reference":
            # use the current path as source
            source_path = path

            # calculate output path using template or the source path folder
            output_path = operations.get_import_as_reference_output_path(source_path)

            # if the output path couldn't be calculated
            if not output_path:
                raise Exception("Error importing the file as reference")

            # if the output path doesn't exist, create it using the alias-translations framework
            if not os.path.exists(output_path):
                framework_aliastranslations = self.load_framework(
                    "tk-framework-aliastranslations_v0.x.x"
                )
                if not framework_aliastranslations:
                    raise Exception("Could not run alias translations")

                tk_framework_aliastranslations = framework_aliastranslations.import_module(
                    "tk_framework_aliastranslations"
                )
                alias_translator = tk_framework_aliastranslations.Translator(
                    source_path, output_path
                )
                alias_translator.execute()

            return operations.create_reference(output_path, standalone=False)

        elif name == "texture_node":
            return operations.create_texture_node(path, standalone=False)

        elif name == "import_subdiv":
            return operations.import_subdiv(path, standalone=False)

    def execute_multiple_actions(self, actions):
        """
        Executes the specified action on a list of items.

        The default implementation dispatches each item from ``actions`` to
        the ``execute_action`` method.

        The ``actions`` is a list of dictionaries holding all the actions to execute.
        Each entry will have the following values:

            name: Name of the action to execute
            sg_publish_data: Publish information coming from Shotgun
            params: Parameters passed down from the generate_actions hook.

        .. note::
            This is the default entry point for the hook. It reuses the ``execute_action``
            method for backward compatibility with hooks written for the previous
            version of the loader.

        .. note::
            The hook will stop applying the actions on the selection if an error
            is raised midway through.

        :param list actions: Action dictionaries.
        """
        messages = {}

        for single_action in actions:
            name = single_action["name"]

            sg_publish_data = single_action["sg_publish_data"]
            params = single_action["params"]
            message = self.execute_action(name, params, sg_publish_data)

            if not isinstance(message, dict):
                continue

            message_type = message.get("message_type")
            message_code = message.get("message_code")
            publish_path = message.get("publish_path")
            is_error = message.get("is_error")

            if message_type not in messages:
                messages[message_type] = {}

            if message_code not in messages[message_type]:
                messages[message_type][message_code] = dict(is_error=is_error, paths=[])

            messages[message_type][message_code]["paths"].append(publish_path)

        active_window = QtGui.QApplication.activeWindow()
        for message_type, message_type_details in messages.items():
            content = ""
            for message_code, message_code_details in message_type_details.items():
                if content:
                    content += "\n\n"

                is_error = message_code_details.get("is_error")
                paths = message_code_details.get("paths")

                if is_error:
                    content += "{}: {}".format(message_code, ", ".join(paths))
                else:
                    if len(paths) == 1:
                        content += "{}: {}".format(message_code, paths[0])
                    else:
                        content += "{} ({})".format(message_code, len(paths))

            getattr(QtGui.QMessageBox, message_type)(
                active_window, message_type.title(), content
            )

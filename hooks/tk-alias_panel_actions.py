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
import os
import commands

HookBaseClass = sgtk.get_hook_baseclass()

class AliasActions(HookBaseClass):

    ##############################################################################################################
    # public interface - to be overridden by deriving classes

    def generate_actions(self, sg_data, actions, ui_area):
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

        :param sg_data: Shotgun data dictionary with all the standard publish fields.
        :param actions: List of action strings which have been defined in the app configuration.
        :param ui_area: String denoting the UI Area (see above).
        :returns List of dictionaries, each with keys name, params, caption and description
        """
        app = self.parent
        app.log_debug("Generate actions called for UI element %s. "
                      "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_data))
        action_instances = []

        if "assign_task" in actions:
            action_instances.append({
                "name": "assign_task",
                "params": None,
                "caption": "Assign Task to yourself",
                "description": "Assign this task to yourself."
            })

        if "task_to_ip" in actions:
            action_instances.append({
                "name": "task_to_ip",
                "params": None,
                "caption": "Set to In Progress",
                "description": "Set the task status to In Progress."
            })

        if "reference" in actions:
            action_instances.append({
                "name": "reference",
                "params": None,
                "caption": "Create Reference",
                "description": "This will add the item to the universe as a standard reference."
            })

        if "import" in actions:
            action_instances.append({
                "name": "import",
                "params": None,
                "caption": "Import into Scene",
                "description": "This will import the item into the current universe."
            })

        if "texture_node" in actions:
            action_instances.append({
                "name": "texture_node",
                "params": None,
                "caption": "Import into Scene",
                "description": "This will import the item into the current universe."
            })

        if "publish_clipboard" in actions:
            if "path" in sg_data and sg_data["path"].get("local_path"):
                # path field exists and the local path is populated
                action_instances.append({
                    "name": "publish_clipboard",
                    "params": None,
                    "caption": "Copy path to clipboard",
                    "description": "Copy the path associated with this publish to the clipboard."
                })

        return action_instances

    def execute_action(self, name, params, sg_data):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.

        :param name: Action name string representing one of the items returned by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_data: Shotgun data dictionary with all the standard publish fields.
        :returns: No return value expected.
        """
        app = self.parent
        app.log_debug("Execute action called for action %s. "
                      "Parameters: %s. Publish Data: %s" % (name, params, sg_data))

        if name == "assign_task":
            if app.context.user is None:
                raise Exception("Cannot establish current user!")

            data = app.shotgun.find_one("Task", [["id", "is", sg_data["id"]]], ["task_assignees"] )
            assignees = data["task_assignees"] or []
            assignees.append(app.context.user)
            app.shotgun.update("Task", sg_data["id"], {"task_assignees": assignees})
        elif name == "task_to_ip":
            app.shotgun.update("Task", sg_data["id"], {"sg_status_list": "ip"})
        elif name == "publish_clipboard":
            self._copy_to_clipboard(sg_data["path"]["local_path"])
        else:
            # resolve path
            path = self.get_publish_path(sg_data)

            if name == "reference":
                self._create_reference(path, sg_data)

            if name == "import":
                self._do_import(path, sg_data)

            if name == "texture_node":
                self._create_texture_node(path, sg_data)


    ##############################################################################################################
    # helper methods which can be subclassed in custom hooks to fine tune the behaviour of things

    def _create_reference(self, path, sg_data):
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        namespace = "%s %s" % (sg_data.get("entity").get("name"), sg_data.get("name"))
        namespace = namespace.replace(" ", "_")

        self.parent.engine.send_to_alias(commands.FileLoadCommand(path, True, namespace).to_string())

    def _do_import(self, path, sg_data):
        """
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        self.parent.engine.send_to_alias(commands.FileLoadCommand(path, False).to_string())

    def _create_texture_node(self, path, sg_data):
        """
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        self.parent.engine.send_to_alias(commands.LoadImageCommand(path).to_string())

    def _copy_to_clipboard(self, text):
        """
        Helper method - copies the given text to the clipboard

        :param text: content to copy
        """
        from sgtk.platform.qt import QtCore, QtGui
        app = QtCore.QCoreApplication.instance()
        app.clipboard().setText(text)

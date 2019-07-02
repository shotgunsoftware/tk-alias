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
from sgtk.platform.qt import QtGui

HookBaseClass = sgtk.get_hook_baseclass()


class AliasActions(HookBaseClass):
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
        try:
            # call base class first
            action_instances += HookBaseClass.generate_actions(self, sg_data, actions, ui_area)
        except AttributeError:
            # base class doesn't have the method, so ignore and continue
            pass

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
            # action_instances.append({
            #     "name": "import_new",
            #     "params": None,
            #     "caption": "Import into New Stage",
            #     "description": "This will import the item into a new scene."
            # })

        if "texture_node" in actions:
            action_instances.append({
                "name": "texture_node",
                "params": None,
                "caption": "Import into Scene",
                "description": "This will import the item into the current universe."
            })

        return action_instances


    def execute_multiple_actions(self, actions):
        """
        Executes the specified action on a list of items.

        The default implementation dispatches each item from ``actions`` to
        the ``execute_action`` method.

        The ``actions`` is a list of dictionaries holding all the actions to
        execute.
        Each entry will have the following values:

            name: Name of the action to execute
            sg_data: Publish information coming from Shotgun
            params: Parameters passed down from the generate_actions hook.

        .. note::
            This is the default entry point for the hook. It reuses the
            ``execute_action`` method for backward compatibility with hooks
            written for the previous version of the loader.

        .. note::
            The hook will stop applying the actions on the selection if an error
            is raised midway through.

        :param list actions: Action dictionaries.
        """
        for single_action in actions:
            name = single_action["name"]
            sg_publish_data = single_action["sg_publish_data"]
            params = single_action["params"]

            self.execute_action(name, params, sg_publish_data)

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

        if name == "reference":
            path = self.get_publish_path(sg_data)
            self._create_reference(path, sg_data)

        elif name == "import":
            path = self.get_publish_path(sg_data)
            self._do_import(path, sg_data, create_stage=False)

        elif name == "import_new":
            path = self.get_publish_path(sg_data)
            self._do_import(path, sg_data, create_stage=True)

        elif name == "texture_node":
            path = self.get_publish_path(sg_data)
            self._create_texture_node(path, sg_data)

        else:
            try:
                HookBaseClass.execute_action(self, name, params, sg_data)
            except AttributeError, e:
                # base class doesn't have the method, so ignore and continue
                pass


    def _create_reference(self, path, sg_data):
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        namespace = "%s %s" % (sg_data.get("entity").get("name"), sg_data.get("name"))
        namespace = namespace.replace(" ", "_")

        command = commands.FileLoadCommand(path, True, namespace)
        message = self.parent.engine.send_and_wait(command)
        if message and message.has_key("initialCommand") and (message["initialCommand"] == command.command):
            if message.has_key("status"):
                if (message["status"] == "ok"):
                    QtGui.QMessageBox.information(
                        QtGui.QApplication.activeWindow(),
                        "Create Reference",
                        "File '{!r}' referenced successfully.".format(
                            sg_data.get("name","NO NAME")
                        )
                    )
                elif (message["status"] == "already referenced"):
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Create Reference",
                        "The selected file {!r} is already referenced. Different versions are treated as the same file".format(
                          sg_data.get("name", "NO NAME")
                        )
                    )
                elif (message["status"] == "invalid json"):
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Create Reference",
                        "Unexpected JSON structure or JSON field value with the file {!r}".format(
                            sg_data.get("name", "NO NAME")
                        )
                    )
                else:
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Create Reference",
                        "An error occurred when referencing the file {!r}.".format(
                            sg_data.get("name","NO NAME")
                        )
                    )

    def _do_import(self, path, sg_data, create_stage):
        """
        Import a file into the current scene.
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        if create_stage:
            command = commands.StageOpenCommand(path)
        else:
            command = commands.FileLoadCommand(path, False, create_stage=create_stage)
        message = self.parent.engine.send_and_wait(command)
        if message and message.has_key("initialCommand") and (message["initialCommand"] == command.command):
            if message.has_key("status"):
                if message["status"] == "ok":
                    QtGui.QMessageBox.information(
                        QtGui.QApplication.activeWindow(),
                        "Import File",
                        "File '{!r}' imported successfully.".format(
                            sg_data.get("name","NO NAME")
                        )
                    )
                elif message["status"] == "invalid json":
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Import File",
                        "Unexpected JSON structure or JSON field value with the file {!r}".format(
                            sg_data.get("name", "NO NAME")
                        )
                    )
                else:
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Import File",
                        "The selected file {!r} could not be imported ({}).".format(
                            sg_data.get("name","NO NAME"),
                            message["status"]
                        )
                    )

    def _create_texture_node(self, path, sg_data):
        """
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        command = commands.LoadImageCommand(path)
        message = self.parent.engine.send_and_wait(command)
        if message and message.has_key("initialCommand") and (message["initialCommand"] == command.command):
            if message.has_key("status"):
                if message["status"] == "ok":
                    QtGui.QMessageBox.information(
                        QtGui.QApplication.activeWindow(),
                        "Import Image",
                        "File '{!r}' imported successfully.".format(
                            sg_data.get("name","NO NAME")
                        )
                    )
                elif message["status"] == "invalid json":
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Import Image",
                        "Unexpected JSON structure or JSON field value with the file {!r}".format(
                            sg_data.get("name", "NO NAME")
                        )
                    )
                else:
                    QtGui.QMessageBox.warning(
                        QtGui.QApplication.activeWindow(),
                        "Import Image",
                        "An error occurred when creating the canvas with the file {!r}.".format(
                            sg_data.get("name","NO NAME"),
                            message["status"]
                        )
                    )
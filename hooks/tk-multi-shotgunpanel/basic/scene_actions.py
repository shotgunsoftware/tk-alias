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
import alias_api

HookBaseClass = sgtk.get_hook_baseclass()


class AliasActions(HookBaseClass):
    """
    Shotgun Panel Actions for Alias
    """

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

        self.logger.debug(
            "Generate actions called for UI element %s. "
            "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_data)
        )

        action_instances = []
        try:
            # call base class first
            action_instances += HookBaseClass.generate_actions(
                self, sg_data, actions, ui_area
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
                    "caption": "Create Canvas",
                    "description": "This will import the item into the current universe.",
                }
            )

        if "import_subdiv" in actions and hasattr(alias_api, "import_subdivision"):
            action_instances.append(
                {
                    "name": "import_subdiv",
                    "params": None,
                    "caption": "Import Subdiv file into Scene",
                    "description": "This will import the subdiv item into the current universe.",
                }
            )

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

        self.logger.debug(
            "Execute action called for action %s. "
            "Parameters: %s. Shotgun Data: %s" % (name, params, sg_data)
        )

        if name == "reference":
            path = self.get_publish_path(sg_data)
            self._create_reference(path)

        elif name == "import":
            path = self.get_publish_path(sg_data)
            self._import_file(path)

        elif name == "import_as_reference":
            path = self.get_publish_path(sg_data)
            self._import_file_as_reference(path)

        elif name == "texture_node":
            path = self.get_publish_path(sg_data)
            self._create_texture_node(path)

        elif name == "import_subdiv":
            path = self.get_publish_path(sg_data)
            self._import_subdivision(path)

        else:
            try:
                HookBaseClass.execute_action(self, name, params, sg_data)
            except AttributeError:
                # base class doesn't have the method, so ignore and continue
                pass

    def execute_multiple_actions(self, actions):
        """
        Executes the specified action on a list of items.

        The default implementation dispatches each item from ``actions`` to
        the ``execute_action`` method.

        The ``actions`` is a list of dictionaries holding all the actions to execute.
        Each entry will have the following values:

            name: Name of the action to execute
            sg_data: Publish information coming from Shotgun
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
        for single_action in actions:
            name = single_action["name"]
            sg_data = single_action["sg_data"]
            params = single_action["params"]
            self.execute_action(name, params, sg_data)

    def _create_reference(self, path):
        """
        Create an Alias reference.

        :param path: Path to the file.
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)
        alias_api.create_reference(path)

    def _import_file(self, path):
        """
        Import the file into the current Alias session.

        :param path: Path to file.
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)
        alias_api.import_file(path)

    def _import_file_as_reference(self, path):
        """
        Import the file as an Alias reference, converting it on the fly as wref.

        :param path: Path to the file.
        """

        reference_template = self.parent.engine.get_template("reference_template")
        source_template = self.sgtk.template_from_path(path)

        # get the path to the reference, using the templates if it's possible otherwise using the source path
        # location
        if reference_template and source_template:
            template_fields = source_template.get_fields(path)
            template_fields["alias.extension"] = os.path.splitext(path)[-1][1:]
            reference_path = reference_template.apply_fields(template_fields)
        else:
            output_path, output_ext = os.path.splitext(path)
            reference_path = "{output_path}_{output_ext}.wref".format(
                output_path=output_path, output_ext=output_ext[1:]
            )

        # if the reference file doesn't exist on disk yet, run the translation
        if not os.path.exists(reference_path):

            framework = self.load_framework("tk-framework-aliastranslations_v0.x.x")
            if not framework:
                raise Exception("Couldn't find tk-framework-aliastranslations_v0.x.x")
            tk_framework_aliastranslations = framework.import_module(
                "tk_framework_aliastranslations"
            )

            translator = tk_framework_aliastranslations.Translator(path, reference_path)
            translator.execute()

        alias_api.create_reference(reference_path)

    def _create_texture_node(self, path):
        """
        Import an image as Canvas in Alias

        :param path:  Path to the image.
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)
        alias_api.create_texture_node(path)

    def _import_subdivision(self, path):
        """
        Import a file as subdivision in the current Alias session.

        :param path: Path to the file.
        """
        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)
        alias_api.import_subdivision(path)

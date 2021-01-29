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
from sgtk.util import LocalFileStorageManager

import alias_api


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

        self.logger.debug(
            "Generate actions called for UI element %s. "
            "Actions: %s. Publish Data: %s" % (ui_area, actions, sg_publish_data)
        )

        action_instances = []

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
        for single_action in actions:
            name = single_action["name"]
            sg_publish_data = single_action["sg_publish_data"]
            params = single_action["params"]
            self.execute_action(name, params, sg_publish_data)

    def execute_action(self, name, params, sg_publish_data):
        """
        Execute a given action. The data sent to this be method will
        represent one of the actions enumerated by the generate_actions method.

        :param name: Action name string representing one of the items returned by generate_actions.
        :param params: Params data, as specified by generate_actions.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        :returns: No return value expected.
        """

        self.logger.debug(
            "Execute action called for action %s. "
            "Parameters: %s. Publish Data: %s" % (name, params, sg_publish_data)
        )

        # resolve path
        path = self.get_publish_path(sg_publish_data)

        if name == "reference":
            self._create_reference(path)

        elif name == "import":
            self._import_file(path)

        elif name == "import_as_reference":
            self._import_file_as_reference(path, sg_publish_data)

        elif name == "texture_node":
            self._create_texture_node(path)

        elif name == "import_subdiv":
            self._import_subdivision(path)

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

    def _import_file_as_reference(self, path, sg_publish_data):
        """
        Import the file as an Alias reference, converting it on the fly as wref.

        :param path:            Path to the file.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields
        """

        # get the tank of the project the file we're trying to import belongs to
        # this will be useful to manipulate configuration settings and templates
        tk = self.__get_tank_instance(sg_publish_data)

        # then, get the reference template and the source template to be able to extract fields and build the path to
        # the translated file
        reference_template = self._get_reference_template(tk, sg_publish_data)
        source_template = tk.template_from_path(path)

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

    def _get_reference_template(self, tk, sg_publish_data):
        """
        Get the template to use to build the path to the reference file

        :param tk:              Tank instance we are using to get configuration settings and templates
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields
        :returns: The reference template if found, None otherwise.
        """

        if not tk:
            return None

        if "task" in sg_publish_data.keys() and sg_publish_data["task"]:
            ctx = tk.context_from_entity_dictionary(sg_publish_data["task"])
            if ctx:
                env = sgtk.platform.engine.get_environment_from_context(tk, ctx)
                engine_settings = env.get_engine_settings(self.parent.engine.name)
                reference_template_name = engine_settings.get("reference_template")
                if reference_template_name:
                    return tk.templates.get(reference_template_name)

        return None

    def __get_tank_instance(self, sg_publish_data):
        """
        Get the tank instance we will use to get configuration settings and templates. As this instance is project and
        configuration related, we need to be sure to query the right config in order to get it.

        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields
        :returns: A :class`sgtk.Sgtk` instance pointing at the right configuration according to the published file
                  project.
        """

        # first of all, we need to determine if the file we're trying to import lives in the current project or in
        # another one
        in_current_project = (
            sg_publish_data["project"]["id"] == self.parent.context.project["id"]
        )

        if in_current_project:
            return self.parent.sgtk

        # if the file we're trying to import lives in another project, we need to access the configuration used by this
        # project in order to get the right configuration settings
        else:

            pc_local_path = self.__get_pipeline_configuration_local_path(
                sg_publish_data["project"]["id"]
            )
            if not pc_local_path:
                self.logger.warning(
                    "Couldn't get tank instance for project {}.".format(
                        sg_publish_data["project"]["id"]
                    )
                )
                return None

            return sgtk.sgtk_from_path(pc_local_path)

    def __get_pipeline_configuration_local_path(self, project_id):
        """
        Get the path to the local configuration (the one which stands in the Sgtk cache folder) in order to be able
        to build a :class`sgtk.Sgtk` instance from this path

        :param project_id: Id of the project we want to retrieve the config for
        :returns: The local path to the config if we could determine which config to use, None otherwise.
        """

        plugin_id = "basic.desktop"

        # first, start the toolkit manager to get all the pipeline configurations related to the distant project
        # here, we are going to use the default plugin id "basic.*" to find the pipeline configurations
        mgr = sgtk.bootstrap.ToolkitManager()
        mgr.plugin_id = sgtk.commands.constants.DEFAULT_PLUGIN_ID
        pipeline_configurations = mgr.get_pipeline_configurations(
            {"type": "Project", "id": project_id}
        )

        if not pipeline_configurations:
            self.logger.warning(
                "Couldn't retrieve any pipeline configuration linked to project {}".format(
                    project_id
                )
            )
            return

        if len(pipeline_configurations) == 1:
            pipeline_config = pipeline_configurations[0]

        else:

            # try to determine which configuration we want to use:
            # 1- if one and only one pipeline configuration is restricted to this project, use it
            # 2- if one pipeline configuration is named Primary and linked to this project, use it
            # 3- reject all the other cases

            pipeline_config = self.__get_project_pipeline_configuration(
                pipeline_configurations, project_id
            )

            if not pipeline_config:
                pipeline_config = self.__get_primary_pipeline_configuration(
                    pipeline_configurations, project_id
                )

        if not pipeline_config:
            self.logger.warning(
                "Couldn't get the pipeline configuration linked to project {}: too many configurations".format(
                    project_id
                )
            )
            return None

        config_local_path = LocalFileStorageManager.get_configuration_root(
            self.sgtk.shotgun_url,
            project_id,
            plugin_id,
            pipeline_config["id"],
            LocalFileStorageManager.CACHE,
        )

        return os.path.join(config_local_path, "cfg")

    def __get_project_pipeline_configuration(self, pipeline_configurations, project_id):
        """
        Parse the pipeline configuration list in order to find if one of them is only used by this project.

        :param pipeline_configurations: List of pipeline configurations to parse
        :param project_id:              Id of the project we want to get the pipeline configuration for
        :returns: The pipeline configuration if only one config has been defined for this project, None otherwise.
        """

        pipeline_configuration = None

        for pc in pipeline_configurations:
            if not pc["project"]:
                continue
            if pc["project"]["id"] == project_id:
                if pipeline_configuration:
                    return None
                pipeline_configuration = pc

        return pipeline_configuration

    def __get_primary_pipeline_configuration(self, pipeline_configurations, project_id):
        """
        Parse the pipeline configuration list in order to find if one of them has been defined as "Primary" for this
        project.

        :param pipeline_configurations: List of pipeline configurations to parse
        :param project_id:              Id of the project we want to get the pipeline configuration for
        :returns: The pipeline configuration if a "Primary" config has been found for this project, None otherwise.
        """

        for pc in pipeline_configurations:
            if (
                pc["project"]
                and pc["project"]["id"] == project_id
                and pc["name"] == sgtk.commands.constants.PRIMARY_PIPELINE_CONFIG_NAME
            ):
                return pc

        return None

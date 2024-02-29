# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

import sgtk
from tank import TankError

HookBaseClass = sgtk.get_hook_baseclass()


class AliasSessionCollector(HookBaseClass):
    """
    Collector that operates on the alias session. Should inherit from the basic
    collector hook.
    """

    @property
    def settings(self):
        collector_settings = super(AliasSessionCollector, self).settings or {}
        alias_session_settings = {
            # "Work Template": {
            #     "type": "template",
            #     "default": None,
            #     "description": "Template path for artist work files. Should "
            #     "correspond to a template defined in "
            #     "templates.yml. If configured, is made available"
            #     "to publish plugins via the collected item's "
            #     "properties. ",
            # },
            # "Background Processing": {
            #     "type": "bool",
            #     "default": False,
            #     "description": "Boolean to turn on/off the background publishing process.",
            # },
        }

        collector_settings.update(alias_session_settings)

        return collector_settings

    def _collect_file(self, parent_item, path, frame_sequence=False):
        """
        Process the supplied file path.

        :param parent_item: parent item instance
        :param path: Path to analyze
        :param frame_sequence: Treat the path as a part of a sequence
        :returns: The item that was created
        """

        # make sure the path is normalized. no trailing separator, separators
        # are appropriate for the current os, no double separators, etc.
        path = sgtk.util.ShotgunPath.normalize(path)

        publisher = self.parent

        # get info for the extension
        item_info = self._get_item_info(path)
        item_type = item_info["item_type"]
        type_display = item_info["type_display"]
        evaluated_path = path
        is_sequence = False

        if frame_sequence:
            # replace the frame number with frame spec
            seq_path = publisher.util.get_frame_sequence_path(path)
            if seq_path:
                evaluated_path = seq_path
                type_display = "%s Sequence" % (type_display,)
                item_type = "%s.%s" % (item_type, "sequence")
                is_sequence = True

        display_name = publisher.util.get_publish_name(path, sequence=is_sequence)

        # create and populate the item
        file_item = parent_item.create_item(item_type, type_display, display_name)
        file_item.set_icon_from_path(item_info["icon_path"])

        # if the supplied path is an image, use the path as the thumbnail.
        if item_type.startswith("file.image") or item_type.startswith("file.texture"):
            file_item.set_thumbnail_from_path(path)

            # disable thumbnail creation since we get it for free
            file_item.thumbnail_enabled = False
        else:
            # Try to generate a thumbnail from the file
            try:
                file_item.thumbnail = publisher.util.get_thumbnail(
                    path, file_item.context
                )
            except TankError as tank_error:
                self.logger.error(
                    f"Failed to generate thumbnail for {path}. Error {tank_error}"
                )
            except Exception as error:
                self.logger.error(
                    f"Unexepcted error occured while attempting to generate thumbnail for {path}. Error {error}"
                )

        # all we know about the file is its path. set the path in its
        # properties for the plugins to use for processing.
        file_item.properties["path"] = evaluated_path

        if is_sequence:
            # include an indicator that this is an image sequence and the known
            # file that belongs to this sequence
            file_item.properties["sequence_paths"] = [path]

        self.logger.info("Collected file: %s" % (evaluated_path,))

        # 
        # Alias publishing
        # 

        # The alias framework is required to launch Alias with the correct plugin
        framework_location = self.__get_framework_location("tk-framework-alias")
        if framework_location is None:
            raise Exception("tk-framework-alias not found")

        # FIXME use software launcher to find paths to exe
        os.environ["ALIAS_PLUGIN_CLIENT_ALIAS_EXECPATH"] = "C:\\Program Files\\Autodesk\\AliasAutoStudio2024.0\\bin\\Alias.exe"
        os.environ["ALIAS_PLUGIN_CLIENT_ALIAS_VERSION"] = "2024.0"

        # Import the alias api module
        bootstrap_python_path = os.path.join(framework_location, "python")
        import sys
        sys.path.insert(0, bootstrap_python_path)
        import tk_framework_alias.server.api as api
        # import tk_framework_alias_utils.startup as startup_utils
        sys.path.remove(bootstrap_python_path)



        # create the session item for the publish hierarchy
        session_item = file_item.create_item(
            "alias.standalone", display_name, "Alias Publish"
        )

        # get the icon path to display for this item
        icon_path = os.path.join(self.disk_location, os.pardir, "icons", "alias.png")
        session_item.set_icon_from_path(icon_path)

        # add a new item for Alias translations to separate them from the main session item
        translation_item = session_item.create_item(
            "alias.standalone.translation", "Alias Translations", "All Alias Translations"
        )
        translation_item.properties["alias_api"] = api.alias_api
        translation_item.properties["path"] = evaluated_path
        # Add it as global import instead
        sys_module_name = "alias_api"
        sys.modules[sys_module_name] = api.alias_api

        return file_item

    def __get_framework_location(self, framework_name):
        """
        Return the file path to the framework bundle.

        :param framework_name: The name of the framework.
        :type framework_name: str

        :return: The file path to the framework bundle.
        :rtype: str
        """

        # FIXME
        framework_and_version = "tk-framework-alias_v1.x.x"
        # framework_and_version = None
        # for framework in self.descriptor.get_required_frameworks():
        #     if framework.get("name") == framework_name:
        #         name_parts = [framework["name"]]
        #         if "version" in framework:
        #             name_parts.append(framework["version"])
        #         framework_and_version = "_".join(name_parts)
        #         break
        # else:
        #     self.logger.error(f"Failed to find location for framework {framework_name}")
        #     return

        # First get the environment object from the current engine and config
        engine = sgtk.platform.current_engine()
        env_name = engine.environment.get("name")
        env = engine.sgtk.pipeline_configuration.get_environment(env_name)

        # Get the framework descriptor from the environment object
        # self.logger.debug(
        #     f"Getting framework descriptor {framework_name} from '{framework}'"
        # )
        framework_desc = env.get_framework_descriptor(framework_and_version)

        self.logger.debug(f"Found framework descriptor {framework_desc}")
        return framework_desc.get_path()
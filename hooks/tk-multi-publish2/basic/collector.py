﻿# Copyright (c) 2017 Shotgun Software Inc.
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
import alias_api

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
            "Work Template": {
                "type": "template",
                "default": None,
                "description": "Template path for artist work files. Should "
                "correspond to a template defined in "
                "templates.yml. If configured, is made available"
                "to publish plugins via the collected item's "
                "properties. ",
            },
            "Background Processing": {
                "type": "bool",
                "default": False,
                "description": "Boolean to turn on/off the background publishing process.",
            },
        }

        collector_settings.update(alias_session_settings)

        return collector_settings

    def process_current_session(self, settings, parent_item):
        """
        Analyzes the current scene open in a DCC and parents a subtree of items
        under the parent_item passed in.

        :param dict settings: Configured settings for this collector
        :param parent_item: Root item instance
        """
        publisher = self.parent

        # store the Batch Processing settings in the root item properties
        bg_processing = settings.get("Background Processing")
        if bg_processing:
            parent_item.properties["bg_processing"] = bg_processing.value

        # get the path to the current file
        path = alias_api.get_current_path()

        # determine the display name for the item
        if path:
            file_info = publisher.util.get_file_path_components(path)
            display_name = file_info["filename"]
        else:
            display_name = "Current Alias Session"

        # create the session item for the publish hierarchy
        session_item = parent_item.create_item(
            "alias.session", "Alias Session", display_name
        )

        # get the icon path to display for this item
        icon_path = os.path.join(self.disk_location, os.pardir, "icons", "alias.png")
        session_item.set_icon_from_path(icon_path)

        # add a new item for Alias translations to separate them from the main session item
        translation_item = session_item.create_item(
            "alias.session.translation", "Alias Translations", "All Alias Translations"
        )

        # if a work template is defined, add it to the item properties so
        # that it can be used by attached publish plugins
        work_template_setting = settings.get("Work Template")
        if work_template_setting:

            work_template = publisher.engine.get_template_by_name(
                work_template_setting.value
            )

            # store the template on the item for use by publish plugins. we
            # can't evaluate the fields here because there's no guarantee the
            # current session path won't change once the item has been created.
            # the attached publish plugins will need to resolve the fields at
            # execution time.
            session_item.properties["work_template"] = work_template
            translation_item.properties["work_template"] = work_template
            self.logger.debug("Work template defined for Alias collection.")

        # add a new item for all VRED publish plugins related
        vred_item = session_item.create_item(
            "alias.session.vred", "VRED Scene", "VRED render items"
        )
        icon_path = os.path.join(self.disk_location, os.pardir, "icons", "vred.png")
        vred_item.set_icon_from_path(icon_path)

        self.logger.info("Collected current Alias file")

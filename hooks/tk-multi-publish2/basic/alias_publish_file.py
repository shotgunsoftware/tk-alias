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

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishFilePlugin(HookBaseClass):
    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(AliasPublishFilePlugin, self).settings or {}

        # settings specific to this class
        publish_settings = {
            "Publish Template": {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        base_settings.update(publish_settings)

        workfile_settings = {
            "Work Template": {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        base_settings.update(workfile_settings)

        return base_settings

    def validate(self, settings, item):
        publisher = self.parent

        publish_template_setting = settings.get("Publish Template")
        publish_template = publisher.engine.get_template_by_name(publish_template_setting.value)

        if not publish_template:
            return False

        if publish_template:
            item.properties["publish_template"] = publish_template

        workfile_template_setting = settings.get("Work Template")
        workfile_template = publisher.engine.get_template_by_name(workfile_template_setting.value)

        if not workfile_template:
            return False

        item.properties["work_template"] = workfile_template
        path = item.properties["path"]

        (next_version_path, version) = self._get_next_version_info(path, item)
        if not next_version_path:
            error_msg = "There's not a suitable next version path for this file."
            self.logger.error(error_msg)
            raise Exception(error_msg)

        if os.path.exists(next_version_path):
            error_msg = "The next version of this file already exists on disk."
            self.logger.error(error_msg)
            raise Exception(error_msg)

        item.properties["next_version_path"] = next_version_path

        return True

    def publish(self, settings, item):
        publisher = self.parent
        engine = publisher.engine

        engine.save_before_publish(item.properties["path"])
        super(AliasPublishFilePlugin, self).publish(settings, item)
        self.logger.info("Saving new version")
        engine.save_after_publish(item.properties["next_version_path"])

    def accept(self, settings, item):
        """
        Method called by the publisher to determine if an item is of any
        interest to this plugin. Only items matching the filters defined via the
        item_filters property will be presented to this method.

        A publish task will be generated for each item accepted here. Returns a
        dictionary with the following booleans:

            - accepted: Indicates if the plugin is interested in this value at
                all. Required.
            - enabled: If True, the plugin will be enabled in the UI, otherwise
                it will be disabled. Optional, True by default.
            - visible: If True, the plugin will be visible in the UI, otherwise
                it will be hidden. Optional, True by default.
            - checked: If True, the plugin will be checked in the UI, otherwise
                it will be unchecked. Optional, True by default.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process

        :returns: dictionary with boolean keys accepted, required and enabled
        """

        return {
            "accepted": True,
            "checked": True,
            "visible": True,
            "enabled": False
        }

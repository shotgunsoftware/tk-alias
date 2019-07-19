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
        engine = publisher.engine
        operations = engine.operations
        path = operations.get_current_path()

        item = super(AliasSessionCollector, self)._collect_file(parent_item, path, frame_sequence=True)

        # get the icon path to display for this item
        icon_path = os.path.join(self.disk_location, os.pardir, "icons", "alias.png")
        item.set_icon_from_path(icon_path)


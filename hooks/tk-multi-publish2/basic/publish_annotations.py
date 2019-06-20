# Copyright (c) 2017 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class PublishAnnotationsPlugin(HookBaseClass):
    @property
    def name(self):
        """
        One line display name describing the plugin
        """
        return "Publish variants to Shotgun"

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["*"]

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
            "visible": True,
            "checked": False,
            "enabled": True
        }

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """
        publisher = self.parent
        engine = publisher.engine
        version_data = item.properties["sg_version_data"]
        annotations = engine.export_annotations()

        if not annotations or not annotations.get("strings"):
            self.logger.info("There are not annotations to export")
            return

        for annotation in annotations.get("strings"):
            note_data = {
                "project": item.context.project,
                "user": item.context.user,
                "subject": "Alias Annotation",
                "content": annotation,
                "note_links": [version_data],
                "tasks": [item.context.task],
            }
            note = publisher.shotgun.create("Note", note_data)

    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once all the publish
        tasks have completed, and can for example be used to version up files.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """
        self.logger.info("Annotations published successfully")

    @property
    def description(self):
        return """
        <p>
            This plugin exports all annotations created using the Locator Annotation tool in Alias. 
        </p>
        <p>
            Each annotation will create a Note in Shotgun. All Notes are linked to this version and file. Use this to 
            sync all review notes made in Alias with Shotgun.
        </p> 
        """

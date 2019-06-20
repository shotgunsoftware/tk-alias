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


class PublishVariantsPlugin(HookBaseClass):
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
        variants = engine.export_variants()

        if not variants or not variants.get("files"):
            self.logger.info("There are not variants to export")
            return

        for variant in variants.get("files"):
            try:
                variant_name, variant_path = variant.split(";")
            except Exception as e:
                engine.logger.exception(e)
                continue

            note_data = {
                "project": item.context.project,
                "user": item.context.user,
                "subject": "Alias Variant",
                "content": variant_name,
                "note_links": [version_data],
                "tasks": [item.context.task],
            }
            note = publisher.shotgun.create("Note", note_data)
            publisher.shotgun.upload(entity_type="Note",
                                     entity_id=note.get("id"),
                                     path=variant_path,
                                     field_name="sg_thumbnail")

    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once all the publish
        tasks have completed, and can for example be used to version up files.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """
        self.logger.info("Variants published successfully")

    @property
    def description(self):
        return """
        <p>
            This plugin exports all Variant images created in Alias and makes a Note in Shotgun for each one. 
        </p>
        <p>  
            All Notes are linked this version & file. Use this to sync all review notes made in Alias with Shotgun. 
        </p>
        <p>
            To see the Variant images that will be exported, check the Alias Variant Lister.
        </p> 
        """

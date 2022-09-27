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
import alias_api

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishVariantsPlugin(HookBaseClass):
    """
    Plugin for publishing variants of the current alias open session
    """

    @property
    def name(self):
        """
        One line display name describing the plugin
        """
        return "Publish Variants to ShotGrid"

    @property
    def description(self):
        return """
        <p>
            This plugin exports all Variant images created in Alias and makes a Note in ShotGrid for each one.
        </p>
        <p>
            All Notes are linked this version & file. Use this to sync all review notes made in Alias with ShotGrid.
        </p>
        <p>
            To see the Variant images that will be exported, check the Alias Variant Lister.
        </p>
        """

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["alias.session"]

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

        if not alias_api.has_variants():
            self.logger.debug("There are not variants to export")
            return {"accepted": False}

        return {"accepted": True, "checked": False}

    def validate(self, settings, item):
        """
        Validates the given item to check that it is ok to publish. Returns a
        boolean to indicate validity.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        :returns: True if item is valid, False otherwise.
        """

        return True

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        # get the publish "mode" stored inside of the root item properties
        bg_processing = item.parent.properties.get("bg_processing", False)
        in_bg_process = item.parent.properties.get("in_bg_process", False)

        # as the alias_api.get_variants() method doesn't work with OpenModel
        # we need to get the variants locally
        if not bg_processing or (bg_processing and not in_bg_process):
            variants = []
            for variant in alias_api.get_variants():
                variants.append((variant.name, variant.path))
            item.properties["alias_variants"] = variants

        if not bg_processing or (bg_processing and in_bg_process):

            publisher = self.parent
            version_data = item.properties.get("sg_version_data")
            publish_data = item.properties["sg_publish_data"]

            # Links, the note will be attached to published file by default
            # if a version is created the note will be attached to this too
            note_links = [publish_data]

            if version_data is not None:
                note_links.append(version_data)

            for variant in item.properties["alias_variants"]:
                data = {
                    "project": item.context.project,
                    "user": item.context.user,
                    "subject": "Alias Variant",
                    "content": variant[0],
                    "note_links": note_links,
                }
                if item.context.task:
                    data["tasks"] = [item.context.task]

                note = publisher.shotgun.create("Note", data)
                publisher.shotgun.upload_thumbnail(
                    entity_type="Note", entity_id=note.get("id"), path=variant[1]
                )
                variant_filepath = variant[1]
                _, file_ext = os.path.splitext(variant_filepath)

                publisher.shotgun.upload(
                    entity_type="Note",
                    entity_id=note.get("id"),
                    path=variant_filepath,
                    field_name="attachments",
                    display_name="{name}{ext}".format(name=variant[0], ext=file_ext),
                )

    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once all the publish
        tasks have completed, and can for example be used to version up files.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        # get the publish "mode" stored inside of the root item properties
        bg_processing = item.parent.properties.get("bg_processing", False)
        in_bg_process = item.parent.properties.get("in_bg_process", False)

        if not bg_processing or (bg_processing and in_bg_process):
            self.logger.info("Variants published successfully")

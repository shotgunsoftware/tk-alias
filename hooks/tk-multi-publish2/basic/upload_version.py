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
import shutil
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class UploadVersionPlugin(HookBaseClass):
    """
    Plugin for sending quicktimes and images to shotgun for review.
    """

    # Translation workers are responsible for performing the LMV translation.
    # 'local': a local translator will be used, determined based on file type and current engine
    # 'framework':  the tk-framework-lmv translator will be used (default)
    TRANSLATION_WORKER_LOCAL = "local"
    TRANSLATION_WORKER_FRAMEWORK = "framework"
    TRANSLATION_WORKERS = [TRANSLATION_WORKER_LOCAL, TRANSLATION_WORKER_FRAMEWORK]

    @property
    def icon(self):
        """
        Path to an png icon on disk
        """

        if hasattr(self, "plugin_icon"):
            return self.plugin_icon

        # look for icon one level up from this hook's folder in "icons" folder
        return os.path.join(self.disk_location, os.pardir, "icons", "review.png")

    @property
    def settings(self):
        """
        Dictionary defining the settings that this plugin expects to recieve
        through the settings parameter in the accept, validate, publish and
        finalize methods.

        A dictionary on the following form::

            {
                "Settings Name": {
                    "type": "settings_type",
                    "default": "default_value",
                    "description": "One line description of the setting"
            }

        The type string should be one of the data types that toolkit accepts as
        part of its environment configuration.
        """
        # inherit the settings from the base publish plugin
        base_settings = super(UploadVersionPlugin, self).settings or {}

        # settings specific to this class
        upload_version_settings = {
            "3D Version": {
                "type": "bool",
                "default": True,
                "description": "Generate a 3D Version instead of a 2D one?",
            },
            "Upload": {
                "type": "bool",
                "default": False,
                "description": "Upload content to Shotgun?",
            },
            "Translation Worker": {
                "type": "str",
                "default": self.TRANSLATION_WORKER_FRAMEWORK,
                "description": "Specify the worker to use to perform LMV translation.",
            },
        }

        # update the base settings
        base_settings.update(upload_version_settings)

        return base_settings

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

        if settings.get("3D Version").value is True:
            self.plugin_icon = os.path.join(
                self.disk_location, os.pardir, "icons", "3d_model.png"
            )

        return {"accepted": True, "checked": True}

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

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        if not framework_lmv:
            self.logger.error("Could not run LMV translation: missing ATF framework")
            return False

        translation_worker = settings.get("Translation Worker").value
        if translation_worker not in self.TRANSLATION_WORKERS:
            self.logger.error(
                "Unknown Translation Worker '{worker}'. Translation worker must be one of {workers}".format(
                    worker=translation_worker,
                    workers=", ".join(self.TRANSLATION_WORKERS),
                )
            )
            return False

        return True

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        publisher = self.parent
        path = item.properties["path"]

        # be sure to strip the extension from the publish name
        path_components = publisher.util.get_file_path_components(path)
        filename = path_components["filename"]
        (publish_name, extension) = os.path.splitext(filename)
        item.properties["publish_name"] = publish_name

        # create the Version in Shotgun
        super(UploadVersionPlugin, self).publish(settings, item)

        # generate the Version content: LMV file or simple 2D thumbnail
        if settings.get("3D Version").value is True:
            use_framework_translator = (
                settings.get("Translation Worker").value
                == self.TRANSLATION_WORKER_FRAMEWORK
            )
            self.logger.debug("Creating LMV files from source file")
            # translate the file to lmv and upload the corresponding package to the Version
            (
                package_path,
                thumbnail_path,
                output_directory,
            ) = self._translate_file_to_lmv(item, use_framework_translator)
            self.logger.info("Uploading LMV files to Shotgun")
            self.parent.shotgun.update(
                entity_type="Version",
                entity_id=item.properties["sg_version_data"]["id"],
                data={"sg_translation_type": "LMV"},
            )
            self.parent.shotgun.upload(
                entity_type="Version",
                entity_id=item.properties["sg_version_data"]["id"],
                path=package_path,
                field_name="sg_uploaded_movie",
            )
            # if the Version thumbnail is empty, update it with the newly created thumbnail
            if not item.get_thumbnail_as_path() and thumbnail_path:
                self.parent.shotgun.upload_thumbnail(
                    entity_type="Version",
                    entity_id=item.properties["sg_version_data"]["id"],
                    path=thumbnail_path,
                )
            # delete the temporary folder on disk
            self.logger.debug("Deleting temporary folder")
            shutil.rmtree(output_directory)

        else:
            thumbnail_path = item.get_thumbnail_as_path()
            self.logger.debug("Using thumbnail image as Version media")
            if thumbnail_path:
                self.parent.shotgun.upload(
                    entity_type="Version",
                    entity_id=item.properties["sg_version_data"]["id"],
                    path=thumbnail_path,
                    field_name="sg_uploaded_movie",
                )
            else:
                use_framework_translator = (
                    settings.get("Translation Worker").value
                    == self.TRANSLATION_WORKER_FRAMEWORK
                )
                self.logger.debug("Converting file to LMV to extract thumbnails")
                output_directory, thumbnail_path = self._get_thumbnail_from_lmv(
                    item, use_framework_translator
                )
                if thumbnail_path:
                    self.logger.info("Uploading LMV thumbnail file to Shotgun")
                    self.parent.shotgun.upload(
                        entity_type="Version",
                        entity_id=item.properties["sg_version_data"]["id"],
                        path=thumbnail_path,
                        field_name="sg_uploaded_movie",
                    )
                    self.parent.shotgun.upload_thumbnail(
                        entity_type="Version",
                        entity_id=item.properties["sg_version_data"]["id"],
                        path=thumbnail_path,
                    )
                self.logger.debug("Deleting temporary folder")
                shutil.rmtree(output_directory)

    def _translate_file_to_lmv(self, item, use_framework_translator):
        """
        Translate the current Alias file as an LMV package in order to upload it to Shotgun as a 3D Version

        :param item: Item to process
        :param use_framework_translator: True will force the translator shipped with tk-framework-lmv to be used
        :returns:
            - The path to the LMV zip file
            - The path to the LMV thumbnail
            - The path to the temporary folder where the LMV files have been processed
        """

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        translator = framework_lmv.import_module("translator")

        # translate the file to lmv
        lmv_translator = translator.LMVTranslator(item.properties.path)
        self.logger.info("Converting file to LMV")
        lmv_translator.translate(use_framework_translator=use_framework_translator)

        # package it up
        self.logger.info("Packaging LMV files")
        package_path, thumbnail_path = lmv_translator.package(
            svf_file_name=str(item.properties["sg_version_data"]["id"]),
            thumbnail_path=item.get_thumbnail_as_path(),
        )

        return package_path, thumbnail_path, lmv_translator.output_directory

    def _get_thumbnail_from_lmv(self, item, use_framework_translator):
        """
        Extract the thumbnail from the source file, using the LMV conversion

        :param item: Item to process
        :param use_framework_translator: True will force the translator shipped with tk-framework-lmv to be used
        :returns:
            - The path to the temporary folder where the LMV files have been processed
            - The path to the LMV thumbnail
        """

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        translator = framework_lmv.import_module("translator")

        # translate the file to lmv
        lmv_translator = translator.LMVTranslator(item.properties.path)
        self.logger.info("Converting file to LMV")
        lmv_translator.translate(use_framework_translator=use_framework_translator)

        self.logger.info("Extracting thumbnails from LMV")
        thumbnail_path = lmv_translator.extract_thumbnail()
        if not thumbnail_path:
            self.logger.warning(
                "Couldn't retrieve thumbnail data from LMV. Version won't have any associated media"
            )
            return lmv_translator.output_directory

        return lmv_translator.output_directory, thumbnail_path

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

FORGE_OPTION1 = True
FORGE_OPTION2 = True


class UploadVersionPlugin(HookBaseClass):
    """
    Plugin for sending quicktimes and images to shotgun for review.
    """

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
            "Translation Worker": {
                "type": "str",
                "default": "local",
                "description": "Use local libraries or Forge Cloud Services for translations.",
            },
            "Upload": {
                "type": "bool",
                "default": False,
                "description": "Upload content to Shotgun?",
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

        if settings.get("Translation Worker").value not in ["local", "forge"]:
            self.logger.error("Unknown Translation Worker")

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

        framework_forge = self.load_framework("tk-framework-forge_v0.1.x")
        if not framework_forge:
            self.logger.error("Could not load Forge framework")
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

        # create the Version in Shotgun
        super(UploadVersionPlugin, self).publish(settings, item)

        translation_worker = settings.get("Translation Worker").value

        # generate the Version content: LMV file or simple 2D thumbnail
        if settings.get("3D Version").value is True:
            self.logger.debug("Creating LMV files from source file")
            # translate the file to lmv and upload the corresponding package to the Version
            (
                package_path,
                thumbnail_path,
                output_directory,
            ) = self._translate_file_to_lmv(item, translation_worker)

            self.logger.debug("Uploading LMV file to Shotgun")
            self.parent.shotgun.update(
                entity_type="Version",
                entity_id=item.properties["sg_version_data"]["id"],
                data={"sg_translation_type": "LMV"},
            )

            if package_path:
                self.parent.shotgun.upload(
                    entity_type="Version",
                    entity_id=item.properties["sg_version_data"]["id"],
                    path=package_path,
                    field_name="sg_uploaded_movie",
                )

            if thumbnail_path:
                # if the Version thumbnail is empty, update it with the newly created thumbnail
                if not item.get_thumbnail_as_path() and thumbnail_path:
                    self.parent.shotgun.upload_thumbnail(
                        entity_type="Version",
                        entity_id=item.properties["sg_version_data"]["id"],
                        path=thumbnail_path,
                    )

            if output_directory:
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
                self.logger.debug("Converting file to LMV to extract thumbnails")
                output_directory, thumbnail_path = self._get_thumbnail_from_lmv(
                    item, translation_worker
                )
                if thumbnail_path:
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

    def _translate_file_to_lmv(self, item, translation_worker="local"):
        """
        Translate the current Alias file as an LMV package in order to upload it to Shotgun as a 3D Version

        :param item: Item to process
        :returns:
            - The path to the LMV zip file
            - The path to the LMV thumbnail
            - The path to the temporary folder where the LMV files have been processed
        """

        package_path = None
        thumbnail_path = None
        output_directory = None

        if translation_worker == "local":
            framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
            translator = framework_lmv.import_module("translator")

            # translate the file to lmv
            lmv_translator = translator.LMVTranslator(item.properties.path)
            self.logger.info("Converting file to LMV")
            lmv_translator.translate()

            # package it up
            self.logger.info("Packaging LMV files")
            package_path, thumbnail_path = lmv_translator.package(
                svf_file_name=str(item.properties["sg_version_data"]["id"]),
                thumbnail_path=item.get_thumbnail_as_path(),
            )
            output_directory = lmv_translator.output_directory

        elif translation_worker == "forge":
            framework_forge = self.load_framework("tk-framework-forge_v0.1.x")
            # forge_api = framework_forge.import_module("forge_api")
            model_derivative_module = framework_forge.import_module("model_derivative")
            model_derivative = model_derivative_module.ModelDerivative()

            urn = model_derivative.translate_source(item.name, item.properties.path)

            if FORGE_OPTION1:
                # Forge Option #1:
                # Set custom field on Version for "URN" value for SG to load in Forge Viewer
                # Pro: fast operation to translate -- job is sent to Forge and we're free to go on
                # Con: requires SG code change to load using URN, in addition to local URL. As well,
                # a Forge App/credentials needs to be shared between Toolkit and SG
                self.parent.shotgun.update(
                    entity_type="Version",
                    entity_id=item.properties["sg_version_data"]["id"],
                    data={"sg_urn": urn},
                )

            if FORGE_OPTION2:
                # Forge Option #2:
                # More of a proof of concept, but we can download the translation files from
                # Forge, and then pass to SG API to upload to S3 for 3D Viewer to access in SG
                # Pro: No code changes to SG, only toolkit
                # Con: Redundancy in uploading to Forge, which uploads to S3 -- then we download the
                # translation files to upload again to SG this time, which also stores it on S3
                # NOTE: could we modify SG to point to Forge S3 location? Then we can get the best
                # of #1 and #2, but uploading to Forge and minimal code change to SG to get S3 files
                # ^I don't think so, since SG also requires that all the necessary files be stores in a folder
                # in a sepcific structure to parse
                # Also, this option requires waiting for the job to finish, since we need the derivatives in the
                # successful manifest
                manifest = model_derivative.get_manifest(urn)

                if model_derivative.is_manifest_successful(manifest):
                    # Download all derivates from Forge, including any file dependencies, and package it up (similar to lmv)
                    (
                        package_path,
                        thumbnail_path,
                        output_directory,
                    ) = model_derivative.download_derivatives(item, manifest)
                else:
                    # TODO: parse manifest["derivatives"] for error messages
                    self.logger.error("Forge Translation failed")

                # Done. Close the forge connection.
                # model_derivative.forge_client.close_connection()

        else:
            self.logger.error(
                "Failed to tranalate file: unknown Translation Worker Type"
            )

        return package_path, thumbnail_path, output_directory

    def _get_thumbnail_from_lmv(self, item, translation_worker="local"):
        """
        Extract the thumbnail from the source file, using the LMV conversion

        :param item: Item to process
        :returns:
            - The path to the temporary folder where the LMV files have been processed
            - The path to the LMV thumbnail
        """

        output_directory = None
        thumbnail_path = None

        if translation_worker == "local":
            framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
            translator = framework_lmv.import_module("translator")

            # translate the file to lmv
            lmv_translator = translator.LMVTranslator(item.properties.path)
            self.logger.info("Converting file to LMV")
            lmv_translator.translate()

            self.logger.info("Extracting thumbnails from LMV")
            thumbnail_path = lmv_translator.extract_thumbnail()
            if not thumbnail_path:
                self.logger.warning(
                    "Couldn't retrieve thumbnail data from LMV. Version won't have any associated media"
                )
                # return lmv_translator.output_directory

            output_directory = lmv_translator.output_directory

        elif translation_worker == "forge":
            framework_forge = self.load_framework("tk-framework-forge_v0.1.x")
            model_derivative_module = framework_forge.import_module("model_derivative")
            model_derivative = model_derivative_module.ModelDerivative()
            urn = model_derivative.translate_source(item.name, item.properties.path)

            if FORGE_OPTION1:
                # Forge Option #1:
                # Set custom field on Version for "URN" value for SG to load in Forge Viewer
                # Pro: fast operation to translate -- job is sent to Forge and we're free to go on
                # Con: requires SG code change to load using URN, in addition to local URL. As well,
                # a Forge App/credentials needs to be shared between Toolkit and SG
                self.parent.shotgun.update(
                    entity_type="Version",
                    entity_id=item.properties["sg_version_data"]["id"],
                    data={"sg_urn": urn},
                )

            elif FORGE_OPTION2:
                manifest = model_derivative.get_manifest(urn)

                if model_derivative.is_manifest_successful(manifest):
                    # Download all derivates from Forge, including any file dependencies, and package it up (similar to lmv)
                    (
                        output_directory,
                        thumbnail_path,
                    ) = model_derivative.download_thumbnails(item, manifest)
                else:
                    # TODO: parse manifest["derivatives"] for error messages
                    self.logger.error("Failed to extract thumbnails using Forge")

                # Done. Close the forge connection. TODO this should happen on publisher destroy/close
                # model_derivative.forge_client.close_connection()

        else:
            self.logger.error(
                "Failed to get thumbnail: unknown Translation Worker Type"
            )

        return output_directory, thumbnail_path

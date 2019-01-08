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
import traceback
from subprocess import check_call
from subprocess import CalledProcessError

import sgtk
from sgtk.util.filesystem import ensure_folder_exists

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishTranslatedFilePlugin(HookBaseClass):
    @property
    def codename(self):
        return self.parent.engine.alias_codename

    @property
    def engine_translator_info(self):
        return self.parent.engine.get_setting("translator_info").get(self.codename)

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(AliasPublishTranslatedFilePlugin, self).settings or {}

        # settings specific to this class
        publish_settings = {
            self.publish_template_yml: {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        base_settings.update(publish_settings)

        workfile_settings = {
            self.work_template_yml: {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        base_settings.update(workfile_settings)

        translator_settings = {
            self.translator_yml: {
                "type": "str",
                "default": None
            }
        }

        base_settings.update(translator_settings)

        file_types_settings = {
            "File Types": {
                "type": "list",
                "default": [
                    ["Alembic Cache", "abc"],
                    ["3dsmax Scene", "max"],
                    ["NukeStudio Project", "hrox"],
                    ["Houdini Scene", "hip", "hipnc"],
                    ["Maya Scene", "ma", "mb"],
                    ["Motion Builder FBX", "fbx"],
                    ["Nuke Script", "nk"],
                    ["Photoshop Image", "psd", "psb"],
                    ["Rendered Image", "dpx", "exr"],
                    ["Texture", "tiff", "tx", "tga", "dds"],
                    ["Image", "jpeg", "jpg", "png"],
                    ["Movie", "mov", "mp4"],
                ],
                "description": (
                    "List of file types to include. Each entry in the list "
                    "is a list in which the first entry is the Shotgun "
                    "published file type and subsequent entries are file "
                    "extensions that should be associated."
                )
            },
        }

        base_settings.update(file_types_settings)

        return base_settings

    def validate(self, settings, item):
        publisher = self.parent

        publish_template_setting = settings.get(self.publish_template_yml)
        publish_template = publisher.engine.get_template_by_name(publish_template_setting.value)

        if not publish_template:
            return False

        if publish_template:
            item.properties[self.publish_template_key] = publish_template

        workfile_template_setting = settings.get(self.work_template_yml)
        workfile_template = publisher.engine.get_template_by_name(workfile_template_setting.value)

        if not workfile_template:
            return False

        item.properties[self.work_template_key] = workfile_template
        item.properties[self.translator_key] = settings.get(self.translator_yml)

        return True

    def accept(self, settings, item):
        base_accept = super(AliasPublishTranslatedFilePlugin, self).accept(settings, item)
        base_accept.update({"checked": False})

        return base_accept

    def _translate_file(self, source_path, target_path, item):
        file_extension = item.properties.get(self.translator_key).value
        engine_translator_info = self.engine_translator_info
        translator_info = engine_translator_info.get("alias_translators").get(file_extension)
        executable = translator_info.get("alias_translator_exe")
        licensed = translator_info.get("alias_translator_is_licensed")
        alias_translator_dir = engine_translator_info.get("alias_translator_dir")
        alias_translator_license_path = engine_translator_info.get("alias_translator_license_path")
        alias_translator_license_prod_key = engine_translator_info.get("alias_translator_license_prod_key")
        alias_translator_license_prod_version = engine_translator_info.get("alias_translator_license_prod_version")
        alias_translator_license_type = engine_translator_info.get("alias_translator_license_type")

        translation_command = [os.path.join(alias_translator_dir, executable)]

        if licensed:
            translation_command += ["-productKey",
                                    alias_translator_license_prod_key,
                                    "-productVersion",
                                    alias_translator_license_prod_version,
                                    "-productLicenseType",
                                    alias_translator_license_type,
                                    "-productLicensePath",
                                    alias_translator_license_path]

        translation_command += ["-i",
                                source_path,
                                "-o",
                                target_path]

        try:
            check_call(translation_command)
        except CalledProcessError as e:
            self.logger.error("Error ocurred {!r}".format(e))
            raise Exception("Error ocurred {!r}".format(e))

    def _get_target_path(self, item):
        source_path = item.properties["path"]
        work_template = item.properties.get("work_template")
        publish_template = item.properties.get("publish_template")

        if not work_template.validate(source_path):
            self.logger.warning(
                "Work file '%s' did not match work template '%s'. "
                "Publishing in place." % (source_path, work_template)
            )
            return

        fields = work_template.get_fields(source_path)

        return publish_template.apply_fields(fields)

    def _copy_work_to_publish(self, settings, item):
        # Validate templates
        work_template = item.properties.get("work_template")
        if not work_template:
            self.logger.debug(
                "No work template set on the item. "
                "Skipping copy file to publish location."
            )
            return

        publish_template = item.properties.get("publish_template")
        if not publish_template:
            self.logger.debug(
                "No publish template set on the item. "
                "Skipping copying file to publish location."
            )
            return

        # Source path
        source_path = item.properties["path"]
        target_path = self._get_target_path(item)

        try:
            publish_folder = os.path.dirname(target_path)
            ensure_folder_exists(publish_folder)
            self._translate_file(source_path, target_path, item)
        except Exception as e:
            raise Exception(
                "Failed to copy work file from '%s' to '%s'.\n%s" %
                (source_path, target_path, traceback.format_exc())
            )

        self.logger.debug("Copied work file '%s' to publish file '%s'." % (source_path, target_path))

    def get_publish_type(self, settings, item):
        publisher = self.parent
        path = self._get_target_path(item)

        # get the publish path components
        path_info = publisher.util.get_file_path_components(path)

        # determine the publish type
        extension = path_info["extension"]

        extension = extension.lstrip(".")

        for type_def in settings["File Types"].value:
            publish_type = type_def[0]
            file_extensions = type_def[1:]

            if extension in file_extensions:
                # found a matching type in settings. use it!
                return publish_type

    def get_publish_name(self, settings, item):
        target_path = self._get_target_path(item)
        publisher = self.parent
        return publisher.util.get_publish_name(
            target_path,
            sequence=False
        )

    def publish(self, settings, item):
        publish_id = item.properties['sg_publish_data']['id']
        
        item.properties["publish_template"] = item.properties[self.publish_template_key]
        item.properties["work_template"] = item.properties[self.work_template_key]

        publish_type = self.get_publish_type(settings, item)
        item.local_properties.publish_type = publish_type

        super(AliasPublishTranslatedFilePlugin, self).publish(settings, item)
        
        entities = [
            {
                'type': 'PublishedFile',
                'id': item.properties['sg_publish_data']['id']
            }
        ]
        source_entity = {
            'type': 'PublishedFile',
            'id': publish_id
        }
        self.parent.engine.shotgun.share_thumbnail(entities=entities, source_entity=source_entity)

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["*"]

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
import errno
import shutil
import base64
import tempfile
import traceback
from subprocess import Popen, PIPE, STDOUT

import sgtk
from sgtk.util.filesystem import ensure_folder_exists

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishLMVProcessedFilePlugin(HookBaseClass):
    TMPDIR = None

    @property
    def codename(self):
        return self.parent.engine.alias_codename

    @property
    def engine_translator_info(self):
        return self.parent.engine.get_setting("translator_info").get(self.codename)

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(AliasPublishLMVProcessedFilePlugin, self).settings or {}

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
        try:
            engine_translator_info = self.engine_translator_info
            translator_info = engine_translator_info.get("alias_translators")
            lmv_translator = translator_info.get('lmv')
            lmv_translator_executable = lmv_translator.get('alias_translator_exe')
            alias_translator_dir = engine_translator_info.get("alias_translator_dir")
            lmv_executable_fullpath = os.path.join(alias_translator_dir, 'LMVExtractor', lmv_translator_executable)
            if os.path.isfile(lmv_executable_fullpath):
                self.logger.info("LMV validation finished.")
                return True
            else:
                self.logger.info("LMV validation filed, extractor not found.")
                return False
        except Exception as w:
            self.logger.info('Error: {}'.format(w))
            return False
        return False

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
        base_accept = super(AliasPublishLMVProcessedFilePlugin, self).accept(settings, item)
        base_accept.update({
            "accepted": True,
            "visible": True,
            "checked": True,
            "enabled": False
        })
        return base_accept

    def makedirs(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _get_translator(self):
        engine_translator_info = self.engine_translator_info
        alias_translators = engine_translator_info.get("alias_translators")
        lmv_translator = alias_translators.get("lmv")
        lmv_translator_exe = lmv_translator.get("alias_translator_exe")
        alias_translator_dir = engine_translator_info.get("alias_translator_dir")

        return os.path.join(alias_translator_dir, "LMVExtractor", lmv_translator_exe)

    def _translate_file(self, source_path, target_path, item):
        self.logger.info("Starting the translation")

        # PublishedFile id
        publish_id = item.properties.sg_publish_data["id"]

        # Get translator
        translator = self._get_translator()

        # Temporal dir
        self.TMPDIR = tempfile.mkdtemp(prefix='sgtk_')

        # Alias file name
        file_name = os.path.basename(source_path)

        # JSON file
        self.logger.info("Creating JSON file")
        index_path = os.path.join(self.TMPDIR, 'index.json')
        with open(index_path, 'w') as _:
            pass

        # Copy source file locally
        self.logger.info("Copy file {} locally.".format(source_path))
        source_path_temporal = os.path.join(self.TMPDIR, file_name)
        shutil.copyfile(source_path, source_path_temporal)

        # Execute translation command
        command = [translator, index_path, source_path_temporal]
        self.logger.info("LMV execution: {}".format(" ".join(command)))
        lmv_subprocess = Popen('"'+'" "'.join(command)+'"', stdout=PIPE, stderr=STDOUT, shell=True)
        while lmv_subprocess.poll() is None:
            self.logger.debug("LMV processing ... [{}]".format(lmv_subprocess.stdout.next().replace('\n', '')))

        if lmv_subprocess.returncode == 0:
            target_path_parent = os.path.dirname(target_path)

            if os.path.exists(target_path):
                shutil.rmtree(target_path)

            if not os.path.exists(target_path_parent):
                self.makedirs(target_path_parent)

            output_directory = os.path.join(self.TMPDIR, "output")

            # Rename svf file
            name, _ = os.path.splitext(file_name)
            svf_file_old_name = "{}.svf".format(name)
            svf_file_new_name = "{}.svf".format(publish_id)
            source_file = os.path.join(output_directory, "1", svf_file_old_name)
            target_file = os.path.join(output_directory, "1", svf_file_new_name)
            os.rename(source_file, target_file)

            shutil.copytree(output_directory, target_path)

            base_name = os.path.join(self.TMPDIR, "{}".format(publish_id))

            self.logger.info("LMV files copied.")
        else:
            self.logger.error("LMV processing fail.")
            return

        thumbnail_data = self._get_thumbnail_data(item, source_path_temporal)
        if thumbnail_data:
            images_path_temporal = os.path.join(output_directory, "images")
            images_path = os.path.join(os.path.dirname(target_path_parent), "images")

            if not os.path.exists(images_path):
                self.makedirs(images_path)

            if not os.path.exists(images_path_temporal):
                self.makedirs(images_path_temporal)

            thumb_big_filename = "{}.jpg".format(publish_id)
            thumb_small_filename = "{}_thumb.jpg".format(publish_id)
            thumb_big_path = os.path.join(images_path_temporal, thumb_big_filename)
            thumb_small_path = os.path.join(images_path_temporal, thumb_small_filename)

            with open(thumb_big_path, 'wb') as thumbnail:
                thumbnail.write(thumbnail_data)
                self.logger.info("LMV image created.")

            with open(thumb_small_path, 'wb') as thumbnail:
                thumbnail.write(thumbnail_data)
                self.logger.info("LMV thumbnail created.")

            self.logger.info("Updating thumbnail.")
            self.parent.engine.shotgun.upload_thumbnail("PublishedFile", publish_id, thumb_small_path)

            self.logger.info("ZIP package")
            zip_path = shutil.make_archive(base_name=base_name,
                                           format="zip",
                                           root_dir=output_directory)

            self.logger.info("Moving images")
            shutil.copy(thumb_small_path, images_path)
            shutil.copy(thumb_big_path, images_path)

            item.properties["thumb_small_path"] = thumb_small_path
        else:
            self.logger.info("ZIP package without images")
            zip_path = shutil.make_archive(base_name=base_name,
                                           format="zip",
                                           root_dir=output_directory)

        self.logger.info("Uploading lmv files")
        self.parent.engine.shotgun.upload(entity_type="PublishedFile",
                                          entity_id=publish_id,
                                          path=zip_path,
                                          field_name="sg_translation_files")

        self.parent.engine.shotgun.update(entity_type="PublishedFile",
                                          entity_id=publish_id,
                                          data=dict(sg_translation_type="LMV"))

        self.logger.info("Updating translation status.")
        self.parent.engine.shotgun.update("PublishedFile", publish_id, dict(sg_translation_status="Completed"))

        self.logger.info("LMV processing finished successfully.")
        self.logger.info('Translate VRED file to LMV file locally (DONE).')

    def _get_thumbnail_data(self, item, source_temporal_path):
        path = item.get_thumbnail_as_path()
        data = None

        if not path:
            with open(source_temporal_path) as src_file:
                line = src_file.readline()

                while line != "thumbnail JPEG\n":
                    line = src_file.readline()

                line = src_file.readline()

                data = []
                while line != "thumbnail end\n":
                    data.append(line.replace('Th ', ''))
                    line = src_file.readline()

                return base64.b64decode(''.join(data))

        if path:
            with open(path, "rb") as fh:
                data = fh.read()

        return data

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

    def _get_lmv_target_path(self, item):
        root_path = item.properties.publish_template.root_path
        publish_id = str(item.properties.sg_publish_data['id'])
        target_path = os.path.join(root_path, 'translations', 'lmv', publish_id)
        images_path = os.path.join(root_path, 'translations', 'images')
        self.makedirs(images_path)

        return target_path

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
        target_path = self._get_lmv_target_path(item)

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

    def publish(self, settings, item):
        item.properties["publish_template"] = item.properties[self.publish_template_key]
        item.properties["work_template"] = item.properties[self.work_template_key]

        publish_type = self.get_publish_type(settings, item)
        item.local_properties.publish_type = publish_type
        self._copy_work_to_publish(settings, item)
        
        # Create version
        path = item.properties['path']
        file_name = os.path.basename(path)
        name, extension = os.path.splitext(file_name)
        item.properties['publish_name'] = name
        super(AliasPublishLMVProcessedFilePlugin, self).publish(settings, item)

        thumbnail_path = item.get_thumbnail_as_path()
        if not thumbnail_path and "thumb_small_path" in item.properties:
            self.parent.engine.shotgun.upload_thumbnail(entity_type="Version",
                                                        entity_id=item.properties["sg_version_data"]["id"],
                                                        path=item.properties["thumb_small_path"])

        try:
            shutil.rmtree(self.TMPDIR)
        except Exception as e:
            pass


    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["*"]

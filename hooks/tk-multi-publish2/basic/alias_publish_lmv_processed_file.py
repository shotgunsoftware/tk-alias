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
from subprocess import check_call
from subprocess import CalledProcessError
from subprocess import Popen, PIPE, STDOUT

import sgtk
from sgtk.util.filesystem import ensure_folder_exists

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishLMVProcessedFilePlugin(HookBaseClass):
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

    def get_thumbnail_data(self, tmp_target):
        with open(tmp_target) as src_file:
            line = src_file.readline()
            while line != 'thumbnail JPEG\n':
                line = src_file.readline()
            line = src_file.readline()
            data = []
            while line != 'thumbnail end\n':
                data.append(line.replace('Th ', ''))
                line = src_file.readline()
            return base64.b64decode(''.join(data))

    def _translate_file(self, source_path, target_path, item):
        self.logger.info('Translate Alias file to LMV file locally')
        self.logger.info('Starting Alias file translation to LMV file')
        engine_translator_info = self.engine_translator_info
        translator_info = engine_translator_info.get("alias_translators")
        lmv_translator = translator_info.get('lmv')
        lmv_translator_executable = lmv_translator.get('alias_translator_exe')
        alias_translator_dir = engine_translator_info.get("alias_translator_dir")
        lmv_executable_fullpath = os.path.join(alias_translator_dir, 'LMVExtractor', lmv_translator_executable)
        tmpdir = tempfile.mkdtemp(prefix='sgtk_')
        index_path = os.path.join(tmpdir, 'index.json')
        tmp_target = os.path.join(tmpdir, os.path.basename(source_path) )
        with open(index_path, 'w') as _:
            pass
        self.logger.info("Copy file {} locally.".format(source_path))
        command = [lmv_executable_fullpath, index_path, source_path]
        self.logger.info("LMV execution: {}".format( ' '.join(command) ))
        shutil.copyfile(source_path, tmp_target)

        root_path = item.properties.publish_template.root_path
        publish_id = str(item.properties.sg_publish_data['id'])
        tmp_source_path = os.path.join(tmpdir, 'output')
        target_path = os.path.join(root_path, 'translations', 'lmv', publish_id)
        self.makedirs(os.path.dirname(target_path))
        th_target_path = os.path.join(root_path, 'translations', 'images', publish_id)
        self.makedirs(os.path.dirname(th_target_path))
        entryfile = '.'.join(os.path.basename(source_path).split('.')[0:-1])
        entrypath = os.path.join(tmp_source_path, '1', '{entryfile}.{ext}')

        custom_thumbnail_path = item.get_thumbnail_as_path()
        if custom_thumbnail_path:
            thumbnail_data = ''
            with open(custom_thumbnail_path, 'rb') as custom_thumbnail:
                thumbnail_data = custom_thumbnail.read()
        else:
            thumbnail_data = self.get_thumbnail_data(tmp_target)

        lmv_subprocess = Popen('"'+'" "'.join(command)+'"', stdout = PIPE, stderr = STDOUT, shell = True)
        while lmv_subprocess.poll() == None:
            self.logger.debug("LMV processing ... [{}]".format(lmv_subprocess.stdout.next().replace('\n', '')))
        if lmv_subprocess.returncode == 0:
            self.logger.info("Copying LMV files.")
            shutil.move(entrypath.format(ext='svf', entryfile=entryfile), 
                        entrypath.format(ext='svf', entryfile=publish_id))
            shutil.copytree(tmp_source_path, target_path)
            self.logger.info("LMV files copied.")
            with open(th_target_path+'.jpg', 'wb') as thumbnail:
                thumbnail.write(thumbnail_data)
                self.logger.info("LMV image created.")
            with open(th_target_path+'_thumb.jpg','wb') as thumbnail:
                thumbnail.write( thumbnail_data )
                self.logger.info("LMV thumbnail created.")
            self.logger.info("Cleaning...")
            shutil.rmtree(tmpdir)
            self.logger.info("Updating thumbnail.")
            self.parent.engine.shotgun.upload_thumbnail('PublishedFile', int(publish_id), th_target_path+'_thumb.jpg')
            self.logger.info("Updating translation status.")
            self.parent.engine.shotgun.update('PublishedFile', int(publish_id), {
                'sg_translation_status': 'Completed'
            })
            self.logger.info("LMV processing finished successfully.")
            self.logger.info('Translate Alias file to LMV file locally (DONE).')
        else:
            self.logger.info("LMV processing fail.")

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

    def publish(self, settings, item):
        item.properties["publish_template"] = item.properties[self.publish_template_key]
        item.properties["work_template"] = item.properties[self.work_template_key]

        publish_type = self.get_publish_type(settings, item)
        item.local_properties.publish_type = publish_type
        self._copy_work_to_publish(settings, item)
        # super(AliasPublishLMVProcessedFilePlugin, self).publish(settings, item)

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["*"]

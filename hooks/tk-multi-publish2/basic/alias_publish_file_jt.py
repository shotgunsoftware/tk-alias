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
from subprocess import check_call
from subprocess import CalledProcessError

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class AliasPublishJTFilePlugin(HookBaseClass):
    @property
    def publish_template_yml(self):
        return "JT Publish Template"

    @property
    def publish_template_key(self):
        return "jt_publish_template"

    @property
    def work_template_yml(self):
        return "JT Work Template"

    @property
    def work_template_key(self):
        return "jt_work_template"

    @property
    def translator_yml(self):
        return "JT Translator"

    @property
    def translator_key(self):
        return "jt_translator"

    @property
    def description(self):
        format_name = "JT"

        return """
        <p>
            This plugin exports the alias file to the <b>{format_name}</b> format. 
        </p> 

        <p>
            Any saved data will be exported to the path defined by this plugin's configured <b>Publish Template</b> 
            setting. 
        </p> 

        <p>
            Publishing this format will allow <b>{format_name}</b> files to be loaded and managed in an Alias scene by 
            Shotgun.
        </p> 
        """.format(format_name=format_name)

    def _get_translator_exe(self, path):
        if os.path.exists(path):
            return path

        file_name = os.path.basename(path)
        dir_path = os.path.dirname(path)

        path = os.path.join(dir_path, "translators", file_name)

        if not os.path.exists(path):
            raise Exception("Translator not found")

        return path

    def _translate_file(self, source_path, target_path, item):
        file_extension = item.properties.get(self.translator_key).value
        engine_translator_info = self.engine_translator_info
        translator_info = engine_translator_info.get("alias_translators").get(file_extension)
        executable = translator_info.get("alias_translator_exe")
        licensed = translator_info.get("alias_translator_is_licensed")
        alias_translator_dir, new_year = self._fix_year_in_path(engine_translator_info.get("alias_translator_dir"))
        alias_translator_license_path, new_year = self._fix_year_in_path(engine_translator_info.get(
            "alias_translator_license_path"), is_license=True)
        alias_translator_license_prod_key = engine_translator_info.get("alias_translator_license_prod_key")
        alias_translator_license_prod_version = engine_translator_info.get("alias_translator_license_prod_version")
        alias_translator_license_type = engine_translator_info.get("alias_translator_license_type")

        translation_command = [self._get_translator_exe(os.path.join(alias_translator_dir, executable))]

        if new_year > 2019:
            source = "K"
            target = chr(ord(source) + (new_year - 2019))
            alias_translator_license_prod_key = alias_translator_license_prod_key.replace(source, target)
            alias_translator_license_prod_version = alias_translator_license_prod_version.replace("2019", str(new_year))

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

        translation_command += ["-e1s",
                                "-g",
                                "-xk",
                                "-l",
                                "-s",
                                "1.0000",
                                "-u",
                                "128",
                                "-m0",
                                "-ta",
                                "-t",
                                "0.100000",
                                "-t1t",
                                "0.250000",
                                "-t2t",
                                "1.000000",
                                "-tl",
                                "1"]

        try:
            check_call(translation_command)
        except CalledProcessError as e:
            self.logger.error("Error ocurred {!r}".format(e))
            raise Exception("Error ocurred {!r}".format(e))

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
        return """
        Publishes the file to Shotgun in JT format.
        """

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

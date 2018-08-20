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


class AliasPublishLMVFilePlugin(HookBaseClass):
    @property
    def publish_template_yml(self):
        return "LMV Publish Template"

    @property
    def publish_template_key(self):
        return "publish_template"

    @property
    def work_template_yml(self):
        return "LMV Work Template"

    @property
    def work_template_key(self):
        return "work_template"

    @property
    def translator_yml(self):
        return "LMV Translator"

    @property
    def translator_key(self):
        return "lmv_translator"

    @property
    def description(self):
        return "Publishes the file to Shotgun in a valid LMV format."

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


class AliasPublishSTEPFilePlugin(HookBaseClass):
    @property
    def publish_template_yml(self):
        return "STEP Publish Template"

    @property
    def publish_template_key(self):
        return "step_publish_template"

    @property
    def work_template_yml(self):
        return "STEP Work Template"

    @property
    def work_template_key(self):
        return "iges_work_template"

    @property
    def translator_yml(self):
        return "STEP Translator"

    @property
    def translator_key(self):
        return "step_translator"

    @property
    def description(self):
        return """
        Publishes the file to Shotgun in STEP format.
        """

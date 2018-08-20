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


class AliasPublishIGESFilePlugin(HookBaseClass):
    @property
    def publish_template_yml(self):
        return "IGES Publish Template"

    @property
    def publish_template_key(self):
        return "iges_publish_template"

    @property
    def work_template_yml(self):
        return "IGES Work Template"

    @property
    def work_template_key(self):
        return "iges_work_template"

    @property
    def translator_yml(self):
        return "IGES Translator"

    @property
    def translator_key(self):
        return "iges_translator"

    @property
    def description(self):
        return """
        Publishes the file to Shotgun in IGES format.
        """

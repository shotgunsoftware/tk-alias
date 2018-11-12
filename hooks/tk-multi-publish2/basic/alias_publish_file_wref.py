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


class AliasPublishWREFFilePlugin(HookBaseClass):
    @property
    def publish_template_yml(self):
        return "WREF Publish Template"

    @property
    def publish_template_key(self):
        return "wref_publish_template"

    @property
    def work_template_yml(self):
        return "WREF Work Template"

    @property
    def work_template_key(self):
        return "iges_work_template"

    @property
    def translator_yml(self):
        return "WREF Translator"

    @property
    def translator_key(self):
        return "wref_translator"

    @property
    def description(self):
        format_name = "WREF"
        
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

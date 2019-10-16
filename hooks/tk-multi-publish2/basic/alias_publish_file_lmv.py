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
        """
        Verbose, multi-line description of what the plugin does. This can
        contain simple html for formatting.
        """
    
        publisher = self.parent
    
        shotgun_url = publisher.sgtk.shotgun_url
    
        media_page_url = "%s/page/media_center" % (shotgun_url,)
        review_url = "https://www.shotgunsoftware.com/features/#review"
    
        return """
            Publishes the file to Shotgun in a valid LMV format.<br>
            Upload the file to Shotgun for review.<br><br>

            A <b>Version</b> entry will be created in Shotgun and a transcoded
            copy of the file will be attached to it. The file can then be reviewed
            via the project's <a href='%s'>Media</a> page, <a href='%s'>RV</a>, or
            the <a href='%s'>Shotgun Review</a> mobile app.
            """ % (media_page_url, review_url, review_url)

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["alias.session"]

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


class AliasPublishVariantsPlugin(HookBaseClass):
    """
    Plugin for publishing variants of the current alias open session
    """
    @property
    def name(self):
        """
        One line display name describing the plugin
        """
        return "Publish Variants to Shotgun"

# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
The default file_usage hook.
"""

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class DefaultFileUsageHook(HookBaseClass):
    def file_attempt_open(self, path):
        """Called when a file is opened."""
        return True

    def file_closed(self, path):
        """Called when a file is closed, either because the user opened another file or closed the application."""
        pass

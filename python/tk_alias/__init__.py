# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from sgtk.util import is_windows

if is_windows():
    from .dialog_parent import DialogParent

from .menu_generation import AliasMenuGenerator
from .alias_event_watcher import AliasEventWatcher
from .data_validator import AliasDataValidator

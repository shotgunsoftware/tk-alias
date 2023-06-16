# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.


class AliasPyBase:
    def __init__(self, alias_py):
        """Initialize the AliasPy base helper class."""

        self.__alias_py = alias_py

    @property
    def alias_py(self):
        """Get the AliasPy module to access the Alias api."""
        return self.__alias_py

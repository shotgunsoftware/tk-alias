# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import pytest
from mock import MagicMock

import sys
from collections import namedtuple


def mock_alias_api_module():
    """
    Provide a mock module for the Alias Python API for when the pytest do not have access to
    the Alias Python API (requires Alias installation). For example, Azure Pipelines will not
    have access to an Alias installation, and so the Alias Python API cannot be imported.

    Mock any additional Alias Python API functionality here for all pytests to use.
    """

    module = type(sys)("alias_api")
    module.__mode__ = "mock"

    # Mock the object types enum
    AlObjectType = namedtuple(
        "AlObjectType",
        [
            "CameraEyeType",
            "CameraViewType",
            "CameraUpType",
            "CurveNodeType",
            "FaceNodeType",
            "GroupNodeType",
            "LightNodeType",
            "LightLookAtNodeType",
            "LightUpNodeType",
            "SurfaceNodeType",
            "TextureNodeType",
        ],
    )
    module.AlObjectType = AlObjectType

    # Mock the menu class
    module.Menu = MockAliasMenu

    return module


class MockAliasMenu:
    """Mock the Alias Python API Menu object."""

    def __init__(self, menu_name):
        self.menu_name = menu_name

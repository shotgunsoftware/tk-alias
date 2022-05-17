# Copyright (c) 2020 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import pytest
from mock import MagicMock

import sys


class TestAliasMenuGenerator:
    """
    A test class for the AliasMenuGeneration class functionality.

    TODO add more test cases for checking the menu items.
    """

    # An ugly workaround untili python 2 unit tests are removed from Azure Pipeline CI
    if sys.version_info.major < 3:
        __test__ = False
    else:
        __test__ = True

    @pytest.fixture(scope="module")
    def menu_generator_class(request):
        """
        Fixture to return the AliasMenuGenerator class.

        Defer the import until this fixture to avoid import errors when this test class should
        be ignored.
        """

        from tk_alias import AliasMenuGenerator

        return AliasMenuGenerator

    @pytest.fixture(scope="module")
    def mock_engine(request):
        """
        Fixture to mock the Alias Engine. Sets the version to 2022.2 but this can be overriden
        after the caller receives the object.
        """

        engine = MagicMock()
        engine.alias_version = "2022.2"
        return engine

    @pytest.mark.skip_open_model
    def test_init_alias_menu_name(self, menu_generator_class, mock_engine):
        """
        Test the init method sets the correct Alias menu name.
        """

        shotgun_versions = [
            "2019",
            "2020",
            "2020.3",
            "2021",
            "2021.0",
            "2021.3.1",
            "2022",
            "2022.0",
            "2022.1",
            "2022.1.2",
        ]
        for version in shotgun_versions:
            mock_engine.alias_version = version
            menu_generator = menu_generator_class(mock_engine)
            assert menu_generator.MENU_NAME == "al_shotgun"
            assert menu_generator._alias_menu
            if hasattr(menu_generator._alias_menu, "menu_name"):
                assert menu_generator._alias_menu.menu_name == "al_shotgun"

        shotgrid_version = [
            "2022.2",
            "2022.2.0",
            "2022.2.1",
            "2023",
            "2023.0",
            "2023.1",
        ]
        for version in shotgrid_version:
            mock_engine.alias_version = version
            menu_generator = menu_generator_class(mock_engine)
            assert menu_generator.MENU_NAME == "al_shotgrid"
            assert menu_generator._alias_menu
            if hasattr(menu_generator._alias_menu, "menu_name"):
                assert menu_generator._alias_menu.menu_name == "al_shotgrid"

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


class TestAliasObjectMenuAdapter:
    """Tests for the 2027.1+ gui menu adapter."""

    def test_clean_removes_tracked_items_and_submenus(self):
        from tk_alias.menu_generation import _AliasObjectMenuAdapter

        alias_py = MagicMock()
        root_menu = MagicMock()
        sub_menu = MagicMock()
        item = MagicMock()
        alias_py.gui = MagicMock()
        alias_py.gui.Menu.side_effect = lambda text: (
            sub_menu if text == "Sub" else root_menu
        )
        alias_py.gui.MenuItem.return_value = item

        adapter = _AliasObjectMenuAdapter(alias_py, root_menu)
        sub = adapter.add_menu("Sub")
        adapter.add_command("Action", lambda: None)
        sub.add_command("Nested", lambda: None)

        adapter.clean()

        root_menu.add_menu.assert_called_with(sub_menu)
        root_menu.remove_menu.assert_called_with(sub_menu)
        root_menu.remove_item.assert_called_with(item)
        sub_menu.add_item.assert_called_with(item)

    def test_remove_on_main_menu_root_only_cleans(self):
        from tk_alias.menu_generation import _AliasObjectMenuAdapter

        alias_py = MagicMock()
        root_menu = MagicMock()
        item = MagicMock()
        alias_py.gui = MagicMock()
        alias_py.gui.MenuItem.return_value = item

        adapter = _AliasObjectMenuAdapter(
            alias_py, root_menu, is_main_menu_root=True
        )
        adapter.add_command("Action", lambda: None)

        adapter.remove()

        root_menu.remove.assert_not_called()
        root_menu.remove_item.assert_called_with(item)

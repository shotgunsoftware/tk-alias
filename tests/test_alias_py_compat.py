# Copyright (c) 2026 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import os
import sys
import types

import pytest
from mock import MagicMock


class TestAliasPyApiCompatibility:
    """Tests for AliasPy compatibility shims across Alias API versions."""

    @pytest.fixture(scope="class")
    def alias_py_class(self):
        from tk_alias.alias_py.alias_py import AliasPy

        return AliasPy

    @staticmethod
    def _status_code_module():
        status_code = types.SimpleNamespace(Success=types.SimpleNamespace(value=0))
        status_code.Failure = types.SimpleNamespace(value=1)
        return status_code

    @staticmethod
    def _new_api_module():
        """Simulate Alias 2027.1+ module layout (renamed / removed legacy helpers)."""

        module = types.ModuleType("alias_api")

        module.save = MagicMock(return_value=0)
        module.save_as = MagicMock(return_value=0)
        module.open = MagicMock(return_value=0)
        module.is_empty = MagicMock(return_value=False)

        stage = types.SimpleNamespace(path="/path/to/scene.wire", name="Stage")
        module.stage = MagicMock(return_value=stage)

        module.stages = types.SimpleNamespace(
            all=MagicMock(return_value=[stage]),
            create=MagicMock(return_value=0),
        )

        product = types.SimpleNamespace(key="966S1", full_version="2027.0.0.F")
        module.AlProduct = product

        module.get_pick_items = MagicMock(return_value=["pick-item"])
        module.get_current_pick_item = MagicMock(return_value=None)
        module.AlStatusCode = TestAliasPyApiCompatibility._status_code_module()

        return module

    @staticmethod
    def _legacy_api_module():
        """Simulate pre-2027.1 module layout with legacy helper names."""

        module = types.ModuleType("alias_api")

        module.save_file = MagicMock(return_value=0)
        module.save_file_as = MagicMock(return_value=0)
        module.open_file = MagicMock(return_value=0)
        module.is_empty_file = MagicMock(return_value=False)

        stage = types.SimpleNamespace(path="/legacy/path.wire", name="LegacyStage")
        module.get_current_stage = MagicMock(return_value=stage)
        module.get_current_path = MagicMock(return_value=stage.path)
        module.get_stages = MagicMock(return_value=[stage])
        module.create_stage = MagicMock(return_value=0)
        module.get_product_information = MagicMock(
            return_value={
                "product_key": "legacy-key",
                "product_version": "2026.0.0.F",
                "product_license_type": "legacy-type",
                "product_license_path": "legacy-path",
            }
        )
        module.first_pick_item = MagicMock(return_value=0)
        module.get_current_pick_item = MagicMock(return_value="legacy-pick")
        module.AlStatusCode = TestAliasPyApiCompatibility._status_code_module()

        return module

    def test_legacy_api_names_are_used_when_present(self, alias_py_class):
        api_module = self._legacy_api_module()
        alias_py = alias_py_class(api_module)

        assert alias_py.save_file is api_module.save_file
        assert alias_py.open_file is api_module.open_file
        assert alias_py.get_current_path is api_module.get_current_path
        assert alias_py.get_current_stage is api_module.get_current_stage
        assert alias_py.first_pick_item is api_module.first_pick_item
        assert alias_py.get_current_pick_item() == "legacy-pick"

    def test_renamed_api_functions_delegate_to_new_names(self, alias_py_class):
        api_module = self._new_api_module()
        alias_py = alias_py_class(api_module)

        assert alias_py.save_file is api_module.save
        assert alias_py.save_file_as is api_module.save_as
        assert alias_py.open_file is api_module.open
        assert alias_py.is_empty_file is api_module.is_empty

        alias_py.save_file()
        api_module.save.assert_called_once_with()

    def test_stage_helpers_use_stage_module(self, alias_py_class):
        api_module = self._new_api_module()
        alias_py = alias_py_class(api_module)

        assert alias_py.get_current_path() == "/path/to/scene.wire"
        assert alias_py.get_current_stage().name == "Stage"
        assert alias_py.get_stages() == [api_module.stage.return_value]
        assert alias_py.create_stage("new-stage") == 0
        api_module.stages.create.assert_called_once_with("new-stage")

    def test_get_product_information_uses_al_product(self, alias_py_class, monkeypatch):
        api_module = self._new_api_module()
        alias_py = alias_py_class(api_module)

        monkeypatch.setenv("ALIAS_PRODUCT_LIC_TYPE", "network")
        monkeypatch.setenv("ALIAS_PRODUCT_LIC_PATH", "/lic/path")

        product_info = alias_py.get_product_information()
        assert product_info == {
            "product_key": "966S1",
            "product_version": "2027.0.0.F",
            "product_license_type": "network",
            "product_license_path": "/lic/path",
        }

    def test_pick_list_compat_without_first_pick_item(self, alias_py_class):
        api_module = self._new_api_module()
        alias_py = alias_py_class(api_module)

        assert alias_py.first_pick_item() == 0
        assert alias_py.get_current_pick_item() == "pick-item"

        api_module.get_pick_items.return_value = []
        assert alias_py.first_pick_item() == 1
        assert alias_py.get_current_pick_item() is None

    def test_adjust_window_patch_for_old_api(self, alias_py_class):
        api_module = types.ModuleType("alias_api")
        alias_py = alias_py_class(api_module)

        assert alias_py.adjust_window() is None

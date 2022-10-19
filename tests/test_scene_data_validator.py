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
from collections import namedtuple

import sys


class TestAliasSceneDataValidator(object):
    """
    A test class for the AliasDataValidator class functionality.

    TODO add more unit tests to check the SDV check and fix functions.
    """

    # An ugly workaround untili python 2 unit tests are removed from Azure Pipeline CI
    if sys.version_info.major < 3:
        __test__ = False
    else:
        __test__ = True

    @pytest.fixture
    def validator_class(request):
        """
        Fixture to return the AliasDataValidator class.

        Defer the import until this fixture to avoid import errors when this test class should
        be ignored.
        """

        from tk_alias import AliasDataValidator

        return AliasDataValidator

    @pytest.fixture
    def validator(request, validator_class):
        """Fixture to return an AliasSceneValidator object."""
        return validator_class()

    @pytest.fixture
    def error_namedtuple(request):
        """Fixture to return a namedtuple to represent a Validation Error object."""
        return namedtuple("ValidationError", ["id", "name", "type"])

    @pytest.fixture
    def error_without_id_namedtuple(request):
        """Fixture to return a namedtuple to represent a Validation Error object without an id."""
        return namedtuple("ValidationErrorWithoutId", ["name", "type"])

    # NOTE the CheckResult class was moved to the data validation hook and renamed to SanitizedResult
    # TODO run these test cases against the new class
    #
    # def test_check_result_init_default(self, validator_class):
    #     """
    #     Test the CheckResult default init.
    #     """

    #     result = validator_class.CheckResult()
    #     assert result.is_valid is True
    #     assert result.errors == []
    #     assert result.args == []
    #     assert result.kwargs == {"error_items": []}

    # @pytest.mark.parametrize(
    #     "is_valid",
    #     [
    #         None,
    #         True,
    #         False,
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     "errors",
    #     [
    #         None,
    #         [],
    #         [
    #             ["id_1", "name_1", lambda: "type_1"],
    #             ["id_2", "name_2", lambda: "type_2"],
    #         ],
    #     ],
    # )
    # def test_check_result_init_with_is_valid(
    #     self, validator_class, error_namedtuple, is_valid, errors
    # ):
    #     """
    #     Test the CheckResult init passing is_valid field.
    #     """

    #     if errors is not None:
    #         for i, err in enumerate(errors):
    #             errors[i] = error_namedtuple(*err)

    #     result = validator_class.CheckResult(is_valid=is_valid, errors=errors)

    #     if is_valid is not None:
    #         assert result.is_valid is is_valid
    #     elif not errors:
    #         assert result.is_valid is True
    #     else:
    #         assert result.is_valid is False

    # @pytest.mark.parametrize(
    #     "errors",
    #     [
    #         None,
    #         [],
    #         [
    #             ["id_1", "name_1", lambda: "type_1"],
    #             ["id_2", "name_2", lambda: "type_2"],
    #             [None, "name_3", lambda: "type_3"],
    #             [None, "name_4", lambda: None],
    #         ],
    #     ],
    # )
    # def test_check_result_init_with_errors(
    #     self, validator_class, error_namedtuple, errors
    # ):
    #     """
    #     Test the CheckResult init passing errors field.
    #     """

    #     expected_errors = []
    #     if errors is not None:
    #         for i, err in enumerate(errors):
    #             err_obj = error_namedtuple(*err)
    #             errors[i] = err_obj
    #             expected_errors.append(
    #                 {
    #                     "id": err_obj.id if err_obj.id else err_obj.name,
    #                     "name": err_obj.name,
    #                     "type": err_obj.type(),
    #                 }
    #             )

    #     result = validator_class.CheckResult(errors=errors)

    #     for i, err in enumerate(result.errors):
    #         assert err["id"] == errors[i].id if errors[i].id else errors[i].name
    #         assert err["name"] == errors[i].name
    #         assert err["type"] == errors[i].type()
    #         assert "error_items" in result.kwargs

    #     if errors is None:
    #         assert result.kwargs["error_items"] == []
    #     else:
    #         assert result.kwargs["error_items"] == errors

    # @pytest.mark.parametrize(
    #     "errors",
    #     [
    #         None,
    #         [],
    #         [
    #             ["name_1", lambda: "type_1"],
    #             ["name_2", lambda: "type_2"],
    #             ["name_3", lambda: None],
    #         ],
    #     ],
    # )
    # def test_check_result_init_with_errors_but_no_id(
    #     self, validator_class, error_without_id_namedtuple, errors
    # ):
    #     """
    #     Test the CheckResult init passing errors field with errors without ids.
    #     """

    #     expected_errors = []
    #     if errors is not None:
    #         for i, err in enumerate(errors):
    #             err_obj = error_without_id_namedtuple(*err)
    #             errors[i] = err_obj
    #             expected_errors.append(
    #                 {"id": err_obj.name, "name": err_obj.name, "type": err_obj.type()}
    #             )

    #     result = validator_class.CheckResult(errors=errors)

    #     for i, err in enumerate(result.errors):
    #         assert err["id"] == errors[i].name
    #         assert err["name"] == errors[i].name
    #         assert err["type"] == errors[i].type()
    #         assert "error_items" in result.kwargs

    #     if errors is None:
    #         assert result.kwargs["error_items"] == []
    #     else:
    #         assert result.kwargs["error_items"] == errors

    # @pytest.mark.parametrize(
    #     "args",
    #     [
    #         None,
    #         [],
    #         [1, 2, 3],
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     "kwargs",
    #     [
    #         None,
    #         {},
    #         {"1": 1, "2": 2, "3": 3},
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     "errors",
    #     [
    #         None,
    #         [],
    #         [
    #             ["name_1", lambda: "type_1"],
    #             ["name_2", lambda: "type_2"],
    #             ["name_3", lambda: None],
    #         ],
    #     ],
    # )
    # def test_check_result_init_with_args_kwargs(
    #     self, validator_class, error_without_id_namedtuple, args, kwargs, errors
    # ):
    #     """
    #     Test the CheckResult init passing args and kwargs fields.
    #     """

    #     if errors is not None:
    #         for i, err in enumerate(errors):
    #             errors[i] = error_without_id_namedtuple(*err)

    #     result = validator_class.CheckResult(errors=errors)

    #     for i, err in enumerate(result.errors):
    #         assert err["id"] == errors[i].name
    #         assert err["name"] == errors[i].name
    #         assert err["type"] == errors[i].type()

    # def test_get_validation_data(self, validator):
    #     """
    #     Test the get_validation_data method.

    #     This simply checks that the validation rule ids are defined.
    #     """

    #     expected_validation_rule_ids = [
    #         "shader_unused",
    #         "shader_is_vred_compatible",
    #         "node_is_null",
    #         "node_has_construction_history",
    #         "node_instances",
    #         "node_has_zero_transform",
    #         "node_templates",
    #         "cos_unused",
    #         "cos_construction_history",
    #         "curves",
    #         "set_empty",
    #         "group_has_single_level_hierarchy",
    #         "layer_is_empty",
    #         "layer_has_single_object",
    #         "layer_symmetry",
    #         "locators",
    #         "references_exist",
    #         "metadata",
    #         "node_dag_top_level",
    #         "node_is_not_in_layer",
    #         "node_layer_matches_parent",
    #         "node_name_matches_layer",
    #     ]

    #     data = validator.get_validation_data()

    #     for expected_id in expected_validation_rule_ids:
    #         assert expected_id in data

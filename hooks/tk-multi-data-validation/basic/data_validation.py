# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class AliasDataValidationHook(HookBaseClass):
    """Hook to define Alias data validation functionality."""

    class AliasDataValidationError(Exception):
        """Custom exception class to report Alias Data Validation errors."""

    class SanitizedResult:
        """Class to represent a sanitized check result object."""

        def __init__(self, is_valid=None, errors=None):
            """
            Initialize the object with the given data.

            :param is_valid: The success status that the check function reported. If not provided, the validity will be determined based on if there are any errors.
            :type is_valid: bool
            :param errors: The data errors the check function found. This should be a list of Alias objects, but
                can be a list of object as long as they follow the expected format.
            :type errors: list
            """

            if is_valid is None:
                self.is_valid = not errors
            else:
                self.is_valid = is_valid

            if errors:
                self.errors = [
                    {
                        "id": item.id if hasattr(item, "id") and item.id else item.name,
                        "name": item.name,
                        "type": item.type(),
                    }
                    for item in errors
                ]
            else:
                self.errors = []

    def get_validation_data(self):
        """
        Return the validation rule data set to validate an Alias scene.

        This method will retrieve the default validation rules returned by
        :meth:`AliasDataValidator.get_validation_data`. To customize the default
        validation rules, override this hook method to modify the returned data dictionary.

        The dictionary returned by this function should be formated such that it can be passed
        to the :class:`~tk-multi-data-validation:api.data.ValidationRule` class constructor to
        create a new validation rule object.

        :return: The validation rules data set.
        :rtype: dict
        """

        data = self.parent.engine.data_validator.get_validation_data()

        # -------------------------------------------------------------------------------------------------------
        #
        # Example:
        #   How to add a custom rule to the default list of validation rules (the data above)
        #
        #   This example assume that the tk-multi-data-validation App is being used to display the validation
        #   data, and to perform the validation functionality.
        #
        # -------------------------------------------------------------------------------------------------------
        #
        #   Step (1) - define the necessary check, fix, and action callbacks that are required by your new rule.
        #   Step (2) - add your custom rule entry into the validation data dictionary `data`
        #   Step (3) - add your custom rule id to your tk-multi-data-validation.yml config settings
        #
        # -------------------------------------------------------------------------------------------------------
        #
        # # Define a global variable to toggle the custom rule valid state, for demonstrations purposes
        # global custom_rule_is_valid
        # custom_rule_is_valid = False
        #
        # def check_my_custom_rule(fail_fast=False):
        #     """
        #     This callback method will execute when the "Validate" button is clicked for this
        #     rule, or validate all is initiated.
        #
        #     NOTE that the check function takes one parameter, `fail_fast`, even if it is not
        #     used, it should still be defined to follow the "check"functions guidelines (see
        #     AliasDataValidator class for more info).
        #
        #     For examples of more advanced check functions, see the AliasDataValidator class
        #     methods prefixed with `check_`.
        #     """
        #
        #     if fail_fast:
        #         # In a fail fast context, just return True or False indicating if the rule is valid
        #         return custom_rule_is_valid
        #
        #     if custom_rule_is_valid:
        #         # Do not report any errors if the rule is valid
        #         errors = None
        #     else:
        #         # The rule is not valid, return the Alias objects that do not pass the check.
        #         # In this example, we using a namedtuple to return a list of Alias objects, but
        #         # a list of Alias objects retrieved from the Alias Python API can also be used
        #         # directly.
        #         from collections import namedtuple
        #         AliasObject = namedtuple("AliasObject", ["name", "type"])
        #         errors = [
        #             AliasObject("node#1", lambda: "AlSurfaceNode()"),
        #             AliasObject("node#2", lambda: "AlSurfaceNode()"),
        #         ]
        #
        #     # If not fail faist, check functions should return the list of error objects
        #     return errors
        #
        # def fix_my_custom_rule(errors=None):
        #     """
        #     This callback method will execute when the "Fix" button is clicked for this rule,
        #     or the fix all is initiated.
        #
        #     This fix function just sets the global valid state to True so that the next time
        #     the check function is executed, it will have a valid state of True.
        #
        #     NOTE that the fix function takes one parameter, `errors`, this is not used here
        #     for simplicity, but it should still be defined to follow the "fix" function
        #     guidelines (see AliasDataValidator class for more info).
        #
        #     For examples of more advanced fix functions, see the AliasDataValidator class
        #     methods prefixed with `fix_`.
        #     """
        #     global custom_rule_is_valid
        #     custom_rule_is_valid = True
        #
        # def action_callback(errors=None):
        #     """
        #     This callback method will execute when the action item is clicked for this rule.
        #
        #     The action item can be found by right-clicking the rule to see the menu actions,
        #     or by clicking the "..." on the rule item row. It is the action called
        #
        #         'Click me! Revalidate to see what happend >:)"
        #
        #     This action function just sets the global valid state to False so that the next time
        #     the check function is executed, it will have a valid state of False.
        #
        #     NOTE that the fix function takes one parameter, `errors`, this is not used here
        #     for simplicity, but it should still be defined to follow the action function
        #     guidelines (see AliasDataValidator class for more info).
        #
        #     For examples of more advanced fix functions, see the AliasDataValidator class
        #     methods.
        #     """
        #     global custom_rule_is_valid
        #     custom_rule_is_valid = False
        #
        # # Step (2)
        # data["my_custom_rule"] = {
        #     "name": "My Custom Validation Rule",
        #     "description": """
        #         This is an example to demonstrate how to add a custom rule. Try validating it ----------><br/>
        #         Right-click and 'Show Details' to open the right-hand panel to see more.
        #     """,
        #     "error_msg": "An error has been found by this rule. Let's fix it!",
        #     "fix_name": "Fix it!",
        #     "check_func": check_my_custom_rule,
        #     "fix_func": fix_my_custom_rule,
        #     "actions": [
        #         {"name": "Click me! Revalidate to see what happend >:)", "callback": action_callback}
        #     ]
        # }

        return data

    def sanitize_check_result(self, result):
        """
        Sanitize the value returned by any validate function to conform to the standard format.

        Convert the incoming list of Alias objects (that are errors) to conform to the standard
        format that the Data Validation App requires:

            is_valid:
                type: bool
                description: True if the validate function succeed with the current data, else
                             False.

            errors:
                type: list
                description: The list of error objects (found by the validate function). None
                             or empty list if the current data is valid.
                items:
                    type: dict
                    key-values:
                        id:
                            type: str | int
                            description: A unique identifier for the error object.
                            optional: False
                        name:
                            type: str
                            description: The display name for the error object.
                            optional: False
                        type:
                            type: str
                            description: The display name of the error object type.
                            optional: True

        This method will be called by the Data Validation App after any validate function is
        called, in order to receive the validate result in the required format.

        :param result: The result returned by a validation rule ``check_func``. This is
            should be a list of Alias objects or a boolean value indicating the validity of
            the check.
        :type result: list

        :return: The result of a ``check_func`` in the Data Validation standardized format.
        :rtype: dict
        """

        if isinstance(result, bool):
            return self.SanitizedResult(is_valid=result)

        if isinstance(result, list):
            return self.SanitizedResult(errors=result)

        raise self.AliasDataValidationError(
            "Cannot sanitize result type '{}'".format(type(result))
        )

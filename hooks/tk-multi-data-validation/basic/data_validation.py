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


class DataValidationHook(HookBaseClass):
    """Hook to define Alias data validation functionality."""

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
        #     This check function just returns the CheckResult with the is_valid state set to
        #     the value of our global `custom_rule_is_valid` variable, and mocks an error list
        #     of objects if the state is not valid.
        #
        #     NOTE that the check function takes one parameter, `fail_fast`, this is not used
        #     here for simplicity, but it should still be defined to follow the "check"
        #     functions guidelines (see AliasDataValidator class for more info).
        #
        #     For examples of more advanced check functions, see the AliasDataValidator class
        #     methods prefixed with `check_`.
        #     """
        #
        #     if custom_rule_is_valid:
        #         # Do not report any errors if the rule is valid
        #         errors = None
        #     else:
        #         # The rule is not valid, pass an error list to the CheckResult object
        #         #
        #         # The errors list passed to the CheckResult object does not have to be a list
        #         # of Alias objects, but it must have the required attributes:
        #         #   1. name (str) - the name of the object (should be unique if 'id' is not included)
        #         #   2. type (function -> str) - returns the type of the object
        #         #   3. id (str) : optional - the unique identifier for the object
        #         #
        #         # Here is an example of what the objects in the error list should look like:
        #         from collections import namedtuple
        #         AliasObject = namedtuple("AliasObject", ["name", "type"])
        #         errors = [
        #             AliasObject("node#1", lambda: "AlSurfaceNode()"),
        #             AliasObject("node#2", lambda: "AlSurfaceNode()"),
        #         ]
        #
        #     # All validation check functions should return an
        #     # AliasDataValidator.CheckResult object. It is not required, but it must
        #     # follow the format that the tk-multi-data-validation ValidationRule expects.
        #     return self.parent.engine.data_validator.CheckResult(is_valid=custom_rule_is_valid, errors=errors)
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

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


class SceneValidatorHook(HookBaseClass):
    """
    Hook to define Alias scene validation functionality.
    """

    def get_validation_data(self):
        """
        Return the scene action data.

        The dictionary returned by this function should be formated such that it can be passed to the
        ValidationRule class constructor to ValidationRule objects.

        :return: The scene validation rules data to be consumed by the ValidationRule class constructor.
        :rtype: dict
        """

        return self.parent.engine.scene_validator.get_validation_data()

    def execute_check_action(self, action_name, *args, **kwargs):
        """
        Execute the Alias scene validation check function.

        :param action_name: The unique id to get the check function to execute.
        :type action_name: str
        :param args: The arguments list to pass to the check function.
        :type args: list
        :param kwargs: The keyword arguments dict to pass to the check function.
        :type kwargs: dict

        :return: The result of the check function that was executed.
        :rtype: AliasSceneValidator.CheckResult
        """

        return self.parent.engine.scene_validator.execute_check_action(
            action_name, *args, **kwargs
        )

    def execute_fix_action(self, action_name, *args, **kwargs):
        """
        Execute the Alias scene validation fix function.

        :param action_name: The unique id to get the fix function to execute.
        :type action_name: str
        :param args: The arguments list to pass to the check function.
        :type args: list
        :param kwargs: The keyword arguments dict to pass to the check function.
        :type kwargs: dict
        """

        return self.parent.engine.scene_validator.execute_fix_action(
            action_name, *args, **kwargs
        )

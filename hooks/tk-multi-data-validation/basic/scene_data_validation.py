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


class SceneDataValidationHook(HookBaseClass):
    """
    Hook to define Alias scene validation functionality.
    """

    def get_validation_data(self):
        """
        Return the validation rule data set to validate an Alias scene.

        This method will retrieve the default validation rules returned by
        :meth:`AliasSceneDataValidator.get_validation_data`. To customize the default
        validation rules, override this hook method to modify the returned data dictionary.

        The dictionary returned by this function should be formated such that it can be passed
        to the :class:`~tk-multi-data-validation:data.ValidationRule` class constructor to
        create a new validation rule object.

        :return: The validation rules data set.
        :rtype: dict
        """

        return self.parent.engine.scene_data_validator.get_validation_data()

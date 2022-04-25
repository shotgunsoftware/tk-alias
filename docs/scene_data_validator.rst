.. _scene_data_validator:

Scene Data Validator
######################################

Overview
***********

The :ref:`Alias Scene Data Validator (ASDV) <scene_data_validator-class>` is the backbone to performing data validation on an Alias scene. This class defines the default data validation rule set, that determines if the data in an Alias scene is valid or not, and provides the necessary actions to resolve the data errors.

How to use it
===============

The :class:`tk_alias.scene_data_validator.AliasSceneDataValidator` includes the core functionality to perform the scene data validation, but does not provide a user interface to use it. The :class:`~tk-multi-data-validation:dialog` App provides the user interface for a DCC to perform data validation.

The Alias Engine instantiates an AliasSceneDataValidator class member :class:`AliasEngine.scene_data_validator` that is used by the `tk-multi-data-validation` App via the engine :ref:`hook <hooks-tk-multi-data-validation-data-validator>`.

.. _scene_data_validator-class:

.. currentmodule:: tk_alias.scene_data_validator

.. autoclass:: AliasSceneDataValidator
    :show-inheritance:
    :members:

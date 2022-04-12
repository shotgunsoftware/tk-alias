.. _scene_data_validator:

Scene Data Validator
######################################

Overview
***********

The :ref:`Alias Scene Data Validator (ASDV) <scene_data_validator-class>` is the backbone to performing data validation on an Alias scene. This class defines the default data validation rule set, which determines if the data in an Alias scene is valid or not, and provides the actions to resolve those violations in the data.

How to use it
===============

The :class:`tk_alias.scene_data_validator.AliasSceneDataValidator` includes the core functionality to perform the scene data validation, but does not provide a user interface to use it.

The Engine instantiates a class member that is an `AliasSceneDataValidator`, and can be used by the `tk-multi-data-validation` Toolkit App.

The tk-multi-data-validation App provides the user interface for a DCC to perform data validation.

See the :ref:`hook <hooks-tk-multi-data-validation-data-validator>` for more details.

.. _scene_data_validator-class:

.. currentmodule:: tk_alias.scene_data_validator

.. autoclass:: AliasSceneDataValidator
    :show-inheritance:
    :members:

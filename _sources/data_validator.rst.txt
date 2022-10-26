.. _data_validator:

Data Validator
######################################

Overview
***********

The :ref:`Alias Data Validator (ADV) <data_validator-class>` is the backbone to performing data validation on Alias data. This class defines the default data validation rule set, that determines if the data in Alias is valid or not, and provides the necessary actions to resolve the data errors.

How to use it
===============

The :class:`tk_alias.data_validator.AliasDataValidator` includes the core functionality to perform the data validation, but does not provide a user interface to use it. The :class:`~tk-multi-data-validation:dialog` App provides the user interface for a DCC to perform data validation.

The Alias Engine instantiates an AliasDataValidator class member :class:`AliasEngine.data_validator` that is used by the `tk-multi-data-validation` App via the engine :ref:`hook <hooks-tk-multi-data-validation-data-validator>`.

.. _data_validator-class:

.. currentmodule:: tk_alias.data_validator

.. autoclass:: AliasDataValidator
    :show-inheritance:
    :members:

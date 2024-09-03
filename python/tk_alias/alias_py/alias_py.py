# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from typing import Optional
from types import ModuleType

from . import dag_node, layer, pick_list, utils
from ..framework_alias import ClientRequestContextManager, AliasClientModuleProxyWrapper


class AliasPy:
    """
    Wrapper class for the Alias Python API module.

    This wrapper class is used by the Alias Engine to access the Alias Python API module,
    instead of accessing the module directly, to help handle multiple api versions. This allows
    the engine to run with any version of Alias, which each may require different versions of
    the api.

    The purpose is to route Alia api requests to the main api module. The way it does this is
    by override the `__getattr__` method, which will be called when an attribute is accessed
    on the AliasPy class, but it does not exist. Then the `__getattr__` method will look up
    the attribute on the Alias api module and return the api attribute. This means that any
    attribute defined on the AliasPy class will override the Alias api attribute, so for this
    reason, the AliasPy class should only define methods to patch Alias api attributes and
    properties that return objects with Alias api helper functionality. Any non private
    attributes (attributes not defined with `__` prefix) should be prefixed with `py_` to help
    avoid name collisions with the Alias api. In addition, unit tests should be added whenever
    this class is modified to ensure there are not any naming collisions.
    """

    class ApiAttributeNotSupported(AttributeError):
        """Thrown when an Alias Python API accessing an attribute that is not supported."""

    def __init__(
        self,
        api_module: ModuleType,
        api_proxy_module: Optional[AliasClientModuleProxyWrapper] = None,  # type: ignore
    ):
        """
        Initialize.

        One of `api_module` or `api_proxy_module` is required. The `api_module`
        should be provided when running in the same process as Alias, and the
        Alias Python API module is directly accessible. The `api_proxy_module`
        should be provided when running in a separate process than Alias, and
        the Alias Python API module is not directly accessible, and we need to
        communicate with Alias through IPC.

        :param api_module: The Alias Python API module.
        :param api_proxy_module: The Alias Python API proxy module.
        """

        # The main Alias api module. This module is used to make requests to Alias.
        self.__api = api_module
        # The Alias api proxy module. When runnig in a separate process than
        # Alias, a proxy module is created to mimic the actual Alias api
        # module, which lives on the Alias (server) side. This proxy module
        # handles the IPC communication between the us (client) and
        # Alias (server).
        self.__api_proxy = api_proxy_module

        # Helper modules that use the main Alias api module.
        self.__dag_node = dag_node.AliasPyDagNode(self)
        self.__layer = layer.AliasPyLayer(self)
        self.__pick_list = pick_list.AliasPyPickList(self)
        self.__utils = utils.AliasPyUtils(self)

        # Define patch functions for Alias api attributes. The keys are the Alias api
        # attribute name, and the values are the functions to call when the Alias api
        # does not have the attribute (e.g. some attributes available only in certain
        # api versions)
        self.__patch_attributes = {
            "adjust_window": self.__get_patch_adjust_window,
        }

    def __getattr__(self, name):
        """
        Get the attribute from the Alias api module.

        From the Python docs:

            Called when the default attribute access fails with an AttributeError (either
            __getattribute__() raises an AttributeError because name is not an instance
            attribute or an attribute in the class tree for self; or __get__() of a name
            property raises AttributeError). Note that if the attribute is found through the
            normal mechanism, __getattr__() is not called.

        The AliasPy class is a wrapper for the Alias api module. Accessing an attribute
        through the AliasPy class will return attribute from the Alias api module, unless the
        attribute is defined on the AliasPy class. For this reason, the AliasPy class should
        not define any other functionality, with the exception to methods that are used to
        provide patches for Alias api attributes (for version handling), or properties that
        return objects that contain Alias api helper functionality. To avoid attribute name
        collisions, prefix all AliasPy attributes with `py_`.

        :param name: The name of the attribute to get.
        :type name: str

        :raises AttributeError: If the attribute not found for the Alias api.

        :return: The Alias api attribute for the given name.
        :rtype: Any
        """

        try:
            # Get the attribute from the api module
            #
            # NOTE if attributes exist in multiple api versions, but require different
            # handling (e.g. function signature changed), then a patch function will need
            # to be run before returning the attribute immediately if it exists.
            return getattr(self.__api, name)

        except AttributeError:
            # Attribute not found in the api, try to patch it.
            patch_func = self.__patch_attributes.get(name)
            if patch_func:
                patched_attr = patch_func()
            else:
                patched_attr = None

            if patched_attr is None:
                raise AliasPy.ApiAttributeNotSupported(
                    f"This Alias version does not support the API attribute: {name}"
                )

            return patched_attr

    # Properties
    # -------------------------------------------------------------------------
    # Alias API helper modules. Prefix with 'py_' to help avoid name collisions
    # with the main api module

    @property
    def py_dag_node(self):
        """Get the helper module for handling Alias dag nodes."""
        return self.__dag_node

    @property
    def py_layer(self):
        """Get the helper module for handling Alias layers."""
        return self.__layer

    @property
    def py_pick_list(self):
        """Get the helper module for handling the Alias pick list."""
        return self.__pick_list

    @property
    def py_utils(self):
        """Get the helper module for performing general functionality in Alias."""
        return self.__utils

    # Public methods
    # ----------------------------------------------------------------------------------------

    def request_context_manager(self, is_async: Optional[bool] = False):
        """
        Return a context manager to handle executing multiple requests at once.
        """

        return ClientRequestContextManager(self.__api_proxy, is_async)

    # Private methods
    # ----------------------------------------------------------------------------------------

    def __get_patch_adjust_window(self):
        """
        Patch the api module function adjust_window.

        The adjust_window function was added in Alias Python API v4.0.0, which is compatibile
        with Alias >= 2024.0. This method should only be used for Alias < 2024.0.

        The patched function will do nothing and return.
        """

        def __patch_adjust_window(*args, **kwargs):
            return

        return __patch_adjust_window

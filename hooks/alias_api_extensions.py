# Copyright (c) 2025 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class AliasApiExtensionsHook(HookBaseClass):
    """
    Hook to allow defining additional Alias Python API functions that can
    be executed on the server side.

    This hook class should only contain a single method:

        get_alias_api_extensions_path

    This hook class itself should not:
        - Import the `alias_api` module
        - Define any methods for extending the Alias Python API
    """

    def get_alias_api_extensions_path(self) -> str:
        """
        Returns a file path to Alias Python API extension functions.

        The file path returned can be one of the following:
            - A file path to a python file containing the extension functions
            - A directory path to containing python files that contain the extension
            functions

        The python file(s) containing the extension functions should only contain:
            - Global functions that are standalone (e.g. any non built-in python
              modules must be imported for each function)
            - Each function must be JSON-serializable

        The extension functions will have access to the `alias_api` module at
        run time (e.g. do not import the `alias_api` module).

        The extension functions will be made available through the `alias_api`
        module in the `AliasApiExtensions` class.

        Default implementation returns None, which does not add any extension
        functions to the Alias Python API. Override this hook method to return
        the location of your custom extension functions.

        Directory Example:
            # Return a directory path containing python files with extension functions
            # that is located in the tk-alias/hooks/alias_custom_api directory
            return os.path.join(os.path.dirname(__file__), "alias_custom_api")

        Single File Example:
            # Return a file path to a python file with extension functions
            # that is located in the tk-alias/hooks/alias_custom_api directory
            return os.path.join(os.path.dirname(__file__), "alias_custom_api.py")

        :return: A directory or file path to Alias Python API extension functions,
            or None if no extension functions are to be added.
        """

        return None

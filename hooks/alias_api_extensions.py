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

    This hook class should only contain a single method that returns the
    file path to python file that only contains the additional Alias API
    functions. This hook class itself should not define any Alias API
    functions.
    """

    def get_alias_api_extensions_path(self) -> str:
        """
        Returns the file path to the custom Alias API functions.

        The contents of the file, whose file path is returned here, should only
        contain global functions. The global functions will be loaded by the
        tk-framework-alias server and will be made available through the
        `alias_api` module class object `AliasApiExtensions`. At runtime on the
        server side, the global functions will have access to the `alias_api`
        module.

        Default implementation returns None, which means no custom Alias API
        functions will be loaded. Override this hook method to return the location
        of your custom Alias API functions file.
        """

        return None

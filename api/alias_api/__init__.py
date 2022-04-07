# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.

import os
import sys

ALIAS_API = {
    "alias2021.3": {"min_version": "2021.3"},
    "alias2020.3-alias2021": {"min_version": "2020.3", "max_version": "2021.2.2"},
    "alias2019-alias2020.2": {"min_version": "2019", "max_version": "2020.2.2"},
}


def import_alias_api():
    """
    Import the right module according to some criteria:
    - the version of Alias
    - the version of Python
    - the execution mode (interactive vs non-interactive)
    """

    alias_release_version = os.environ.get("TK_ALIAS_VERSION")
    if not alias_release_version:
        return

    # get the name of the folder containing the files to import according to the version of Alias we want to use
    api_folder_name = None
    for api_folder in ALIAS_API:
        min_version = ALIAS_API[api_folder].get("min_version")
        max_version = ALIAS_API[api_folder].get("max_version")
        if min_version and alias_release_version < min_version:
            continue
        if max_version and alias_release_version > max_version:
            continue
        api_folder_name = api_folder

    if not api_folder_name:
        return

    # get the right file to import according to the running mode (interactive vs non-interactive)
    module_name = "alias_api" if os.path.basename(sys.executable) == "Alias.exe" else "alias_api_om"
    module_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            # "..",
            "python{}".format(sys.version_info.major),
            api_folder_name,
            "{}.pyd".format(module_name)
        )
    )

    if not os.path.exists(module_path):
        return

    # finally, import the alias_api module directly from the pyd file
    if sys.version_info.major == 3:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        alias_api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(alias_api)
    else:
        import imp
        alias_api = imp.load_source("alias_api", module_path)

    # add the newly created module oject to sys.modules and remap the globals accessor to point at our new module
    sys.modules["alias_api"] = alias_api
    globals()["alias_api"] = sys.modules["alias_api"]


import_alias_api()

# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.

import os
import sys

# The Alias Python API (APA) python module is decided based on the current version of Alias
# that is running. Defined here is the Alias version grouping:
#
#    < v2020.3              -- use APA from folder alias2019-alias2020.2
#   >= v2020.3 & < v2021.3  -- use APA from folder alias2020.3-alias2021
#   >= v2021.3 & < v2022.2  -- use APA from folder alias2021.3
#   >= v2022.2 & < v2023.0  -- use APA from folder alias2022.2
#   >= v2023.0              -- use APA from folder alias2023
#
# TODO: the Alias Python API, starting at version 2023.0, will have a build to match
#       the exact version of Alias that is running - update how we pick the python api
#       by specifying exact version, instead of by grouping (min/max version)
#
ALIAS_API = {
    "alias2023.1": {"min_version": "2023.1"},
    "alias2023.0": {"min_version": "2023.0", "max_version": "2023.1"},
    "alias2022.2": {"min_version": "2022.2", "max_version": "2023.0"},
    "alias2021.3": {"min_version": "2021.3", "max_version": "2022.2"},
    "alias2020.3-alias2021": {"min_version": "2020.3", "max_version": "2021.3"},
    "alias2019-alias2020.2": {"min_version": "2019", "max_version": "2020.3"},
}


class AliasPythonAPIImportError(Exception):
    """Exception for Alias Python API import errors."""

    pass


def version_cmp(version1, version2):
    """
    Compare the version strings.

    :param version1: A version string to compare against version2 e.g. 2022.2
    :param version2: A version string to compare against version1 e.g. 2021.3.1

    :return: The result of the comparison:
         1 - version1 is greater than version2
         0 - version1 and version2 are equal
        -1 - version1 is less than version2
    :rtype: int
    """

    # This will split both the versions by the '.' char to get the major, minor, patch values
    arr1 = version1.split(".")
    arr2 = version2.split(".")
    n = len(arr1)
    m = len(arr2)

    # Converts to integer from string
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]

    # Compares which list is bigger and fills the smaller list with zero (for unequal
    # delimeters)
    if n > m:
        for i in range(m, n):
            arr2.append(0)
    elif m > n:
        for i in range(n, m):
            arr1.append(0)

    # Returns 1 if version1 is greater
    # Returns -1 if version2 is greater
    # Returns 0 if they are equal
    for i in range(len(arr1)):
        if arr1[i] > arr2[i]:
            return 1
        elif arr2[i] > arr1[i]:
            return -1
    return 0


def import_alias_api():
    """
    Import the right Alias Python API module according to the criteria:
        - the version of Alias
        - the execution mode (interactive vs non-interactive)

    The Alias Python API supports Python >= 3
    """

    # Import requires python >= 3, place it inside this function so that the python version
    # can be checked first, without failing to import.
    import importlib.util

    # Get the Alias version from the environment variable
    alias_release_version = os.environ.get("TK_ALIAS_VERSION")
    if alias_release_version == "docs":
        # Special case handling when importing the module to generate docs. Just skip the
        # whole import process since Sphinx does not actually need the module set up, it
        # just needs to access the code
        return

    if not alias_release_version:
        msg = "Alias version is not set. Set the environment variable TK_ALIAS_VERSION (e.g. 2022.2)."
        raise AliasPythonAPIImportError(msg)

    # Determine the name of the folder containing the files to import according to the version
    # of Alias
    api_folder_name = None
    for api_folder in ALIAS_API:
        min_version = ALIAS_API[api_folder].get("min_version")
        if min_version and version_cmp(alias_release_version, min_version) < 0:
            continue

        max_version = ALIAS_API[api_folder].get("max_version")
        if max_version and version_cmp(alias_release_version, max_version) >= 0:
            continue

        api_folder_name = api_folder

    if not api_folder_name:
        raise AliasPythonAPIImportError(
            "Cound not determine module path for Alias version {}".format(
                alias_release_version
            )
        )

    # Get the right file to import according to the running mode (interactive vs non-interactive)
    module_name = (
        "alias_api"
        if os.path.basename(sys.executable) == "Alias.exe"
        else "alias_api_om"
    )
    module_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "python3",
            api_folder_name,
            "{}.pyd".format(module_name),
        )
    )
    if not os.path.exists(module_path):
        raise AliasPythonAPIImportError("Module does not exist {}".format(module_path))

    # Find and create the module spec object for the Alias Python API
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not spec:
        # NOTE importlib.util.spec_from_location does not seem to find the module on macos
        raise AliasPythonAPIImportError(
            "Could not find the Alias Python API module {}".format(module_path)
        )

    try:
        alias_api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(alias_api)
    except Exception as e:
        info_msg = "The specific Alias version that the Alias Python API requires must be installed. The Alias bin directory path must be in the system environment PATH variable. If more than one version of Alias is installed, it must appear before all other versions in the PATH."
        raise AliasPythonAPIImportError(
            "{error}\n{info}".format(error=str(e), info=info_msg)
        )

    # Add the newly created module oject to sys.modules and remap the globals accessor to point at our new module
    sys.modules["alias_api"] = alias_api
    globals()["alias_api"] = sys.modules["alias_api"]


#
# First check the python version is at least 3
#
if sys.version_info.major < 3:
    error_msg = "Alias Python API only supports Python 3. You are using Python {major}.{minor}. Please refer to this <a href='https://github.com/shotgunsoftware/tk-alias/wiki/Python-Version-Support'>page</a> for additional information.".format(
        major=sys.version_info.major,
        minor=sys.version_info.minor,
    )
    raise AliasPythonAPIImportError(error_msg)

#
# Import the Alias Python API module
#
import_alias_api()

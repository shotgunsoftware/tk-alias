# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import re
import sys

import sgtk
from sgtk.platform import SoftwareLauncher, SoftwareVersion, LaunchInformation


class AliasLauncher(SoftwareLauncher):
    """
    Handles launching Alias executables.

    Automatically starts up a tk-alias engine with the current
    context.
    """

    # Product code names
    CODE_NAMES = {
        "AutoStudio": dict(flags="-a as", icon="icon_as_256.png"),
        "Surface": dict(flags="-a ss", icon="icon_ss_256.png"),
        "Design": dict(flags="-a ds", icon="icon_cs_256.png"),
        "Concept": dict(flags="-a cs", icon="icon_cs_256.png"),
    }

    # Named regex strings to insert into the executable template paths when
    # matching against supplied versions and products. Similar to the glob
    # strings, these allow us to alter the regex matching for any of the
    # variable components of the path in one place
    COMPONENT_REGEX_LOOKUP = {
        "version": r"[\d.]+",
        "code_name": "(?:{code_names})".format(code_names="|".join(CODE_NAMES)),
    }

    # Fallback code name to use when none is given
    FALLBACK_CODE_NAME = "AutoStudio"

    # # ShotGrid default plugins
    ALIAS_PLUGINS = {
        "alias2022.2": {"min_version": "2022.2"},
        "alias2021.3": {"min_version": "2021.3", "max_version": "2022.2"},
        "alias2020.3-alias2021": {"min_version": "2020.3", "max_version": "2021.3"},
        "alias2019-alias2020.2": {"min_version": "2019", "max_version": "2020.3"},
    }

    # This dictionary defines a list of executable template strings for each
    # of the supported operating systems. The templates are used for both
    # globbing and regex matches by replacing the named format placeholders
    # with an appropriate glob or regex string. As Side FX adds modifies the
    # install path on a given OS for a new release, a new template will need
    # to be added here.
    EXECUTABLE_TEMPLATES = {
        "win32": [
            # Example: C:\Program Files\Autodesk\AliasAutoStudio2019\bin\Alias.exe
            r"C:\Program Files\Autodesk\Alias{code_name}{version}\bin\Alias.exe",
        ],
    }

    @property
    def minimum_supported_version(self):
        """The minimum software version that is supported by the launcher."""
        return "2019"

    def prepare_launch(self, exec_path, args, file_to_open=None):
        """
        Prepares an environment to launch Alias.

        This environment will automatically load Toolkit and the tk-alias engine when
        the program starts.

        :param str exec_path: Path to Alias executable.
        :param str args: Command line arguments as strings.
        :param str file_to_open: (optional) Full path name of a file to open on launch.
        :returns: :class:`LaunchInformation` instance
        """
        required_env = {}
        args = self._clean_args(args)

        # Add flags according to the code_name
        tk_alias_codename = None
        for code_name, data in self.CODE_NAMES.items():
            if code_name in exec_path and data.get("flags"):
                flags = self._clean_args(data.get("flags"))
                if flags not in args:
                    args += " " + flags
                tk_alias_codename = code_name
                break

        # Flag -P (plugins list file)
        plugins_list_file = self._get_plugins_list_file(exec_path, tk_alias_codename)
        if plugins_list_file:
            args += ' -P "{0}'.format(plugins_list_file)
            args += '"'

        # Append executable folder to PATH environment variable
        sgtk.util.append_path_to_env_var("PATH", os.path.dirname(sys.executable))

        # Make the engine startup module to be available when Alias starts up
        # by appending it to the env PYTHONPATH.
        startup_path = os.path.join(self.disk_location, "startup")
        sgtk.util.append_path_to_env_var("PYTHONPATH", startup_path)

        # Add the root path of the Alias Python API to the PYTHONPATH
        # The right module will be loaded at import time according to some criteria
        # (the Alias version, the Python version and the execution mode)
        alias_api_path = os.path.join(self.disk_location, "api")
        sgtk.util.append_path_to_env_var("PYTHONPATH", alias_api_path)

        # We're going to append all of this Python process's sys.path to the
        # PYTHONPATH environment variable. This will ensure that we have access
        # to all libraries available in this process. We're appending instead of
        # setting because we don't want to stomp on any PYTHONPATH that might already
        # exist that we want to persist
        sgtk.util.append_path_to_env_var("PYTHONPATH", os.pathsep.join(sys.path))

        required_env["PYTHONPATH"] = os.environ["PYTHONPATH"]

        # Prepare the launch environment with variables required by the
        # classic bootstrap approach.
        self.logger.debug("Preparing Alias Launch...")
        required_env["SGTK_ENGINE"] = self.engine_name
        required_env["SGTK_CONTEXT"] = sgtk.context.serialize(self.context)

        if file_to_open:
            # Add the file name to open to the launch environment
            required_env["SGTK_FILE_TO_OPEN"] = file_to_open

        # Add executable path and codename
        required_env["TK_ALIAS_EXECPATH"] = exec_path

        if tk_alias_codename:
            tk_alias_codename_lower = tk_alias_codename.lower()
            required_env["TK_ALIAS_VERSION"] = self._get_release_version(
                exec_path, tk_alias_codename
            )
        else:
            tk_alias_codename_lower = self.FALLBACK_CODE_NAME.lower()
            required_env["TK_ALIAS_VERSION"] = self._get_release_version(
                exec_path, self.FALLBACK_CODE_NAME
            )

        required_env["TK_ALIAS_CODENAME"] = tk_alias_codename_lower

        return LaunchInformation(exec_path, args, required_env)

    ##########################################################################################
    # private methods

    def _icon_from_executable(self, code_name):
        """
        Find the application icon based on the code_name.

        :param code_name: Product code_name (AutoStudio, Design, ...).

        :returns: Full path to application icon as a string or None.
        """
        if code_name in self.CODE_NAMES:
            icon_name = self.CODE_NAMES.get(code_name).get("icon")
            path = os.path.join(self.disk_location, "icons", icon_name)
        else:
            path = os.path.join(self.disk_location, "icon_256.png")

        return path

    def scan_software(self):
        """
        Scan the filesystem for maya executables.

        :return: A list of :class:`SoftwareVersion` objects.
        """
        self.logger.debug("Scanning for Alias executables...")

        supported_sw_versions = []
        for sw_version in self._find_software():
            (supported, reason) = self._is_supported(sw_version)
            if supported:
                supported_sw_versions.append(sw_version)
            else:
                self.logger.debug(
                    "SoftwareVersion %s is not supported: %s" % (sw_version, reason)
                )

        return supported_sw_versions

    def _find_software(self):
        """
        Find executables in the default install locations.
        """
        # all the executable templates for the current OS
        executable_templates = self.EXECUTABLE_TEMPLATES.get(sys.platform, [])

        # all the discovered executables
        sw_versions = []

        for executable_template in executable_templates:
            self.logger.debug("Processing template %s.", executable_template)

            executable_matches = self._glob_and_match(
                executable_template, self.COMPONENT_REGEX_LOOKUP
            )

            # Extract all products from that executable.
            for (executable_path, key_dict) in executable_matches:
                # extract the matched keys form the key_dict (default to None if
                # not included)
                version = key_dict.get("version")
                code_name = key_dict.get("code_name")

                sw_versions.append(
                    SoftwareVersion(
                        version,
                        "Alias {code_name}".format(code_name=code_name),
                        executable_path,
                        self._icon_from_executable(code_name),
                    )
                )

        return sw_versions

    def _get_plugins_list_file(self, exec_path, code_name):
        """
        Generates plugins.lst file used by alias in the plugins bootstrap process

        :exec_path: alias executable file path
        :code_name: alias code name
        :return: plugins.lst path
        """

        plugins_directory = os.path.join(self.disk_location, "plugins")
        if not os.path.isdir(plugins_directory):
            return None

        code_name = code_name or self.FALLBACK_CODE_NAME
        release_version = self._get_release_version(exec_path, code_name)

        plugin_folder_name = None
        for plugin_folder in self.ALIAS_PLUGINS:
            min_version = self.ALIAS_PLUGINS[plugin_folder].get("min_version")
            max_version = self.ALIAS_PLUGINS[plugin_folder].get("max_version")

            if min_version and version_cmp(release_version, min_version) < 0:
                continue

            if max_version and version_cmp(release_version, max_version) >= 0:
                continue

            plugin_folder_name = plugin_folder
            break

        if not plugin_folder_name:
            self.logger.error("Failed to find plugin folder.")
            return

        plugin_file_basename = (
            "shotgun" if version_cmp(release_version, "2022.2") < 0 else "shotgrid"
        )

        # Set plugins list file to the user TEMP directory
        plugin_temp_file_directory = os.environ["TEMP"]
        plugins_list_file = os.path.join(plugin_temp_file_directory, "plugins.lst")
        python_major_version = sys.version_info.major

        if python_major_version < 3:
            raise Exception(
                "Alias ShotGrid plugin does not support Python version {}.{}.{}".format(
                    sys.version_info.major,
                    sys.version_info.minor,
                    sys.version_info.micro,
                )
            )

        success = False
        with open(plugins_list_file, "w") as plf:
            plugin_file_path = os.path.join(
                plugins_directory,
                "python3",
                plugin_folder_name,
                "{}.plugin".format(plugin_file_basename),
            )
            # Overwrite the lst file with the plugin file path found
            plf.write("{}\n".format(plugin_file_path))
            success = True

        # returns plugins.lst path or None
        return plugins_list_file if success else None

    def _clean_args(self, args):
        if args:
            args = re.sub(" +", " ", args).strip()

        return args

    def _get_release_version(self, exec_path, code_name):
        alias_bindir = os.path.dirname(exec_path)
        about_box_file = os.path.join(
            os.path.dirname(alias_bindir), "resources", "AboutBox.txt"
        )

        with open(about_box_file, "r") as f:
            about_box_file_first_line = f.readline().split("\r")[0].strip()

        release_prefix = "Alias " + code_name
        releases = about_box_file_first_line.strip().split(",")
        release_info = [
            item.strip() for item in releases if item.strip().startswith(release_prefix)
        ][0]
        release_version = release_info[len(release_prefix) :].strip()

        return release_version


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

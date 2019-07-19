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
        "Design": dict(flags="-a ds", icon="icon_ds_256.png"),
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

        # Add flags according to the code_name
        tk_alias_codename = None
        for code_name, data in self.CODE_NAMES.items():
            if code_name in exec_path and data.get("flags"):
                args += data.get("flags")
                tk_alias_codename = code_name
                break

        # Flag -P (plugins list file)
        plugins_list_file = self._get_plugins_list_file()
        if plugins_list_file:
            args += " -P {0}".format(plugins_list_file)

        # Make the engine startup module to be available when Alias starts up
        # by appending it to the env PYTHONPATH.
        startup_path = os.path.join(self.disk_location, "startup")
        sgtk.util.append_path_to_env_var("PYTHONPATH", startup_path)

        # Add site packages to PYTHONPATH
        site_packages = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages")
        if os.path.exists(site_packages):
            sgtk.util.append_path_to_env_var("PYTHONPATH", site_packages)

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
        required_env["TK_ALIAS_CODENAME"] = tk_alias_codename.lower()

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
                    "SoftwareVersion %s is not supported: %s" %
                    (sw_version, reason)
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
                executable_template,
                self.COMPONENT_REGEX_LOOKUP
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
                        self._icon_from_executable(code_name)
                    )
                )

        return sw_versions

    def _get_plugins_list_file(self):
        """
        Generates plugins.lst file used by alias in the plugins bootstrap process

        :return: plugins.lst path
        """
        # get plugins folder
        plugins_directory = os.path.join(self.disk_location, "plugins")
        plugins_list_file = os.path.join(plugins_directory, "plugins.lst")
        plugins_number = 0

        # plugins folder exists?
        if not os.path.isdir(plugins_directory):
            return None

        # creates plugins.lst file in disk
        with open(plugins_list_file, "w") as plf:
            # loops plugins folder searching for *.plugin files
            for plugin_file_name in os.listdir(plugins_directory):
                if not plugin_file_name.endswith(".plugin"):
                    continue

                # build *.plugin file path
                plugin_file_path = os.path.join(plugins_directory, plugin_file_name)

                # appends found *.plugin file path in plugins.lst file
                plf.write("{0}\n".format(plugin_file_path))
                plugins_number += 1

        # returns plugins.lst path or None
        return plugins_list_file if plugins_number else None

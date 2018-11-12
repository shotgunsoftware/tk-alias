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
    Handles launching Alias executables. Automatically starts up
    a tk-alias engine with the current context in the new session
    of Alias.
    """

    # Named regex strings to insert into the executable template paths when
    # matching against supplied versions and products. Similar to the glob
    # strings, these allow us to alter the regex matching for any of the
    # variable components of the path in one place
    COMPONENT_REGEX_LOOKUP = {
        "version": "[\d.]+",
        "product": "(?:AutoStudio|Surface|Design)",
    }

    # This dictionary defines a list of executable template strings for each
    # of the supported operating systems. The templates are used for both
    # globbing and regex matches by replacing the named format placeholders
    # with an appropriate glob or regex string. As Side FX adds modifies the
    # install path on a given OS for a new release, a new template will need
    # to be added here.
    EXECUTABLE_TEMPLATES = {
        "win32": [
            # C:/Program Files/Autodesk/AliasSurface2019/bin/Alias.exe
            "C:/Program Files/Autodesk/Alias{product}{version}/bin/Alias.exe",
        ]
    }

    @property
    def minimum_supported_version(self):
        """
        The minimum software version that is supported by the launcher.
        """
        return "2019"

    def prepare_launch(self, exec_path, args, file_to_open=None):
        """
        Prepares an environment to launch Alias in that will automatically
        load Toolkit and the tk-alias engine when Alias starts.

        :param str exec_path: Path to Alias executable to launch.
        :param str args: Command line arguments as strings.
        :param str file_to_open: (optional) Full path name of a file to open on launch.
        :returns: :class:`LaunchInformation` instance
        """
        # find the bootstrap script and import it.
        # note: all the business logic for how to launch is
        #       located in the python/startup folder to be compatible
        #       with older versions of the launch workflow
        extra_args = {}
        if 'AutoStudio' in exec_path:
            extra_args['codename'] = 'autostudio'
            args += '-a as'
        elif 'Surface' in exec_path:
            extra_args['codename'] = 'surface'
            args += '-a ss'
        elif 'Design' in exec_path:
            extra_args['codename'] = 'design'
            args += '-a ds'
        bootstrap_python_path = os.path.join(self.disk_location, "python", "startup")
        sys.path.insert(0, bootstrap_python_path)
        import alias_bootstrap

        # determine all environment variables
        required_env = alias_bootstrap.compute_environment(extra_args, self.engine_name,
                                                           sgtk.context.serialize(self.context),
                                                           file_to_open)
        # copy the extension across to the deploy folder
        args = alias_bootstrap.compute_args(args)

        # Add std context and site info to the env
        std_env = self.get_standard_plugin_environment()
        required_env.update(std_env)

        return LaunchInformation(exec_path, args, required_env)

    ##########################################################################################
    # private methods

    def _icon_from_executable(self, product):
        """
        Find the application icon based on the executable path and
        current platform.

        :param product: product.

        :returns: Full path to application icon as a string or None.
        """

        # the engine icon in case we need to use it as a fallback
        icon_name = "icon_256.png"
        if product == 'AutoStudio':
            icon_name = "icon_as_256.png"
        elif product == 'Surface':
            icon_name = "icon_ss_256.png"
        elif product == 'Design':
            icon_name = "icon_ds_256.png"
        engine_icon = os.path.join(self.disk_location, icon_name)
        if not os.path.exists(engine_icon):
            engine_icon = os.path.join(self.disk_location, "icon_256.png")
        return engine_icon

    def scan_software(self):
        """
        Scan the filesystem for alias executables.

        :return: A list of :class:`SoftwareVersion` objects.
        """

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
                executable_version = key_dict.get('version')

                sw_versions.append(
                    SoftwareVersion(
                        executable_version,
                        "Alias {0}".format(key_dict.get("product")),
                        executable_path,
                        self._icon_from_executable(key_dict.get('product'))
                    )
                )

        return sw_versions
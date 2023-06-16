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

    # The name used to establish the ShotGrid Alias Engine client with Alias
    TK_ALIAS_CLIENT_NAME = "shotgrid"

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

        self.logger.debug("Preparing Alias Launch...")

        # import sys
        # sys.path.append("C:\\python_libs")
        # import ptvsd
        # ptvsd.enable_attach()
        # ptvsd.wait_for_attach()

        try:
            # The alias framework is required to launch Alias with the correct plugin
            framework_location = self.__get_framework_location("tk-framework-alias")
            if framework_location is None:
                raise Exception("tk-framework-alias not found")

            code_name = self._get_code_name(exec_path)
            release_version = self._get_release_version(exec_path, code_name)

            # Ensure the plugin is ready to be launched with Alias. This will install the
            # Toolkit plugin com.sg.basic.alias that will bootstrap the engine once the Alias
            # plugin is loaded. It will also ensure the necessary Python version is available.
            plugin_file_path, plugin_env = self.__ensure_plugin_ready(
                framework_location, release_version, exec_path
            )

            # Set up the environment variables required for Alias Plugin to load and launch the
            # ShotGrid Alias Engine
            #
            # Append executable folder to PATH environment variable
            server_python_exe = plugin_env.get("ALIAS_PLUGIN_SERVER_PYTHON")
            if server_python_exe:
                sgtk.util.append_path_to_env_var(
                    "PATH", os.path.dirname(server_python_exe)
                )
            else:
                sgtk.util.append_path_to_env_var(
                    "PATH", os.path.dirname(sys.executable)
                )
                # We're going to append all of this Python process's sys.path to the
                # PYTHONPATH environment variable. This will ensure that we have access
                # to all libraries available in this process. We're appending instead of
                # setting because we don't want to stomp on any PYTHONPATH that might already
                # exist that we want to persist
                sgtk.util.append_path_to_env_var(
                    "PYTHONPATH", os.pathsep.join(sys.path)
                )

            # Make the 'start_engine' function available to the Alias Plugin
            startup_path = os.path.join(self.disk_location, "startup")
            sgtk.util.append_path_to_env_var("PYTHONPATH", startup_path)

            # Make the framework python available to the Alias Plugin
            framework_python_path = os.path.join(framework_location, "python")
            sgtk.util.append_path_to_env_var("PYTHONPATH", framework_python_path)

            # Set up required environment variables to pass to launch
            required_env = {}
            required_env.update(plugin_env)
            required_env["PYTHONPATH"] = os.environ["PYTHONPATH"]

            # Prepare the launch environment with variables required by the
            # classic bootstrap approach.
            required_env["SGTK_ENGINE"] = self.engine_name
            required_env["SGTK_CONTEXT"] = sgtk.context.serialize(self.context)

            # Add Alias specific env vars
            required_env["TK_ALIAS_VERSION"] = release_version
            required_env["TK_ALIAS_EXECPATH"] = exec_path
            required_env["TK_ALIAS_CODENAME"] = code_name.lower()

            # Add the file name to open to the launch environment
            if file_to_open:
                required_env["SGTK_FILE_TO_OPEN"] = file_to_open

            # Get the launch app path and args
            app_path, app_args = self.__prepare_launch_args(
                args, code_name, plugin_file_path, exec_path, server_python_exe
            )
            return LaunchInformation(app_path, app_args, required_env)

        except Exception as prepare_launch_error:
            error_msg = (
                f"Error preparing launch for {self.engine_name}: {prepare_launch_error}"
            )
            raise Exception(error_msg)

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

    ##########################################################################################
    # protected methods

    def _icon_from_executable(self, code_name):
        """
        Find the application icon based on the code_name.

        :param code_name: Product code_name (AutoStudio, Design, ...).

        :return: Full path to application icon as a string or None.
        """
        if code_name in self.CODE_NAMES:
            icon_name = self.CODE_NAMES.get(code_name).get("icon")
            path = os.path.join(self.disk_location, "icons", icon_name)
        else:
            path = os.path.join(self.disk_location, "icon_256.png")

        return path

    def _find_software(self):
        """Find executables in the default install locations."""

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

    def _clean_args(self, args):
        """Format and sanitize the command line args."""

        if args:
            args = re.sub(" +", " ", args).strip()

        return args

    def _get_code_name(self, exec_path):
        """Return the Alias code name given the executable path and launch arguments."""

        for code_name in self.CODE_NAMES:
            if code_name in exec_path:
                return code_name
        return self.FALLBACK_CODE_NAME

    def _get_release_version(self, exec_path, code_name):
        """
        Return the Alias version for the given executable path and code name.

        :return: The Alias version string.
        :rtype: str
        """

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

        # Strip out any text that comes after the version number string (e.g. Preview)
        release_version = release_version.split(" ")[0]

        return release_version

    ##########################################################################################
    # private methods

    def __prepare_launch_args(
        self, args, code_name, plugin_file_path, alias_exe, python_exe=None
    ):
        """
        Prepare the command line arguments to launch Alias.

        In some cases, Alias must be launched with a specifc version of Python to ensure that
        the Alias Plugin embeds the specific Python version. To do so, the command to launch
        Alias is wrapped to be launched via Python, using the specific version of Python.

        :parm args: The raw command line arguments (as a string) passed to launch Alias.
        :type args: str
        :parm code_name: The Alias code name.
        :type code_name: str
        :parm plugin_file_path: The file path to the .lst file used to auto load plugins.
        :type plugin_file_path: str
        :param alias_exe: The file path to the Alias executable.
        :type alias_exe: str
        :param python_exe: (Optional) file path to a python executable to launch Alias
        :type python_exe: str

        :return: A tuple containing the application to launch and the command line arguments.
        :rtype: tuple
        """

        # First clean the args
        app_args = self._clean_args(args)

        # Add the Alis code name to the args
        code_name_data = self.CODE_NAMES[code_name]
        code_name_flags = self._clean_args(code_name_data.get("flags"))
        if code_name_flags not in args:
            app_args += " " + code_name_flags

        if python_exe is None:
            # Launching Alias application directly - add the plugin file path to the Alias cmd
            # line args to auto-load the plugin.
            app_args += ' -P "{0}'.format(plugin_file_path)
            app_args += '"'
            app_path = alias_exe
        else:
            # Launching Alias indirectly to ensure the Alias Plugin uses a specific Python
            # version - wrap the command line to launch Alias with the given python executable
            app_args += f' -P \\"{plugin_file_path}\\"'
            python_args = f'import os;os.system(r\'start /B \\"App\\" \\"{alias_exe}\\" {app_args}\')'
            app_args = f'-c "{python_args}"'
            app_path = python_exe

        return app_path, app_args

    def __get_framework_location(self, framework_name):
        """
        Return the file path to the framework bundle.

        :param framework_name: The name of the framework.
        :type framework_name: str

        :return: The file path to the framework bundle.
        :rtype: str
        """

        framework_and_version = None
        for framework in self.descriptor.get_required_frameworks():
            if framework.get("name") == framework_name:
                name_parts = [framework["name"]]
                if "version" in framework:
                    name_parts.append(framework["version"])
                framework_and_version = "_".join(name_parts)
                break
        else:
            self.logger.error(f"Failed to find location for framework {framework_name}")
            return

        # First get the environment object from the current engine and config
        engine = sgtk.platform.current_engine()
        env_name = engine.environment.get("name")
        env = engine.sgtk.pipeline_configuration.get_environment(env_name)

        # Get the framework descriptor from the environment object
        self.logger.debug(
            f"Getting framework descriptor {framework_name} from '{framework}'"
        )
        framework_desc = env.get_framework_descriptor(framework_and_version)

        self.logger.debug(f"Found framework descriptor {framework_desc}")
        return framework_desc.get_path()

    def __ensure_plugin_ready(self, framework_location, alias_version, alias_exec_path):
        """
        Ensure that the plugin is installed and ready to be launched.

        This method will ensure the plugin is installed and will return the plugin file path
        that can be used to launch the plugin with Alias on startup, and the required
        environment variables to successfully start the plugin.

        :param framework_location: The file path to the framework on local disk.
        :type framework_location: str
        :param alias_version: The Alias version required for the plugin.
        :type alias_version: str
        :param alias_exec_path: The file path to the Alias application executable.
        :type alias_exec_path: str
        :param client_name: The name for this Alias ShotGrid client application.
        :type client_name: str
        :param client_exe: The file path to the python script to bootstrap the Shotgrid
            client application.
        :type client_exe: str

        :return: A tuple containing plugin info required to launch the plugin: (1) the file
            path to the alias framework module, (2) the alias plugin file path, (3) the plugin
            environment variables.
        :rtype: tuple[str,str,dict]
        """

        # Get the framework startup utils
        bootstrap_python_path = os.path.join(framework_location, "python")
        sys.path.insert(0, bootstrap_python_path)
        import tk_framework_alias_utils.startup as startup_utils

        sys.path.remove(bootstrap_python_path)

        # Get the pipeline config id
        engine = sgtk.platform.current_engine()
        pipeline_config_id = engine.sgtk.pipeline_configuration.get_shotgun_id()
        entity_type = self.context.project["type"]
        entity_id = self.context.project["id"]

        # Ensure the basic.alias plugin is installed and up to date
        return startup_utils.ensure_plugin_ready(
            alias_version,
            alias_exec_path,
            self.TK_ALIAS_CLIENT_NAME,
            pipeline_config_id,
            entity_type,
            entity_id,
            os.environ.get("TK_DEBUG", "0"),
            self.logger,
        )

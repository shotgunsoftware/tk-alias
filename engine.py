# Copyright (c) 2019 Shotgun Software Inc.
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
from sgtk.util import LocalFileStorageManager
import alias_api


class AliasEngine(sgtk.platform.Engine):
    """
    An Alias DC engine for Shotgun Toolkit.
    """

    def __init__(self, tk, context, engine_instance_name, env):
        """Initialize custom attributes."""
        # Custom attributes
        self._tk_alias = None
        self._qt_app = None
        self._plugin_is_ready = False
        self.alias_codename = None
        self.alias_execpath = None
        self.alias_bindir = None
        self._dialog_parent = None

        self._menu_generator = None
        self._contexts_by_stage_name = {}
        self._contexts_by_path = {}
        self._stop_watching = False

        if not hasattr(sys, "argv"):
            sys.argv = [""]

        super(AliasEngine, self).__init__(tk, context, engine_instance_name, env)

    @property
    def host_info(self):
        """
        Returns information about the application hosting this engine.

        :returns: A {"name": application name, "version": application version}
                  dictionary. eg: {"name": "AfterFX", "version": "2017.1.1"}
        """
        return dict(name="Alias", version="unknown")

    @property
    def context_change_allowed(self):
        """
        Specifies that context changes are allowed by the engine.
        """
        return True

    @staticmethod
    def get_current_engine():
        """
        Return the engine that Toolkit is currently running. This is used by the Alias
        C++ Plugin to ensure that its reference to the engine is not stale (e.g. the
        plugin's reference will become stale after the engine has been reloaded).
        """

        return sgtk.platform.current_engine()

    def post_context_change(self, old_context, new_context):
        """
        Runs after a context change has occurred.

        :param old_context: The previous context.
        :param new_context: The current context.
        """

        self.logger.debug("%s: Post context change...", self)

        # Rebuild the menu only if we change of context
        self._menu_generator.create_menu()
        self._menu_generator.refresh()

    def pre_app_init(self):
        """
        Sets up the engine into an operational state. This method called before
        any apps are loaded.
        """

        self.logger.debug("%s: Initializing..." % (self,))

        # unicode characters returned by the shotgun api need to be converted
        # to display correctly in all of the app windows
        # tell QT to interpret C strings as utf-8
        from sgtk.platform.qt import QtCore

        utf8 = QtCore.QTextCodec.codecForName("utf-8")
        QtCore.QTextCodec.setCodecForCStrings(utf8)
        self.logger.debug("set utf-8 codec for widget text")

        pyside_folder = os.path.dirname(QtCore.__file__)
        site_packages_folder = os.path.dirname(pyside_folder)
        lib_folder = os.path.dirname(site_packages_folder)
        python_folder = os.path.dirname(lib_folder)
        shotgun_create_folder = os.path.dirname(python_folder)
        qt_folder = os.path.join(shotgun_create_folder, "Qt")

        # PySide plugins
        plugins_dir = os.path.join(pyside_folder, "plugins")
        if os.path.exists(plugins_dir):
            QtCore.QCoreApplication.addLibraryPath(plugins_dir)

        # QT plugins
        plugins_dir = os.path.join(qt_folder, "plugins")
        if os.path.exists(plugins_dir):
            QtCore.QCoreApplication.addLibraryPath(plugins_dir)

        # Init QT main loop
        self.init_qt_app()

        # import python/tk_alias module
        self._tk_alias = self.import_module("tk_alias")

        # dialog parent handler
        self._dialog_parent = self._tk_alias.DialogParent(engine=self)

        # Env vars
        self.alias_execpath = os.getenv("TK_ALIAS_EXECPATH", None)
        self.alias_bindir = os.path.dirname(self.alias_execpath)
        self.alias_codename = os.getenv("TK_ALIAS_CODENAME", "autostudio")

        # Be sure the current version is supported
        alias_version = int(os.getenv("TK_ALIAS_VERSION", None))
        if not alias_version:
            self.logger.debug("Couldn't get Alias version. Skip version comparison")
            return

        if alias_version > self.get_setting("compatibility_dialog_min_version", 2021):
            from sgtk.platform.qt import QtGui

            msg = (
                "The Shotgun Pipeline Toolkit has not yet been fully tested with Alias %d. "
                "You can continue to use the Toolkit but you may experience bugs or "
                "instability.  Please report any issues you see to %s"
                % (alias_version, sgtk.support_url)
            )
            self.logger.warning(msg)
            QtGui.QMessageBox.warning(
                self.get_parent_window(), "Warning - Shotgun Pipeline Toolkit!", msg,
            )

    def post_app_init(self):
        """
        Runs after all apps have been initialized.
        """
        self.logger.debug("%s: Post Initializing...", self)

        # init menu
        self._menu_generator = self._tk_alias.AliasMenuGenerator(engine=self)
        self._menu_generator.create_menu(clean_menu=False)

        self._run_app_instance_commands()

    def destroy_engine(self):
        """
        Called when the engine should tear down itself and all its apps.
        """
        self.logger.debug("%s: Destroying...", self)

        # Clean the menu
        self._menu_generator.clean_menu()

        # Close all Shotgun app dialogs that are still opened since
        # some apps do threads cleanup in their onClose event handler
        # Note that this function is called when the engine is restarted (through "Reload Engine and Apps")

        # Important: Copy the list of dialogs still opened since the call to close() will modify created_qt_dialogs
        dialogs_still_opened = self.created_qt_dialogs[:]

        for dialog in dialogs_still_opened:
            dialog.close()

    def init_qt_app(self):
        """
        Initialize QT application.
        """
        from sgtk.platform.qt import QtGui

        self.logger.debug("%s: Initializing QtApp", self)

        # Get current instance
        instance = QtGui.QApplication.instance()

        # Create instance
        if not instance:
            self._qt_app = QtGui.QApplication(sys.argv)
            self._qt_app.setQuitOnLastWindowClosed(False)
            self.logger.info("Created QApplication instance: {0}".format(self._qt_app))

            def _app_quit():
                QtGui.QApplication.processEvents()

            QtGui.QApplication.instance().aboutToQuit.connect(_app_quit)
        # Use current instance
        else:
            self._qt_app = instance

        # Make the QApplication use the dark theme. Must be called after the QApplication is instantiated
        self._initialize_dark_look_and_feel()

    def _get_dialog_parent(self):
        """
        Get Alias dialog parent
        """
        return self._dialog_parent.get_dialog_parent()

    def _run_app_instance_commands(self):
        """
        Runs the series of app instance commands listed in the 'run_at_startup' setting
        of the environment configuration yaml file.
        """

        # Build a dictionary mapping app instance names to dictionaries of commands they registered with the engine.
        app_instance_commands = {}
        for (command_name, value) in self.commands.items():
            app_instance = value["properties"].get("app")
            if app_instance:
                # Add entry 'command name: command function' to the command dictionary of this app instance.
                command_dict = app_instance_commands.setdefault(
                    app_instance.instance_name, {}
                )
                command_dict[command_name] = value["callback"]

        commands_to_run = []
        # Run the series of app instance commands listed in the 'run_at_startup' setting.
        for app_setting_dict in self.get_setting("run_at_startup", []):

            app_instance_name = app_setting_dict["app_instance"]
            # Menu name of the command to run or '' to run all commands of the given app instance.
            setting_command_name = app_setting_dict["name"]

            # Retrieve the command dictionary of the given app instance.
            command_dict = app_instance_commands.get(app_instance_name)

            if command_dict is None:
                self.logger.warning(
                    "%s configuration setting 'run_at_startup' requests app '%s' that is not installed.",
                    self.name,
                    app_instance_name,
                )
            else:
                if not setting_command_name:
                    # Run all commands of the given app instance.
                    for (command_name, command_function) in command_dict.items():
                        self.logger.debug(
                            "%s startup running app '%s' command '%s'.",
                            self.name,
                            app_instance_name,
                            command_name,
                        )
                        commands_to_run.append(command_function)
                else:
                    # Run the command whose name is listed in the 'run_at_startup' setting.
                    command_function = command_dict.get(setting_command_name)
                    if command_function:
                        self.logger.debug(
                            "%s startup running app '%s' command '%s'.",
                            self.name,
                            app_instance_name,
                            setting_command_name,
                        )
                        commands_to_run.append(command_function)
                    else:
                        known_commands = ", ".join(
                            "'%s'" % name for name in command_dict
                        )
                        self.logger.warning(
                            "%s configuration setting 'run_at_startup' requests app '%s' unknown command '%s'. "
                            "Known commands: %s",
                            self.name,
                            app_instance_name,
                            setting_command_name,
                            known_commands,
                        )

        # no commands to run. just bail
        if not commands_to_run:
            return

        # finally, run the commands
        for command in commands_to_run:
            command()

    def save_context_for_stage(self, context=None):
        """
        Save the context associated to the current Alias stage.
        We need to save and restore the context because of the different stages the user can use.
        As the Stages can change their name, we need to store the context for both the stage name and the stage path.

        :param context:  We can specify a context to associate to the current stage. If no one is supplied, we will use
                         the current one.
        """

        if not context:
            context = self.context

        current_stage = alias_api.get_current_stage()
        if current_stage.path:
            self._contexts_by_path[current_stage.path] = context
        self._contexts_by_stage_name[current_stage.name] = context

    #####################################################################################
    # Alias Callbacks

    def on_plugin_init(self):
        """
        A callback happening when the Alias Shotgun plugin is initialized. It happens once and only once when Alias
        starts.
        """

        path = os.environ.get("SGTK_FILE_TO_OPEN", None)
        if path:
            alias_api.open_file(path)

    def on_stage_selected(self):
        """
        A callback happening when an Alias stage is selected.
        """

        current_stage = alias_api.get_current_stage()

        # sometimes, we need to stop switching the context on stage selection as some Alias operations need to change
        # current stage but this action must not affect Shotgun Context switch behaviour
        if self._stop_watching:
            return

        if not current_stage:
            return
        if not current_stage.name and not current_stage.path:
            return

        # try to get the context from the file path
        if current_stage.path and current_stage.path in self._contexts_by_path:
            self.change_context(self._contexts_by_path[current_stage.path])
        # otherwise, try to get the context from the stage name
        elif current_stage.name and current_stage.name in self._contexts_by_stage_name:
            self.change_context(self._contexts_by_stage_name[current_stage.name])
        # finally, use the project context as the default one
        else:
            project_context = self.sgtk.context_from_entity_dictionary(
                self.context.project
            )
            self.change_context(project_context)

    #####################################################################################
    # QT Utils

    @staticmethod
    def get_parent_window():
        """
        Return current active window as parent
        """
        from sgtk.platform.qt import QtGui

        return QtGui.QApplication.activeWindow()

    def open_save_as_dialog(self):
        """
        Launch a Qt file browser to select a file, then save the supplied
        project to that path.
        """

        from sgtk.platform.qt import QtGui

        # Alias doesn't appear to have a "save as" dialog accessible via
        # python. so open our own Qt file dialog.
        file_dialog = QtGui.QFileDialog(
            parent=self.get_parent_window(),
            caption="Save As",
            directory=os.path.expanduser("~"),
            filter="Alias file (*.wire)",
        )
        file_dialog.setLabelText(QtGui.QFileDialog.Accept, "Save")
        file_dialog.setLabelText(QtGui.QFileDialog.Reject, "Cancel")
        file_dialog.setOption(QtGui.QFileDialog.DontResolveSymlinks)
        file_dialog.setOption(QtGui.QFileDialog.DontUseNativeDialog)
        if not file_dialog.exec_():
            return
        path = file_dialog.selectedFiles()[0]

        if os.path.splitext(path)[-1] != ".wire":
            path = "{0}.wire".format(path)

        if path:
            alias_api.save_file_as(path)

    def open_delete_stages_dialog(self, new_file=False):
        """
        Launch a QT prompt dialog to ask the user if he wants to delete all the existing stages or keep them when
        opening a new file.
        """

        from sgtk.platform.qt import QtGui

        if new_file:
            message = "DELETE all objects, shaders, views and actions in all existing Stage before Opening a New File?"
        else:
            message = "DELETE all objects, shaders, views and actions in all existing Stage before Opening this File?"
        message_type = (
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
        )
        answer = QtGui.QMessageBox.question(
            self.get_parent_window(), "Open", message, message_type
        )

        return answer

    #####################################################################################
    # Logging

    def _emit_log_message(self, handler, record):
        """
        Called by the engine to log messages in Alias Terminal.
        All log messages from the toolkit logging namespace will be passed to this method.

        :param handler: Log handler that this message was dispatched from.
                        Its default format is "[levelname basename] message".
        :type handler: :class:`~python.logging.LogHandler`
        :param record: Standard python logging record.
        :type record: :class:`~python.logging.LogRecord`
        """
        # TODO: improve Alias API to redirect the logs to the Alias Promptline
        pass

    #####################################################################################
    # Utils

    def get_tk_from_project_id(self, project_id):
        """
        Get the tank instance given the project ID. This is useful when you have to deal with files from library project

        :param project_id: Id of the project you want to get the tank instance for
        :return: An instance of :class`sgtk.Sgtk`
        """

        # first of all, we need to determine if the file we're trying to import lives in the current project or in
        # another one
        in_current_project = project_id == self.context.project["id"]

        if in_current_project:
            return self.sgtk

        # if the file we're trying to import lives in another project, we need to access the configuration used by this
        # project in order to get the right configuration settings
        else:

            pc_local_path = self.__get_pipeline_configuration_local_path(project_id)
            if not pc_local_path:
                self.logger.warning(
                    "Couldn't get tank instance for project {}.".format(project_id)
                )
                return None

            return sgtk.sgtk_from_path(pc_local_path)

    def get_reference_template(self, tk, sg_data):
        """
        Get the reference_template according to the given context

        :param tk: Instance of :class`sgtk.Sgtk` for the project we want to get the reference template from
        :param sg_data: Dictionary of Shotgun data containing some context information. This dictionary must contain
                        the 'task' field
        :return: The reference template object
        """

        if "task" not in sg_data.keys():
            self.logger.error("Couldn't find 'task' key in sg_data dictionary")
            return

        ctx = tk.context_from_entity_dictionary(sg_data["task"])

        if not ctx:
            self.logger.error("Couldn't find context from data: {}".format(sg_data))
            return

        env = sgtk.platform.engine.get_environment_from_context(tk, ctx)
        if not env:
            self.logger.error("Couldn't get environment from context")
            return

        engine_settings = env.get_engine_settings(self.name)
        if not engine_settings:
            self.logger.error("Couldn't get engine settings")
            return

        reference_template_name = engine_settings.get("reference_template")
        if not reference_template_name:
            self.logger.error("Couldn't get reference template from settings")
            return

        return tk.templates.get(reference_template_name)

    def __get_pipeline_configuration_local_path(self, project_id):
        """
        Get the path to the local configuration (the one which stands in the Sgtk cache folder) in order to be able
        to build a :class`sgtk.Sgtk` instance from this path

        :param project_id: Id of the project we want to retrieve the config for
        :returns: The local path to the config if we could determine which config to use, None otherwise.
        """

        plugin_id = "basic.desktop"

        # first, start the toolkit manager to get all the pipeline configurations related to the distant project
        # here, we are going to use the default plugin id "basic.*" to find the pipeline configurations
        mgr = sgtk.bootstrap.ToolkitManager()
        mgr.plugin_id = sgtk.commands.constants.DEFAULT_PLUGIN_ID
        pipeline_configurations = mgr.get_pipeline_configurations(
            {"type": "Project", "id": project_id}
        )

        if not pipeline_configurations:
            self.logger.warning(
                "Couldn't retrieve any pipeline configuration linked to project {}".format(
                    project_id
                )
            )
            return

        if len(pipeline_configurations) == 1:
            pipeline_config = pipeline_configurations[0]

        else:

            # try to determine which configuration we want to use:
            # 1- if one and only one pipeline configuration is restricted to this project, use it
            # 2- if one pipeline configuration is named Primary and linked to this project, use it
            # 3- reject all the other cases

            pipeline_config = self.__get_project_pipeline_configuration(
                pipeline_configurations, project_id
            )

            if not pipeline_config:
                pipeline_config = self.__get_primary_pipeline_configuration(
                    pipeline_configurations, project_id
                )

        if not pipeline_config:
            self.logger.warning(
                "Couldn't get the pipeline configuration linked to project {}: too many configurations".format(
                    project_id
                )
            )
            return None

        config_local_path = LocalFileStorageManager.get_configuration_root(
            self.sgtk.shotgun_url,
            project_id,
            plugin_id,
            pipeline_config["id"],
            LocalFileStorageManager.CACHE,
        )

        return os.path.join(config_local_path, "cfg")

    def __get_project_pipeline_configuration(self, pipeline_configurations, project_id):
        """
        Parse the pipeline configuration list in order to find if one of them is only used by this project.

        :param pipeline_configurations: List of pipeline configurations to parse
        :param project_id:              Id of the project we want to get the pipeline configuration for
        :returns: The pipeline configuration if only one config has been defined for this project, None otherwise.
        """

        pipeline_configuration = None

        for pc in pipeline_configurations:
            if not pc["project"]:
                continue
            if pc["project"]["id"] == project_id:
                if pipeline_configuration:
                    return None
                pipeline_configuration = pc

        return pipeline_configuration

    def __get_primary_pipeline_configuration(self, pipeline_configurations, project_id):
        """
        Parse the pipeline configuration list in order to find if one of them has been defined as "Primary" for this
        project.

        :param pipeline_configurations: List of pipeline configurations to parse
        :param project_id:              Id of the project we want to get the pipeline configuration for
        :returns: The pipeline configuration if a "Primary" config has been found for this project, None otherwise.
        """

        for pc in pipeline_configurations:
            if (
                pc["project_id"] == project_id
                and pc["name"] == sgtk.commands.constants.PRIMARY_PIPELINE_CONFIG_NAME
            ):
                return pc

        return None

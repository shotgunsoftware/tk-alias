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


class AliasEngine(sgtk.platform.Engine):
    """
    An Alias DCC engine for Shotgun Toolkit.
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
        self.alias_version = None
        self._dialog_parent = None
        self.__event_watcher = None
        self.__data_validator = None

        self._menu_generator = None
        self._contexts_by_stage_name = {}
        self._contexts_by_path = {}

        if not hasattr(sys, "argv"):
            sys.argv = [""]

        super(AliasEngine, self).__init__(tk, context, engine_instance_name, env)

    # -------------------------------------------------------------------------------------------------------
    # Static methods
    # -------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_current_engine():
        """
        Return the engine that Toolkit is currently running. This is used by the Alias
        C++ Plugin to ensure that its reference to the engine is not stale (e.g. the
        plugin's reference will become stale after the engine has been reloaded).
        """

        return sgtk.platform.current_engine()

    @staticmethod
    def get_parent_window():
        """
        Return the current active window Qt window.

        This is a fallback method to get the main window, if `_get_dialog_parent` cannot be used.
        """
        from sgtk.platform.qt import QtGui

        return QtGui.QApplication.activeWindow()

    # -------------------------------------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------------------------------------

    @property
    def host_info(self):
        """
        Returns information about the application hosting this engine.

        :returns: A {"name": application name, "version": application version}
                  dictionary. eg: {"name": "AfterFX", "version": "2017.1.1"}
        """
        return dict(name="Alias", version="unknown")

    @property
    def has_ui(self):
        """
        Detect and return if Alias is running in interactive/non-interactive mode
        """
        if os.path.basename(sys.executable) == "Alias.exe":
            return True
        else:
            return False

    @property
    def context_change_allowed(self):
        """
        Specifies that context changes are allowed by the engine.
        """
        return True

    @property
    def event_watcher(self):
        """Get the AliasEventWatcher object to help manager Alias message events and Python callbacks."""
        return self.__event_watcher

    @property
    def data_validator(self):
        """Get the AliasDataValidator object to help validate the Alias data."""
        return self.__data_validator

    # -------------------------------------------------------------------------------------------------------
    # Override base Engine class methods
    # -------------------------------------------------------------------------------------------------------

    def pre_app_init(self):
        """
        Sets up the engine into an operational state. Executed by the system and typically
        implemented by deriving classes. This method called before any apps are loaded.
        """

        self.logger.debug("%s: Initializing..." % (self,))

        from sgtk.platform.qt import QtCore, QtGui

        # unicode characters returned by the shotgun api need to be converted
        # to display correctly in all of the app windows
        # tell QT to interpret C strings as utf-8
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
        if self.has_ui:
            self._init_qt_app()

        # Defer importing the Alias Python API until now so that a proper info message can be displayed to
        # user if the api failed to import.
        # NOTE: Ensure this check runs after the Qt app is created and before attempting to import the
        # alias_api module, which means any engine functions that requires the alias_api module should import
        # the module at the function declaration. TODO: move all alias_api functionality outside the engine
        # and to its own module.
        try:
            import alias_api
        except Exception as api_import_error:
            error_msg = str(api_import_error)
            self.logger.critical(error_msg)
            if self.has_ui:
                QtGui.QMessageBox.critical(
                    self.get_parent_window(),
                    "Failed to import the Alias Python API",
                    error_msg,
                )

        # import python/tk_alias module
        self._tk_alias = self.import_module("tk_alias")

        # dialog parent handler
        self._dialog_parent = (
            self._tk_alias.DialogParent(engine=self) if self.has_ui else None
        )

        # event watcher
        self.__event_watcher = self._init_alias_event_watcher()

        # data validator
        self.__data_validator = self._tk_alias.AliasDataValidator()

        # Env vars
        self.alias_execpath = os.getenv("TK_ALIAS_EXECPATH", None)
        self.alias_bindir = os.path.dirname(self.alias_execpath)
        self.alias_codename = os.getenv("TK_ALIAS_CODENAME", "autostudio")

        # Be sure the current version is supported
        self.alias_version = os.getenv("TK_ALIAS_VERSION", None)
        if not self.alias_version:
            self.logger.debug("Couldn't get Alias version. Skip version comparison")
            return

        if int(self.alias_version[0:4]) > self.get_setting(
            "compatibility_dialog_min_version", 2021
        ):
            msg = (
                "The ShotGrid Pipeline Toolkit has not yet been fully tested with Alias %s. "
                "You can continue to use the Toolkit but you may experience bugs or "
                "instability.  Please report any issues you see to %s"
                % (self.alias_version, sgtk.support_url)
            )
            self.logger.warning(msg)
            if self.has_ui:
                QtGui.QMessageBox.warning(
                    self.get_parent_window(),
                    "Warning - ShotGrid Pipeline Toolkit!",
                    msg,
                )
        elif int(self.alias_version[0:4]) < 2021 and self.get_setting(
            "compatibility_dialog_old_version"
        ):
            msg = (
                "The ShotGrid Pipeline Toolkit is not fully capable with Alias %s. "
                "You should consider upgrading to a more recent version of Alias. "
                "Please report any issues you see to %s"
                % (self.alias_version, sgtk.support_url)
            )
            self.logger.warning(msg)
            if self.has_ui:
                QtGui.QMessageBox.warning(
                    self.get_parent_window(),
                    "Warning - ShotGrid Pipeline Toolkit!",
                    msg,
                )

    def post_app_init(self):
        """
        Executed by the system and typically implemented by deriving classes.
        This method called after all apps have been loaded.
        """

        self.logger.debug("%s: Post Initializing...", self)

        # init menu
        if self.has_ui:
            self._menu_generator = self._tk_alias.AliasMenuGenerator(engine=self)
            self._menu_generator.create_menu(clean_menu=False)

        self._run_app_instance_commands()

    def destroy_engine(self):
        """
        Called when the engine should tear down itself and all its apps.
        """

        self.logger.debug("%s: Destroying...", self)

        # Clean the menu
        if self.has_ui:
            self._menu_generator.clean_menu()

        self.event_watcher.shutdown()

        # Close all Shotgun app dialogs that are still opened since
        # some apps do threads cleanup in their onClose event handler
        # Note that this function is called when the engine is restarted (through "Reload Engine and Apps")

        # Important: Copy the list of dialogs still opened since the call to close() will modify created_qt_dialogs
        dialogs_still_opened = self.created_qt_dialogs[:]

        for dialog in dialogs_still_opened:
            dialog.close()

    def show_panel(self, panel_id, title, bundle, widget_class, *args, **kwargs):
        """
        Show a dialog as panel in Alias as they are not properly supported. In case the widget has already been opened,
        do not create a second widget but use the existing one instead.

        :param panel_id: Unique identifier for the panel, as obtained by register_panel().
        :param title: The title of the panel
        :param bundle: The app, engine or framework object that is associated with this window
        :param widget_class: The class of the UI to be constructed. This must derive from QWidget.

        Additional parameters specified will be passed through to the widget_class constructor.

        :returns: the created widget_class instance
        """

        self.logger.debug("Begin showing panel {}".format(panel_id))

        if not self.has_ui:
            self.logger.error(
                "Sorry, this environment does not support UI display! Cannot show "
                "the requested window '{}'.".format(title)
            )
            return None

        # try to find existing window in order to avoid having many instances of the same app opened at the same time
        for qt_dialog in self.created_qt_dialogs:
            if not hasattr(qt_dialog, "_widget"):
                continue
            if qt_dialog._widget.objectName() == panel_id:
                widget_instance = qt_dialog
                widget_instance.raise_()
                widget_instance.activateWindow()
                break
        # in case we can't find an existing widget, create a new one
        else:
            widget_instance = self.show_dialog(
                title, bundle, widget_class, *args, **kwargs
            )
            widget_instance.setObjectName(panel_id)

        return widget_instance

    def _get_dialog_parent(self):
        """
        Get Alias dialog parent window.
        """

        return self._dialog_parent.get_dialog_parent()

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

    # -------------------------------------------------------------------------------------------------------
    # Protected methods
    # -------------------------------------------------------------------------------------------------------

    def _init_qt_app(self):
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

    def _init_alias_event_watcher(self):
        """
        Initialize the Alis event watcher.

        Register any initial Alias message event callbacks, and start watching for events immediately.

        NOTE: registering callback for event AlMessageType.DagNameModified causes a crash on startup.
        This looks like a bug where Alias is not ready to handle events yet but we can register them.

        :return: The Alias event watcher object.
        :rtype: AliasEventWatcher
        """

        import alias_api

        event_watcher = self._tk_alias.AliasEventWatcher()

        # Register event callbacks
        # NOTE: cannot call engine class methods directly, must use lambda in order to have
        # access to the engine object to call its class methods. The event callbacks must
        # take one parameter, which is the result passed from the Alias Python API for the
        # Alias event
        event_watcher.register_alias_callback(
            lambda result, engine=self: engine.on_stage_active(result),
            alias_api.AlMessageType.StageActive,
        )

        # Now start watching the events. This should be called after registering events to
        # ensure the event watcher starts listening.
        event_watcher.start_watching()

        return event_watcher

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

    # -------------------------------------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------------------------------------

    def on_plugin_init(self):
        """
        This function is called by the Alias ShotGrid Plugin on initialization.

        This is called once, and only once when Alias starts up.
        """

        path = os.environ.get("SGTK_FILE_TO_OPEN", None)
        if path:
            self.open_file(path)

    def post_context_change(self, old_context, new_context):
        """
        Runs after a context change has occurred.

        :param old_context: The previous context.
        :param new_context: The current context.
        """

        self.logger.debug("%s: Post context change...", self)

        # Rebuild the menu only if we change of context and if we're running Alias in interactive mode
        if self.has_ui:
            self._menu_generator.create_menu()
            self._menu_generator.refresh()

    def save_context_for_stage(self, context=None):
        """
        Save the context associated to the current Alias stage.
        We need to save and restore the context because of the different stages the user can use.
        As the Stages can change their name, we need to store the context for both the stage name and the stage path.

        :param context:  We can specify a context to associate to the current stage. If no one is supplied, we will use
                         the current one.
        """

        import alias_api

        if not context:
            context = self.context

        current_stage = alias_api.get_current_stage()
        if not current_stage:
            return

        if current_stage.path:
            self._contexts_by_path[current_stage.path] = context
        self._contexts_by_stage_name[current_stage.name] = context

    #####################################################################################
    # File I/O

    def save_file(self):
        """
        Convenience function to call the Alias Python API to save the file and ensure
        the context is saved for the current stage.
        """

        import alias_api

        status = alias_api.save_file()
        if status != int(alias_api.AlStatusCode.Success):
            self.logger.error(
                "Alias Python API Error: save_file returned non-success status code {}".format(
                    status
                )
            )

        # Save context for the current stage that was updated
        self.save_context_for_stage()

    def save_file_as(self, path):
        """
        Convenience function to call the Alias Python API to save the file and ensure
        the context is saved for the current stage.

        :param path: the file path to save.
        :type path: str
        """

        import alias_api

        status = alias_api.save_file_as(path)
        if status != int(alias_api.AlStatusCode.Success):
            self.logger.error(
                "Alias Python API Error: save_file_as('{}') returned non-success status code {}".format(
                    path, status
                )
            )

        # Save context for the current stage that was updated
        self.save_context_for_stage()

    def open_file(self, path):
        """
        Convenience function to call the Alias Python API to open a file and ensure
        the context is saved for the current stage.

        :param path: the file path to open.
        :type path: str
        """

        import alias_api

        status = alias_api.open_file(path)
        if status != int(alias_api.AlStatusCode.Success):
            self.logger.error(
                "Alias Python API Error: open_file('{}') returned non-success status code {}".format(
                    path, status
                )
            )

        # Save context for the current stage that was updated
        self.save_context_for_stage()

    #####################################################################################
    # AliasEventWatcher callbacks

    def on_stage_active(self, result):
        """
        This is a callback that is triggered by Alias "StageCreated" events.

        Update the ShotGrid context according to the current stage (since it may have changed).

        :param result: The result of the Alias stage created event.
        :type result: alias_api.PythonCallbackMessageResult
        """

        import alias_api

        current_stage = alias_api.get_current_stage()

        # Do nothing if the current stage is invalid
        if not current_stage or (not current_stage.name and not current_stage.path):
            return

        # Do nothing if there are no SG contexts saved for Alias stages yet
        if not self._contexts_by_path and not self._contexts_by_stage_name:
            return

        # Attempt to get the saved SG context for the current Alias stage
        context = None
        if current_stage.path and current_stage.path in self._contexts_by_path:
            # Found the context form the stage path
            context = self._contexts_by_path[current_stage.path]
        elif current_stage.name and current_stage.name in self._contexts_by_stage_name:
            # Found the context form the stage name
            context = self._contexts_by_stage_name[current_stage.name]
        else:
            # Context not found, reset to the project context
            context = self.sgtk.context_from_entity_dictionary(self.context.project)

        # Only change the context if we found one and it is not the current context
        if context and context != self.context:
            self.change_context(context)

    #####################################################################################
    # QT Utils

    def open_save_as_dialog(self):
        """
        Try to open tk-multi-workfiles2 Save As... dialog if it exists otherwise
        launch a Qt file browser for the Save As...
        """
        open_dialog_func = None
        kwargs = {}
        workfiles = self.apps.get("tk-multi-workfiles2", None)

        if workfiles:
            if hasattr(workfiles, "show_file_save_dlg"):
                open_dialog_func = workfiles.show_file_save_dlg
                kwargs["use_modal_dialog"] = True

        if open_dialog_func:
            open_dialog_func(**kwargs)

        else:
            # Alias doesn't appear to have a "save as" dialog accessible via
            # python. so open our own Qt file dialog.

            from sgtk.platform.qt import QtGui

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
            self.save_file_as(path)

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
            try:
                if (
                    pc["project_id"] == project_id
                    and pc["name"]
                    == sgtk.commands.constants.PRIMARY_PIPELINE_CONFIG_NAME
                ):
                    return pc
            except KeyError:
                self.logger.warning("No project_id key for {}.".format(pc))
        return None

    # -------------------------------------------------------------------------------------------------------
    # Deprecated methods - to be removed in next major version v3.0.0
    # -------------------------------------------------------------------------------------------------------

    def execute_api_ops_and_defer_event_callbacks(self, alias_api_ops, event_types):
        """
        Marked as deprecated and to be removed in v3.0.0. Use AliasEventWatcher.ContextManager to handle
        triggering Python callbacks to ensure there is no conflict while performing Alias operations.

        Call an Alias API function while blocking any Alias event callbacks until the
        API function is done executing. Once finished, the registered Python callbacks
        will be triggered for the event types provided. Any event types not provided
        will not be triggered at all by the API function executed.
        NOTE since the callbacks are deferred to after the event operation has completed,
        we do not have access to the Alias callback return result that we normally get.
        TODO implement this deferred event handling in the Alias Python API side, for now
        we will just pass None for the message result to the Python callback function.
        Implementing the deferred event handling will also improve the way we currently
        ignore event callbacks by unregistering and re-registering events.
        :param alias_api_ops: The name of the main Alias API function to execute.
        :type alias_api_ops: list<AliasApiOp>, where AliasApiOp is of format:
            tuple<alias_api_func_name, func_args, func_keyword_args>
                alias_api_func: str
                obj: If None the alias_api_func is a function of the `alias_api` module.
                     If not None, the alias_api_func is a method of the `obj`.
                args: list
                kwargs: dict
        :param event_types: The Alias event types to defer callbacks until the main
                            operation is complete. Any event types that are not listed
                            will not be triggered at all for for this operation.
        :type event_types: list<AlMessageType>
        """

        import alias_api

        # Check that all api functions exist, if not abort
        for api_func, obj, _, _ in alias_api_ops:
            obj = obj or alias_api
            if not hasattr(obj, api_func):
                self.logger.error(
                    "Failed execute_api_ops_and_defer_event_callbcaks: Alias Python API function not found '{}.{}'".format(
                        obj, api_func
                    )
                )
                return

        if not isinstance(event_types, list):
            event_types = [event_types]

        if not self.event_watcher.is_watching:
            # If the event watcher is already paused, just execute the the operations normally.
            for api_func, obj, args, kwargs in alias_api_ops:
                obj = obj or alias_api
                getattr(obj, api_func)(*args, **kwargs)

        else:
            # Pause the event watcher
            self.event_watcher.stop_watching()

            # Execute all alias api operations in order
            for api_func, obj, args, kwargs in alias_api_ops:
                obj = obj or alias_api
                getattr(obj, api_func)(*args, **kwargs)

            # Enable the event watcher now that the operations have completed
            self.event_watcher.start_watching()

            # Now manually trigger the registered callbacks for the event types
            for event_type in event_types:
                callback_fns = self.event_watcher.get_callbacks(event_type)
                for callback_fn in callback_fns:
                    callback_fn(msg=None)

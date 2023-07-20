# Copyright (c) 2023 Autodesk Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk Inc.


import os
import sys
import pprint

import sgtk
from sgtk.util import LocalFileStorageManager


class AliasEngine(sgtk.platform.Engine):
    """Alias engine for ShotGrid Toolkit."""

    # The name of the hidden window, used to parent SG widgets to the Alias main window.
    __PROXY_WINDOW_TITLE = "sgtk dialog owner proxy"

    def __init__(self, tk, context, engine_instance_name, env):
        """Initialize the engine."""

        # Get all environment variables that the engine cares about
        self.alias_execpath = os.getenv("TK_ALIAS_EXECPATH", None)
        self.alias_bindir = os.path.dirname(self.alias_execpath)
        self.alias_codename = os.getenv("TK_ALIAS_CODENAME", "autostudio")
        self.alias_version = os.getenv("TK_ALIAS_VERSION", None)
        self.__hostname = os.getenv("SHOTGRID_ALIAS_HOST", None)
        self.__namespace = os.getenv("SHOTGRID_ALIAS_NAMESPACE", None)
        self.__port = os.getenv("SHOTGRID_ALIAS_PORT", None)
        if self.__port is not None:
            self.__port = int(self.__port)

        # The tk-alias python module
        self._tk_alias = None

        # Keep track of the ShotGrid context by stage name and path to allow context switching.
        self._contexts_by_stage_name = {}
        self._contexts_by_path = {}

        # The menu generator is responsible for adding the ShotGrid menu to the Alias window.
        self.__menu_generator = None

        # The event watcher manages handling Alias event callbacks.
        self.__event_watcher = None

        # The data validator provides the functionality for validating Alias data. This is
        # set up to be used by the Data Validation App.
        self.__data_validator = None

        # A socketio client used to communicate with Alias in OpenModel
        self.__sio = None
        # Information about the server that the socketio client is connected to.
        self.__server_info = {}
        # Information about the plugin that bootstrapped the engine
        self.__plugin_info = {}

        # This module will be initialized with the Alias Python API and utility functions on
        # calling '__init_api'
        self.__alias_py = None

        # Create a QWidget to parent all ShotGrid windows to. This widget will set its parent
        # as the Alias main window.
        self.__proxy_window = None

        # When running in the same process as Alias (for Alias versions <2024.0), the engine
        # will create the qt app instance.
        self.__qt_app = None

        if not hasattr(sys, "argv"):
            sys.argv = [""]

        # Flag inidicating if ShotGrid is running in the same process as Alias. This will
        # determine how ShotGrid will communicate with Alias.
        self.__in_alias_process = os.path.basename(sys.executable) == "Alias.exe"
        open_model = os.getenv("TK_ALIAS_OPEN_MODEL")
        if open_model is None:
            # For backward compatibility, OpenModel mode is when not executing in the same process
            # as Alias (unless )
            self.__is_open_model = not self.__in_alias_process
        else:
            self.__is_open_model = open_model in ("1", "true", "True")

        # Determine if the engine is running with a GUI or not
        if "TK_ALIAS_HAS_UI" in os.environ:
            # Found the environment variable to explicitly turn on/off GUI mode.
            self.__has_ui = os.environ.get("TK_ALIAS_HAS_UI", False) in (
                "1",
                "true",
                "True",
            )
        else:
            # Not explicitly defined to have a UI, we will say there is a UI if running in the
            # same process as Alias (for backward compatibility)
            self.__has_ui = self.__in_alias_process

        # Call the base engine init method
        super(AliasEngine, self).__init__(tk, context, engine_instance_name, env)

    # -------------------------------------------------------------------------------------------------------
    # Plugin version < 4.0.0 methods
    # -------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_current_engine():
        """
        Return the engine that Toolkit is currently running. This is used by the Alias
        C++ Plugin to ensure that its reference to the engine is not stale (e.g. the
        plugin's reference will become stale after the engine has been reloaded).
        """
        return sgtk.platform.current_engine()

    def on_plugin_init(self, plugin, alias, python):
        """
        Called on plugin initialization for shotgrid.plugin (plugin version <= 3) and for
        Alias version < 2024.0.
        """

        self.logger.info(
            f"Plugin initialized: v{plugin} Alias v{alias} Python v{python}"
        )
        self.__plugin_info = {
            "plugin_version": plugin,
            "alias_version": alias,
            "python_version": python,
        }

    # -------------------------------------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------------
    # Base Engine properties

    @property
    def host_info(self):
        """
        Returns information about the application hosting this engine.

        :returns: A {"name": application name, "version": application version}
                  dictionary. eg: {"name": "AfterFX", "version": "2017.1.1"}
        """
        return dict(name="Alias", version=self.plugin_info.get("alias_version"))

    @property
    def has_ui(self):
        """Return True if Alias is running in interactive mode (OpenAlias), otherwise False (for OpenModel)."""
        return self.__has_ui

    @property
    def context_change_allowed(self):
        """Specifies that context changes are allowed by the engine."""
        return True

    # -------------------------------------------------------------------------------------------------------
    # Alias Engine properties

    @property
    def plugin_info(self):
        """Get the information about the plugin the engine is running with."""
        return self.__plugin_info

    @property
    def in_alias_process(self):
        """Get whether or not the engine is running in the same process as Alias or not."""
        return self.__in_alias_process

    @property
    def alias_py(self):
        """
        Get the AliasPy object that can be used to communicate with Alias.

        Use the AliasPy.api property to access the Alias API and make requests. Use the other
        AliasPy properties for api helper methods.
        """
        return self.__alias_py

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

        # Import python/tk_alias module
        self._tk_alias = self.import_module("tk_alias")

        # Initialize the Alias Python API module (requires tk_alias module)
        self.__init_api(self.__hostname, self.__port, self.__namespace)

        if self.__sio:
            self.__server_info = self.__sio.call_threadsafe("server_info")
            self.__plugin_info = self.__server_info.get("client") or {}
            self.logger.debug(
                f"Alias server info: {pprint.pformat(self.__server_info)}"
            )
        else:
            # No server, we're in OpenModel mode.
            self.__server_info = {}

    def post_app_init(self):
        """This method called after all apps have been loaded."""

        from sgtk.platform.qt import QtGui

        # If qt is already running (e.g. on engine restart) do the post qt init now, otherwise
        # post_qt_init will be called in startup/bootstrap.py after engine created.
        instance = QtGui.QApplication.instance()
        if instance:
            self.post_qt_init()

    def post_context_change(self, old_context, new_context):
        """
        Runs after a context change has occurred.

        :param old_context: The previous context.
        :param new_context: The current context.
        """

        self.logger.debug("%s: Post context change...", self)

        # Rebuild the menu only if we change of context and if we're running Alias in interactive mode
        if self.has_ui:
            self.__menu_generator.build()

    def destroy_engine(self):
        """Called when the engine should tear down itself and all its apps."""

        self.logger.debug("%s: Destroying...", self)

        if self.__event_watcher:
            self.__event_watcher.shutdown()
            self.__event_watcher = None

        if self.__menu_generator:
            if not self.__sio or self.__sio.connected:
                self.__menu_generator.clean_menu()
            self.__menu_generator = None

        # Close all Shotgun app dialogs that are still opened since some apps do threads
        # cleanup in their onClose event handler
        # Note that this function is called when the engine is restarted (through "Reload
        # Engine and Apps")
        #
        # Important: Copy the list of dialogs still opened since the call to close() will modify created_qt_dialogs
        dialogs_still_opened = self.created_qt_dialogs[:]
        for dialog in dialogs_still_opened:
            dialog.close()

        if self.__sio:
            if self.__sio.connected:
                self.__sio.disconnect()
            self.__sio = None

        if self.__qt_app:
            self.__qt_app.quit()

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
            # Widgets application
            widget_instance = self.show_dialog(
                title, bundle, widget_class, *args, **kwargs
            )
            widget_instance.setObjectName(panel_id)

        return widget_instance

    def _get_dialog_parent(self):
        """Get Alias dialog parent window."""

        # No parent dialog if the engine is not running in GUI mode.
        if not self.has_ui:
            return None

        window = self.__get_or_create_proxy_window()
        if window:
            return window

        return super(AliasEngine, self)._get_dialog_parent()

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
    # Public methods
    # -------------------------------------------------------------------------------------------------------

    def restart_process(self):
        """
        Restart the process that the engine is running in.

        This is only applicable when the engine has a socketio client set up to communicate
        with Alias (e.g. OpenAlias mode).
        """

        if self.__menu_generator:
            self.__menu_generator.clean_menu()

        if self.__sio:
            self.__sio.emit_threadsafe("restart")
        else:
            raise NotImplementedError()

    def shutdown(self):
        """
        Shutdown the application running the engine.

        This method attempts to exit the Qt application runnign the engine, which will be
        responsible for ensuring that the engine is destroyed properly (e.g. calling destroy
        on the engine itself).
        """

        from sgtk.platform.qt import QtGui

        qt_app = QtGui.QApplication.instance() or self.__qt_app
        if qt_app:
            qt_app.quit()
        else:
            # Destroy the engine if there is no qt app
            self.destroy()

    def __init_qt_app(self):
        """
        Initialize the Qt Application.

        This should only be called when ShotGrid is running in the same process as Alias, and
        Alias does not create a Qt Application (for Alias < 2024.0).
        """

        from sgtk.platform.qt import QtCore, QtGui

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

        self.__qt_app = QtGui.QApplication.instance()
        if not self.__qt_app:
            self.__qt_app = QtGui.QApplication(["ShotGrid Alias Engine"])
            self.__qt_app.setQuitOnLastWindowClosed(False)

            def _app_quit():
                QtGui.QApplication.processEvents()

            self.__qt_app.aboutToQuit.connect(_app_quit)

    def post_qt_init(self):
        """
        Initialize the engine after Qt has been initialized and an app has been created.

        This is used by the startup/bootstrap.py to finish setting up the engine after the
        Qt app instance has been created, but before the event loop has started.
        """

        from sgtk.platform.qt import QtCore, QtGui

        instance = QtGui.QApplication.instance()
        if not instance:
            # Nothing to do if there is no QApplication running.
            self.logger.warning(
                "Attempted to initialize for Qt but Qt application instance not found."
            )
            self.__has_ui = False
            return

        # Ensure that the has ui flag has been set, though it should have been set on engine
        # creation to ensure it was initialized properly.
        self.__has_ui = True

        # Initialie the SG Toolkit style to the application.
        self._initialize_dark_look_and_feel()

        # unicode characters returned by the shotgun api need to be converted
        # to display correctly in all of the app windows
        # tell QT to interpret C strings as utf-8
        utf8 = QtCore.QTextCodec.codecForName("utf-8")
        QtCore.QTextCodec.setCodecForCStrings(utf8)
        self.logger.debug("set utf-8 codec for widget text")

        # Create the parent dialog for ShotGrid widgets
        self.__get_or_create_proxy_window()

        # Check that the Alias version is supported. Pop up a warning dialog if not.
        self.__check_version_support()

        # Initialize engine members that require Qt
        self.__menu_generator = self._tk_alias.menu_generation.AliasMenuGenerator(self)
        self.__data_validator = self._tk_alias.data_validator.AliasDataValidator(self)
        self.__event_watcher = self.__init_alias_event_watcher()

        # Build the ShotGrid menu in Alias. It will be added to the Alias main menu bar.
        self.__menu_generator.build()

        # Run the start up commands
        self.__run_app_instance_commands()

        # Check if there is a file set to open on startup
        path = os.environ.get("SGTK_FILE_TO_OPEN", None)
        if path:
            self.open_file(path)
            # clear the env var after loading so that it doesn't get reopened on an engine restart.
            del os.environ["SGTK_FILE_TO_OPEN"]

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

        current_stage = self.alias_py.get_current_stage()
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

        status = self.alias_py.save_file()
        if status != self.alias_py.AlStatusCode.Success.value:
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

        status = self.alias_py.save_file_as(path)
        if status != self.alias_py.AlStatusCode.Success.value:
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

        status = self.alias_py.open_file(path)
        if status != self.alias_py.AlStatusCode.Success.value:
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

        current_stage = self.alias_py.get_current_stage()

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

        workfiles = self.apps.get("tk-multi-workfiles2", None)
        if workfiles:
            if hasattr(workfiles, "show_file_save_dlg"):
                kwargs = {"use_modal_dialog": True}
                workfiles.show_file_save_dlg(**kwargs)
        else:
            # Alias doesn't appear to have a "save as" dialog accessible via
            # python. so open our own Qt file dialog.

            from sgtk.platform.qt import QtGui

            file_dialog = QtGui.QFileDialog(
                parent=self._get_dialog_parent(),
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
            self._get_dialog_parent(), "Open", message, message_type
        )

        return answer

    #####################################################################################
    # Utils

    def get_tk_from_project(self, project):
        """
        Get the tank instance given the project ID.

        This is useful when you have to deal with files from library project.

        This method performs the same operation as get_tk_from_project_id, except that it
        provides a fallback code path to ensure the pipeline configuration is loaded.

        :param project: The project you want to get the tank instance for.
        :type project: dict

        :return: An sgtk instance.
        :rtype: :class`sgtk.Sgtk`
        """

        project_id = project["id"]

        # first of all, we need to determine if the file we're trying to import lives in the current project or in
        # another one
        in_current_project = project_id == self.context.project["id"]

        if in_current_project:
            return self.sgtk

        # if the file we're trying to import lives in another project, we need to access the configuration used by this
        # project in order to get the right configuration settings
        else:
            pc_local_path = self.__get_pipeline_configuration_local_path(project)
            if not pc_local_path:
                self.logger.warning(
                    "Couldn't get tank instance for project {}.".format(project_id)
                )
                return None

            return sgtk.sgtk_from_path(pc_local_path)

    def get_tk_from_project_id(self, project_id):
        """
        Get the tank instance given the project ID.

        This is useful when you have to deal with files from library project.

        NOTE use get_tk_from_project for a more robust method to get the sgtk instance.

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

    # -------------------------------------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------------------------------------

    def __setup_sio(self, hostname, port, namespace):
        """
        Set up the socketio communication with Alias.

        Create a socketio client to connect to the running Alias server.

        :param hostname: The api server host name to connect to.
        :type hostname: str
        :param port: The api server port name to connect to.
        :type port: int
        :param namespace: The api server namespace to connect to.
        :type namespace: str

        :return: True if the socketio client was created and is connected to the server, False
            otherwise.
        :rtype: bool
        """

        # Create and connect to the server to communicate with Alias
        self.__sio = self._tk_alias.ShotGridAliasSocketIoClient(self, namespace)

        if not self.__sio:
            raise Exception("Failed to create socketio client")

        # Connect to the server to start communicating
        self.__sio.start(hostname, port)

        # Return the connection status
        return self.__sio.connected

    def __init_api(self, hostname=None, port=None, namespace=None, force=False):
        """
        Initialize the Alias Python api module to allow communication with Alias.

        The api can be initialized for either OpenAlias (GUI) or OpenModel (headless/batch)
        mode.

        For OpenAlias, the hostname, port and namespace arguments must be provided. These are
        required to connect to the running instance of Alias via a socketio server, which will
        provide the Alias API access.

        For OpenModel, none of the arguments are needed. Instead of connecting to a server to
        access the Alias API, the Alias Python API module can be directly imported (since it
        does not need to communicate with a running instance of Alias).

        :param hostname: For OpenAlias, the server host name to connect to, to access the api.
        :type hostname: str
        :param port: For OpenAlias, the server port to connect to, to access the api.
        :type port: int
        :param namespace: For OpenAlias, the server namespace to connect to, to access the api.
        :type namespace: str
        :param force: Force the api to be initialized, even if it has already been initialized.
        :type force: bool
        """

        if self.__alias_py and not force:
            # Already initialized.
            return

        if self.__in_alias_process:
            # ShotGrid is running in the same process as Alias. This is the old way that the
            # engine was set up for, and will not work with Alias versions that use Qt for its
            # GUI (>=2024.0).
            try:
                import alias_api
            except Exception as api_import_error:
                raise Exception(
                    f"Failed to import Alias Python API in same process as Alias.\n{api_import_error}"
                )
            api_module = alias_api

            if self.__has_ui:
                # When running ShotGrid in the same process as Alias, the qt app needs to be
                # created by the engine
                self.__init_qt_app()
        else:
            # ShotGrid is running in a separate process than Alias. This is the new way how
            # the engine operates: the Alias plugin will bootstrap the engine in a separate
            # process than Alias (to avoid Qt conflicts between QtQuick/QML and QWidgets).

            if self.__is_open_model or None in (hostname, port, namespace):
                # Run in OpenModel model (headless/batch), directly import the Alias Python API
                # module for OpenModel, which should already be imported via importing the
                # tk-framework-alias module (in python/tk_alias/framework_alias.py).
                try:
                    import alias_api_om
                except Exception as api_import_error:
                    raise Exception(
                        f"Failed to import Alias Python API for OpenModel.\n{api_import_error}"
                    )

                api_module = alias_api_om
                # Initialize the universe to make the api ready for requests.
                api_module.initialize_universe()
            else:
                # Run in OpenAlias mode, an instance of Alias should be running with a server
                # listening for client connections to communicate with. Using the socket
                # communication, the api will be imported.
                connected = self.__setup_sio(hostname, port, namespace)
                if not connected:
                    raise Exception("Failed to connect to Alias api server")

                # Get the server info and api module through the socket connection
                api_module = self.__sio.get_alias_api()
                if not api_module:
                    raise Exception("Failed to get Alias Python API for OpenAlias.")

        # Create the AliasPy object to wrap the api module. All Alias api requests can be made
        # directly with the AliasPy object, it will route the request to the actual api module
        self.__alias_py = self._tk_alias.AliasPy(api_module)

        # Allow the AliasPy object to be imported. This is for backward compatibility with
        # previous engine versions aceessing the alias_api.pyd module directly through import
        sys_module_name = "alias_api"
        sys.modules[sys_module_name] = self.__alias_py

        try:
            # Sanity check that the module can be imported.
            import alias_api

            assert alias_api is self.__alias_py
        except Exception as import_error:
            raise Exception(
                f"Failed to set up the Alias Python API module\n{import_error}"
            )

    def __init_alias_event_watcher(self):
        """
        Initialize the Alias event watcher.

        Register any initial Alias message event callbacks, and start watching for events immediately.

        NOTE: registering callback for event AlMessageType.DagNameModified causes a crash on startup.
        This looks like a bug where Alias is not ready to handle events yet but we can register them.

        :return: The Alias event watcher object.
        :rtype: AliasEventWatcher
        """

        event_watcher = self._tk_alias.alias_event_watcher.AliasEventWatcher(self)

        # Register event callbacks
        event_watcher.register_alias_callback(
            self.on_stage_active,
            self.alias_py.AlMessageType.StageActive,
        )

        # Now start watching the events. This should be called after registering events to
        # ensure the event watcher starts listening.
        event_watcher.start_watching()

        return event_watcher

    def __check_version_support(self):
        """
        Check that the Alias version is supported.

        The Alias version must be set before calling this method.

        The Qt application must be created before calling this method.
        """

        from sgtk.platform.qt import QtGui

        if not self.alias_version:
            self.logger.debug("Couldn't get Alias version. Skip version comparison")
            return False

        if int(self.alias_version[0:4]) > self.get_setting(
            "compatibility_dialog_min_version", 2020
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
                    self._get_dialog_parent(),
                    "Warning - ShotGrid Pipeline Toolkit!",
                    msg,
                )
                return False

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
                    self._get_dialog_parent(),
                    "Warning - ShotGrid Pipeline Toolkit!",
                    msg,
                )
                return False

        # Version successfully checked and is supported
        return True

    def __get_or_create_proxy_window(self):
        """
        Create a widget to parent all ShotGrid windows to.

        This widget itself will be parented to the Alias main window.

        This method must be called after Qt and the Alias Python API has been initialized.
        """

        if not self.has_ui:
            return None

        # import alias_api
        from sgtk.platform.qt import QtGui

        if not self.__proxy_window:
            if hasattr(self.alias_py, "set_parent_window"):
                # The Alias API version >= 4.0.0 provides functions to manage the Alias main
                # window (e.g. set as parent to ShotGrid windows)
                self.__proxy_window = QtGui.QWidget()
                self.__proxy_window.setWindowTitle(self.__PROXY_WINDOW_TITLE)
                self.alias_py.set_parent_window(self.__proxy_window.winId())
            else:
                self.__proxy_window = (
                    self._tk_alias.DialogParent() if self.has_ui else None
                )

        if isinstance(self.__proxy_window, self._tk_alias.DialogParent):
            window = self.__proxy_window.get_dialog_parent()
            if window:
                return window
            else:
                return QtGui.QApplication.activeWindow()
        else:
            # Adjust window to center of Alias main window (this will only take effect when using
            # Alias Python API version >= 4.0.0
            self.alias_py.adjust_window(self.__proxy_window.winId())
            return self.__proxy_window

    def __run_app_instance_commands(self):
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

    #####################################################################################
    # Pipeline config utils

    def __get_pipeline_configuration_local_path(self, project):
        """
        Get the path to the local configuration (the one which stands in the Sgtk cache folder) in order to be able
        to build a :class`sgtk.Sgtk` instance from this path

        :param project: The project entity dict or id that we want to retrieve the config for.
            The project entity dict is required to perform the fallback code to ensure the
            pipeline config is loaded.
        :type project: dict | int

        :return: The local path to the config if we could determine which config to use, None otherwise.
        :rtype: str
        """

        # For backward compatibility, allow passing the project id (instead of entity dict),
        # though if only the id is given, then the fallback code to load the pipeline config
        # will not be executed
        if isinstance(project, dict):
            project_id = project["id"]
        else:
            project_id = project
            project = None

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
        config_local_path = os.path.join(config_local_path, "cfg")

        # If the config has not been loaded on on disk yet, force it to load before returning
        # the path.
        if project and not os.path.exists(config_local_path):
            mgr = sgtk.bootstrap.ToolkitManager()
            mgr.plugin_id = plugin_id
            mgr.pipeline_configuration = pipeline_config["id"]
            mgr.prepare_engine("tk-desktop", project)

        return config_local_path

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

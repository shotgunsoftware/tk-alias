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
        self._stage_context = {}
        self._dialog_parent = None

        self.menu = None
        self.operations = None

        if not hasattr(sys, 'argv'):
            sys.argv = ['']

        super(AliasEngine, self).__init__(tk, context, engine_instance_name, env)

    def post_context_change(self, old_context, new_context):
        """
        Runs after a context change has occurred.

        :param old_context: The previous context.
        :param new_context: The current context.
        """
        self.logger.debug("%s: Post context change...", self)
        if self.context_change_allowed:
            self._create_menu()

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

    def post_app_init(self):
        """
        Runs after all apps have been initialized.
        """
        self.logger.debug("%s: Post Initializing...", self)

        # Init QT main loop
        self.init_qt_app()

        # import python/tk_alias module
        self._tk_alias = self.import_module("tk_alias")

        # dialog parent handler
        self._dialog_parent = self._tk_alias.DialogParent(engine=self)

        # init menu
        self.menu = self._tk_alias.AliasMenu(engine=self)

        # Env vars
        self.alias_execpath = os.getenv("TK_ALIAS_EXECPATH", None)
        self.alias_bindir = os.path.dirname(self.alias_execpath)
        self.alias_codename = os.getenv("TK_ALIAS_CODENAME", "autostudio")

        # init operations
        self.operations = self._tk_alias.AliasOperations(engine=self)

    def destroy_engine(self):
        """
        Called when the engine should tear down itself and all its apps.
        """
        self.logger.debug("%s: Destroying...", self)

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

    def on_plugin_init(self):
        """Alias plugin has been initialized."""
        self.logger.debug("Plugin initialized signal received")

        # Create menu
        self._create_menu()

        path = os.environ.get("SGTK_FILE_TO_OPEN", None)
        if path:
            self.operations.open_file(path)

    def on_plugin_exit(self):
        """Alias plugin has been finished."""
        self.operations.current_file_closed()

    def _create_menu(self):
        """Create the menu."""
        self.logger.debug("Creating menu")
        self.menu.create()
        self.logger.debug("Raw menu options: {}".format(self.menu.raw_options))
        self.logger.debug("Menu options: {}".format(self.menu.options))

        alias_api.create_menu(self.menu.options)

    def stage_selected(self):
        """Stage was selected"""
        self.logger.debug("Stage selected")

        path = self.operations.get_current_path()

        if path:
            self.logger.debug("Stage with path {} selected".format(path))
            ctx = self.sgtk.context_from_path(path, self.context)

            if not ctx.project:
                self.logger.debug("The context is not valid with this path, project context selected".format(path))
                ctx = self.sgtk.context_from_entity(self.context.project["type"], self.context.project["id"])
        else:
            self.logger.debug("Empty Stage selected")
            ctx = self.sgtk.context_from_entity(self.context.project["type"], self.context.project["id"])

        if ctx != sgtk.platform.current_engine().context:
            self.change_context(ctx)
            self.logger.debug("Context changed")
        else:
            self.logger.debug("Context not changed")

    def _get_dialog_parent(self):
        """ Get Alias dialog parent"""
        return self._dialog_parent.get_dialog_parent()


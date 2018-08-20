# -*- coding: utf-8 -*-
# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
"""
This is a simple wrapper over ZeroMQ sockets which uses the current protocol
(ECHO, LOAD, etc. messages) to control the Alias C++ plugin.
"""

import os
import sys
import time
import logging
import threading
import json
import webbrowser
import unicodedata
import tempfile
from datetime import datetime
import uuid

import tank
from PySide import QtCore, QtGui
from psutil import pid_exists

from parent_handler import ParentHandler
from session import Session
from commands import PidRequest, FileOpenCommand, MenuRebuildCommand, \
    StageOpenCommand, FileSaveCommand, ResetCommand, CurrentFileCommand, \
    ExportAnnotationsCommand, ExportVariantsCommand


PID_CHECK_PERIOD = 2


class GlobalState(object):
    pass

globals = GlobalState()


class AliasEngine(tank.platform.Engine):
    """
    The Alias engine.
    """

    async_callbacks = {}
    alias_codename = "autostudio"
    SYNC_APPS = ['tk-multi-snapshot']

    def pre_app_init(self):
        """
        Runs after the engine is set up but before any apps have been initialized.

        We use this method to set up basic things that will be needed through
        the lifecycle of the Engine, such as the logger and instance variables.
        """
        # tell QT to interpret C strings as utf-8
        utf8 = tank.platform.qt.QtCore.QTextCodec.codecForName("utf-8")
        tank.platform.qt.QtCore.QTextCodec.setCodecForCStrings(utf8)
        self.logger.debug("set utf-8 codec for widget text")
        
        self.initialize()

        self.last_opened_file = None

        self.log_info("Engine started, pre app initialization")

    def post_app_init(self):
        """
        Runs when all apps have initialized.

        This method opens the connection to the Alias plugin and starts threads
        for communicating with it. This method blocks after starting the Qt main
        loop.
        """

        # request the PID
        globals.session.send(PidRequest())

        self.log_info("Engine started, apps initialized")
        self._initialize_dark_look_and_feel()

        # If the app was launched to open a file, do so
        file_to_open = os.environ.get("TANK_FILE_TO_OPEN", None)
        if file_to_open:
            self.load_file(file_to_open, self.create_menu)
        else:
            self.create_menu()

    def initialize(self):
        """
        Set up everything.
        """
        logging.basicConfig()
        self.__logger = self.logger
        self.current_file = ""

        self.log_info("Initializing tk-alias engine")

        # Initial values
        globals.run_threads = True
        globals.callbacks = {}
        globals.callback_runner = CallbackRunner(self.__logger)
        globals.parent_pid = -1
        globals.current_file = None
        self.message_callbacks = MessageCallbackStore()
        globals.parent_handler = None

        # Create the Session and connect to the Alias plugin
        port = os.environ["TK_ALIAS_PORT"]
        self.log_info("Connecting to Alias on port {}".format(port))
        globals.session = Session(port)
        globals.session.connect()
        self.log_info("Connected")

        # Codename
        self.alias_codename = os.environ.get("TK_ALIAS_CODENAME", "autostudio")

        # Spawn separate receiver thread
        globals.ipc_thread = threading.Thread(target=self.run_socket_loop, args=())
        globals.ipc_thread.daemon = True
        self.log_info("Starting IPC thread")
        globals.ipc_thread.start()
        self.log_info("Started")

        # Spawn separate pid check thread
        globals.pid_check_thread = threading.Thread(target=self.run_pid_check, args=())
        globals.pid_check_thread.daemon = True
        self.log_info("Starting pid check thread")
        globals.pid_check_thread.start()
        self.log_info("Started")

    def destroy_engine(self):
        """
        Called when the engine should tear itself down.
        """
        self.log_info("Destroying engine")

    def quit(self):
        """
        Called after Alias has shut down.
        """
        def __quit():
            self.log_info("Quitting")

            # Stop threads
            globals.run_threads = False

            # First, notify anyone who might be listening that the current file is
            # closing.
            path = self.last_opened_file
            if path:
                self.execute_hook_method("file_usage_hook", "file_closed", path=path)

            # Wait until threads finish
            globals.pid_check_thread.join()
            globals.ipc_thread.join()

            # Close socket
            globals.session.disconnect()

            self.log_info("Alias has closed")

            os._exit(0)

        # Ensure all logging makes it
        sys.stderr.flush()

        # Quit from the main thread
        self.send_to_main_thread(__quit)

    def send_to_main_thread(self, fn, *args, **kwargs):
        """
        Wrap a function in a RunCallbackEvent, and send it to the main thread, where
        it will be processed by the Engine's CallbackRunner.
        """
        QtCore.QCoreApplication.postEvent(globals.callback_runner,
                                          RunCallbackEvent(fn, *args, **kwargs))

    # Thread methods
    def run_socket_loop(self):
        """
        The main loop for the IPC thread, this continually reads messages from the
        Alias plugin.
        Plugin Message structure:
            {
                u'status': u'ok',
                u'initialCommand': u'FileSave',
                u'command': u'CommandCompleted'
            }
        """
        while globals.run_threads:
            self.log_info("Waiting for message")
            message = globals.session.read_message()

            if not message:
                if not globals.run_threads:
                    break
                else:
                    continue

            self.log_info("Received IPC message: {!r}".format(message))
            try:
                decoded = ""
                message = message.replace("\\", "/")
                decoded = json.loads(message)
                if decoded["command"] == "CommandCompleted":
                    if decoded["status"] == u'ok' and decoded["initialCommand"] in self.async_callbacks:
                        self.log_info('\n* Execute async for {0}\n'.format(decoded))
                        self.async_callbacks[decoded["initialCommand"]]()
                elif decoded["command"] == "PidResponse":
                    self.log_info("Received PID request message")
                    try:
                        globals.parent_pid = int(decoded["pid"])
                    except Exception as exp:
                        globals.parent_pid = -1
                        self.log_info(exp)
                elif decoded["command"] == "uiClicked":
                    self.log_info("Received a click event from Alias")
                    ui_callback = decoded["buttonId"]
                    if ui_callback in globals.callbacks.keys():
                        self.log_info("Sending click callback to main thread")
                        self.send_to_main_thread(globals.callbacks[ui_callback])
                    else:
                        self.log_info("Requested callback does not exists")
                elif decoded["command"] == "ContextChange":
                    self.log_info("Received a Context change event")
                    path = decoded["path"]
                    if path:
                        self.log_info("Changing current file")
                        self.load_file(path, lambda: None)
                    else:
                        self.log_info("Context did not specify a new file path")

                # check if there is a callback waiting for this message
                callback = self.message_callbacks.find_message_callback(decoded)
                if callback:
                    callback_name, callback_fn = callback

                    # invoke the callback
                    callback_fn(decoded)

                    # remove the old data
                    self.message_callbacks.remove_message_callback(callback_name)
                else:
                    self.log_info("No callback found for this message")
            except Exception as e:
                self.log_info("Non-JSON message received: \n\nerror: [{!r}]\nmessage: [{!r}]\ndecoded: [{!r}]".format(e, message, decoded))

        self.log_info("Finished run_socket_loop")

    def run_pid_check(self):
        """
        The main loop for the pid check thread, when we have a process ID this method
        periodically checks if Alias is still running. When no process is found
        with that specific ID then Alias is closed.
        """
        try_count = 0

        while globals.run_threads:
            # Check if Alias is still alive
            if globals.parent_pid is not None:
                if globals.parent_pid != -1 and not pid_exists(globals.parent_pid):
                    self.log_info("Alias process is not longer running")
                    break

                if globals.parent_pid == -1 and try_count > 20:
                    self.log_info("Alias never started")
                    break

            # Sleep for a while to give Alias time to start
            time.sleep(PID_CHECK_PERIOD)
            try_count += 1

        self.log_info("Finished run_pid_check")
        self.quit()

    def run_qt_loop(self):
        """
        The PySide/Qt main loop.
        """
        if QtGui.qApp is None:
            QtGui.QApplication(sys.argv)
        QtGui.qApp.setQuitOnLastWindowClosed(False)
        engine_path = os.path.dirname(os.path.abspath(__file__))
        icon = QtGui.QIcon(os.path.join(engine_path, "icon_256.png"))
        QtGui.qApp.setWindowIcon(icon)
        sys.exit(QtGui.qApp.exec_())

    def _get_dialog_parent(self):
        if globals.parent_pid != -1:
            self.log_info("Parent pid is {}\n".format(globals.parent_pid))
            if not hasattr(self, "parent_handler"):
                self.parent_handler = ParentHandler(globals.parent_pid)
            self.hnd_win = self.parent_handler._get_dialog_parent()
            return self.hnd_win
        else:
            return super(AliasEngine, self)._get_dialog_parent()

    def create_menu(self):
        # Tell the Alias plugin to create a menu
        # NOTE: MenuRequests will likely change as the protocol evolves
        self.log_info("Creating Shotgun menu")

        buttons = []

        # Create the entity submenu
        context_name = str(self.context)
        menu_items = self._add_shotgun_buttons()
        for button_name in menu_items:
            buttons.append({"name": button_name, "path": context_name, "message": ""})

        # now enumerate all items and create menu objects for them
        self.panel_items = []
        for (cmd_name, cmd_details) in self.commands.items():
            if cmd_name != 'Upload Files':
                self.panel_items.append(AppCommand(cmd_name, cmd_details, self.__logger))

        # sort list of commands in name order
        self.panel_items.sort(key=lambda x: x.name)

        self.log_info("Panel Items: {!r}".format([item.name for item in self.panel_items]))

        # First divider
        buttons.append({"separator": True, "path": ""})

        # now add favourites
        for fav in self.get_setting("menu_favourites"):
            app_instance_name = fav["app_instance"]
            menu_name = fav["name"]
            # scan through all menu items
            for cmd in self.panel_items:
                 if cmd.get_app_instance_name() == app_instance_name and cmd.name == menu_name:
                     # found our match!
                     buttons.append({"name": menu_name, "path": "", "message": ""})
                     self.log_info("--- favorite menu item {}".format(menu_name))
                     # mark as a favourite item
                     cmd.favourite = True
                     cmd.add_to_callbacks(globals.callbacks)

        # Second divider
        buttons.append({"separator": True, "path": ""})

        # now go through all of the panel items.
        # separate them out into various sections
        self.commands_by_app = {}

        for cmd in self.panel_items:
            if cmd.get_type() == "context_menu":
                # context menu!
                cmd.add_to_callbacks(globals.callbacks)

                if not filter(lambda x: x.has_key("name") and x["name"] == cmd.name, buttons):
                    buttons.append({"name": cmd.name, "path": context_name, "message": ""})
            else:
                # normal menu
                app_name = cmd.get_app_name()
                if app_name is None:
                    # un-parented app
                    app_name = "Other Items"
                if not app_name in self.commands_by_app:
                    self.commands_by_app[app_name] = []
                self.commands_by_app[app_name].append(cmd)

        self.log_info("Set command callbacks")

        # now add all apps to main menu
        self._add_app_menu(self.commands_by_app, buttons, globals.callbacks)

        self.log_info(buttons)
        self.send_and_wait(message=MenuRebuildCommand(buttons))

        self.available_callbacks = ",".join(globals.callbacks.keys())
        self.log_info("Available callbacks: {}".format(self.available_callbacks))

    def _add_shotgun_buttons(self):
        """
        Register some commands. Returns a list of the command names.
        """
        shotgun_commands = [
            ("Jump to Shotgun", self._jump_to_sg, {"type": "context_menu", "short_name": "jump_to_sg"}),
            ("Jump to File System", self._jump_to_fs, {"type": "context_menu", "short_name": "jumdesp_to_fs"})
        ]

        for command in shotgun_commands:
            self.register_command(*command)
        return [command[0] for command in shotgun_commands]

    def _jump_to_sg(self):
        """
        Launch the user's web browser to the URL that corresponds to the
        current Shotgun context."
        """
        webbrowser.open(self.context.shotgun_url, autoraise=True)

    def _jump_to_fs(self):
        """
        Open the file manager to the filesystem location that corresponds to
        the current Shotgun context.
        """
        # launch one window for each location on disk
        paths = self.context.filesystem_locations
        for disk_location in paths:

            # get the setting
            system = sys.platform

            # run the app
            if system == "linux2":
                cmd = "xdg-open \"{}\"".format(disk_location)
            elif system == "darwin":
                cmd = "open \"{}\"".format(disk_location)
            elif system == "win32":
                cmd = "cmd.exe /C start \"Folder\" \"{}\"".format(disk_location)
            else:
                raise Exception("Platform {!r} is not supported.".format(system))

            exit_code = os.system(cmd)
            if exit_code != 0:
                self.log_error("Failed to launch {!r}!".format(cmd))

    def _add_app_menu(self, commands_by_app, buttons, callbacks):
        """
        Add all apps to the main menu, process them one by one.
        """
        for app_name in sorted(commands_by_app.keys()):
            if len(commands_by_app[app_name]) > 1:
                # more than one menu entry fort his app
                # make a sub menu and put all items in the sub menu

                # get the list of menu cmds for this app
                cmds = commands_by_app[app_name]
                # make sure it is in alphabetical order
                cmds.sort(key=lambda x: x.name)

                for cmd in cmds:
                    self.log_info('\n\n--->{0}'.format(cmd.name))
                    buttons.append({"name": cmd.name, "path": app_name, "message": ""})
                    cmd.add_to_callbacks(callbacks)
            else:
                # this app only has a single entry.
                # display that on the menu
                # todo: Should this be labelled with the name of the app
                # or the name of the menu item? Not sure.
                cmd_obj = commands_by_app[app_name][0]
                if not cmd_obj.favourite:
                    # skip favourites since they are alreay on the menu
                    buttons.append({"name": cmd_obj.name, "path": "", "message": ""})
                    cmd_obj.add_to_callbacks(callbacks)

    def log_info(self, message):
        """
        Log debugging information.
        """
        self.__logger.info(message)

    def load_file(self, path, callback):
        """
        Load a file from the specified path into the workspace.
        """
        # Notify the file usage hook that the file was opened
        if not hasattr(self, "current_file"):
            current_file = self.get_current_file()
        else:
            if self.current_file is not None:
                current_file = self.current_file
            else:
                current_file = self.get_current_file()

        allowed_to_open = self.execute_hook_method("file_usage_hook", "file_attempt_open", path=path)
        if allowed_to_open:
            open_as_new_stage = False
            if current_file:
                answer = QtGui.QMessageBox.question(
                    QtGui.QApplication.activeWindow(),
                    "Open",
                    "DELETE all objects, shaders, views and actions in all existing Stage before Opening this File?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
                )

                if answer == QtGui.QMessageBox.No:
                    open_as_new_stage = True
                elif answer == QtGui.QMessageBox.Yes:
                    open_as_new_stage = False

                    # Opening a file involves closing the old one.
                    # Notify the file usage hook of the closing.
                    self.current_file_closed(current_file=current_file)
                elif answer == QtGui.QMessageBox.Cancel:
                    return

            if open_as_new_stage:
                self.send_async(StageOpenCommand(path), callback)
            else:
                self.log_info("Opening file {!r}".format(path))
                self.send_async(FileOpenCommand(path), callback)
            self.last_opened_file = path

    def save_file(self, path, parent=None):
        """
        Save the current workspace to the specified path.

        This method is synchronous, and returns when the file has been saved.
        """
        self.current_file_closed()
        def check_lock():
            self.log_info("\n* Check lock process for file '{0}'".format(path))
            allowed_to_open = self.execute_hook_method("file_usage_hook", "file_attempt_open", path=path)
            if not allowed_to_open:
                raise TankError("Can't save file: a lock for this path already exists")
            self.last_opened_file = path
        if parent in self.SYNC_APPS:
            self.send_and_wait(message=FileSaveCommand(path))
        else:
            self.send_and_wait_async(message=FileSaveCommand(path), timeout=120, cb=check_lock)

    def reset_scene(self, current_file=None):
        """
        Clear the Alias scene. This sends the reset command to the plugin,
        which closes the current file and opens a new workspace.
        """
        if current_file:
            self.log_info("Resetting scene")
            self.send_and_wait(message=ResetCommand())

            # Notify the file usage hook that the file was closed
            self.current_file_closed(current_file=current_file)

    def pre_context_change(self, old_context, new_context):
        """
        Called when a context switch is about to happen.
        """
        # Just log for testing purposes, this implementation can be
        # removed if there is nothing to do here
        self.log_info("pre_context_change called")

    def post_context_change(self, old_context, new_context):
        """
        Called right after a context switch, let's send the new
        context to the Alias side.
        """
        self.log_info("post_context_change called with context {}".format(new_context))
        if self.context_change_allowed:
            self.create_menu()

    @property
    def context_change_allowed(self):
        """
        Overriding the engine base class property to allow
        context switch without a restart of this engine.
        """
        # see: http://developer.shotgunsoftware.com/tk-core/platform.html?highlight=context_change_allowed#sgtk.platform.Engine.context_change_allowed
        return True

    def get_current_file(self):
        """
        Query Alias for the path of the current .wire file. Returns the empty
        string if no file is open.
        """
        message = self.send_and_wait(message=CurrentFileCommand(), command="CurrentFileAck", timeout=3)
        if message and "openedFile" in message:
            self.current_file = message["openedFile"]
            return self.current_file
        else:
            return self.current_file

    def current_file_closed(self, current_file=None):
        """
        This method should be called when the current file is closed.
        """
        if current_file is None:
            path = self.get_current_file()
        else:
            path = current_file
        if path:
            self.log_info("current_file_closed: notifying the file usage hook that the current file has closed")
            self.execute_hook_method("file_usage_hook", "file_closed", path=path)
        else:
            self.log_info("current_file_closed: in empty scene, no need to notify file usage hook")

    def _call_func_in_dir(self, func, *args, **opts):
        """
        This function will call func with the given arguments in the
        execution context of the own func containing folder, and then
        restore the original calling directory.
        """
        prev = os.path.abspath(os.getcwd()) # Save the real cwd
        try:
            # Get the child's physical location.
            func_path = sys.modules[func.__module__].__file__
        except:
            # Die; we got passed a built-in function (no __file__)
            # Or you could just call it, I guess: return func(*args, **opts)
            return None

        # Change to the expected directory and run the function.
        os.chdir(os.path.dirname(func_path))
        result = func(*args, **opts)

        # Fix the cwd, and return.
        os.chdir(prev)
        return result

    def send_and_wait_async(self, message, timeout=30, command=None, cb=None):
        self.log_info("send_and_wait_async: {!r} {!r}".format(message, command))
        return_message = {}
        def send_and_wait_cb():
            self.message_callbacks.remove_message_callback(command_key)
            if cb:
                cb()
        def get_message(incoming_message):
            return_message["thisisahack"] = incoming_message

        if command:
            command_key = {"command": command}
        else:
            command_key = {"command": "CommandCompleted", "initialCommand": message.command}

        self.async_callbacks[message.command] = send_and_wait_cb
        self.message_callbacks.add_message_callback(key=command_key, callback=get_message)
        globals.session.send(message)

    def send_and_wait(self, message, timeout=30, command=None):
        """
        Send a command to the Alias plugin and wait for the reply.
        """
        self.log_info("send_and_wait: {!r} {!r}".format(message, command))

        return_message = {}

        def get_message(incoming_message):
            return_message["thisisahack"] = incoming_message

        if command:
            command_key = {"command": command}
        else:
            command_key = {"command": "CommandCompleted", "initialCommand": message.command}

        self.message_callbacks.add_message_callback(key=command_key, callback=get_message)
        globals.session.send(message)
        start_wait = datetime.now()
        # now we wait
        while (not return_message.has_key("thisisahack")) and ((datetime.now() - start_wait).seconds < timeout):
            time.sleep(0.1)

        if return_message.has_key("thisisahack"):
            self.log_info("send_and_wait: received a reply for {}".format(command_key))
            result = return_message["thisisahack"]
        else:
            self.log_info("send_and_wait: did not receive a reply for {}".format(command_key))
            result = None

        self.message_callbacks.remove_message_callback(command_key)
        return result

    def send_async(self, command, callback):
        """
        Send a command and add a callback to call when it's done.
        """
        command_key = {"command": "CommandCompleted", "initialCommand": command.command}

        def internal_callback(message):
            callback()
            self.message_callbacks.remove_message_callback(command_key)

        self.message_callbacks.add_message_callback(key=command_key, callback=internal_callback)
        globals.session.send(command)

    def export_variants(self):
        if not hasattr(self, "current_file") or not self.current_file:
            current_file = self.get_current_file()
        else:
            current_file = self.current_file

        if not current_file:
            file_name_prefix = str(uuid.uuid4()).replace("-", "")
        else:
            current_file_name, current_file_extension = os.path.splitext(os.path.basename(current_file))
            file_name_prefix = "{}-variant-".format(current_file_name)

        temp_dir = tempfile.mkdtemp()

        try:
            results = self.send_and_wait(message=ExportVariantsCommand(file_name_prefix, temp_dir),
                                         timeout=120,
                                         command="CurrentVariants")
        except Exception as es:
            results = None

        return {
            "files": results.get("files").split(",") if results else None,
            "temp_dir": temp_dir,
        }

    def export_annotations(self):
        try:
            results = self.send_and_wait(message=ExportAnnotationsCommand(),
                                         timeout=120,
                                         command="CurrentAnnotations")
        except Exception as e:
            results = None

        return {
            "strings": results.get("strings").split("SEP") if results else None,
        }

    def save_after_publish(self, path):
        """
        Save the scene after publish in order to get a new version in the workfiles folder
        """
        self.send_and_wait(FileSaveCommand(path))


class AppCommand(object):
    """
    Wraps around a single command that you get from engine.commands
    """

    def __init__(self, name, command_dict, logger):
        self.name = name
        self.properties = command_dict["properties"]
        self.callback = command_dict["callback"]
        self.favourite = False
        self.__logger = logger

    def get_app_name(self):
        """
        Returns the name of the app that this command belongs to.
        """
        if "app" in self.properties:
            return self.properties["app"].display_name
        return None

    def get_app_instance_name(self):
        """
        Returns the name of the app instance, as defined in the environment.
        Returns None if not found.
        """
        if "app" not in self.properties:
            return None

        app_instance = self.properties["app"]
        engine = app_instance.engine

        for (app_instance_name, app_instance_obj) in engine.apps.items():
            if app_instance_obj == app_instance:
                # found our app!
                return app_instance_name
        return None

    def get_documentation_url_str(self):
        """
        Returns the documentation as a string.
        """
        if "app" in self.properties:
            app = self.properties["app"]
            doc_url = app.documentation_url
            # deal with nuke's inability to handle unicode. #fail
            if doc_url.__class__ == unicode:
                doc_url = unicodedata.normalize("NFKD", doc_url).encode("ascii", "ignore")
            return doc_url

        return None

    def get_type(self):
        """
        Returns the command type. Returns 'node', 'custom_pane' or 'default'.
        """
        return self.properties.get("type", "default")

    def add_to_callbacks(self, callbacks):
        """
        Adds an app to the callbacks dictionary.
        """
        callbacks[self.name] = self.callback
        self.__logger.info("Adding {!r} to the callback list".format(self.name))


# Callback management code

class CallbackRunner(QtCore.QObject):
    """
    Runs callbacks in the main thread.
    """

    def __init__(self, logger):
        """
        Initialize the CallbackRunner object.

        :param logging.Logger logger: The logger instance.
        """
        super(CallbackRunner, self).__init__()
        self._logger = logger

    def event(self, event):
        """
        The main event handler.

        :param QtCore.QEvent event: An event.
        :return: :code:`True` to prevent event propagation.
        :rtype bool:
        """
        self._logger.info("Responding to an event")
        try:
            if (getattr(event.fn, "_tkLog", True)):
                self._logger.info("Callback %s", str(event.fn))
            event.fn(*event.args, **event.kwargs)
        except Exception as e:
            self._logger.exception("Error in callback %s", str(event.fn))
        return True

class RunCallbackEvent(QtCore.QEvent):
    """
    Encapsulates a callback in an Event. The event is used to notify the
    CallbackRunner.
    """

    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, fn, *args, **kwargs):
        QtCore.QEvent.__init__(self, RunCallbackEvent.EVENT_TYPE)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

# Thread-safe callback store

class MessageCallbackStore(object):
    """
    A thread safe store of message callbacks.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._store = []

    def add_message_callback(self, key, callback):
        """
        Associate a key to a callback function.
        """
        self._lock.acquire()
        if not self._find_message_callback(key):
            self._store.append((key, callback))
        self._lock.release()

    def remove_message_callback(self, key):
        """
        Remove a message callback identified by its key.
        """
        self._lock.acquire()
        item = self._find_message_callback(key)
        if item:
            self._store.remove(item)
        self._lock.release()

    def _find_message_callback(self, key):
        """
        Find a message callback function by its key.
        Returns None if no matching key was found.
        This method doesn't affect the state of the store lock, so it's only to
        be used internally.
        """
        for (msg_key, callback) in self._store:
             if all(map(lambda (k, v): key.has_key(k) and key[k] == v, msg_key.items())):
                return (msg_key, callback)
        return None

    def find_message_callback(self, key):
        """
        Find a message callback function by its key.
        Returns None if no matching key was found.
        """
        self._lock.acquire()
        callback = self._find_message_callback(key)
        self._lock.release()
        return callback

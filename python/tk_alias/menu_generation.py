# Copyright (c) 2020 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
import os

from tank_vendor import six
from sgtk.platform.qt import QtGui, QtCore
from sgtk.util import is_windows, is_macos, is_linux

import alias_api


class AliasMenuGenerator(object):
    """
    Menu handling for Alias.
    """

    MENU_NAME = "al_shotgun"

    def __init__(self, engine):
        """
        Initializes a new menu generator.

        :param engine: The currently-running engine.
        :type engine: :class:`tank.platform.Engine`
        """
        self._engine = engine
        self._alias_menu = alias_api.Menu(self.MENU_NAME)

    def create_menu(self, clean_menu=True):
        """
        Render the entire Shotgun menu.

        :param clean_menu:  If clean_menu is set to true, the previous Shotgun menu will be cleaned before creating the
                            new one. This is useful in the case you're rebuilding the menu after context switching.
        """

        # First, ensure that the Shotgun menu inside Alias is empty.
        # This is to ensure we can recover from weird context switches
        # where the engine didn't clean up after itself properly.
        if clean_menu:
            self._alias_menu.clean()

        # Add the context item on top of the main menu
        self._context_menu = self._add_context_menu()

        # Now enumerate all items and create menu objects for them.
        menu_items = []
        for (cmd_name, cmd_details) in self._engine.commands.items():
            menu_items.append(AppCommand(cmd_name, cmd_details))

        # Sort list of commands in name order
        menu_items.sort(key=lambda x: x.name)

        # Add favourites
        add_separator = True
        for fav in self._engine.get_setting("menu_favourites"):
            app_instance_name = fav["app_instance"]
            menu_name = fav["name"]

            # scan through all menu items.
            for cmd in menu_items:
                if cmd.app_instance_name == app_instance_name and cmd.name == menu_name:
                    cmd.add_command_to_menu(
                        self._alias_menu, add_separator=add_separator
                    )
                    cmd.favourite = True
                    # Only add a separator for the first menu item
                    add_separator = False

        # Go through all of the menu items.
        # Separate them out into various sections.
        commands_by_app = {}
        add_separator = True
        for cmd in menu_items:

            # context menu case
            if cmd.app_type == "context_menu":
                cmd.add_command_to_menu(
                    self._alias_menu,
                    sub_menu=self._context_menu,
                    add_separator=add_separator,
                )
                add_separator = False

            # normal menu
            else:
                if cmd.app_name not in commands_by_app:
                    commands_by_app[cmd.app_name] = []
                commands_by_app[cmd.app_name].append(cmd)

        # add all the apps to the main menu
        self._add_apps_to_menu(commands_by_app)

    def clean_menu(self):
        """
        Clean the Shotgun menu in Alias by removing all its entries.
        """
        self._alias_menu.clean()

    def _add_context_menu(self):
        """
        Adds a context menu which displays the current context

        :return:  An :class:`alias_api.MenuItem` instance representing the context menu.
        """
        ctx = self._engine.context
        ctx_name = six.ensure_str(str(self._engine.context))

        # Create the menu object
        ctx_menu = self._alias_menu.add_menu(ctx_name)
        self._alias_menu.add_command(
            "Jump to Shotgun", self._jump_to_sg, parent=ctx_menu
        )
        if ctx.filesystem_locations:
            self._alias_menu.add_command(
                "Jump to File System", self._jump_to_fs, parent=ctx_menu
            )

        return ctx_menu

    def _add_apps_to_menu(self, commands_by_app):
        """
        Add all apps to the main menu, process them one by one.

        :param commands_by_app:  List of all the apps to add to the menu
        """

        add_separator = True
        for app_name in sorted(commands_by_app.keys()):
            if len(commands_by_app[app_name]) > 1:
                # more than one menu entry fort his app
                # make a sub menu and put all items in the sub menu
                sub_menu = self._alias_menu.add_menu(app_name)

                # get the list of menu commands for this app and make sure it is in alphabetical order
                commands = commands_by_app[app_name]
                commands.sort(key=lambda x: x.name)

                for cmd_obj in commands:
                    cmd_obj.add_command_to_menu(self._alias_menu, sub_menu)

            else:
                # this app only has a single entry.
                # display that on the menu
                cmd_obj = commands_by_app[app_name][0]
                if not cmd_obj.favourite:
                    cmd_obj.add_command_to_menu(
                        self._alias_menu, add_separator=add_separator
                    )
                    add_separator = False

    def _jump_to_sg(self):
        """
        Jump to shotgun, launch web browser
        """
        url = self._engine.context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _jump_to_fs(self):
        """
        Jump from a context to the filesystem.
        """
        # launch one window for each location on disk
        paths = self._engine.context.filesystem_locations

        for disk_location in paths:
            if is_linux():
                cmd = 'xdg-open "%s"' % disk_location
            elif is_macos():
                cmd = 'open "%s"' % disk_location
            elif is_windows():
                cmd = 'cmd.exe /C start "Folder" "%s"' % disk_location
            else:
                raise Exception("Platform is not supported.")

            self._engine.logger.debug("Jump to filesystem command: {}".format(cmd))

            exit_code = os.system(cmd)
            if exit_code != 0:
                self._engine.logger.error("Failed to launch '%s'!", cmd)

    def refresh(self):
        """
        Refresh the menu by forcing Alias to rebuild of its menus.
        """
        self._alias_menu.refresh()


class AppCommand(object):
    """
    Wraps around a single command that you get from engine.commands
    """

    def __init__(self, name, command_dict):
        """
        Class constructor

        :param name: Command name
        :param command_dict: Dictionary containing Command details
        """
        self.name = name
        self.properties = command_dict["properties"]
        self.favourite = False
        self.callback = command_dict["callback"]

    @property
    def app_instance_name(self):
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
                return app_instance_name

        return None

    @property
    def app_type(self):
        """
        Returns the command type
        """
        return self.properties.get("type", "default")

    @property
    def app_name(self):
        """
        Returns the name of the app that this command belongs to
        """
        if "app" in self.properties:
            return self.properties["app"].display_name
        return "Other Items"

    def add_command_to_menu(self, menu, sub_menu=None, add_separator=False):
        """
        Adds an app command to the menu

        :param menu: Menu to add the command to
        :param sub_menu:  If a submenu is provided by the user, add the command under it
        :return:
        """
        if sub_menu:
            return menu.add_command(
                self.name, self.callback, add_separator=add_separator, parent=sub_menu
            )
        return menu.add_command(self.name, self.callback, add_separator=add_separator)

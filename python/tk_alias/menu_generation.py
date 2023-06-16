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
from sgtk.util import is_windows, is_macos, is_linux


class AliasMenuGenerator(object):
    """Menu handling for Alias."""

    def __init__(self, engine):
        """
        Initializes a new menu generator.

        :param engine: The currently-running engine.
        :type engine: :class:`tank.platform.Engine`
        """

        self.__engine = engine

        if self._version_check(engine.alias_version, "2024.0") >= 0:
            self.__menu_name = "ShotGrid"
        elif self._version_check(engine.alias_version, "2022.2") >= 0:
            self.__menu_name = "al_shotgrid"
        else:
            self.__menu_name = "al_shotgun"

        self.__alias_menu = None

    @property
    def engine(self):
        return self.__engine

    @property
    def menu_name(self):
        return self.__menu_name

    @property
    def alias_menu(self):
        return self.__alias_menu

    def build(self):
        """
        Build the ShotGrid menu shown in Alias.

        If the menu has already been created, it will be rebuilt based on the Alias Engine's
        current context.
        """

        if self.alias_menu is None:
            # First, create the ShotGrid menu in Alias.
            self.__alias_menu = self.engine.alias_py.Menu(self.menu_name)
        else:
            # Make sure we're starting with a fresh menu
            self.clean_menu()

        # Add the context item on top of the main menu
        self._context_menu = self._add_context_menu()

        # Add a plugin submenu for dev only
        if not self.engine.in_alias_process and os.environ.get("TK_DEBUG") in (
            "1",
            "true",
            "True",
        ):
            plugin_menu = self.alias_menu.add_menu("Plugin")
            self.alias_menu.add_command(
                "Restart ShotGrid Client",
                self.engine.restart_process,
                parent=plugin_menu,
            )

        # Now enumerate all items and create menu objects for them.
        menu_items = []
        for (cmd_name, cmd_details) in self.engine.commands.items():
            menu_items.append(AppCommand(cmd_name, cmd_details))

        # Sort list of commands in name order
        menu_items.sort(key=lambda x: x.name)

        # Add favourites
        add_separator = True
        for fav in self.engine.get_setting("menu_favourites"):
            app_instance_name = fav["app_instance"]
            menu_name = fav["name"]

            # scan through all menu items.
            for cmd in menu_items:
                if cmd.app_instance_name == app_instance_name and cmd.name == menu_name:
                    cmd.add_command_to_menu(
                        self.alias_menu, add_separator=add_separator
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
                    self.alias_menu,
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
        """Clean the ShotGrid menu in Alias by removing all its entries."""

        self.alias_menu.clean()

    def _add_context_menu(self):
        """
        Adds a context menu which displays the current context

        :return:  An :class:`alias_api.MenuItem` instance representing the context menu.
        """

        ctx = self.engine.context
        ctx_name = six.ensure_str(str(self.engine.context))

        # Create the submenu
        ctx_menu = self.alias_menu.add_menu(ctx_name)

        # Add the context submenu actions
        self.alias_menu.add_command(
            "Jump to ShotGrid", self._jump_to_sg, parent=ctx_menu
        )
        if ctx.filesystem_locations:
            self.alias_menu.add_command(
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
                sub_menu = self.alias_menu.add_menu(app_name)

                # get the list of menu commands for this app and make sure it is in alphabetical order
                commands = commands_by_app[app_name]
                commands.sort(key=lambda x: x.name)

                for cmd_obj in commands:
                    cmd_obj.add_command_to_menu(self.alias_menu, sub_menu)

            else:
                # this app only has a single entry.
                # display that on the menu
                cmd_obj = commands_by_app[app_name][0]
                if not cmd_obj.favourite:
                    cmd_obj.add_command_to_menu(
                        self.alias_menu, add_separator=add_separator
                    )
                    add_separator = False

    def _jump_to_sg(self):
        """
        Jump to ShotGrid, launch web browser
        """

        # Defer import to avoid import error for unit tests
        from sgtk.platform.qt import QtGui, QtCore

        url = self.engine.context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _jump_to_fs(self):
        """
        Jump from a context to the filesystem.
        """
        # launch one window for each location on disk
        paths = self.engine.context.filesystem_locations

        for disk_location in paths:
            if is_linux():
                cmd = 'xdg-open "%s"' % disk_location
            elif is_macos():
                cmd = 'open "%s"' % disk_location
            elif is_windows():
                cmd = 'cmd.exe /C start "Folder" "%s"' % disk_location
            else:
                raise Exception("Platform is not supported.")

            self.engine.logger.debug("Jump to filesystem command: {}".format(cmd))

            exit_code = os.system(cmd)
            if exit_code != 0:
                self.engine.logger.error("Failed to launch '%s'!", cmd)

    def _version_check(self, version1, version2):
        """
        Compare version strings and return 1 if version1 is greater than version2,
            0 if they are equal and -1 if version1 is less than version2

        :param version1: A version string to compare against version2 e.g. 2022.2
        :param version2: A version string to compare against version1 e.g. 2021.3.1

        :return: 1, 0, -1 as per above.
        """
        # This will split both the versions by the '.' character
        arr1 = version1.split(".")
        arr2 = version2.split(".")
        n = len(arr1)
        m = len(arr2)

        # Converts to integer from string
        arr1 = [int(i) for i in arr1]
        arr2 = [int(i) for i in arr2]

        # Compares which list is bigger and fills
        # the smaller list with zero (for unequal delimeters)
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

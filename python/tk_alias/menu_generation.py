# Copyright (c) 2020 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from collections import OrderedDict
import os

from sgtk.util import is_windows, is_macos, is_linux

# Alias 2027.1+ (FPTR plugin / split process):
#   - Menus use alias_api.gui (MainMenu, Menu, MenuItem) via socket client proxies, not
#     legacy alias_api.Menu.
#   - The engine runs outside Alias; menu objects live on the server and RPC carries
#     instance calls (add_item, remove_menu, …) and client callback ids.
#   - MainMenu(menu_name) is the single menubar root ("Flow Production Tracking"); submenus
#     are gui.Menu children.
# Legacy in-process Alias still uses alias_api.Menu when gui is unavailable.


class _AliasObjectMenuAdapter:
    """
    Bridge from toolkit menu API (add_menu / add_command / clean) to ``alias_api.gui``.

    Tracks created submenus and items so context rebuilds can call remove_menu /
    remove_item on the server-side objects through the client proxies.
    """

    def __init__(self, alias_py, menu):
        self._alias_py = alias_py
        self._menu = menu
        self._items = []
        self._submenus = []

    def add_menu(self, text):
        submenu = self._alias_py.gui.Menu(text)
        self._menu.add_menu(submenu)
        child = _AliasObjectMenuAdapter(self._alias_py, submenu)
        self._submenus.append(child)
        return child

    def add_command(self, name, callback, parent=None, add_separator=False):
        adapter = parent if parent is not None else self
        item = self._alias_py.gui.MenuItem(name, callback)
        adapter._menu.add_item(item)
        adapter._items.append(item)

    def clean(self):
        for child in reversed(self._submenus):
            child.clean()
            self._menu.remove_menu(child._menu)
        self._submenus = []
        for item in reversed(self._items):
            self._menu.remove_item(item)
        self._items = []

    def remove(self):
        try:
            return self._menu.remove()
        except AttributeError:
            self.clean()
            return None


class AliasMenuGenerator(object):
    """Menu handling for Alias."""

    MENU_CUSTOMIZATION_HOOK = "hook_menu_customization"

    def __init__(self, engine):
        """
        Initializes a new menu generator.

        :param engine: The currently-running engine.
        :type engine: :class:`tank.platform.Engine`
        """

        self.__engine = engine

        menu_customization_path = engine.get_setting(self.MENU_CUSTOMIZATION_HOOK)
        self.__menu_customization_hook_instance = engine.create_hook_instance(
            menu_customization_path
        )

        if engine.compare_alias_versions(engine.alias_version, "2024.0") >= 0:
            self.__menu_name = "Flow Production Tracking"
        elif engine.compare_alias_versions(engine.alias_version, "2022.2") >= 0:
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
        Build the Flow Production Tracking menu shown in Alias.

        If the menu has already been created, it will be rebuilt based on the Alias Engine's
        current context.
        """

        if self.alias_menu is None:
            alias_py = self.engine.alias_py
            try:
                gui = alias_py.gui
            except AttributeError:
                gui = None
            # 2027.1+: one MainMenu root in the menubar; apps/context attach as gui.Menu below it.
            if gui is not None and hasattr(gui, "MainMenu"):
                root = gui.MainMenu(self.menu_name)
                self.__alias_menu = _AliasObjectMenuAdapter(alias_py, root)
            elif gui is not None and hasattr(gui, "Menu"):
                root = gui.Menu(self.menu_name)
                self.__alias_menu = _AliasObjectMenuAdapter(alias_py, root)
            elif hasattr(alias_py, "Menu"):
                self.__alias_menu = alias_py.Menu(self.menu_name)
            else:
                raise AttributeError(
                    "No supported Alias menu API found "
                    "(expected alias_api.gui.MainMenu, alias_api.gui.Menu, "
                    "or alias_api.Menu)."
                )
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
                "Restart Flow Production Tracking Client",
                self.engine.restart_process,
                parent=plugin_menu,
            )

        # Call the hook to get the engine commands in order.
        menu_commands = self.__menu_customization_hook_instance.sorted_menu_commands(
            self.engine.commands
        )

        # Convert command dictionaries to list of AppCommand objects
        menu_items = []
        for cmd_name, cmd_details in menu_commands:
            menu_items.append(AppCommand(cmd_name, cmd_details))

        # Add favourites in the order that they are defined in the config settings.
        add_separator = True
        for fav in self.engine.get_setting("menu_favourites", []):
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

        # Add the rest of the menu commands. Use an OrderedDict to ensure the ordering of menu
        # command is preservered (for Python < 3.7)
        commands_by_app = OrderedDict()
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

    def remove_menu(self):
        """Remove the Flow Production Tracking menu from Alias. The menu will be destroyed."""

        if not self.alias_menu:
            return self.engine.alias_py.AlStatusCode.InvalidObject
        if hasattr(self.alias_menu, "remove"):
            status = self.alias_menu.remove()
        else:
            status = self.clean_menu()
        self.__alias_menu = None
        return status

    def clean_menu(self):
        """Clean the Flow Production Tracking menu in Alias by removing all its entries."""

        return self.alias_menu.clean()

    def _add_context_menu(self):
        """
        Adds a context menu which displays the current context

        :return:  Context submenu adapter or handle for parent= wiring.
        """

        ctx = self.engine.context
        ctx_name = str(self.engine.context)

        # Create the submenu
        ctx_menu = self.alias_menu.add_menu(ctx_name)

        # Add the context submenu actions
        self.alias_menu.add_command(
            "Jump to Flow Production Tracking", self._jump_to_sg, parent=ctx_menu
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
        for app_name in commands_by_app:
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
        Jump to Flow Production Tracking, launch web browser
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

        for app_instance_name, app_instance_obj in engine.apps.items():
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

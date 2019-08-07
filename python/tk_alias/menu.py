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
Menu handling for Alias
"""

from collections import OrderedDict
import os
import sys
import uuid

from sgtk.platform.qt import QtGui
from sgtk.platform.qt import QtCore


class AliasMenu(object):
    """Alias menu handler."""

    def __init__(self, engine):
        """Initialize attributes."""
        # engine instance
        self._engine = engine

        self.logger = self._engine.logger
        self.raw_options = None
        self.options = None

    def create(self):
        self.options = []
        self.raw_options = []

        # fill raw_options
        self._collect()

        # create context submenu
        self._create_context_submenu()

        # create favourites options
        self._create_favourites_options()

        # create apps options
        self._create_apps_options()

    def _collect(self):
        """Browse configuration to set raw options."""
        self.raw_options = []

        for caption, data in self._engine.commands.items():
            short_name = data.get("properties").get("short_name")
            callback = data.get("callback")
            is_context_submenu_option = data.get("properties").get("type") == "context_menu"

            if not short_name:
                short_name = uuid.uuid4().hex

            callback_invoker, callback_invoker_name = self._build_callback_invoker(callback=callback,
                                                                                   short_name=short_name)
            if 'app' in data.get("properties"):
                app = data.get("properties").get("app")
                app_name = app.name
                app_display_name = app.display_name
            else:
                app_name = None
                app_display_name = None

            kwargs = dict(option_type="item",
                          option_id=short_name,
                          caption=caption,
                          callback_invoker_name=callback_invoker_name,
                          app_name=app_name,
                          app_display_name=app_display_name,
                          is_context_submenu_option=is_context_submenu_option)
            self.raw_options.append(MenuOption(**kwargs))

    def _build_callback_invoker(self, callback, short_name):
        """
        Creates a dynamic method inside this class.

        The dynamic method allows invoking the callback by its name.

        :param callback: function to be called when the method is invoked
        :param short_name: method name
        :return: the new method object
        """
        def callback_invoker():
            callback()

        callback_invoker_name = "invoke_{}".format(short_name)
        callback_invoker.__name__ = callback_invoker_name
        setattr(self, callback_invoker_name, callback_invoker)

        return callback_invoker, callback_invoker_name

    def _create_context_submenu(self):
        """Creates context submenu."""
        self.logger.debug("Creating context submenu")

        # filter raw options
        submenu_options = list(filter(lambda option: option.is_context_submenu_option, self.raw_options))

        # add Jump to Shotgun option
        kwargs = dict(option_id="jump_to_sg",
                      caption="Jump to Shotgun",
                      callback_invoker_name=self.jump_to_sg.__name__,
                      is_context_submenu_option=True)
        submenu_options.append(MenuOption(**kwargs))

        # add Jump to File System option
        kwargs = dict(option_id="jump_to_fs",
                      caption="Jump to File System",
                      callback_invoker_name=self.jump_to_fs.__name__,
                      is_context_submenu_option=True)
        submenu_options.append(MenuOption(**kwargs))

        # create submenu
        submenu = self._create_submenu(caption=self.context_name, submenu_options=submenu_options)

        # add to options
        self.options.append(submenu)

    def _create_favourites_options(self):
        """Creates favourites options."""
        favourites_options = []

        for favourite in self._engine.get_setting("menu_favourites"):
            app_instance = favourite["app_instance"]
            name = favourite["name"]

            # filter raw_options
            favourites_options += list(filter(
                lambda option: option.app_name == app_instance and option.caption == name, self.raw_options))

        # add to options
        if favourites_options:
            favourites_options[0].has_separator = True
            self.options += favourites_options

    def _create_apps_options(self):
        """Creates applications menu options."""
        favourites = [(favourite["app_instance"], favourite["name"])
                      for favourite in self._engine.get_setting("menu_favourites")]

        # filter raw_options
        filtered_raw_options = filter(lambda option: not option.is_context_submenu_option, self.raw_options)

        groups = OrderedDict()
        for option in filtered_raw_options:
            app_name = option.app_name

            if app_name not in groups:
                groups[app_name] = []

            groups[app_name].append(option)

        apps_options = []
        for app_name, options in groups.items():
            first_option = options[0]
            options_number = len(options)

            if options_number > 1:
                app_display_name = first_option.app_display_name
                apps_options.append(self._create_submenu(app_display_name, options))
            elif options_number == 1 and (first_option.app_name, first_option.caption) not in favourites:
                apps_options.append(first_option)

        self._sort_options(apps_options)

        if apps_options:
            apps_options[0].has_separator = True
            self.options += apps_options

    def _create_submenu(self, caption, submenu_options, sort_options=True, has_separator=False):
        """Creates submenu tuple."""
        if sort_options:
            self._sort_options(submenu_options)
        return MenuOption(option_type="submenu", caption=caption, options=submenu_options, has_separator=has_separator)

    @staticmethod
    def _sort_options(options_to_sort):
        """Sort options by caption."""
        options_to_sort.sort(key=lambda option: option.caption)

    @property
    def context_name(self):
        """Returns the context name used by the context submenu caption."""
        return str(self._engine.context).decode("utf-8")

    def jump_to_sg(self):
        """
        Jump to shotgun, launch web browser
        """
        url = self._engine.context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def jump_to_fs(self):
        """
        Jump from context to FS
        """
        # launch one window for each location on disk
        paths = self._engine.context.filesystem_locations

        for disk_location in paths:
            # get the setting
            system = sys.platform

            # run the app
            if system == "linux2":
                cmd = 'xdg-open "%s"' % disk_location
            elif system == "darwin":
                cmd = 'open "%s"' % disk_location
            elif system == "win32":
                cmd = 'cmd.exe /C start "Folder" "%s"' % disk_location
            else:
                raise Exception("Platform '%s' is not supported." % system)

            self._engine.logger.debug("Jump to filesystem command: {}".format(cmd))

            exit_code = os.system(cmd)
            if exit_code != 0:
                self._engine.logger.error("Failed to launch '%s'!", cmd)


class MenuOption(object):
    def __init__(self, **kwargs):
        self.option_type = kwargs.get("option_type", "item")
        self.caption = kwargs.get("caption", None)
        self.option_id = kwargs.get("option_id", None)
        self.callback_invoker_name = kwargs.get("callback_invoker_name", None)
        self.is_context_submenu_option = kwargs.get("is_context_submenu_option", None)
        self.app_name = kwargs.get("app_name", None)
        self.app_display_name = kwargs.get("app_display_name", None)
        self.options = kwargs.get("options", None)
        self.has_separator = kwargs.get("has_separator", False)

    def __str__(self):
        return self.as_string

    def __repr__(self):
        return self.as_string

    @property
    def as_string(self):
        if self.option_type == "item":
            return "<{}, {}, {}, {}>".format(self.option_type, self.caption, self.has_separator,
                                             self.callback_invoker_name)
        elif self.option_type == "submenu":
            return "<{}, {}, {}, [{}]>".format(self.option_type, self.caption, self.has_separator, self.options)

        return self.caption

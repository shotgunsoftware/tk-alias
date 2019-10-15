# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sgtk
import subprocess

HookBaseClass = sgtk.get_hook_baseclass()


class AliasTranslationPublishPlugin(HookBaseClass):
    """
    Plugin for publishing an open alias session.

    This hook relies on functionality found in the base file publisher hook in
    the publish2 app and should inherit from it in the configuration. The hook
    setting for this plugin should look something like this::

        hook: "{self}/publish_file.py:{engine}/tk-multi-publish2/basic/publish_session.py"

    """

    # NOTE: The plugin icon and name are defined by the base file plugin.

    @property
    def translator_settings(self):
        """
        Dictionary defining the translator settings that this plugin expects to access
        when finding translator data.
        """

        publisher = self.parent

        return {
            "wref": {
                "exec_path": os.path.join(
                    publisher.engine.alias_bindir,
                    "AlToRef.exe"
                ),
                "extra_parameters": []
            }
        }

    @property
    def description(self):
        """
        Verbose, multi-line description of what the plugin does. This can
        contain simple html for formatting.
        """

        loader_url = "https://support.shotgunsoftware.com/hc/en-us/articles/219033078"

        return """
        Publishes the file to Shotgun. A <b>Publish</b> entry will be
        created in Shotgun which will include a reference to the file's current
        path on disk. If a publish template is configured, a copy of the
        current session will be copied to the publish template path which
        will be the file that is published. Other users will be able to access
        the published file via the <b><a href='%s'>Loader</a></b> so long as
        they have access to the file's location on disk.
        
        <br><br><b color='red'>NOTE:</b> it's not possible to publish a WREF file 
        if you already have WREF files loaded in your current session. 
        """ % (loader_url,)

    @property
    def settings(self):
        """
        Dictionary defining the settings that this plugin expects to receive
        through the settings parameter in the accept, validate, publish and
        finalize methods.

        A dictionary on the following form::

            {
                "Settings Name": {
                    "type": "settings_type",
                    "default": "default_value",
                    "description": "One line description of the setting"
            }

        The type string should be one of the data types that toolkit accepts as
        part of its environment configuration.
        """

        # inherit the settings from the base publish plugin
        base_settings = super(AliasTranslationPublishPlugin, self).settings or {}

        # settings specific to this class
        alias_publish_settings = {
            "Publish Template": {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        # update the base settings
        base_settings.update(alias_publish_settings)

        return base_settings

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["alias.session"]

    def accept(self, settings, item):
        """
        Method called by the publisher to determine if an item is of any
        interest to this plugin. Only items matching the filters defined via the
        item_filters property will be presented to this method.

        A publish task will be generated for each item accepted here. Returns a
        dictionary with the following booleans:

            - accepted: Indicates if the plugin is interested in this value at
                all. Required.
            - enabled: If True, the plugin will be enabled in the UI, otherwise
                it will be disabled. Optional, True by default.
            - visible: If True, the plugin will be visible in the UI, otherwise
                it will be hidden. Optional, True by default.
            - checked: If True, the plugin will be checked in the UI, otherwise
                it will be unchecked. Optional, True by default.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process

        :returns: dictionary with boolean keys accepted, required and enabled
        """

        publisher = self.parent
        operations = publisher.engine.operations

        publish_template_setting = settings.get("Publish Template").value
        if publish_template_setting:

            # if a publish template is configured, disable context change. This
            # is a temporary measure until the publisher handles context switching
            # natively.
            item.context_change_allowed = False

            # get the publish template definition to determine if we are trying to publish a WREF file.
            # If so, disable the plugin if some references are loaded in the current session
            publish_template = publisher.engine.get_template_by_name(publish_template_setting)
            if publish_template and "wref" in publish_template.definition:
                alias_references = operations.get_references()
                if alias_references:
                    return {
                        "accepted": True,
                        "enabled": False,
                        "checked": False
                    }

        path = _session_path()

        if not path:
            # the session has not been saved before (no path determined).
            # provide a save button. the session will need to be saved before
            # validation will succeed.
            self.logger.warn(
                "The Alias session has not been saved.",
                extra=_get_save_as_action()
            )

        self.logger.info(
            "Alias '%s' plugin accepted the current Alias session." %
            (self.name,)
        )

        return {"accepted": True}

    def validate(self, settings, item):
        """
        Validates the given item to check that it is ok to publish. Returns a
        boolean to indicate validity.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        :returns: True if item is valid, False otherwise.
        """

        publisher = self.parent
        operations = publisher.engine.operations

        path = _session_path()

        # ---- ensure the session has been saved

        if not path:
            # the session still requires saving. provide a save button.
            # validation fails.
            error_msg = "The Alias session has not been saved."
            self.logger.error(
                error_msg,
                extra=_get_save_as_action()
            )
            raise Exception(error_msg)

        # ---- check the session against any attached work template

        # get the path in a normalized state. no trailing separator,
        # separators are appropriate for current os, no double separators,
        # etc.
        path = sgtk.util.ShotgunPath.normalize(path)

        # if the session item has a known work template, see if the path
        # matches. if not, warn the user and provide a way to save the file to
        # a different path
        work_template = item.properties.get("work_template")
        if not work_template or not work_template.validate(path):
            self.logger.warning(
                "The current session does not match the configured work "
                "file template.",
                extra={
                    "action_button": {
                        "label": "Save File",
                        "tooltip": "Save the current VRED session to a "
                                   "different file name",
                        # will launch wf2 if configured
                        "callback": _get_save_as_action()
                    }
                }
            )
            return False
        else:
            self.logger.debug(
                "Work template configured and matches session file.")

        # ---- populate the necessary properties and call base class validation

        # set the session path on the item for use by the base plugin validation
        # step. NOTE: this path could change prior to the publish phase.
        item.properties["path"] = path

        # if we don't have a publish path, we can't publish
        publish_path = self.get_publish_path(settings, item)
        if not publish_path:
            self.logger.warning(
                "Couldn't find a valid publish path for the translation file."
            )
            return False

        # if we don't have translator settings, we can't publish
        translation_type = self.get_translation_type(publish_path)
        if not translation_type:
            self.logger.warning(
                "Couldn't find the translation type."
            )
            return False

        translator_settings = self.translator_settings.get(translation_type)
        if not translator_settings:
            self.logger.warning(
                "Couldn't find translator settings."
            )
            return False

        return super(AliasTranslationPublishPlugin, self).validate(settings, item)

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        publisher = self.parent
        operations = publisher.engine.operations

        # get the path to create and publish
        publish_path = self.get_publish_path(settings, item)

        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)

        # get translation data in order to build the command line to export the translation
        translation_type = self.get_translation_type(publish_path)
        translator_settings = self.translator_settings.get(translation_type)

        # get alias info
        alias_info = operations.get_info()

        cmd = [
            translator_settings.get("exec_path"),
            "-productKey",
            alias_info.get("product_key"),
            "-productVersion",
            alias_info.get("product_version"),
            "-productLicenseType",
            alias_info.get("product_license_type"),
            "-productLicensePath",
            alias_info.get("product_license_path"),
            "-i",
            item.properties["path"],
            "-o",
            publish_path
        ]

        if translator_settings["extra_parameters"]:
            cmd.extend(translator_settings["extra_parameters"])

        try:
            self.logger.debug("Command for translation: {}".format(" ".join(cmd)))
            subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
        except Exception as e:
            self.logger.error("Failed to export translation: %s" % e)
            return

        super(AliasTranslationPublishPlugin, self).publish(settings, item)

    def get_publish_template(self, settings, item):
        """
        Get a publish template for the supplied settings and item.

        :param settings: This plugin instance's configured settings
        :param item: The item to determine the publish template for

        :return: A template representing the publish path of the item or
            None if no template could be identified.
        """

        publisher = self.parent

        # here we can't use the item.properties.publish_path value as it can store the current session publish template
        publish_template_setting = settings.get("Publish Template")
        publish_template = publisher.engine.get_template_by_name(
            publish_template_setting.value)

        return publish_template

    def get_publish_type(self, settings, item):
        """
        Get a publish type for the supplied settings and item.

        :param settings: This plugin instance's configured settings
        :param item: The item to determine the publish type for

        :return: A publish type or None if one could not be found.
        """

        publisher = self.parent

        # get the publish type from the publish path extension as the item will have the session publish type
        publish_path = self.get_publish_path(settings, item)

        path_info = publisher.util.get_file_path_components(publish_path)
        extension = path_info["extension"]

        if extension:
            publish_type = "%s File" % extension.capitalize()
        else:
            publish_type = "Folder"

        return publish_type

    def get_publish_name(self, settings, item):
        """
        Get the publish name for the supplied settings and item.

        :param settings: This plugin instance's configured settings
        :param item: The item to determine the publish name for

        Uses the path info hook to retrieve the publish name.
        """

        publisher = self.parent
        publish_path = self.get_publish_path(settings, item)

        return publisher.util.get_publish_name(
            publish_path,
            sequence=False
        )

    def get_translation_type(self, path):
        """
        Get the translation type according to the path extension

        :param path: The path to determine the translation type from

        :return: The translation type or None if the path extension is unknown.
        """

        publisher = self.parent
        operations = publisher.engine.operations

        path_info = publisher.util.get_file_path_components(path)
        extension = path_info["extension"]

        # ensure lowercase and no dot
        if extension:
            extension = extension.lstrip(".").lower()

        return extension


def _session_path():
    """
    Return the path to the current session
    :return:
    """

    engine = sgtk.platform.current_engine()
    operations = engine.operations

    return operations.get_current_path()


def _get_save_as_action():
    """
    Simple helper for returning a log action dict for saving the session
    """

    engine = sgtk.platform.current_engine()
    operations = engine.operations

    # default save callback
    callback = operations.open_save_as_dialog

    # if workfiles2 is configured, use that for file save
    if "tk-multi-workfiles2" in engine.apps:
        app = engine.apps["tk-multi-workfiles2"]
        if hasattr(app, "show_file_save_dlg"):
            callback = app.show_file_save_dlg

    return {
        "action_button": {
            "label": "Save As...",
            "tooltip": "Save the current session",
            "callback": callback
        }
    }

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
import alias_api

HookBaseClass = sgtk.get_hook_baseclass()


class AliasSessionPublishPlugin(HookBaseClass):
    """
    Plugin for publishing an open alias session.

    This hook relies on functionality found in the base file publisher hook in
    the publish2 app and should inherit from it in the configuration. The hook
    setting for this plugin should look something like this::

        hook: "{self}/publish_file.py:{engine}/tk-multi-publish2/basic/publish_session.py"

    """

    # Publish mode string constants
    PUBLISH_MODE_DEFAULT = "Default"
    PUBLISH_MODE_EXPORT_SELECTION = "Export Selection"

    # Publish mode options
    PUBLISH_MODE_OPTIONS = [
        PUBLISH_MODE_DEFAULT,
        PUBLISH_MODE_EXPORT_SELECTION,
    ]

    @property
    def description(self):
        """
        Verbose, multi-line description of what the plugin does. This can
        contain simple html for formatting.
        """

        loader_url = "https://help.autodesk.com/view/SGDEV/ENU/?contextId=PC_APP_LOADER"

        return """
        Publishes the file to Flow Production Tracking. A <b>Publish</b>
        entry will be created in Flow Production Tracking which will
        include a reference to the file's current path on disk. If a
        publish template is configured, a copy of the current session
        will be copied to the publish template path which will be the
        file that is published. Other users will be able to access the
        published file via the <b><a href='%s'>Loader</a></b> so long as
        they have access to the file's location on disk.

        If the session has not been saved, validation will fail and a button
        will be provided in the logging output to save the file.

        <h3>File versioning</h3>
        If the filename contains a version number, the process will bump the
        file to the next version after publishing.

        The <code>version</code> field of the resulting <b>Publish</b> in
        Flow Production Tracking will also reflect the version number identified
        in the filename. The basic worklfow recognizes the following version
        formats by default:

        <ul>
        <li><code>filename.v###.ext</code></li>
        <li><code>filename_v###.ext</code></li>
        <li><code>filename-v###.ext</code></li>
        </ul>

        After publishing, if a version number is detected in the work file, the
        work file will automatically be saved to the next incremental version
        number. For example, <code>filename.v001.ext</code> will be published
        and copied to <code>filename.v002.ext</code>

        If the next incremental version of the file already exists on disk, the
        validation step will produce a warning, and a button will be provided in
        the logging output which will allow saving the session to the next
        available version number prior to publishing.

        <br><br><i>NOTE: any amount of version number padding is supported. for
        non-template based workflows.</i>

        <h3>Overwriting an existing publish</h3>
        In non-template workflows, a file can be published multiple times,
        however only the most recent publish will be available to other users.
        Warnings will be provided during validation if there are previous
        publishes.
        """ % (
            loader_url,
        )

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
        base_settings = super().settings or {}

        # settings specific to this class
        alias_publish_settings = {
            "Publish Template": {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                "correspond to a template defined in "
                "templates.yml.",
            },
            "Publish Mode": {
                "type": "str",
                "default": self.PUBLISH_MODE_DEFAULT,
                "description": "The mode to use when publishing the session. User can choose between 'Default' and 'Export Selection'.",
            },
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

        # if a publish template is configured, disable context change. This
        # is a temporary measure until the publisher handles context switching
        # natively.
        if settings.get("Publish Template").value:
            item.context_change_allowed = False

        path = _session_path()

        if not path:
            # the session has not been saved before (no path determined).
            # provide a save button. the session will need to be saved before
            # validation will succeed.
            self.logger.warning(
                "The Alias session has not been saved.",
                extra=_get_save_as_action(),
            )

        self.logger.info(
            "Alias '%s' plugin accepted the current Alias session." % (self.name,)
        )
        return {"accepted": True, "checked": True}

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
        path = _session_path()

        # ---- ensure the valid publish mode
        publish_mode = settings.get("Publish Mode").value
        if publish_mode not in self.PUBLISH_MODE_OPTIONS:
            self.logger.error(f"Unsupported Publish Mode {publish_mode}")
            return False

        if publish_mode == self.PUBLISH_MODE_EXPORT_SELECTION:
            bg_processing = item.parent.get_property("bg_processing", False)
            if bg_processing:
                error_msg = "Export Selection mode is not supported with Background Publishing. Please change the Publish Mode or turn off Background Publishing."
                self.logger.error(error_msg)
                return False
            # Ensure the user has selected something to export. Use Alias API to
            # init the first pick item, and check that there is at least one
            # item selected.
            alias_api.first_pick_item()
            current_pick_item = alias_api.get_current_pick_item()
            if not current_pick_item:
                error_msg = "Nothing selected, please select the items you would like to include in the publish or switch the Publish Mode to 'Default'"
                self.logger.error(error_msg)
                return False

        # ---- ensure the session has been saved

        if not path:
            # the session still requires saving. provide a save button.
            # validation fails.
            error_msg = "The Alias session has not been saved."
            self.logger.error(
                error_msg,
                extra=_get_save_as_action(),
            )
            raise Exception(error_msg)

        # ---- check that references exist, display warning for invalid refs

        for reference in alias_api.get_references():
            ref_path = reference.path
            if not os.path.exists(ref_path):
                self.logger.warning(
                    "Reference path does not exist '{}'".format(ref_path)
                )

        # ---- check the session against any attached work template

        # get the path in a normalized state. no trailing separator,
        # separators are appropriate for current os, no double separators,
        # etc.
        path = sgtk.util.ShotgunPath.normalize(path)

        # if the session item has a known work template, see if the path
        # matches. if not, warn the user and provide a way to save the file to
        # a different path
        work_template = item.properties.get("work_template")
        if work_template:
            if not work_template.validate(path):
                error_msg = "The current session does not match the configured work file template."
                self.logger.warning(
                    error_msg,
                    extra={
                        "action_button": {
                            "label": "Save File",
                            "tooltip": "Save the current Alias session to a "
                            "different file name",
                            "callback": sgtk.platform.current_engine().open_save_as_dialog,
                        }
                    },
                )
                raise Exception(error_msg)
            else:
                self.logger.debug("Work template configured and matches session file.")
        else:
            self.logger.debug("No work template configured.")

        # ---- see if the version can be bumped post-publish

        # check to see if the next version of the work file already exists on
        # disk. if so, warn the user and provide the ability to jump to save
        # to that version now
        (next_version_path, version) = self._get_next_version_info(path, item)
        if next_version_path and os.path.exists(next_version_path):

            # determine the next available version_number. just keep asking for
            # the next one until we get one that doesn't exist.
            while os.path.exists(next_version_path):
                (next_version_path, version) = self._get_next_version_info(
                    next_version_path, item
                )

            error_msg = "The next version of this file already exists on disk."
            self.logger.error(
                error_msg,
                extra={
                    "action_button": {
                        "label": "Save to v%s" % (version,),
                        "tooltip": "Save to the next available version number, "
                        "v%s" % (version,),
                        "callback": lambda: publisher.engine.save_file_as(
                            next_version_path
                        ),
                    }
                },
            )
            raise Exception(error_msg)

        # ---- populate the necessary properties and call base class validation

        # populate the publish template on the item if found
        publish_template_setting = settings.get("Publish Template")
        publish_template = publisher.engine.get_template_by_name(
            publish_template_setting.value
        )
        if publish_template:
            item.properties["publish_template"] = publish_template

        # set the session path on the item for use by the base plugin validation
        # step. NOTE: this path could change prior to the publish phase.
        item.properties["path"] = path

        # run the base class validation
        return super().validate(settings, item)

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        # get the publish "mode" stored inside of the root item properties
        bg_processing = item.parent.properties.get("bg_processing", False)
        in_bg_process = item.parent.properties.get("in_bg_process", False)

        # get the path in a normalized state. no trailing separator, separators
        # are appropriate for current os, no double separators, etc.
        path = sgtk.util.ShotgunPath.normalize(_session_path())

        # ensure the session is saved
        # we need to do this action locally to be sure the background process could access the work file
        if not bg_processing or (bg_processing and not in_bg_process):
            # Save the working file before publishing
            self.parent.engine.save_file()

            # store the current session path in the root item properties
            # it will be used later in the background process to open the file before running the publishing actions
            if bg_processing and "session_path" not in item.parent.properties:
                item.parent.properties["session_path"] = path
                item.parent.properties["session_name"] = (
                    "Alias Session - {task_name}, {entity_type} {entity_name} - {file_name}".format(
                        task_name=item.context.task["name"],
                        entity_type=item.context.entity["type"],
                        entity_name=item.context.entity["name"],
                        file_name=os.path.basename(path),
                    )
                )

        # update the item with the saved session path
        item.properties["path"] = path

        if not bg_processing or (bg_processing and in_bg_process):

            # add dependencies for the base class to register when publishing
            item.properties["publish_dependencies"] = (
                _alias_find_additional_session_dependencies()
            )

            # let the base class register the publish
            super().publish(settings, item)

    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once all the publish
        tasks have completed, and can for example be used to version up files.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        # get the publish "mode" stored inside of the root item properties
        bg_processing = item.parent.properties.get("bg_processing", False)
        in_bg_process = item.parent.properties.get("in_bg_process", False)

        if not bg_processing or (bg_processing and in_bg_process):
            # do the base class finalization
            super().finalize(settings, item)

        # bump the session file to the next version
        if not bg_processing or (bg_processing and not in_bg_process):
            self._save_to_next_version(
                item.properties["path"], item, self.parent.engine.save_file_as
            )

    ############################################################################
    # Methods for creating/displaying custom plugin interface

    def create_settings_widget(self, parent, items=None):
        """
        Creates a Qt widget, for the supplied parent widget (a container widget
        on the right side of the publish UI).

        :param parent: The parent to use for the widget being created.
        :param items: A list of PublishItems the selected publish tasks are parented to.
        :return: A QtGui.QWidget or subclass that displays information about
            the plugin and/or editable widgets for modifying the plugin's
            settings.
        """

        # defer Qt-related imports
        from sgtk.platform.qt import QtGui

        # The main widget
        widget = QtGui.QWidget(parent)
        widget_layout = QtGui.QVBoxLayout()

        # The description widget
        description_groupbox = super().create_settings_widget(parent, items)

        # Add a combobox to edit the publish mode
        publish_mode_label = QtGui.QLabel("Publish Mode:")
        publish_mode_combobox = QtGui.QComboBox(widget)
        publish_mode_combobox.setAccessibleName("Publish mode selection dropdown")
        publish_mode_combobox.addItems(self.PUBLISH_MODE_OPTIONS)
        publish_mode_widget = QtGui.QWidget(widget)
        publish_mode_widget.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred
        )
        publish_mode_layout = QtGui.QHBoxLayout()
        publish_mode_layout.setContentsMargins(0, 0, 0, 0)
        publish_mode_layout.addWidget(publish_mode_label)
        publish_mode_layout.addWidget(publish_mode_combobox)
        publish_mode_layout.addStretch()
        publish_mode_widget.setLayout(publish_mode_layout)

        # Add all the minor widgets to the main widget
        widget_layout.addWidget(publish_mode_widget)
        widget_layout.addWidget(description_groupbox)
        widget.setLayout(widget_layout)

        # Set the widget property to store the combobox to access in get_ui_settings and set_ui_settings
        widget.setProperty("publish_mode_combobox", publish_mode_combobox)

        return widget

    def get_ui_settings(self, widget, items=None):
        """
        This method is required to be defined in order for the custom UI to show up in the app.

        Invoked by the Publisher when the selection changes. This method gathers the settings
        on the previously selected task, so that they can be later used to repopulate the
        custom UI if the task gets selected again. They will also be passed to the accept, validate,
        publish and finalize methods, so that the settings can be used to drive the publish process.

        The widget argument is the widget that was previously created by
        `create_settings_widget`.

        The method returns a dictionary, where the key is the name of a
        setting that should be updated and the value is the new value of that
        setting. Note that it is up to you how you want to store the UI's state as
        settings and you don't have to necessarily to return all the values from
        the UI. This is to allow the publisher to update a subset of settings
        when multiple tasks have been selected.

        Example::

            {
                 "setting_a": "/path/to/a/file"
            }

        :param widget: The widget that was created by `create_settings_widget`
        """

        ui_settings = {}

        # Get the Publish Mode settings value from the UI combobox
        publish_mode_combobox = widget.property("publish_mode_combobox")
        if publish_mode_combobox:
            mode_index = publish_mode_combobox.currentIndex()
            if 0 <= mode_index < len(self.PUBLISH_MODE_OPTIONS):
                ui_settings["Publish Mode"] = self.PUBLISH_MODE_OPTIONS[mode_index]
            else:
                self.logger.debug(f"Invalid Publish Mode index {mode_index}")

        return ui_settings

    def set_ui_settings(self, widget, settings, items=None):
        """
        This method is required to be defined in order for the custom UI to show up in the app.

        Allows the custom UI to populate its fields with the settings from the
        currently selected tasks.

        The widget is the widget created and returned by
        `create_settings_widget`.

        A list of settings dictionaries are supplied representing the current
        values of the settings for selected tasks. The settings dictionaries
        correspond to the dictionaries returned by the settings property of the
        hook.

        Example::

            settings = [
            {
                 "seeting_a": "/path/to/a/file"
                 "setting_b": False
            },
            {
                 "setting_a": "/path/to/a/file"
                 "setting_b": False
            }]

        The default values for the settings will be the ones specified in the
        environment file. Each task has its own copy of the settings.

        When invoked with multiple settings dictionaries, it is the
        responsibility of the custom UI to decide how to display the
        information. If you do not wish to implement the editing of multiple
        tasks at the same time, you can raise a ``NotImplementedError`` when
        there is more than one item in the list and the publisher will inform
        the user than only one task of that type can be edited at a time.

        :param widget: The widget that was created by `create_settings_widget`.
        :param settings: a list of dictionaries of settings for each selected
            task.
        :param items: A list of PublishItems the selected publish tasks are parented to.
        """

        if not settings:
            return

        if len(settings) > 1:
            raise NotImplementedError

        publish_mode_combobox = widget.property("publish_mode_combobox")
        if not publish_mode_combobox:
            self.logger.debug(
                "Failed to retrieve Publish Mode combobox to set custom UI"
            )
            return

        # Get the default setting for publish mode
        default_value = self.settings.get("Publish Mode", {}).get("default")

        # Get the publish mode value from the settings, and set the combobox accordingly
        publish_mode = settings[0].get("Publish Mode", default_value)
        try:
            publish_mode_index = max(self.PUBLISH_MODE_OPTIONS.index(publish_mode), 0)
        except ValueError:
            publish_mode_index = 0

        # Set the publish mode combobox
        current_version_index = publish_mode_combobox.currentIndex()
        if current_version_index == publish_mode_index:
            return  # Nothing to do

        publish_mode_combobox.setCurrentIndex(publish_mode_index)

    ############################################################################
    # protected methods

    def _copy_to_publish(self, settings, item):
        """
        Copy the item file to the publish location.

        :param settings: This plugin instance's configured settings.
        :param item: The item containing the file to copy.
        """

        publish_mode = settings.get("Publish Mode").value
        if publish_mode == self.PUBLISH_MODE_EXPORT_SELECTION:
            publish_path = self.get_publish_path(settings, item)
            self.parent.engine.alias_py.store_active(publish_path)
        else:
            super()._copy_to_publish(settings, item)


def _alias_find_additional_session_dependencies():
    """
    Find additional dependencies from the session
    """

    references = []
    for reference in alias_api.get_references():
        path = reference.path
        if path not in references and os.path.exists(path):
            references.append(path)

    return references


def _session_path():
    """
    Return the path to the current session
    :return:
    """

    return alias_api.get_current_path()


def _get_save_as_action():
    """Simple helper for returning a log action to show the "File Save As" dialog"""
    return {
        "action_button": {
            "label": "Save As...",
            "tooltip": "Save the current session",
            "callback": sgtk.platform.current_engine().open_save_as_dialog,
        }
    }

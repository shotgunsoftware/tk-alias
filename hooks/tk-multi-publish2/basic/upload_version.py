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
import shutil
import tempfile

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class UploadVersionPlugin(HookBaseClass):
    """
    Plugin for sending quicktimes and images to ShotGrid for review.
    """

    # Translation workers are responsible for performing the LMV translation.
    # 'local': a local translator will be used, determined based on file type and current engine
    # 'framework':  the tk-framework-lmv translator will be used (default)
    TRANSLATION_WORKER_LOCAL = "local"
    TRANSLATION_WORKER_FRAMEWORK = "framework"
    TRANSLATION_WORKERS = [TRANSLATION_WORKER_LOCAL, TRANSLATION_WORKER_FRAMEWORK]

    # Version Type string constants
    VERSION_TYPE_2D = "2D Version"
    VERSION_TYPE_3D = "3D Version"

    # Version Type Options
    VERSION_TYPE_OPTIONS = [
        VERSION_TYPE_2D,
        VERSION_TYPE_3D,
    ]

    # Descriptions for Version Types
    VERSION_TYPE_DESCRIPTIONS = {
        VERSION_TYPE_2D: """
                Create a Version in ShotGrid for Review.<br/><br/>
                A 2D Version (image or video representation of your file/scene) will be created in ShotGrid.
                This Version can then be reviewed via ShotGrid's many review apps.
            """,
        VERSION_TYPE_3D: """
                Create a Version in ShotGrid for Review.<br/><br/>
                A 3D Version (LMV translation of your file/scene's geometry) will be created in ShotGrid.
                This Version can then be reviewed via ShotGrid's many review apps.
            """,
    }

    @property
    def icon(self):
        """
        Path to an png icon on disk
        """

        return os.path.join(self.disk_location, os.pardir, "icons", "review.png")

    @property
    def settings(self):
        """
        Dictionary defining the settings that this plugin expects to recieve
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
        base_settings = super(UploadVersionPlugin, self).settings or {}

        # settings specific to this class
        upload_version_settings = {
            "Version Type": {
                "type": "str",
                "default": self.VERSION_TYPE_2D,
                "description": "Generate a {options} or {last_option} Version".format(
                    options=", ".join(self.VERSION_TYPE_OPTIONS[:-1]),
                    last_option=self.VERSION_TYPE_OPTIONS[-1],
                ),
            },
            "Upload": {
                "type": "bool",
                "default": False,
                "description": "Upload content to ShotGrid?",
            },
            "Translation Worker": {
                "type": "str",
                "default": self.TRANSLATION_WORKER_FRAMEWORK,
                "description": "Specify the worker to use to perform LMV translation.",
            },
        }

        # update the base settings
        base_settings.update(upload_version_settings)

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

        # Validate fails if the Version Type is not supported
        version_type = settings.get("Version Type").value
        if version_type not in self.VERSION_TYPE_OPTIONS:
            self.logger.error("Unsupported Version Type '{}'".format(version_type))
            return False

        # Check the site pref for 3D Review enabled. Provide warning messages if the user is
        # attempting to create a 3D Version but may not have 3D Review enabled on their site, but
        # do not block the user from publishing.
        if version_type == self.VERSION_TYPE_3D:
            is_3d_viewer_enabled = self._is_3d_viewer_enabled()
            if is_3d_viewer_enabled is None:
                self.logger.warning(
                    "Failed to check if 3D Review is enabled for your site."
                )
                self.logger.warning(
                    "Please contact Autodesk support to access your site preference for 3D Review or use the 2D Version publish option instead."
                )
            elif not is_3d_viewer_enabled:
                self.logger.warning("Your site does not have 3D Review enabled.")
                self.logger.warning(
                    "Please contact Autodesk support to have 3D Review enabled on your ShotGrid site or use the 2D Version publish option instead."
                )

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        if not framework_lmv:
            self.logger.error("Could not run LMV translation: missing ATF framework")
            return False

        translation_worker = settings.get("Translation Worker").value
        if translation_worker not in self.TRANSLATION_WORKERS:
            self.logger.error(
                "Unknown Translation Worker '{worker}'. Translation worker must be one of {workers}".format(
                    worker=translation_worker,
                    workers=", ".join(self.TRANSLATION_WORKERS),
                )
            )
            return False

        return True

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """

        # Get the publish "mode" stored inside of the root item properties
        bg_processing = item.parent.properties.get("bg_processing", False)
        in_bg_process = item.parent.properties.get("in_bg_process", False)

        if not bg_processing or (bg_processing and in_bg_process):

            publisher = self.parent
            path = item.properties["path"]

            # Be sure to strip the extension from the publish name
            path_components = publisher.util.get_file_path_components(path)
            filename = path_components["filename"]
            (publish_name, _) = os.path.splitext(filename)
            item.properties["publish_name"] = publish_name

            # Create the Version in ShotGrid
            super(UploadVersionPlugin, self).publish(settings, item)

            # Generate media content and upload to ShotGrid
            version_type = item.properties["sg_version_data"]["type"]
            version_id = item.properties["sg_version_data"]["id"]
            thumbnail_path = item.get_thumbnail_as_path()
            media_package_path = None
            media_version_type = settings.get("Version Type").value
            if media_version_type == self.VERSION_TYPE_3D:
                # Pass the thumbnail retrieved to override the LMV thumbnail, and ignore the
                # LMV thumbnail output
                use_framework_translator = (
                    settings.get("Translation Worker").value
                    == self.TRANSLATION_WORKER_FRAMEWORK
                )
                media_package_path, _, _ = self._translate_file_to_lmv(
                    item,
                    use_framework_translator=use_framework_translator,
                    thumbnail_path=thumbnail_path,
                )
                self.logger.info("Translated file to LMV")

            if media_package_path:
                # For 3D media, a media package path will be generated. Set the translation
                # type on the Version in order to view 3D media in ShotGrid Web.
                self.parent.shotgun.update(
                    entity_type=version_type,
                    entity_id=version_id,
                    data={"sg_translation_type": "LMV"},
                )
                self.logger.info("Set Version translation type to LMV")

            uploaded_movie_path = media_package_path or thumbnail_path
            if uploaded_movie_path:
                self.parent.shotgun.upload(
                    entity_type=version_type,
                    entity_id=version_id,
                    path=uploaded_movie_path,
                    field_name="sg_uploaded_movie",
                )
                self.logger.info(
                    f"Uploaded Version media from path {uploaded_movie_path}"
                )

            if thumbnail_path:
                self.parent.shotgun.upload_thumbnail(
                    entity_type=version_type,
                    entity_id=version_id,
                    path=thumbnail_path,
                )
                self.logger.info(
                    f"Uploaded Version thumbnail from path {thumbnail_path}"
                )

            # Remove the temporary directory or files created to generate media content
            self._cleanup_temp_files(media_package_path)

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
            super(UploadVersionPlugin, self).finalize(settings, item)

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
        from sgtk.platform.qt import QtCore, QtGui

        # The main widget
        widget = QtGui.QWidget(parent)
        widget_layout = QtGui.QVBoxLayout()

        # create a group box to display the description
        description_group_box = QtGui.QGroupBox(widget)
        description_group_box.setTitle("Description:")

        # Defer setting the description text, this will be updated when
        # the version type combobox value is changed
        description_label = QtGui.QLabel()
        description_label.setWordWrap(True)
        description_label.setOpenExternalLinks(True)
        description_label.setTextFormat(QtCore.Qt.RichText)

        # create the layout to use within the group box
        description_layout = QtGui.QVBoxLayout()
        description_layout.addWidget(description_label)
        description_layout.addStretch()
        description_group_box.setLayout(description_layout)

        # Add a combobox to edit the version type option
        version_type_combobox = QtGui.QComboBox(widget)
        version_type_combobox.setAccessibleName("Version type selection dropdown")
        version_type_combobox.addItems(self.VERSION_TYPE_OPTIONS)
        # Hook up the signal/slot to update the description according to the current version type
        version_type_combobox.currentIndexChanged.connect(
            lambda index: self._on_version_type_changed(
                version_type_combobox.currentText(), description_label
            )
        )

        # Add all the minor widgets to the main widget
        widget_layout.addWidget(description_group_box)
        widget_layout.addWidget(version_type_combobox)
        widget.setLayout(widget_layout)

        # Set the widget property to store the combobox to access in get_ui_settings and set_ui_settings
        widget.setProperty("description_label", description_label)
        widget.setProperty("version_type_combobox", version_type_combobox)

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

        # Get the Version Type settings value from the UI combobox
        version_type_combobox = widget.property("version_type_combobox")
        if version_type_combobox:
            version_type_index = version_type_combobox.currentIndex()
            # if version_type_index >= 0 and version_type_index < len(self.VERSION_TYPE_OPTIONS):
            if 0 <= version_type_index < len(self.VERSION_TYPE_OPTIONS):
                self.VERSION_TYPE_OPTIONS[version_type_index]
                ui_settings["Version Type"] = self.VERSION_TYPE_OPTIONS[
                    version_type_index
                ]
            else:
                self.logger.debug(
                    "Invalid Version Type index {}".format(version_type_index)
                )

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

        version_type_combobox = widget.property("version_type_combobox")
        if not version_type_combobox:
            self.logger.debug(
                "Failed to retrieve Version Type combobox to set custom UI"
            )
            return

        description_label = widget.property("description_label")
        if not description_label:
            self.logger.debug(
                "Failed to retrieve Version Type combobox to set custom UI"
            )

        # Get the default setting for version type
        default_value = self.settings.get("Version Type", {}).get(
            "default", self.VERSION_TYPE_OPTIONS[0]
        )

        # Get the version type value from the settings, and set the combobox accordingly
        version_type_value = settings[0].get("Version Type", default_value)
        version_type_index = max(self.VERSION_TYPE_OPTIONS.index(version_type_value), 0)
        # Set the version type combobox
        current_version_index = version_type_combobox.currentIndex()
        if current_version_index == version_type_index:
            # Combobox already has the correct verstion type - manually trigger the 'currentIndexChanged'
            # slot to update the description label based on the version
            self._on_version_type_changed(version_type_value, description_label)
        else:
            version_type_combobox.setCurrentIndex(version_type_index)

    def _on_version_type_changed(self, version_type, description_label):
        """
        Slot called when the Version Type combobox selector index changes.

        Update the description based on the current Version Type.

        :param version_type: The current Version Type.
        :type version_type: str
        :param description_label: The label widget to set the description on
        :type description_label: QLabel
        """

        if not description_label:
            return

        note = ""
        if version_type == self.VERSION_TYPE_3D:
            is_3d_viewer_enabled = self._is_3d_viewer_enabled()

            if is_3d_viewer_enabled is None:
                note = """
                    <br/><br/>
                    <b>NOTE:</b>
                    <br/>
                    <b>
                        Failed to check if 3D Review is enabled for your site.
                    <br/>
                        You may create a 3D Version for review, but if 3D Review is not enabled,
                        you will see an error message 'No web playable media available' when trying to open the Version with the Media viewer.
                    </b>
                    <br/><br/>
                    <b>
                        Please contact Autodesk support to access your site preference for 3D Review or use the 2D Version publish option instead.
                    </b>
                """
            elif not is_3d_viewer_enabled:
                note = """
                    <br/><br/>
                    <b>NOTE:</b>
                    <br/>
                    <b>
                       Your site does not have 3D Review enabled.
                        <br/>
                       You may create a 3D Version for review, but until your site has 3D Review enabled,
                       you will see an error message 'No web playable media available' when trying to open the Version with the Media viewer.
                    </b>
                    <br/><br/>
                    <b>
                        Please contact Autodesk support to have 3D Review enabled on your ShotGrid site or use the 2D Version publish option instead.
                    </b>
                """

        text = "{description}{note}".format(
            description=self.VERSION_TYPE_DESCRIPTIONS.get(
                version_type, self.description
            ),
            note=note,
        )
        description_label.setText(text)

    ############################################################################
    # Protected functions

    def _cleanup_temp_files(self, path, remove_from_root=True):
        """
        Remove any temporary directories or files from the given path.

        If `remove_from_root` is True, the top most level directory of the given path is
        used to remove all sub directories and files.        
        
        :param path: The file path to remove temporary files and/or directories from.
        :type path: str
        :param remove_from_root: True will remove directories and files from the top most level
            directory within the root temporary directory, else False will remove the single
            file or directory (and its children). Default is True.
        :type remove_from_root: bool
        """

        if path is None or not os.path.exists(path):
            return  # Cannot clean up a path that does not exist

        tempdir = tempfile.gettempdir()
        if os.path.commonpath([path, tempdir]) != tempdir:
            return  # Not a temporary directory or file

        if remove_from_root:
            # Get the top most level of the path that is inside the root temp dir
            relative_path = os.path.relpath(path, tempdir)
            path = os.path.normpath(
                os.path.join(
                    tempdir,
                    relative_path.split(os.path.sep)[0]
                )
            )

        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def _translate_file_to_lmv(self, item, use_framework_translator, thumbnail_path=None):
        """
        Translate the current Alias file as an LMV package in order to upload it to ShotGrid as a 3D Version

        :param item: Item to process
        :type item: PublishItem
        :param use_framework_translator: True will force the translator shipped with tk-framework-lmv to be used
        :type use_framework_translator: bool
        :param thumbnail_path: Optionally pass a thumbnail file path to override the LMV
            thumbnail (this thumbnail will be included in the LMV packaged zip file).
        :type thumbnail_path: str

        :returns:
            - The path to the LMV zip file
            - The path to the LMV thumbnail
            - The path to the temporary folder where the LMV files have been processed
        """

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        translator = framework_lmv.import_module("translator")

        file_name = str(item.properties["sg_version_data"]["id"])
        thumbnail_path = thumbnail_path or item.get_thumbnail_as_path()

        # Translate the file to LMV
        lmv_translator = translator.LMVTranslator(item.properties.path)
        lmv_translator.translate(use_framework_translator=use_framework_translator)

        # Package up the LMV files into a zip file
        package_path, lmv_thumbnail_path = lmv_translator.package(
            svf_file_name=file_name,
            thumbnail_path=thumbnail_path,
        )

        return package_path, lmv_thumbnail_path, lmv_translator.output_directory

    def _get_thumbnail_from_lmv(self, item, use_framework_translator):
        """
        Extract the thumbnail from the source file, using the LMV conversion

        :param item: Item to process
        :param use_framework_translator: True will force the translator shipped with tk-framework-lmv to be used
        :returns:
            - The path to the temporary folder where the LMV files have been processed
            - The path to the LMV thumbnail
        """

        framework_lmv = self.load_framework("tk-framework-lmv_v0.x.x")
        translator = framework_lmv.import_module("translator")

        # translate the file to lmv
        lmv_translator = translator.LMVTranslator(item.properties.path)
        self.logger.info("Converting file to LMV")
        lmv_translator.translate(use_framework_translator=use_framework_translator)

        self.logger.info("Extracting thumbnails from LMV")
        thumbnail_path = lmv_translator.extract_thumbnail()
        if not thumbnail_path:
            self.logger.warning(
                "Couldn't retrieve thumbnail data from LMV. Version won't have any associated media"
            )
            return lmv_translator.output_directory

        return lmv_translator.output_directory, thumbnail_path

    def _is_3d_viewer_enabled(self):
        """
        Look up the ShotGrid site preference to check if the 3D Viewer is enabled. Return True
        if the 3D Viewer is enabled, False if it is disabled, or None if the 3D Viewer Enabled
        site pref could not be accessed.

        If the ShotGrid API returns an empty dictionary, the hidden site preference could not be
        accessed. Ensure that the hidden site preference "API hidden allowed list of preferences"
        contains the "enable_3d_viewer" in its list.

        :return: True if the 3D Viewer is enabled for the ShotGrid site, False if it is disabled,
                 or None if the 3D Viewer site pref could not be accessed.
        :rtype: bool
        """

        enable_3d_viewer_pref = "enable_3d_viewer"
        prefs = self.parent.shotgun.preferences_read(prefs=[enable_3d_viewer_pref])

        if not prefs:
            # The 'enable_3d_viewer' site pref could not be accessed
            return None

        return prefs[enable_3d_viewer_pref]

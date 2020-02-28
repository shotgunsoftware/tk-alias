# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import tempfile
import uuid

import sgtk
from sgtk.platform.qt import QtGui

import alias_api


class AliasOperations(object):
    OPEN_FILE_TARGET_NEW_SCENE = 0
    OPEN_FILE_TARGET_NEW_STAGE = 1
    OPEN_FILE_TARGET_CURRENT_STAGE = 2

    def __init__(self, engine):
        """Initialize attributes."""
        self._engine = engine
        self.logger = self._engine.logger

    def get_current_path(self):
        """Get current opened file path."""
        self.logger.debug("Getting current path")
        current_path = alias_api.get_current_path()
        self.logger.debug("Result: {}".format(current_path))

        return current_path

    def save_file(self, path):
        """Save file"""
        self.logger.debug("Saving file: {}".format(path))

        is_new = path != self.get_current_path()

        if is_new:
            self.current_file_closed()

        ctx = self._engine.context
        success, message = alias_api.save_file(path)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            raise Exception("Error saving the file {}".format(path))

        self._engine.save_context_for_path(path=path, ctx=ctx)
        self._engine.save_context_for_stage_name(ctx=ctx)

        if is_new:
            self._engine.execute_hook_method(
                "file_usage_hook", "file_attempt_open", path=path
            )

    def open_file(self, path, target=None):
        """Open a file in the scene."""
        self.logger.debug("Opening file {}".format(path))

        # Check if the file is locked
        if not self.can_open_file(path):
            self.logger.debug("Open file aborted because the file is locked")
            return

        if not target:
            target = self.OPEN_FILE_TARGET_NEW_SCENE

            # Scene is empty: open the file in the current stage
            if self.is_pristine():
                target = self.OPEN_FILE_TARGET_CURRENT_STAGE
            else:
                self.logger.debug(
                    "Asking user for deleting the scene or creating a new stage"
                )
                answer = self._can_delete_current_objects()

                if answer == QtGui.QMessageBox.Cancel:
                    self.logger.debug("Open file aborted by the user")
                    return

                if answer == QtGui.QMessageBox.No:
                    target = self.OPEN_FILE_TARGET_NEW_STAGE

            if target == self.OPEN_FILE_TARGET_NEW_SCENE:
                self.current_file_closed()

        ctx = self._engine.context
        success, message = alias_api.open_file(path, target)
        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            raise Exception("Error opening the file {}".format(path))

        self._engine.save_context_for_path(path=path, ctx=ctx)
        self._engine.save_context_for_stage_name(ctx=ctx)

    def open_save_as_dialog(self):
        """
        Launch a Qt file browser to select a file, then save the supplied
        project to that path.
        """
        # Alias doesn't appear to have a "save as" dialog accessible via
        # python. so open our own Qt file dialog.
        file_dialog = QtGui.QFileDialog(
            parent=self.get_parent_window(),
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
            self.save_file(path)

    def reset(self):
        """Reset the current scene."""
        self.logger.debug("Resetting the scene")

        self.current_file_closed()

        success, message = alias_api.reset()

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            raise Exception("Error resetting the scene")

    @staticmethod
    def get_parent_window():
        """Return current active window as parent"""
        return QtGui.QApplication.activeWindow()

    def current_file_closed(self):
        """This method should be called when the current file is closed."""
        path = self.get_current_path()
        if not path:
            return

        self.logger.debug(
            "current_file_closed: notifying the file usage hook that the current file has closed"
        )
        self._engine.execute_hook_method("file_usage_hook", "file_closed", path=path)

    def can_open_file(self, path):
        """Check if file can be opened."""
        self.logger.debug("Check availability of {}".format(path))

        return self._engine.execute_hook_method(
            "file_usage_hook", "file_attempt_open", path=path
        )

    def _can_delete_current_objects(self):
        """Confirm if can delete objects."""
        message = "DELETE all objects, shaders, views and actions in all existing Stage before Opening this File?"
        message_type = (
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
        )
        answer = QtGui.QMessageBox.question(
            self.get_parent_window(), "Open", message, message_type
        )

        return answer

    def want_to_delete_current_objects(self):
        """Confirm if can delete objects."""
        message = (
            "DELETE all objects, shaders, views and actions in all existing Stages before Opening a New "
            "File?"
        )
        message_type = (
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
        )
        answer = QtGui.QMessageBox.question(
            self.get_parent_window(), "Open", message, message_type
        )

        return answer == QtGui.QMessageBox.Yes

    def create_reference(self, path, standalone=True):
        """Load a file inside the scene as a reference."""
        self.logger.debug("Creating a reference to {}".format(path))

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        success, message = alias_api.create_reference(path)
        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(
                message_type=message_type,
                message_code=message,
                publish_path=path,
                is_error=False if success else True,
            )

        if not success:
            raise Exception("Error creating the reference")

        QtGui.QMessageBox.information(
            self.get_parent_window(), "Reference File", "File referenced successfully."
        )

    def import_file(self, path, create_stage=False, standalone=True):
        """Import a file into the current scene."""
        self.logger.debug(
            "Importing the file {}, and the create stage: {}".format(path, create_stage)
        )

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        if create_stage:
            success, message = alias_api.open_file(
                path, self.OPEN_FILE_TARGET_NEW_STAGE
            )
        else:
            success, message = alias_api.import_file(path)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(
                message_type=message_type,
                message_code=message,
                publish_path=path,
                is_error=False if success else True,
            )

        if not success:
            raise Exception("Error import the file")

        QtGui.QMessageBox.information(
            self.get_parent_window(), "Import File", "File imported successfully."
        )

    def create_texture_node(self, path, standalone=True):
        """Create a texture node."""
        self.logger.debug("Creating a texture node of {}".format(path))

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        success, message = alias_api.create_texture_node(path)
        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(
                message_type=message_type,
                message_code=message,
                publish_path=path,
                is_error=False if success else True,
            )

        if not success:
            raise Exception("Error creating a texture node")

        QtGui.QMessageBox.information(
            self.get_parent_window(),
            "Texture Node",
            "Texture node created successfully.",
        )

    def get_references(self):
        """Get references."""
        self.logger.debug("Getting references")

        COL_SEPARATOR = "COLSEP"
        ROW_SEPARATOR = "ROWSEP"
        references_string = alias_api.get_references()
        references = []

        self.logger.debug("Received: {}".format(references_string))

        for row in references_string.split(ROW_SEPARATOR):
            if not row or COL_SEPARATOR not in row:
                continue

            name, path = row.split(COL_SEPARATOR)

            references.append(
                {
                    "node": name,
                    "type": "reference",
                    "path": path.replace("/", os.path.sep),
                }
            )

        self.logger.debug("Sending: {}".format(references))

        return references

    def update_scene(self, items):
        """Get references."""
        self.logger.debug("Updating scene {}".format(items))

        if not items:
            self.logger.debug("No items to update")
            return

        success, message = alias_api.update_scene(items)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            msg = (
                "One or more selected items cannot be updated.\nIf there is another version of this file "
                "referenced, please check the Alias Reference Manager and remove its reference to enable the update."
            )
            raise Exception(msg)

    def get_info(self):
        """
        Get info.

        :returns: Dict with keys version_number, product_version, product_key, product_license_type,
                                 product_license_path, product_name
        """
        self.logger.debug("Getting info")

        info = alias_api.get_info()

        self.logger.debug("Result: {}".format(info))

        return info

    def get_annotations(self):
        """Export annotations."""
        self.logger.debug("Getting annotations")

        annotations = alias_api.get_annotations()

        self.logger.debug("Result: {}".format(annotations))

        return annotations

    def get_variants(self):
        """
        Get variants list.

        Returns a list of tuples composed by (name, path) or an empty list.
        """
        self.logger.debug("Getting variants")
        success, variants = alias_api.get_variants(
            tempfile.gettempdir(), uuid.uuid4().hex
        )
        self.logger.debug("Result: {}, Message: {}".format(success, variants))

        if not success:
            raise Exception("Error getting variants")

        normalized_variants = [
            (name, sgtk.util.ShotgunPath.normalize(path)) for name, path in variants
        ]

        return normalized_variants

    def has_variants(self):
        """
        Check if there are variants created in the scene.

        Returns True or False.
        """
        self.logger.debug("Checking if there are variants")

        return alias_api.has_variants()

    def get_stages_number(self):
        """Get stages number."""
        self.logger.debug("Getting stages number")
        stages_number = alias_api.get_stages_number()
        self.logger.debug("Result: {}".format(stages_number))

        return stages_number

    def get_current_stage(self):
        """Get current stage name."""
        return alias_api.get_current_stage()

    def is_pristine(self):
        """Check the scene if it's pristine"""
        stages_number = self.get_stages_number()
        current_stage = self.get_current_stage()
        return stages_number == 1 and current_stage == "Stage"

    def import_subdiv(self, path, standalone=True):
        """Import a subdiv file into the current scene."""
        self.logger.debug("Importing subdiv file {}".format(path))

        if not alias_api.is_subdiv_supported():
            QtGui.QMessageBox.information(
                self.get_parent_window(),
                "Import Subdiv",
                "Subdiv import is not supported in this version of Alias.",
            )
            return

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        success, message = alias_api.import_subdiv(path)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(
                message_type=message_type,
                message_code=message,
                publish_path=path,
                is_error=False if success else True,
            )

        if not success:
            raise Exception("Error importing subdiv file")

        QtGui.QMessageBox.information(
            self.get_parent_window(),
            "Import Subdiv",
            "Subdiv File imported successfully.",
        )

    def is_subdiv_supported(self):
        return alias_api.is_subdiv_supported()

    def create_stage(self, name=None):
        """Creates an empty stage."""
        if not name:
            name = uuid.uuid4().hex
        return alias_api.create_stage(name)

    def get_import_as_reference_output_path(self, source_path):
        """
        Returns an output path form importing a file (wire, jt, CATPart, ...) as a reference (wref) in the scenes.

        It tries to calculate the path using the setting `reference_template`,  if there's not a template defined it
        uses the source path to get the folder and returns it.

        source_path: It's a filesystem path. The file name has the form {name}.{version}.{extension}
                     Ex. C:\myproject\assets\Vehicle\myasset\CSA\publish\alias\scene.v002.wire
        """
        # get the setting reference_template
        template_name = self._engine.get_setting("reference_template")

        # scene.v002.wire
        base_name = os.path.basename(source_path)

        # scene.v002, .wire
        base_file_name, base_file_extension = os.path.splitext(base_name)

        # scene, v002, wire, 2
        name, version = base_file_name.split(".")
        extension = base_file_extension[1:]  # .wire => wire
        version_number = int(version[1:])  # v002 => 2

        # scene_wire.v002.wref
        output_file_name = "{name}_{extension}.{version}.wref".format(name=name, extension=extension, version=version)

        if not template_name:
            # if none template was defined by the user, use the container's folder of the source path
            parent_path = os.path.dirname(source_path)
            output_path = os.path.join(parent_path, output_file_name)
        else:
            # if template exists, try to get the output path joining the parts required
            template = self._engine.get_template_by_name(template_name)
            fields = self._engine.context.as_template_fields(template, validate=True)
            missing_keys = template.missing_keys(fields)

            if "version" in missing_keys:
                fields["version"] = version_number
                missing_keys.remove("version")

            if "name" in missing_keys:
                fields["name"] = name
                missing_keys.remove("name")

            if "alias.extension" in missing_keys:
                fields["alias.extension"] = extension
                missing_keys.remove("alias.extension")

            if missing_keys:
                raise Exception("Not enough keys to apply publish fields (%s) "
                                "to publish template (%s)" % (fields, template))

            output_path = template.apply_fields(fields)

        return output_path

    def get_publish_version(self, settings, item):
        """
        Get the publish version for the supplied settings and item.

        :param settings: This plugin instance's configured settings
        :param item: The item to determine the publish version for

        Extracts the publish version via the configured work template if
        possible. Will fall back to using the path info hook.
        """
        publish_version = item.get_property("publish_version")
        if publish_version:
            return publish_version

        # fall back to the template/path_info logic
        publisher = self.parent
        path = item.properties.path

        self.logger.debug("Using path info hook to determine publish version.")
        publish_version = publisher.util.get_version_number(path)
        if publish_version is None:
            publish_version = 1

        return publish_version

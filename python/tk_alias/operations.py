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

        success, message = alias_api.save_file(path)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            raise Exception("Error saving the file {}".format(path))

        if is_new:
            self._engine.execute_hook_method("file_usage_hook", "file_attempt_open", path=path)

    def open_file(self, path):
        """Open a file in the scene."""
        self.logger.debug("Opening file {}".format(path))

        # Check if the file is locked
        if not self.can_open_file(path):
            self.logger.debug("Open file aborted because the file is locked")
            return

        target = self.OPEN_FILE_TARGET_NEW_SCENE

        # Scene is empty: open the file in the current stage
        if self.is_pristine():
            target = self.OPEN_FILE_TARGET_CURRENT_STAGE
        else:
            self.logger.debug("Asking user for deleting the scene or creating a new stage")
            answer = self._can_delete_current_objects()

            if answer == QtGui.QMessageBox.Cancel:
                self.logger.debug("Open file aborted by the user")
                return

            if answer == QtGui.QMessageBox.No:
                target = self.OPEN_FILE_TARGET_NEW_STAGE

        if target == self.OPEN_FILE_TARGET_NEW_SCENE:
            self.current_file_closed()

        success, message = alias_api.open_file(path, target)
        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not success:
            raise Exception("Error opening the file {}".format(path))

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
            filter="Alias file (*.wire)"
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

        self.logger.debug("current_file_closed: notifying the file usage hook that the current file has closed")
        self._engine.execute_hook_method("file_usage_hook", "file_closed", path=path)

    def can_open_file(self, path):
        """Check if file can be opened."""
        self.logger.debug("Check availability of {}".format(path))

        return self._engine.execute_hook_method("file_usage_hook", "file_attempt_open", path=path)

    def _can_delete_current_objects(self):
        """Confirm if can delete objects."""
        message = "DELETE all objects, shaders, views and actions in all existing Stage before Opening this File?"
        message_type = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
        answer = QtGui.QMessageBox.question(self.get_parent_window(), "Open", message, message_type)

        return answer

    def want_to_delete_current_objects(self):
        """Confirm if can delete objects."""
        message = "DELETE all objects, shaders, views and actions in all existing Stages before Opening a New " \
                  "File?"
        message_type = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
        answer = QtGui.QMessageBox.question(self.get_parent_window(), "Open", message, message_type)

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
            return dict(message_type=message_type, message_code=message, publish_path=path,
                        is_error=False if success else True)

        if not success:
            raise Exception("Error creating the reference")

        QtGui.QMessageBox.information(self.get_parent_window(), "Reference File", "File referenced successfully.")

    def import_file(self, path, create_stage=False, standalone=True):
        """Import a file into the current scene."""
        self.logger.debug("Importing the file {}, and the create stage: {}".format(path, create_stage))

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        if create_stage:
            success, message = alias_api.open_file_as_new_stage(path)
        else:
            success, message = alias_api.import_file(path)

        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(message_type=message_type, message_code=message, publish_path=path,
                        is_error=False if success else True)

        if not success:
            raise Exception("Error import the file")

        QtGui.QMessageBox.information(self.get_parent_window(), "Import File", "File imported successfully.")

    def create_texture_node(self, path, standalone=True):
        """Create a texture node."""
        self.logger.debug("Creating a texture node of {}".format(path))

        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)

        success, message = alias_api.create_texture_node(path)
        self.logger.debug("Result: {}, Message: {}".format(success, message))

        if not standalone:
            message_type = "information" if success else "warning"
            return dict(message_type=message_type, message_code=message, publish_path=path,
                        is_error=False if success else True)

        if not success:
            raise Exception("Error creating a texture node")

        QtGui.QMessageBox.information(self.get_parent_window(), "Texture Node", "Texture node created successfully.")

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

            references.append({
                "node": name,
                "type": "reference",
                "path": path.replace("/", os.path.sep)
            })

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
            msg = "One or more selected items cannot be updated.\nIf there is another version of this file " \
                  "referenced, please check the Alias Reference Manager and remove its reference to enable the update."
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
        """Export variants."""
        self.logger.debug("Getting variants")
        success, variants = alias_api.get_variants(tempfile.gettempdir(), uuid.uuid4().hex)
        self.logger.debug("Result: {}, Message: {}".format(success, variants))

        return variants

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
        return self.get_stages_number() == 1 and self.get_current_stage() == "Stage"

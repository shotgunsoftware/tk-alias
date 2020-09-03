# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import alias_api

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    """
    Hook called to perform an operation with the
    current file
    """

    def execute(self, operation, file_path, **kwargs):
        """
        Main hook entry point

        :operation: String
                    Scene operation to perform

        :file_path: String
                    File path to use if the operation
                    requires it (e.g. open)

        :returns:   Depends on operation:
                    'current_path' - Return the current scene
                                     file path as a String
                    all others     - None
        """

        self.parent.engine._stop_watching = True

        try:

            if operation == "current_path":
                return alias_api.get_current_path()

            elif operation == "open":
                open_in_current_stage = self.parent.engine.open_delete_stages_dialog()
                if open_in_current_stage == QtGui.QMessageBox.Cancel:
                    return
                elif open_in_current_stage == QtGui.QMessageBox.No:
                    alias_api.open_file(file_path, new_stage=False, delete_current=True)
                else:
                    alias_api.reset()
                    alias_api.open_file(file_path, new_stage=False)

            elif operation == "save":
                alias_api.save_file()

        finally:
            self.parent.engine._stop_watching = False
            if operation in ["open", "save"]:
                self.parent.engine.save_context_for_stage()

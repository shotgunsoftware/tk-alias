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
import uuid

import sgtk
from sgtk.platform.qt import QtGui

HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    """
    Hook called to perform an operation with the
    current file
    """

    def execute(
        self,
        operation,
        file_path,
        context=None,
        parent_action=None,
        file_version=None,
        read_only=None,
        **kwargs
    ):
        """
        Main hook entry point

        :param operation:       String
                                Scene operation to perform

        :param file_path:       String
                                File path to use if the operation
                                requires it (e.g. open)

        :param context:         Context
                                The context the file operation is being
                                performed in.

        :param parent_action:   This is the action that this scene operation is
                                being executed for.  This can be one of:
                                - open_file
                                - new_file
                                - save_file_as
                                - version_up

        :param file_version:    The version/revision of the file to be opened.  If this is 'None'
                                then the latest version should be opened.

        :param read_only:       Specifies if the file should be opened read-only or not

        :returns:               Depends on operation:
                                'current_path' - Return the current scene
                                                 file path as a String
                                'reset'        - True if scene was reset to an empty
                                                 state, otherwise False
                                all others     - None
        """

        self.parent.engine._stop_watching = True

        try:

            if operation == "current_path":
                return alias_api.get_current_path()

            elif operation == "open":
                # if the current file is an empty file, we can erase it and open the new file instead
                if alias_api.is_empty_file():
                    alias_api.open_file(file_path, new_stage=False)
                # otherwise, ask the use what he'd like to do
                else:
                    open_in_current_stage = (
                        self.parent.engine.open_delete_stages_dialog()
                    )
                    if open_in_current_stage == QtGui.QMessageBox.Cancel:
                        return
                    elif open_in_current_stage == QtGui.QMessageBox.No:
                        alias_api.open_file(file_path, new_stage=True)
                    else:
                        alias_api.reset()
                        alias_api.open_file(file_path, new_stage=False)

            elif operation == "save":
                alias_api.save_file()

            elif operation == "save_as":
                alias_api.save_file_as(file_path)

            elif operation == "reset":
                # do not reset the file if we try to open another one as we have to deal with the stages an resetting
                # the current session will delete all the stages
                if parent_action == "open_file":
                    return True
                if alias_api.is_empty_file() and len(alias_api.get_stages()) == 1:
                    alias_api.reset()
                    return True
                else:
                    open_in_current_stage = self.parent.engine.open_delete_stages_dialog(
                        new_file=True
                    )
                    if open_in_current_stage == QtGui.QMessageBox.Cancel:
                        return False
                    elif open_in_current_stage == QtGui.QMessageBox.No:
                        stage_name = uuid.uuid4().hex
                        alias_api.create_stage(stage_name)
                    else:
                        alias_api.reset()
                    return True

        finally:

            self.parent.engine._stop_watching = False
            if operation in ["save_as", "prepare_new", "open"]:
                self.parent.engine.save_context_for_stage(context)

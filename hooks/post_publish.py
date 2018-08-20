# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from tank import Hook
from tank import TankError


class PostPublishHook(Hook):
    """
    Hook that implements post-publish functionality
    """

    def execute(self, work_template, primary_task, secondary_tasks, progress_cb,
                user_data, **kwargs):
        """
        Main hook entry point

        :param work_template:   template
                                This is the template defined in the config that
                                represents the current work file

        :param primary_task:    The primary task that was published by the primary publish hook.  Passed
                                in here for reference.

        :param secondary_tasks: The list of secondary tasks that were published by the secondary
                                publish hook.  Passed in here for reference.

        :param progress_cb:     Function
                                A progress callback to log progress during pre-publish.  Call:

                                    progress_cb(percentage, msg)

                                to report progress to the UI

        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.

        :returns:               None
        :raises:                Raise a TankError to notify the user of a problem
        """

        """
             push to PDM, TC in this case
        """

        self.parent.engine.log_info("Starting post publish")
        self.parent.engine.log_info("Will send the file to TeamCenter")

        # import maya.cmds as cmds

        progress_cb(0, "Versioning up the scene file")

        # get the current scene path:
        scene_path = self.parent.engine.get_current_file()

        # increment version and construct new file name:
        progress_cb(25, "Finding next version number")
        fields = work_template.get_fields(scene_path)
        next_version = self._get_next_work_file_version(work_template, fields)
        fields["version"] = next_version
        new_scene_path = work_template.apply_fields(fields)

        # log info
        self.parent.log_debug("Version up work file %s --> %s..." % (scene_path, new_scene_path))

        # rename and save the file
        progress_cb(50, "Saving the scene file")
        self.parent.engine.save_file(new_scene_path)

        progress_cb(100)

        return None

    def _get_next_work_file_version(self, work_template, fields):
        """
        Find the next available version for the specified work_template and fields.
        """
        existing_versions = self.parent.tank.paths_from_template(work_template, fields, ["version"])
        version_numbers = [work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        return max(curr_v_no, max_v_no) + 1

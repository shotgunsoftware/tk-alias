# Copyright (c) 2013 Shotgun Software Inc.
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

import tank
from tank import Hook
from tank import TankError
from os.path import isfile,basename,dirname,splitext
from os import remove
from subprocess import check_call,CalledProcessError
from collections import namedtuple


class PublishHook(Hook):
    """
    Single hook that implements publish functionality for secondary tasks
    """
    def execute(
        self, tasks, work_template, comment, thumbnail_path, sg_task, primary_task,
        primary_publish_path, progress_cb, user_data, **kwargs):
        """
        Main hook entry point
        :param tasks:                   List of secondary tasks to be published.  Each task is a
                                        dictionary containing the following keys:
                                        {
                                            item:   Dictionary
                                                    This is the item returned by the scan hook
                                                    {
                                                        name:           String
                                                        description:    String
                                                        type:           String
                                                        other_params:   Dictionary
                                                    }

                                            output: Dictionary
                                                    This is the output as defined in the configuration - the
                                                    primary output will always be named 'primary'
                                                    {
                                                        name:             String
                                                        publish_template: template
                                                        tank_type:        String
                                                    }
                                        }

        :param work_template:           template
                                        This is the template defined in the config that
                                        represents the current work file

        :param comment:                 String
                                        The comment provided for the publish

        :param thumbnail:               Path string
                                        The default thumbnail provided for the publish

        :param sg_task:                 Dictionary (shotgun entity description)
                                        The shotgun task to use for the publish

        :param primary_publish_path:    Path string
                                        This is the path of the primary published file as returned
                                        by the primary publish hook

        :param progress_cb:             Function
                                        A progress callback to log progress during pre-publish.  Call:

                                            progress_cb(percentage, msg)

                                        to report progress to the UI

        :param primary_task:            The primary task that was published by the primary publish hook.  Passed
                                        in here for reference.  This is a dictionary in the same format as the
                                        secondary tasks above.

        :param user_data:               A dictionary containing any data shared by other hooks run prior to
                                        this hook. Additional data may be added to this dictionary that will
                                        then be accessible from user_data in any hooks run after this one.

        :returns:                       A list of any tasks that had problems that need to be reported
                                        in the UI.  Each item in the list should be a dictionary containing
                                        the following keys:
                                        {
                                            task:   Dictionary
                                                    This is the task that was passed into the hook and
                                                    should not be modified
                                                    {
                                                        item:...
                                                        output:...
                                                    }

                                            errors: List
                                                    A list of error messages (strings) to report
                                        }
        """
        self.parent.engine.log_info("Starting secondary publish")

        self._primary_created_version = sg_task.pop("primary_created_version", None)

        # Setup Data Objects
        app = self.parent
        engine = tank.platform.current_engine()

        translator_data_reference = app.get_setting("translator_data_reference")
        if not translator_data_reference:
            raise TankError("Configuration Error: Check translator_data_reference in app configuration.")
        
        # Get and verify data needed for translators.
        # Note: Check if the translator info exists but only if there are translation tasks to be one.
        # If there are tasks to be done and no translator info exists then throw an exception.
        # If there are no tasks then just exit early. 
        if "translator_info" not in translator_data_reference.keys():
            if len(tasks) > 0:
                raise TankError("Configuration Error: Check translator_info exists in app_launchers for alias.")
            else:
                return []
            
        main_translator_info = translator_data_reference["translator_info"]

        self.verify_core_translator_info(main_translator_info)
        
        # Initalize the return Task Data List
        return_task_data = []

        exported_variants = None

        # Translate Files Here
        # Each task should be a file to be translated.
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors_list = []

            # report progress:
            progress_cb(0, "Publishing", task)

            # Fake Version Creation
            if output["name"] == "quickreview":
                try:
                    self.__publish_quick_review(
                        item,
                        output,
                        primary_task,
                        primary_publish_path,
                        sg_task,
                        comment,
                        thumbnail_path,
                        progress_cb,
                    )
                except Exception as e:
                    errors_list.append("Publish failed - %s" % e)

            elif output["name"].lower().endswith("translation"):
                # Handle Translator Task
                translator_data_reference = app.get_setting("translator_data_reference")
                if not translator_data_reference:
                    raise TankError("Configuration Error: Check translator_data_reference in app "
                                    "configuration.")
                
                # Get and verify data needed for translators.
                # Note: Check if the translator info exists but only if there are translation tasks 
                #       to be one.
                # If there are tasks to be done and no translator info exists then throw an 
                # exception.
                # If there are no tasks then just exit early. 
                if not "translator_info" in translator_data_reference.keys():
                    if len(tasks) > 0:
                        raise TankError("Configuration Error: Check translator_info exists in app_launchers for Alias.")
                    else:
                        return []
                    
                main_translator_info = translator_data_reference["translator_info"]
                self.verify_core_translator_info(main_translator_info)

                if "output" in task.keys():
                    if "name" in task["output"].keys():
                    
                        scene_path = self.parent.engine.get_current_file()
                        fields = work_template.get_fields(scene_path)
                        # create the publish path by applying the fields
                        # with the publish template:
                        output_publish_template = output["publish_template"]
                        publish_path = output_publish_template.apply_fields(fields)

                        # work out publish name:
                        publish_name = self._get_publish_name(publish_path, output_publish_template, fields)

                        errors_list = self.translate_and_publish_file(
                            main_translator_info, 
                            output["name"],
                            publish_name,
                            primary_publish_path,
                            comment,
                            sg_task,
                            work_template,
                            thumbnail_path,
                            item["type"],
                            progress_cb,
                            publish_path=publish_path
                        )
                    else:
                        errors_list.append("Task Data Error: Task is missing name attribute in output dictionary")
                else:
                    errors_list.append("Task Data Error: Task is missing an output attribute")

            elif output["name"] == "export_variants":
                if not exported_variants:
                    exported_variants = engine.export_variants()
                    self.parent.engine.log_info("Exported variants {!r}".format(exported_variants))

                if not exported_variants:
                    errors_list.append("error trying to publish the variants")
                elif exported_variants.get("files"):
                    for variant_file in exported_variants.get("files"):
                        name, path = variant_file.split(";")

                        data = {
                            "project": self.parent.context.project,
                            "user": tank.util.get_current_user(self.parent.tank),
                            "subject": "Alias Variant",
                            "content": name,
                            "note_links": []
                        }

                        if self._primary_created_version:
                            data["note_links"].append(self._primary_created_version)

                        note = self.parent.shotgun.create("Note", data)
                        self.parent.shotgun.upload(entity_type="Note",
                                                   entity_id=note.get("id"),
                                                   path=path,
                                                   field_name="sg_thumbnail")

                    continue
            elif output["name"] == "export_annotations":
                exported_annotations = engine.export_annotations()
                self.parent.engine.log_info("Exported annotations {!r}".format(exported_annotations))

                if not exported_annotations:
                    errors_list.append("error trying to publish the annotations")
                elif exported_annotations.get("strings"):
                    for annotation_string in exported_annotations.get("strings"):
                        data = {
                            "project": self.parent.context.project,
                            "user": tank.util.get_current_user(self.parent.tank),
                            # "sg_status_list": "opn",
                            "subject": "Alias Annotation",
                            "content": annotation_string,
                            # "sg_metadata": "",
                            # "sg_annotations": "",
                            # "sg_additional_info": "",
                            "note_links": []
                        }

                        if self._primary_created_version:
                            data["note_links"].append(self._primary_created_version)

                        note = self.parent.shotgun.create("Note", data)

                    continue
            else:
                # don't know how to publish this output types!
                errors_list.append("Don't know how to publish this item! %s" % task)

            # Add the result to the return value.
            new_task_data = {}
            new_task_data["task"] = task
            new_task_data["errors"] = errors_list
            return_task_data.append(new_task_data)

            progress_cb(100)

        if exported_variants and exported_variants.get("temp_dir") and os.path.exists(exported_variants.get("temp_dir")):
            shutil.rmtree(exported_variants.get("temp_dir"))

        return return_task_data
                
    def verify_core_translator_info(self, all_translator_info):
        """
        This will verify that the basic licensing data is present in the launchers yml file.
        """
        if "alias_translator_dir" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translator_dir under translator_info in app_launchers configuration")
        if "alias_translator_license_prod_key" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translator_license_prod_key under translator_info in app_launchers configuration")
        if "alias_translator_license_prod_version" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translator_license_prod_version under translator_info in app_launchers configuration")
        if "alias_translator_license_type" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translator_license_type under translator_info in app_launchers configuration")
        if "alias_translator_license_path" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translator_license_path under translator_info in app_launchers configuration")
        if "alias_translators" not in all_translator_info.keys():
            raise TankError("Configuration Error: Check alias_translators under under translator_info in app_launchers configuration")
            
    def verify_translator(self, specific_translator_info):
        """
        This will verify that the data need for a translator is present in the launchers yml file.
        """
        errors_list = []
        if "alias_translator_exe" not in specific_translator_info.keys():
            errors_list.append("alias_translator_exe is missing from configuration")
        if "alias_translator_file_ext" not in specific_translator_info.keys():
            errors_list.append("alias_translator_file_ext is missing from configuration")
        if "alias_translator_is_licensed" not in specific_translator_info.keys():
            errors_list.append("alias_translator_is_licensed is missing from configuration")
        if "alias_translator_name" not in specific_translator_info.keys():
            errors_list.append("alias_translator_name is missing from configuration")

        return errors_list
        
    def translate_and_publish_file(self, all_translator_info, translatorName, publish_name, primary_publish_path,
                                   comment, sg_task, work_template, thumbnail_path,
                                   publish_file_type, progress_cb, publish_path=None):
        """
        This will perform the translation for the current listed translator name given in the 
        method.
        
        Returns a string if an error occurred.
        """
        app = self.parent
        progress_cb(10, "Determining publish details")
       
        # Perform Publish Here
        # Get Primary Publish Template
        publish_template = app.get_template("primary_publish_template")
        if publish_template is None:
            raise TankError("Configuration Error:  Could not find template specified with primary_publish_template")
        
        errors_list = []
        
        # Initalize a current translator config to use.
        current_translator_config = None
        
        # Get translator Configuration
        for translator_config in all_translator_info["alias_translators"]:
            if "alias_translator_name" in translator_config.keys():
                if translator_config["alias_translator_name"] == translatorName:
                    errors_list = self.verify_translator(translator_config)
                    if len(errors_list) > 0:
                        return errors_list
                    current_translator_config = translator_config
            else:
                raise TankError("Configuration Error:  alias_translator_name is missing from one of the translator configurations in alias translators")
                
        progress_cb(30, "Translating file...")

        ## Perform Translation of Alias wire file to specified translator.
        # Get the new file path
        if not publish_path:
            translator_file_path = dirname(primary_publish_path) + "\\" + \
                                 splitext(basename(primary_publish_path))[0] + "." + \
                                 current_translator_config["alias_translator_file_ext"]
        else:
            translator_file_path = publish_path
        
        # Delete file if present
        if isfile(translator_file_path):
            remove(translator_file_path)
            self.parent.engine.log_info("Deleted previous file: "+translator_file_path)
        else:
            # TODO: Remove this part because future projects will have the directory already created
            translator_file_dir = dirname(translator_file_path)
            if not os.path.exists(translator_file_dir):
                os.makedirs(translator_file_dir)
                self.parent.engine.log_info("Created directories path: "+translator_file_path)

        self.parent.engine.log_info("Converting Wire File: %s with %s" % (
                primary_publish_path,
                current_translator_config["alias_translator_exe"]
                )
        )
        
        # Setup Command
        transConvCmd = "%s\\%s" % (all_translator_info["alias_translator_dir"], 
                                   current_translator_config["alias_translator_exe"])
        transCmdLine = [transConvCmd]
        if current_translator_config["alias_translator_is_licensed"]:
            transCmdLine.append("-productKey")
            transCmdLine.append(all_translator_info["alias_translator_license_prod_key"])
            transCmdLine.append("-productVersion")
            transCmdLine.append(all_translator_info["alias_translator_license_prod_version"])
            transCmdLine.append("-productLicenseType")
            transCmdLine.append(all_translator_info["alias_translator_license_type"])
            transCmdLine.append("-productLicensePath")
            transCmdLine.append(all_translator_info["alias_translator_license_path"])

        # Handle the input file and the output file of the translator
        transCmdLine.append("-i")
        transCmdLine.append(primary_publish_path)
        transCmdLine.append("-o")
        transCmdLine.append(translator_file_path)
        
        try:
            check_call(transCmdLine)
            self.parent.engine.log_info("Writing out %s File: %s" % (
                current_translator_config["alias_translator_exe"],
                translator_file_path
                )
            )
        except CalledProcessError as e:
            errors_list.append("Error occured, status code: %s" % e.returncode)
            
        # Check if the translation has occured and a file is present
        if not isfile(translator_file_path):
            errors_list.append("File Error: File: %s was not found after "
                                "translation" % translator_file_path)

        template_fields = publish_template.get_fields(primary_publish_path)
        progress_cb(70, "Registering Publish for %s" % publish_file_type)
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": translator_file_path,
            "name": publish_name,
            "version_number": template_fields["version"],
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": [primary_publish_path],
            "published_file_type": publish_file_type
        }
        tank.util.register_publish(**args)
        
        return errors_list

    def __publish_quick_review(self, item, output, primary_task, primary_publish_path,
                               sg_task, comment, thumbnail_path, progress_cb):

        # determine the publish info to use
        #
        progress_cb(10, "Determining publish details")

        primary_publish_template = primary_task["output"]["publish_template"]
        fields = primary_publish_template.get_fields(primary_publish_path)

        publish_version = fields["version"]
        tank_type = output["tank_type"]

        # create the publish path by applying the fields
        # with the publish template:
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)

        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)

        # determine the publish name:
        publish_name = fields.get("name")
        if not publish_name:
            publish_name = os.path.basename(publish_path)

        # register the publish:
        progress_cb(50, "Registering Publish for %s" % tank_type)
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": publish_name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": [primary_publish_path],
            "published_file_type": tank_type
        }
        publish = tank.util.register_publish(**args)

        progress_cb(65, "Generating Quicktime")
        quicktime = self._generate_quicktime(publish_path)
        self._validate_quicktime(quicktime)

        progress_cb(85, "Creating Version and uploading Quicktime")
        self._create_version(quicktime, publish, thumbnail_path)

    def _create_version(self, quicktime, publish, thumbnail_path):
        """
        Creates a new version entity and uploads the quicktime for review.
        """
        # now create a version record in Shotgun
        current_user = tank.util.get_current_user(self.parent.tank)

        data = {
            "code": "%s Review" % publish["path"]["name"],
            "user": current_user,
            "entity": self.parent.context.entity,
            "project": self.parent.context.project,
            "created_by": current_user,
            "description": publish.get("description", ""),
            "image": thumbnail_path,
            "published_files": [publish]
        }

        if self.parent.context.task:
            data["sg_task"] = self.parent.context.task

        version = self.parent.shotgun.create("Version", data)

        return version

    def _generate_quicktime(self, quicktime_path):
        """
        Returns a Quicktime object with info about the generated quicktime.

        NOTE: This is dummy code and doesn't do anything yet.
        """
        quicktime = namedtuple("Quicktime", [
                "success",
                "error_msg",
                "frame_count",
                "frame_range",
                "first_frame",
                "last_frame",
                "path",
        ])

        quicktime.success = True 
        quicktime.path = "/dummy/path/quicktime.mov"

        return quicktime        

    def _validate_quicktime(self, quicktime):

        return (
            quicktime.success and
            quicktime.path 
            # and os.path.exists(quicktime.path)
        )

    def _get_publish_name(self, path, template, fields=None):
        """
        Return the 'name' to be used for the file - if possible
        this will return a 'versionless' name
        """
        # first, extract the fields from the path using the template:
        fields = fields.copy() if fields else template.get_fields(path)
        if "name" in fields and fields["name"]:
            # well, that was easy!
            name = fields["name"]
        else:
            # find out if version is used in the file name:
            template_name, _ = os.path.splitext(os.path.basename(template.definition))
            version_in_name = "{version}" in template_name

            # extract the file name from the path:
            name, _ = os.path.splitext(os.path.basename(path))
            delims_str = "_-. "
            if version_in_name:
                # looks like version is part of the file name so we
                # need to isolate it so that we can remove it safely.
                # First, find a dummy version whose string representation
                # doesn't exist in the name string
                version_key = template.keys["version"]
                dummy_version = 9876
                while True:
                    test_str = version_key.str_from_value(dummy_version)
                    if test_str not in name:
                        break
                    dummy_version += 1

                # now use this dummy version and rebuild the path
                fields["version"] = dummy_version
                path = template.apply_fields(fields)
                name, _ = os.path.splitext(os.path.basename(path))

                # we can now locate the version in the name and remove it
                dummy_version_str = version_key.str_from_value(dummy_version)

                v_pos = name.find(dummy_version_str)
                # remove any preceeding 'v'
                pre_v_str = name[:v_pos].rstrip("v")
                post_v_str = name[v_pos + len(dummy_version_str):]

                if (pre_v_str and post_v_str
                    and pre_v_str[-1] in delims_str
                    and post_v_str[0] in delims_str):
                    # only want one delimiter - strip the second one:
                    post_v_str = post_v_str.lstrip(delims_str)

                versionless_name = pre_v_str + post_v_str
                versionless_name = versionless_name.strip(delims_str)

                if versionless_name:
                    # great - lets use this!
                    name = versionless_name
                else:
                    # likely that version is only thing in the name so
                    # instead, replace the dummy version with #'s:
                    zero_version_str = version_key.str_from_value(0)
                    new_version_str = "#" * len(zero_version_str)
                    name = name.replace(dummy_version_str, new_version_str)

        return name

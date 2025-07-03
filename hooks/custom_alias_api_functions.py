# Copyright (c) 2025 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Example file for demonstrating how to define custom Alias API functions.
"""


def my_custom_log_to_prompt():
    """
    Test function to log a message to the Alias prompt.
    This is used to verify that the custom hook is working correctly.
    """

    # This function, when executed on the tk-framework-alias server side, will
    # have access to the `alias_api` module`
    alias_api.log_to_prompt("Hello, from my custom Alias API function!")


def my_custom_delete_all(al_objects):
    """Delete all objects."""

    for al_object in al_objects:
        al_object.delete_object()


def my_custom_create_layers_from_objects(al_objects):
    """Create a layer for each object by its name."""

    for al_object in al_objects:
        alias_api.create_layer(al_object.name)

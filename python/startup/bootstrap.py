# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from alias_bootstrap import compute_environment, compute_args

def bootstrap(engine_name, context, app_path, app_args, extra_args):
    """
    Prepares for the bootstrapping process that will run during startup of
    Alias.
    """

    env = compute_environment(extra_args)

    return_args = compute_args(app_args)

    return app_path, return_args

# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from tank_vendor import six

import alias_api


# -------------------------------------------------------------------------------------------------------
# AlLayer functions
# -------------------------------------------------------------------------------------------------------


def get_symmetric_layers(layers=None, check_exists=False, skip_layers=None):
    """
    Get the list of all layers with symmetry property turned on.

    :param layers: The layers to check. If not provided, all layers in the current scene will be checked.
    :type layers: list<AlLayer> | list<str>
    :param check_exists: Set to True to return immediately upon finding a layer with symmetry.
    :type check_exists: bool
    :param skip_layers: A list of layer names to skip in checking for symmetry
    :type skip_layers: list<str>

    :return: If `check_exists` is True, return True if a layer was found with symmetry, else False.
             If `check_exists` is False, return the list of layers with symmetry.
    :rtype: bool | list<AlLayer>
    """

    symmetric_layers = []
    layers = layers or alias_api.get_layers()

    for layer in layers:
        if isinstance(layer, six.string_types):
            layer = alias_api.get_layer_by_name(layer)

        if (
            layer
            and (not skip_layers or layer.name not in skip_layers)
            and layer.symmetric
        ):
            if check_exists:
                return True
            symmetric_layers.append(layer)

    return False if check_exists else symmetric_layers

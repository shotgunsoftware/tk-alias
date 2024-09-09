# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from typing import Optional, List, Union
from .al_typing import AlLayerList

from .base import AliasPyBase


class AliasPyLayer(AliasPyBase):
    """Alias Python API utility class."""

    def __init__(self, alpy):
        super(AliasPyLayer, self).__init__(alpy)

    # -------------------------------------------------------------------------------------------------------
    # AlLayer functions
    # -------------------------------------------------------------------------------------------------------

    def get_symmetric_layers(
        self,
        layers: Optional[Union[List[str], AlLayerList]] = None,
        skip_layers: Optional[List[str]] = None,
    ) -> AlLayerList:
        """
        Get the list of all layers with symmetry property turned on.

        :param layers: The layers to check. If not provided, all layers in the
            current scene will be checked.
        :param skip_layers: The layer names to skip in checking for symmetry

        :return: The layers with symmetry property turned on.
        """

        if layers:
            if isinstance(layers[0], str):
                layer_names = [
                    layer_name for layer_name in layers if layer_name not in skip_layers
                ]
                layers = self.alias_py.get_layers_by_name(layer_names)
            else:
                layers = [
                    layer
                    for layer in layers
                    if not skip_layers or layer.name not in skip_layers
                ]
        else:
            layers = self.alias_py.get_layers(ignore_names=set(skip_layers))

        with self.alias_py.request_context_manager() as manager:
            for layer in layers:
                manager.result.append(layer.symmetric)

        return [
            layers[i] for i, is_symmetric in enumerate(manager.result) if is_symmetric
        ]

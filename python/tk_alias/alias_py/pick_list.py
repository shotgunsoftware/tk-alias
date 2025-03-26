# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from typing import List, Union, Optional

from .base import AliasPyBase
from .al_typing import (
    AlDagNodeList,
    AlLocatorList,
    AlShaderList,
    AlLayerList,
)


class AliasPyPickList(AliasPyBase):
    """Alias Python API pick list class."""

    def __init__(self, alpy):
        super().__init__(alpy)

    # -------------------------------------------------------------------------------------------------------
    # Pick functions
    # -------------------------------------------------------------------------------------------------------

    def pick_nodes(
        self, nodes: Union[List[str], AlDagNodeList], clear_pick_list=True, redraw=True
    ):
        """
        Pick the given nodes.

        :param nodes: The nodes to pick.
        :param clear_pick_list: True will clear the current pick list before
            anything is picked.
        :param redraw: True will refresh the Alias scene to reflect the pick
            changes.
        """

        with self.alias_py.request_context_manager(is_async=True):
            if clear_pick_list:
                self.alias_py.clear_pick_list()

            if nodes:
                self.alias_py.pick_nodes(nodes)

            if redraw:
                self.alias_py.redraw_screen()

    def pick_curves_on_surface_from_nodes(
        self,
        nodes: Union[List[str], AlDagNodeList],
        clear_pick_list: Optional[bool] = True,
        redraw: Optional[bool] = True,
    ):
        """
        Pick the curves on surface from the given nodes.

        :param nodes: The nodes to pick curves on surface from.
        :param clear_pick_list: True will clear the current pick list before
            anything is picked.
        :param redraw: True will refresh the Alias scene to reflect the pick
            changes.
        """

        unused_curves = (
            self.alias_py.py_dag_node.get_unused_curves_on_surface_for_nodes(
                nodes=nodes
            )
        )

        with self.alias_py.request_context_manager(is_async=True):
            if clear_pick_list:
                self.alias_py.clear_pick_list()

            if unused_curves:
                self.alias_py.pick(unused_curves)

            if redraw:
                self.alias_py.redraw_screen()

    def pick_nodes_assigned_to_shaders(
        self,
        shaders: Union[List[str], AlShaderList],
        clear_pick_list: Optional[bool] = True,
        redraw: Optional[bool] = True,
    ):
        """
        Pick the nodes assigned to the given shaders.

        :param shaders: The shaders to pick nodes from
        :param clear_pick_list: True will clear the current pick list before
            anything is picked.
        :param redraw: True will refresh the Alias scene to reflect the pick
            changes.
        """

        if not shaders:
            return

        with self.alias_py.request_context_manager(is_async=True):
            if clear_pick_list:
                self.alias_py.clear_pick_list()
            self.alias_py.pick_nodes_assigned_to_shaders(shaders)
            if redraw:
                self.alias_py.redraw_screen()

    def pick_nodes_assigned_to_layers(
        self,
        layers: Union[List[str], AlLayerList],
        clear_pick_list: Optional[bool] = True,
        redraw: Optional[bool] = True,
    ):
        """
        Pick the nodes assigned to the given layers.

        :param layers: The layers to pick nodes from
        :type layers: list<AlLayer>
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        with self.alias_py.request_context_manager(is_async=True):
            if clear_pick_list:
                self.alias_py.clear_pick_list()

            self.alias_py.pick_nodes_assigned_to_layers(layers)

            if redraw:
                self.alias_py.redraw_screen()

    def pick_layers(
        self,
        layers: Optional[Union[List[str], AlLayerList]] = None,
        pick_all: Optional[bool] = False,
        clear_pick_list: Optional[bool] = True,
        redraw: Optional[bool] = True,
    ):
        """
        Pick the given layers.

        :param layers: The layers to pick.
        :param pick_all: Pick all the layers in the current scene. The layers
            list will be ignored.
        :param clear_pick_list: True will clear the current pick list before
            anything is picked.
        :param redraw: True will refresh the Alias scene to reflect the pick
            changes.
        """

        with self.alias_py.request_context_manager(is_async=True):
            if pick_all:
                self.alias_py.pick_all_layers()
            elif clear_pick_list:
                self.alias_py.unpick_all_layers()

            if not pick_all and layers:
                self.alias_py.pick_layers(layers)

            if redraw:
                self.alias_py.redraw_screen()

    def pick_locators(
        self,
        locators: Optional[Union[List[str], AlLocatorList]] = None,
        pick_all: Optional[bool] = False,
        clear_pick_list: Optional[bool] = True,
        redraw: Optional[bool] = True,
    ):
        """
        Pick the given locators.

        :param locators: The locators to pick.
        :param pick_all: Pick all the locators in the current scene. The
            locators list will be ignored.
        :param clear_pick_list: True will clear the current pick list before
            anything is picked.
        :param redraw: True will refresh the Alias scene to reflect the pick
            changes.
        """

        with self.alias_py.request_context_manager(is_async=True):
            if pick_all:
                self.alias_py.pick_all_locators()
            elif clear_pick_list:
                self.alias_py.unpick_all_locators()

            if not pick_all and locators:
                self.alias_py.pick_locators(locators)

            if redraw:
                self.alias_py.redraw_screen()

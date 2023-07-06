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

from .base import AliasPyBase


class AliasPyPickList(AliasPyBase):
    """Alias Python API pick list class."""

    def __init__(self, alpy):
        super(AliasPyPickList, self).__init__(alpy)

    # -------------------------------------------------------------------------------------------------------
    # Pick functions
    # -------------------------------------------------------------------------------------------------------

    def pick_nodes(self, nodes, clear_pick_list=True, redraw=True):
        """
        Pick the given nodes.

        :param nodes: The nodes to pick.
        :type nodes: list<AlDagNode>
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        if clear_pick_list:
            self.alias_py.clear_pick_list()

        for node in nodes:
            if isinstance(node, six.string_types):
                node = self.alias_py.find_dag_node_by_name(node)

            if node:
                node.pick()

        if redraw:
            self.alias_py.redraw_screen()

    def pick_curves_on_surface_from_nodes(
        self, nodes, clear_pick_list=True, redraw=True
    ):
        """
        Pick the curves on surface from the given nodes.

        :param nodes: The nodes to pick curves on surface from.
        :type nodes: list<AlDagNode>
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        if clear_pick_list:
            self.alias_py.clear_pick_list()

        unused_curves = (
            self.alias_py.py_dag_node.get_unused_curves_on_surface_for_nodes(
                nodes=nodes
            )
        )

        for curve in unused_curves:
            curve.pick()

        if redraw:
            self.alias_py.redraw_screen()

    def pick_nodes_assigned_to_shaders(
        self, shaders, clear_pick_list=True, redraw=True, skip_shaders=None
    ):
        """
        Pick the nodes assigned to the given shaders.

        :param shaders: The shaders to pick nodes from
        :type shaders: list<AlShader>
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        :param skip_shaders: A list of shader names to skip (their assigned nodes will not be picked)
        :type skip_shaders: list<str>
        """

        skip_shaders = skip_shaders or []

        if clear_pick_list:
            self.alias_py.clear_pick_list()

        for shader in shaders:
            if isinstance(shader, six.string_types):
                if shader in skip_shaders:
                    continue

                shader = self.alias_py.get_shader_by_name(shader)
                if not shader:
                    continue

            elif shader.name in skip_shaders:
                continue

            for node in shader.get_assigned_nodes():
                node.pick()

        if redraw:
            self.alias_py.redraw_screen()

    def pick_nodes_assigned_to_layers(self, layers, clear_pick_list=True, redraw=True):
        """
        Pick the nodes assigned to the given layers.

        :param layers: The layers to pick nodes from
        :type layers: list<AlLayer>
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        if clear_pick_list:
            self.alias_py.clear_pick_list()

        for layer in layers:
            if isinstance(layer, six.string_types):
                layer = self.alias_py.get_layer_by_name(layer)

            if layer:
                for node in layer.get_assigned_nodes():
                    node.pick()

        if redraw:
            self.alias_py.redraw_screen()

    def pick_layers(
        self, layers=None, pick_all=False, clear_pick_list=True, redraw=True
    ):
        """
        Pick the given layers.

        :param layers: The layers to pick.
        :type layers: list<AlLayer>
        :param pick_all: Pick all the layers in the current scene. The layers list will be ignored.
        :type pick_all: bool
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        if isinstance(layers, six.string_types):
            layers = [layers]

        if clear_pick_list or pick_all:
            # NOTE this does not clear the node pick list, this unpicks all the layers.
            for layer in self.alias_py.get_layers():
                if pick_all:
                    layer.pick()
                else:
                    layer.unpick()

        if not pick_all:
            for layer in layers:
                if isinstance(layer, six.string_types):
                    layer = self.alias_py.get_layer_by_name(layer)

                if layer:
                    layer.pick()

        if redraw:
            self.alias_py.redraw_screen()

    def pick_locators(
        self, locators, pick_all=False, clear_pick_list=True, redraw=True
    ):
        """
        Pick the given locators.

        :param locators: The locators to pick.
        :type locators: list<AlLocator>
        :param pick_all: Pick all the locators in the current scene. The locators list will be ignored.
        :type pick_all: bool
        :param clear_pick_list: True will clear the current pick list before anything is picked.
        :type clear_pick_list: bool
        :param redraw: True will refresh the Alias scene to reflect the pick changes.
        :type redraw: bool
        """

        if clear_pick_list or pick_all:
            # NOTE this does not clear the node pick list, this unpicks all the locators.
            for locator in self.alias_py.get_locators():
                if pick_all:
                    locator.pick()
                else:
                    locator.unpick()

        if not pick_all:
            for locator in locators:
                if isinstance(locator, six.string_types):
                    locator = self.alias_py.get_locator_by_name(locator)

                if locator:
                    locator.pick()

        if redraw:
            self.alias_py.redraw_screen()

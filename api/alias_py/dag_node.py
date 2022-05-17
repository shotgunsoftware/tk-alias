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

from . import traverse_dag as api_traverse_dag
from . import utils as api_utils


# -------------------------------------------------------------------------------------------------------
# AlDagNode functions
# -------------------------------------------------------------------------------------------------------


def is_node_template(node):
    """
    Check if the node is set as a template.

    :param node: The node to check.
    :type node: AlDagNode
    """

    return bool(node.is_display_mode_set(alias_api.AlDisplayModeType.Template))


def get_node_shader(node):
    """
    Get the shader assigned to the given node.

    :param node: The node to get the shader from
    :type node: AlDagNode

    :return: The shader assigned to the node.
    :rtype: AlShader
    """

    if not node:
        return None

    return alias_api.node_first_shader(node)


def get_instanced_nodes(nodes=None, check_exists=False):
    """
    Process all nodes in the current scene, or the specfied nodes, and check if they are instanced nodes.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>
    :param check_exists: Set to True to return immediately on finding an instanced node. Default=False
    :type check_exists: bool

    :return: If check_exists is set to True, return True if an instanced node is found, else False.
             If check_exists is set to False, return the list of instanced nodes.
    :rtype: bool | list<AlDagNode>
    """

    instances = []

    if nodes:
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if api_utils.is_success(api_traverse_dag.node_is_instance(node)):
                if check_exists:
                    return True
                instances.append(node)

        return False if check_exists else instances

    else:
        # NOTE check_exists does not apply to traverse dag yet
        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_is_instance(input_data)
        return result.nodes


def get_nodes_with_construction_history(
    nodes=None, check_exists=False, skip_node_types=None
):
    """
    Process all nodes in the current scene, or the specfied nodes, and check if they have construction
    history.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>
    :param check_exists: Set to True to return immediately on finding a node with history. Default=False
    :type check_exists: bool
    :param skip_node_types: A list of node types to skip when checking for history.
    :type skip_node_types: list<alias_api.AlObjectType>

    :return: If check_exists is set to True, return True if a node with history is found, else False.
             If check_exists is set to False, return the list of nodes with history.
    :rtype: bool | list<AlDagNode>
    """

    skip_node_types = skip_node_types or set()
    nodes_with_history = []

    if nodes:
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() in skip_node_types:
                continue

            if alias_api.has_history(node):
                if check_exists:
                    return True
                nodes_with_history.append(node)

        return False if check_exists else nodes_with_history

    else:
        # NOTE check_exists does not apply to traverse dag yet
        input_data = alias_api.TraverseDagInputData(skip_node_types, False)
        result = alias_api.search_node_has_history(input_data)
        return result.nodes


def get_nodes_with_non_zero_transform(
    nodes=None, check_exists=False, skip_node_types=None
):
    """
    Process all nodes in the current scene, or the specfied nodes, and check if they have a
    non-zero transform.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>
    :param check_exists: Set to True to return immediately on finding a node with history. Default=False
    :type check_exists: bool
    :param skip_node_types: A list of node types to skip when checking for history.
    :type skip_node_types: list<alias_api.AlObjectType>

    :return: If check_exists is set to True, return True if a node with non-zero transform is found,
        else False.
             If check_exists is set to False, return the list of nodes with pivots not at the origin.
    :rtype: bool | list<AlDagNode>
    """

    skip_node_types = skip_node_types or set()
    invalid_nodes = []

    if nodes:
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() in skip_node_types:
                continue

            status = api_traverse_dag.node_has_non_zero_transform(node)
            if api_utils.is_success(status):
                if check_exists:
                    return True
                invalid_nodes.append(node)

        return False if check_exists else invalid_nodes

    else:
        # NOTE check_exists does not apply to traverse dag yet
        input_data = alias_api.TraverseDagInputData(skip_node_types, False)
        result = alias_api.search_node_has_non_zero_transform(input_data)
        return result.nodes


def get_nodes_with_non_origin_pivot(
    nodes=None, check_exists=False, skip_node_types=None
):
    """
    Process all nodes in the current scene, or the specfied nodes, and check if they have their pivots
    not set to the origin.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>
    :param check_exists: Set to True to return immediately on finding a node with history. Default=False
    :type check_exists: bool
    :param skip_node_types: A list of node types to skip when checking for history.
    :type skip_node_types: list<alias_api.AlObjectType>

    :return: If check_exists is set to True, return True if a node with pivots not at the origin is found,
        else False. If check_exists is set to False, return the list of nodes with pivots not at the origin.
    :rtype: bool | list<AlDagNode>
    """

    skip_node_types = skip_node_types or set()
    invalid_nodes = []

    if nodes:
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() in skip_node_types:
                continue

            status = api_traverse_dag.node_has_non_origin_pivot(node)
            if api_utils.is_success(status):
                if check_exists:
                    return True
                invalid_nodes.append(node)

        return False if check_exists else invalid_nodes

    else:
        # NOTE check_exists does not apply to traverse dag yet
        input_data = alias_api.TraverseDagInputData(skip_node_types, False)
        result = alias_api.search_node_has_non_origin_pivot(input_data)
        return result.nodes


def get_nodes_with_unused_curves_on_surface(nodes=None, check_exists=False):
    """
    Process all nodes in the current scene, or the specfied nodes, and check if they have unused curve on
    surface.

    A curve on surface is unused if it is not being used to trim the surface it is on.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>
    :param check_exists: Set to True to return immediately on finding a node with history. Default=False
    :type check_exists: bool
    :param skip_node_types: A list of node types to skip when checking for history.
    :type skip_node_types: list<alias_api.AlObjectType>

    :return: If check_exists is set to True, return True if a node with unused curve on surface is found,
        else False. If check_exists is set to False, return the list of nodes with unnused curves on surface.
    :rtype: bool | list<AlDagNode>
    """

    if nodes:
        nodes_with_unused_curves_on_surface = []
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            status = api_traverse_dag.node_has_unused_curve_on_surface(
                node, check_exists=True
            )
            if api_utils.is_success(status):
                if check_exists:
                    return True
                nodes_with_unused_curves_on_surface.append(node)

        return False if check_exists else nodes_with_unused_curves_on_surface

    else:
        # NOTE check_exists does not apply to traverse dag yet
        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_unused_curves_on_surface(input_data)
        return result.nodes


def get_unused_curves_on_surface_for_nodes(nodes=None):
    """
    Process all nodes in the current scene, or the specfied nodes, and return all unused curves on surface.

    A curve on surface is unused if it is not being used to trim the surface it is on.

    :param nodes: The list of nodes to process. If not provided, all nodes in the scene will be processed.
                  Default=None
    :type nodes: list<AlDagNode>

    :return: The unused curves on surface.
    :rtype: list<AlCurveOnSurface>
    """

    unused_curves = []

    if nodes:
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() != alias_api.AlObjectType.SurfaceNodeType:
                continue

            surface = node.surface()
            if not surface:
                continue

            for curve in surface.get_curves_on_surface():
                if not curve.in_trim():
                    unused_curves.append(curve)

    else:
        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_unused_curves_on_surface(input_data)
        unused_curves = result.curves_on_surface

    return unused_curves


def get_nodes_by_type(node_types):
    """
    Get a list of all the nodes for the given types.

    :param node_types: The list of types to get nodes of.
    :type node_tyeps: list<AlObjectType>

    :return: The list of nodes that are of the given types.
    :rtype: list<AlDagNode>
    """

    accept_node_types = set(node_types)
    input_data = alias_api.TraverseDagInputData(accept_node_types, True)
    result = alias_api.search_dag(input_data)

    return result.nodes


def delete_nodes(nodes):
    """
    Convience function to delete the list of nodes.

    :param nodes: The nodes to delete.
    :type nodes: list<str> | list<AlDagNode>
    """

    if not nodes:
        return

    if isinstance(nodes, six.string_types):
        nodes = [nodes]

    for node in nodes:
        if isinstance(node, six.string_types):
            node = alias_api.find_dag_node_by_name(node)

        if node:
            node.delete_object()

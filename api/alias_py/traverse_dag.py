# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import alias_api

from . import dag_node as api_dag_node
from . import utils as api_utils

# -------------------------------------------------------------------------------------------------------
# Callback functions for 'traverse_dag'
# -------------------------------------------------------------------------------------------------------
#   Requirements:
#       (1) takes a single parameter fo type AlDagNode
#       (2) return type is alias_api.AlStatusCode
# -------------------------------------------------------------------------------------------------------


def node_is_instance(node):
    """
    Return success if the given node is an instance.

    A node is considered to be an instance if:
        (1) it is a group node
        (2) it shares its children with another sibling group node; e.g. when
            group_node.is_instanced() returns True
        (3) its previous sibling node is an instance; e.g. when
            group_node.prev_instance() return value is not None

    This function can be used a node callback in a DAG traversal operation.

    :return: Success status code if the node is an instance else Failure.
    :rtype: AlStatusCode
    """

    if not node:
        return api_utils.failure_status()

    if not api_utils.is_group_node(node):
        return api_utils.failure_status()

    if node.is_instanced() and node.prev_instance():
        return api_utils.success_status()

    return api_utils.failure_status()


def node_is_template(node):
    """
    Return success if the given node set as a template.

    This function can be used a node callback in a DAG traversal operation.

    :return: Success status code if the node is an instance else Failure.
    :rtype: AlStatusCode
    """

    if not node:
        return api_utils.failure_status()

    if api_dag_node.is_node_template(node):
        return api_utils.success_status()

    return api_utils.failure_status()


def node_has_non_zero_transform(node):
    """
    Return success if the given node does not have a zero transform.

    A node has a zero transform if its global transformation matrix is the identity matrix.

    This function can be used a node callback in a DAG traversal operation.

    :return: Success status code if the node does not have a zero transform else Failure.
    :rtype: AlStatusCode

    :raises alias_api.AliasPythonException: If the node's global transformation matrix failed to be retrieved.
    """

    if not node:
        return api_utils.failure_status()

    status, transform_matrix = node.global_transformation_matrix()
    if not api_utils.is_success(status):
        raise alias_api.AliasPythonException(
            "Failed to retrieve node global transformation matrix."
        )

    if api_utils.is_identity(transform_matrix):
        return api_utils.failure_status()

    return api_utils.success_status()


def node_has_non_origin_pivot(node):
    """
    Return success if the given node does not both scale and rotate pivots set to the origin.

    This function can be used a node callback in a DAG traversal operation.

    :return: Success status code if the node does not have pivots at the origin, else Failure.
    :rtype: AlStatusCode

    :raises alias_api.AliasPythonException: If the node's scale or rotate pivots failed to be retrieved.
    """

    if not node:
        return api_utils.failure_status()

    status, pivot = node.scale_pivot()
    if not api_utils.is_success(status):
        raise alias_api.AliasPythonException("Failed to retrieve node scale pivot.")

    if not api_utils.is_origin(pivot):
        return api_utils.success_status()

    status, pivot = node.rotate_pivot()
    if not api_utils.is_success(status):
        raise alias_api.AliasPythonException("Failed to retrieve node rotate pivot.")

    if not api_utils.is_origin(pivot):
        return api_utils.success_status()

    return api_utils.failure_status()


def node_has_unused_curve_on_surface(node, check_exists=False, delete=False):
    """
    Return success if the given node has unused curves on surface.

    A curve on surface is considered to be unused if it is not being used to trim the surface it is on.

    This function can be used a node callback in a DAG traversal operation.

    :param node: The node to check
    :type node: AlDagNode
    :param check_exists: Set to True to return immediately upon finding an unused curve on surface.
    :type check_exists: bool
    :param delete: Set to True to delete any unused curves on surface found.
    :type delete: bool

    :return: Success status code if the node has unused curves on surface, else Failure.
    :rtype: AlStatusCode

    :raises alias_api.AliasPythonException: If the node's global transformation matrix failed to be retrieved.
    """

    if not node or node.type() != alias_api.AlObjectType.SurfaceNodeType:
        return api_utils.failure_status()

    surface = node.surface()
    if not surface:
        return api_utils.failure_status()

    has_unused_curves = False
    for curve in surface.get_curves_on_surface():
        if not curve.in_trim():
            # Found an unnused curve on surface
            if check_exists:
                return api_utils.success_status()

            if delete:
                curve.delete_object()

            has_unused_curves = True

    return (
        api_utils.success_status() if has_unused_curves else api_utils.failure_status()
    )

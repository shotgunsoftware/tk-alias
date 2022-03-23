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
# General functions
# -------------------------------------------------------------------------------------------------------

def success_status(int_value=False):
    """
    """

    status = alias_api.AlStatusCode.Success
    if int_value:
        return int(status)
    return status

def failure_status(int_value=False):
    """
    """

    status = alias_api.AlStatusCode.Failure
    if int_value:
        return int(status)
    return status

def is_success(alias_status):
    """
    Return True if the given status is successfull.
    """

    success_status = alias_api.AlStatusCode.Success

    if isinstance(alias_status, alias_api.AlStatusCode):
        return alias_status == success_status

    return alias_status == int(success_status)

def is_group_node(alias_object):
    """
    Return True if the given Alias Object is a group node.
    """

    return alias_object.type() == alias_api.AlObjectType.GroupNodeType

def camera_node_types():
    """
    Return the list of Alias node types for cameras.
    """

    return [
        alias_api.AlObjectType.CameraEyeType,
        alias_api.AlObjectType.CameraViewType,
        alias_api.AlObjectType.CameraUpType,
    ]

def light_node_types():
    """
    Return the list of Alias node types for lights.
    """

    return [
        alias_api.AlObjectType.LightNodeType,
        alias_api.AlObjectType.LightLookAtNodeType,
        alias_api.AlObjectType.LightUpNodeType,
    ]

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
    
    :return: Success status code if the node is an instance else Failure. This function returns the Alias
             status code instead of a boolean so that it can be passed as a callback to the Alias Python
             API `traverse_dag` function.
    :rtype: AlStatusCode
    """

    if not node:
        return failure_status()
    
    if not is_group_node(node):
        return failure_status()
    
    if node.is_instanced() and node.prev_instance():
        return success_status()

    return failure_status()

def node_has_non_zero_transform(node):
    """
    """

    if not node:
        return failure_status()

    status, transform_matrix = node.global_transformation_matrix()
    if not is_success(status):
        # NOTE should we raise an AliasPythonException if we fail to retrieve the necessary data to check?
        return failure_status()

    if is_identity(transform_matrix):
        return failure_status()
    
    return success_status()

def node_has_non_origin_pivot(node):
    """
    """

    if not node:
        return failure_status()

    status, pivot = node.scale_pivot()
    if not is_success(status):
        # NOTE should we raise an AliasPythonException if we fail to retrieve the necessary data to check?
        return failure_status()

    if not is_origin(pivot):
        return success_status()

    status, pivot = node.rotate_pivot()
    if not is_success(status):
        return failure_status()

    if not is_origin(pivot):
        return success_status()

    return failure_status()

def node_has_unused_curve_on_surface(node, check_exists=False, delete=False):
    """
    """

    if not node or node.type() != alias_api.AlObjectType.SurfaceNodeType:
        return failure_status()

    surface = node.surface()
    if not surface:
        return failure_status()

    has_unused_curves = False
    for curve in surface.get_curves_on_surface():
        if not curve.in_trim():
            # Found an unnused curve on surface
            if check_exists:
                return success_status()

            if delete:
                curve.delete_object()

            has_unused_curves = True

    return success_status() if has_unused_curves else failure_status()

# -------------------------------------------------------------------------------------------------------
# AlDagNode functions
# -------------------------------------------------------------------------------------------------------

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
            
            if is_success(node_is_instance(node)):
                if check_exists:
                    return True
                instances.append(node)

        return False if check_exists else instances

    input_data = alias_api.TraverseDagInputData()
    result = alias_api.search_node_is_instance(input_data)
    return result.nodes

def get_nodes_with_construction_history(nodes=None, check_exists=False, skip_node_types=None):
    """
    """

    skip_node_types = skip_node_types or set()
    nodes_with_history = []

    if nodes:
        while nodes:
            node = nodes.pop()

            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() in skip_node_types:
                continue

            if alias_api.has_history(node):
                if check_exists:
                    return True
                nodes_with_history.append(node)

        return False if check_exists else nodes_with_history
    
    # 
    # TODO check_exists does not apply to traverse dag yet
    # 
    # input_data = alias_api.TraverseDagInputData(set(), skip_node_types)
    input_data = alias_api.TraverseDagInputData(skip_node_types, False)
    result = alias_api.search_node_has_history(input_data)
    return result.nodes

def get_nodes_with_non_zero_transform(nodes=None, check_exists=False, skip_node_types=None):
    """
    """

    skip_node_types = skip_node_types or set()
    invalid_nodes = []

    if nodes:
        while nodes:
            node = nodes.pop()
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)
            
            if not node or node.type() in skip_node_types:
                continue

            status = node_has_non_zero_transform(node)
            if is_success(status):
                if check_exists:
                    return True
                invalid_nodes.append(node)
    
        return False if check_exists else invalid_nodes
            
    # 
    # TODO check_exists does not apply to traverse dag yet
    # 
    # input_data = alias_api.TraverseDagInputData(set(), skip_node_types)
    input_data = alias_api.TraverseDagInputData(skip_node_types, False)
    result = alias_api.search_node_has_non_zero_transform(input_data)
    return result.nodes

def get_nodes_with_non_origin_pivot(nodes=None, check_exists=False, skip_node_types=None):
    """
    """

    skip_node_types = skip_node_types or set()
    invalid_nodes = []

    if nodes:
        while nodes:
            node = nodes.pop()
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            if not node or node.type() in skip_node_types:
                continue

            status = node_has_non_origin_pivot(node)
            if is_success(status):
                if check_exists:
                    return True
                invalid_nodes.append(node)
    
        return False if check_exists else invalid_nodes

    # 
    # TODO check_exists does not apply to traverse dag yet
    # 
    # input_data = alias_api.TraverseDagInputData(set(), skip_node_types)
    input_data = alias_api.TraverseDagInputData(skip_node_types, False)
    result = alias_api.search_node_has_non_origin_pivot(input_data)
    return result.nodes

def get_node_shader(node):
    """
    """

    if not node:
        return None

    return alias_api.node_first_shader(node)

def get_nodes_with_unused_curves_on_surface(nodes=None, check_exists=False):
    """
    """

    if nodes:
        nodes_with_unused_curves_on_surface = []
        for node in nodes:
            if isinstance(node, six.string_types):
                node = alias_api.find_dag_node_by_name(node)

            status = node_has_unused_curve_on_surface(node, None, check_exists=True)
            if is_success(status):
                if check_exists:
                    return True
                nodes_with_unused_curves_on_surface.append(node)

        return False if check_exists else nodes_with_unused_curves_on_surface
    
    input_data = alias_api.TraverseDagInputData()
    result = alias_api.search_node_unused_curves_on_surface(input_data)
    return result.nodes

# -------------------------------------------------------------------------------------------------------
# AlCurveonSurface functions
# -------------------------------------------------------------------------------------------------------

def get_unused_curves_on_surface_for_nodes(nodes=None):
    """
    """

    unused_curves = []

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

    return unused_curves

def delete_unused_curves_on_surface_for_nodes(nodes=None):
    """
    """

    if nodes:
       unused_curves = get_unused_curves_on_surface_for_nodes(nodes)

    else:
        input_data = alias_api.TraverseDagInputData()
        result = alias_api.search_node_unused_curves_on_surface(input_data)
        unused_curves = result.curves_on_surface

    for curve in unused_curves:
        curve.delete_object()

# -------------------------------------------------------------------------------------------------------
# AlLayer functions
# -------------------------------------------------------------------------------------------------------

def get_empty_layers(layers=None, check_exists=False, skip_layers=None):
    """
    """

    skip_layers = skip_layers or set()
    empty_layers = alias_api.get_empty_layers(True, skip_layers)

    if layers:
        empty_layers = [layer for layer in empty_layers if layer.name in layers]
    
    return bool(empty_layers) if check_exists else empty_layers

def get_symmetric_layers(layers=None, check_exists=False, skip_layers=None):
    """
    """

    skip_layers = skip_layers or set()

    symmetric_layers = []
    layers = layers or alias_api.get_layers()

    for layer in layers:
        if isinstance(layer, six.string_types):
            layer = alias_api.get_layer_by_name(layer)
        
        if layer and layer.name not in skip_layers and layer.symmetric:
            if check_exists:
                return True
            symmetric_layers.append(layer)
    
    return False if check_exists else symmetric_layers


# -------------------------------------------------------------------------------------------------------
# AlLocator functions
# -------------------------------------------------------------------------------------------------------

def get_locators(check_exists=False):
    """
    """

    locator = alias_api.first_locator()
    if check_exists:
        has_locator = bool(locator)
        del locator
        return has_locator

    locators = []
    while locator:
        locators.append(locator)
        next_locator = alias_api.next_locator(locator)
        del locator
        locator = next_locator
    
    return locators


# -------------------------------------------------------------------------------------------------------
# Matrix functions
# -------------------------------------------------------------------------------------------------------

def is_close(a, b, rel_tol=1e-03, abs_tol=0.0):
    """
    Standard test for if a float or double value is approximately equal
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def is_zero(determinant, threshold=0.000001):
    """
    Return True if the determinant is less than the threshold, indicating that the number is very small
    and basically equal to zero.
    """

    return abs(determinant) < threshold

def is_origin(pivot):
    """
    Test if the pivot (point) is near the 0,0,0 origin.

    :param pivot: The pivot point in world space.
    :return: True if the point is close to the origin.
    """

    return is_zero(pivot.x) and is_zero(pivot.y) and is_zero(pivot.z)

def is_identity(matrix):
    """
    Tests if the matrix is close to the unit or identity matrix
    :param matrix: The matrix (4x4) to test
    :return: True is close to the identity matrix, else False.
    """

    if not (is_close(matrix[0][0], 1.0)):
        return False
    if not (is_close(matrix[1][1], 1.0)):
        return False
    if not (is_close(matrix[2][2], 1.0)):
        return False
    if not (is_close(matrix[3][3], 1.0)):
        return False

    if not (is_close(matrix[0][1], 0.0)):
        return False
    if not (is_close(matrix[0][2], 0.0)):
        return False
    if not (is_close(matrix[0][3], 0.0)):
        return False

    if not (is_close(matrix[1][0], 0.0)):
        return False
    if not (is_close(matrix[1][2], 0.0)):
        return False
    if not (is_close(matrix[1][3], 0.0)):
        return False

    if not (is_close(matrix[2][0], 0.0)):
        return False
    if not (is_close(matrix[2][1], 0.0)):
        return False
    if not (is_close(matrix[2][3], 0.0)):
        return False

    if not (is_close(matrix[3][0], 0.0)):
        return False
    if not (is_close(matrix[3][1], 0.0)):
        return False
    if not (is_close(matrix[3][2], 0.0)):
        return False

    return True

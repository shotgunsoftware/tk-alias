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
from .al_typing import (
    AlDagNode,
    AlDagNodeList,
    AlShader,
    AlObjectTypeList,
    AlCurveOnSurfaceList,
    TraverseDagOutputData,
)

from .base import AliasPyBase


class AliasPyDagNode(AliasPyBase):
    """Alias Python API utility class."""

    def __init__(self, alpy):
        super(AliasPyDagNode, self).__init__(alpy)

    # -------------------------------------------------------------------------------------------------------
    # AlDagNode functions
    # -------------------------------------------------------------------------------------------------------

    def is_template(self, node: AlDagNode) -> bool:
        """
        :param node: The node to check.
        :return: True if the node is a template, else False
        """

        return bool(node.is_display_mode_set(self.alias_py.AlDisplayModeType.Template))

    def is_instance(self, node: AlDagNode) -> bool:
        """
        :param node: The node to check.
        :return: True if the given node is an instance, else False.
        """

        if not node:
            return False

        if not self.alias_py.py_utils.is_group_node(node):
            return False

        if node.is_instanced() and node.prev_instance():
            return True

        return False

    def has_zero_transform(self, node: AlDagNode) -> bool:
        """
        Check if the given node has a zero transform.

        :param node: The node to check.
        :return: True if the node has a zero transform, else False.
        """

        if not node:
            return False

        status, transform_matrix = node.global_transformation_matrix()
        if not self.alias_py.py_utils.is_success(status):
            return False

        return self.alias_py.py_utils.is_identity(transform_matrix)

    def has_origin_pivot(self, node: AlDagNode) -> bool:
        """
        Check if the given node has its pivot set to the origin.

        A node is considered to have its pivot set to the origin if both its
        scale and rotate pivots are set to the origin.

        :param node: The node to check.
        :return: True if the node has its pivot set to the origin, else False.
        """

        if not node:
            return False

        status, scale_pivot = node.scale_pivot()
        if not self.alias_py.py_utils.is_success(status):
            return False

        status, rotate_pivot = node.rotate_pivot()
        if not self.alias_py.py_utils.is_success(status):
            return False

        return self.alias_py.py_utils.is_origin(
            scale_pivot
        ) and self.alias_py.py_utils.is_origin(rotate_pivot)

    def get_node_shader(self, node: AlDagNode) -> AlShader:
        """
        :param node: The node to get the shader from
        :return: The shader assigned to the node.
        """

        if not node:
            return None
        return self.alias_py.node_first_shader(node)

    def get_instanced_nodes(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        return_nodes: Optional[bool] = True,
    ) -> Union[AlDagNodeList, TraverseDagOutputData]:
        """
        Return nodes that are instanced.

        A node is considered to be an instance if:
            (1) it is a group node
            (2) it shares its children with another sibling group node; e.g. when
                group_node.is_instanced() returns True
            (3) its previous sibling node is an instance; e.g. when
                group_node.prev_instance() return value is not None

        :param nodes: The nodes to process. If not provided, all nodes in the
            scene will be processed. Default is None.
        :param return_nodes: True will return the list of nodes found that are
            instanced. False will return the whole search result object. Default
            is True.

        :return: The instanced nodes if `return_nodes` is True, else the whole
            search result object.
        """

        node_names = set(self.__get_node_names(nodes))
        input_data = self.alias_py.TraverseDagInputData(node_names, True)
        result = self.alias_py.search_node_is_instance(input_data)
        if return_nodes:
            return result.nodes
        return result

    def get_nodes_with_construction_history(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
        return_nodes: Optional[bool] = True,
    ) -> Union[AlDagNodeList, TraverseDagOutputData]:
        """
        Return nodes with construction history.

        :param nodes: The nodes to process. If not provided, all nodes in the
            scene will be processed. Default is None.
        :param skip_node_types: A list of AlObjectType objects to skip.
        :param return_nodes: True will return the list of nodes found that have
            construction history. False will return the whole search result object.

        :return: The nodes with construction history if `return_nodes` is True,
            else the whole search result object.
        """

        skip_node_types_set = set(skip_node_types or [])
        node_names = set(self.__get_node_names(nodes))
        input_data = self.alias_py.TraverseDagInputData(
            node_names, True, skip_node_types_set, False
        )
        result = self.alias_py.search_node_has_history(input_data)
        if return_nodes:
            return result.nodes
        return result

    def get_nodes_with_non_zero_transform(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
        top_level_only: Optional[bool] = False,
        return_nodes: Optional[bool] = True,
    ) -> Union[AlDagNodeList, TraverseDagOutputData]:
        """
        Return nodes with non-zero transform.

        A node has a zero transform if its global transformation matrix is the
        identity matrix.

        :param nodes: The nodes to process. If not provided, all nodes in the
            scene will be processed. Default is None.
        :param skip_node_types: A list of node types to skip.
        :param top_level_only: If True, only the top level nodes will be checked.
            Default is False.
        :param return_nodes: True will return the list of nodes found that have
            non-zero transform. False will return the whole search result object.

        :return: The nodes with non-zero transform if `return_nodes` is True,
            else the whole search result object.
        """

        skip_node_types_set = set(skip_node_types or [])
        node_names = set(self.__get_node_names(nodes))
        input_data = self.alias_py.TraverseDagInputData(
            node_names, True, skip_node_types_set, False
        )
        result = self.alias_py.search_node_has_non_zero_transform(
            input_data, top_level_only=top_level_only
        )
        if return_nodes:
            return result.nodes
        return result

    def get_nodes_with_non_origin_pivot(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        skip_node_types: Optional[AlObjectTypeList] = None,
        return_nodes: Optional[bool] = True,
    ) -> Union[AlDagNodeList, TraverseDagOutputData]:
        """
        Return the nodes that do not have their pivots set to the origin.

        A node with pivot at the origin must have both scale and rotate pivots
        set to the origin.

        NOTE: For performance, it is recommended to pass `return_nodes` as False
        to return search result object, that can be used to check the number of
        nodes found that do not have their pivots set to the origin. If the
        number of nodes is small, then you can access the nodes without a
        performance hit, otherwise if the number of nodes is large, then
        accessing that list of nodes will be slow (since the data will be
        passed from the api server to the client).

        :param nodes: The list of nodes to process. If not provided, all nodes
            in the scene will be processed. Default is None.
        :param skip_node_types: The node types to skip.
        :param return_nodes: True will return the list of nodes found that do
            not have their pivots set to the origin. False will return the
            whole search result object. Default is True.

        :return: The nodes that do not have their pivots set to the origin, if
            `return_nodes` is True, else the whole search result object.
        """

        skip_node_types_set = set(skip_node_types or [])
        node_names = set(self.__get_node_names(nodes))
        input_data = self.alias_py.TraverseDagInputData(
            node_names, True, skip_node_types_set, False
        )
        result = self.alias_py.search_node_has_non_origin_pivot(input_data)
        if return_nodes:
            return result.nodes
        return result

    def get_nodes_with_unused_curves_on_surface(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        return_nodes: Optional[bool] = True,
        return_cos: Optional[bool] = False,
    ) -> Union[AlDagNodeList, AlCurveOnSurfaceList, TraverseDagOutputData]:
        """
        Return the nodes that have unused curve on surface.

        A curve on surface is unused if it is not being used to trim the surface
        it is on.

        :param nodes: The list of nodes to check. If not provides, all nodes
            with unused curves on surface will be returned. Default is None.
        :param return_nodes: True will return the list of nodes found that have
            unused curves on surface.
        :param return_cos: True will return the list of curves on surface found
            that are unused.

        :return: The nodes that have unused curves on surface if `return_nodes`
            is True, else the whole search result object.
        """

        node_names = set(self.__get_node_names(nodes))
        input_data = self.alias_py.TraverseDagInputData(node_names, True)
        result = self.alias_py.search_node_unused_curves_on_surface(input_data)
        if return_nodes:
            return result.nodes
        if return_cos:
            return result.curves_on_surface
        return result

    def get_unused_curves_on_surface_for_nodes(
        self,
        nodes: Optional[Union[List[str], AlDagNodeList]] = None,
        return_cos: Optional[bool] = True,
    ) -> Union[AlCurveOnSurfaceList, TraverseDagOutputData]:
        """
        Return the unused curves on surface for the given nodes.

        A curve on surface is unused if it is not being used to trim the surface
        it is on.

        :param nodes: The list of nodes to check. If not provides, all nodes
            with unused curves on surface will be returned. Default is None.
        :param return_cos: True will return the list of curves on surface found
            that are unused. False will return the whole search result object.

        :return: The unused curves on surface for the given nodes if `return_cos`
            is True, else the whole search result object.
        """

        return self.get_nodes_with_unused_curves_on_surface(
            nodes, return_nodes=False, return_cos=return_cos
        )

    def get_nodes_by_type(
        self,
        node_types: AlObjectTypeList,
        return_nodes: Optional[bool] = True,
    ) -> Union[AlDagNodeList, TraverseDagOutputData]:
        """
        Get a list of all the nodes for the given types.

        :param node_types: The list of types to get nodes of.
        :param return_nodes: True will return the list of nodes found that are
            of the given types. False will return the whole search result object.

        :return: The nodes of the given types if `return_nodes` is True, else
            the whole search result object.
        """

        accept_node_types = set(node_types)
        input_data = self.alias_py.TraverseDagInputData(accept_node_types, True)
        result = self.alias_py.search_dag(input_data)
        if return_nodes:
            return result.nodes
        return result

    def delete_nodes(self, nodes: Union[str, List[str], AlDagNodeList]):
        """
        Delete the given list of nodes.

        :param nodes: The nodes to delete.
        """

        if not nodes:
            return

        if isinstance(nodes, str):
            self.alias_py.delete_dag_nodes_by_name([nodes])
        elif isinstance(nodes[0], str):
            self.alias_py.delete_dag_nodes_by_name(nodes)
        else:
            self.alias_py.delete_all(nodes)

    # -------------------------------------------------------------------------------------------------------
    # Private helper methods

    def __get_node_names(
        self,
        nodes: Union[List[str], AlDagNodeList],
    ) -> List[str]:
        """Convencience function to get the names of the given nodes."""

        if not nodes:
            return []

        if isinstance(nodes[0], self.alias_py.AlDagNode):
            return [node.name for node in nodes]

        if isinstance(nodes[0], str):
            return nodes

        raise ValueError("Invalid node list.")

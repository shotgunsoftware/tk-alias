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


# -------------------------------------------------------------------------------------------------------
# General functions
# -------------------------------------------------------------------------------------------------------


def success_status(int_value=False):
    """
    Return the Alias Python API (APA) success status.

    :param int_value: Set to True to return the int value of the APA success status.
    :type int_value: bool

    :return: The APA success status
    :rtype: alias_api.AlStatusCode | int
    """

    status = alias_api.AlStatusCode.Success
    if int_value:
        return int(status)
    return status


def failure_status(int_value=False):
    """
    Return the Alias Python API (APA) failure status.

    :param int_value: Set to True to return the int value of the APA failure status.
    :type int_value: bool

    :return: The APA failure status
    :rtype: alias_api.AlStatusCode | int
    """

    status = alias_api.AlStatusCode.Failure
    if int_value:
        return int(status)
    return status


def is_success(alias_status):
    """
    Check if the given status is the Alias Python API (APA) success status.

    :return: True if the given status is the Alias Python API (APA) success status, else False.
    :rtype: bool
    """

    success = alias_api.AlStatusCode.Success

    if isinstance(alias_status, alias_api.AlStatusCode):
        return alias_status == success

    return alias_status == int(success)


def raise_exception(msg, error_status=None):
    """
    Convenience function to raise an Alias Python Exception.

    :param msg: The message to include in the raised exception.
    :type msg: str
    :param error_status: The Alias error status to report.
    :type error_status: int

    :raises alias_api.AliasPythonException: always
    """

    error_msg = msg

    if error_status is not None:
        error_msg += "\nError status {}".format(error_status)

    raise alias_api.AliasPythonException(error_msg)


def is_group_node(alias_object):
    """
    Check if the given `alias_object` is an Alias group node.

    :param alias_object: The Alias object to check
    :type alias_object: alias_api.AlObject

    :return: True if the given Alias Object is a group node, else False.
    :rtype: bool
    """

    return alias_object.type() == alias_api.AlObjectType.GroupNodeType


def camera_node_types():
    """
    :return: The list of Alias node types for cameras.
    :rtype: list<alias_api.AlObjectType>
    """

    return [
        alias_api.AlObjectType.CameraEyeType,
        alias_api.AlObjectType.CameraViewType,
        alias_api.AlObjectType.CameraUpType,
    ]


def light_node_types():
    """
    :return: The list of Alias node types for lights.
    :rtype: list<alias_api.AlObjectType>
    """

    return [
        alias_api.AlObjectType.LightNodeType,
        alias_api.AlObjectType.LightLookAtNodeType,
        alias_api.AlObjectType.LightUpNodeType,
    ]


# -------------------------------------------------------------------------------------------------------
# Matrix functions
# -------------------------------------------------------------------------------------------------------


def is_close(a, b, rel_tol=1e-03, abs_tol=0.0):
    """
    Compare two floating point values to determine if they are approximately equal.

    :param a: The first value to compare
    :type a: float
    :param b: The second value to compare
    :type b: float
    :param rel_tol: The relative tolerance used to determine if a and b are approximately equal.
    :type rel_tol: float
    :param abs_tol: The maximum different used to determine if a and b are approximately equal.
    :type abs_tol: float

    :return: True if a and b are approximately equal, else False.
    :rtype: bool
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def is_zero(value):
    """
    Check if the value is approximately equal to zero.

    :parma value: The value to check
    :type value: float

    :return: True if the value is approximately equal to zero, else False.
    :rtype: bool
    """

    return is_close(value, 0.0)


def is_origin(point):
    """
    Check if the point is at the origin.

    Note that this checks that the point is approximately at the origin for floating point values.

    :param point: The vector point in world space.
    :type point: alias_api.Vec3

    :return: True if the point is at the origin.
    :rtype: bool
    """

    return is_zero(point.x) and is_zero(point.y) and is_zero(point.z)


def is_identity(matrix):
    """
    Check if the matrix is identity (unit) matrix.

    Note that this checks that the matrix is approximately equal to the identity matrix for floating point
    values.

    :param matrix: The matrix to check
    :type matrix: list (4x4)

    :return: True if the matrix is the identity matrix, else False.
    :rtype: bool
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


# -------------------------------------------------------------------------------------------------------
# AlLocator functions
# -------------------------------------------------------------------------------------------------------


def get_locators(check_exists=False):
    """
    Get all Alias locators in the current scene.

    :param check_exists: Set to True to return immediately upon finding a locator.
    :type check_exists: bool

    :return: If `check_exists` is True, True is returned if there is at least one locator found, else False.
             If `check_exists` is False, the list of locator objects is returned.
    :rtype: bool | list<alias_api.AlLocator>
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

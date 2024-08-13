# Copyright (c) 2024 Autodesk Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk Inc.

from typing import TypeVar, List

AlDagNode = TypeVar("AlDagNode")
AlDagNodeList = List[AlDagNode]

AlObjectType = TypeVar("AlObjectType")
AlObjectTypeList = List[AlObjectType]

AlShader = TypeVar("AlShader")
AlShaderList = List[AlShader]

AlLocator = TypeVar("AlLocator")
AlLocatorList = List[AlLocator]

AlReferenceFile = TypeVar("AlReferenceFile")
AlReferenceFileList = List[AlReferenceFile]

AlLayer = TypeVar("AlLayer")
AlLayerList = List[AlLayer]

AlCurveNode = TypeVar("AlCurveNode")
AlCurveNodeList = List[AlCurveNode]

AlCurveOnSurface = TypeVar("AlCurveOnSurface")
AlCurveOnSurfaceList = List[AlCurveOnSurface]

AlSet = TypeVar("AlSet")
AlSetList = List[AlSet]

TraverseDagOutputData = TypeVar("TraverseDagOutputData")

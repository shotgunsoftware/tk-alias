# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import sgtk

tk_framework_alias = sgtk.platform.import_framework(
    "tk-framework-alias", "tk_framework_alias"
)


AliasSocketIoClient = tk_framework_alias.client.AliasSocketIoClient
AliasClientNamespace = tk_framework_alias.client.AliasClientNamespace
ClientRequestContextManager = tk_framework_alias.client.ClientRequestContextManager

client_exceptions = tk_framework_alias.client.exceptions
AliasClientNotConnected = client_exceptions.AliasClientNotConnected

AliasClientModuleProxyWrapper = tk_framework_alias.client.AliasClientModuleProxyWrapper

QtImportError = tk_framework_alias.server.utils.exceptions.QtImportError
QtModuleNotFound = tk_framework_alias.server.utils.exceptions.QtModuleNotFound
QtAppInstanceNotFound = tk_framework_alias.server.utils.exceptions.QtAppInstanceNotFound

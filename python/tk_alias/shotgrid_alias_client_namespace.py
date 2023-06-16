# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from .framework_alias import AliasClientNamespace


class ShotGridAliasClientNamespace(AliasClientNamespace):
    """Namespace for ShotGrid specific communication with Alias."""

    def on_shutdown(self):
        """
        Shutdown event received from the server.

        Destroy the engine.
        """

        super(ShotGridAliasClientNamespace, self).on_shutdown()

        self.client.engine.shutdown()

    def _handle_callback(self, callback_func, data=None):
        """
        Handle the event callback from Alias.

        The server has forwarded an event callback triggered by Alias. Execute the callback
        function in the main GUI thread.

        :param callback_func: The callback function to execute.
        :type callback_func: function
        :param data: A dictionary containing the callback function arguments.
        :type data: dict

        :return: The return value from executing the callback function.
        :rtype: any
        """

        data = data or {}
        args = data.get("args", [])
        kwargs = data.get("kwargs", {})
        return self.client.engine.execute_in_main_thread(callback_func, *args, **kwargs)

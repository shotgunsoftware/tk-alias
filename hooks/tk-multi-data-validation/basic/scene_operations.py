# Copyright (c) 2024 Autodesk Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk Inc.


import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class AliasSceneOperationsHook(HookBaseClass):
    """Hook class to set up Alias scene events to update the Data Validation App."""

    def __init__(self, *args, **kwargs):
        super(AliasSceneOperationsHook, self).__init__(*args, **kwargs)
        self.__alias_event_callbacks = []

    def register_scene_events(self, reset_callback, change_callback):
        """
        Register events for when the scene has changed.

        The function reset_callback provided will reset the current Data Validation App,
        when called. The function change_callback provided will display a warning in the
        Data Validation App UI that the scene has changed and the current validatino state
        may be stale.

        :param reset_callback: Callback function to reset the Data Validation App.
        :type reset_callback: callable
        :param change_callback: Callback function to handle the changes to the scene.
        :type change_callback: callable
        """

        if self.__alias_event_callbacks:
            # Scene events already registered
            return

        engine = self.parent.engine

        # Define the list of Alias event to that will trigger the reset callback.
        reset_event_names = [
            "PostRetrieve",
            "StageActive",
        ]
        reset_events = []
        for reset_event in reset_event_names:
            reset_event_obj = self.__get_message_type(reset_event)
            if reset_event_obj:
                reset_events.append(reset_event_obj)
        reset_event_cb = (
            lambda result, cb=reset_callback: self.__handle_reset_event_callback(
                result, cb
            )
        )

        # Define the list of Alias event to that will trigger the change
        # callback.
        # NOTE: turning off the following change events, since Alias does not
        # optimize emitting events, and so listening for these events will
        # severely degrade performance:
        # - DagNodeDeleted
        # - DagNameModified
        change_event_names = [
            "DagNodeModified",
            # "DagNodeDeleted",
            # "DagNameModified",
            "ShaderAdded",
            "ShaderDeleted",
            "LayerAdded",
            "LayerDeleted",
            "LayerAttributeChanged",
            "ReferenceFileAdded",
            "ReferenceFileDeleted",
            "ReferenceFileModified",
            "LocatorAdded",
            "LocatorDeleted",
            "LocatorModified",
        ]
        change_events = []
        for change_event in change_event_names:
            change_event_obj = self.__get_message_type(change_event)
            if change_event_obj:
                change_events.append(change_event_obj)
        change_event_cb = (
            lambda result, cb=change_callback: self.__handle_change_event_callback(
                result, cb
            )
        )

        # Keep track of the Alias event callbacks that will be registered, so that they can
        # properly be unregistered on shut down.
        self.__alias_event_callbacks = [
            (reset_event_cb, reset_events),
            (change_event_cb, change_events),
        ]

        # Register the event callbacks to the engine's event watcher
        for callback, events in self.__alias_event_callbacks:
            engine.event_watcher.register_alias_callback(callback, events)

    def unregister_scene_events(self):
        """Unregister the scene events."""

        event_watcher = self.parent.engine.event_watcher
        if not event_watcher:
            # Engine already shutdown and removed event callbacks
            return

        # Unregister the event callbacks from the engine's event watcher
        for callback, events in self.__alias_event_callbacks:
            event_watcher.unregister_alias_callback(callback, events)

        # Clear the list of Alias event callbacks
        self.__alias_event_callbacks = []

    def __handle_change_event_callback(self, event_result, change_callback):
        """
        Intermediate callback handler for Alias events to trigger the Data Validation change
        callback.

        Process the result returned by the Alias event that triggered the callback, to call
        the scene callback function with the appropriate parameters.

        :param event_result: The object returned by the Alias event.
        :type event_result: alias_api.MessageResult
        :param change_callback: The callback to execute.
        :type change_callback: function
        """

        if event_result.message_type == self.__get_message_type("DagNodeModified"):
            warning_text = "Dag node modified"
        elif event_result.message_type == self.__get_message_type("DagNodeDeleted"):
            warning_text = "Dag node deleted"
        elif event_result.message_type == self.__get_message_type("DagNameModified"):
            warning_text = "Dag name modified"
        elif event_result.message_type == self.__get_message_type("ShaderAdded"):
            warning_text = "Shader added"
        elif event_result.message_type == self.__get_message_type("ShaderDeleted"):
            warning_text = "Shader deleted"
        elif event_result.message_type == self.__get_message_type("LayerAdded"):
            warning_text = "Layer added"
        elif event_result.message_type == self.__get_message_type("LayerDeleted"):
            warning_text = "Layer deleted"
        elif event_result.message_type == self.__get_message_type(
            "LayerAttributeChanged"
        ):
            warning_text = "Layer attribute changed"
        elif event_result.message_type == self.__get_message_type("ReferenceFileAdded"):
            warning_text = "Reference file added"
        elif event_result.message_type == self.__get_message_type(
            "ReferenceFileDeleted"
        ):
            warning_text = "Reference file deleted"
        elif event_result.message_type == self.__get_message_type(
            "ReferenceFileModified"
        ):
            warning_text = "Reference file modified"
        elif event_result.message_type == self.__get_message_type("LocatorAdded"):
            warning_text = "Locator added"
        elif event_result.message_type == self.__get_message_type("LocatorDeleted"):
            warning_text = "Locator deleted"
        elif event_result.message_type == self.__get_message_type("LocatorModified"):
            warning_text = "Locator modified"
        else:
            warning_text = None

        change_callback(text=warning_text)

    def __handle_reset_event_callback(self, event_result, reset_callback):
        """
        Intermediate callback handler for Alias events to trigger the Data Validation reset
        callback.

        :param event_result: The object returned by the Alias event.
        :type event_result: alias_api.MessageResult
        :param reset_callback: The callback to execute.
        :type reset_callback: function
        """

        reset_callback()

    def __get_message_type(self, message_type):
        """
        Return the Alias message type object for the given message type.

        If the message type is supported, the AlMessageType will be retruend.

        :param message_type: The message type to retrieve.
        :type message_type: str

        :return: The Alias message type object.
        :rtype: AlMessageType
        """

        alias_py = self.parent.engine.alias_py
        try:
            return getattr(alias_py.AlMessageType, message_type)
        except AttributeError:
            self.parent.logger.warning(
                f"Alias version does not support message type '{message_type}'"
            )

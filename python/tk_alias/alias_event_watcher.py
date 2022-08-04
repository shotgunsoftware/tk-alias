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


class AliasEventWatcher(object):
    """
    An object to manage Alias message events and callbacks.

    This class provides methods to register and unregister Alias message event callbacks.
    The events and their callbacks are stored in the class object so that they can be
    managed, including removing the callbacks on application shutdown.

    An Alias message event can be registered, which adds the message handler using the
    Alias Python API. The callbacks associated with the events will be triggered when
    this object is `watching` for Alias message events.

    Similarly, an Alias message event can be unregistered, meaning that the Python callback
    will no longer be triggered for the Alias message event.
    """

    class ContextManager:
        """
        A custom context manager to handle Alias events triggering Python callbacks.

        The purpose of this context manager is to ensure that Alias operations and Python
        callbacks triggered from Alias message events do not conflict. The entry method
        ensures that any Python callbacks triggered by Alias message events are queued
        (not executed immediately), and will be executed once the exit method is called.

        .. code-block:: python

            with AliasEventWatch.ContextManager():
                alias_api.open_file(file_path)

        This way of managing executing Python callbacks is preferred to using the
        AliasEventWAtcher watcher methods `start_watching` and `stop_watching`.
        """

        def __init__(self, ignore_events=False):
            """
            Initialize the context manager.

            :param ignore_events: Set to True to avoid triggering Python callbacks for any
                Alias message events that occur.
            :type ignore_events: bool
            """

            self.ignore_events = ignore_events

        def __enter__(self):
            """
            Set up the context manager.

            This entry method just calls the Alias Python API function to indicate to start
            queuing any callbacks triggered by Alias message events. This means that any
            Python callback that would be triggered by an Alias event, is not executed until
            the Alias Python API function is called to execute the callbacks that have been
            queued.
            """

            alias_api.queue_events(True)

        def __exit__(self, exc_type, exc_value, exc_tb):
            """
            Set up the context manager.

            This exit method calls the Alias Python API function to execute the Python
            callbacks that have been added to the queue. The queue will become empty after
            this API call.

            :param exc_type: The exception class
            :param exc_value: The exception instance
            :param exc_tb: The traceback object
            """

            # TODO handle exceptions

            if self.ignore_events:
                # Clear the queued events, but do not trigger their callacks.
                alias_api.clear_queued_events()
            else:
                # Trigger any Python callbacks for the queued events. The queue will become
                # empty after this.
                alias_api.queue_events(False)

    def __init__(self):
        """
        Initialize the Alias event watcher.
        """

        # Store the Alias message event callbacks that have been registered. For example,
        #
        #   self.__scene_events = {
        #       AliasEventType : {
        #           cb_fn1: cb_id1,
        #           ...
        #       },
        #       ...
        #   }
        #
        # , such that:
        #   - AliasEventType is an alias_api.AlMessageType object
        #   - cn_fn is the python callback we want to execute
        #   - cb_id is the id of the registered callback in Alias
        self.__scene_events = {}

        # Property flag indicating whether or not the event watching is currently watching for
        # Alias message events. When set to True, Python callbacks will be triggered, else
        # when False, Python callbacks will not be triggered.
        self.__is_watching = False

    # -------------------------------------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------------------------------------

    @property
    def is_watching(self):
        """
        Get the property indicating if the event watcher is watching for Alias events.

        Python callbacks registered for Alias message events will only be triggered when this
        proeprty is True. Python callbacks will be ignored when this property is False.
        """
        return self.__is_watching

    # -------------------------------------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------------------------------------

    def get_callbacks(self, scene_event):
        """
        Get the list of Python callback functions for the Alias event type.

        :param scene_event: The Alias event type
        :type scene_event: alias_api.AlMessageType

        :return: The list of Python callback functions.
        :rtype: list<function>
        """

        return self.__scene_events.get(scene_event, {}).keys()

    def register_alias_callback(self, cb_fn, scene_events):
        """
        Add the given callback to the list of registered callbacks
        If we're currently watching, register this callback in Alias.

        :param cb_fn: Python callback we want to register.
        :type cb_fn: function
        :param scene_events: Single Alias event or list of Alias events we want to register
            this callback for.
        :type scene_events: list<alias_api.AlMessageType>
        """

        callback_id = None

        if not isinstance(scene_events, list):
            scene_events = [scene_events]

        for ev in scene_events:
            if self.__is_callback_registered(ev, cb_fn):
                continue
            # we only want to register the callback if we're currently watching
            # otherwise, we just want to add the callback to the list of registered callbacks
            # it will be properly registered next time the watcher is started
            if self.is_watching:
                status, callback_id = alias_api.add_message_handler(ev, cb_fn)
            self.__scene_events.setdefault(ev, {})[cb_fn] = callback_id

    def unregister_alias_callback(self, cb_fn, scene_events):
        """
        Remove the given callback to the list of registered callbacks
        If we're currently watching, unregister this callback in Alias.

        :param cb_fn: Python c.allback we want to unregister
        :type cb_fn: function
        :param scene_events: Single Alias event or list of Alias events we want to unregister
            this callback for.
        :type scene_events: list<alias_api.AlMessageType>
        """

        if not isinstance(scene_events, list):
            scene_events = [scene_events]

        for ev in scene_events:
            if not self.__is_callback_registered(ev, cb_fn):
                continue

            # Remove the callback from the list, and use the callback id to remove
            # the Alias message handler.
            callback_id = self.__scene_events[ev].pop(cb_fn)
            alias_api.remove_message_handler(ev, callback_id)

    def start_watching(self):
        """
        Starts watching for Alias scene events.

        The registered Alias message events are being watched by adding the message handler
        that triggers the Python callback when the event occurs. When Alias message events
        are being watched, this means that the associated Python callbacks will be triggered.

        NOTE: start and stop watching methods were created before adding the custom
        context manager class `AliasEventWatcher.ContextManager`. The context manager is the
        preferred way to managing calling Alias Python API functions to perform Alias
        operations, while ensuring that Python callbacks triggered by Alias message events
        do not conflict. These methods still exist for back supporting
        """

        # if we're already watching, just exit
        if self.is_watching:
            return

        # if we don't have any registered callbacks, exit too
        if not self.__scene_events:
            return

        for ev, callbacks in self.__scene_events.items():
            for cb_fn in callbacks.keys():
                status, callback_id = alias_api.add_message_handler(ev, cb_fn)
                if status == int(alias_api.AlStatusCode.Success):
                    self.__scene_events[ev][cb_fn] = callback_id

        self.__is_watching = True

    def stop_watching(self, force=False):
        """
        Stops watching for Alias scene events.

        The registered Alias message events are ignored by removing the message handler that
        triggers the Python callback when the event occurs. When Alias message events are
        being ignored, this means that the associated Python callbacks will not be triggered.

        :param force: Set to True to perform stop watching operations regardless of current
            watching state, else False to only perform stop watching operations if currently
            watching events.
        :type force: bool
        """

        if not self.is_watching:
            return

        for ev, callbacks in self.__scene_events.items():
            for cb_fn, callback_id in callbacks.items():
                if not callback_id:
                    return
                alias_api.remove_message_handler(ev, callback_id)
                self.__scene_events[ev][cb_fn] = None

        self.__is_watching = False

    def shutdown(self):
        """Shut down the event watcher."""

        self.stop_watching(force=True)
        self.__scene_events = {}

    # -------------------------------------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------------------------------------

    def __is_callback_registered(self, scene_event, cb_fn):
        """
        Check if a callback is already registered

        :param scene_event: Type of the Alias Event the callback is linked to
        :type scene_event: alias_api.AlMessageType
        :param cb_fn: Callback to check
        :type cb_fn: function

        :return: True if the callback is already registered, False otherwise
        :rtype: bool
        """

        if not self.__scene_events:
            return False

        for fn in self.__scene_events.get(scene_event, {}).keys():
            if cb_fn == fn:
                return True
        return False

# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.

import alias_api


class AliasEventWatcher(object):
    """
    Python object used to manage Alias callbacks.
    """

    def __init__(self):
        """
        Class constructor.
        """

        # used to store the registered callbacks
        # need to be formatted like this
        # self.__scene_events = {
        #   AliasEventType : {
        #       cb_fn1: cb_id1,
        #       cb_fn2: cb_id2
        #   }
        # }
        # where :
        # - AliasEventType is an alias_api.AlMessageType object
        # - cn_fn is the python callback we want to execute
        # - cb_id is the id of the registered callback in Alias
        self.__scene_events = {}
        self.__is_watching = False

    @property
    def is_watching(self):
        """
        Return True if the EventWatcher is actually watching for the even, False otherwise.
        """
        return self.__is_watching

    def get_callbacks(self, scene_event):
        """
        Get the list of Python callback functions for the Alias event type.

        :param scene_event: The Alias event type
        :type scene_event: alias_api.AlMessageType

        :return: The list of Python callback functions.
        :rtype: list<callable>
        """

        return self.__scene_events.get(scene_event, {}).keys()

    def register_alias_callback(self, cb_fn, scene_events):
        """
        Add the given callback to the list of registered callbacks
        If we're currently watching, register this callback in Alias.

        :param cb_fn: Python callback we want to register
        :param scene_events: Single Alias event or list of Alias events we want to register
            this callback for
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

        :param cb_fn: Python callback we want to unregister
        :param scene_events: Single Alias event or list of Alias events we want to unregister
            this callback for
        """

        if not isinstance(scene_events, list):
            scene_events = [scene_events]

        for ev in scene_events:
            if not self.__is_callback_registered(ev, cb_fn):
                continue
            callback_id = self.__scene_events[ev].pop(cb_fn)
            if self.is_watching:
                alias_api.remove_message_handler(ev, callback_id)

    def __is_callback_registered(self, scene_event, cb_fn):
        """
        Check if a callback is already registered

        :param scene_event: Type of the Alias Event the callback is linked to
        :param cb_fn: Callback to check
        :returns: True if the callback is already registered, False otherwise
        """
        for fn in self.__scene_events.get(scene_event, {}).keys():
            if cb_fn == fn:
                return True
        return False

    def start_watching(self):
        """
        Starts watching for scene events.
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

    def stop_watching(self):
        """
        Stops watching the scene events.
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

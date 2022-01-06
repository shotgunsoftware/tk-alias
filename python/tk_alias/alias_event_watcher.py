# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.

import alias_api


class AliasEventWatcher(object):
    """
    """

    def __init__(self):
        """
        """

        self.__registered_callbacks = []
        self.__scene_events = {}
        self.__is_watching = False

        # register scene event callbacks
        self.start_watching()

    @property
    def is_watching(self):
        return self.__is_watching

    def register_alias_callback(self, cb_fn, scene_events):
        """
        """
        if not isinstance(scene_events, list):
            scene_events = [scene_events]

        self.stop_watching()
        for ev in scene_events:
            if self.__is_callback_registered(ev, cb_fn):
                continue
            existing_callbacks = self.__scene_events.get(ev, [])
            existing_callbacks.append(cb_fn)
            self.__scene_events[ev] = existing_callbacks
        self.start_watching()

    def unregister_alias_callback(self, cb_fn, scene_events):
        """
        """

        if not isinstance(scene_events, list):
            scene_events = [scene_events]

        self.stop_watching()
        for ev in scene_events:
            if not self.__is_callback_registered(ev, cb_fn):
                continue
            self.__scene_events[ev].remove(cb_fn)
        self.start_watching()

    def __is_callback_registered(self, scene_event, cb_fn):
        """
        """
        for fn in self.__scene_events.get(scene_event, []):
            if cb_fn == fn:
                return True
        return False

    def start_watching(self):
        """
        Starts watching for scene events.
        """

        # if currently watching then stop
        if len(self.__registered_callbacks) != 0:
            self.stop_watching()

        for ev, callbacks in self.__scene_events.items():
            for cb_fn in callbacks:
                status, callback_id = alias_api.add_message_handler(ev, cb_fn)
                if status == int(alias_api.AlStatusCode.Success):
                    self.__registered_callbacks.append((ev, callback_id, cb_fn))

        self.__is_watching = True

    def stop_watching(self):
        """
        Stops watching the scene events.
        """

        for message_type, callback_id, cb_fn in self.__registered_callbacks:
            alias_api.remove_message_handler(message_type, callback_id)
        self.__registered_callbacks = []
        self.__is_watching = False

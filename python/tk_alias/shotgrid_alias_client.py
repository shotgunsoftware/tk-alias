# Copyright (c) 2022 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from .framework_alias import AliasSocketIoClient, QtImportError
from .shotgrid_alias_client_namespace import ShotGridAliasClientNamespace


class ShotGridAliasSocketIoClient(AliasSocketIoClient):
    """A ShotGrid specific client."""

    def __init__(self, engine, namespace, *args, **kwargs):
        """Initialize the ShotGrid Alias socketio client."""

        super(ShotGridAliasSocketIoClient, self).__init__(*args, **kwargs)

        self.__engine = engine
        self.__qt_app = None
        self._default_namespace = namespace
        self.add_namespace(ShotGridAliasClientNamespace(namespace))

    # -------------------------------------------------------------------------------------------------------
    # Properties

    @property
    def engine(self):
        """Get the ShotGrid Alias Engine that is running this client io"""
        return self.__engine

    @property
    def qt_app(self):
        """Get the running ShotGrid client Qt application instance."""
        if not self.__qt_app:
            from sgtk.platform.qt import QtGui

            self.__qt_app = QtGui.QApplication.instance()
        return self.__qt_app

    # -------------------------------------------------------------------------------------------------------
    # Override base methods

    def cleanup(self):
        """Clean up the client on disconnect."""

        super(ShotGridAliasSocketIoClient, self).cleanup()
        self.__qt_app = None

    def _process_events(self):
        """
        Process GUI events.

        ShotGrid runs a Qt application for its GUI, so this method will process Qt GUI events,
        excluding user input events.

        This method is called while waiting for an sio event to return. This allows Alias to
        perform any necessary GUI events during an api request from the client (else
        the app may become deadlocked if the client makes an api request while blocking GUI
        events, but the api requests needs to perform some actions in the GUI).
        """

        from sgtk.platform.qt import QtCore

        if self.qt_app:
            self.qt_app.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)

    def _handle_server_error(self, error):
        """Handle an error returned by the server from an event."""

        from sgtk.platform.qt import QtGui

        if error.__class__.__name__ == QtImportError.__name__:
            parent = None
        else:
            parent = self.engine._get_dialog_parent()

        QtGui.QMessageBox.critical(
            parent,
            "Alias Server Error",
            f"{error.__class__.__name__}: {error}",
        )

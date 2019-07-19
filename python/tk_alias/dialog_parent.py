import sys

import win_32_api

from sgtk.platform.qt import QtGui


class DialogParent(object):
    # Constants
    HWND_CLASSNAME = "StudioProxy"
    PROXY_WINDOW_TITLE = "sgtk dialog owner proxy"

    # Cache
    _main_hwnd = None
    _proxy_window = None

    def __init__(self, engine):
        self._engine = engine

    def get_main_hwnd(self):
        """
        Windows specific method to find the main Alias window
        handle (HWND)
        """
        if not self._main_hwnd:
            hwnds = win_32_api.find_windows(class_name=self.HWND_CLASSNAME)
            if len(hwnds) > 0:
                self._main_hwnd = hwnds[0]

        return self._main_hwnd

    def get_proxy_window(self):
        """
        Windows specific method to get the proxy window that will 'own' all Toolkit dialogs.  This
        will be parented to the main Alias application.  Creates the proxy window
        if it doesn't already exist.
        """
        if not self._proxy_window:
            main_hwnd = self.get_main_hwnd()

            if not main_hwnd:
                return None

            self._proxy_window = QtGui.QWidget()
            self._proxy_window.setWindowTitle(self.PROXY_WINDOW_TITLE)

            proxy_window_id = self._proxy_window.winId()
            proxy_window_hwnd = win_32_api.qwidget_winid_to_hwnd(proxy_window_id)

            # set no parent notify
            proxy_window_style = win_32_api.GetWindowLong(proxy_window_hwnd, win_32_api.GWL_EXSTYLE)
            win_32_api.SetWindowLong(proxy_window_hwnd, win_32_api.GWL_EXSTYLE,
                                     proxy_window_style|win_32_api.WS_EX_NOPARENTNOTIFY)

            # parent to Alias application window
            win_32_api.SetParent(proxy_window_hwnd, main_hwnd)

        return self._proxy_window

    def get_dialog_parent(self):
        """
        Get the QWidget parent for all dialogs created through
        show_dialog & show_modal.
        """
        # determine the parent widget to use:
        if sys.platform == "win32":
            # for windows, we create a proxy window parented to the
            # main application window that we can then set as the owner
            # for all Toolkit dialogs
            return self.get_proxy_window()

        return self._engine.operations.get_parent_window()

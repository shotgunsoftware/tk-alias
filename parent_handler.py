import sys
import ctypes
from ctypes import wintypes


class ParentHandler(object):
    def __init__(self, pid):
        self._win32_alias_process_id = pid

    def _win32_get_alias_process_id(self):
        """
        Windows specific method to find the process id of Alias.  This
        assumes that it is the parent process of this python process
        """
        if hasattr(self, "_win32_alias_process_id"):
            return self._win32_alias_process_id
        self._win32_alias_process_id = None
        return self._win32_alias_process_id

    def _win32_get_alias_main_hwnd(self):
        """
        Windows specific method to find the main Alias window
        handle (HWND)
        """
        if hasattr(self, "_win32_alias_main_hwnd"):
            return self._win32_alias_main_hwnd
        self._win32_alias_main_hwnd = None

        # find alias process id:
        alias_process_id = self._win32_get_alias_process_id()

        if alias_process_id != None:
            # get main application window for alias process:
            from tk_alias import win_32_api
            found_hwnds = win_32_api.find_windows(process_id=alias_process_id, class_name="StudioProxy")
            if len(found_hwnds) >= 1:
                self._win32_alias_main_hwnd = found_hwnds[0]
        return self._win32_alias_main_hwnd

    def _win32_get_proxy_window(self):
        """
        Windows specific method to get the proxy window that will 'own' all Toolkit dialogs.  This
        will be parented to the main Alias application.  Creates the proxy window
        if it doesn't already exist.
        """
        if hasattr(self, "_win32_proxy_win"):
            return self._win32_proxy_win
        self._win32_proxy_win = None

        # get the main Alias window:
        ps_hwnd = self._win32_get_alias_main_hwnd()
        if ps_hwnd != None:

            from tank.platform.qt import QtGui
            from tk_alias import win_32_api

            # create the proxy QWidget:
            self._win32_proxy_win = QtGui.QWidget()
            self._win32_proxy_win.setWindowTitle('sgtk dialog owner proxy')

            proxy_win_hwnd = win_32_api.qwidget_winid_to_hwnd(self._win32_proxy_win.winId())

            # set no parent notify:
            win_ex_style = win_32_api.GetWindowLong(proxy_win_hwnd, win_32_api.GWL_EXSTYLE)
            win_32_api.SetWindowLong(proxy_win_hwnd, win_32_api.GWL_EXSTYLE,
                                     win_ex_style
                                     | win_32_api.WS_EX_NOPARENTNOTIFY)

            # parent to Alias application window:
            win_32_api.SetParent(proxy_win_hwnd, ps_hwnd)

        return self._win32_proxy_win

    def _get_dialog_parent(self):
        """
        Get the QWidget parent for all dialogs created through
        show_dialog & show_modal.
        """
        # determine the parent widget to use:
        parent_widget = None
        if sys.platform == "win32":
            # for windows, we create a proxy window parented to the
            # main application window that we can then set as the owner
            # for all Toolkit dialogs
            parent_widget = self._win32_get_proxy_window()
        else:
            from tank.platform.qt import QtGui
            parent_widget = QtGui.QApplication.activeWindow()

        return parent_widget

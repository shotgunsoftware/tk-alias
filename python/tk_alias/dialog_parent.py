# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
set of win32 functions used by Alias engine to manage toolkit UI under windows
"""
import ctypes
from ctypes import wintypes

from sgtk.platform.qt import QtCore
from sgtk.platform.qt import QtGui
from sgtk.util import is_windows

# user32.dll
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
)
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
SendMessage = ctypes.windll.user32.SendMessageW
SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutW
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
SetParent = ctypes.windll.user32.SetParent
RealGetWindowClass = ctypes.windll.user32.RealGetWindowClassW
EnableWindow = ctypes.windll.user32.EnableWindow
IsWindowEnabled = ctypes.windll.user32.IsWindowEnabled
GetWindowLong = ctypes.windll.user32.GetWindowLongW
SetWindowLong = ctypes.windll.user32.SetWindowLongW

# kernel32.dll
CloseHandle = ctypes.windll.kernel32.CloseHandle
CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
Process32First = ctypes.windll.kernel32.Process32FirstW
Process32Next = ctypes.windll.kernel32.Process32NextW

# some defines
TH32CS_SNAPPROCESS = 0x00000002
WM_GETTEXT = 0x000D
SMTO_ABORTIFHUNG = 0x0002
SMTO_BLOCK = 0x0001
GWL_EXSTYLE = -20
WS_EX_NOPARENTNOTIFY = 0x00000004
WS_EX_NOINHERITLAYOUT = 0x00100000


# structures
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_wchar * wintypes.MAX_PATH),
    ]


def find_parent_process_id(process_id):
    """
    Find the parent process id for a given process
    :param process_id: id of process to find parent of
    :returns: parent process id or None if parent not found
    """
    parent_process_id = None
    try:
        h_process_snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)

        ret = Process32First(h_process_snapshot, ctypes.byref(pe))
        while ret:
            if pe.th32ProcessID == process_id:
                parent_process_id = pe.th32ParentProcessID
                break
            ret = Process32Next(h_process_snapshot, ctypes.byref(pe))
    except Exception:
        pass
    else:
        CloseHandle(h_process_snapshot)

    return parent_process_id


def safe_get_window_text(hwnd):
    """
    Safely get the window text (title) of a specified window
    :param hwnd: window handle to get the text of
    :returns: window title if found
    """
    title = ""
    try:
        buffer_sz = 1024
        buffer = ctypes.create_unicode_buffer(buffer_sz)
        result = SendMessageTimeout(
            hwnd,
            WM_GETTEXT,
            buffer_sz,
            ctypes.byref(buffer),
            SMTO_ABORTIFHUNG | SMTO_BLOCK,
            100,
            0,
        )
        if result != 0:
            title = buffer.value
    except Exception:
        pass
    return title


def find_windows(
    process_id=None, class_name=None, window_text=None, stop_if_found=True
):
    """
    Find top level windows matching certain criteria
    :param process_id: only match windows that belong to this process id if specified
    :param class_name: only match windows that match this class name if specified
    :param window_text: only match windows that match this window text if specified
    :param stop_if_found: stop when find a match
    :returns: list of window handles found by search
    """
    found_hwnds = []

    # sub-function used to actually enumerate the windows in EnumWindows
    def enum_windows_proc(hwnd, lparam):
        # try to match process id:
        matches_proc_id = True
        if process_id is not None:
            win_process_id = ctypes.c_long()
            GetWindowThreadProcessId(hwnd, ctypes.byref(win_process_id))
            matches_proc_id = win_process_id.value == process_id
        if not matches_proc_id:
            return True

        # try to match class name:
        matches_class_name = True
        if class_name is not None:
            buffer_len = 1024
            buffer = ctypes.create_unicode_buffer(buffer_len)
            RealGetWindowClass(hwnd, buffer, buffer_len)
            matches_class_name = class_name == buffer.value
        if not matches_class_name:
            return True

        # try to match window text:
        matches_window_text = True
        if window_text is not None:
            hwnd_text = safe_get_window_text(hwnd)
            matches_window_text = window_text in hwnd_text
        if not matches_window_text:
            return True

        # found a match
        found_hwnds.append(hwnd)

        return not stop_if_found

    # enumerate all top-level windows:
    EnumWindows(EnumWindowsProc(enum_windows_proc), None)

    return found_hwnds


def qwidget_winid_to_hwnd(id):
    """
    Convert the winid for a qtwidget to a HWND
    :param id: qtwidget winid to convert
    :returns: window handle
    """
    if QtCore.__version__.startswith("5."):
        hwnd = id
    else:
        # Setup arguments and return types
        ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]

        # Convert PyCObject to a void pointer
        hwnd = ctypes.pythonapi.PyCObject_AsVoidPtr(id)

    return hwnd


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
            hwnds = find_windows(class_name=self.HWND_CLASSNAME)
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
            proxy_window_hwnd = qwidget_winid_to_hwnd(proxy_window_id)

            # set no parent notify
            proxy_window_style = GetWindowLong(proxy_window_hwnd, GWL_EXSTYLE)
            SetWindowLong(
                proxy_window_hwnd,
                GWL_EXSTYLE,
                proxy_window_style | WS_EX_NOPARENTNOTIFY,
            )

            # parent to Alias application window
            SetParent(proxy_window_hwnd, main_hwnd)

        return self._proxy_window

    def get_dialog_parent(self):
        """
        Get the QWidget parent for all dialogs created through
        show_dialog & show_modal.
        """
        # determine the parent widget to use:
        if is_windows():
            # for windows, we create a proxy window parented to the
            # main application window that we can then set as the owner
            # for all Toolkit dialogs
            return self.get_proxy_window()

        return self._engine.get_parent_window()

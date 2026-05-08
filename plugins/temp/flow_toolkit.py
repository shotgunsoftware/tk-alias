from __future__ import annotations

import os
import sys

# Add the framework path to sys.path for Alias's embedded Python interpreter
_fw_path = os.environ.get("TK_FRAMEWORK_ALIAS_PYTHON_PATH")
print(f"TK_FRAMEWORK_ALIAS_PYTHON_PATH: {_fw_path}")
if _fw_path and _fw_path not in sys.path:
    sys.path.insert(0, _fw_path)

import alias_api as alpy

from tk_framework_alias.server import AliasBridge

PLUGIN_VERSION = "dev"


def start():
    """Start the AliasBridge server and bootstrap the client application."""

    alias_bridge = AliasBridge()

    hostname = os.environ.get("ALIAS_PLUGIN_CLIENT_SIO_HOSTNAME")
    port_str = os.environ.get("ALIAS_PLUGIN_CLIENT_SIO_PORT")
    port = int(port_str) if port_str else -1

    max_retries = 0 if (hostname and port >= 0) else -1

    if not alias_bridge.start_server(hostname, port, max_retries):
        print("Failed to start Alias communication")
        return None

    print("Running Alias Python API server")

    client_name = os.environ.get("ALIAS_PLUGIN_CLIENT_NAME", "plugin-client")

    client_info = {
        "plugin_version": PLUGIN_VERSION,
        "alias_version": getattr(alpy, "__version__", "unknown"),
        "python_version": sys.version,
    }

    if alias_bridge.bootstrap_client(client_name, client_info):
        print(f"Starting client '{client_name}'...")

    return alias_bridge


alias_bridge = start()

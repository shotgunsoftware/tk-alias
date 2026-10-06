from __future__ import annotations

import os
import sys

# Add the framework path to sys.path for Alias's embedded Python interpreter
_fw_path = os.environ.get("TK_FRAMEWORK_ALIAS_PYTHON_PATH")
print(f"TK_FRAMEWORK_ALIAS_PYTHON_PATH: {_fw_path}")
if _fw_path and _fw_path not in sys.path:
    sys.path.insert(0, _fw_path)

try:
    import alias_api as alpy
except ImportError:
    import alias_api_d as alpy

from tk_framework_alias.server import AliasBridge

PLUGIN_VERSION = "dev"

_alias_bridge: AliasBridge | None = None


@alpy.plugin(
    name="Flow PT for Alias",
    description="Flow Production Tracking Toolkit integration for Alias",
    author="Autodesk",
    version="0.1",
)
class FlowToolkitAliasPlugin:
    """Register the Flow Production Tracking Toolkit plugin with Alias."""


@alpy.momentary_tool(keep_active_tool=True, attribute_string="fptalias")
class FlowToolkitTool:
    """Placeholder tool required by Alias plugin parser."""

    @alpy.on_activate
    def on_activate(self) -> None:
        alpy.log_to_prompt("Flow Production Tracking Toolkit for Alias activated")


@alpy.plugin_init
def initialize():
    """Start the AliasBridge server and bootstrap the client application."""
    global _alias_bridge

    _alias_bridge = AliasBridge()

    hostname = os.environ.get("ALIAS_PLUGIN_CLIENT_SIO_HOSTNAME")
    port_str = os.environ.get("ALIAS_PLUGIN_CLIENT_SIO_PORT")
    port = int(port_str) if port_str else -1

    max_retries = 0 if (hostname and port >= 0) else -1

    if not _alias_bridge.start_server(hostname, port, max_retries):
        print("Failed to start Alias communication")
        return

    print("Running Alias Python API server")

    client_name = os.environ.get("ALIAS_PLUGIN_CLIENT_NAME", "plugin-client")

    client_info = {
        "plugin_version": PLUGIN_VERSION,
        "alias_version": getattr(alpy, "__version__", "unknown"),
        "python_version": sys.version,
    }

    if _alias_bridge.bootstrap_client(client_name, client_info):
        print(f"Starting client '{client_name}'...")


@alpy.plugin_exit
def deinit():
    """Stop the AliasBridge server."""
    global _alias_bridge

    if _alias_bridge:
        try:
            _alias_bridge.stop_server()
        except Exception as exc:
            print(str(exc))

    _alias_bridge = None

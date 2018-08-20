# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
import os
import sys
import subprocess
from os.path import dirname, abspath, join
from sgtk.util import prepend_path_to_env_var


def compute_environment(extra_args, engine_name=None, context=None):
    env = {}
    
    startup_path = dirname(abspath(sys.modules[compute_environment.__module__].__file__))
    
    # extra args
    extra_args = extra_args or {}
    codename = extra_args.get("codename", "autostudio")
    if not codename:
        codename = "autostudio"
    
    os.environ["TK_ALIAS_CODENAME"] = extra_args.get("codename")
    env["TK_ALIAS_CODENAME"] = os.environ["TK_ALIAS_CODENAME"]
    
    resources = join(dirname(dirname(startup_path)), "resources")
    
    # Add Python dependencies directory to PYTHONPATH
    py_deps_dir = join(resources, "python")
    prepend_path_to_env_var("PYTHONPATH", py_deps_dir)
    
    # Add ZMQ library directory to PATH
    zmq_dir = join(resources, "libzmq", "dll")
    prepend_path_to_env_var("PATH", zmq_dir)
    env["PATH"] = os.environ["PATH"]
    
    # Get the path to the python executable
    python_binary = sys.executable
    
    # Get the path to the start.py
    start_path = abspath(join(startup_path, "start.py"))
    
    # Run start.py
    args = [python_binary, start_path]
    prepend_path_to_env_var("PYTHONPATH", dirname(dirname(startup_path)))
    env["PYTHONPATH"] = os.environ["PYTHONPATH"]
    set_port_number(choose_port_number())
    env["TK_ALIAS_PORT"] = os.environ["TK_ALIAS_PORT"]
    
    if engine_name:
        os.environ['SGTK_ENGINE'] = engine_name
        env['SGTK_ENGINE'] = os.environ['SGTK_ENGINE']
    
    if context:
        os.environ['TANK_CONTEXT'] = context
        env['TANK_CONTEXT'] = os.environ['TANK_CONTEXT']
    
    subprocess.Popen(args, close_fds=True)
    
    return env


def compute_args(app_args):
    startup_path = dirname(abspath(sys.modules[compute_args.__module__].__file__))
    app_args = app_args or ""
    
    resources = join(dirname(dirname(startup_path)), "resources")
    
    # Tell Alias to load our plugin
    plugin_list_file = register_plugin(resources)
    
    return_args = "{} -P {}".format(app_args, plugin_list_file)
    
    return return_args


def register_plugin(resources_dir):
    """
    Tell Alias to load our plugin.
    """
    plugin_path = join(resources_dir, "plugin", "shotgun.plugin")
    plugin_list_file = join(resources_dir, "plugin_list.txt")
    
    with open(plugin_list_file, "w+") as f:
        f.write("{}\n".format(plugin_path))
    
    return plugin_list_file


def choose_port_number():
    """
    Return an open port number.
    """
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))  # Bind to 0 to get a free port number
    sock.listen(1)
    
    port = sock.getsockname()[1]
    sock.close()
    
    return port


def set_port_number(port):
    """
    Store the chosen port number in an environment variable,
    where it is acccessible to the Engine and the Alias app.
    """
    os.environ["TK_ALIAS_PORT"] = str(port)
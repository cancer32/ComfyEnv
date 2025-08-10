import json
from pathlib import Path

from .common import is_process_running
from .exceptions import NoEnvFoundError


def get_env_status(config):
    """Get the status of a ComfyUI environment.

    Args:
        config (dict): Configuration dictionary containing environment details

    Returns:
        dict: Status information including running state, PID, port, and PID file info
    """
    env_name = config["env_name"]
    pid_file = config["pid_path"]
    comfyui_args = config.get("comfyui_args", [])
    
    # Default port
    port = 8188
    
    # Check for --port in comfyui_args
    if comfyui_args and "--port" in comfyui_args:
        try:
            port_index = comfyui_args.index("--port") + 1
            if port_index < len(comfyui_args):
                port = int(comfyui_args[port_index])
        except (ValueError, IndexError):
            # If port parsing fails, use default port
            pass


    status_info = {
        "env_name": env_name,
        "is_running": False,
        "pid": None,
        "port": None,
        "pid_file": None
    }

    pid = is_process_running(pid_file)
    if pid is False:
        return status_info

    status_info["pid_file"] = pid_file
    status_info["is_running"] = True
    status_info["pid"] = pid
    status_info["port"] = int(port)

    # Print status in JSON format
    print(json.dumps(status_info, indent=2), flush=True)
    return status_info

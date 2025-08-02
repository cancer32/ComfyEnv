import json
from pathlib import Path

from .env_config import get_envpref


def list_envs(config):
    envs = get_envpref(config["envpref_path"])
    if config["json"]:
        print(json.dumps(envs), flush=True)
        return
    print("# ComfyUI Environments:\n#", flush=True)
    for env_name, env_dir in envs.items():
        print(f"{env_name:<25}{Path(env_dir).parent}", flush=True)

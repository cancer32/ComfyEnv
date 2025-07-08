import os
from pathlib import Path

from .env_config import JsonParser


def list_envs(config):
    print("# ComfyUI Environments:\n#")
    env_root = Path(config["envs_root"])
    if not env_root.exists():
        return
    for env_dir in env_root.iterdir():
        env_config = env_dir / config["env_config_name"]
        if not env_config.exists():
            continue
        if JsonParser.load(env_config).get('env_created') == False:
            continue
        print(f"{env_dir.name:<25}{env_dir}")

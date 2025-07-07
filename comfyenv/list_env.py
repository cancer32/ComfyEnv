import os
from pathlib import Path

from .env_config import JsonParser


def list_envs(config):
    print("# ComfyUI Environments:\n#")
    for env_name in os.listdir(config["envs_root"]):
        env_config = Path(config["envs_root"]) / env_name / "config.json"
        if JsonParser.load(env_config).get('env_created') == False:
            continue
        print(f"{env_name:<25}{Path(config["envs_root"]) / env_name}")

import json
from pathlib import Path

from .env_config import JsonParser


def list_envs(config):
    envs = get_env_json(config=config)
    if config["json"]:
        print(json.dumps(envs), flush=True)
        return
    print("# ComfyUI Environments:\n#", flush=True)
    for env_name, env_dir in envs.items():
        print(f"{env_name:<25}{Path(env_dir).parent}", flush=True)


def get_env_json(config):
    env = {}
    env_root = Path(config["envs_root"])
    if not env_root.exists():
        return env

    for env_dir in env_root.iterdir():
        env_config = env_dir / config["env_config_name"]
        if not env_config.exists():
            continue
        if JsonParser.load(env_config).get('env_created') == False:
            continue
        env[env_dir.name] = str(env_config)

    return env
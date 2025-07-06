import os
from pathlib import Path

from .env_config import EnvConfig
from .common import get_user_shell


def get_config(args):
    config_path = Path(__file__).resolve().parent.parent / "envs" / args['env_name'] / "config.json"
    config = EnvConfig.load(config_path)
    config.update(args)
    return config


def activate_env(args):
    print(f'Activating environment {args["env_name"]}')
    config = get_config(args)
    if config['conda_only']:
        os.system(f'conda activate {config["conda_env_name"]} && {get_user_shell()}')
        return
    
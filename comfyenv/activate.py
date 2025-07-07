import os

from .common import get_user_shell


def activate_env(config):
    print(f'Activating environment {config["env_name"]}')
    os.system(f'conda activate {config["conda_env_name"]} && {get_user_shell()}')

import subprocess
from pathlib import Path

from comfyenv.env_config import EnvConfig


def get_config(args):
    config_path = Path(__file__).resolve().parent.parent / "envs" / args['env_name'] / "config.json"
    config = EnvConfig.load(config_path)
    config.update(args)
    return config


def run_comfyui(args):
    print(f'Starting ComfyUI from environment {args["env_name"]}')
    config = get_config(args)
    command = (f'conda run --live-stream -n {config["conda_env_name"]} '
               f'python {config["comfyenv_root"]}/run_comfy.py {config["env_config_path"]} ')
    s = subprocess.run(command, shell=True)


if __name__ == '__main__':
    import sys
    sys.argv[1]
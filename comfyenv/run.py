import subprocess
from pathlib import Path

from comfyenv.env_config import EnvConfig
from comfyenv.common import stop_process


def get_config(args):
    config_path = Path(__file__).resolve().parent.parent / "envs" / args['env_name'] / "config.json"
    config = EnvConfig.load(config_path)
    config.update(args)
    return config


def run_comfyui(args):
    print(f'Starting ComfyUI from the environment \"{args["env_name"]}\"')
    config = get_config(args=args)
    config.dump()
    command = (
        f'conda run --live-stream -n {config["conda_env_name"]} '
        f'python \"{config["comfyenv_root"]}/run_comfy.py\" {config['env_config_path']}'
    )
    try:
        subprocess.run(command, shell=True)
    except:
        pass


def stop_comfyui(args):
    print(f'Stopping ComfyUI from the environment \"{args["env_name"]}\"')
    config = get_config(args=args)
    pid_path = config["pid_path"]
    stop_process(pid_path)

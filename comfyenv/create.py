import os
from pathlib import Path
import subprocess

from .env_config import JsonParser
from .torch_cuda import get_pytorch_cuda
from .common import copy_extra_model_config


def create_env(config):
    # Create directories
    os.makedirs(f"{config['user_dir']}/input", exist_ok=True)
    os.makedirs(f"{config['user_dir']}/output", exist_ok=True)
    os.makedirs(config['models_dir'], exist_ok=True)
    os.makedirs(config['env_dir'], exist_ok=True)
    os.makedirs(config['user_dir'], exist_ok=True)

    # Check if conda env exists
    conda_env_exists = False
    conda_envs = JsonParser.loads(
        subprocess.check_output('conda env list --json', shell=True))
    for conda_env in conda_envs['envs']:
        if config["conda_env_name"] == Path(conda_env).name:
            conda_env_exists = True
            break

    if not conda_env_exists:
        print(f"Creating environment '{config['env_name']}' "
              f"with Python {config['python']}")
        subprocess.run(f'conda create -y -n {config["conda_env_name"]} python=={config["python"]}',
                       shell=True)

    if config['with_torch']:
        print(f'Installing pytorch...')
        subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                       f'pip install torch torchvision torchaudio '
                       f'--index-url https://download.pytorch.org/whl/{get_pytorch_cuda()}',
                       shell=True)

    # Pulling comfyui
    subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                   f'git submodule update --remote {config["comfyui_dir_name"]}',
                   shell=True, cwd=config["comfyenv_root"])

    # Installing required modules in both envs
    subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                   f'pip install psutil',
                   shell=True)

    # Installing comfyui's requirements.txt
    subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                   f'python -m pip install --upgrade '
                   f'pip -r "{config["comfyui_root"]}/requirements.txt"',
                   shell=True)

    # Installing/Updating ComfyUI-Manager
    comfy_manager_dir = f'{config["env_dir"]}/custom_nodes/comfyui-manager'
    if (Path(comfy_manager_dir) / ".git").exists():
        subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                       f'git pull',
                       shell=True, cwd=comfy_manager_dir)
    else:
        subprocess.run(f'conda run --live-stream -n {config["conda_env_name"]} '
                       f'git clone "https://github.com/ltdrdata/ComfyUI-Manager" "{comfy_manager_dir}"',
                       shell=True)

    # Copying extra_model_config
    copy_extra_model_config(config=config)

    # Savning env config
    config['env_created'] = True
    config.dump(config['env_config_path'])

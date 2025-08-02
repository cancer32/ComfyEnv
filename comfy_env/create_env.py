import os
from pathlib import Path
import subprocess

from .env_config import JsonParser, get_envpref
from .torch_cuda import get_pytorch_cuda
from .common import copy_extra_model_config


def run_command(cmd, raise_error=True, **kwargs):
    process = subprocess.Popen(cmd, **kwargs)
    process.communicate()  # wait for the process to finish
    if raise_error and process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode, cmd
        )


def create_update_env(config):
    # Create directories
    os.makedirs(f"{config['user_dir']}/input", exist_ok=True)
    os.makedirs(f"{config['user_dir']}/output", exist_ok=True)
    os.makedirs(config['envs_root'], exist_ok=True)
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
              f"with Python {config['python']}", flush=True)
        run_command(f'conda create -y -n {config["conda_env_name"]} python=={config["python"]}',
                    shell=True)

    # Installing pytorch
    print(f'Installing pytorch...', flush=True)
    torch_requirements = (Path(config["COMFYENV_ROOT"])
                          / "torch_requirements.txt")
    torch_dep = (torch_requirements.read_text()
                 .replace('\n', ' ')
                 .replace('{TORCH_CUDA}', get_pytorch_cuda()))
    run_command(f'conda run --live-stream -n {config["conda_env_name"]} '
                f'pip install {torch_dep}',
                shell=True)

    # Pulling comfyui
    comfyui_root = Path(config["comfyui_root"])
    if (comfyui_root / ".git").exists():
        cmd = 'git stash'
        cmd += ' && git checkout master'
        cmd += ' && git pull'
        if config["comfyui_version"] != "latest":
            cmd += f' && git checkout tags/{config["comfyui_version"]}'
        run_command(cmd, shell=True, cwd=comfyui_root)
        run_command('git stash pop', raise_error=False, shell=True, cwd=comfyui_root)
    else:
        run_command(f'git clone "https://github.com/comfyanonymous/ComfyUI.git" '
                    f'"{comfyui_root}"',
                    shell=True)

    # Installing comfyui's requirements.txt
    run_command(f'conda run --live-stream -n {config["conda_env_name"]} '
                f'pip install psutil==7.0.0 '
                f'-r "{config["comfyui_root"]}/requirements.txt" ',
                shell=True)

    # Installing/Updating ComfyUI-Manager
    comfy_manager_dir = f'{config["env_dir"]}/custom_nodes/comfyui-manager'
    if (Path(comfy_manager_dir) / ".git").exists():
        run_command(f'git pull',
                    shell=True, cwd=comfy_manager_dir)
    else:
        run_command(f'git clone "https://github.com/ltdrdata/ComfyUI-Manager" '
                    f'"{comfy_manager_dir}"',
                    shell=True)
    run_command(f'conda run --live-stream -n {config["conda_env_name"]} '
                f'pip install '
                f'-r "{comfy_manager_dir}/requirements.txt" ',
                shell=True)

    if config["command"] == "create":
        # Copying extra_model_config
        copy_extra_model_config(config=config)
        # Savning env config
        config['env_created'] = True
        config.dump(config['env_config_path'])
        # Put env in envpref file
        envpref = get_envpref(config["envpref_path"])
        envpref[config["env_name"]] = config['env_config_path']
        envpref.dump()

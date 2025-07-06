import os
from pathlib import Path
from tempfile import gettempdir
import subprocess

from .env_config import EnvConfig, JsonParser
from .torch_cuda import get_pytorch_cuda


def get_config(config_path, args):
    config = EnvConfig.load(config_path)
    config.update(args)
    config["HOME"] = str(Path.home())
    config["TEMP"] = gettempdir()
    config["USERNAME"] = os.getlogin()
    config["COMFYENV_ROOT"] = str(Path(__file__).resolve().parent.parent)
    config["conda_env_name"] = args.get(
        "conda_env_name",
        ('comfyui' + ''.join(args.get("python", "3.12.*").split('.')[0:2]))
    )
    return config


def create_env(config_path, args):
    config = get_config(config_path, args)

    # Create directories
    os.makedirs(f"{config['user_dir']}/input", exist_ok=True)
    os.makedirs(f"{config['user_dir']}/output", exist_ok=True)
    os.makedirs(config['models_dir'], exist_ok=True)
    os.makedirs(config['env_dir'], exist_ok=True)
    os.makedirs(config['user_dir'], exist_ok=True)

    # Check if conda env exists
    conda_env_exists = False
    conda_envs = JsonParser.loads(subprocess.check_output('conda env list --json', shell=True))
    for conda_env in conda_envs['envs']:
        if config["conda_env_name"] == Path(conda_env).name:
            conda_env_exists = True
            break

    if not conda_env_exists:
        print(f"Creating environment '{config['env_name']}' with Python {config['python']}")
        os.system(f'conda create -y -n {config["conda_env_name"]} python=={config["python"]}')

    if config['with_torch']:
        print(f'Installing pytorch...')
        subprocess.run(f'conda run -n {config["conda_env_name"]} ' \
                       f'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/{get_pytorch_cuda()}', shell=True)

    config.dump(config['env_config_path'])

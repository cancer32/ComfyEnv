import os
import traceback
from tempfile import gettempdir
from pathlib import Path

from comfy_env.exceptions import (NoEnvFoundError, NoProcessFoundError,
                                  AlreadyRunningError)
from comfy_env.env_config import EnvConfig, manage_config, get_envpref
from comfy_env.args import get_args
from comfy_env.create_env import create_update_env
from comfy_env.activate import activate_env
from comfy_env.run_env import run_comfyui, stop_comfyui
from comfy_env.list_env import list_envs
from comfy_env.remove_env import remove_env
from comfy_env.status_env import get_env_status
from comfy_env.version import __version__

# Variables
ROOT_DIR = Path(__file__).resolve().parent


def get_config(args, config_path=None):
    default_config_path = ROOT_DIR / 'config.json'
    default_config = EnvConfig.load(default_config_path)

    _loaded_default_config = False
    if config_path is None:
        config_path = default_config_path
        _loaded_default_config = True

    config = EnvConfig.load(config_path)
    config.update(args)
    if _loaded_default_config:
        config["HOME"] = str(Path.home())
        config["TEMP"] = gettempdir()
        config["USERNAME"] = os.getlogin()
        config["COMFYENV_ROOT"] = str(ROOT_DIR)
        config["conda_env_name"] = args.get("conda_env_name",
                                            config["env_name"])
    # Get envpref_path from default config always
    config["envpref_path"] = default_config["envpref_path"]
    return config


def find_config(args):
    default_config = EnvConfig.load(ROOT_DIR / 'config.json')
    default_config["COMFYENV_ROOT"] = str(ROOT_DIR)
    envpref = get_envpref(default_config["envpref_path"])
    if args["env_name"] not in envpref:
        raise NoEnvFoundError(f'Could not find comfyui environment: '
                              f'"{args["env_name"]}"')
    return envpref[args["env_name"]]


def main():
    args = get_args()
    ret = 0
    try:
        if args['command'] == "create":
            create_update_env(get_config(args=args))
        elif args['command'] == "update":
            create_update_env(get_config(args=args,
                                         config_path=find_config(args)))
        elif args['command'] == "activate":
            activate_env(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "stop":
            stop_comfyui(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "run":
            run_comfyui(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "list":
            list_envs(get_config(args=args))
        elif args['command'] == "config":
            manage_config(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "remove":
            remove_env(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "status":
            get_env_status(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "version":
            print(__version__, flush=True)
    except (NoEnvFoundError, NoProcessFoundError,
            AlreadyRunningError, ValueError) as e:
        print(f'Error: {str(e)}', flush=True)
        ret = 1
    except Exception as e:
        traceback.print_exception(e)
        ret = 1
    return ret


if __name__ == '__main__':
    os._exit(main())

import os
import traceback
from tempfile import gettempdir
from pathlib import Path

from comfyenv.exceptions import (NoEnvFoundError, NoProcessFoundError,
                                 AlreadyRunningError)
from comfyenv.env_config import EnvConfig, manage_config, get_envpref
from comfyenv.args import get_args
from comfyenv.create import create_update_env
from comfyenv.activate import activate_env
from comfyenv.run import run_comfyui, stop_comfyui
from comfyenv.list import list_envs
from comfyenv.remove import remove_env

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
            remove_env(get_config(args=args))
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

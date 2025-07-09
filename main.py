import os
from tempfile import gettempdir
from pathlib import Path

from comfyenv.env_config import EnvConfig
from comfyenv.args import get_args
from comfyenv.create import create_update_env
from comfyenv.activate import activate_env
from comfyenv.run import run_comfyui, stop_comfyui
from comfyenv.list import list_envs
from comfyenv.remove import remove_env

# Variables
ROOT_DIR = Path(__file__).resolve().parent


def get_config(args, config_path=None):
    _loaded_default_config = False
    if config_path is None:
        config_path = ROOT_DIR / 'config.json'
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
    return config


def find_config(args):
    config_path = ROOT_DIR / "envs" / args['env_name'] / "config.json"
    if not config_path.exists():
        raise IOError(f'Error: could not find the environment: '
                      f'{args["env_name"]}')
    return config_path


def main():
    args = get_args()
    ret = 0
    try:
        if args['command'] == "create":
            create_update_env(get_config(args=args))
        elif args['command'] == "update":
            create_update_env(
                get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "activate":
            activate_env(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "stop":
            stop_comfyui(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "run":
            run_comfyui(get_config(args=args, config_path=find_config(args)))
        elif args['command'] == "list":
            list_envs(get_config(args=args))
        elif args['command'] == "remove":
            remove_env(get_config(args=args))

    except Exception as e:
        print(f'Error: {str(e)}')
        ret = 1
    return ret


if __name__ == '__main__':
    os._exit(main())

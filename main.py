from pathlib import Path

from comfyenv.args import get_args
from comfyenv.create import create_env
from comfyenv.activate import activate_env
from comfyenv.run import run_comfyui

# Variables
ROOT_DIR = Path(__file__).resolve().parent


if __name__ == '__main__':
    args = get_args()

    if args['command'] == "create":
        create_env(config_path=ROOT_DIR / 'config.json', args=args)

    elif args['command'] == "activate":
        activate_env(args)

    elif args['command'] == "install":
        print(f'Installing package {args["package"]} into the active environment')

    elif args['command'] == "run":
        run_comfyui(args)
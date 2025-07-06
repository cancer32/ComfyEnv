from pathlib import Path

from comfyenv.args import get_args
from comfyenv.create import create_env

# Variables
ROOT_DIR = Path(__file__).resolve().parent


if __name__ == '__main__':
    args = get_args()

    if args['command'] == "create":
        create_env(config_path=ROOT_DIR / 'config.json', args=args)

    elif args['command'] == "activate":
        print(f"Activating environment '{args['env_name']}'")

    elif args['command'] == "install":
        print(f"Installing package '{args['package']}' into the active environment")

    elif args['command'] == "run":
        print(f"Installing package '{args['package']}' into the active environment")
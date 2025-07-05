from os import getlogin
from pathlib import Path
from tempfile import gettempdir 

from comfyenv.args import get_args
from comfyenv.env_config import EnvConfig

# Variables
ROOT_DIR = Path(__file__).resolve().parent


if __name__ == '__main__':
    args = get_args()
    config = EnvConfig.load(ROOT_DIR / 'config.json')
    config["HOME"] = str(Path.home())
    config["TEMP"] = gettempdir()
    config["USERNAME"] = getlogin()
    config["COMFYENV_ROOT"] = str(Path(__file__).resolve().parent)
    config.update(args)

    if args['command'] == "create":
        print(f"Creating environment '{config['env_name']}' with Python {config['python']}")
        if config['no_torch']:
            print("Torch will not be installed.")
        if config['conda_env_name']:
            print(f"Using custom conda env name: {config['conda_env_name']}")

    elif args['command'] == "activate":
        print(f"Activating environment '{config['env_name']}'")

    elif args['command'] == "install":
        print(f"Installing package '{config['package']}' into the active environment")
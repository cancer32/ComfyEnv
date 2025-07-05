import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(ROOT_DIR, 'lib')
if lib_path not in sys.path:
	sys.path.append(lib_path)

from comfyenv.args import get_args


if __name__ == '__main__':
    args = get_args()
    print(vars(args))  # Debug print

    if args.command == "create":
        print(f"Creating environment '{args.env_name}' with Python {args.python}")
        if args.no_torch:
            print("Torch will not be installed.")
        if args.conda_name:
            print(f"Using custom conda env name: {args.conda_name}")

    elif args.command == "activate":
        print(f"Activating environment '{args.env_name}'")

    elif args.command == "install":
        print(f"Installing package '{args.package}' into the active environment")
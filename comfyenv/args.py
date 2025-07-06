import argparse


def get_args():
    parser = argparse.ArgumentParser(prog="comfyenv", description="Environment manager for ComfyUI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser.add_argument("--list", action='store_true', help="List all environments")
    parser.add_argument("--list-conda", action='store_true', help="List all conda environments")

    # comfyenv create <env-name> --python=3.10
    create_parser = subparsers.add_parser("create", help="Create a new environment")
    create_parser.add_argument("-n", "--name", required=True, dest="env_name", help="Name of the environment to create")
    create_parser.add_argument("--python", help="Python version for the environment (e.g., 3.10)")
    create_parser.add_argument("--user-root", help="Custom user root directory path")
    create_parser.add_argument("--envs-root", help="Custom environment root directory path")
    create_parser.add_argument("--conda-env-name", help="Optional: custom name for the conda environment")
    create_parser.add_argument("--with-torch", action="store_true", help="Install the py torch library with cuda")

    # comfyenv remove <env-name>
    remove_parser = subparsers.add_parser("remove", help="Remove an environment")
    remove_parser.add_argument("-n", "--name", required=True, dest="env_name", help="Name of the environment to create")

    # comfyenv activate <env-name>
    activate_parser = subparsers.add_parser("activate", help="Activate an existing environment")
    activate_parser.add_argument("-n", "--name", required=True, dest="env_name", help="Name of the environment to activate")

    # comfyenv install <package-name>
    install_parser = subparsers.add_parser("install", help="Install a package (e.g., custom node) into the active environment")
    install_parser.add_argument("package", help="Name of the package to install")

    # comfyenv run <env-name> -- <comfyui args>
    run_parser = subparsers.add_parser("run", help="Run ComfyUI inside a specific environment")
    run_parser.add_argument("-n", "--name", required=True, dest="env_name", help="Name of the environment to run")
    run_parser.add_argument("comfyui_args", nargs=argparse.REMAINDER, help="Additional arguments passed to ComfyUI")

    args = parser.parse_args().__dict__
    print(args)
    return dict((k,v) for k,v in args.items() if v is not None)
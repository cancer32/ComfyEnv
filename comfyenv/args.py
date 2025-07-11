import argparse


def get_args():
    parser = argparse.ArgumentParser(prog="comfyenv",
                                     description="Environment manager for ComfyUI")
    subparsers = parser.add_subparsers(dest="command",
                                       required=True)

    # comfyenv list
    list_parser = subparsers.add_parser("list",
                                        help="List all the environments")
    list_parser.add_argument("-j", "--json", action="store_true",
                             help="Output list of environments in json format")

    # comfyenv create <env-name> --python=3.10
    create_parser = subparsers.add_parser("create",
                                          help="Create a new environment")
    create_parser.add_argument("-n", "--name", required=True,
                               dest="env_name", help="Name of the environment to create")
    create_parser.add_argument("--python",
                               help="Python version for the environment (e.g., 3.10)")
    create_parser.add_argument("--user-root",
                               help="Custom user root directory path")
    create_parser.add_argument("--envs-root",
                               help="Custom environment root directory path")
    create_parser.add_argument("--conda-env-name",
                               help="Optional: custom name for the conda environment")
    create_parser.add_argument("--comfyui-version",
                               help="ComfyUI version tag to checkout, eg 'v0.3.43' default: latest")

    # comfyenv update -n <env-name>
    update_parser = subparsers.add_parser("update",
                                          help="Update given environment")
    update_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment to create")

    # comfyenv config -n <env-name>
    config_parser = subparsers.add_parser("config",
                                          help="Get/Set the config of the given environment")
    config_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment")
    config_parser.add_argument("-e", "--edit", action="store_true",
                               help="Open the config file to edit")

    # comfyenv remove -n <env-name>
    remove_parser = subparsers.add_parser("remove",
                                          help="Remove the given environment data")
    remove_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment to create")
    remove_parser.add_argument("-y", "--yes", action="store_true",
                               help="wont ask for confirmation prompt")

    # comfyenv activate -n <env-name>
    activate_parser = subparsers.add_parser("activate",
                                            help="Activate an existing environment")
    activate_parser.add_argument("-n", "--name", required=True, dest="env_name",
                                 help="Name of the environment to activate")

    # comfyenv stop -n <env-name>
    stop_parser = subparsers.add_parser("stop",
                                        help="Stops the current running comfyui process from given environment")
    stop_parser.add_argument("-n", "--name", required=True, dest="env_name",
                             help="Name of the environment to stop")

    # comfyenv run -n <env-name> -- <comfyui args>
    run_parser = subparsers.add_parser("run",
                                       help="Run ComfyUI inside a specific environment")
    run_parser.add_argument("-n", "--name", required=True, dest="env_name",
                            help="Name of the environment to run")
    run_parser.add_argument("comfyui_args", nargs=argparse.REMAINDER,
                            help="Additional arguments passed to ComfyUI")

    args = parser.parse_args().__dict__
    return dict((k, v) for k, v in args.items() if v not in (None, []))

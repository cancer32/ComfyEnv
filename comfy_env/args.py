import argparse


def get_args():
    parser = argparse.ArgumentParser(prog="comfy_env",
                                     description="Environment manager for ComfyUI")
    subparsers = parser.add_subparsers(dest="command",
                                       required=True)

    # comfy_env list
    list_parser = subparsers.add_parser("list",
                                        help="List all the environments")
    list_parser.add_argument("-j", "--json", action="store_true",
                             help="Output list of environments in json format")

    # comfy_env create <env-name> --python=3.10
    create_parser = subparsers.add_parser("create",
                                          help="Create a new environment")
    create_parser.add_argument("-n", "--name", required=True,
                               dest="env_name", help="Name of the environment to create")
    create_parser.add_argument("--python",
                               help="Python version for the environment (e.g., 3.12.*)")
    create_parser.add_argument("--user-root",
                               help="Custom user root directory path")
    create_parser.add_argument("--envs-root",
                               help="Custom environment root directory path")
    create_parser.add_argument("--conda-env-name",
                               help="Optional: custom name for the conda environment")
    create_parser.add_argument("--comfyui-version",
                               help="ComfyUI version tag to checkout, eg 'v0.3.43' default: latest")

    # comfy_env update -n <env-name>
    update_parser = subparsers.add_parser("update",
                                          help="Update given environment")
    update_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment to create")

    # comfy_env config -n <env-name>
    config_parser = subparsers.add_parser("config",
                                          help="Get/Set the config of the given environment")
    config_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment")
    config_parser.add_argument("-e", "--edit", action="store_true",
                               help="Open the config file to edit")

    # comfy_env remove -n <env-name>
    remove_parser = subparsers.add_parser("remove",
                                          help="Remove the given environment data")
    remove_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment to create")
    remove_parser.add_argument("-y", "--yes", action="store_true",
                               help="wont ask for confirmation prompt")

    # comfy_env activate -n <env-name>
    activate_parser = subparsers.add_parser("activate",
                                            help="Activate an existing environment")
    activate_parser.add_argument("-n", "--name", required=True, dest="env_name",
                                 help="Name of the environment to activate")

    # comfy_env stop -n <env-name>
    stop_parser = subparsers.add_parser("stop",
                                        help="Stops the current running comfyui process from given environment")
    stop_parser.add_argument("-n", "--name", required=True, dest="env_name",
                             help="Name of the environment to stop")

    # comfy_env run -n <env-name> -- <comfyui args>
    run_parser = subparsers.add_parser("run",
                                       help="Run ComfyUI from an environment")
    run_parser.add_argument("-n", "--name", required=True, dest="env_name",
                            help="Name of the environment to run")
    run_parser.add_argument("comfyui_args", nargs=argparse.REMAINDER,
                            help="Additional arguments passed to ComfyUI")

    # comfy_env status -n <env-name>
    status_parser = subparsers.add_parser("status",
                                          help="Get the status of a ComfyUI environment")
    status_parser.add_argument("-n", "--name", required=True, dest="env_name",
                               help="Name of the environment to check")

    # comfy_env version
    version_parser = subparsers.add_parser("version",
                                           help="Print the comfy_env version")

    args = parser.parse_args().__dict__
    return dict((k, v) for k, v in args.items() if v not in (None, []))

import subprocess

from comfy_env.common import stop_process


def run_comfyui(config):
    print(f'Starting ComfyUI from the environment \"{config["env_name"]}\"',
          flush=True)

    # Setting the arguments in config
    comfyui_args = config.get("comfyui_args", [])
    
    # Remove '--' if present
    if '--' in comfyui_args:
        comfyui_args.remove('--')
    
    # Check if port is specified in args
    if '--port' not in comfyui_args:
        # Add default port if not specified
        comfyui_args.extend(['--port', '8188'])
    
    config["comfyui_args"] = comfyui_args
    config.dump()

    command = (
        f'conda run --live-stream -n {config["conda_env_name"]} '
        f'python \"{config["comfyenv_root"]}/comfyui_main.py\" {config["env_config_path"]}'
    )
    subprocess.run(command, shell=True)


def stop_comfyui(config):
    print(f'Stopping ComfyUI from the environment \"{config["env_name"]}\"',
          flush=True)
    pid_path = config["pid_path"]
    return stop_process(pid_path)

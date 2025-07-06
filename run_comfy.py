import subprocess

from comfyenv.env_config import EnvConfig


def run_comfyui(config_path):
    config = EnvConfig.load(config_path)
    print(f'Starting ComfyUI from environment {config["env_name"]}')
    command = (
        f'python \"{config["comfyui_root"]}/main.py\" '
        f'--base-directory \"{config["env_dir"]}\" '
        f'--output-directory \"{config["user_dir"]}/output\" '
        f'--temp-directory \"{config["temp_dir"]}\" '
        f'--input-directory \"{config["user_dir"]}/input\" '
        f'--extra-model-paths-config \"{config["extra_model_paths_config_path"]}\" '
        f'--user-directory \"{config["user_dir"]}\" '
        f'--enable-cors-header --disable-auto-launch '
        #f"--port {port} --listen "
    )
    s = subprocess.Popen(command, shell=False)
    print(s.pid)
    s.wait()


if __name__ == '__main__':
    import sys
    run_comfyui(sys.argv[1])
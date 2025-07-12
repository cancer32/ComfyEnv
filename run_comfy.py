import os
import sys
import shlex

from comfyenv.env_config import EnvConfig
from comfyenv.common import create_pid, remove_pid
from comfyenv.exceptions import AlreadyRunningError


def main(args):
    config = EnvConfig.load(args[1])
    sys.path.append(config["comfyui_root"])

    main_py = f'{config["comfyui_root"]}/main.py'
    pid_path = config["pid_path"]

    try:
        idx = config["comfyui_args"].index('--port') + 1
        port = config["comfyui_args"][idx]
    except (ValueError, IndexError):
        port = 8188

    try:
        create_pid(pid_path, port)
    except AlreadyRunningError as e:
        print('Error: %s' % str(e), flush=True)
        return 1

    new_args = shlex.split(
        f'"{main_py}" '
        f'--output-directory \"{config["user_dir"]}/output\" '
        f'--temp-directory \"{config["temp_dir"]}\" '
        f'--input-directory \"{config["user_dir"]}/input\" '
        f'--extra-model-paths-config \"{config["extra_model_paths_config_path"]}\" '
        f'--user-directory \"{config["user_dir"]}\" '
        f'--enable-cors-header '
        f'--listen '
    )
    sys.argv = new_args + config["comfyui_args"]

    ret = 0
    with open(main_py) as f:
        try:
            code = compile(f.read(), "main.py", 'exec')
            exec(code, {'__name__': '__main__', '__file__': main_py})
            ret = 0
        except Exception as e:
            print('Error: %s' % str(e), flush=True)
            ret = 1
        finally:
            remove_pid(pid_path)

    return ret


if __name__ == '__main__':
    os._exit(main(sys.argv))

import os
import sys
import shlex

from comfyenv.env_config import EnvConfig
from comfyenv.common import create_pid, remove_pid


def main(args):
    ret = 0
    config = EnvConfig.load(args[1])
    sys.path.append(config["comfyui_root"])

    main_py = f'{config["comfyui_root"]}/main.py'
    pid_path = config["pid_path"]
    create_pid(pid_path)

    new_args = shlex.split(
        f'"{main_py}" '
        f'--base-directory \"{config["env_dir"]}\" '
        f'--output-directory \"{config["user_dir"]}/output\" '
        f'--temp-directory \"{config["temp_dir"]}\" '
        f'--input-directory \"{config["user_dir"]}/input\" '
        f'--extra-model-paths-config \"{config["extra_model_paths_config_path"]}\" '
        f'--user-directory \"{config["user_dir"]}\" '
        f'--enable-cors-header '
        f'--disable-auto-launch '
        f'--listen '
    )
    comfyui_args = list(config["comfyui_args"])
    if '--' in comfyui_args:
        comfyui_args.remove('--')
    sys.argv = new_args + comfyui_args

    with open(main_py) as f:
        try:
            code = compile(f.read(), "main.py", 'exec')
            exec(code, {'__name__': '__main__', '__file__' : main_py})
            ret = 0
        except Exception as e:
            print('Error: %s' % str(e))
            ret = 1
        finally:
            remove_pid(pid_path)

    return ret


if __name__ == '__main__':
    os._exit(main(sys.argv))

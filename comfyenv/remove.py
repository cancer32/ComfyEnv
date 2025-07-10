import os
import subprocess
import shutil
from pathlib import Path

from .common import get_user_shell
from .env_config import JsonParser


def remove_env(config):
    env_dir = Path(config["env_dir"])
    if not env_dir.exists():
        raise ValueError(f'Could not find environment "{config["env_name"]}"')

    if not config["yes"]:
        ans = input(f'Are you sure want to remove '
                    f'"{config["env_name"]}" ? (yes/[no]): ')
        if ans.lower() not in ('yes', 'y'):
            return
    print(f'Removing environment "{config['env_name']}"', flush=True)
    subprocess.run(f'conda env remove -y -n {config["conda_env_name"]}',
                   shell=True)

    shell = get_user_shell()
    if 'cmd.exe' in shell.lower():
        os.system(f'rmdir /S /Q "{env_dir}"')
    elif 'bash' in shell:
        os.system(f'rm -fr "{env_dir}"')
    else:
        shutil.rmtree(env_dir)

    # Remove env from envpref file
    envpref = JsonParser.load(config["envpref_path"])
    envpref.pop(config["env_name"])
    envpref.dump()
    print("Done", flush=True)

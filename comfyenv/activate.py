import os

from .common import get_user_shell


def activate_env(config):
    print(f'Activating environment {config["env_name"]}')
    shell = get_user_shell()
    if 'cmd.exe' in shell.lower():
        os.system(f'conda activate {config["conda_env_name"]} '
                  f'&& {get_user_shell()}')
    elif 'bash' in shell.lower():
        bash_script = f'''
        source $CONDA_ROOT/etc/profile.d/conda.sh;
        conda activate {config["conda_env_name"]};
        exec {shell} --noprofile --norc;
        '''
        os.system(f'{shell} -i -c "{bash_script}"')

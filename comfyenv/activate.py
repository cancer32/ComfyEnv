import subprocess

from .common import get_user_shell


def activate_env(config):
    print(f'Activating environment {config["env_name"]}')
    shell = get_user_shell()
    if 'cmd.exe' in shell.lower():
        subprocess.run(f'{shell} /K conda activate {config["env_name"]}',
                       shell=True,
                       cwd=config["env_dir"])
    elif 'bash' in shell.lower():
        bash_script = f'''
        source $CONDA_ROOT/etc/profile.d/conda.sh;
        conda activate {config["conda_env_name"]};
        exec {shell} --noprofile --norc;
        '''
        subprocess.run(f'{shell} -i -c "{bash_script}"',
                       shell=True,
                       cwd=config["env_dir"])

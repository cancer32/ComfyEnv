import subprocess

from .common import get_user_shell


def activate_env(config):
    print(f'Activating environment {config["pkgmgr_env_name"]}')
    shell = get_user_shell()
    if 'cmd.exe' in shell.lower():
        cmd = f'{config["pkgmgr"]} activate {config["pkgmgr_env_name"]}'
        subprocess.run(f'{shell} /K {cmd}', cwd=config["env_dir"])
    elif 'bash' in shell.lower():
        bash_script = "Script to activate micromamba"
        if config["pkgmgr"] == "conda":
            bash_script = f'''
            source $CONDA_ROOT/etc/profile.d/pkgmgr.sh;
            pkgmgr activate {config["pkgmgr_env_name"]};
            exec {shell} --noprofile --norc;
            '''
        subprocess.run(f'{shell} -i -c "{bash_script}"',
                       shell=True,
                       cwd=config["env_dir"])

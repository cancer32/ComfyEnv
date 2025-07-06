import os
import platform
import shutil


def get_user_shell():
    system = platform.system()

    if system == 'Windows':
        # Try to get COMSPEC (usually cmd.exe), fallback to powershell
        shell = os.environ.get('COMSPEC')  # Usually C:\Windows\System32\cmd.exe
        if not shell:
            # Fallback: check for PowerShell
            shell = shutil.which('powershell') or shutil.which('cmd')
        return shell

    elif system in ('Linux', 'Darwin'):  # Darwin = macOS
        # Try SHELL environment variable
        shell = os.environ.get('SHELL')
        if shell:
            return shell
        else:
            # Try using getent passwd
            try:
                import pwd
                return pwd.getpwuid(os.getuid()).pw_shell
            except Exception:
                return '/bin/sh'  # Safe default
    else:
        return None  # Unknown OS


def copy_extra_model_config(config):
    source_config = f'{config["comfyenv_root"]}/{config["extra_model_paths_config"]}.tmp'
    dest_config = config["extra_model_paths_config_path"]
    shutil.copy(source_config, dest_config)
    # Replace BASE_PATH with the actual models directory path
    with open(dest_config, "r") as file:
        content = file.read()
    content = content.replace("ENV_DIR", config["models_dir"])
    with open(dest_config, "w") as file:
        file.write(content)
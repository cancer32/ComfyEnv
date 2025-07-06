import os
import sys
import platform
import shutil
import psutil


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


def is_process_running(pid_path):
    pid_exists = os.path.exists(pid_path)
    pid = None
    if not pid_exists:
        return False
    with open(pid_path, 'r') as f:
        pid = int(f.read().strip())
    if not pid:
        return False
    return pid if psutil.pid_exists(pid) else False


def stop_process(pid_path):
    false_or_pid = is_process_running(pid_path)
    if false_or_pid is not False:
        os.kill(false_or_pid, 2)
    if os.path.exists(pid_path):
        os.remove(pid_path)


def create_pid(pid_path):
    import atexit

    false_or_pid = is_process_running(pid_path)
    if false_or_pid is not False:
        print('server is already running: %s, Exiting....' % pid_path)
        sys.exit(1)

    pid = str(os.getpid())
    with open(pid_path, "w") as f:
        f.write(pid)

    def remove_pid():
        os.remove(pid_path)
    atexit.register(remove_pid)
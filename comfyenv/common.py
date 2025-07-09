import os
import sys
import platform
import shutil


def get_user_shell():
    system = platform.system()

    if system == 'Windows':
        # Try to get COMSPEC (usually cmd.exe), fallback to powershell
        # Usually C:\Windows\System32\cmd.exe
        shell = os.environ.get('COMSPEC')
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
    content = content.replace("MODELS_DIR", config["models_dir"])
    with open(dest_config, "w") as file:
        file.write(content)


def is_process_running(pid_path):
    import psutil
    pid_exists = os.path.exists(pid_path)
    pid = None
    if not pid_exists:
        return False
    with open(pid_path, 'r') as f:
        pid = int(f.read().strip())
    if not pid:
        return False
    return pid if psutil.pid_exists(pid) else False


def stop_process(pid_path, quiet=False):
    false_or_pid = is_process_running(pid_path)
    process_killed = False
    try:
        if false_or_pid is not False:
            os.kill(false_or_pid, 2)
            process_killed = True
    except Exception as e:
        print('Error: stopping process: %s' % str(e))

    remove_pid(pid_path)

    if not process_killed and not quiet:
        raise IOError('No process found to stop')


def create_pid(pid_path, port):
    import atexit

    port_occupied, running_pid = is_port_listening(port)
    false_or_pid = is_process_running(pid_path)
    if false_or_pid is not False:
        raise RuntimeError('Seems ComfyUI is already running: %s, Exiting....'
                           % pid_path)
    if port_occupied:
        raise RuntimeError(f'Port {port} already listening, '
                           'Please try some other port')

    pid = str(os.getpid())
    with open(pid_path, "w") as f:
        f.write(pid)

    def remove_pid_file():
        remove_pid(pid_path)
    atexit.register(remove_pid_file)


def remove_pid(pid_path):
    try:
        if os.path.exists(pid_path):
            os.remove(pid_path)
    except Exception as e:
        print('Error: removing pid file: %s' % str(e))


def is_port_listening(port):
    import psutil
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == int(port) and conn.status == psutil.CONN_LISTEN:
            return True, conn.pid
    return False, 0

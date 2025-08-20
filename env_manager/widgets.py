import platform
import shlex
import shutil
import json
import subprocess
import re
import webbrowser

from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QMessageBox, QToolButton,
    QSizePolicy, QInputDialog
)

from .dialogs import ConsoleWindow


class EnvItemWidget(QWidget):
    def __init__(self, env_name, parent_gui):
        super().__init__()
        self.env_name = env_name
        self.config = {}
        self.parent_gui = parent_gui

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel(self.env_name)
        self.label.setStyleSheet("font-size: 12pt;")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.open_btn = QToolButton()
        self.open_btn.setMinimumSize(34, 34)
        self.open_btn.setText("🌐")
        self.open_btn.setToolTip("Open in Browser")
        self.open_btn.clicked.connect(self.open_browser)

        self.run_btn = QToolButton()
        self.run_btn.setText("🚀")
        self.run_btn.setMinimumSize(34, 34)
        self.run_btn.setToolTip("Run ComfyUI")
        self.run_btn.clicked.connect(self.run)

        self.stop_btn = QToolButton()
        self.stop_btn.setText("⏹")
        self.stop_btn.setMinimumSize(34, 34)
        self.stop_btn.setToolTip("Stop ComfyUI")
        self.stop_btn.clicked.connect(self.stop)

        self.config_btn = QToolButton()
        self.config_btn.setText("⚙️")
        self.config_btn.setMinimumSize(34, 34)
        self.config_btn.setToolTip("Open Config File")
        self.config_btn.clicked.connect(self.open_config)

        self.shell_btn = QToolButton()
        self.shell_btn.setText("🖥")
        self.shell_btn.setMinimumSize(34, 34)
        self.shell_btn.setToolTip("Open Shell")
        self.shell_btn.clicked.connect(self.shell)

        self.console_btn = QToolButton()
        self.console_btn.setText("📜")
        self.console_btn.setMinimumSize(34, 34)
        self.console_btn.setToolTip("Open Console Output")
        self.console_btn.clicked.connect(self.open_console)

        self.update_btn = QToolButton()
        self.update_btn.setText("🔄")
        self.update_btn.setMinimumSize(34, 34)
        self.update_btn.setToolTip("Update Environment")
        self.update_btn.clicked.connect(self.update_env)

        self.delete_btn = QToolButton()
        self.delete_btn.setText("🗑️")
        self.delete_btn.setMinimumSize(34, 34)
        self.delete_btn.setToolTip("Delete Environment")
        self.delete_btn.clicked.connect(self.delete_env)

        layout.addWidget(self.label)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.config_btn)
        layout.addWidget(self.shell_btn)
        layout.addWidget(self.console_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        # Restore process state if running
        self.mark_running()

    @property
    def is_running(self):
        process = self.parent_gui.running_processes.get(self.env_name)
        if process and process.poll() is None:
            return True
        return False

    def mark_running(self):
        is_running = self.is_running
        label = f'{self.env_name}  🚀' if is_running else self.env_name
        self.label.setText(label)
        self.open_btn.setHidden(not is_running)
        self.console_btn.setHidden(not is_running)
        self.run_btn.setHidden(is_running)
        self.update_btn.setHidden(is_running)
        self.delete_btn.setHidden(is_running)
        self.config_btn.setHidden(is_running)

    def mark_processing(self, updating, icon=None):
        label = f'{self.env_name}  {icon}' if updating else self.env_name
        self.label.setText(label)
        self.open_btn.setHidden(updating)
        self.stop_btn.setHidden(updating)
        self.console_btn.setHidden(updating)
        self.run_btn.setHidden(updating)
        self.update_btn.setHidden(updating)
        self.delete_btn.setHidden(updating)
        self.config_btn.setHidden(updating)
        self.shell_btn.setHidden(updating)

    def run(self):
        if self.is_running:
            QMessageBox.information(self, "Already Running",
                                    "The environment is already running.")
            return

        config = subprocess.check_output(f'comfy-env config -n {self.env_name}',
                                         shell=True).decode()
        self.config = json.loads(config)
        comfyui_args = self.config['comfyui_args']

        # Prompt user for extra arguments
        user_args, ok = QInputDialog.getText(
            self, "ComfyUI Arguments",
            "Enter ComfyUI arguments (e.g., --port 8188):",
            text=' '.join(comfyui_args)
        )
        if not ok:
            return

        command = f'comfy-env run -n {self.env_name}'
        if user_args:
            command += f' -- {user_args}'

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding='utf-8'
        )

        self.parent_gui.running_processes[self.env_name] = process
        self.console = ConsoleWindow(self.env_name, process,
                                     parent=self, close_worker=False)
        self.console.show()

        # Disable relevant buttons
        self.mark_running()

        def on_process_finished(exit_code):
            self.mark_running()
            if self.env_name in self.parent_gui.running_processes:
                del self.parent_gui.running_processes[self.env_name]

        self.console.worker.finished.connect(on_process_finished)

    def stop(self, wait=False):
        if self.is_running:
            self.parent_gui.running_processes[self.env_name].terminate()

        command = f"comfy-env stop -n {self.env_name}"
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding='utf-8'
        )

        if wait:
            process.wait()
            self.console.worker.wait()

        console = ConsoleWindow(self.env_name, process, self)
        console.show()

        def on_process_finished(exit_code):
            if self.env_name in self.parent_gui.running_processes:
                del self.parent_gui.running_processes[self.env_name]
        console.worker.finished.connect(on_process_finished)

    def shell(self):
        system = platform.system()
        command = f"comfy-env activate -n {shlex.quote(self.env_name)}"

        if system == "Windows":
            # Launch in new cmd window
            subprocess.Popen(
                ["cmd.exe", "/k", command],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                encoding='utf-8'
            )

        elif system == "Linux":
            # Detect common terminals
            terminals = ["gnome-terminal", "konsole", "x-terminal-emulator",
                         "xfce4-terminal", "lxterminal", "xterm"]
            for term in terminals:
                if shutil.which(term):
                    subprocess.Popen(
                        [term, "--", "bash", "-c", f"{command}; exec bash"],
                        encoding='utf-8')
                    break
            else:
                QMessageBox.warning(self, "Terminal Not Found",
                                    "No supported terminal emulator found.")

        elif system == "Darwin":
            # macOS: use osascript to open Terminal.app and run the command
            apple_script = f'''
            tell application "Terminal"
                activate
                do script "{command}"
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script],
                             encoding='utf-8')
        else:
            QMessageBox.warning(self, "Unsupported Platform",
                                f"{system} is not supported.")

    def open_browser(self):
        config = subprocess.check_output(f'comfy-env config -n {self.env_name}',
                                         shell=True).decode()
        self.config = json.loads(config)
        args = self.config.get("comfyui_args", [])
        port_match = re.search(r"--port\s+(\d+)", ' '.join(args))
        port = port_match.group(1) if port_match else "8188"
        url = f"http://localhost:{port}"
        webbrowser.open(url)

    def open_config(self):
        subprocess.Popen(
            f"comfy-env config -n {self.env_name} --edit",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding='utf-8'
        )

    def open_console(self):
        process = self.parent_gui.running_processes.get(self.env_name)
        if not process:
            return
        self.console.show()

    def update_env(self):
        confirm = QMessageBox.question(
            self, "Update Environment",
            f"Do you want to update environment '{self.env_name}'?"
        )
        if confirm == QMessageBox.No:
            return

        self.mark_processing(True, icon="🔄")

        def on_process_finished(exit_code):
            self.mark_processing(False)

        self.parent_gui.run_in_console(
            f"comfy-env update -n {self.env_name}",
            title=f"Updating {self.env_name}",
            refresh_after=True,
            callback=on_process_finished,
            stop_button=True
        )

    def delete_env(self):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete environment '{self.env_name}'?"
        )
        if confirm == QMessageBox.No:
            return

        self.mark_processing(True, icon="🗑️")

        def on_process_finished(exit_code):
            self.mark_processing(False)

        self.parent_gui.run_in_console(
            f"comfy-env remove -n {self.env_name} -y",
            title=f"Delete: {self.env_name}",
            refresh_after=True,
            callback=on_process_finished
        )

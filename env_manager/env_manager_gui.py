import os
import json
import platform
import subprocess

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QDialog,
    QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox,
)

from .dialogs import ConsoleWindow, CreateEnvDialog
from .widgets import EnvItemWidget


class EnvManagerGUI(QWidget):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle(f'Comfy Environment Manager ({version})')
        self.setMinimumWidth(580)
        self.setMinimumHeight(320)

        self.running_processes = {}  # Store env_name -> Popen

        self.root_layout = QVBoxLayout()
        self.env_list = QListWidget()

        self.root_layout.addWidget(QLabel("Available Environments:"))
        self.root_layout.addWidget(self.env_list)

        self.create_button = QPushButton("➕ Create")
        self.create_button.setMinimumHeight(30)
        self.create_button.setToolTip("Create ComfyUI Environment")
        btn_row = QHBoxLayout()
        btn_row.addStretch()  # Pushes following widgets to the right
        btn_row.addWidget(self.create_button)
        self.root_layout.addLayout(btn_row)

        self.setLayout(self.root_layout)
        self.connect_signals()
        self.refresh_envs()

    def connect_signals(self):
        self.create_button.clicked.connect(self.create_env)

    def run_in_console(self, command, title="Command", refresh_after=False,
                       callback=None, stop_button=None):
        platform_ = platform.system()
        group_args = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if platform_ == "Windows" else
                      {"preexec_fn": os.setsid} if platform_ == "Linux" else
                      {})
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            **group_args
        )
        console = ConsoleWindow(title, process, parent=self,
                                stop_button=stop_button)
        if refresh_after:
            console.worker.finished.connect(self.refresh_envs)
        if callback:
            console.worker.finished.connect(callback)
        console.show()

    def refresh_envs(self):
        process = subprocess.Popen(
            "comfy-env list --json",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
        output, _ = process.communicate()

        self.env_list.clear()

        try:
            data = json.loads(output.strip())
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to parse environment list:\n{e}")
            return

        for env_name in data:
            item_widget = EnvItemWidget(env_name, self)
            item = QListWidgetItem(self.env_list)
            item.setSizeHint(item_widget.sizeHint())
            self.env_list.addItem(item)
            self.env_list.setItemWidget(item, item_widget)

    def create_env(self):
        dialog = CreateEnvDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return
        args = dialog.get_args()
        if not args:
            return

        command = f"comfy-env create {' '.join(args)}"
        self.run_in_console(command, title=f"Creating {args[1]}",
                            refresh_after=True,
                            stop_button=True)

    def closeEvent(self, event):
        if not len(self.running_processes):
            event.accept()
            return

        confirm = QMessageBox.question(
            self,
            "Quit",
            "Some processes are still running.\nDo you want to terminate all and exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.No:
            event.ignore()
            return

        # Terminate all running comfyui processes
        for i in range(self.env_list.count()):
            item = self.env_list.item(i)
            widget = self.env_list.itemWidget(item)
            if widget and widget.env_name in self.running_processes:
                widget.stop(wait=True)

        event.accept()

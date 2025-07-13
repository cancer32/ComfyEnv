import platform

from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QMessageBox, QToolButton,
    QTextEdit, QDialog, QFileDialog
)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from .workers import SubprocessWorker


class CreateEnvDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Environment")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        def labeled_input(label_text, browseable=False):
            layout.addWidget(QLabel(label_text))

            hbox = QHBoxLayout()
            line_edit = QLineEdit()
            hbox.addWidget(line_edit)

            if browseable:
                line_edit.setReadOnly(True)

                browse_btn = QToolButton()
                browse_btn.setText("📂")
                browse_btn.setToolTip("Browse")
                hbox.addWidget(browse_btn)

                clear_btn = QToolButton()
                clear_btn.setText("❌")
                clear_btn.setToolTip("Clear")
                hbox.addWidget(clear_btn)

                def open_dialog():
                    path = QFileDialog.getExistingDirectory(
                        self, "Select Folder")
                    if path:
                        line_edit.setText(path)

                def clear_field():
                    line_edit.clear()

                browse_btn.clicked.connect(open_dialog)
                clear_btn.clicked.connect(clear_field)

            layout.addLayout(hbox)
            return line_edit

        self.name_input = labeled_input("Environment Name (required):")
        self.name_input.setMaxLength(16)
        self.name_input.setValidator(QRegularExpressionValidator(
            QRegularExpression(r"^[a-zA-Z0-9_-]+$")))
        self.python_input = labeled_input("Python Version (default: 3.12.*):")
        self.python_input.setValidator(QRegularExpressionValidator(
            QRegularExpression(r"^[0-9.*]+$")))
        self.comfyui_version_input = labeled_input(
            "ComfyUI Version (optional):")
        self.comfyui_version_input.setValidator(QRegularExpressionValidator(
            QRegularExpression(r"^v[0-9.]+$")))

        self.user_root_input = labeled_input("User Root Path (optional):",
                                             browseable=True)
        self.envs_root_input = labeled_input("Envs Root Path (optional):",
                                             browseable=True)

        btn_row = QHBoxLayout()
        self.ok_btn = QPushButton("Create")
        self.cancel_btn = QPushButton("Cancel")
        btn_row.addWidget(self.ok_btn)
        btn_row.addWidget(self.cancel_btn)

        layout.addLayout(btn_row)
        self.setLayout(layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_args(self):
        args = []
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error",
                                "Environment name is required.")
            return None
        args += ["-n", name]

        if py := self.python_input.text().strip():
            args += ["--python", py]
        if ur := self.user_root_input.text().strip():
            args += ["--user-root", ur]
        if er := self.envs_root_input.text().strip():
            args += ["--envs-root", er]
        if ce := self.conda_env_input.text().strip():
            args += ["--conda-env-name", ce]
        if ver := self.comfyui_version_input.text().strip():
            args += ["--comfyui-version", ver]

        return args


class ConsoleWindow(QDialog):
    def __init__(self, env_name, process, parent=None, close_worker=True, stop_button=False):
        super().__init__(parent)
        self.setWindowTitle(f"Console - {env_name}")
        self.setMinimumSize(600, 400)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Add a Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setHidden(not stop_button)
        self.stop_button.clicked.connect(self.stop_process)
        # Layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.stop_button)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.close_worker = close_worker
        self.worker = SubprocessWorker(process)
        self.worker.output_ready.connect(self.append_output)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def append_output(self, text):
        self.output.append(text)

    def on_finished(self, exit_code):
        self.output.append(f"\nProcess exited with code {exit_code}.")
        self.stop_button.setEnabled(False)  # Disable stop button when done

    def stop_process(self):
        if not (self.worker and self.worker.process):
            return

        self.output.append("\nTerminating process...")

        platform_ = platform.system()
        if platform_ == 'Windows':
            import subprocess
            import time
            self.worker.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
            time.sleep(.5)
            self.worker.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
            time.sleep(.5)
            self.worker.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
            time.sleep(.5)
        elif platform_ == 'Linux':
            import os
            import signal
            os.killpg(os.getpgid(self.worker.process.pid), signal.SIGTERM)
        self.worker.process.terminate()

    def closeEvent(self, event):
        if self.close_worker:
            self.worker.quit()
        event.accept()

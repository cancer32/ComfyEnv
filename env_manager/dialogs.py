from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox, QToolButton, QSizePolicy,
    QTextEdit, QDialog
)

from .workers import SubprocessWorker


class CreateEnvDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Environment")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        def labeled_input(label_text):
            layout.addWidget(QLabel(label_text))
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            return line_edit

        self.name_input = labeled_input("Environment Name (required):")
        self.python_input = labeled_input("Python Version (default: 3.12.*):")
        self.comfyui_version_input = labeled_input(
            "ComfyUI Version (optional):")
        self.user_root_input = labeled_input("User Root Path (optional):")
        self.envs_root_input = labeled_input("Envs Root Path (optional):")
        self.conda_env_input = labeled_input("Conda Env Name (optional):")

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
    def __init__(self, env_name, process, parent=None, close_worker=True):
        super().__init__(parent)
        self.setWindowTitle(f"Console - {env_name}")
        self.setMinimumSize(600, 400)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
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

    def closeEvent(self, event):
        if self.close_worker:
            self.worker.quit()
        event.accept()

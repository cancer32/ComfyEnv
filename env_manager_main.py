import sys

from PySide6.QtWidgets import QApplication

from env_manager.env_manager_gui import EnvManagerGUI
from comfy_env.version import __version__


def main(args):
    app = QApplication(args)
    window = EnvManagerGUI(version=__version__)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)

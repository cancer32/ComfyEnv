from PySide6.QtCore import Qt, QThread, Signal


class SubprocessWorker(QThread):
    output_ready = Signal(str)
    finished = Signal(int)

    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self):
        for line in self.process.stdout:
            self.output_ready.emit(line.strip())
        self.process.wait()
        self.finished.emit(self.process.returncode)

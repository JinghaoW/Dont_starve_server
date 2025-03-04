# log_handler.py - 日志处理模块
from PySide6.QtCore import QThread, Signal
import time


class LogMonitorThread(QThread):
    log_received = Signal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True

    def run(self):
        """实时读取进程输出"""
        while self.running:
            output = self.process.stdout.readline()
            if output:
                self.log_received.emit(output.strip())
            time.sleep(0.1)

    def stop(self):
        """停止监控"""
        self.running = False
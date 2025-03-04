# main.py - 主界面程序
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QFileDialog,
                               QTextEdit, QProgressBar, QLabel, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from steamcmd_manager import SteamCMDManager
from server_manager import ServerManager


class DSTServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.steamcmd_manager = SteamCMDManager()
        self.server_manager = ServerManager()
        self.process = None  # 服务器进程对象
        self.init_ui()
        self.setWindowTitle("饥荒服务器管理器")
        self.setMinimumSize(800, 600)

    def init_ui(self):
        """初始化用户界面"""
        main_widget = QWidget()
        layout = QVBoxLayout()

        # SteamCMD安装模块
        self.steamcmd_group = self.create_path_group(
            "SteamCMD路径：",
            self.select_steamcmd_path,
            "状态：未安装"
        )
        layout.addWidget(self.steamcmd_group)

        # 服务器安装模块
        self.server_group = self.create_path_group(
            "服务器路径：",
            self.select_server_path,
            "状态：未安装"
        )
        layout.addWidget(self.server_group)

        # 存档选择模块
        self.cluster_group = self.create_path_group(
            "存档路径：",
            self.select_cluster_path,
            "状态：未选择"
        )
        layout.addWidget(self.cluster_group)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.install_btn = QPushButton("安装/验证")
        self.install_btn.clicked.connect(self.start_installation)
        self.start_btn = QPushButton("启动服务器")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setEnabled(False)
        self.stop_btn = QPushButton("停止服务器")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)

        btn_layout.addWidget(self.install_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # 日志显示
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(QLabel("运行日志："))
        layout.addWidget(self.log_display)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def create_path_group(self, label, callback, status_text):
        """创建路径选择组件"""
        group = QWidget()
        layout = QVBoxLayout(group)

        # 路径输入行
        path_layout = QHBoxLayout()
        lbl = QLabel(label)
        self.path_input = QLineEdit()
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(callback)

        path_layout.addWidget(lbl)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)

        # 状态显示
        status_lbl = QLabel(status_text)
        status_lbl.setObjectName("status_label")

        layout.addLayout(path_layout)
        layout.addWidget(status_lbl)
        return group

    def select_steamcmd_path(self):
        """选择SteamCMD安装路径"""
        path = QFileDialog.getExistingDirectory(self, "选择SteamCMD安装目录")
        if path:
            # 找到SteamCMD路径输入框
            inputs = self.steamcmd_group.findChildren(QLineEdit)
            if inputs:
                inputs[0].setText(os.path.normpath(path))
                self.check_steamcmd_status()

    def select_server_path(self):
        """选择服务器安装路径"""
        path = QFileDialog.getExistingDirectory(self, "选择服务器目录")
        if path:
            # 找到服务器路径输入框
            inputs = self.server_group.findChildren(QLineEdit)
            if inputs:
                inputs[0].setText(os.path.normpath(path))
                self.check_server_status()

    def select_cluster_path(self):
        """选择存档文件夹路径"""
        path = QFileDialog.getExistingDirectory(self, "选择存档文件夹")
        if path:
            # 找到存档路径输入框
            inputs = self.cluster_group.findChildren(QLineEdit)
            if inputs:
                inputs[0].setText(os.path.normpath(path))
                self.check_cluster_status()

    def check_steamcmd_status(self):
        """更新SteamCMD安装状态"""
        path = self.steamcmd_group.findChildren(QLineEdit)[0].text()
        status_label = self.steamcmd_group.findChildren(QLabel)[1]  # 第二个QLabel是状态标签

        if self.steamcmd_manager.is_installed(path):
            status_label.setText("状态：已安装 ✔️")
            return True
        status_label.setText("状态：未安装 ❌")
        return False

    def check_server_status(self):
        """更新服务器安装状态"""
        path = self.server_group.findChildren(QLineEdit)[0].text()
        status_label = self.server_group.findChildren(QLabel)[1]

        required_files = [
            os.path.join(path, "bin", "dontstarve_dedicated_server_nullrenderer.exe"),
            os.path.join(path, "cluster")
        ]

        status = all(os.path.exists(p) for p in required_files)
        status_label.setText("状态：已安装 ✔️" if status else "状态：未安装 ❌")
        return status

    def check_cluster_status(self):
        """更新存档文件状态"""
        path = self.cluster_group.findChildren(QLineEdit)[0].text()
        status_label = self.cluster_group.findChildren(QLabel)[1]

        required_files = ["cluster.ini", "cluster_token.txt"]
        valid = all(os.path.exists(os.path.join(path, f)) for f in required_files)
        status_label.setText("状态：有效 ✔️" if valid else "状态：无效 ❌")
        return valid

    def start_installation(self):
        """开始安装流程"""
        try:
            steamcmd_path = self.steamcmd_group.findChild(QLineEdit).text()
            server_path = self.server_group.findChild(QLineEdit).text()

            # 安装SteamCMD
            if not self.steamcmd_manager.install(steamcmd_path, self.update_progress):
                return

            # 部署服务器
            self.server_manager.deploy_server(
                steamcmd_path,
                server_path,
                self.update_progress
            )

            # 启用启动按钮
            self.start_btn.setEnabled(True)

        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        """显示错误对话框"""
        QMessageBox.critical(
            self,
            "错误",
            message,
            QMessageBox.Ok
        )

    def start_server(self):
        """启动服务器"""
        server_path = self.server_group.findChild(QLineEdit).text()
        cluster_path = self.cluster_group.findChild(QLineEdit).text()

        try:
            self.process = self.server_manager.start_server(server_path, cluster_path)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.log_display.append("服务器已启动！")
        except Exception as e:
            self.show_error(str(e))

    def stop_server(self):
        """停止服务器"""
        if self.server_manager.stop_server(self.process):
            self.log_display.append("服务器已停止")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def update_progress(self, value):
        """更新进度条"""
        self.progress.setValue(value)
        if value == 100:
            self.progress.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DSTServerGUI()
    window.show()
    sys.exit(app.exec())
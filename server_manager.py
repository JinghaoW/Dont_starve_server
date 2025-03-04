# server_manager.py
import os
import shutil
import subprocess


class ServerManager:
    def __init__(self):
        self.process = None

    def validate_cluster(self, cluster_path):
        """验证存档文件完整性（带异常处理）"""
        required_files = ["cluster.ini", "cluster_token.txt"]

        try:
            # 检查路径有效性
            if not os.path.isdir(cluster_path):
                return False

            # 检查每个文件是否存在
            return all(
                os.path.isfile(os.path.join(cluster_path, f))
                for f in required_files
            )
        except Exception as e:
            print(f"存档验证错误: {str(e)}")
            return False

    def start_server(self, install_path, cluster_path):
        """启动服务器"""
        """启动服务器（带完整异常处理）"""
        try:
            server_path = self.server_group.findChildren(QLineEdit)[0].text()
            cluster_path = self.cluster_group.findChildren(QLineEdit)[0].text()

            if not server_path or not cluster_path:
                raise ValueError("请先设置服务器路径和存档路径")

            self.process = self.server_manager.start_server(server_path, cluster_path)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.log_display.append("服务器启动成功！")

        except Exception as e:
            self.show_error(f"启动服务器失败: {str(e)}")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
        if not self.validate_cluster(cluster_path):
            raise ValueError("存档文件验证失败，请检查cluster.ini和cluster_token.txt")

        # 复制存档（使用固定目录名）
        dst_cluster = os.path.join(install_path, "cluster")
        if os.path.exists(dst_cluster):
            shutil.rmtree(dst_cluster)
        shutil.copytree(cluster_path, dst_cluster)

        # 构建启动命令
        bat_path = os.path.join(install_path, "bin", "scripts", "launch_preconfigured_servers.bat")
        if not os.path.exists(bat_path):
            raise FileNotFoundError(f"找不到启动脚本: {bat_path}")

        return subprocess.Popen(
            ['cmd.exe', '/c', f'"{bat_path}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )

    def stop_server(self, process):
        """停止服务器"""
        if process and process.poll() is None:
            process.terminate()
            return True
        return False
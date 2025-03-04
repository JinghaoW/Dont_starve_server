# steamcmd_manager.py - SteamCMD管理模块
import os
import urllib.request
import zipfile
from threading import Thread


class SteamCMDManager:
    def __init__(self):
        self.steamcmd_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"

    def is_installed(self, path):
        """检查SteamCMD是否已安装"""
        return os.path.exists(os.path.join(path, "steamcmd.exe"))

    def install(self, path, progress_callback):
        """安装SteamCMD"""
        if self.is_installed(path):
            progress_callback(100)
            return True

        def _install():
            try:
                os.makedirs(path, exist_ok=True)
                zip_path = os.path.join(path, "steamcmd.zip")

                # 下载文件
                urllib.request.urlretrieve(
                    self.steamcmd_url,
                    zip_path,
                    lambda c, b, t: progress_callback(int(c * b / t * 100))
                )

                # 解压文件
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(path)

                os.remove(zip_path)
                progress_callback(100)
                return True
            except Exception as e:
                print(f"安装失败: {str(e)}")
                return False

        Thread(target=_install).start()
        return True
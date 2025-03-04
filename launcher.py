import os
from pathlib import Path
from tkinter import messagebox


def launch_server(server_path):
    """启动服务器"""
    try:
        bat_path = Path(server_path) / "bin" / "scripts" / "launch_preconfigured_servers.bat"

        if not bat_path.exists():
            raise FileNotFoundError("找不到启动脚本")

        os.startfile(str(bat_path))
        return True
    except Exception as e:
        messagebox.showerror("启动失败", f"错误详情：{str(e)}")
        return False
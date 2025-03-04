from pathlib import Path
import os

def check_steamcmd(path):
    """检查 SteamCMD 是否安装"""
    steamcmd_path = Path(path)
    return any(steamcmd_path.joinpath(f).exists() for f in ["steamcmd.exe", "steamcmd.sh"])


def check_server(path):
    """检查服务器文件是否完整"""
    server_dir = Path(path)
    required_files = {
        "bin/dontstarve_dedicated_server_nullrenderer.exe": False,
        "bin/scripts/launch_preconfigured_servers.bat": False
    }

    for root, dirs, files in os.walk(server_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), server_dir)
            if rel_path in required_files:
                required_files[rel_path] = True

    missing = [k for k, v in required_files.items() if not v]
    return len(missing) == 0, missing


def check_cluster(path):
    """检查存档配置是否存在"""
    return Path(path).joinpath("Cluster_1").exists()

def check_mods_directory(server_path):
    """检查服务器 mods 目录是否存在"""
    mods_dir = Path(server_path) / "mods"
    return mods_dir.exists()
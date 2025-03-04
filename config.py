import json
import os
from pathlib import Path

CONFIG_FILE = "dst_tool_config.json"

DEFAULT_PATHS = {
    "steamcmd_path": str(Path.home() / "SteamCMD"),
    "server_path": str(Path.home() / "DST_Server"),
    "cluster_path": str(Path.home() / "Documents" / "Klei" / "DoNotStarveTogether"),
    "mods_path": ""  # 默认模组路径为空
}

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_PATHS

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
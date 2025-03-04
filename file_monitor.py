## file_monitor.py - 文件监控模块
import os
import hashlib


class FileMonitor:
    @staticmethod
    def is_bat_modified(bat_path):
        """检查bat文件是否已正确修改"""
        expected_lines = [
            'start "Don\'t Starve Together Overworld"',
            '-cluster Cluster_1 -console -shard Master',
            'start "Don\'t Starve Together Caves"',
            '-cluster Cluster_1 -console -shard Caves'
        ]

        if not os.path.exists(bat_path):
            return False

        with open(bat_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return all(line in content for line in expected_lines)

    @staticmethod
    def get_file_hash(file_path):
        """获取文件哈希值用于验证"""
        if not os.path.exists(file_path):
            return None
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
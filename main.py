import platform
from gui import DSTInstallerApp

if __name__ == "__main__":
    if platform.system() != 'Windows':
        print("错误: 本工具仅支持Windows系统")
        exit(1)

    app = DSTInstallerApp()
    app.mainloop()
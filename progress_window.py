import tkinter as tk
from tkinter import ttk


class DownloadProgressWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("服务器更新进度")
        self.geometry("400x150")
        self.resizable(False, False)

        self.progress_bar = ttk.Progressbar(self, mode='determinate', length=300)
        self.progress_bar.pack(pady=20)

        self.status_label = tk.Label(self, text="准备更新...")
        self.status_label.pack()

        self.cancel_button = tk.Button(
            self,
            text="取消更新",
            command=self.on_cancel,
            state=tk.NORMAL
        )
        self.cancel_button.pack(pady=10)

        self.cancelled = False

    def on_cancel(self):
        self.cancelled = True
        self.cancel_button.config(state=tk.DISABLED)
        self.status_label.config(text="正在取消...")

    def update_progress(self, percentage, status):
        self.progress_bar['value'] = percentage
        self.status_label.config(text=status)
        self.update_idletasks()
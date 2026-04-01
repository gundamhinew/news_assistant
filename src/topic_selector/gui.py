from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from .pipeline import TopicPipeline


class TopicSelectorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("国际政经新闻选题程序")
        self.root.geometry("1100x760")
        self.pipeline = TopicPipeline()

        top = ttk.Frame(root)
        top.pack(fill=tk.X, padx=10, pady=10)

        self.start_btn = ttk.Button(top, text="开始", command=self.start)
        self.start_btn.pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="待运行")
        ttk.Label(top, textvariable=self.status_var).pack(side=tk.LEFT, padx=12)

        paned = ttk.Panedwindow(root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_100 = ttk.Labelframe(paned, text="100条大列表")
        frame_25 = ttk.Labelframe(paned, text="25条小列表")
        paned.add(frame_100, weight=1)
        paned.add(frame_25, weight=1)

        self.txt100 = tk.Text(frame_100, wrap=tk.WORD)
        self.txt100.pack(fill=tk.BOTH, expand=True)

        self.txt25 = tk.Text(frame_25, wrap=tk.WORD)
        self.txt25.pack(fill=tk.BOTH, expand=True)

    def start(self) -> None:
        self.start_btn.config(state=tk.DISABLED)
        self.status_var.set("运行中：正在抓取与筛选...")
        t = threading.Thread(target=self._run_pipeline, daemon=True)
        t.start()

    def _run_pipeline(self) -> None:
        try:
            big, small, small_text = self.pipeline.run(target_big=100, target_small=25)
        except Exception as e:
            self.root.after(0, lambda: self._on_error(e))
            return
        self.root.after(0, lambda: self._on_success(big, small, small_text))

    def _on_error(self, e: Exception) -> None:
        self.status_var.set("运行失败")
        self.start_btn.config(state=tk.NORMAL)
        messagebox.showerror("错误", str(e))

    def _on_success(self, big, small, small_text: str) -> None:
        self.txt100.delete("1.0", tk.END)
        self.txt25.delete("1.0", tk.END)
        from .formatter import render_list

        self.txt100.insert(tk.END, render_list(big))
        self.txt25.insert(tk.END, small_text)
        self.status_var.set(f"完成：100条={len(big)}，25条={len(small)}")
        self.start_btn.config(state=tk.NORMAL)


def run_gui() -> None:
    root = tk.Tk()
    TopicSelectorGUI(root)
    root.mainloop()

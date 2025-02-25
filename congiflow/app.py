import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkbs
from PIL import Image, ImageTk
import pystray
from .backend import ClipboardMonitor, ProcessingPipeline
from .processors.formula import FormulaProcessor

class CongiFlowApp:
    def __init__(self):
        # 初始化后端服务
        self.monitor = ClipboardMonitor()
        self.pipeline = ProcessingPipeline()
        self.pipeline.register_processor(FormulaProcessor({}))
        
        # 创建主界面
        self.root = ttkbs.Window(themename="minty")
        self._setup_ui()
        self._setup_tray()
        
        # 启动后台服务
        self.monitor.start()
        self.root.after(100, self._check_events)

    def _setup_ui(self):
        self.root.title("CongiFlow")
        self.root.geometry("800x600")
        
        # 主布局
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左右面板
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧原始内容
        self.left_panel = ttkbs.Frame(paned)
        self.raw_text = tk.Text(self.left_panel, wrap=tk.WORD)
        self.raw_text.pack(fill=tk.BOTH, expand=True)
        paned.add(self.left_panel, weight=1)
        
        # 右侧处理结果
        self.right_panel = ttkbs.Frame(paned)
        self.processed_text = tk.Text(self.right_panel, wrap=tk.WORD)
        self.processed_text.pack(fill=tk.BOTH, expand=True)
        paned.add(self.right_panel, weight=1)
        
        # 底部日志
        log_frame = ttkbs.Frame(main_frame)
        self.log = ttkbs.Treeview(log_frame, columns=('time', 'message'), show='headings')
        self.log.heading('time', text='Time')
        self.log.heading('message', text='Message')
        self.log.pack(fill=tk.BOTH, expand=True)
        log_frame.pack(fill=tk.BOTH, expand=False, pady=10)

    def _check_events(self):
        while not self.monitor.event_queue.empty():
            event_type, data = self.monitor.event_queue.get()
            if event_type == 'clipboard_update':
                self._update_content(data)
        self.root.after(100, self._check_events)
        
    def _update_content(self, text):
        processed = self.pipeline.process(text)
        self.raw_text.delete(1.0, tk.END)
        self.raw_text.insert(tk.END, text)
        self.processed_text.delete(1.0, tk.END)
        self.processed_text.insert(tk.END, processed)
        
    def _setup_tray(self):
        image = Image.open("congi/resources/icon.png")
        menu = pystray.Menu(
            pystray.MenuItem("Show", self._restore_window),
            pystray.MenuItem("Exit", self._quit)
        )
        self.tray = pystray.Icon("CongiFlow", image, "CongiFlow", menu)
        
    def _restore_window(self):
        self.root.deiconify()
        
    def _quit(self):
        self.monitor.stop()
        self.root.destroy()

def main():
    app = CongiFlowApp()
    app.root.mainloop()

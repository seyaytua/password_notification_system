"""
ログビューアー
"""
import customtkinter as ctk
from tkinter import scrolledtext
import queue
import logging


class LogViewer(ctk.CTkFrame):
    """ログビューアーフレーム"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # ラベル
        label = ctk.CTkLabel(
            self,
            text="ログビューアー",
            font=("Arial", 14, "bold")
        )
        label.pack(pady=(10, 5), padx=10, anchor="w")
        
        # テキストエリア
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap="word",
            width=80,
            height=15,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4"
        )
        self.text_area.pack(pady=5, padx=10, fill="both", expand=True)
        
        # ログキュー
        self.log_queue = queue.Queue()
        
        # ログハンドラを設定
        self._setup_log_handler()
        
        # 定期的にログを更新
        self.after(100, self._update_log)
    
    def _setup_log_handler(self):
        """ログハンドラを設定"""
        class QueueHandler(logging.Handler):
            def __init__(self, log_queue):
                super().__init__()
                self.log_queue = log_queue
            
            def emit(self, record):
                self.log_queue.put(self.format(record))
        
        # ルートロガーにハンドラを追加
        queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', 
                                     datefmt='%Y-%m-%d %H:%M:%S')
        queue_handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(queue_handler)
    
    def _update_log(self):
        """ログを更新"""
        while not self.log_queue.empty():
            try:
                log_message = self.log_queue.get_nowait()
                self.text_area.insert("end", log_message + "\n")
                self.text_area.see("end")  # 自動スクロール
            except queue.Empty:
                break
        
        # 100ms後に再度実行
        self.after(100, self._update_log)
    
    def clear(self):
        """ログをクリア"""
        self.text_area.delete("1.0", "end")

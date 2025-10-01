"""
ログ管理モジュール
"""
import logging
from pathlib import Path
from datetime import datetime


class Logger:
    """ログ管理クラス"""
    
    def __init__(self, name="PasswordNotificationSystem"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # ログディレクトリの作成
        log_dir = Path.home() / "password_system_logs"
        log_dir.mkdir(exist_ok=True)
        
        # ログファイル名（日付ごと）
        log_file = log_dir / f"log_{datetime.now().strftime('%Y%m%d')}.log"
        
        # ファイルハンドラ
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # コンソールハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # フォーマット
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # ハンドラが既に追加されていない場合のみ追加
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """情報ログ"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告ログ"""
        self.logger.warning(message)
    
    def error(self, message):
        """エラーログ"""
        self.logger.error(message)
    
    def critical(self, message):
        """致命的エラーログ"""
        self.logger.critical(message)


# グローバルロガーインスタンス
_global_logger = None


def get_logger():
    """グローバルロガーを取得"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger()
    return _global_logger

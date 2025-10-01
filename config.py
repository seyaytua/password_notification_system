"""
設定ファイル
"""
from pathlib import Path

# アプリケーション情報
APP_NAME = "パスワードお知らせシステム"
APP_VERSION = "1.0.0"

# ログ設定
LOG_DIR = Path.home() / "password_system_logs"
LOG_MAX_DAYS = 30

# デフォルト出力先
DEFAULT_OUTPUT_DIR = Path.home() / "Downloads"

# CSV設定
CSV_ENCODING_PRIMARY = "utf-8"
CSV_ENCODING_SECONDARY = "shift-jis"

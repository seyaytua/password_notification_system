"""
パスワードお知らせシステム - メインエントリーポイント
"""
import sys
from ui.dashboard import Dashboard
from utils.logger import get_logger


def main():
    """メイン関数"""
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("パスワードお知らせシステムを起動")
    logger.info("=" * 60)
    
    try:
        app = Dashboard()
        app.mainloop()
    except Exception as e:
        logger.critical(f"アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

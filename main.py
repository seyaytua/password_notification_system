"""
パスワードお知らせシステム - メインエントリーポイント
"""
import sys

def check_dependencies():
    """依存関係チェック"""
    try:
        import numpy
        import pandas
        print(f"✅ NumPy: {numpy.__version__}")
        print(f"✅ Pandas: {pandas.__version__}")
        return True
    except ImportError as e:
        print(f"❌ 依存関係エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def main():
    """メイン関数"""
    # バージョン表示オプション
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("パスワードお知らせシステム v1.0.1")
        return
    
    # 依存関係チェック
    if not check_dependencies():
        input("依存関係エラーが発生しました。Enterキーで終了...")
        sys.exit(1)
    
    try:
        from ui.dashboard import Dashboard
        from utils.logger import get_logger
        
        logger = get_logger()
        logger.info("=" * 60)
        logger.info("パスワードお知らせシステムを起動")
        logger.info("=" * 60)
        
        app = Dashboard()
        app.mainloop()
        
    except Exception as e:
        print(f"❌ アプリケーションエラー: {e}")
        import traceback
        traceback.print_exc()
        input("Enterキーで終了...")
        sys.exit(1)

if __name__ == "__main__":
    main()

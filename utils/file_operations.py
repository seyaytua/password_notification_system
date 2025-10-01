"""
ファイル操作ユーティリティ
"""
import os
import sys
import subprocess
from pathlib import Path


def open_folder(folder_path):
    """
    フォルダをエクスプローラー/Finderで開く
    
    Args:
        folder_path (Path or str): 開くフォルダのパス
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        raise FileNotFoundError(f"フォルダが存在しません: {folder_path}")
    
    if sys.platform == "win32":
        os.startfile(folder_path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", folder_path])
    else:
        subprocess.Popen(["xdg-open", folder_path])


def get_file_extension(filename):
    """
    ファイルの拡張子を取得
    
    Args:
        filename (str): ファイル名
    
    Returns:
        str: 拡張子（ドット付き）
    """
    return Path(filename).suffix


def get_account_name(email):
    """
    メールアドレスから@前部分を取得
    
    Args:
        email (str): メールアドレス
    
    Returns:
        str: @前部分（8桁）
    """
    if '@' in email:
        return email.split('@')[0]
    return email

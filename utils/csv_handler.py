"""
CSV操作ユーティリティ
"""
import pandas as pd
from pathlib import Path
from utils.logger import get_logger


logger = get_logger()


def read_csv(csv_path, encoding='utf-8'):
    """
    CSVファイルを読み込む
    
    Args:
        csv_path (str): CSVファイルのパス
        encoding (str): エンコーディング
    
    Returns:
        pd.DataFrame: 読み込んだデータフレーム
    """
    try:
        df = pd.read_csv(csv_path, encoding=encoding, dtype=str)
        logger.info(f"CSVファイルを読み込みました: {csv_path}")
        return df.fillna('')
    except UnicodeDecodeError:
        # UTF-8で失敗したらShift-JISで試す
        try:
            df = pd.read_csv(csv_path, encoding='shift-jis', dtype=str)
            logger.info(f"CSVファイルを読み込みました（Shift-JIS）: {csv_path}")
            return df.fillna('')
        except Exception as e:
            logger.error(f"CSVファイルの読み込みに失敗しました: {e}")
            raise
    except Exception as e:
        logger.error(f"CSVファイルの読み込みに失敗しました: {e}")
        raise


def write_csv(df, csv_path, encoding='utf-8'):
    """
    データフレームをCSVファイルに書き込む
    
    Args:
        df (pd.DataFrame): データフレーム
        csv_path (str): 出力先CSVファイルのパス
        encoding (str): エンコーディング
    """
    try:
        df.to_csv(csv_path, index=False, encoding=encoding)
        logger.info(f"CSVファイルを保存しました: {csv_path}")
    except Exception as e:
        logger.error(f"CSVファイルの保存に失敗しました: {e}")
        raise

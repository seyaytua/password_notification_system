"""
Unicode正規化モジュール
濁点・半濁点の分離問題に対応
"""
import unicodedata


def normalize_string(text):
    """
    文字列をUnicode正規化する（NFC形式）
    
    Args:
        text (str): 正規化対象の文字列
    
    Returns:
        str: 正規化後の文字列
    """
    if not text:
        return text
    
    # NFC正規化（濁点・半濁点を結合）
    normalized = unicodedata.normalize('NFC', text)
    
    return normalized


def clean_filename(filename):
    """
    ファイル名として使用できない文字を置換する
    
    Args:
        filename (str): 元のファイル名
    
    Returns:
        str: クリーンアップされたファイル名
    """
    # 正規化
    filename = normalize_string(filename)
    
    # 無効な文字を置換
    invalid_chars = r'\/*?:"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # 先頭・末尾のスペースとドットを除去
    filename = filename.strip().strip('.')
    
    # 空文字列の場合はデフォルト名
    if not filename:
        filename = "unnamed"
    
    return filename


def clean_foldername(foldername):
    """
    フォルダ名として使用できない文字を置換する
    
    Args:
        foldername (str): 元のフォルダ名
    
    Returns:
        str: クリーンアップされたフォルダ名
    """
    return clean_filename(foldername)

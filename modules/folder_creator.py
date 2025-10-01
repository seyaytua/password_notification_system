"""
Module2: フォルダ作成
CSVから生徒ごとのフォルダを作成
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.logger import get_logger
from utils.csv_handler import read_csv
from utils.unicode_normalizer import clean_foldername
from utils.file_operations import open_folder


logger = get_logger()


class FolderCreator:
    """フォルダ作成クラス"""
    
    def __init__(self):
        self.created_folders = 0
        self.output_folder = None
    
    def run(self):
        """
        メイン処理を実行
        
        Returns:
            bool: 成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Step 2: フォルダ作成を開始")
        logger.info("=" * 60)
        
        # CSVファイルを選択
        csv_path = self._select_csv_file()
        if not csv_path:
            logger.info("CSVファイルの選択がキャンセルされました")
            return False
        
        try:
            # CSVを読み込み
            df = read_csv(csv_path)
            
            # E列（メールアドレス）の確認
            if len(df.columns) < 5:
                messagebox.showerror(
                    "エラー",
                    "CSVファイルにE列（メールアドレス）が存在しません。\n"
                    "正しいフォーマットのCSVを使用してください。"
                )
                logger.error("CSVファイルの列数が不足しています")
                return False
            
            # E列（インデックス4）のメールアドレスを取得
            email_column = df.iloc[:, 4]
            folder_names = email_column.dropna().astype(str).tolist()
            
            # 空のメールアドレスを除外
            folder_names = [name.strip() for name in folder_names if name.strip()]
            
            if not folder_names:
                messagebox.showerror("エラー", "CSVにメールアドレスのデータがありません。")
                logger.error("メールアドレスのデータが存在しません")
                return False
            
            logger.info(f"対象フォルダ数: {len(folder_names)}")
            
            # 出力先フォルダを作成
            downloads_folder = Path.home() / "Downloads"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_folder = downloads_folder / f"CSVFolders_{timestamp}"
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"出力先: {self.output_folder}")
            
            # フォルダを作成
            self.created_folders = 0
            existing_folders = 0
            
            for i, email in enumerate(folder_names, 1):
                # フォルダ名をクリーンアップ
                clean_email = clean_foldername(email)
                
                if clean_email:
                    folder_path = self.output_folder / clean_email
                    
                    if not folder_path.exists():
                        folder_path.mkdir(parents=True, exist_ok=True)
                        self.created_folders += 1
                        logger.info(f"作成 ({i}/{len(folder_names)}): {clean_email}")
                    else:
                        existing_folders += 1
                        logger.info(f"既存 ({i}/{len(folder_names)}): {clean_email}")
                
                # 進捗表示（100件ごと）
                if i % 100 == 0:
                    logger.info(f"進捗: {i}/{len(folder_names)} ({i/len(folder_names)*100:.0f}%)")
            
            logger.info("=" * 60)
            logger.info(f"フォルダ作成完了")
            logger.info(f"新規作成: {self.created_folders}件")
            logger.info(f"既存: {existing_folders}件")
            logger.info("=" * 60)
            
            # 結果表示
            result_msg = (
                f"フォルダ作成完了!\n\n"
                f"新規作成: {self.created_folders}件\n"
                f"既存: {existing_folders}件\n"
                f"出力先: {self.output_folder}\n\n"
                f"次にStep1またはStep3を実行してください。"
            )
            messagebox.showinfo("完了", result_msg)
            
            # 出力フォルダを開く
            try:
                open_folder(self.output_folder)
            except Exception as e:
                logger.warning(f"フォルダを開けませんでした: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"フォルダ作成中にエラーが発生しました: {e}")
            messagebox.showerror("エラー", f"フォルダ作成中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _select_csv_file(self):
        """
        CSVファイル選択ダイアログを表示
        
        Returns:
            str: 選択されたCSVファイルのパス（キャンセル時はNone）
        """
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="【Step2】生徒マスタCSVファイルを選択してください",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        return file_path if file_path else None


# スタンドアロン実行用
if __name__ == "__main__":
    creator = FolderCreator()
    creator.run()

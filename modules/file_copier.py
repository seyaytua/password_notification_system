"""
Module5: ファイル一括コピー
指定したファイルをすべてのサブフォルダにコピー
"""
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.logger import get_logger
from utils.file_operations import open_folder


logger = get_logger()


class FileCopier:
    """ファイル一括コピークラス"""
    
    def __init__(self):
        self.copied_count = 0
        self.error_count = 0
        self.results = []
    
    def run(self):
        """
        メイン処理を実行
        
        Returns:
            bool: 成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Step 5: ファイル一括コピーを開始")
        logger.info("=" * 60)
        
        # ファイルを選択
        source_file = self._select_source_file()
        if not source_file:
            logger.info("ファイルの選択がキャンセルされました")
            return False
        
        # 対象フォルダを選択
        target_folder = self._select_target_folder()
        if not target_folder:
            logger.info("フォルダの選択がキャンセルされました")
            return False
        
        source_path = Path(source_file)
        target_path = Path(target_folder)
        
        # ファイルの存在確認
        if not source_path.exists():
            messagebox.showerror("エラー", f"ファイルが存在しません:\n{source_file}")
            logger.error(f"ファイルが存在しません: {source_file}")
            return False
        
        if not source_path.is_file():
            messagebox.showerror("エラー", f"選択されたパスはファイルではありません:\n{source_file}")
            logger.error(f"選択されたパスはファイルではありません: {source_file}")
            return False
        
        if not target_path.exists():
            messagebox.showerror("エラー", f"フォルダが存在しません:\n{target_folder}")
            logger.error(f"フォルダが存在しません: {target_folder}")
            return False
        
        try:
            logger.info(f"コピー元ファイル: {source_path}")
            logger.info(f"コピー先フォルダ: {target_path}")
            
            # サブフォルダ数をカウント
            subfolders = [d for d in target_path.iterdir() if d.is_dir()]
            logger.info(f"対象サブフォルダ数: {len(subfolders)}")
            
            if len(subfolders) == 0:
                messagebox.showinfo("情報", "サブフォルダが見つかりませんでした。")
                logger.info("サブフォルダが見つかりませんでした")
                return False
            
            # 確認ダイアログ
            confirm_msg = (
                f"以下の操作を実行します:\n\n"
                f"ファイル: {source_path.name}\n"
                f"コピー先: {target_path}\n"
                f"対象サブフォルダ数: {len(subfolders)}個\n\n"
                f"すべてのサブフォルダにファイルをコピーします。\n\n"
                f"実行しますか？"
            )
            if not messagebox.askyesno("確認", confirm_msg):
                logger.info("ユーザーが処理をキャンセルしました")
                return False
            
            # コピー実行
            self.copied_count = 0
            self.error_count = 0
            self.results = []
            
            for i, subfolder in enumerate(subfolders, 1):
                destination = subfolder / source_path.name
                
                try:
                    shutil.copy2(source_path, destination)
                    self.copied_count += 1
                    result_msg = f"✓ {subfolder.name}/{source_path.name}"
                    self.results.append(result_msg)
                    logger.info(f"コピー成功 ({i}/{len(subfolders)}): {destination}")
                except Exception as e:
                    self.error_count += 1
                    result_msg = f"✗ {subfolder.name}/{source_path.name} - エラー: {e}"
                    self.results.append(result_msg)
                    logger.error(f"コピー失敗 ({i}/{len(subfolders)}): {destination} - {e}")
                
                # 進捗表示（10件ごと）
                if i % 10 == 0:
                    logger.info(f"進捗: {i}/{len(subfolders)} フォルダ処理済み")
            
            logger.info("=" * 60)
            logger.info(f"ファイル一括コピー完了")
            logger.info(f"成功: {self.copied_count}件")
            logger.info(f"失敗: {self.error_count}件")
            logger.info("=" * 60)
            
            # 結果表示
            result_msg = (
                f"ファイル一括コピー完了!\n\n"
                f"ファイル: {source_path.name}\n"
                f"対象フォルダ数: {len(subfolders)}\n\n"
                f"成功: {self.copied_count}個\n"
                f"失敗: {self.error_count}個"
            )
            
            if self.copied_count == 0:
                result_msg += "\n\nサブフォルダが見つかりませんでした"
            
            messagebox.showinfo("完了", result_msg)
            
            # 詳細ログを出力
            logger.info("\n" + "=" * 60)
            logger.info("コピー結果の詳細:")
            logger.info("=" * 60)
            for result in self.results:
                logger.info(result)
            logger.info("=" * 60)
            
            # ターゲットフォルダを開く
            try:
                open_folder(target_path)
            except Exception as e:
                logger.warning(f"フォルダを開けませんでした: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"ファイル一括コピー中にエラーが発生しました: {e}")
            messagebox.showerror("エラー", f"ファイル一括コピー中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _select_source_file(self):
        """コピー元ファイル選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        root.update()
        
        try:
            file_path = filedialog.askopenfilename(
                parent=root,
                title="【Step5-1】コピーするファイルを選択してください",
                filetypes=[
                    ("すべてのファイル", "*.*"),
                    ("PDFファイル", "*.pdf"),
                    ("テキストファイル", "*.txt"),
                    ("画像ファイル", "*.jpg;*.jpeg;*.png;*.gif")
                ]
            )
            return file_path if file_path else None
        finally:
            root.destroy()
    
    def _select_target_folder(self):
        """コピー先フォルダ選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        root.update()
        
        try:
            folder_path = filedialog.askdirectory(
                parent=root,
                title="【Step5-2】コピー先の親フォルダを選択してください"
            )
            return folder_path if folder_path else None
        finally:
            root.destroy()


# スタンドアロン実行用
if __name__ == "__main__":
    copier = FileCopier()
    copier.run()

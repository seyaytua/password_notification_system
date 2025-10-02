"""
Module1: ファイル名変更（修正版）
CustomTkinterダイアログを使用してクラッシュを回避
"""
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from utils.logger import get_logger
from utils.csv_handler import read_csv
from utils.unicode_normalizer import normalize_string, clean_filename
from utils.file_operations import get_file_extension, get_account_name


logger = get_logger()


class FileRenamer:
    """ファイル名変更クラス"""
    
    def __init__(self, parent_ui=None):
        self.renamed_count = 0
        self.parent_ui = parent_ui  # 親UI（Dashboard）への参照
    
    def run(self):
        """
        メイン処理を実行
        
        Returns:
            bool: 成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Step 1: ファイル名変更を開始")
        logger.info("=" * 60)
        
        # CSVファイルを選択
        csv_path = self._select_csv_file()
        if not csv_path:
            logger.info("CSVファイルの選択がキャンセルされました")
            return False
        
        # 対象フォルダを選択
        folder_path = self._select_folder()
        if not folder_path:
            logger.info("フォルダの選択がキャンセルされました")
            return False
        
        # 講座名を入力（CustomTkinterダイアログ）
        course_name = self._input_course_name()
        if not course_name:
            logger.info("講座名の入力がキャンセルされました")
            return False
        
        # カテゴリ名を入力（CustomTkinterダイアログ）
        category_name = self._input_category_name()
        if not category_name:
            logger.info("カテゴリ名の入力がキャンセルされました")
            return False
        
        try:
            return self._execute_rename(csv_path, folder_path, course_name, category_name)
        except Exception as e:
            logger.error(f"ファイル名変更中にエラーが発生しました: {e}")
            messagebox.showerror("エラー", f"ファイル名変更中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _select_csv_file(self):
        """CSVファイル選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        root.update()
        
        try:
            file_path = filedialog.askopenfilename(
                parent=root,
                title="【Step1-1】講座受講者CSVファイルを選択してください",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            return file_path if file_path else None
        finally:
            root.destroy()
    
    def _select_folder(self):
        """フォルダ選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        root.update()
        
        try:
            folder_path = filedialog.askdirectory(
                parent=root,
                title="【Step1-2】リネーム対象のファイルがあるフォルダを選択してください"
            )
            return folder_path if folder_path else None
        finally:
            root.destroy()
    
    def _input_course_name(self):
        """講座名入力ダイアログ（CustomTkinter版）"""
        dialog = ctk.CTkInputDialog(
            text="講座名を入力してください:\n（例: 数学Ⅰイ①）",
            title="講座名入力"
        )
        # 親UIが指定されている場合は設定
        if self.parent_ui:
            dialog.transient(self.parent_ui)
        
        course_name = dialog.get_input()
        return course_name.strip() if course_name else None
    
    def _input_category_name(self):
        """カテゴリ名入力ダイアログ（CustomTkinter版）"""
        dialog = ctk.CTkInputDialog(
            text="カテゴリ名を入力してください:\n（例: document, test, homework）",
            title="カテゴリ名入力"
        )
        # 親UIが指定されている場合は設定
        if self.parent_ui:
            dialog.transient(self.parent_ui)
        
        category_name = dialog.get_input()
        return category_name.strip() if category_name else None
    
    def _execute_rename(self, csv_path, folder_path, course_name, category_name):
        """ファイル名変更を実行"""
        # CSVを読み込み
        df = read_csv(csv_path)
        
        # A列（講座名）、B列（メールアドレス）の確認
        if len(df.columns) < 2:
            messagebox.showerror(
                "エラー",
                "CSVファイルの列数が不足しています。\n"
                "A列: 講座名, B列: メールアドレス が必要です。"
            )
            logger.error("CSVファイルの列数が不足しています")
            return False
        
        # 該当講座の受講者を抽出
        course_students = df[df.iloc[:, 0] == course_name]
        
        if len(course_students) == 0:
            messagebox.showerror(
                "エラー",
                f"講座名「{course_name}」に該当する受講者が見つかりませんでした。"
            )
            logger.error(f"講座名「{course_name}」が見つかりません")
            return False
        
        # メールアドレスのリストを取得
        emails = course_students.iloc[:, 1].tolist()
        logger.info(f"該当受講者数: {len(emails)}")
        
        # 対象フォルダ内のファイル一覧を取得
        folder = Path(folder_path)
        files = sorted([f for f in folder.iterdir() if f.is_file()])
        logger.info(f"対象ファイル数: {len(files)}")
        
        # ファイル数と受講者数の照合
        if len(files) != len(emails):
            response = messagebox.askyesno(
                "確認",
                f"ファイル数と受講者数が一致しません。\n\n"
                f"ファイル数: {len(files)}\n"
                f"受講者数: {len(emails)}\n\n"
                f"処理を続行しますか？\n"
                f"（ファイル数分のみ処理されます）"
            )
            if not response:
                logger.info("ユーザーが処理をキャンセルしました")
                return False
        
        # 処理件数を決定
        process_count = min(len(files), len(emails))
        
        # 確認ダイアログ
        confirm_msg = (
            f"以下の内容でファイル名を変更します。\n\n"
            f"講座名: {course_name}\n"
            f"カテゴリ: {category_name}\n"
            f"処理件数: {process_count}件\n\n"
            f"実行しますか？"
        )
        if not messagebox.askyesno("確認", confirm_msg):
            logger.info("ユーザーが処理をキャンセルしました")
            return False
        
        # ファイル名変更を実行
        self.renamed_count = 0
        for i in range(process_count):
            file_path = files[i]
            email = emails[i]
            
            # 新しいファイル名を生成
            account_name = get_account_name(email)
            extension = get_file_extension(file_path.name)
            seq = i + 1
            
            # ファイル名の形式: {アカウント名}_{講座名}_{カテゴリ}_{連番}.{拡張子}
            new_filename = f"{account_name}_{course_name}_{category_name}_{seq}{extension}"
            
            # ファイル名をクリーンアップ
            new_filename = clean_filename(new_filename)
            
            # リネーム実行
            new_path = file_path.parent / new_filename
            
            try:
                file_path.rename(new_path)
                self.renamed_count += 1
                logger.info(f"変更 ({seq}/{process_count}): {file_path.name} → {new_filename}")
            except Exception as e:
                logger.error(f"ファイル名変更に失敗: {file_path.name} - {e}")
        
        logger.info("=" * 60)
        logger.info(f"ファイル名変更完了: {self.renamed_count}件")
        logger.info("=" * 60)
        
        # 結果表示
        result_msg = (
            f"ファイル名変更完了!\n\n"
            f"変更したファイル数: {self.renamed_count}件\n"
            f"講座名: {course_name}\n"
            f"カテゴリ: {category_name}"
        )
        messagebox.showinfo("完了", result_msg)
        
        return True


# スタンドアロン実行用
if __name__ == "__main__":
    renamer = FileRenamer()
    renamer.run()

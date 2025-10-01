"""
Module4: ファイル振り分け
ファイルを各生徒のフォルダに配置
"""
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.logger import get_logger
from utils.file_operations import open_folder


logger = get_logger()


class FileOrganizer:
    """ファイル振り分けクラス"""
    
    def __init__(self):
        self.copied_files = 0
        self.skipped_files = 0
        self.unmatched_files = 0
    
    def run(self):
        """
        メイン処理を実行
        
        Returns:
            bool: 成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Step 4: ファイル振り分けを開始")
        logger.info("=" * 60)
        
        # ソースフォルダを選択
        source_folder = self._select_source_folder()
        if not source_folder:
            logger.info("ソースフォルダの選択がキャンセルされました")
            return False
        
        # ターゲットフォルダを選択
        target_root = self._select_target_folder()
        if not target_root:
            logger.info("ターゲットフォルダの選択がキャンセルされました")
            return False
        
        source_path = Path(source_folder)
        target_root_path = Path(target_root)
        
        # フォルダの存在確認
        if not source_path.exists():
            messagebox.showerror("エラー", f"ソースフォルダが存在しません:\n{source_folder}")
            logger.error(f"ソースフォルダが存在しません: {source_folder}")
            return False
        
        if not target_root_path.exists():
            messagebox.showerror("エラー", f"ターゲットフォルダが存在しません:\n{target_root}")
            logger.error(f"ターゲットフォルダが存在しません: {target_root}")
            return False
        
        try:
            logger.info(f"ソースフォルダ: {source_path}")
            logger.info(f"ターゲットルート: {target_root_path}")
            
            # ソースフォルダのファイル一覧を取得
            source_files = [f for f in source_path.iterdir() if f.is_file()]
            logger.info(f"対象ファイル数: {len(source_files)}")
            
            if len(source_files) == 0:
                messagebox.showinfo("情報", "ソースフォルダにファイルがありません。")
                logger.info("ソースフォルダにファイルがありません")
                return False
            
            # ターゲットフォルダ一覧を取得
            target_folders = [d for d in target_root_path.iterdir() if d.is_dir()]
            logger.info(f"検索対象フォルダ数: {len(target_folders)}")
            
            if len(target_folders) == 0:
                messagebox.showerror("エラー", "ターゲットフォルダ内にサブフォルダが見つかりません。")
                logger.error("ターゲットフォルダ内にサブフォルダがありません")
                return False
            
            # 確認ダイアログ
            confirm_msg = (
                f"以下の内容でファイルを振り分けます。\n\n"
                f"対象ファイル数: {len(source_files)}\n"
                f"振り分け先フォルダ数: {len(target_folders)}\n\n"
                f"実行しますか？"
            )
            if not messagebox.askyesno("確認", confirm_msg):
                logger.info("ユーザーが処理をキャンセルしました")
                return False
            
            # カウンター初期化
            self.copied_files = 0
            self.skipped_files = 0
            self.unmatched_files = 0
            
            # 各ファイルを処理
            for i, source_file in enumerate(source_files, 1):
                file_name = source_file.name
                
                # ファイル名の最初の8文字を取得
                file_prefix = file_name[:8] if len(file_name) >= 8 else file_name
                
                logger.info(f"処理中 ({i}/{len(source_files)}): {file_name} (prefix: {file_prefix})")
                
                # 作成したフォルダと照合
                match_found = False
                for target_folder in target_folders:
                    folder_name = target_folder.name
                    
                    # フォルダ名の最初の8文字と比較
                    if len(folder_name) >= 8 and folder_name[:8] == file_prefix:
                        target_file_path = target_folder / file_name
                        
                        # ファイルが既に存在しない場合のみコピー
                        if not target_file_path.exists():
                            shutil.copy2(source_file, target_file_path)
                            self.copied_files += 1
                            logger.info(f"→ コピー: {file_name} → {folder_name}")
                        else:
                            self.skipped_files += 1
                            logger.info(f"→ スキップ（既存）: {file_name} → {folder_name}")
                        
                        match_found = True
                        break  # マッチしたら次のファイルへ
                
                # マッチしなかったファイルをログ出力
                if not match_found:
                    self.unmatched_files += 1
                    logger.warning(f"→ マッチなし: {file_name} (prefix: {file_prefix})")
                
                # 進捗表示（10件ごと）
                if i % 10 == 0:
                    logger.info(f"進捗: {i}/{len(source_files)} ファイル処理済み")
            
            logger.info("=" * 60)
            logger.info(f"ファイル振り分け完了")
            logger.info(f"コピー: {self.copied_files}件")
            logger.info(f"スキップ: {self.skipped_files}件")
            logger.info(f"マッチなし: {self.unmatched_files}件")
            logger.info("=" * 60)
            
            # 結果表示
            result_msg = (
                f"ファイル振り分け完了!\n\n"
                f"処理したファイル数: {len(source_files)}\n"
                f"コピーしたファイル: {self.copied_files}件\n"
                f"スキップしたファイル: {self.skipped_files}件\n"
                f"マッチしなかったファイル: {self.unmatched_files}件"
            )
            messagebox.showinfo("完了", result_msg)
            
            # ターゲットフォルダを開く
            try:
                open_folder(target_root_path)
            except Exception as e:
                logger.warning(f"フォルダを開けませんでした: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"ファイル振り分け中にエラーが発生しました: {e}")
            messagebox.showerror("エラー", f"ファイル振り分け中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _select_source_folder(self):
        """ソースフォルダ選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(
            title="【Step4-1】整理したいファイルがあるフォルダを選択してください"
        )
        return folder_path if folder_path else None
    
    def _select_target_folder(self):
        """ターゲットフォルダ選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(
            title="【Step4-2】個人フォルダ群のルートフォルダを選択してください"
        )
        return folder_path if folder_path else None


# スタンドアロン実行用
if __name__ == "__main__":
    organizer = FileOrganizer()
    organizer.run()

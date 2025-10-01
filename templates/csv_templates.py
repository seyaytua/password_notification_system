"""
CSVテンプレート生成モジュール
"""
import pandas as pd
from pathlib import Path
from tkinter import filedialog
import tkinter as tk
from utils.logger import get_logger


logger = get_logger()


class CSVTemplateGenerator:
    """CSVテンプレート生成クラス"""
    
    @staticmethod
    def generate_step1_template():
        """
        Step1（ファイル名変更）用のCSVテンプレートを生成
        
        Returns:
            bool: 成功した場合True
        """
        # ヘッダー行のみのデータフレーム
        df = pd.DataFrame(columns=['講座名', 'メールアドレス'])
        
        # 保存先を選択
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Step1用CSVテンプレートの保存先を選択",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="step1_file_rename.csv"
        )
        
        if not file_path:
            logger.info("テンプレート保存がキャンセルされました")
            return False
        
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            logger.info(f"Step1用テンプレートを保存しました: {file_path}")
            return True
        except Exception as e:
            logger.error(f"テンプレート保存に失敗しました: {e}")
            return False
    
    @staticmethod
    def generate_step2_template():
        """
        Step2（フォルダ作成）用のCSVテンプレートを生成
        
        Returns:
            bool: 成功した場合True
        """
        # ヘッダー行のみのデータフレーム
        df = pd.DataFrame(columns=['生徒番号', '出席番号', '氏名', 'ふりがな', 'メールアドレス'])
        
        # 保存先を選択
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Step2用CSVテンプレートの保存先を選択",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="step2_folder_create.csv"
        )
        
        if not file_path:
            logger.info("テンプレート保存がキャンセルされました")
            return False
        
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            logger.info(f"Step2用テンプレートを保存しました: {file_path}")
            return True
        except Exception as e:
            logger.error(f"テンプレート保存に失敗しました: {e}")
            return False
    
    @staticmethod
    def generate_step3_template():
        """
        Step3（ライセンスPDF作成）用のCSVテンプレートを生成
        
        Returns:
            bool: 成功した場合True
        """
        # ヘッダー行（15教科分 = 60列）
        headers = ['メールアドレス']
        for i in range(1, 16):
            headers.extend([
                f'教科書名{i}',
                f'ID{i}',
                f'PASSWORD{i}',
                f'SERIAL CODE{i}'
            ])
        
        df = pd.DataFrame(columns=headers)
        
        # 保存先を選択
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Step3用CSVテンプレートの保存先を選択",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="step3_license_pdf.csv"
        )
        
        if not file_path:
            logger.info("テンプレート保存がキャンセルされました")
            return False
        
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            logger.info(f"Step3用テンプレートを保存しました: {file_path}")
            return True
        except Exception as e:
            logger.error(f"テンプレート保存に失敗しました: {e}")
            return False

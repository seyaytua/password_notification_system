"""
Module3: ライセンスPDF作成
CSVからライセンス情報PDFを生成
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from utils.logger import get_logger
from utils.csv_handler import read_csv
from utils.file_operations import get_account_name, open_folder


logger = get_logger()


class LicensePdfGenerator:
    """ライセンスPDF生成クラス"""
    
    def __init__(self):
        self.generated_count = 0
        self.skipped_count = 0
        self.jp_font = self._register_japanese_font()
    
    def _register_japanese_font(self):
        """日本語フォントを登録"""
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
            logger.info("日本語フォント（HeiseiKakuGo-W5）を登録しました")
            return 'HeiseiKakuGo-W5'
        except Exception as e:
            logger.error(f"日本語フォント登録エラー: {e}")
            return 'HeiseiKakuGo-W5'
    
    def run(self):
        """
        メイン処理を実行
        
        Returns:
            bool: 成功した場合True
        """
        logger.info("=" * 60)
        logger.info("Step 3: ライセンスPDF作成を開始")
        logger.info("=" * 60)
        
        # CSVファイルを選択
        csv_path = self._select_csv_file()
        if not csv_path:
            logger.info("CSVファイルの選択がキャンセルされました")
            return False
        
        # 出力先フォルダを選択
        output_folder = self._select_output_folder()
        if not output_folder:
            logger.info("出力先フォルダの選択がキャンセルされました")
            return False
        
        try:
            # CSVを読み込み
            df = read_csv(csv_path)
            
            if len(df) == 0:
                messagebox.showerror("エラー", "CSVにデータがありません。")
                logger.error("CSVにデータがありません")
                return False
            
            logger.info(f"対象生徒数: {len(df)}")
            
            # タイムスタンプ
            timestamp_str = datetime.now().strftime("%Y.%m.%d")
            
            # 各生徒のPDFを生成
            self.generated_count = 0
            self.skipped_count = 0
            
            for index, row in df.iterrows():
                email = row.iloc[0].strip() if row.iloc[0] else ""
                
                if not email:
                    self.skipped_count += 1
                    logger.warning(f"スキップ: {index+1}行目 - メールアドレスが空です")
                    continue
                
                # 教科書情報を抽出
                textbook_data = self._extract_textbook_data(row)
                
                if not textbook_data:
                    self.skipped_count += 1
                    logger.warning(f"スキップ: {email} - 有効な教科書データがありません")
                    continue
                
                # PDFを生成
                success = self._create_pdf(email, textbook_data, output_folder, timestamp_str)
                if success:
                    self.generated_count += 1
                    logger.info(f"生成 ({self.generated_count}/{len(df)}): {email} ({len(textbook_data)}教科)")
                else:
                    self.skipped_count += 1
            
            logger.info("=" * 60)
            logger.info(f"ライセンスPDF作成完了")
            logger.info(f"生成: {self.generated_count}件")
            logger.info(f"スキップ: {self.skipped_count}件")
            logger.info("=" * 60)
            
            # 結果表示
            result_msg = (
                f"ライセンスPDF作成完了!\n\n"
                f"生成したPDF: {self.generated_count}件\n"
                f"スキップ: {self.skipped_count}件\n"
                f"出力先: {output_folder}"
            )
            messagebox.showinfo("完了", result_msg)
            
            # 出力フォルダを開く
            try:
                open_folder(output_folder)
            except Exception as e:
                logger.warning(f"フォルダを開けませんでした: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"ライセンスPDF作成中にエラーが発生しました: {e}")
            messagebox.showerror("エラー", f"ライセンスPDF作成中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _extract_textbook_data(self, row):
        """
        行から教科書データを抽出
        
        Args:
            row: DataFrameの行
        
        Returns:
            list: 教科書データのリスト
        """
        textbook_data = []
        
        # B列から4列セットで処理
        col_index = 1
        while col_index + 3 < len(row):
            textbook_name = row.iloc[col_index].strip() if row.iloc[col_index] else ""
            user_id = row.iloc[col_index + 1].strip() if row.iloc[col_index + 1] else ""
            password = row.iloc[col_index + 2].strip() if row.iloc[col_index + 2] else ""
            serial_code = row.iloc[col_index + 3].strip() if row.iloc[col_index + 3] else ""
            
            # 教科書名が存在する場合のみ追加
            if textbook_name:
                textbook_data.append({
                    "name": textbook_name,
                    "id": user_id,
                    "password": password,
                    "serial": serial_code
                })
            
            col_index += 4
        
        return textbook_data
    
    def _create_pdf(self, email, textbook_data, output_folder, timestamp_str):
        """
        PDFファイルを生成
        
        Args:
            email (str): メールアドレス
            textbook_data (list): 教科書データ
            output_folder (str): 出力先フォルダ
            timestamp_str (str): タイムスタンプ文字列
        
        Returns:
            bool: 成功した場合True
        """
        try:
            account_name = get_account_name(email)
            pdf_filename = f"{account_name}_ライセンス情報.pdf"
            pdf_path = Path(output_folder) / pdf_filename
            
            # PDFドキュメントを作成
            doc = SimpleDocTemplate(
                str(pdf_path),
                pagesize=A4,
                leftMargin=20*mm,
                rightMargin=20*mm,
                topMargin=25*mm,
                bottomMargin=20*mm
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # スタイル定義
            main_title_style = ParagraphStyle(
                name='MainTitle',
                parent=styles['Title'],
                fontName=self.jp_font,
                fontSize=18,
                leading=22,
                spaceAfter=6,
                textColor=colors.black,
                alignment=0
            )
            
            caution_style = ParagraphStyle(
                name='Caution',
                parent=styles['Normal'],
                fontName=self.jp_font,
                fontSize=10,
                leading=14,
                spaceAfter=20,
                textColor=colors.HexColor('#d9534f')
            )
            
            textbook_title_style = ParagraphStyle(
                name='TextbookTitle',
                parent=styles['Heading2'],
                fontName=self.jp_font,
                fontSize=14,
                leading=18,
                spaceAfter=8,
                textColor=colors.HexColor('#343a40')
            )
            
            info_label_style = ParagraphStyle(
                name='InfoLabel',
                parent=styles['Normal'],
                fontSize=10,
                leading=16,
                textColor=colors.black,
                fontName='Helvetica'
            )
            
            info_value_style = ParagraphStyle(
                name='InfoValue',
                parent=styles['Normal'],
                fontSize=11,
                leading=16,
                textColor=colors.black,
                fontName=self.jp_font
            )
            
            # タイトルと注意書き
            story.append(Paragraph("ライセンス情報", main_title_style))
            story.append(Paragraph("この情報は他の人と共有しないでください", caution_style))
            
            # 各教科書の情報
            for data in textbook_data:
                story.append(Paragraph(f"教科書：{data['name']}", textbook_title_style))
                
                info_rows = []
                
                # IDがある場合
                if data['id']:
                    info_rows.append([
                        Paragraph("ID:", info_label_style),
                        Paragraph(data['id'], info_value_style)
                    ])
                
                # パスワードがある場合
                if data['password']:
                    info_rows.append([
                        Paragraph("PASSWORD:", info_label_style),
                        Paragraph(data['password'], info_value_style)
                    ])
                
                # シリアルコードがある場合
                if data['serial']:
                    info_rows.append([
                        Paragraph("SERIAL CODE:", info_label_style),
                        Paragraph(data['serial'], info_value_style)
                    ])
                
                # 情報テーブル
                if info_rows:
                    info_table = Table(info_rows, colWidths=[35*mm, 115*mm])
                    info_table.setStyle(TableStyle([
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
                        ('PADDING', (0,0), (-1,-1), 8),
                        ('LEFTPADDING', (0,0), (0,-1), 10),
                        ('ALIGN', (0,0), (0,-1), 'LEFT'),
                        ('ALIGN', (1,0), (1,-1), 'LEFT'),
                    ]))
                    story.append(info_table)
                
                story.append(Spacer(1, 10*mm))
            
            # PDFを生成
            doc.build(story, onFirstPage=lambda c, d: self._add_header(c, d, timestamp_str),
                     onLaterPages=lambda c, d: self._add_header(c, d, timestamp_str))
            
            return True
            
        except Exception as e:
            logger.error(f"PDF生成エラー ({email}): {e}")
            return False
    
    def _add_header(self, canvas, doc, timestamp_str):
        """PDFヘッダーを追加"""
        canvas.saveState()
        
        box_width = 35*mm
        box_height = 6*mm
        x_position = A4[0] - 20*mm - box_width
        y_position = A4[1] - 12*mm - box_height/2
        
        canvas.setFillColor(colors.HexColor('#f8f9fa'))
        canvas.setStrokeColor(colors.HexColor('#dee2e6'))
        canvas.setLineWidth(0.5)
        canvas.roundRect(x_position, y_position, box_width, box_height, 2, fill=1, stroke=1)
        
        canvas.setFillColor(colors.HexColor('#6c757d'))
        canvas.setFont('Helvetica', 8)
        canvas.drawString(
            x_position + 2*mm,
            y_position + 2*mm,
            f"Issue Date: {timestamp_str}"
        )
        
        canvas.restoreState()
    
    def _select_csv_file(self):
        """CSVファイル選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="【Step3-1】ライセンス情報CSVファイルを選択してください",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        return file_path if file_path else None
    
    def _select_output_folder(self):
        """出力先フォルダ選択ダイアログ"""
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(
            title="【Step3-2】PDFの出力先フォルダを選択してください"
        )
        return folder_path if folder_path else None


# スタンドアロン実行用
if __name__ == "__main__":
    generator = LicensePdfGenerator()
    generator.run()

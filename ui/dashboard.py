"""
メインダッシュボードUI（Step5追加版）
"""
import customtkinter as ctk
from tkinter import messagebox
from ui.log_viewer import LogViewer
from modules.folder_creator import FolderCreator
from modules.file_renamer import FileRenamer
from modules.license_pdf_generator import LicensePdfGenerator
from modules.file_organizer import FileOrganizer
from modules.file_copier import FileCopier
from templates.csv_templates import CSVTemplateGenerator
from utils.logger import get_logger


logger = get_logger()


class Dashboard(ctk.CTk):
    """メインダッシュボード"""
    
    def __init__(self):
        super().__init__()
        
        # ウィンドウ設定
        self.title("パスワードお知らせシステム - 環境構築ダッシュボード")
        self.geometry("900x900")  # 高さを増やしてStep5を追加
        
        # カラーテーマ
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # UI構築
        self._create_ui()
        
        logger.info("ダッシュボードを起動しました")
    
    def _create_ui(self):
        """UI要素を作成"""
        
        # ヘッダー
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title = ctk.CTkLabel(
            header_frame,
            text="パスワードお知らせシステム",
            font=("Arial", 28, "bold"),
            text_color="#1976D2"
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="環境構築ツール統合ダッシュボード",
            font=("Arial", 14),
            text_color="#757575"
        )
        subtitle.pack()
        
        # メインコンテンツフレーム（スクロール可能）
        main_frame = ctk.CTkScrollableFrame(self, height=400)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # ツールカード
        self._create_tool_card(
            main_frame,
            "Step 1: ファイル名変更",
            "スキャンPDFのファイル名を統一形式に変更",
            self.run_step1,
            self.export_step1_template,
            row=0
        )
        
        self._create_tool_card(
            main_frame,
            "Step 2: フォルダ作成",
            "CSVから生徒ごとのフォルダを作成",
            self.run_step2,
            self.export_step2_template,
            row=1
        )
        
        self._create_tool_card(
            main_frame,
            "Step 3: ライセンスPDF作成",
            "CSVからライセンス情報PDFを生成",
            self.run_step3,
            self.export_step3_template,
            row=2
        )
        
        self._create_tool_card(
            main_frame,
            "Step 4: ファイル振り分け",
            "ファイルを各生徒のフォルダに配置",
            self.run_step4,
            None,
            row=3
        )
        
        self._create_tool_card(
            main_frame,
            "Step 5: ファイル一括コピー",
            "1つのファイルをすべてのサブフォルダにコピー",
            self.run_step5,
            None,
            row=4
        )
        
        # ログビューアー
        self.log_viewer = LogViewer(self)
        self.log_viewer.pack(pady=10, padx=20, fill="both", expand=True)
        
        # ステータスバー
        status_frame = ctk.CTkFrame(self, height=40)
        status_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="準備完了 - 処理を開始してください",
            font=("Arial", 11),
            text_color="#757575"
        )
        self.status_label.pack(pady=5)
    
    def _create_tool_card(self, parent, title, description, run_command, template_command, row):
        """ツールカードを作成"""
        card = ctk.CTkFrame(parent, fg_color="#F5F5F5", corner_radius=8)
        card.grid(row=row, column=0, pady=8, padx=10, sticky="ew")
        parent.grid_columnconfigure(0, weight=1)
        
        # 左側: ボタンとテンプレート
        left_frame = ctk.CTkFrame(card, fg_color="transparent")
        left_frame.pack(side="left", padx=15, pady=10)
        
        # 実行ボタン
        run_btn = ctk.CTkButton(
            left_frame,
            text="実行",
            command=run_command,
            width=100,
            height=35,
            font=("Arial", 13, "bold"),
            fg_color="#1976D2",
            hover_color="#1565C0"
        )
        run_btn.pack(side="left", padx=5)
        
        # テンプレート出力ボタン
        if template_command:
            template_btn = ctk.CTkButton(
                left_frame,
                text="📄 CSVテンプレート",
                command=template_command,
                width=160,
                height=35,
                font=("Arial", 12),
                fg_color="#FFFFFF",
                text_color="#212121",
                border_width=1,
                border_color="#E0E0E0",
                hover_color="#EEEEEE"
            )
            template_btn.pack(side="left", padx=5)
        
        # 右側: 説明
        right_frame = ctk.CTkFrame(card, fg_color="transparent")
        right_frame.pack(side="left", fill="x", expand=True, padx=10)
        
        title_label = ctk.CTkLabel(
            right_frame,
            text=title,
            font=("Arial", 14, "bold"),
            text_color="#212121",
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            right_frame,
            text=description,
            font=("Arial", 11),
            text_color="#757575",
            anchor="w"
        )
        desc_label.pack(anchor="w")
    
    def update_status(self, message, color="#757575"):
        """ステータスメッセージを更新"""
        self.status_label.configure(text=message, text_color=color)
        self.update()
    
    # Step 1
    def run_step1(self):
        """Step 1: ファイル名変更を実行"""
        self.update_status("Step 1: ファイル名変更を実行中...", "#1976D2")
        try:
            renamer = FileRenamer(parent_ui=self)
            success = renamer.run()
            if success:
                self.update_status("✓ Step 1 完了: ファイル名変更成功", "#4CAF50")
            else:
                self.update_status("Step 1 キャンセル", "#757575")
        except Exception as e:
            logger.error(f"Step 1でエラーが発生しました: {e}")
            self.update_status("✗ Step 1 エラー", "#F44336")
    
    def export_step1_template(self):
        """Step 1用CSVテンプレートを出力"""
        success = CSVTemplateGenerator.generate_step1_template()
        if success:
            messagebox.showinfo("完了", "Step1用CSVテンプレートを保存しました。")
    
    # Step 2
    def run_step2(self):
        """Step 2: フォルダ作成を実行"""
        self.update_status("Step 2: フォルダ作成を実行中...", "#1976D2")
        try:
            creator = FolderCreator()
            success = creator.run()
            if success:
                self.update_status("✓ Step 2 完了: フォルダ作成成功", "#4CAF50")
            else:
                self.update_status("Step 2 キャンセル", "#757575")
        except Exception as e:
            logger.error(f"Step 2でエラーが発生しました: {e}")
            self.update_status("✗ Step 2 エラー", "#F44336")
    
    def export_step2_template(self):
        """Step 2用CSVテンプレートを出力"""
        success = CSVTemplateGenerator.generate_step2_template()
        if success:
            messagebox.showinfo("完了", "Step2用CSVテンプレートを保存しました。")
    
    # Step 3
    def run_step3(self):
        """Step 3: ライセンスPDF作成を実行"""
        self.update_status("Step 3: ライセンスPDF作成を実行中...", "#1976D2")
        try:
            generator = LicensePdfGenerator()
            success = generator.run()
            if success:
                self.update_status("✓ Step 3 完了: PDF作成成功", "#4CAF50")
            else:
                self.update_status("Step 3 キャンセル", "#757575")
        except Exception as e:
            logger.error(f"Step 3でエラーが発生しました: {e}")
            self.update_status("✗ Step 3 エラー", "#F44336")
    
    def export_step3_template(self):
        """Step 3用CSVテンプレートを出力"""
        success = CSVTemplateGenerator.generate_step3_template()
        if success:
            messagebox.showinfo("完了", "Step3用CSVテンプレートを保存しました。")
    
    # Step 4
    def run_step4(self):
        """Step 4: ファイル振り分けを実行"""
        self.update_status("Step 4: ファイル振り分けを実行中...", "#1976D2")
        try:
            organizer = FileOrganizer()
            success = organizer.run()
            if success:
                self.update_status("✓ Step 4 完了: ファイル振り分け成功", "#4CAF50")
            else:
                self.update_status("Step 4 キャンセル", "#757575")
        except Exception as e:
            logger.error(f"Step 4でエラーが発生しました: {e}")
            self.update_status("✗ Step 4 エラー", "#F44336")
    
    # Step 5（新規追加）
    def run_step5(self):
        """Step 5: ファイル一括コピーを実行"""
        self.update_status("Step 5: ファイル一括コピーを実行中...", "#1976D2")
        try:
            copier = FileCopier()
            success = copier.run()
            if success:
                self.update_status("✓ Step 5 完了: ファイル一括コピー成功", "#4CAF50")
            else:
                self.update_status("Step 5 キャンセル", "#757575")
        except Exception as e:
            logger.error(f"Step 5でエラーが発生しました: {e}")
            self.update_status("✗ Step 5 エラー", "#F44336")

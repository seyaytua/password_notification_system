# パスワードお知らせシステム

生徒ごとのライセンス情報とスキャンデータを個別フォルダに整理し、Microsoft Power AutomateによるURL配信システムの環境を構築するツールです。

## 機能

### Step 1: ファイル名変更
スキャンしたPDFファイルを、生徒のメールアドレスと講座情報に基づいてリネームします。

### Step 2: フォルダ作成
生徒マスタCSVから、生徒ごとの個人フォルダを一括作成します。

### Step 3: ライセンスPDF作成
ライセンス情報CSVから、生徒ごとにライセンス情報をまとめたPDFを生成します。

### Step 4: ファイル振り分け
リネーム済みファイルとライセンスPDFを、ファイル名の最初8文字とフォルダ名の最初8文字を照合して、該当する個人フォルダに振り分けます。

## インストール

### 必要要件
- Python 3.9以上

### セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd password_notification_system

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存ライブラリをインストール
pip install -r requirements.txt
使用方法
Copypython main.py
CSVフォーマット
Step 1用: 講座受講者リスト
講座名,メールアドレス
数学Ⅰイ①,tanaka@school.jp
数学Ⅰイ①,suzuki@school.jp
Step 2用: 生徒マスタ
生徒番号,出席番号,氏名,ふりがな,メールアドレス
2024001,F1211,田中太郎,たなかたろう,tanaka@school.jp
Step 3用: ライセンス情報
メールアドレス,教科書名1,ID1,PASSWORD1,SERIAL CODE1,...
tanaka@school.jp,数学I,tanaka_math,pass123,SN-001,...
ライセンス
MIT License

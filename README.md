# arXiv 論文取得・要約スクリプト

## 概要
このスクリプトは、arXiv APIを使用して指定した期間の論文を検索・ダウンロードし、Excelファイルに整理して保存します。

## ファイル構成
```
★論文/
├── get_arXiv.py          # メインスクリプト
├── config.ini            # 設定ファイル（実行前に編集）
├── config.ini.template   # 設定ファイルのテンプレート
├── verify_config.py      # 設定確認用スクリプト
└── README.md             # このファイル
```

## 必要なライブラリ
```bash
pip install -r requirements.txt
```

または個別にインストール：
```bash
pip install openai==0.28.1 feedparser PyMuPDF requests pandas openpyxl
```

## 環境変数の設定（要約機能を使用する場合）

Azure OpenAI APIを使用して論文を要約する場合、以下の環境変数を設定してください。

### Windows (PowerShell)
```powershell
$env:AZURE_OPENAI_API_KEY="your_api_key_here"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
$env:AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

### Linux / macOS
```bash
export AZURE_OPENAI_API_KEY="your_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

### .env ファイルを使用する場合
1. `.env.example` を `.env` にコピー
2. `.env` ファイルに実際の API キーなどを記入
3. プログラムで読み込む（別途 python-dotenv などが必要）

**⚠️ 注意:** 
- API キーは絶対に GitHub などに公開しないでください
- `.env` ファイルは `.gitignore` に含まれています
- 現在、要約機能は `arxiv_cli.py` 内でコメントアウトされています

## 使い方

### 1. 設定ファイルの編集
`config.ini` を開いて、以下の項目を編集します：

```ini
[DateRange]
start_date = 2024/01/01  # 検索開始日（YYYY/MM/DD形式）
end_date = 2024/01/31    # 検索終了日（YYYY/MM/DD形式）

[Search]
query = all:"machine learning"  # 検索クエリ
max_results = 100               # 最大取得件数

[Files]
excel_file = arxiv_summaries.xlsx  # 出力ファイル名
```

### 2. 設定の確認（オプション）
設定が正しく読み込まれるか確認します：
```bash
python verify_config.py
```

### 3. スクリプトの実行
```bash
python get_arXiv.py
```

## 設定項目の詳細

### [DateRange] - 日付範囲
| 項目 | 説明 | 形式 | 例 |
|------|------|------|-----|
| start_date | 検索開始日 | YYYY/MM/DD | 2024/01/01 |
| end_date | 検索終了日 | YYYY/MM/DD | 2024/01/31 |

**注意:**
- 1日だけ処理する場合は、`start_date` と `end_date` を同じ日付に設定
- `start_date` は `end_date` 以前の日付である必要があります

### [Search] - 検索設定
| 項目 | 説明 | 形式 | 例 |
|------|------|------|-----|
| query | arXiv検索クエリ | テキスト | all:"machine learning" |
| max_results | 最大取得件数 | 数値 | 100 |

**検索クエリの例:**
- `all:"machine learning"` - すべてのフィールドから検索
- `ti:"neural network"` - タイトルのみ検索
- `au:"Smith"` - 著者名で検索
- `all:"ML" OR all:"AI"` - 複数キーワード（OR検索）
- `all:"ML" AND all:"AI"` - 複数キーワード（AND検索）

### [Files] - ファイル設定
| 項目 | 説明 | 形式 | 例 |
|------|------|------|-----|
| excel_file | Excel出力ファイル名 | ファイルパス | arxiv_summaries.xlsx |

**パスの指定方法:**
- 相対パス: `arxiv_summaries.xlsx`（スクリプトと同じフォルダに保存）
- 絶対パス: `C:\Users\YourName\Documents\results.xlsx`

## 出力結果

### Excelファイル
- **ファイル名:** `config.ini` の `excel_file` で指定
- **シート名:** 日付ごと（例: `2024-01-01`）
- **列:**
  - 投稿日
  - タイトル
  - arXiv ID
  - PDF URL
  - ファイル名
  - 要約

### PDFファイル
- **保存場所:** 日付フォルダ（例: `20240101/`）
- **ファイル名:** arXiv ID（例: `2401.12345.pdf`）

### ログファイル
- **ファイル名:** `arxiv_process.log`
- **内容:** 処理の詳細ログ

## 実行例

### 例1: 1日だけ処理
```ini
[DateRange]
start_date = 2024/01/15
end_date = 2024/01/15
```

### 例2: 1週間分処理
```ini
[DateRange]
start_date = 2024/01/01
end_date = 2024/01/07
```

### 例3: 複数キーワード検索
```ini
[Search]
query = all:"model extraction" OR all:"prompt injection"
max_results = 200
```

## トラブルシューティング

### エラー: "設定ファイルが見つかりません"
→ `config.ini` が存在しません。`config.ini.template` をコピーして `config.ini` を作成してください。

### エラー: "start_dateがend_dateより後の日付になっています"
→ `config.ini` の日付を確認してください。`start_date` は `end_date` 以前である必要があります。

### エラー: "Excelファイルが開かれています"
→ 出力先のExcelファイルを閉じてから再実行してください。

### 警告: "既に調査済みです"
→ その日付は既に処理済みです。再処理したい場合は、Excelファイルの該当シートを削除してください。

## 注意事項

1. **arXiv APIのレート制限**
   - 短時間に大量のリクエストを送ると制限される可能性があります
   - `max_results` は100～500程度を推奨

2. **日付範囲**
   - 長期間（数ヶ月～年単位）を指定すると、処理に時間がかかります
   - 必要に応じて期間を分割して実行してください

3. **要約機能**
   - 現在、OpenAI API呼び出しはコメントアウトされています
   - 要約機能を有効にする場合は、`get_arXiv.py` の該当部分のコメントを解除してください

## ライセンス
このスクリプトは教育・研究目的で使用してください。

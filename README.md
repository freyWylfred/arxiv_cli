# arXiv 論文取得・要約スクリプト

arXiv APIを使用して指定した期間の論文を検索・ダウンロードし、Excelファイルに整理して保存します。
オプションでAzure OpenAI APIを使用した日本語要約機能も利用できます。

## ファイル構成

```
arxiv_cli/
├── arxiv_cli.py          # メインスクリプト
├── config.ini            # 設定ファイル（実行前に編集）
├── config.ini.template   # 設定ファイルのテンプレート
├── verify_config.py      # 設定確認用スクリプト
├── requirements.txt      # 必要なライブラリ
├── .env.example          # 環境変数のサンプル
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

## クイックスタート

1. `config.ini.template` を `config.ini` にコピー
2. `config.ini` を編集して検索条件を設定
3. `python arxiv_cli.py` を実行

## 設定ファイル (config.ini)

### 基本設定

```ini
[DateRange]
start_date = 2024/01/01    # 検索開始日（YYYY/MM/DD形式）
end_date = 2024/01/31      # 検索終了日（YYYY/MM/DD形式）
today_only = false         # trueにすると今日の論文のみ取得

[Search]
query = all:"machine learning"  # 検索クエリ
max_results = 100               # 最大取得件数

[Files]
excel_file = arxiv_summaries.xlsx  # 出力ファイル名

[OpenAI]
use_openai = false  # OpenAI要約機能（true/false）
```

### OpenAI要約機能

`use_openai = true` に設定すると、Azure OpenAI APIを使用して論文の要約を自動生成します。

**デフォルト: false（無効）**

要約機能を使用する場合は、以下の環境変数を設定してください：

#### Windows (PowerShell)
```powershell
$env:AZURE_OPENAI_API_KEY="your_api_key_here"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
$env:AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

#### Linux / macOS
```bash
export AZURE_OPENAI_API_KEY="your_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

## 使い方

### 1. 設定ファイルの準備
```bash
cp config.ini.template config.ini
```

### 2. 設定の編集
`config.ini` を開いて検索条件を編集します。

### 3. 設定の確認（オプション）
```bash
python verify_config.py
```

### 4. スクリプトの実行
```bash
python arxiv_cli.py
```

## 設定項目の詳細

### [DateRange] - 日付範囲

| 項目 | 説明 | 形式 | 例 |
|------|------|------|-----|
| start_date | 検索開始日 | YYYY/MM/DD | 2024/01/01 |
| end_date | 検索終了日 | YYYY/MM/DD | 2024/01/31 |
| today_only | 今日のみモード | true/false | false |

### [Search] - 検索設定

| 項目 | 説明 | 例 |
|------|------|-----|
| query | arXiv検索クエリ | all:"machine learning" |
| max_results | 最大取得件数 | 100 |

**検索クエリの例:**
- `all:"machine learning"` - すべてのフィールドから検索
- `ti:"neural network"` - タイトルのみ検索
- `au:"Smith"` - 著者名で検索
- `all:"ML" OR all:"AI"` - 複数キーワード（OR検索）
- `all:"ML" AND all:"AI"` - 複数キーワード（AND検索）

### [Files] - ファイル設定

| 項目 | 説明 | 例 |
|------|------|-----|
| excel_file | Excel出力ファイル名 | arxiv_summaries.xlsx |

### [OpenAI] - 要約設定

| 項目 | 説明 | デフォルト |
|------|------|----------|
| use_openai | 要約機能の有効/無効 | false |

## 出力結果

### Excelファイル
- **シート名:** 日付ごと（例: `2024-01-01`）
- **列:** 投稿日、タイトル、arXiv ID、PDF URL、ファイル名、要約

### PDFファイル
- **保存場所:** 日付フォルダ（例: `20240101/`）
- **ファイル名:** arXiv ID（例: `2401.12345.pdf`）

### ログファイル
- **ファイル名:** `arxiv_process.log`

## 実行例

### 例1: 1日だけ処理
```ini
[DateRange]
start_date = 2024/01/15
end_date = 2024/01/15
today_only = false
```

### 例2: 今日の論文のみ取得
```ini
[DateRange]
today_only = true
```

### 例3: 要約機能を有効化
```ini
[OpenAI]
use_openai = true
```

## トラブルシューティング

### エラー: "設定ファイルが見つかりません"
`config.ini.template` をコピーして `config.ini` を作成してください。

### エラー: "start_dateがend_dateより後の日付になっています"
`config.ini` の日付を確認してください。

### エラー: "Excelファイルが開かれています"
出力先のExcelファイルを閉じてから再実行してください。

### 警告: "既に調査済みです"
その日付は既に処理済みです。再処理したい場合は、Excelファイルの該当シートを削除してください。

### 要約が「要約未実施」と表示される
`config.ini` で `use_openai = true` に設定し、環境変数を設定してください。

## 注意事項

1. **arXiv APIのレート制限**
   - 短時間に大量のリクエストを送ると制限される可能性があります
   - `max_results` は100〜500程度を推奨

2. **日付範囲**
   - 長期間を指定すると処理に時間がかかります
   - 必要に応じて期間を分割して実行してください

3. **APIキーの管理**
   - APIキーは絶対にGitHubなどに公開しないでください
   - `.env` ファイルは `.gitignore` に含まれています

## ライセンス

MITライセンス

## 利用用途

本スクリプトは**研究・教育目的**での利用を想定しています。

- 学術研究における論文調査・文献レビューの効率化
- 教育機関での最新研究動向の把握
- 個人学習における論文収集・整理

商用利用の際は、arXiv の利用規約および各論文の著作権にご注意ください。

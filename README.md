# arXiv Paper Fetcher & Summarizer

> 🇯🇵 [Japanese README (docs/README_ja.md)](./docs/README_ja.md)

A CLI tool that searches and downloads papers from arXiv for a specified date range using the arXiv API, and saves the results to an Excel file.
Optionally generates summaries via the Azure OpenAI API.

## Features

- Search arXiv papers by keyword and date range
- Automatically download PDFs into date-based folders
- Export results to Excel with hyperlinks
- Optional AI-powered paper summarization (Azure OpenAI)

## File Structure

```
arxiv_cli/
├── arxiv_cli.py          # Main script
├── config.ini            # Configuration file (edit before running)
├── config.ini.template   # Configuration template
├── verify_config.py      # Configuration verifier
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable sample
├── README.md             # This file (English)
└── docs/README_ja.md     # Japanese README
```

## Requirements

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install openai==0.28.1 feedparser PyMuPDF requests pandas openpyxl
```

## Quick Start

1. Copy `config.ini.template` to `config.ini`
2. Edit `config.ini` to set your search criteria
3. Run `python arxiv_cli.py`

## Configuration (config.ini)

### Basic Settings

```ini
[DateRange]
start_date = 2024/01/01    # Start date (YYYY/MM/DD)
end_date = 2024/01/31      # End date (YYYY/MM/DD)
today_only = false          # true: fetch today's papers only

[Search]
query = all:"machine learning"  # Search query
max_results = 100                # Max results

[Files]
excel_file = arxiv_summaries.xlsx  # Output file

[OpenAI]
use_openai = false  # AI summarization (true/false)
```

### OpenAI Summarization

Set `use_openai = true` to enable automatic paper summarization via Azure OpenAI API.

**Default: false (disabled)**

Set the following environment variables to use the summarization feature:

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

## Usage

### 1. Prepare Configuration

```bash
cp config.ini.template config.ini
```

### 2. Edit Configuration

Open `config.ini` and edit the search parameters.

### 3. Verify Configuration (Optional)

```bash
python verify_config.py
```

### 4. Run

```bash
python arxiv_cli.py
```

## Configuration Reference

### [DateRange] – Date Range

| Key | Description | Format | Example |
|------|-------------|--------|---------|
| `start_date` | Start date | YYYY/MM/DD | 2024/01/01 |
| `end_date` | End date | YYYY/MM/DD | 2024/01/31 |
| `today_only` | Today-only mode | true/false | false |

### [Search] – Search Settings

| Key | Description | Example |
|------|-------------|---------|
| `query` | arXiv search query | `all:"machine learning"` |
| `max_results` | Max number of results | 100 |

**Query Examples:**

- `all:"machine learning"` – Search all fields
- `ti:"neural network"` – Title only
- `au:"Smith"` – Author name
- `all:"ML" OR all:"AI"` – OR search
- `all:"ML" AND all:"AI"` – AND search

### [Files] – File Settings

| Key | Description | Example |
|------|-------------|---------|
| `excel_file` | Excel output filename | `arxiv_summaries.xlsx` |

### [OpenAI] – Summarization Settings

| Key | Description | Default |
|------|-------------|---------|
| `use_openai` | Enable/disable summarization | `false` |

## Output

### Excel File

- **Sheet name:** One per date (e.g., `2024-01-01`)
- **Columns:** Posted Date, Title, arXiv ID, PDF URL, Filename, Summary

### PDF Files

- **Location:** Date folders (e.g., `20240101/`)
- **Filename:** arXiv ID (e.g., `2401.12345.pdf`)

### Log File

- **Filename:** `arxiv_process.log`

## Examples

### Process a single day

```ini
[DateRange]
start_date = 2024/01/15
end_date = 2024/01/15
today_only = false
```

### Fetch today's papers only

```ini
[DateRange]
today_only = true
```

### Enable summarization

```ini
[OpenAI]
use_openai = true
```

## Troubleshooting

| Error / Warning | Solution |
|-----------------|----------|
| Configuration file not found | Copy `config.ini.template` to `config.ini` |
| start_date is later than end_date | Check the dates in `config.ini` |
| Excel file is open | Close the Excel file and retry |
| Already processed | Delete the corresponding sheet in the Excel file to reprocess |
| Summary not performed | Set `use_openai = true` and configure env vars |

## Notes

1. **arXiv API Rate Limits** – Avoid sending too many requests in a short period. `max_results` of 100–500 is recommended.
2. **Date Range** – Long ranges take more time. Split into smaller chunks if needed.
3. **API Key Security** – Never commit API keys to GitHub. The `.env` file is in `.gitignore`.

## License

MIT License

## Intended Use

This script is designed for **research and educational purposes**:

- Streamlining literature reviews in academic research
- Tracking latest research trends in educational institutions
- Collecting and organizing papers for personal study

For commercial use, please refer to the arXiv terms of service and individual paper copyrights.

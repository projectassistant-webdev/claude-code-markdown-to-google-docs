# 📄 MD-to-Drive

> Automatically sync your Markdown and CSV files to Google Drive (Docs & Sheets)

Convert local `.md` files to Google Docs and `.csv` files to Google Sheets with one command. Perfect for documentation workflows, technical writing, and collaborative editing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## ✨ Features

- 📄 **Markdown → Google Docs**: Converts `.md` files to editable Google Docs
- 📊 **CSV → Google Sheets**: Uploads CSV files as Google Sheets
- 🗂️ **Preserves Structure**: Creates matching folder hierarchy in Google Drive
- 🔄 **Smart Updates**: Updates existing files instead of creating duplicates
- ☁️ **Shared Drive Support**: Works with Google Workspace Shared Drives
- ⚡ **Multiple Triggers**: CLI, Git hooks, or programmatic API
- 🔒 **Secure**: Uses service account authentication (no OAuth prompts)
- 🎯 **Selective Sync**: Sync specific files or entire directories
- 🐳 **Docker Ready**: Included Dockerfile for containerized workflows

---

## 🚀 Quick Start

### Installation

```bash
pip install md-to-drive
```

Or install from source:

```bash
git clone https://github.com/YOUR_USERNAME/md-to-drive.git
cd md-to-drive
pip install -e .
```

### Setup

1. **Create Google Cloud credentials** (see [Setup Guide](#setup-guide))
2. **Download `credentials.json`** to your project
3. **Run the sync**:

```bash
md-to-drive sync docs/
```

That's it! Your markdown files are now Google Docs.

---

## 📖 Usage

### Basic CLI

```bash
# Sync entire directory
md-to-drive sync docs/

# Sync specific file
md-to-drive sync README.md

# Sync to specific Google Drive folder
md-to-drive sync docs/ --folder-id "abc123xyz"

# Watch for changes and auto-sync
md-to-drive watch docs/

# Export Google Docs back to Markdown
md-to-drive export --folder-id "abc123xyz" --output ./downloaded/
```

### Git Hook Integration

Add to `.git/hooks/post-commit`:

```bash
#!/bin/bash
md-to-drive sync docs/ --quiet
```

### Python API

```python
from md_to_drive import GoogleDriveSync

sync = GoogleDriveSync(credentials_file='credentials.json')

# Sync markdown to Google Docs
doc_id = sync.markdown_to_doc('README.md', folder_id='abc123')

# Sync CSV to Google Sheets
sheet_id = sync.csv_to_sheet('data.csv', folder_id='abc123')

# Export Google Doc to Markdown
sync.doc_to_markdown(doc_id, output_path='exported.md')
```

### Configuration File

Create `.md-to-drive.yml`:

```yaml
credentials: credentials.json
drive_folder_id: "your-folder-id-here"

sync:
  - path: docs/
    exclude:
      - "*.draft.md"
      - "temp/"

  - path: README.md
    name: "Project README"

watch:
  enabled: true
  interval: 60  # seconds
```

Then simply run:

```bash
md-to-drive sync
```

---

## 🛠️ Setup Guide

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Drive API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in details:
   - **Name**: `md-to-drive-sync`
   - **Description**: `Markdown to Google Drive sync`
4. Click "Create and Continue"
5. Skip optional role assignment
6. Click "Done"

### 3. Generate Credentials

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose **JSON** format
5. Download the file
6. Rename to `credentials.json`
7. Place in your project directory

### 4. Share Google Drive Folder

1. Create a folder in Google Drive for your docs
2. Share with the service account email (from `credentials.json`)
3. Give "Editor" permissions
4. Copy folder ID from URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`

### 5. Test the Setup

```bash
md-to-drive sync README.md --folder-id "YOUR_FOLDER_ID"
```

Check your Google Drive - you should see the converted document!

---

## 📂 Project Structure

```
md-to-drive/
├── src/
│   └── md_to_drive/
│       ├── __init__.py
│       ├── cli.py           # Command-line interface
│       ├── sync.py          # Core sync logic
│       ├── converter.py     # Markdown/CSV conversion
│       └── auth.py          # Google authentication
├── examples/
│   ├── git-hook.sh          # Git hook example
│   ├── config.yml           # Configuration example
│   └── workflow.yml         # GitHub Action example
├── docs/
│   ├── setup.md             # Detailed setup guide
│   ├── api.md               # Python API documentation
│   └── troubleshooting.md   # Common issues
├── tests/
│   └── test_sync.py
├── .github/
│   └── workflows/
│       └── test.yml
├── setup.py
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🎯 Use Cases

### Documentation Workflow

Write docs in Markdown locally (with version control), automatically sync to Google Docs for stakeholder review:

```bash
# Write docs
vim docs/architecture.md

# Commit
git add docs/
git commit -m "Update architecture docs"

# Git hook auto-syncs to Google Drive
# Stakeholders can comment in Google Docs
# Pull comments back to Markdown
```

### Collaborative Writing

- Write technical content in Markdown
- Non-technical team members edit in Google Docs
- Sync changes bidirectionally

### Data Reporting

- Generate CSV reports locally
- Auto-upload to Google Sheets for visualization
- Share with team via Google Drive

---

## 🔒 Security

- `credentials.json` contains sensitive keys - **never commit it**
- Add to `.gitignore`:
  ```
  credentials.json
  .md-to-drive.yml
  ```
- Use environment variables for CI/CD:
  ```bash
  export MD_TO_DRIVE_CREDENTIALS=$(cat credentials.json | base64)
  ```

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/md-to-drive.git
cd md-to-drive
pip install -e ".[dev]"
pytest
```

### Roadmap

- [ ] Bidirectional sync (Google Docs → Markdown)
- [ ] Watch mode for auto-sync
- [ ] GitHub Action for automated workflows
- [ ] Support for Google Slides (Markdown → Slides)
- [ ] Conflict resolution for bidirectional sync
- [ ] Web UI for configuration

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Google Drive API](https://developers.google.com/drive)
- Inspired by various docs-as-code workflows

---

## 💬 Support

- 📖 [Documentation](https://github.com/YOUR_USERNAME/md-to-drive/wiki)
- 🐛 [Issue Tracker](https://github.com/YOUR_USERNAME/md-to-drive/issues)
- 💡 [Feature Requests](https://github.com/YOUR_USERNAME/md-to-drive/issues/new?labels=enhancement)

---

**Made with ❤️ by [Your Name]**

*Star ⭐ this repo if you find it useful!*

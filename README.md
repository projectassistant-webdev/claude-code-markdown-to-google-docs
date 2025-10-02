# 📄 MD-to-Drive for Claude Code

> Automatically sync your Markdown and CSV files to Google Drive while coding with Claude

A Claude Code integration that converts local `.md` files to Google Docs and `.csv` files to Google Sheets with a simple slash command. Perfect for keeping documentation in sync, enabling stakeholder collaboration, and maintaining docs-as-code workflows.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Integration-5436DA.svg)](https://claude.ai/code)

---

## ✨ Why MD-to-Drive?

**Write in Markdown. Share in Google Docs. Keep everything in sync.**

- 📝 **Local-first editing** - Write docs in your favorite editor with version control
- 🔄 **One-command sync** - `/sync-docs` and your team has the latest in Google Drive
- 👥 **Stakeholder-friendly** - Non-technical reviewers use familiar Google Docs
- 🚫 **No duplicates** - Smart updates prevent duplicate files on every sync
- ☁️ **Shared Drive ready** - Works with Google Workspace team drives
- 🐳 **Docker-based** - No local Python installation required

---

## 🚀 Quick Start

### 1. Installation

Install directly from your project:

```bash
# Clone into your project's tools directory
git clone https://github.com/projectassistant-webdev/md-to-drive.git tools/md-to-drive

# Or add as a git submodule
git submodule add https://github.com/projectassistant-webdev/md-to-drive.git tools/md-to-drive
```

### 2. Setup Google Credentials

Create a Google Cloud service account and download credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project → Enable Google Drive API
3. Create Service Account → Download JSON key
4. Save as `tools/md-to-drive/credentials.json`
5. Share your Google Drive folder with the service account email

[📖 Detailed Setup Guide](#setup-guide)

### 3. Configure

Copy the example environment file:

```bash
cp tools/md-to-drive/.env.example tools/md-to-drive/.env
```

Edit `.env` with your settings:

```bash
# Google Drive folder ID from URL: https://drive.google.com/drive/folders/{FOLDER_ID}
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here

# Paths to sync (comma-separated)
SYNC_PATHS=docs,README.md

# Subfolder structure
SYNC_SUBFOLDERS=guides,api,tutorials
```

### 4. Sync Your Docs! 🎉

#### Using Claude Code Slash Command

In Claude Code, simply run:

```bash
/sync-docs
```

That's it! Your documentation is now synced to Google Drive.

#### Manual Docker Sync

```bash
cd tools/md-to-drive
docker compose up
```

---

## 🎯 Claude Code Integration

### Slash Commands

This tool includes a custom Claude Code slash command for seamless workflow integration.

#### `/sync-docs`

Syncs all configured documentation to Google Drive.

**Location:** `.claude/commands/sync-docs.js`

**What it does:**
1. Checks for `tools/md-to-drive` directory
2. Runs Docker Compose sync
3. Shows real-time progress
4. Reports success/failure

**Example Output:**

```
📤 Syncing documentation to Google Drive...

🔄 Starting Google Drive sync...

📁 Found existing folder: Guides
📁 Found existing folder: API
📁 Found existing folder: Tutorials

📄 Syncing configured paths...
🔄 Updated: docs/guides/quickstart.md → Google Doc
🔄 Updated: docs/api/endpoints.md → Google Doc
✅ Created: docs/tutorials/setup.md → Google Doc

📊 Syncing CSV files...
🔄 Updated: data/metrics.csv → Google Sheet

✨ Sync complete!
```

### Custom Commands

Add this to your project's `.claude/commands/` directory:

```javascript
#!/usr/bin/env node
// .claude/commands/sync-docs.js

const { execSync } = require('child_process');
const path = require('path');

async function main() {
  console.log('📤 Syncing documentation to Google Drive...\n');

  const syncDir = path.join(process.cwd(), 'tools/md-to-drive');

  try {
    execSync('docker compose up', {
      cwd: syncDir,
      stdio: 'inherit'
    });
    console.log('\n✨ Sync complete!');
  } catch (error) {
    console.error('❌ Error during sync:', error.message);
    process.exit(1);
  }
}

main();
```

---

## ✨ Features

### Smart Updates
- 🔄 **Updates existing files** instead of creating duplicates
- 📁 **Reuses folders** across multiple syncs
- 🎯 **Idempotent** - safe to run multiple times

### File Support
- 📄 **Markdown → Google Docs** - Full formatting preservation
- 📊 **CSV → Google Sheets** - Ready for charts and collaboration
- 🗂️ **Folder Structure** - Mirrors your local organization

### Google Drive Integration
- ☁️ **Shared Drive support** - Works with Google Workspace team drives
- 🔒 **Service Account auth** - No OAuth prompts or token expiry
- 🌐 **Direct links** - Get shareable URLs for all synced files

### Developer Experience
- 🐳 **Docker-based** - No Python installation needed
- ⚙️ **Configurable** - Customize paths and folder structure via `.env`
- 📝 **Visual feedback** - Clear indicators for created vs updated files
- 🚀 **Fast** - Direct conversion, no temp files

---

## 📖 Usage Examples

### Sync Entire Docs Folder

```bash
# .env configuration
SYNC_PATHS=docs
SYNC_SUBFOLDERS=guides,api,reference,tutorials

# Run sync
/sync-docs
```

### Sync Multiple Directories

```bash
# .env configuration
SYNC_PATHS=docs,wiki,notes,README.md
SYNC_SUBFOLDERS=

# Run sync
/sync-docs
```

### Custom Folder Structure

```bash
# .env configuration
SYNC_PATHS=documentation
SYNC_SUBFOLDERS=getting-started,advanced,troubleshooting

# Run sync
/sync-docs
```

---

## 🛠️ Configuration

### Environment Variables

Create `tools/md-to-drive/.env`:

```bash
# Required: Google Drive folder ID
GOOGLE_DRIVE_FOLDER_ID=0AN3XxYXJHzK5Uk9PVA

# Optional: Paths to sync (default: docs,README.md)
SYNC_PATHS=docs,README.md

# Optional: Subfolder structure (default: inventory,setup,analysis)
SYNC_SUBFOLDERS=guides,api,tutorials
```

### Docker Compose

The included `docker-compose.yml` handles all dependencies:

```yaml
version: '3.8'

services:
  sync:
    build: .
    container_name: docs_sync
    volumes:
      - ../../docs:/app/docs:ro
      - ../../README.md:/app/README.md:ro
      - ./credentials.json:/app/credentials.json:ro
    env_file:
      - .env
```

### File Structure

```
your-project/
├── .claude/
│   └── commands/
│       └── sync-docs.js          # Slash command
├── tools/
│   └── md-to-drive/
│       ├── sync_to_google.py     # Main sync script
│       ├── docker-compose.yml    # Docker config
│       ├── Dockerfile            # Python container
│       ├── credentials.json      # Service account (gitignored)
│       ├── .env                  # Configuration (gitignored)
│       └── .env.example          # Template
└── docs/
    ├── guides/
    ├── api/
    └── tutorials/
```

---

## 🔒 Security

### Credentials Management

**Never commit sensitive files:**

```gitignore
# .gitignore
tools/md-to-drive/credentials.json
tools/md-to-drive/.env
```

The included `.gitignore` handles this automatically.

### Service Account Permissions

Your service account needs:
- **Google Drive API** enabled
- **Editor** access to target folder
- No broader permissions required

### Best Practices

✅ Use service accounts (not OAuth)
✅ Share specific folders only
✅ Keep credentials in gitignored files
✅ Use environment variables in CI/CD
✅ Rotate credentials periodically

---

## 📋 Setup Guide

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Name it (e.g., "md-to-drive-sync")
4. Click "Create"

### Step 2: Enable Google Drive API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click "Enable"

### Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - **Name**: `md-to-drive-sync`
   - **Description**: `Sync documentation to Google Drive`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue" → "Done")

### Step 4: Generate JSON Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose **JSON** format
5. Download the file
6. Save as `tools/md-to-drive/credentials.json`

### Step 5: Share Google Drive Folder

#### Option A: Regular Google Drive Folder

1. Create a folder in Google Drive
2. Right-click → "Share"
3. Add the service account email (from `credentials.json`)
4. Give "Editor" permissions
5. Copy folder ID from URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`

#### Option B: Google Workspace Shared Drive (Recommended)

1. Create a Shared Drive in Google Drive
2. Add the service account email as a member
3. Give "Content Manager" or "Manager" role
4. Copy the Shared Drive ID from the URL

### Step 6: Configure Environment

```bash
cp tools/md-to-drive/.env.example tools/md-to-drive/.env
```

Edit `.env`:
```bash
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
SYNC_PATHS=docs,README.md
SYNC_SUBFOLDERS=guides,api,tutorials
```

### Step 7: Test the Setup

In Claude Code:
```bash
/sync-docs
```

Or manually:
```bash
cd tools/md-to-drive
docker compose up
```

Check your Google Drive - you should see your converted documents!

---

## 🎨 Use Cases

### 📚 Documentation Workflow

**Local**: Write technical docs in Markdown with version control
**Sync**: `/sync-docs` after major updates
**Review**: Stakeholders comment in Google Docs
**Update**: Incorporate feedback locally and re-sync

### 👥 Stakeholder Collaboration

**Problem**: Non-technical stakeholders don't use GitHub
**Solution**: Write in Markdown, share as Google Docs
**Benefit**: Everyone uses their preferred tool

### 📊 Data Sharing

**Local**: Generate CSV reports from scripts
**Sync**: Automatically upload to Google Sheets
**Share**: Team visualizes data with charts

### 🔄 Bidirectional Workflow

1. Developer writes in Markdown (versioned)
2. Syncs to Google Docs with `/sync-docs`
3. Manager reviews and comments in Google Docs
4. Developer incorporates feedback in Markdown
5. Re-sync updates the Google Doc (no duplicates!)

---

## 🐳 Docker Details

### Why Docker?

- ✅ No Python installation required
- ✅ Consistent environment across machines
- ✅ Isolated dependencies
- ✅ Works on any OS

### Included Services

**Container**: Python 3.11-slim
**Dependencies**: Google API client libraries
**Volumes**: Read-only mounts for security
**Network**: None required (outbound only)

### Custom Docker Usage

```bash
# Build the image
cd tools/md-to-drive
docker build -t md-to-drive .

# Run manually
docker run --rm \
  -v $(pwd)/../../docs:/app/docs:ro \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  --env-file .env \
  md-to-drive
```

---

## 🔧 Troubleshooting

### Files Not Syncing

**Check:**
- ✅ `SYNC_PATHS` points to existing directories
- ✅ Files exist in those directories
- ✅ File extensions are `.md` or `.csv`

### Permission Denied Errors

**Check:**
- ✅ Folder shared with service account email
- ✅ Service account has "Editor" or "Content Manager" role
- ✅ `credentials.json` is valid and not expired

### Duplicates Still Created

**Check:**
- ✅ Using latest version (has smart update logic)
- ✅ File names haven't changed
- ✅ Files are in the same folder structure

### Docker Issues

**Check:**
- ✅ Docker is running: `docker ps`
- ✅ Credentials file exists: `ls tools/md-to-drive/credentials.json`
- ✅ .env file exists: `ls tools/md-to-drive/.env`

### Shared Drive Not Working

**Ensure:**
- ✅ Using a Shared Drive (Team Drive), not regular folder
- ✅ Service account is added as a member
- ✅ Using the Shared Drive ID (starts with `0`)

---

## 🤝 Contributing

Contributions welcome! This project is maintained for the Claude Code community.

### Development Setup

```bash
git clone https://github.com/projectassistant-webdev/md-to-drive.git
cd md-to-drive
pip install -e ".[dev]"
pytest
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- **Built for**: [Claude Code](https://claude.ai/code) users
- **Powered by**: [Google Drive API](https://developers.google.com/drive)
- **Inspired by**: Docs-as-code workflows

---

## 💬 Support

- 📖 [Documentation](https://github.com/projectassistant-webdev/md-to-drive/wiki)
- 🐛 [Issue Tracker](https://github.com/projectassistant-webdev/md-to-drive/issues)
- 💡 [Feature Requests](https://github.com/projectassistant-webdev/md-to-drive/issues/new?labels=enhancement)

---

**Made with ❤️ for the Claude Code community**

*Star ⭐ this repo if you find it useful!*

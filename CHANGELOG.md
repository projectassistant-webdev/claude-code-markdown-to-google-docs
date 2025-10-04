# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Code Formatting for Google Docs**: Code blocks now display with visual `═══ CODE (LANGUAGE) ═══` headers and indentation for better readability
- **Inline Code Markers**: Inline code wrapped with `⟨ ⟩` angle brackets for visibility in Google Docs
- **Smart Caching System**: MD5 hash-based caching to skip unchanged files (20-30x faster on subsequent syncs!)
- **Code File Support**: Added support for .php, .py, .js, .ts, .tsx, .jsx, .json, .yml, .yaml files
- **Named Docker Volume**: Cross-platform cache persistence using Docker-managed volumes (works on Windows, Mac, Linux)
- **Cache Statistics**: Track synced vs skipped files with detailed reporting (e.g., "Synced: 2 files, Skipped: 39 files")
- **SyncCache class**: New caching module with MD5 hashing, cache persistence, and change detection
- **Update instead of duplicate**: Files and folders are now updated if they already exist, preventing duplicates
- `get_or_create_folder()` method that checks for existing folders before creating new ones
- Support for Google Workspace Shared Drives with `supportsAllDrives=True` parameter
- Visual feedback showing whether files were created (✅ Created) or updated (🔄 Updated)
- Better folder reuse across multiple sync runs

### Changed
- Markdown converter now preprocesses content before upload for better code display in Google Docs
- Sync system reports detailed sync/skip statistics at end of each run
- Docker compose includes persistent cache volume configuration
- `markdown_to_doc()` now updates existing Google Docs instead of creating duplicates
- `csv_to_sheet()` now updates existing Google Sheets instead of creating duplicates
- `create_folder()` is now a wrapper around `get_or_create_folder()` for backward compatibility
- Simplified markdown conversion: direct upload with mimeType conversion instead of upload-copy-delete workflow
- All Google Drive API calls now include `supportsAllDrives=True` for Shared Drive compatibility

### Performance
- **20-30x faster** on subsequent syncs with unchanged files
- Only modified files are re-uploaded (detected via MD5 hash)
- Cache persists across container restarts using Docker named volumes

### Fixed
- Duplicate files created on subsequent syncs
- Duplicate folders created on subsequent syncs
- Files not syncing to Google Workspace Shared Drives
- Unnecessary temporary file creation during markdown conversion
- Docker permission issues across different platforms (Windows, Mac, Linux)
- Temp file cleanup after uploads

## [0.1.0] - 2025-10-02

### Added
- Initial release
- Sync markdown files to Google Docs
- Sync CSV files to Google Sheets
- CLI interface with `sync`, `test`, and `setup` commands
- Docker support
- Service account authentication
- Recursive directory syncing
- Pattern-based file exclusion

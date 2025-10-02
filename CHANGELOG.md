# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Update instead of duplicate**: Files and folders are now updated if they already exist, preventing duplicates
- `get_or_create_folder()` method that checks for existing folders before creating new ones
- Support for Google Workspace Shared Drives with `supportsAllDrives=True` parameter
- Visual feedback showing whether files were created (✅ Created) or updated (🔄 Updated)
- Better folder reuse across multiple sync runs

### Changed
- `markdown_to_doc()` now updates existing Google Docs instead of creating duplicates
- `csv_to_sheet()` now updates existing Google Sheets instead of creating duplicates
- `create_folder()` is now a wrapper around `get_or_create_folder()` for backward compatibility
- Simplified markdown conversion: direct upload with mimeType conversion instead of upload-copy-delete workflow
- All Google Drive API calls now include `supportsAllDrives=True` for Shared Drive compatibility

### Fixed
- Duplicate files created on subsequent syncs
- Duplicate folders created on subsequent syncs
- Files not syncing to Google Workspace Shared Drives
- Unnecessary temporary file creation during markdown conversion

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

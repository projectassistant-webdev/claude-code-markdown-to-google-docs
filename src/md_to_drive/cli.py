"""
Command-line interface for MD-to-Drive
"""

import click
import sys
from pathlib import Path
from typing import Optional

from . import GoogleDriveSync
from .__init__ import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """MD-to-Drive: Sync Markdown and CSV files to Google Drive"""
    pass


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--credentials', '-c', default='credentials.json',
              help='Path to Google service account credentials JSON')
@click.option('--folder-id', '-f', envvar='GOOGLE_DRIVE_FOLDER_ID',
              help='Google Drive folder ID to sync to')
@click.option('--recursive/--no-recursive', '-r', default=True,
              help='Recursively sync subdirectories')
@click.option('--exclude', '-e', multiple=True,
              help='Patterns to exclude (can be used multiple times)')
@click.option('--quiet', '-q', is_flag=True,
              help='Suppress output')
def sync(path, credentials, folder_id, recursive, exclude, quiet):
    """
    Sync files or directories to Google Drive

    Examples:

        md-to-drive sync docs/

        md-to-drive sync README.md --folder-id abc123

        md-to-drive sync docs/ --exclude "*.draft.md" --exclude "temp/"
    """
    if not quiet:
        click.echo(f"🔄 Starting sync from: {path}\n")

    try:
        syncer = GoogleDriveSync(credentials_file=credentials, folder_id=folder_id)

        path_obj = Path(path)

        if path_obj.is_file():
            # Sync single file
            file_id = syncer.sync_file(path_obj, folder_id)
            if file_id and not quiet:
                click.echo(f"\n✨ Sync complete! File ID: {file_id}")

        elif path_obj.is_dir():
            # Sync directory
            synced = syncer.sync_directory(
                path_obj,
                recursive=recursive,
                exclude=list(exclude) if exclude else None
            )

            if not quiet:
                click.echo(f"\n✨ Sync complete!")
                click.echo(f"   Files synced: {len(synced)}")

        return 0

    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("\nRun 'md-to-drive setup' for configuration help", err=True)
        return 1

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        return 1


@main.command()
@click.option('--credentials', '-c', default='credentials.json',
              help='Path to credentials file to test')
def test(credentials):
    """
    Test Google Drive API connection

    Verifies that credentials are valid and API access works.
    """
    click.echo("🔍 Testing Google Drive connection...\n")

    try:
        syncer = GoogleDriveSync(credentials_file=credentials)
        syncer.auth.test_connection()

        click.echo("✅ Connection successful!")
        click.echo(f"   Credentials: {credentials}")
        click.echo("   API: Google Drive v3")
        return 0

    except FileNotFoundError as e:
        click.echo(f"❌ {e}", err=True)
        return 1

    except Exception as e:
        click.echo(f"❌ Connection failed: {e}", err=True)
        return 1


@main.command()
def setup():
    """
    Display setup instructions

    Shows step-by-step guide for creating Google Cloud credentials.
    """
    instructions = """
📖 MD-to-Drive Setup Guide
═══════════════════════════════════════════════════════════════

Step 1: Create Google Cloud Project
────────────────────────────────────
1. Go to https://console.cloud.google.com
2. Click "Select a project" → "New Project"
3. Name it (e.g., "md-to-drive-sync")
4. Click "Create"

Step 2: Enable Google Drive API
────────────────────────────────
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it, then click "Enable"

Step 3: Create Service Account
───────────────────────────────
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - Name: md-to-drive-sync
   - Description: Sync markdown to Google Drive
4. Click "Create and Continue"
5. Skip optional steps (click "Continue" → "Done")

Step 4: Generate JSON Key
──────────────────────────
1. Click on the service account you created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose JSON format
5. Click "Create"
6. Save the downloaded file as 'credentials.json'

Step 5: Share Google Drive Folder (Optional)
─────────────────────────────────────────────
1. Create a folder in Google Drive
2. Right-click → "Share"
3. Add service account email (from credentials.json)
4. Give "Editor" permissions
5. Copy folder ID from URL:
   https://drive.google.com/drive/folders/[FOLDER_ID]

Step 6: Test Connection
────────────────────────
Run: md-to-drive test

Step 7: Sync Your Files!
─────────────────────────
Run: md-to-drive sync docs/ --folder-id YOUR_FOLDER_ID

═══════════════════════════════════════════════════════════════

For more help, visit:
https://github.com/YOUR_USERNAME/md-to-drive#setup-guide
"""
    click.echo(instructions)
    return 0


@main.command()
@click.argument('folder_id')
@click.option('--output', '-o', type=click.Path(), default='./exported',
              help='Output directory for exported files')
@click.option('--credentials', '-c', default='credentials.json',
              help='Path to Google service account credentials JSON')
def export(folder_id, output, credentials):
    """
    Export Google Docs back to Markdown (Future feature)

    Args:
        folder_id: Google Drive folder ID to export from
    """
    click.echo("⚠️  Export functionality coming soon!")
    click.echo("\nPlanned features:")
    click.echo("  • Export Google Docs → Markdown")
    click.echo("  • Export Google Sheets → CSV")
    click.echo("  • Bidirectional sync with conflict resolution")
    click.echo("\nStar the repo to follow development!")
    return 0


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--credentials', '-c', default='credentials.json',
              help='Path to Google service account credentials JSON')
@click.option('--folder-id', '-f', envvar='GOOGLE_DRIVE_FOLDER_ID',
              help='Google Drive folder ID to sync to')
@click.option('--interval', '-i', default=60, type=int,
              help='Check interval in seconds (default: 60)')
def watch(path, credentials, folder_id, interval):
    """
    Watch directory for changes and auto-sync (Future feature)

    Args:
        path: Directory to watch
    """
    click.echo("⚠️  Watch mode coming soon!")
    click.echo(f"\nPlanned: Auto-sync {path} every {interval}s")
    click.echo("\nFor now, use a cron job or git hook:")
    click.echo("  */5 * * * * cd /path/to/project && md-to-drive sync docs/")
    return 0


if __name__ == '__main__':
    sys.exit(main())

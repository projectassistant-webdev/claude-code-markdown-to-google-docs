"""
Core synchronization logic for MD-to-Drive
"""

import os
from pathlib import Path
from typing import Optional, List, Dict
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from .auth import GoogleAuthenticator
from .converter import FileTypeDetector, MarkdownConverter, CSVConverter


class GoogleDriveSync:
    """Main sync class for uploading files to Google Drive"""

    def __init__(self, credentials_file='credentials.json', folder_id: Optional[str] = None):
        """
        Initialize Google Drive sync

        Args:
            credentials_file: Path to service account JSON
            folder_id: Optional Google Drive folder ID to sync to
        """
        self.auth = GoogleAuthenticator(credentials_file)
        self.service = self.auth.authenticate()
        self.folder_id = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')

    def get_or_create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Get existing folder or create if it doesn't exist

        Args:
            name: Folder name
            parent_id: Parent folder ID (None for root)

        Returns:
            Folder ID
        """
        parent_id = parent_id or 'root'

        try:
            # Search for existing folder
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            files = results.get('files', [])

            if files:
                print(f"📁 Found existing folder: {name}")
                return files[0]['id']

            # Create new folder if it doesn't exist
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_id:
                folder_metadata['parents'] = [parent_id]

            folder = self.service.files().create(
                body=folder_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            print(f"📁 Created folder: {name}")
            return folder['id']

        except HttpError as error:
            raise Exception(f"Error with folder '{name}': {error}")

    def create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Create folder in Google Drive (legacy method, use get_or_create_folder)

        Args:
            name: Folder name
            parent_id: Parent folder ID (None for root)

        Returns:
            Created folder ID
        """
        return self.get_or_create_folder(name, parent_id)

    def create_folder_structure(self, base_path: Path, parent_id: Optional[str] = None) -> Dict[str, str]:
        """
        Create folder structure matching local directory

        Args:
            base_path: Local directory path
            parent_id: Parent Google Drive folder ID

        Returns:
            Dictionary mapping local paths to Google Drive folder IDs
        """
        folders = {}
        parent_id = parent_id or self.folder_id or 'root'

        # Create main folder
        main_folder_name = base_path.name
        main_folder_id = self.create_folder(main_folder_name, parent_id)
        folders[str(base_path)] = main_folder_id

        # Create subdirectories
        for subdir in base_path.rglob('*'):
            if subdir.is_dir():
                relative_path = subdir.relative_to(base_path.parent)
                parent_path = subdir.parent

                if str(parent_path) in folders:
                    parent_folder_id = folders[str(parent_path)]
                else:
                    parent_folder_id = main_folder_id

                folder_id = self.create_folder(subdir.name, parent_folder_id)
                folders[str(subdir)] = folder_id

        return folders

    def markdown_to_doc(self, md_file: Path, folder_id: Optional[str] = None, custom_name: Optional[str] = None) -> str:
        """
        Convert and upload markdown file to Google Docs (update if exists)

        Args:
            md_file: Path to markdown file
            folder_id: Target Google Drive folder ID
            custom_name: Optional custom name for the document

        Returns:
            Google Doc ID
        """
        md_file = Path(md_file)
        folder_id = folder_id or self.folder_id or 'root'

        converter = MarkdownConverter()
        file_metadata = converter.prepare_for_upload(md_file)

        if custom_name:
            file_metadata['name'] = custom_name

        file_name = file_metadata['name']

        try:
            # Check if file already exists
            query = f"name='{file_name}' and mimeType='application/vnd.google-apps.document' and '{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            files = results.get('files', [])
            media = MediaFileUpload(str(md_file), mimetype='text/markdown', resumable=True)

            if files:
                # Update existing file
                doc = self.service.files().update(
                    fileId=files[0]['id'],
                    media_body=media,
                    supportsAllDrives=True
                ).execute()
                print(f"🔄 Updated: {md_file} → Google Doc (ID: {doc['id']})")
            else:
                # Create new file - direct upload with conversion
                file_metadata['mimeType'] = 'application/vnd.google-apps.document'
                file_metadata['parents'] = [folder_id]

                doc = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                print(f"✅ Created: {md_file} → Google Doc (ID: {doc['id']})")

            return doc['id']

        except HttpError as error:
            raise Exception(f"Error syncing {md_file}: {error}")

    def csv_to_sheet(self, csv_file: Path, folder_id: Optional[str] = None, custom_name: Optional[str] = None) -> str:
        """
        Convert and upload CSV file to Google Sheets (update if exists)

        Args:
            csv_file: Path to CSV file
            folder_id: Target Google Drive folder ID
            custom_name: Optional custom name for the sheet

        Returns:
            Google Sheet ID
        """
        csv_file = Path(csv_file)
        folder_id = folder_id or self.folder_id or 'root'

        converter = CSVConverter()
        file_metadata = converter.prepare_for_upload(csv_file)

        if custom_name:
            file_metadata['name'] = custom_name

        file_name = file_metadata['name']

        try:
            # Check if file already exists
            query = f"name='{file_name}' and mimeType='application/vnd.google-apps.spreadsheet' and '{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, webViewLink)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            files = results.get('files', [])
            media = MediaFileUpload(str(csv_file), mimetype='text/csv', resumable=True)

            if files:
                # Update existing file
                sheet = self.service.files().update(
                    fileId=files[0]['id'],
                    media_body=media,
                    fields='id,webViewLink',
                    supportsAllDrives=True
                ).execute()
                print(f"🔄 Updated: {csv_file} → Google Sheet")
                print(f"   View at: {sheet.get('webViewLink')}")
            else:
                # Create new file
                file_metadata['mimeType'] = converter.get_conversion_mimetype()
                file_metadata['parents'] = [folder_id]

                sheet = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,webViewLink',
                    supportsAllDrives=True
                ).execute()
                print(f"✅ Created: {csv_file} → Google Sheet")
                print(f"   View at: {sheet.get('webViewLink')}")

            return sheet['id']

        except HttpError as error:
            raise Exception(f"Error syncing {csv_file}: {error}")

    def sync_file(self, file_path: Path, folder_id: Optional[str] = None) -> str:
        """
        Auto-detect file type and sync to Google Drive

        Args:
            file_path: Path to file
            folder_id: Target Google Drive folder ID

        Returns:
            Google Drive file ID
        """
        file_path = Path(file_path)

        try:
            converter_class = FileTypeDetector.get_converter(file_path)

            if converter_class == MarkdownConverter:
                return self.markdown_to_doc(file_path, folder_id)
            elif converter_class == CSVConverter:
                return self.csv_to_sheet(file_path, folder_id)

        except ValueError as e:
            print(f"⚠️  Skipped: {file_path} - {e}")
            return None

    def sync_directory(self, directory: Path, recursive: bool = True, exclude: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Sync entire directory to Google Drive

        Args:
            directory: Local directory path
            recursive: Include subdirectories
            exclude: List of patterns to exclude

        Returns:
            Dictionary mapping local files to Google Drive IDs
        """
        directory = Path(directory)
        exclude = exclude or []
        synced_files = {}

        # Create folder structure
        folders = self.create_folder_structure(directory, self.folder_id)

        # Get files to sync
        pattern = '**/*' if recursive else '*'
        files = [f for f in directory.glob(pattern) if f.is_file()]

        # Filter excluded patterns
        for pattern in exclude:
            files = [f for f in files if not f.match(pattern)]

        # Sync each file
        for file_path in files:
            # Determine target folder
            parent_dir = str(file_path.parent)
            target_folder = folders.get(parent_dir, self.folder_id or 'root')

            try:
                file_id = self.sync_file(file_path, target_folder)
                if file_id:
                    synced_files[str(file_path)] = file_id
            except Exception as e:
                print(f"❌ Error syncing {file_path}: {e}")

        return synced_files

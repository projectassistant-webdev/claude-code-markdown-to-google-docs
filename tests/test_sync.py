"""
Basic tests for MD-to-Drive sync functionality
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from md_to_drive import GoogleDriveSync
from md_to_drive.converter import FileTypeDetector, MarkdownConverter, CSVConverter


class TestFileTypeDetector:
    """Test file type detection"""

    def test_markdown_detection(self):
        """Test markdown file detection"""
        md_file = Path("test.md")
        converter = FileTypeDetector.get_converter(md_file)
        assert converter == MarkdownConverter

    def test_csv_detection(self):
        """Test CSV file detection"""
        csv_file = Path("data.csv")
        converter = FileTypeDetector.get_converter(csv_file)
        assert converter == CSVConverter

    def test_unsupported_file(self):
        """Test unsupported file type raises error"""
        txt_file = Path("test.txt")
        with pytest.raises(ValueError, match="Unsupported file type"):
            FileTypeDetector.get_converter(txt_file)


class TestConverters:
    """Test converter classes"""

    def test_markdown_converter_metadata(self):
        """Test markdown metadata preparation"""
        md_file = Path("test.md")
        metadata = MarkdownConverter.prepare_for_upload(md_file)

        assert metadata['name'] == 'test'
        assert metadata['mimeType'] == 'text/markdown'

    def test_csv_converter_metadata(self):
        """Test CSV metadata preparation"""
        csv_file = Path("data.csv")
        metadata = CSVConverter.prepare_for_upload(csv_file)

        assert metadata['name'] == 'data'
        assert metadata['mimeType'] == 'text/csv'

    def test_markdown_conversion_mimetype(self):
        """Test Google Docs MIME type"""
        mimetype = MarkdownConverter.get_conversion_mimetype()
        assert mimetype == 'application/vnd.google-apps.document'

    def test_csv_conversion_mimetype(self):
        """Test Google Sheets MIME type"""
        mimetype = CSVConverter.get_conversion_mimetype()
        assert mimetype == 'application/vnd.google-apps.spreadsheet'


# Integration tests would require actual Google Drive credentials
# These should be run separately in CI/CD with test credentials

@pytest.mark.skip(reason="Requires Google Drive credentials")
class TestGoogleDriveSync:
    """Integration tests for Google Drive sync"""

    def test_authentication(self):
        """Test Google Drive authentication"""
        # Would test with real credentials in CI/CD
        pass

    def test_folder_creation(self):
        """Test creating folders in Google Drive"""
        pass

    def test_markdown_upload(self):
        """Test uploading markdown file"""
        pass

    def test_csv_upload(self):
        """Test uploading CSV file"""
        pass

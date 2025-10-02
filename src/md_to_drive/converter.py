"""
File conversion utilities for Markdown and CSV
"""

from pathlib import Path
from typing import Optional


class MarkdownConverter:
    """Convert Markdown files to Google Docs format"""

    @staticmethod
    def prepare_for_upload(md_file: Path) -> dict:
        """
        Prepare markdown file for upload

        Args:
            md_file: Path to markdown file

        Returns:
            Dictionary with file metadata
        """
        return {
            'name': md_file.stem,
            'mimeType': 'text/markdown',
            'description': f'Converted from {md_file.name}'
        }

    @staticmethod
    def get_conversion_mimetype() -> str:
        """Get Google Docs MIME type for conversion"""
        return 'application/vnd.google-apps.document'


class CSVConverter:
    """Convert CSV files to Google Sheets format"""

    @staticmethod
    def prepare_for_upload(csv_file: Path) -> dict:
        """
        Prepare CSV file for upload

        Args:
            csv_file: Path to CSV file

        Returns:
            Dictionary with file metadata
        """
        return {
            'name': csv_file.stem,
            'mimeType': 'text/csv',
            'description': f'Converted from {csv_file.name}'
        }

    @staticmethod
    def get_conversion_mimetype() -> str:
        """Get Google Sheets MIME type for conversion"""
        return 'application/vnd.google-apps.spreadsheet'


class FileTypeDetector:
    """Detect file types and choose appropriate converter"""

    CONVERTERS = {
        '.md': MarkdownConverter,
        '.markdown': MarkdownConverter,
        '.csv': CSVConverter,
    }

    @classmethod
    def get_converter(cls, file_path: Path):
        """
        Get appropriate converter for file type

        Args:
            file_path: Path to file

        Returns:
            Converter class or None if unsupported

        Raises:
            ValueError: If file type is not supported
        """
        suffix = file_path.suffix.lower()
        converter = cls.CONVERTERS.get(suffix)

        if converter is None:
            raise ValueError(
                f"Unsupported file type: {suffix}\n"
                f"Supported types: {', '.join(cls.CONVERTERS.keys())}"
            )

        return converter

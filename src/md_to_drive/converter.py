"""
File conversion utilities for Markdown and CSV
"""

import re
import tempfile
from pathlib import Path
from typing import Optional


class MarkdownConverter:
    """Convert Markdown files to Google Docs format"""

    @staticmethod
    def preprocess_markdown_for_google_docs(md_content: str) -> str:
        """
        Preprocess markdown to make code blocks more readable in Google Docs.
        Wraps code blocks with visual markers that Google Docs will preserve.

        Args:
            md_content: Raw markdown content

        Returns:
            Processed markdown content with formatted code blocks
        """
        # Process fenced code blocks (```language ... ```)
        def replace_code_block(match):
            language = match.group(1) or ''
            code = match.group(2)

            # Add visual markers around code blocks
            header = f"═══ CODE ({language.upper()}) ═══" if language else "═══ CODE ═══"
            footer = "═" * len(header)

            # Indent code slightly for better visibility
            indented_code = '\n'.join('    ' + line for line in code.split('\n'))

            return f"\n{header}\n{indented_code}\n{footer}\n"

        # Replace fenced code blocks
        md_content = re.sub(
            r'```(\w+)?\n(.*?)```',
            replace_code_block,
            md_content,
            flags=re.DOTALL
        )

        # Process inline code (`code`)
        # Wrap with special markers that are visible in plain text
        md_content = re.sub(
            r'`([^`]+)`',
            r'⟨ \1 ⟩',
            md_content
        )

        return md_content

    @staticmethod
    def prepare_for_upload(md_file: Path, format_code: bool = True) -> dict:
        """
        Prepare markdown file for upload with optional code formatting

        Args:
            md_file: Path to markdown file
            format_code: Whether to apply code formatting (default: True)

        Returns:
            Dictionary with file metadata and preprocessed content path
        """
        if format_code:
            # Read and preprocess markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Preprocess to make code blocks readable
            processed_content = MarkdownConverter.preprocess_markdown_for_google_docs(md_content)

            # Create temporary file with processed content
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
            temp_file.write(processed_content)
            temp_file.close()

            return {
                'name': md_file.stem,
                'mimeType': 'text/markdown',
                'description': f'Converted from {md_file.name}',
                'temp_file': temp_file.name  # Track temp file for cleanup
            }
        else:
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
        # Code files - treat as markdown for formatted display
        '.php': MarkdownConverter,
        '.py': MarkdownConverter,
        '.js': MarkdownConverter,
        '.ts': MarkdownConverter,
        '.tsx': MarkdownConverter,
        '.jsx': MarkdownConverter,
        '.json': MarkdownConverter,
        '.yml': MarkdownConverter,
        '.yaml': MarkdownConverter,
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

"""
HireSignal - Text Extraction Service
Extracts and normalizes text from PDF, DOCX, and raw text files.
Includes robust fallbacks for edge-case encodings and malformed layouts.
"""

import re
import io
from typing import Tuple, Dict, Any


def clean_and_normalize_text(text: str) -> str:
    """Normalize whitespace, standardize unicode bullet characters, and strip zero-width chars."""
    if not text:
        return ""
    # Replace non-standard bullets and dashes
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25CF\u25CB\u25A0]', ' • ', text)
    text = re.sub(r'[\u2013\u2014\u2015]', '-', text)
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201C\u201D]', '"', text)
    text = re.sub(r'[\u00A0\u200B\uFEFF]', ' ', text)
    # Collapse consecutive horizontal whitespace while preserving line breaks
    text = re.sub(r'[ \t]+', ' ', text)
    # Collapse more than two consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Parse PDF into clean text using pypdf with fallback.
    Extracts metadata and flags potential layout issues.
    """
    metadata = {"num_pages": 1, "has_text": False, "method": "pypdf"}
    extracted_chunks = []
    
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        metadata["num_pages"] = len(reader.pages)
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_chunks.append(page_text)
        text = "\n\n".join(extracted_chunks)
        metadata["has_text"] = bool(text.strip())
        return clean_and_normalize_text(text), metadata
    except Exception as e:
        # Fallback raw byte extraction for plain stream text
        try:
            raw_str = file_bytes.decode('utf-8', errors='ignore')
            # Filter readable ASCII/UTF strings
            readable = re.findall(r'[\x20-\x7E\s]{4,}', raw_str)
            text = " ".join(readable)
            metadata["method"] = "fallback_stream"
            return clean_and_normalize_text(text), metadata
        except Exception:
            return "", {"error": str(e), "method": "failed"}


def extract_text_from_docx(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Parse DOCX into clean text using python-docx or zipfile XML parsing.
    """
    metadata = {"method": "docx"}
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        # Also extract table text
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    paragraphs.append(" | ".join(row_text))
        text = "\n".join(paragraphs)
        return clean_and_normalize_text(text), metadata
    except Exception as e:
        import zipfile
        import xml.etree.ElementTree as ET
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            # Find all w:t text nodes
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text_nodes = tree.findall('.//w:t', namespaces)
            text = " ".join(node.text for node in text_nodes if node.text)
            metadata["method"] = "xml_fallback"
            return clean_and_normalize_text(text), metadata
        except Exception:
            return "", {"error": str(e), "method": "failed"}


def parse_resume_content(content: bytes, filename: str) -> Tuple[str, Dict[str, Any]]:
    """Unified entry point for parsing resume files based on extension or signature."""
    lower_name = filename.lower()
    if lower_name.endswith('.pdf') or content.startswith(b'%PDF'):
        return extract_text_from_pdf(content)
    elif lower_name.endswith('.docx') or content.startswith(b'PK'):
        return extract_text_from_docx(content)
    else:
        # Default plain text
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('latin-1', errors='ignore')
        return clean_and_normalize_text(text), {"method": "plain_text"}

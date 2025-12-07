import PyPDF2
import pdfplumber
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting PDF with pdfplumber: {str(e)}")
            return self._fallback_extraction(file_path)
    
    def _fallback_extraction(self, file_path: str) -> str:
        """Fallback PDF extraction using PyPDF2"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error with fallback PDF extraction: {str(e)}")
            return ""
    
    def extract_metadata(self, file_path: str) -> Dict[str, any]:
        """Extract PDF metadata"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata
                return {
                    "title": metadata.get("/Title", "") if metadata else "",
                    "author": metadata.get("/Author", "") if metadata else "",
                    "pages": len(reader.pages)
                }
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {str(e)}")
            return {}
    
    def extract_tables(self, file_path: str) -> list:
        """Extract tables from PDF"""
        try:
            tables = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            return []

pdf_parser = PDFParser()
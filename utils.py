"""
PDF Text Extraction Utilities
Handles extracting and cleaning text from uploaded PDF resumes.
Pattern: Same approach used for document ingestion in RAG systems (Phase 2).
"""
 
import re
from PyPDF2 import PdfReader
from typing import Optional
 
 
def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """
    Extract text from an uploaded PDF file.
    Args:
        pdf_file: A file-like object (from Streamlit's file_uploader)
    Returns:
        Cleaned text string, or None if extraction fails
    """
    try:
        reader = PdfReader(pdf_file)
 
        if len(reader.pages) == 0:
            return None
 
        text_parts = []
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
 
        if not text_parts:
            return None
 
        full_text = "\n".join(text_parts)
        return clean_text(full_text)
 
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None
 
 
def clean_text(text: str) -> str:
    """Clean extracted text by fixing common PDF extraction issues."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = text.strip()
    return text
 
 
def validate_resume_text(text: str) -> dict:
    """
    Basic validation to check if extracted text looks like a resume.
    Returns:
        dict with is_valid (bool), word_count (int), warnings (list)
    """
    warnings = []
    word_count = len(text.split())
 
    if word_count < 50:
        warnings.append("Very short text. May be a scanned PDF (image-based).")
        warnings.append("Tip: Use a text-based PDF for best results.")
 
    if word_count > 5000:
        warnings.append("Very long resume. Consider trimming to most relevant content.")
 
    resume_keywords = ["experience", "education", "skills", "work", "project"]
    found_keywords = [kw for kw in resume_keywords if kw.lower() in text.lower()]
 
    if len(found_keywords) == 0:
        warnings.append("This doesn't appear to be a resume. No common resume sections found.")
 
    return {
        "is_valid": word_count >= 50 and len(found_keywords) > 0,
        "word_count": word_count,
        "warnings": warnings,
        "sections_found": found_keywords,
    }

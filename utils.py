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
    Validate extracted text and return detailed status.

    Returns:
        dict with:
            is_valid (bool)
            word_count (int)
            warnings (list)  — yellow, non-blocking
            errors (list)    — red, blocks analysis
            sections_found (list)
    """
    warnings = []
    errors = []
    word_count = len(text.split())

    # ── Scanned / image-only PDF (< 10 words) ────────────
    if word_count < 10:
        errors.append(
            "This looks like a scanned (image-only) PDF. "
            "No readable text was found. Please upload a "
            "text-based PDF, or copy-paste your resume into "
            "a Word doc and re-export as PDF."
        )
        return {
            "is_valid": False,
            "word_count": word_count,
            "warnings": warnings,
            "errors": errors,
            "sections_found": [],
        }

    # ── Very short resume (< 50 words) — warn, allow ─────
    if word_count < 50:
        warnings.append(
            "Very short text (under 50 words). Analysis may "
            "be less accurate. Consider a more detailed resume."
        )

    # ── Very long resume (> 5000 words) — show error ─
    if word_count > 5000:
        errors.append(
            f"🚫 INVALID FILE — {word_count:,} words detected. "
            "This is not a resume (resumes are typically "
            "300–1,000 words). Maximum allowed: 5,000 words. "
            "Please upload an actual resume to continue."
        )
        return {
            "is_valid": False,
            "word_count": word_count,
            "warnings": warnings,
            "errors": errors,
            "sections_found": [],
        }
        #if word_count > 5000:
            #warnings.append("❌ This file exceeds the 5,000-word limit and is not a valid resume. "
            #                "Resumes are typically 300–1,000 words. Please upload an actual resume.")
            #   estimated_tokens = int(word_count * 1.3)
            #   warnings.append(
            #      f"Very long resume ({word_count} words ≈ "
            #       f"{estimated_tokens} tokens). This will use more "
            #       "API tokens. Consider trimming to relevant content."
            #   )
    # ── Check for resume-like sections ────────────────────
    resume_keywords = ["experience", "education", "skills", "work", "project"]
    found_keywords = [kw for kw in resume_keywords if kw.lower() in text.lower()]

    if len(found_keywords) == 0:
        warnings.append(
            "This doesn't appear to be a resume — no common "
            "sections (Experience, Education, Skills) found."
        )

    return {
        "is_valid": word_count >= 10 and word_count<=5000 and len(found_keywords) > 0,
        "word_count": word_count,
        "warnings": warnings,
        "errors": errors,
        "sections_found": found_keywords,
    }
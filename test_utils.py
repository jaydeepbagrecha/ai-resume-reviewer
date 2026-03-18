from utils import extract_text_from_pdf, validate_resume_text
 
with open("sample_resume.pdf", "rb") as f:
    text = extract_text_from_pdf(f)
 
if text:
    print(f"Extracted {len(text)} characters")
    print(f"First 200 chars: {text[:200]}")
    print()
    validation = validate_resume_text(text)
    print(f"Valid: {validation['is_valid']}")
    print(f"Word count: {validation['word_count']}")
    print(f"Sections found: {validation['sections_found']}")
    for w in validation["warnings"]:
        print(f"  Warning: {w}")
else:
    print("Failed to extract text")

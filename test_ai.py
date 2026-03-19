from ai_engine import analyze_resume
 
sample_resume = """
John Doe
Software Engineer
Experience: 3 years Python development at TechCorp
Skills: Python, JavaScript, SQL, Git, REST APIs
Education: B.S. Computer Science, State University 2021
"""
 
sample_jd = """
Senior Python Developer
Requirements: 5+ years Python, Django, AWS, Docker, PostgreSQL
Nice to have: Kubernetes, CI/CD, machine learning experience
"""
 
result = analyze_resume(sample_resume, sample_jd)
 
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Match Score: {result['match_score']}/100")
    print(f"Missing Keywords: {result['missing_keywords']}")
    print(f"Strengths: {len(result['strengths'])} found")
    print(f"Improvements: {len(result['improvements'])} found")
    print(f"Tokens used: {result['total_tokens']}")
    print(f"\nRewritten Summary:\n{result['rewritten_summary']}")

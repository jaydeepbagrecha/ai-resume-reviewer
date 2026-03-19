"""
Prompt Templates for AI Resume Reviewer
 
This module contains all prompts used by the application.
Centralizing prompts makes them easy to iterate, test, and version control.
Key principle: Prompt quality determines product quality.
"""
 
SYSTEM_PROMPT = """You are an expert resume reviewer and career coach with 15 years
of experience in technical recruiting across startups and Fortune 500 companies.
 
Your task is to analyze a candidate's resume against a specific job description
and provide actionable, detailed feedback.
 
Rules:
- Only reference information actually present in the resume
- Do not invent or assume qualifications the candidate doesn't have
- Be constructive and specific in your feedback
- Provide actionable suggestions, not vague advice
- Score honestly - a 90+ score should mean the resume is genuinely excellent for this role
 
Always respond in valid JSON format with no additional text outside the JSON."""
 
 
def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    """
    Build the user prompt that includes the resume and job description.
    Uses chain-of-thought: instructs the AI to analyze step by step.
    """
    return f"""Analyze the following resume against the job description.
 
STEP 1: Read the job description carefully. Identify the key requirements,
must-have skills, nice-to-have skills, and experience level expected.
 
STEP 2: Read the resume. Map the candidate's skills, experience, and
achievements to the job requirements identified in Step 1.
 
STEP 3: Provide your analysis as a JSON object with these exact keys:
 
{{
    "match_score": <integer 0-100>,
    "score_explanation": "<1-2 sentence explanation of the score>",
    "missing_keywords": ["<keyword1>", "<keyword2>", ...],
    "strengths": [
        "<specific strength with evidence from resume>",
        "<another strength>",
        ...
    ],
    "improvements": [
        "<specific, actionable improvement suggestion>",
        "<another improvement>",
        ...
    ],
    "rewritten_summary": "<A 3-4 sentence professional summary tailored to this job>"
}}
 
---
JOB DESCRIPTION:
{job_description}
 
---
RESUME:
{resume_text}
 
---
Respond with ONLY the JSON object. No markdown, no code fences, no explanation."""
 
 
# Example of a well-structured output (for testing/reference)
EXAMPLE_OUTPUT = {
    "match_score": 72,
    "score_explanation": "Strong technical skills match but lacks required 5+ years of cloud experience.",
    "missing_keywords": ["Kubernetes", "Terraform", "CI/CD pipelines", "AWS certification"],
    "strengths": [
        "3 years of Python development experience directly relevant to the role",
        "Led a team of 4 developers, demonstrating the leadership skills mentioned in the JD",
        "Published open-source contributions showing initiative and community engagement"
    ],
    "improvements": [
        "Add a dedicated Skills section listing cloud technologies (AWS, GCP, Azure)",
        "Quantify achievements: instead of 'improved performance', say 'reduced latency by 40%'",
        "Include the word 'Kubernetes' - it appears 3 times in the job description",
        "Move the Professional Summary to the top and tailor it to this specific role"
    ],
    "rewritten_summary": "Results-driven Python developer with 3 years of experience..."
}

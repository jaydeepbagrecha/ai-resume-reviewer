"""
AI Analysis Engine
Handles communication with the OpenAI API.
 
Pattern: This is the exact pattern for any LLM-powered feature:
1. Format the prompt with user data
2. Call the API with error handling
3. Parse the structured response
4. Return clean results
"""
 
import os
import json
import time
from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, build_analysis_prompt
 
load_dotenv()
 
# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
# Configuration
MODEL = "gpt-4.1-mini"
MAX_TOKENS = 4096
MAX_RETRIES = 3
RETRY_DELAY = 2
 
 
def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Send resume and job description to OpenAI for analysis.
 
    Args:
        resume_text: Extracted text from the resume PDF
        job_description: The job description to compare against
 
    Returns:
        dict with analysis results, or error dict if something fails
    """
    # Build the prompt
    user_prompt = build_analysis_prompt(resume_text, job_description)
 
    # Call the API with retry logic
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
            )
 
            # Extract the text content from the response
            raw_text = response.choices[0].message.content
 
            # Parse JSON response
            result = parse_ai_response(raw_text)
 
            if result:
                # Add metadata
                result["model"] = MODEL
                result["input_tokens"] = response.usage.prompt_tokens
                result["output_tokens"] = response.usage.completion_tokens
                result["total_tokens"] = response.usage.total_tokens
                return result
            else:
                return {"error": "Failed to parse AI response", "raw": raw_text}
 
        except RateLimitError:
            wait_time = RETRY_DELAY * attempt
            print(f"Rate limited. Waiting {wait_time}s... (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait_time)
            continue
 
        except APITimeoutError:
            print(f"Timeout on attempt {attempt}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                continue
            return {"error": "API request timed out after all retries"}
 
        except APIError as e:
            return {"error": f"API error: {str(e)}"}
 
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
 
    return {"error": "Failed after all retry attempts"}
 
 
def parse_ai_response(raw_text: str) -> dict | None:
    """
    Parse the AI response text into a structured dict.
    Handles common issues:
    - Response wrapped in markdown code fences
    - Extra whitespace or newlines
    - Invalid JSON (returns None)
    """
    text = raw_text.strip()
 
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
 
    try:
        result = json.loads(text)
 
        required_keys = [
            "match_score", "missing_keywords",
            "strengths", "improvements", "rewritten_summary"
        ]
        for key in required_keys:
            if key not in result:
                print(f"Missing required key in response: {key}")
                return None
 
        if not (0 <= result["match_score"] <= 100):
            result["match_score"] = max(0, min(100, result["match_score"]))
 
        return result
 
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw text: {text[:500]}")
        return None

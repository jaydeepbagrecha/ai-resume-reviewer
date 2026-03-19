# Phase 1: LLM APIs & Prompt Engineering (OpenAI GPT)

**Build an AI Resume Reviewer SaaS tool from scratch in 2–3 weeks.**

Part of the [AI Product Builder Milestone Guide](./AI_Product_Builder_Milestone_Guide.docx) · March 2026

---

## What You're Building

An AI-powered Resume Reviewer that accepts a PDF resume and a job description, analyzes the match using the OpenAI GPT API, and returns a detailed report — complete with a match score, missing keywords, strengths, improvement suggestions, and a rewritten professional summary. The finished product is deployed live on Streamlit Community Cloud.

---

## Key Skills Covered

- **LLM API Integration** — Calling the OpenAI Python SDK with structured output
- **Prompt Engineering** — System prompts, chain-of-thought reasoning, JSON-formatted responses
- **PDF Processing** — Extracting and cleaning text from uploaded resumes
- **Web App Development** — Building an interactive UI with Streamlit (pure Python, no frontend code)
- **Cloud Deployment** — Shipping to Streamlit Community Cloud with secrets management
- **Error Handling & Retries** — Production-grade resilience for LLM API calls
- **Token Usage Tracking** — Monitoring and estimating API cost per request

---

## Prerequisites

- Completed **Phase 0** (or equivalent Python + Git comfort)
- Python 3.10+ with virtual environment knowledge
- A GitHub account and basic Git commands (`add`, `commit`, `push`)
- An OpenAI account ([platform.openai.com](https://platform.openai.com))
- A credit card for OpenAI API usage (~$2–$5 for the entire project)

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **OpenAI GPT API** | LLM-powered resume analysis |
| **Streamlit** | Python-native web framework for the UI |
| **PyPDF2** | PDF text extraction |
| **python-dotenv** | Environment variable management |
| **Streamlit Community Cloud** | Free deployment and hosting |

---

## Project Structure

```
resume-reviewer/
├── app.py               # Main Streamlit application
├── prompts.py           # System prompts & prompt templates
├── utils.py             # PDF extraction & helper functions
├── .env                 # API key (NEVER commit this)
├── .gitignore           # Files Git should ignore
├── requirements.txt     # Project dependencies
├── sample_resume.pdf    # A test resume for demo
└── README.md            # Project documentation
```

---

## Step-by-Step Breakdown

| Step | Task | Time Estimate |
|------|------|---------------|
| 1 | **Set Up Project & Install Dependencies** — Create the project folder, virtual environment, install packages, configure `.env` and `.gitignore` | 1–2 hours |
| 2 | **Build the PDF Text Extractor (`utils.py`)** — Extract and clean text from uploaded PDF resumes, handle edge cases | 2–3 hours |
| 3 | **Design Your Prompt Chain (`prompts.py`)** — Craft system prompts using prompt engineering best practices; structure output as JSON | 3–4 hours |
| 4 | **Build the AI Analysis Function** — Wire up OpenAI API calls with retry logic, JSON parsing, and token tracking | 3–4 hours |
| 5 | **Build the Streamlit UI (`app.py`)** — File upload, text input, color-coded results display, progress indicators | 4–5 hours |
| 6 | **Add Polishing Features** — Download report button, built-in example resume, token cost display, error states | 3–4 hours |
| 7 | **Deploy to Streamlit Cloud** — Push to GitHub, deploy on Streamlit Community Cloud, configure secrets | 1–2 hours |

**Total: 17–24 hours (2–3 weeks at part-time pace)**

---

## How to Use This Guide

1. Open `Phase_1_Complete_StepByStep_Guide_OpenAI.docx` and follow each step sequentially.
2. Every command, every file, and every line of code is provided — type it out yourself for maximum retention.
3. Use the **checkpoints** at the end of each step to verify your progress before moving on.
4. After deployment, share your live URL and collect feedback from real users.

---

## What Comes Next

After completing Phase 1, you move to **Phase 2: RAG Systems & Vector Databases**, where you will:

- Ingest multiple documents into a vector database (instead of processing a single PDF)
- Build a retrieval-augmented generation (RAG) pipeline
- Add source citations and confidence metrics
- Reuse the OpenAI API, prompt design, and Streamlit skills from this phase

---

## Related Guides

| Document | Description |
|---|---|
| `Phase_0_Complete_StepByStep_Guide.docx` | Python + Git foundations (prerequisite) |
| `Phase_1_Complete_StepByStep_Guide.docx` | Phase 1 using the Anthropic Claude API |
| `Phase_2_Complete_StepByStep_Guide_OpenAI.docx` | Phase 2 — RAG & Vector Databases (OpenAI) |
| `AI_Product_Builder_Milestone_Guide.docx` | Full 5-phase curriculum overview |

---

> **Phase 1 complete.** You have a live AI product. Now go get feedback and start Phase 2.

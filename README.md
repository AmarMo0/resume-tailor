# AI Resume Tailor

A Python prototype that compares a CV with a job description,
identifies requirements not demonstrated in the CV, and generates
a tailored CV.

## Features

- Extracts job requirements using structured model output.
- Compares requirements against evidence across the full CV.
- Reports missing and partially demonstrated requirements.
- Generates revised CV text with instructions to preserve facts.

## Setup

Requires Python and uv.

```powershell
uv sync
Copy-Item .env.example .env
```

Add your OpenAI API key to `.env`.

## Run

Edit `cv_test.txt` and `job_description.txt`, then run:

```powershell
uv run python main.py
```

The included CV and job description are fictional examples.
Running the application makes paid OpenAI API calls.

## Outputs

- `comparison.json`
- `gap_report.txt`
- `tailored_cv.txt`

Output files are overwritten on each run.

## Limitations

Model results may contain incorrect matches or unsupported claims.
Review the generated CV before using it. Missing CV evidence does
not necessarily mean the candidate lacks a skill.

This prototype processes plain text and does not predict hiring
outcomes or provide an ATS score.
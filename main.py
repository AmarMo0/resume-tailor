from pathlib import Path

from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from prompts import comparison_prompt, system_prompt, tailoring_prompt
from schemas import CVComparison, JobAnalysis


BASE_DIR = Path(__file__).resolve().parent


def extract_requirements(
    llm: ChatOpenAI,
    job_description: str,
) -> JobAnalysis:
    structured_model = llm.with_structured_output(JobAnalysis)

    return structured_model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=job_description),
    ])


def compare_cv(
    llm: ChatOpenAI,
    cv: str,
    analysis: JobAnalysis,
) -> CVComparison:
    comparison_model = llm.with_structured_output(CVComparison)

    return comparison_model.invoke([
        SystemMessage(content=comparison_prompt),
        HumanMessage(content=f"""
Job requirements:
{analysis.model_dump_json(indent=2)}

CV:
{cv}
"""),
    ])


def build_gap_report(comparison: CVComparison) -> str:
    missing = []
    partial = []

    for match in comparison.matches:
        if match.status == "not_evidenced":
            missing.append(
                f"- {match.requirement}: {match.explanation}"
            )
        elif match.status == "partially_supported":
            partial.append(
                f"- {match.requirement}: {match.explanation}"
            )

    sections = [
        "JOB GAP REPORT",
        "This report describes evidence in the CV, not everything "
        "the candidate may know.",
    ]

    if missing:
        sections.append(
            "Not demonstrated in your CV:\n" + "\n".join(missing)
        )

    if partial:
        sections.append(
            "Partially demonstrated in your CV:\n" + "\n".join(partial)
        )

    if not missing and not partial:
        sections.append(
            "No gaps were identified in the supplied comparison."
        )

    return "\n\n".join(sections)


def tailor_cv(
    llm: ChatOpenAI,
    cv: str,
    analysis: JobAnalysis,
    comparison: CVComparison,
) -> str:
    response = llm.invoke([
        SystemMessage(content=tailoring_prompt),
        HumanMessage(content=f"""
Original CV:
{cv}

Job requirements:
{analysis.model_dump_json(indent=2)}

Comparison:
{comparison.model_dump_json(indent=2)}
"""),
    ])

    return response.content


def main():
    load_dotenv(BASE_DIR / ".env")

    job_description = (
        BASE_DIR / "job_description.txt"
    ).read_text(encoding="utf-8")

    cv = (BASE_DIR / "cv_test.txt").read_text(encoding="utf-8")

    if not job_description.strip() or not cv.strip():
        raise ValueError("The CV and job description must not be empty.")

    llm = ChatOpenAI(model="gpt-5-nano")

    print("Extracting job requirements...")
    analysis = extract_requirements(llm, job_description)

    print("Comparing the CV...")
    comparison = compare_cv(llm, cv, analysis)

    (BASE_DIR / "comparison.json").write_text(
        comparison.model_dump_json(indent=2),
        encoding="utf-8",
    )

    gap_report = build_gap_report(comparison)

    (BASE_DIR / "gap_report.txt").write_text(
        gap_report,
        encoding="utf-8",
    )

    print(f"\n{gap_report}\n")

    print("Generating the tailored CV...")
    tailored_cv = tailor_cv(llm, cv, analysis, comparison)

    output_path = BASE_DIR / "tailored_cv.txt"

    output_path.write_text(
        tailored_cv,
        encoding="utf-8",
    )

    print(f"\nSaved tailored CV: {output_path}")
    print(tailored_cv)


if __name__ == "__main__":
    main()
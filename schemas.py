from typing import Literal, List 
from pydantic import BaseModel, Field

class JobRequirement(BaseModel):
    requirement: str = Field(
        ...,
        description="requirment in job description")
    importance: Literal['required', 'preferred', 'unspecified']

class JobAnalysis(BaseModel):
    requirements: list[JobRequirement] = Field(
        ...,
        description="All requirements extracted from the job description",
    )

class RequirementMatch(BaseModel):
    requirement: str 
    status: Literal[
        "supported", 
        "partially_supported", 
        "not_evidenced"
    ]
    evidence: list[str] = Field(
        ...,
        description="Exact supporting passages from the CV; empty if none",
    )
    explanation: str

class CVComparison(BaseModel):
    matches: list[RequirementMatch] = Field(
        ...,
        description="One comparison result for each job requirement",
    )
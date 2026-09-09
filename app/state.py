from __future__ import annotations
from typing import Annotated, Literal, TypedDict

from langgraph.graph.message import add_messages

from pydantic import BaseModel, Field

def merge_dicts(left: dict | None, right: dict|None) -> dict:
    left = left or {}
    right = right or {}
    return {**left, **right}

class ParseJD(BaseModel):
    title: str = Field(description= "Job title e.g 'Software Engineer'")
    must_have_skills: list[str] = Field(description="Non negotiable required skills mentioned in JD")
    nice_to_have_skills: list[str] = Field(description="optional/bonus skills mentioned in JD")
    min_expreience_years: float = Field(description= "Minimum years of experience required, 0 if fresher role")
    key_responsibilities: list[str] = Field(description= "3-6 core responsibilities extracted from JD")

class ParseResume(BaseModel):
    candidate_name: str
    total_experience_years: float = Field(description= "Best effort estimate of total professional experience in years")
    skills: list[str] = Field(description="All technicals and professional skills mentioned in resume")
    education: str = Field(description="Highest/most relevant qualification, one line")
    past_roles: list[str] = Field(default_factory=list, description="Job titles held previously,most recent first")

class CandidateScore(BaseModel):
    candidate_name: str
    skill_match_score: float = Field(gr=0, le=100, description= "0-100 skills overlap score")
    experience_match_score: float = Field(gr=0, le=100)
    overall_score: float = Field(gr=0, le=100, description= "0-100 weighted final score")
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list, description="Missing must-have skills etc.")
    recommendations: Literal["shortlist","rejected","manual_review"] = Field(description=" shortlist if overall_score>75, reject if <45, else manual_review")
    reasoning: str = Field(description="1-2 line justification for the recommendation")

class BiasReport(BaseModel):
    candidate_name: str
    flags: list[str] = Field(default_factory=list, description= "Any bias-risk phrases found in reasoning (age/gender/name-based etc.)")
    is_clean: bool = Field(description="True is no bias detected")


class GraphState(TypedDict, total = False):
    jd_text : str
    resume_texts: dict[str,str]
    parsed_jd: ParseJD
    parsed_resume: Annotated[dict[str, ParseResume],merge_dicts]
    scores: Annotated[dict[str, CandidateScore], merge_dicts]
    bias_reports: Annotated[dict[str, BiasReport], merge_dicts]

    shortlisted: list[str]

    rejected: list[str]

    manual_review: list[str]

    manual_review_decision: dict[str,str]

    interview_questions: dict[str,list[str]]

    final_report: str

    messages: Annotated[str, add_messages]

class ResumeFanoutState(TypedDict):
    candidate_id: str
    resume_text: str
    parsed_jd : ParseJD



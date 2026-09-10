from langchain_groq import ChatGroq
from app.state import CandidateScore, ParseJD, ParseResume

MATCH_PROMPT = """
You are an expert senior technical recruiter who scores the candidates objectively.

JOB REQUIREMENTS:
- Title:{jd_title}
- Must_have skilss: {must_have}
- Nice_to_have skills: {nice_to_have}
- Min Experience required: {min_exp} years

Candidate Profile:
- Name:{name}
- Experience: {exp} years
- Skills: {skills}
- Education: {education}
- Past roles: {past_roles}

Scoring_rules:
- skill_match_score:
  Score 0-100 based on how well the candidate's skills match the JD's must-have and nice-to-have skills.

- experience_match_score:
  Score 0-100 based on how closely the candidate's total experience matches the minimum experience required.

- overall_score:
  Calculate a weighted final score from skill_match_score and experience_match_score, ranging from 0-100.

- strengths:
  List the candidate's key strengths that directly align with the JD requirements.

- gaps:
  List important missing must-have skills, insufficient experience, or other major mismatches.

- recommendations:
  Return "shortlist" if overall_score > 75, "rejected" if overall_score < 45, otherwise "manual_review".

- reasoning:
  Provide a concise 1-2 line justification explaining the recommendation based on the scores, strengths, and gaps.
"""

def score_candidate(llm: ChatGroq, parsed_jd: ParseJD, candidate_id:str, resume: ParseResume) -> CandidateScore:

    structured_llm = llm.with_structured_output(CandidateScore)
    result = structured_llm.invoke(MATCH_PROMPT.format(
        jd_title = parsed_jd.title,
        must_have = ", ".join(parsed_jd.must_have_skills),
        nice_to_have = ", ".join(parsed_jd.nice_to_have_skills) or "None",
        min_exp = parsed_jd.min_expreience_years,
        name = resume.candidate_name or candidate_id,
        exp = resume.total_experience_years,
        skills = ", ".join(resume.skills),
        education = resume.education,
        past_roles = ", ".join(resume.past_roles) or "Not Specified"
    ))

    return result
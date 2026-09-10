from app.llm import get_llm
from app.nodes.bias_checker import check_bias
from app.nodes.matcher import score_candidate
from app.nodes.resume_parser import parse_resume
from app.state import ResumeFanoutState

def candidate_pipeline_node(state: ResumeFanoutState) -> dict:
    llm = get_llm()
    candidate_id = state["candidate_id"]

    parsed_resume = parse_resume(llm, state["resume_text"])

    score = score_candidate(llm, state["parsed_jd"], candidate_id, parsed_resume)

    bias_report = check_bias(llm, candidate_id, score)

    log_line = (
        f"[Candidate Pipeline] {candidate_id}->{parsed_resume.candidate_name}"
        f"score = {score.overall_score} -> {score.recommendations}"
    )

    if not bias_report.is_clean:
        log_line += f"| BIAS FLAG: {bias_report.flags}"
    
    return {
        "parsed_resumes":{candidate_id: parsed_resume},
        "scores":{candidate_id: score},
        "bias_reports":{candidate_id: bias_report},
        "messages": [{"role":"assistant", "content":log_line}]
    }
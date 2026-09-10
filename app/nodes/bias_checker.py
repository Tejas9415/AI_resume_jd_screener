from langchain_groq import ChatGroq
from app.state import BiasReport, CandidateScore

BIAS_REPORT_CHECKER_PROMPT = """
Check the following candidate scoring reasoning for potential hiring bias.

Rules:

- flags:
  List any phrases that indicate potential bias based on protected or irrelevant factors such as age, gender, name, race, religion, nationality, marital status, disability, or similar personal characteristics.
  Return an empty list if no bias-risk phrases are found.

- is_clean:
  Return True if no bias is detected in the reasoning; otherwise return False.

Reasoning:
{reasoning}
"""

def check_bias(llm: ChatGroq, candidate_id: str, score: CandidateScore) -> BiasReport:
    structured_llm = llm.with_structured_output(BiasReport)
    return structured_llm.invoke(BIAS_REPORT_CHECKER_PROMPT.format(
        reasoning = score.reasoning
    ))
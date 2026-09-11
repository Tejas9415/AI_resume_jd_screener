"""
report_generator.py
--------------------
Final node - saara pipeline output ek clean Markdown hiring report mein
compile karta hai. Yeh pure Python formatting hai (LLM call nahi).
"""

from datetime import datetime

from app.state import GraphState


def generate_report_node(state: GraphState) -> dict:
    jd = state["parsed_jd"]
    lines: list[str] = []
    # ^ report ko line-by-line build karenge, end mein "\n".join() se
    #   ek poori string banegi - bar-bar string += karne se better hai

    lines.append(f"# Recruitment Screening Report - {jd.title}")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append(
        f"**Candidates screened:** {len(state['scores'])} | "
        f"**Shortlisted:** {len(state.get('shortlisted', []))} | "
        f"**Rejected:** {len(state.get('rejected', []))}\n"
    )

    lines.append("## Shortlisted Candidates\n")
    for cid in state.get("shortlisted", []):
        score = state["scores"][cid]
        lines.append(f"### {score.candidate_name} (`{cid}`) - Score: {score.overall_score:.0f}/100")
        lines.append(f"- **Strengths:** {', '.join(score.strengths) or 'N/A'}")
        lines.append(f"- **Gaps:** {', '.join(score.gaps) or 'None major'}")
        lines.append(f"- **Reasoning:** {score.reasoning}")
        if cid in state.get("manual_review_decisions", {}):
            # agar is candidate ka decision insaan ne diya tha, wo transparently note karo
            lines.append("- **Note:** Human-reviewed (borderline AI score, recruiter approved)")
        questions = state.get("interview_questions", {}).get(cid, [])
        if questions:
            lines.append("- **Suggested interview questions:**")
            for q in questions:
                lines.append(f"  - {q}")
        lines.append("")

    lines.append("## Rejected Candidates\n")
    for cid in state.get("rejected", []):
        score = state["scores"][cid]
        note = " (human-reviewed)" if cid in state.get("manual_review_decisions", {}) else ""
        lines.append(f"- **{score.candidate_name}** (`{cid}`) - Score: {score.overall_score:.0f}/100{note}")
        lines.append(f"  - Gaps: {', '.join(score.gaps) or 'N/A'}")

    bias_flags = {
        cid: r.flags for cid, r in state.get("bias_reports", {}).items() if not r.is_clean
    }
    # ^ dict comprehension: sirf un candidates ko rakho jinke bias_report
    #   mein is_clean False hai - baaki sab (clean) is dict mein nahi aayenge

    if bias_flags:
        lines.append("\n## \u26a0 Fairness Audit Flags\n")
        for cid, flags in bias_flags.items():
            lines.append(f"- `{cid}`: {flags}")
    else:
        lines.append("\n## Fairness Audit\n")
        lines.append("No bias risk flagged across any candidate reasoning. \u2705")

    report = "\n".join(lines)
    return {
        "final_report": report,
        "messages": [{"role": "assistant", "content": "[Report Generator] Final report ready."}],
    }
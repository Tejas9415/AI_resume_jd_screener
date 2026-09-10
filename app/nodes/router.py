from app.state import GraphState

def sort_candidates_node(state: GraphState) -> dict:

    shortlisted, rejected, manual_review = [],[],[]

    for candidate_id, score in state["scores"].items():

        if score.recommendations == "shortlist":
            shortlisted.append(candidate_id)
        elif score.recommendations == "rejected":
            rejected.append(candidate_id)
        else:
            manual_review.append(candidate_id)

    
    return {
        "shortlisted": shortlisted,
        "rejected": rejected,
        "manual_review":manual_review,
        "messages":[
            {
                "role":"assistant",
                "content": f"[Router] shortlist = {len(shortlisted)},rejected = {len(rejected)}, manual_review = {len(manual_review)}"
            }
        ]
    }
def route_after_sort(state: GraphState) -> str:
    if state.get("manual_review"):
        return "human_reviews"
    
    return "generate_questions"
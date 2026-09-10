from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from app.nodes.candidate_pipeline import candidate_pipeline_node
from app.nodes.jd_parser import parse_jd_node
from app.nodes.router import sort_candidates_node
from app.state import GraphState

def fanout_resumes(state: GraphState) -> list[Send]:
    return [
        Send(
            "candidate_pipeline", #kis node ko target karna hai 
            {
                "candidate_id": candidate_id,
                "resume_text": resume_text,
                "parsed_jd": state["parsed_jd"]
    
            }
        )
        for candidate_id, resume_text in state["resume_texts"].items()
    ]
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("parsed_jd", parse_jd_node)
    graph.add_node("candidate_pipeline",candidate_pipeline_node)
    graph.add_node("sort_candidates", sort_candidates_node)

    graph.add_edge(START,"parsed_jd")
    graph.add_conditional_edges("parsed_jd",fanout_resumes,["candidate_pipeline"])

    graph.add_edge("candidate_pipeline","sort_candidates")
    graph.add_edge("sort_candidates", END)

    checkpointer = MemorySaver()

    return graph.compile(checkpointer= checkpointer)
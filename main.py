from graph import build_graph
from app.state import GraphState

graph = build_graph()
config = {"configurable":{"thread_id":"test-1"}}

result = graph.invoke(
    {
        "jd_text": """We are looking for an AI Engineer to join our team and build production-ready
Generative AI applications. The ideal candidate should have 2+ years of experience
in software or AI engineering and strong hands-on experience with Python and LLMs.

You should have experience building RAG applications, working with LangChain or
similar frameworks, and developing APIs using FastAPI. Knowledge of vector databases
such as FAISS, ChromaDB, or Pinecone is required. Experience with AWS or Azure,
Docker, and Git is also expected.

Experience with LangGraph, multi-agent systems, OpenAI APIs, MCP, Databricks, or
Apache Spark would be a plus.

The role involves developing LLM-powered applications, building RAG pipelines,
creating AI agents and workflows, integrating LLM APIs and external tools, and
developing scalable backend services.""",

        "resume_texts": {
            "candidate1": "Rahul Sharma, Software Engineer with 4 years of experience in Python, FastAPI, AWS, PostgreSQL, Docker, and REST APIs. B.Tech in Computer Science from IIT Delhi.",
            "candidate2": "Priya Mehta, Software Developer with 3 years of experience in Java, Spring Boot, MySQL, Docker, and AWS. B.E. in Computer Science from VIT."
        }
    },
    config=config
)

print("Shortlisted:", result.get("shortlisted"))
print("Rejected:", result.get("rejected"))
print("Manual Review:", result.get("manual_review"))

score = result["scores"]
print(score)
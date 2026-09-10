from app.llm import get_llm
from app.state import GraphState, ParseJD

PARSE_JD_PROMPT = """
You are an expert Job Description parser. Parse the given JD and extract information
according to the ParseJD schema.

Rules:

- title:
  Extract the primary job title from the JD. Keep it concise and use the exact or
  most appropriate title mentioned in the JD.

- must_have_skills:
  Extract all skills, technologies, tools, frameworks, programming languages,
  platforms, or qualifications that are explicitly required or mandatory.

- nice_to_have_skills:
  Extract skills, technologies, tools, frameworks, or qualifications that are
  explicitly optional, preferred, bonus, or good-to-have.

- min_expreience_years:
  Extract the minimum years of experience required.

- key_responsibilities:
  Extract 3-6 of the most important responsibilities from the JD.

General rules:
- Return only structured output matching the ParseJD schema.

Job Description:
{jd_text}
"""

def parse_jd_node(state: GraphState) -> dict:
    llm = get_llm(temperature= 0)

    structured_llm = llm.with_structured_output(ParseJD)

    parsed: ParseJD = structured_llm.invoke(PARSE_JD_PROMPT.format(jd_text = state["jd_text"]))

    return {
        "parsed_jd": parsed,

        "messages":[
            {
                "role":"assistant",
                "content":f"[JD Parser] '{parsed.title} role is parsed"
            }
        ]
    }
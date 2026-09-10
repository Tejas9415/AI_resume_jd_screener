from langchain_groq import ChatGroq
from app.state import ParseResume

PARSE_RESUME_PROMPT = """
You are an expert resume parser. Parse the following resume and extract information
according to the ParseResume schema.

Rules:
- total_experience_years:
  Estimate the candidate's total professional work experience in years.
  Consider full-time jobs, internships, and other relevant professional experience.
  Avoid double-counting overlapping experiences. Use 0.0 for a fresher.

- skills:
  Extract all technical and professional skills explicitly mentioned in the resume,
  including programming languages, frameworks, libraries, databases, cloud platforms,
  tools, technologies, soft skills, and domain-specific skills.

- education:
  Extract the highest or most relevant educational qualification.
  Include the degree, specialization, and institution where available.
  Keep it to one concise line.
  
- past_roles:
  Extract job titles held by the candidate, with the most recent role first.
  Include internships and relevant previous professional roles.
  Do not include projects, responsibilities, or company names as roles.

General rules:
- Use only information present in the resume.
- Do not hallucinate or infer missing information.
- Keep the output concise and structured according to the ParseResume schema.
- Return only the structured output.
  
Resume:
{resume_text}
"""


def parse_resume(llm: ChatGroq, resume_text: str) -> ParseResume:
    structured_llm  = llm.with_structured_output(ParseResume)
    return structured_llm.invoke(PARSE_RESUME_PROMPT.format(resume_text = resume_text))
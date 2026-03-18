import json
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import SYSTEM_PROMPT, ARCHITECT_PROMPT


def get_llm(api_key: str, provider: str = "openai", model: str = "gpt-4o", temperature: float = 0.3):
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=model,
            temperature=temperature,
            groq_api_key=api_key,
            max_tokens=4000,
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key,
            max_tokens=4000,
        )


def build_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(ARCHITECT_PROMPT),
    ])
    chain = prompt | llm | StrOutputParser()
    return chain


def generate_architecture(idea: str, api_key: str, provider: str = "openai", model: str = "gpt-4o") -> dict:
    if not idea or not idea.strip():
        raise ValueError("Project idea cannot be empty.")
    if not api_key or not api_key.strip():
        raise ValueError("API key is required.")

    llm = get_llm(api_key, provider, model)
    chain = build_chain(llm)

    raw_output = chain.invoke({"idea": idea.strip()})

    raw_output = raw_output.strip()
    if raw_output.startswith("```"):
        raw_output = raw_output.split("\n", 1)[-1]
    if raw_output.endswith("```"):
        raw_output = raw_output.rsplit("```", 1)[0]
    raw_output = raw_output.strip()

    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON. Please try again.\nError: {str(e)}")

    return result

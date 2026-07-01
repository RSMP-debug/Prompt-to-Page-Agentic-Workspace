from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from .prompts import *
from .states import *
from .tools import *


load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")


def planner_agent(state: dict) -> dict:
    user_input = state["user_prompt"]

    planner_chain = planner_prompt_template() | llm.with_structured_output(Plan)
    resp = planner_chain.invoke({"user_prompt": user_input})


    return {"plan": resp}


def architect_agent(state: dict) -> dict:

    plan_instance: Plan = state["plan"]


    plan_string_data = str(plan_instance.model_dump())

    architect_chain = architect_prompt_template() | llm.with_structured_output(Task)
    resp = architect_chain.invoke({"plan": plan_string_data})


    return {"task_plan": resp}


def clean_code(code: str) -> str:
    code = code.strip()

    if code.startswith("```"):
        lines = code.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines)

    return code.strip()

def coder_agent(state: dict) -> dict:

    task_plan: Task = state["task_plan"]

    generated_files = {}

    coder_chain = (
        coder_prompt_template()
        | llm
    )

    for step in task_plan.implementation_steps:

        file_path = step.file_path

        existing_code = read_file.invoke(
            {"path": file_path}
        )

        generated_code = coder_chain.invoke(
            {
                "task_description": step.implementation_task,
                "file_path": file_path,
                "current_code": existing_code,
            }
        ).content

        generated_code = clean_code(generated_code)

        write_file.invoke(
            {
                "path": file_path,
                "content": generated_code
            }
        )

        generated_files[file_path] = generated_code

    return {
        "generated_files": generated_files
    }



graph = StateGraph(MasterGraphState)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge(START, "planner")
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_edge("coder", END)


agent = graph.compile()
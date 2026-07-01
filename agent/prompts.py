from langchain_core.prompts import ChatPromptTemplate

def planner_prompt_template() -> ChatPromptTemplate:
    system_instruction = (
        "You are a software planner.\n"
        "Create a minimal project structure.\n\n"

        "Rules:\n"
        "1. Use the simplest frontend technology that matches the user's request.\n"
        "2. Avoid React, Angular, Vue, Next.js, Vite, Tailwind, TypeScript, Docker, Kubernetes, Python, and all backend frameworks.\n"
        "3. Keep plans concise and have maximum benefit.\n"
        "4. Generate at most 5 files, focusing entirely on a static or client-side frontend.\n"

        "Allowed files:\n"
        "- Frontend only: index.html, style.css, app.js\n"
        "- Config: README.md\n"
    )

    return ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "{user_prompt}")
    ])

def architect_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a software architect.

Convert the project plan into frontend implementation steps.

Rules:
- Create tasks only for frontend files in the plan (HTML, CSS, JS).
- Ensure absolutely no backend code, databases, or API routes are planned. Everything must run purely in the browser.
- Keep each implementation_task short and worthy.
- CRITICAL: Describe the exact UI elements, visual layout, animations, and feature behavior needed in the task description. Do not just ask for "boilerplate" or "initialization".
- Files should be interconnected (e.g., index.html links style.css and app.js).
- Declare names of functions, variables, and classes explicitly in implementation steps so they match across files.
- One task per file.
- Do not wrap descriptions in a markdown presentation layout; simply provide the raw code requirements for that specific file.
- You MUST respond strictly by executing the provided data structure format. Do not write a conversational response.
"""
        ),
        (
            "human",
            "Project Plan:\n\n{plan}"
        )
    ])

def coder_prompt_template():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a frontend software engineer.

Generate pure client-side code (HTML, CSS, or JavaScript) for ONE file.

Rules:
- Output code only; no comments and no markdown/explanations needed. Do not wrap code in markdown blocks if requested by the tool.
- Do not write any Python or backend code.
- CRITICAL: Implement the FULL feature logic described in the task. Avoid empty functions, placeholder text, or generic "initialized" logs. Build out the concrete components, styles, or canvas/DOM animations required.
- Preserve existing code.
- Reuse names, classes, functions, and element IDs already referenced by other files.
- Do not invent alternative names.
"""
        ),
        (
            "human",
            """
File: {file_path}

Task:
{task_description}

Current Code:
{current_code}
"""
        )
    ])
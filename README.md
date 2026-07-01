# GraphForge UI: Multi-Agent Stateful Frontend Generator

An autonomous frontend web application generator powered by a multi-agent system. Instead of making standard, singular LLM API calls, this system leverages a graph-based orchestration topology to distribute work sequentially among specialized AI agents (a Planner, an Architect, and a tool-using Coder ReAct loop) to produce production-ready, client-side source code.

## 🧠 System Architecture & Workflow

The orchestration engine handles user requests through a stateful network, passing updated context safely via discrete graph nodes:

1. **Planner Agent:** Scopes out the simplest, cleanest architectural layout that completely matches the user's requirements. It strictly enforces a set of rules preventing bloated frameworks and isolates the scope to essential static frontend components.
2. **Architect Agent:** Translates the project plan into structural implementation maps. It outlines exact layouts, functions, DOM elements, and CSS classes file-by-file to ensure perfect interoperability across the application.
3. **Coder Agent:** A tool-using ReAct (Reasoning and Action) loop that safely handles execution. It reads existing context, uses dedicated tools to perform write operations, and programmatically manages media downloads.

## 🛠️ Tech Stack & Environment
- **Orchestration Framework:** LangGraph, LangChain
- **Language Models:** Groq API Client (Optimized for Llama-3/Mixtral structures)
- **Package Manager:** `uv` by Astral (Lightning-fast Python environment isolation)
- **Target Outputs:** Semantic HTML5, Responsive CSS3 (including print-friendly layouts), and Vanilla JavaScript (ES6+)

## 🚀 Key Technical Challenges Solved

### 1. Robust State Isolation and Reduction
Managed sequential workflow pipeline progression without mutating cross-node metadata or causing variable drift. By defining a strict `MasterGraphState` TypedDict schema mapping precise object instances (`Plan`, `Task`, and `dict[str, str]`), state context smoothly propagates linearly from `START` to `END` without data loss or graph interruptions.

### 2. Strict Schema Enforcement on LLM Infrastructure
Addressed potential structured parser validation breaks when using open-source models for multi-step tasks. Resolved this by chaining system configurations with `.with_structured_output()`, explicitly pairing strict system prompt constraints (banning markdown formatting, conversational filler, and empty boilerplate placeholders) directly with Pydantic class field descriptions.

### 3. File System Sandbox Traversal Prevention
Implemented secure execution layers for file mutations. Developed a centralized validation layer (`safe_path_for_project`) utilizing absolute path resolution and parent-relative tracking to prevent the agent from accidentally writing or reading files outside of the designated `generated_project/` folder path.

## 💻 Local Setup (Powered by UV)

Ensure you have `uv` installed. Clone the repository and spin up the environment with the following commands:

```bash
# Sync and activate the virtual environment
uv sync

# Duplicate the sample environment file to create your secret key file
cp .env.example .env

#Open your newly created .env file and insert your private Groq API key:
GROQ_API_KEY=your_actual_groq_api_key_here

#Run the application
uv run main.py
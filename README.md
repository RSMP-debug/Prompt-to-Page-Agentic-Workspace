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

### 1. State Mutability & Time-Travel Debugging
During initial builds, graph execution risked state corruption due to inline dictionary modifications. I implemented deep-copying configurations within the graph nodes (`coder_state = deepcopy(state.get("coder_state"))`) to protect historical states, ensuring compatibility with LangGraph's native time-travel debugging feature.

### 2. Schema Enforcement on Groq Open-Source Infrastructure
Faced API schema execution dropouts (`BadRequestError: 400`) due to models defaulting to markdown lists rather than structured schemas when `tool_choice` or structured output was required. Resolved this by refactoring system prompts to strictly ban conversational formatting, enforcing raw JSON/Pydantic property matching.

### 3. Eliminating Asset Hallucinations
Prevented the standard LLM "ghost asset" pattern (where the coder guesses local image names or points to broken external placeholders). Built a custom programmatic image downloader tool (`download_stock_image`) linked to a public API gateway and taught the Architect to explicitly budget downloading phases before code creation.

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
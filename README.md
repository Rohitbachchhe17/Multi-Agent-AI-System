# Multi-Agent-AI-System

A **CrewAI‑style** multi‑agent pipeline built with **Python** and **Streamlit**, featuring a premium dark‑theme UI, live progress badges, and secure API handling.

---

## Table of Contents
1. [Features](#features)
2. [Demo](#demo)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the App](#running-the-app)
7. [Project Structure](#project-structure)
8. [Agents Overview](#agents-overview)
9. [Customising the UI](#customising-the-ui)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Features
- **Three specialised agents**
  - `ResearchBot` – gathers raw knowledge & data.
  - `AnalystBot` – extracts insights, patterns, SWOT.
  - `WriterBot` – produces a polished final document.
- **Dynamic API key handling** via `.env` (no hard‑coded secrets).
- **Live progress UI** with glass‑morphism cards, badge states (`IDLE`, `RUNNING`, `DONE`).
- **High‑contrast dark theme** using the `Outfit` font, animated gradient background, and solid dark input fields.
- **Downloadable results** (Markdown & JSON).
- **Extensible** – add new agents, output formats, or pipeline steps with minimal code changes.

---

## Demo
<p align="center">
  <img src="https://i.imgur.com/9vE3wX8.png" alt="Demo screenshot" width="80%" />
</p>

---

## Architecture
```
┌─────────────────────┐     ┌─────────────────────┐
│   Streamlit UI       │     │   agents.py (logic) │
│   – app.py          │<───▶│   – get_client()    │
│   – CSS, layout     │     │   – Agent classes   │
└─────────────────────┘     └─────────────────────�n    │                               │
    │   env variable (OPENROUTER_API_KEY)
    ▼                               ▼
 OpenRouter API  ◀─────────────────────► LLM calls
```
- **`app.py`** – UI, CSS, input handling, phase orchestration.
- **`agents.py`** – Base `Agent` class, concrete bots, lazy client getter.
- **`.env`** – Stores `OPENROUTER_API_KEY`.
- **`requirements.txt`** – Dependencies (`streamlit`, `openai`, `python‑dotenv`, …).

---

## Installation
```bash
# Clone the repository (or copy the folder)
git clone https://github.com/youruser/multi-agent-system.git
cd multi-agent-system

# Optional: create a virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration
Create a `.env` file in the project root:
```text
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
```
> **Security tip:** Add `.env` to `.gitignore` if you push the repo publicly.

---

## Running the App
```bash
streamlit run app.py
```
Navigate to the URL shown in the console (usually `http://localhost:8501`).
1. **Enter your OpenRouter API key** (or rely on the `.env` value).
2. **Provide a research topic** (or click one of the quick‑topic buttons).
3. Click **🚀 Launch Crew**.
4. Watch the three phases progress (Research → Analysis → Writing).
5. Download the final markdown or the full JSON report.

---

## Project Structure
```
multi_agent_system/
│
├─ app.py            # Streamlit UI, CSS, orchestration
├─ agents.py         # Agent classes, lazy OpenAI client getter
├─ .env              # OpenRouter API key (not tracked in git)
├─ requirements.txt  # Python dependencies
└─ README.md         # This file
```

---

## Agents Overview
| Agent | Role | Prompt snippet |
|-------|------|----------------|
| **ResearchBot** | Gather comprehensive facts, data, trends | `Research the following topic thoroughly: '{topic}'` |
| **AnalystBot**  | Extract insights, patterns, SWOT | `Analyze the research on '{topic}': …` |
| **WriterBot**   | Produce a polished output | `Write a polished {output_format} on '{topic}' using the research and analysis.` |

---

## Customising the UI
All CSS lives in the `<style>` block at the top of `app.py`. You can:
- Adjust the gradient colors or animation speed.
- Change font families (Google Fonts import is already present).
- Modify card hover effects, badge colors, or input styling.
- Add additional CSS variables for easy theme tweaks.

---

## Troubleshooting
- **API key errors** – Ensure the key is present in `.env` or entered in the sidebar. Verify the key works on the OpenRouter dashboard.
- **Dependency issues** – Run `pip install -r requirements.txt` inside the virtual environment.
- **UI not loading** – Check that `streamlit` is up‑to‑date (`pip install --upgrade streamlit`).
- **Slow responses** – Adjust `max_tokens` or `temperature` in `agents.py` to reduce token usage.

---

## License
This project is licensed under the MIT License. Feel free to fork, modify, and use it in your own projects.

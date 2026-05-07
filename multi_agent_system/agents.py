"""
Multi-Agent System - CrewAI Style
Agents: Research → Analyst → Writer
Flow: Plan → Execute → Review
"""

import os
import time
import json
from dataclasses import dataclass, field
from typing import Optional
from openai import OpenAI

# Auto-load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── OpenRouter Client (lazy — always reads latest env var) ─────────────────
def get_client() -> OpenAI:
    """Return a fresh OpenAI client using the current API key."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to .env or enter it in the sidebar."
        )
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

MODEL = "openai/gpt-4o-mini"   # change to any OpenRouter model


# ─── Agent Base ───────────────────────────────────────────────────────────────
@dataclass
class AgentResult:
    agent_name: str
    role: str
    task: str
    output: str
    status: str = "done"
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):
        return {
            "agent_name": self.agent_name,
            "role": self.role,
            "task": self.task,
            "output": self.output,
            "status": self.status,
            "timestamp": self.timestamp,
        }


class BaseAgent:
    def __init__(self, name: str, role: str, goal: str, backstory: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def _system_prompt(self) -> str:
        return (
            f"You are {self.name}, a {self.role}.\n"
            f"Your Goal: {self.goal}\n"
            f"Backstory: {self.backstory}\n\n"
            "Always be concise, structured, and professional. "
            "Use markdown formatting where helpful (bullet points, headers, bold text)."
        )

    def run(self, task: str, context: str = "") -> AgentResult:
        user_msg = task
        if context:
            user_msg = f"Context from previous agents:\n{context}\n\nYour Task:\n{task}"

        response = get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        output = response.choices[0].message.content.strip()
        return AgentResult(
            agent_name=self.name,
            role=self.role,
            task=task,
            output=output,
        )


# ─── Specialized Agents ───────────────────────────────────────────────────────

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="🔍 ResearchBot",
            role="Senior Research Specialist",
            goal="Gather comprehensive, accurate, and well-structured information on any given topic",
            backstory=(
                "You are a world-class researcher with expertise in quickly scanning "
                "complex topics, identifying key facts, trends, and data points. "
                "You synthesize information from multiple domains and present it in a clear, "
                "organized manner for further analysis."
            ),
        )


class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="📊 AnalystBot",
            role="Senior Data & Strategy Analyst",
            goal="Analyze research findings, identify patterns, insights, and strategic implications",
            backstory=(
                "You are a sharp analytical mind with expertise in breaking down complex data, "
                "spotting trends, and drawing actionable insights. You transform raw research "
                "into structured analysis with clear pros/cons, risk assessments, and "
                "strategic recommendations."
            ),
        )


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="✍️ WriterBot",
            role="Expert Content Strategist & Writer",
            goal="Transform research and analysis into compelling, polished written content",
            backstory=(
                "You are a seasoned writer and communicator who excels at turning complex "
                "technical analysis into clear, engaging, and professional content. "
                "You structure narratives logically, use persuasive language, and tailor "
                "output for the intended audience."
            ),
        )


# ─── Crew Orchestrator ────────────────────────────────────────────────────────

class Crew:
    """Orchestrates agents in a Plan → Execute → Review pipeline."""

    def __init__(self):
        self.researcher = ResearchAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.results: list[AgentResult] = []

    def kickoff(self, topic: str, output_format: str = "report") -> list[AgentResult]:
        """Run the full pipeline: Research → Analysis → Writing."""
        self.results = []

        # ── PHASE 1: Research ─────────────────────────────────────────────────
        research_task = (
            f"Research the following topic thoroughly: '{topic}'\n\n"
            "Provide:\n"
            "1. **Overview** – What is this topic about?\n"
            "2. **Key Facts & Data** – Important statistics, dates, figures\n"
            "3. **Current Trends** – What's happening now?\n"
            "4. **Key Players/Concepts** – Who or what matters most?\n"
            "5. **Open Questions** – What needs deeper analysis?"
        )
        r1 = self.researcher.run(research_task)
        self.results.append(r1)

        # ── PHASE 2: Analysis ─────────────────────────────────────────────────
        analysis_task = (
            f"Analyze the research on '{topic}' and provide:\n\n"
            "1. **Key Insights** – What does the data really tell us?\n"
            "2. **Patterns & Trends** – Identify any patterns\n"
            "3. **SWOT Analysis** – Strengths, Weaknesses, Opportunities, Threats\n"
            "4. **Strategic Implications** – What should stakeholders do?\n"
            "5. **Conclusion** – Your analytical verdict in 2–3 sentences"
        )
        r2 = self.analyst.run(analysis_task, context=r1.output)
        self.results.append(r2)

        # ── PHASE 3: Writing ──────────────────────────────────────────────────
        writing_task = (
            f"Write a polished {output_format} on '{topic}' based on the research and analysis.\n\n"
            "Requirements:\n"
            "- Engaging title and introduction\n"
            "- Well-structured body with clear sections\n"
            "- Professional yet accessible tone\n"
            "- Actionable takeaways or conclusion\n"
            "- Ready for publication/presentation"
        )
        context = f"RESEARCH:\n{r1.output}\n\nANALYSIS:\n{r2.output}"
        r3 = self.writer.run(writing_task, context=context)
        self.results.append(r3)

        return self.results

    def to_json(self) -> str:
        return json.dumps([r.to_dict() for r in self.results], indent=2)

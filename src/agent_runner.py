import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except Exception:  # pragma: no cover - PyYAML may not be installed
    yaml = None
from pydantic import BaseModel, Field

try:
    import openai
except Exception:  # pragma: no cover - openai may not be installed in tests
    openai = None

from .prompts import PROMPT_TEMPLATES
from .tools import load_tool, Tool


class ToolSpec(BaseModel):
    type: str
    description: Optional[str] = None


class StepSpec(BaseModel):
    role: str
    model: Optional[str] = None
    tool: Optional[str] = None


class AgentSpec(BaseModel):
    llm: Dict[str, Any] = Field(default_factory=dict)
    retry: int = 1
    tools: Dict[str, ToolSpec] = Field(default_factory=dict)
    steps: List[StepSpec]


class AgentRunner:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec = self._load_spec(self.spec_path)
        self.tools: Dict[str, Tool] = {
            name: load_tool(tool_spec.type)
            for name, tool_spec in self.spec.tools.items()
        }

    def _load_spec(self, path: Path) -> AgentSpec:
        data = path.read_text()
        if path.suffix in {".yml", ".yaml"}:
            if not yaml:
                raise RuntimeError("PyYAML is required to load YAML specs")
            parsed = yaml.safe_load(data)
        else:
            parsed = json.loads(data)
        return AgentSpec(**parsed)

    def _call_llm(self, model: str, prompt: str) -> str:
        retries = self.spec.retry
        last_err = None
        for _ in range(retries):
            try:
                if openai and os.getenv("OPENAI_API_KEY"):
                    resp = openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message["content"].strip()
                else:
                    return f"[Mock response from {model} for prompt: {prompt[:50]}...]"
            except Exception as e:  # pragma: no cover - network errors not testable
                last_err = e
                time.sleep(1)
        raise RuntimeError(f"LLM call failed after {retries} attempts: {last_err}")

    def run(self, user_input: str) -> (str, List[Dict[str, Any]]):
        context = user_input
        trace = []
        for step in self.spec.steps:
            start = time.time()
            if step.tool:
                tool = self.tools.get(step.tool)
                if not tool:
                    raise ValueError(f"Tool '{step.tool}' not found")
                output = tool.run(context)
                prompt = None
            else:
                model = step.model or self.spec.llm.get("default_model", "gpt-3.5-turbo")
                template = PROMPT_TEMPLATES.get(step.role, "{input}")
                prompt = template.format(input=context)
                output = self._call_llm(model, prompt)
            end = time.time()
            trace.append(
                {
                    "role": step.role,
                    "prompt": prompt,
                    "output": output,
                    "runtime": round(end - start, 2),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            context = output
        return context, trace

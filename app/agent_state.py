# app/state.py

from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    task: str

    messages: list[dict[str, Any]] = Field(default_factory=list)
    #messages is a list of elements where each element is a dictionary with string keys and values of any type. The default value is an empty list.
    iteration: int = Field(default=0, ge=0)

    status: Literal[
        "ready",
        "running",
        "completed",
        "failed",
        "max_iterations"
    ] = "ready"

    final_answer: str | None = None

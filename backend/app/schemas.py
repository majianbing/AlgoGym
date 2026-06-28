from datetime import date, datetime

from pydantic import BaseModel, Field


class ProblemOut(BaseModel):
    id: int
    title: str
    leetcode_url: str
    pattern: str
    difficulty: str
    week: int
    day: int
    prompt: str

    model_config = {"from_attributes": True}


class SessionOut(BaseModel):
    id: int
    date: date
    problem_id: int
    status: str
    time_spent_mins: int
    notes: str
    hint_level_used: int
    review_due: date | None

    model_config = {"from_attributes": True}


class DocumentOut(BaseModel):
    id: int
    filename: str
    chunked: bool
    embedded: bool
    chunks_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StartSessionRequest(BaseModel):
    problem_id: int


class FinishSessionRequest(BaseModel):
    status: str = Field(pattern="^(solved|failed)$")
    time_spent_mins: int = Field(default=0, ge=0)
    notes: str = ""
    hint_level_used: int = Field(default=0, ge=0, le=3)


class HintRequest(BaseModel):
    problem_id: int | None = None
    problem: str = ""
    current_attempt: str = ""
    level: int = Field(default=1, ge=1, le=3)
    unlock_solution: bool = False


class SettingsPayload(BaseModel):
    ollama_base_url: str | None = None
    llm_model: str | None = None
    embedding_model: str | None = None
    api_key: str | None = None


class PlanGenerateRequest(BaseModel):
    goal: str = "Build a 6-week interview algorithm habit"

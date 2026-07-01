from pydantic import BaseModel, Field,ConfigDict
from typing import TypedDict,Optional

from pydantic import BaseModel, Field, ConfigDict


class File(BaseModel):
    file: str = Field(
        description="File name."
    )
    purpose: str = Field(
        description="Purpose of the file."
    )


class Plan(BaseModel):
    title: str = Field(
        description="Project title."
    )
    description: str = Field(
        description="Short project summary."
    )
    tech_stack: list[str] = Field(
        description="Technologies used."
    )
    features: list[str] = Field(
        description="Main features."
    )
    files: list[File] = Field(
        description="Project files."
    )


class Implementation(BaseModel):
    file_path: str = Field(
        description="Target file."
    )
    implementation_task: str = Field(
        description="Task to implement in detail steps with same names for var,functions,classes if necessary."
    )


class Task(BaseModel):
    implementation_steps: list[Implementation] = Field(
        description="Implementation steps."
    )

    model_config = ConfigDict(extra="ignore")


class MasterGraphState(TypedDict):
    user_prompt: str
    plan: Optional[Plan]
    task_plan: Optional[Task]
    generated_files: Optional[dict[str, str]]

from pydantic import BaseModel
from typing import TypedDict


class Blog(BaseModel):
    title: str
    content: str


class State(TypedDict):
    blog: Blog
    topic: str
    language: str

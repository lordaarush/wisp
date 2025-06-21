from pydantic import BaseModel

class PollCreate(BaseModel):
    question: str
    option_a: str
    option_b: str

class Vote(BaseModel):
    option: str  # must be "a" or "b"

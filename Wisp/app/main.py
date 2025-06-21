from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict
from uuid import uuid4
import random
from app.models import PollCreate, Vote

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory poll storage
polls: Dict[str, dict] = {}

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("static/wisp.html", "r") as f:
        return f.read()

@app.post("/api/create")
def create_poll(data: PollCreate):
    poll_id = str(uuid4())[:8]
    polls[poll_id] = {
        "question": data.question,
        "a": data.option_a,
        "b": data.option_b,
        "votes": {"a": 0, "b": 0}
    }
    return {"poll_id": poll_id}

@app.get("/api/poll/random")
def get_random_poll():
    if not polls:
        raise HTTPException(404, "No polls available.")
    poll_id = random.choice(list(polls.keys()))
    return {"poll_id": poll_id, **polls[poll_id]}

@app.get("/api/poll/{poll_id}")
def get_poll(poll_id: str):
    if poll_id not in polls:
        raise HTTPException(404, "Poll not found.")
    return polls[poll_id]

@app.post("/api/poll/{poll_id}/vote")
def vote_poll(poll_id: str, vote: Vote):
    if poll_id not in polls or vote.option not in ("a", "b"):
        raise HTTPException(400, "Invalid vote or poll.")
    polls[poll_id]["votes"][vote.option] += 1
    return {"votes": polls[poll_id]["votes"]}

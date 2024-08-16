from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    Pose: str

class Scoreboard(BaseModel):
    username: str
    score: float
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    Pose: str

class Spawn(BaseModel):
    Object: str

class Scoreboard(BaseModel):
    username: str
    score: float
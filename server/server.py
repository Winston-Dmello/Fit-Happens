import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from database import DB

db = DB()

class Message(BaseModel):
    Pose: str

class Scoreboard(BaseModel):
    username: str
    score: float


app = FastAPI()

global msg
msg = None

@app.websocket("/ws")
async def web_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            global msg
            if msg:
                data = {"Pose":msg}
                print(data)
                await websocket.send_json(data)
                msg = None
            try:
                # Use a non-blocking receive with a timeout
                await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            except asyncio.TimeoutError:
                pass 
    except WebSocketDisconnect:
        print("Connection disconnected")

@app.post("/message")
async def sreceive(message: Message):
    global msg
    msg = message.Pose
    print(msg)
    try:
        return {"status": "Message sent", "message": message}
    except Exception as e:
        raise HTTPException(statuscode=500, detail=str(e))


@app.post("/scoreboard")
async def postscoreboard(Score: Scoreboard):
    db.insert_score(Score.username, Score.score)

    return {"status": "Score added"}

@app.get("/scoreboard")
async def getscoreboard():
    
    data = db.get_scoreboard()
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8000)
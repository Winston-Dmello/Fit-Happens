import asyncio
from fastapi import FastAPI, Form, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from models import *
from database import DB

db = DB()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)

    if db.user_exists(user.username):
        if db.login_user(user.username, user.password):
            return JSONResponse({"success":"true"})
        else:
            raise HTTPException(status_code=411, detail="Incorrect Password")
    else:
        try:
            db.create_user(user.username, user.password)
            return JSONResponse({"success":"true"})
        except:
            raise HTTPException(status_code=500, detail="Failed to create user")


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
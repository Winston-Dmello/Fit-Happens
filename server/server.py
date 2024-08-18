import asyncio
from fastapi import FastAPI, Form, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import subprocess


from models import *
from database import DB
from analysis import analyse_runs

db = DB()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

run = {}

global msg
msg = None

global spawn
spawn = None

@app.websocket("/ws")
async def web_endpoint(websocket: WebSocket):
    await websocket.accept()
    process = subprocess.Popen(["python3.10", "../MrPose/mrpose.py", "-v", "/dev/video1"])
    run["Dodge"] = 0
    run["JumpingJack"] = 0
    run["Squat"] = 0
    try:
        while True:
            global msg
            if msg:
                if msg in run:
                    run[msg] += 1
                else:
                    run["Dodge"] += 1
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
    if process:
        process.kill()

@app.websocket("/ws2")
async def web_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            global spawn
            if spawn:
                data = {"Spawn":spawn}
                print(data)
                await websocket.send_json(data)
                print("sent successfully!")
                spawn = None
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

@app.get("/load_start_game", response_class=HTMLResponse)
async def load_start_game(request: Request):
    return templates.TemplateResponse("startGame.html", {"request": request})

@app.get("/load_analysis", response_class=HTMLResponse)
async def load_analysis(request: Request):
    some_value = analyse_runs(run["Username"])
    return templates.TemplateResponse("Analysis.html", {"request": request, "some_value":some_value})

@app.get("/load_about_us", response_class=HTMLResponse)
async def load_about_us(request: Request):
    return templates.TemplateResponse("Aboutus.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)

    if db.user_exists(user.username):
        if db.login_user(user.username, user.password):
            run["Username"] = user.username
            return RedirectResponse(url="/dashboard", status_code=302)
        else:
            return templates.TemplateResponse("home.html",{"request":request,"error_message":"Incorrect Password"})
    else:
        try:
            db.create_user(user.username, user.password)
            run["Username"] = user.username
            return RedirectResponse(url="/dashboard", status_code=302)
        except:
            return templates.TemplateResponse("home.html", {"request":request, "error_message":"Failed to create user"})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request":request})

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
    run["Score"] = Score.score
    print(run)
    db.insert_run(run)
    return {"status": "Score added"}

@app.get("/scoreboard")
async def getscoreboard():
    
    data = db.get_scoreboard()
    return JSONResponse(content=data)


@app.post("/spawn")
async def create(sp: Spawn):
    global spawn
    spawn = sp.Object
    try:
        return {"status": "Spawn added"}
    except Exception as e:
        raise HTTPException(statuscode=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8000)
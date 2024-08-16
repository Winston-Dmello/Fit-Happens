from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from test1 import generate_pie_chart

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = [50, 30, 20, 10]
    labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
    pie_chart = generate_pie_chart(data, labels)
    return templates.TemplateResponse("test3.html", {"request": request, "pie_chart": pie_chart})

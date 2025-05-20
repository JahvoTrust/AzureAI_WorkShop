from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import os
from pydantic import BaseModel
import json


app = FastAPI(title="Prompt Flow Search API")

# Jinja2 템플릿 경로 설정 (templates 폴더 기준)
templates = Jinja2Templates(directory="templates")


# 환경변수
url = ""
api_key = ""


class QueryRequest(BaseModel):
    Query: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask")
def ask(request_data: QueryRequest):
    data = {'Query': request_data.Query}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    try:
        req = requests.post(url, headers=headers, json=data)
        req.raise_for_status()
        return {"answer": req.json()}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8888)

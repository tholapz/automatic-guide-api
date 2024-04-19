from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Item import Item
from ModelEnum import ModelEnum
from llm import populate_payload
import requests
from typing import Dict
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/items/')
async def create_item(item: Item):
    headers = {
        'Content-Type': 'application/json'
    }
    if item.mode == ModelEnum.openai:
        url = 'https://api.openai.com/v1/chat/completions'
        headers['Authorization'] = f'Bearer {os.environ["OPENAI_API_KEY"]}'
    elif item.mode == ModelEnum.gorilla:
        url = 'http://34.132.127.197:8000/v1'
        headers['Authorization'] = 'Bearer EMPTY'
    else:
        url = 'http://192.168.0.12:11434/api/generate'
    try:
        response = requests.post(
            url,
            json = populate_payload(item),
            headers = headers
        )
        return response.json()
    except Exception as e:
        return f'Error: {e}'
    

app.mount('/static', StaticFiles(directory='static'), name='static')
import time
from fastapi import FastAPI
from Item import Item
from ModelEnum import ModelEnum
from llm.populate_payload import templates, populate_payload
import requests
import os
from dotenv import load_dotenv, find_dotenv
import json

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
    if item.model == ModelEnum.openai:
        url = 'https://api.openai.com/v1/chat/completions'
        headers['Authorization'] = f'Bearer {os.environ["OPENAI_API_KEY"]}'
    elif item.model == ModelEnum.gorilla:
        url = f'http://{os.environ["GORILLA_HOST"]}:8000/v1'
        headers['Authorization'] = 'Bearer EMPTY'
    else:
        url = f'http://{os.environ["OLLAMA_HOST"]}:11434/api/generate'
    try:
        html_form = requests.get(item.url).text
        response1 = requests.post(
            url,
            json = populate_payload(item, templates[0].replace('[HTML_FORM]', html_form)),
            headers = headers
        )
        json_object = response1.json()['response'].strip()
        # otherwise, ollama will just crash... :p
        time.sleep(5)
        response = requests.post(
            url,
            json = populate_payload(item, templates[1].replace('[MESSAGE]', item.prompt).replace('[JSON_OBJECT]', json_object)),
            headers = headers
        )
        return json.loads(response.json()['response'].strip())
    except Exception as e:
        return f'Error: {e}'

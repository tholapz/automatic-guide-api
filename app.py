from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from enum import Enum
from llm.ollama import ollama
from llm.gorilla import get_gorilla_response


class ModeEnum(str, Enum):
    openai='openai'
    gorilla='gorilla'
    mistral='mistral'
    llama3='llama3'
    mixtral='mixtral'
    wizardlm2='wizardlm2'
    drbx='drbx'
    gemma='gemma'
    llama2='llama2'

class Item(BaseModel):
    url: str
    prompt: str
    mode: ModeEnum = ModeEnum.openai

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    # if item.mode == ModeEnum.openai:
        # return openai(url=item.url, prompt=item.prompt)
    # elif item.mode == ModeEnum.gorilla:
        # return get_gorilla_response(url=item.url, prompt=item.prompt)
    return ollama(url=item.url, userInput=item.prompt, model=item.mode)

app.mount("/static", StaticFiles(directory="static"), name="static")
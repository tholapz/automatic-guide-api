import requests

def ollama(url, userInput, model):
    # with open("prompt.txt", "r") as prompt_file:
    prompt_template = """
Description:
You have received a message containing various pieces of information that need to be filled into an HTML form. Your task is to extract the relevant data from the message and populates the corresponding fields in the HTML form.

Message:
[MESSAGE]

HTML Form:
[HTML_FORM]

Criteria for Success:
Ensure each fields are populated correctly
Respond in JSON
"""
    pageContent = requests.get(url=url).content
    prompt = prompt_template.replace('[MESSAGE]', userInput).replace('[HTML_FORM]', pageContent)
    data = {
        "model": f"{model}:latest",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    response = requests.post(url="http://192.168.0.12:11434/api/generate", json=data)
    return response.json()

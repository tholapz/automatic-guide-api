from openai import OpenAI
import requests

client = OpenAI()

def openai(url, prompt):
    with open("prompt.txt", "r") as prompt_file:
        prompt_template = prompt_file.read()
    pageContent = requests.get(url=url).content
    content = prompt_template.replace('[MESSAGE]', prompt).replace('[HTML_FORM]', pageContent)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content
from openai import OpenAI
import requests
from Item import Item
from llm.populate_payload import templates
import json

client = OpenAI()

def invoke_openai(item: Item):
    print('invoke openai')
    try:
        html_form = requests.get(item.url).text
        content = templates[2].replace('[HTML_FORM]', html_form).replace('[MESSAGE]', item.prompt)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You have received a message containing various pieces of information that need to be filled into an HTML form. Your task is to extract the relevant data from the message and populates the corresponding fields in the HTML form."},{"role": "user", "content": content}]
            )
        print(completion.choices[0].message.content.replace('```json','').replace('```', ''))
        return json.loads(completion.choices[0].message.content.replace('```json','').replace('```', ''))
    except Exception as e:
        return f'Error: {e}'

import requests
from Item import Item
from ModelEnum import ModelEnum

template = """
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

def populate_payload(item: Item):
    payload = { 'model': item.model }

    html_form = requests.get(item.url).content

    content = template.replace('[MESSAGE]', item.prompt).replace('[HTML_FORM]', html_form)

    if item.model == ModelEnum.openai | item.model == ModelEnum.gorilla:
        payload['messages'] = [
            {
                'role': 'user',
                'content': content
            }
        ]
    else:
        payload['prompt'] = content
        payload['format'] = 'json'
        payload['stream'] = False

    return payload
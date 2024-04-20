import requests
from Item import Item
from ModelEnum import ModelEnum

templates = [
    """Takes an HTML form as input and returns a JSON object containing key-value pairs for each input field. The key should be the name of the field, and the value should be a string describing that field.

**Example Input HTML Form:**

```html
<form>
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" placeholder="Enter your username">

    <label for="password">Password:</label>
    <input type="password" id="password" name="password" placeholder="Enter your password">

    <label for="email">Email:</label>
    <input type="email" id="email" name="email" placeholder="Enter your email">

    <input type="submit" value="Submit">
</form>
```

**Example Output JSON:**

```json
{
    "username": "Text input field for the user's username",
    "password": "Password input field for the user's password",
    "email": "Email input field for the user's email"
}
```

Here is the HTML Form:
```html
[HTML_FORM]
```""",
"""
Description:
You are tasked with extracting specific pieces of information from a message provided by a user. Along with the message, a JSON object will be provided outlining the names of each piece of information to be extracted. Your task is to create the JSON object according to the provided specifications.

Message:
[MESSAGE]

JSON Object:
[JSON_OBJECT]

Criteria for Success:
Ensure each fields are populated correctly
Respond in JSON
""",
"""
Message:
[MESSAGE]

HTML Form:
[HTML_FORM]

Criteria for Success:
Ensure each fields are populated correctly
Respond in JSON
"""
]

def populate_payload(item: Item, content):
    payload = { 'model': item.model }

    if item.model == ModelEnum.openai or item.model == ModelEnum.gorilla:
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
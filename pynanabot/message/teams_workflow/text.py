import requests
import json

def teams_text_message(url: str, message: str):
    headers = {"Content-Type": "application/json"}

    data = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": message,
                "wrap": True,
            }
        ],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

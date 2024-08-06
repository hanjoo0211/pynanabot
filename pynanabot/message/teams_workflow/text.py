import requests
import json

def teams_text_message(url: str, message: str):
    headers = {"Content-Type": "application/json"}

    data = {
        "type": "messageCard",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True,
                        }
                    ],
                },
            }
        ],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

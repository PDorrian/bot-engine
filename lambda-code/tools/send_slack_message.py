import requests

import lambda_function


class send_slack_message:
    @staticmethod
    def run(instance, product, quantity, price):
        url = lambda_function.response['send_slack_endpoint']
        payload = {
            "Message": f"Deal finalised with {lambda_function.email_address} for {quantity} {product} at {price} euro each.",
        }
        response = requests.post(url, json=payload)
        return response

    description = {
        "type": "function",
        "function": {
            "name": "send_slack_message",
            "description": "Notify the Slack channel that a deal has been finalised with details of the deal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product being sold. e.g. 'guest posts'"
                    },
                    "quantity": {
                        "type": "number",
                        "description": "The quantity of the product being sold."
                    },
                    "price": {
                        "type": "number",
                        "description": "The price of the product."
                    }
                },
                "required": ["product", "quantity", "price"]
            }
        }
    }
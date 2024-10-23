import lambda_function


class send_notification:
    @staticmethod
    def run(instance, message):
        print('send_notification triggered')
        lambda_function.response['notification_message'] = message

    description = {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Send a notification message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to be sent."
                    }
                },
                "required": ["message"]
            }
        }
    }

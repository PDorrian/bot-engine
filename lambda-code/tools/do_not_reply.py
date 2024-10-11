import lambda_function


class do_not_reply:
    @staticmethod
    def run(instance):
        lambda_function.response['do_reply'] = False

    description = {
        "type": "function",
        "function": {
            "name": "do_not_reply",
            "description": "Prevents a response from being sent to the sender.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

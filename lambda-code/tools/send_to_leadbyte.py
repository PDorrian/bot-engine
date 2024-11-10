import lambda_function


class send_to_leadbyte:
    @staticmethod
    def run(instance):
        lambda_function.response['send_to_leadbyte'] = True

    description = {
        "type": "function",
        "function": {
            "name": "send_to_leadbyte",
            "description": "Send a client to Leadbyte.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

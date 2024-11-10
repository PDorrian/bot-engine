import lambda_function


class send_to_do_not_contact:
    @staticmethod
    def run(instance):
        lambda_function.response['do_not_contact'] = True

    description = {
        "type": "function",
        "function": {
            "name": "send_to_do_not_contact",
            "description": "Send a client to the 'Do not contact' list.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

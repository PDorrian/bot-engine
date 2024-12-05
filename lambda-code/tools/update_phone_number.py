import lambda_function


class update_phone_number:
    @staticmethod
    def run(instance, phone_number):
        lambda_function.response['phone_number'] = phone_number

    description = {
        "type": "function",
        "function": {
            "name": "update_phone_number",
            "description": "Update the user's phone number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {
                        "type": "string",
                        "description": "The phone number of the user."
                    }
                },
                "required": ["phone_number"]
            }
        }
    }

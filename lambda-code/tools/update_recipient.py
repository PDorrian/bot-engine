import lambda_function


class update_recipient:
    @staticmethod
    def run(instance, new_recipient):
        lambda_function.response['email_address'] = new_recipient
        return f'Sending email to {new_recipient}'

    description = {
        "type": "function",
        "function": {
            "name": "update_recipient",
            "description": "Change the recipient of your email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_recipient": {
                        "type": "string",
                        "description": "The email address that will receive your email."
                    }
                },
                "required": ["new_recipient"]
            }
        }
    }

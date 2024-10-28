import lambda_function


class send_invoice:
    @staticmethod
    def run(instance, company_name, email_address, country, product, quantity, unit_price, email_body, thread_id, discount_percent=0, address_line_1='', city='', tax_number=''):
        print('send_invoice triggered')

        payload = {
            "Company Name": company_name,
            "Email Address": email_address,
            "Country": country,
            "Product": product,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Discount %": discount_percent,
            "Address Line 1": address_line_1,
            "City": city,
            "Tax Number": tax_number,
            "Email Body": email_body,
            "Thread ID": thread_id
        }
        lambda_function.response['invoice'] = payload

    description = {
        "name": "send_invoice",
        "description": "Send an invoice from the accounts department.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The name of the company to send the invoice to"
                },
                "email_address": {
                    "type": "string",
                    "description": "The email address of the company to send the invoice to"
                },
                "country": {
                    "type": "string",
                    "description": "The country of the company to send the invoice to"
                },
                "product": {
                    "type": "string",
                    "description": "The product to invoice (e.g. 'Guest Post')"
                },
                "quantity": {
                    "type": "number",
                    "description": "The quantity of the product to invoice"
                },
                "unit_price": {
                    "type": "number",
                    "description": "The unit price of the product to invoice"
                },
                "discount_percent": {
                    "type": "number",
                    "description": "The discount percentage to apply to the invoice (optional)"
                },
                "address_line_1": {
                    "type": "string",
                    "description": "The address line 1 of the company to send the invoice to (optional)"
                },
                "city": {
                    "type": "string",
                    "description": "The city of the company to send the invoice to (optional)"
                },
                "tax_number": {
                    "type": "string",
                    "description": "The tax number of the company to send the invoice to (optional)"
                },
                "email_body": {
                    "type": "string",
                    "description": "The email body of the email that will accompany the invoice"
                }
            },
            "required": [
                "company_name",
                "email_address",
                "country",
                "product",
                "quantity",
                "unit_price"
            ]
        }
    }

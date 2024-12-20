import os

from openai import OpenAI

from thread import Thread
from utils.aws import read_file_from_s3

from tools.send_notification import send_notification
from tools.do_not_reply import do_not_reply
from tools.update_recipient import update_recipient
from tools.send_invoice import send_invoice
from tools.send_to_do_not_contact import send_to_do_not_contact
from tools.send_to_leadbyte import send_to_leadbyte
from tools.update_phone_number import update_phone_number


client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))


def lambda_handler(event, _):
    global response
    response = event
    
    tools = {
        'send_notification': send_notification,
        'send_invoice': send_invoice,
        'do_not_reply': do_not_reply,
        'update_recipient': update_recipient,
        'send_to_do_not_contact': send_to_do_not_contact,
        'send_to_leadbyte': send_to_leadbyte,
        'update_phone_number': update_phone_number
    }
    
    selected_tools = event.get('tools', [])
    tools = {key:val for key,val in tools.items() if key in selected_tools} or None
    bucket = event['bucket']
    thread_id = event.get('thread_id')

    if thread_id is None or not Thread.exists(bucket, thread_id):
        thread = Thread(client, bucket, thread_id, tools=tools)
        role_prompt = read_file_from_s3(bucket, event.get('role_prompt_key', 'role_prompt.md'))
        thread.add_message({"role": "system", "content": role_prompt})
    else:
        thread = Thread.load(client, bucket, thread_id, tools=tools)
    
    if event.get('content') is not None:
        thread.add_message(event)
    
    outgoing_message = thread.run()
    response['response'] = outgoing_message
    response['do_reply'] = response.get('do_reply', thread.is_active)

    if thread_id is not None and response.get('save', True) and response['do_reply']:
        thread.save()

    return response

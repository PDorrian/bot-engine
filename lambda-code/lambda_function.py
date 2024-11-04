import os

from openai import OpenAI

from thread import Thread
from utils.aws import read_file_from_s3

from tools.send_notification import send_notification
from tools.do_not_reply import do_not_reply
from tools.update_recipient import update_recipient
from tools.send_invoice import send_invoice


client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))


def lambda_handler(event, _):
    global response
    response = event
    
    tools = {
        'send_notification': send_notification,
        'send_invoice': send_invoice,
        'do_not_reply': do_not_reply,
        'update_recipient': update_recipient
    }
    selected_tools = event.get('tools', [])
    tools = {key:val for key,val in tools.items() if key in selected_tools}

    bucket = event['bucket']
    incoming_message = event.get('message')
    role = event.get('role', 'user')
    thread_id = event.get('thread_id')

    if thread_id is None or not Thread.exists(bucket, thread_id):
        thread = Thread(client, bucket, thread_id, tools=tools)
        role_prompt = read_file_from_s3(bucket, event.get('role_prompt_key', 'role_prompt.md'))
        thread.add_message({"role": "system", "content": role_prompt})
    else:
        thread = Thread.load(client, bucket, thread_id, tools=tools)
    
    if incoming_message is not None:
        name = event.get('from_name')
        if name is not None:
            name = name.replace(' ', '_')
            name = ''.join(c for c in name if c.isalpha() or c.isdigit() or c=='_')
        thread.add_message({"role": role, "content": incoming_message, "name": name})
    
    outgoing_message = thread.run()
    if thread_id is not None and event.get('save_thread', True):
        thread.save()

    response['message'] = outgoing_message
    response['do_reply'] = response.get('do_reply', thread.is_active)

    return response

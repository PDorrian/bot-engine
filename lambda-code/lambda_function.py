import os

from openai import OpenAI

from thread import Thread
from utils.aws import read_file_from_s3

from tools.send_slack_message import send_slack_message
from tools.do_not_reply import do_not_reply
from tools.update_recipient import update_recipient


client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))


def lambda_handler(event, _):
    global response
    response = event
    
    tools = {
        'send_slack_message': send_slack_message,
        'do_not_reply': do_not_reply,
        'update_recipient': update_recipient
    }
    selected_tools = event.get('tools')
    tools = {key:val for key,val in tools.items() if key in selected_tools}

    bucket = event['bucket']
    incoming_message = event['message']
    role = event.get('role', 'user')
    thread_id = event.get('thread_id')

    role_prompt = read_file_from_s3(bucket, event.get('role_prompt_key', 'role_prompt.md'))

    if thread_id is None or not Thread.exists(bucket, thread_id):
        thread = Thread(client, bucket, thread_id, tools=tools)
        thread.add_message({"role": "system", "content": role_prompt})
    else:
        thread = Thread.load(client, bucket, thread_id, tools=tools)
    
    if incoming_message is not None:
        thread.add_message({"role": role, "content": incoming_message})
    
    outgoing_message = thread.run()
    if thread_id is not None:
        thread.save()

    response['message'] = outgoing_message
    response['do_reply'] = response.get('do_reply', thread.is_active)

    return response
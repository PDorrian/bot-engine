import os

from openai import OpenAI
from moto import mock_aws
import boto3

from utils.aws import write_file_to_s3
from lambda_function import lambda_handler


client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))




@mock_aws
def test_do_not_reply():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="role_prompt.md", Body=b"Your function calling capabilities are being tested.")

    event = {
        'bucket': 'test-bucket',
        'message': 'Use the do_not_reply tool.',
        'role': 'system',
        'tools': ['do_not_reply']
    }

    response = lambda_handler(event, None)

    assert response['do_reply'] is False


@mock_aws
def test_update_recipient():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="role_prompt.md", Body=b"Your function calling capabilities are being tested.")

    event = {
        'bucket': 'test-bucket',
        'message': 'Use the update_recipient tool to change the recipient to new@mail.com.',
        'role': 'system',
        'tools': ['update_recipient'],
        'email_address': 'old@mail.com'
    }

    response = lambda_handler(event, None)

    assert response['email_address'] == 'new@mail.com'

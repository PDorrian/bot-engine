from moto import mock_aws
import boto3

from utils.aws import read_file_from_s3, write_file_to_s3, file_exists_in_s3


@mock_aws
def test_read_file_from_s3():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")

    test_data = "test-data"
    s3.put_object(Bucket="test-bucket", Key="test-key", Body=test_data)

    data = read_file_from_s3("test-bucket", "test-key")
    assert data == test_data


@mock_aws
def test_write_file_to_s3():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")

    test_data = b"test-data"
    write_file_to_s3("test-bucket", "test-key", test_data)

    response = s3.get_object(Bucket="test-bucket", Key="test-key")
    data = response["Body"].read()
    assert data == test_data


@mock_aws
def test_file_exists_in_s3():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")

    assert not file_exists_in_s3("test-bucket", "test-key")

    test_data = b"test-data"
    s3.put_object(Bucket="test-bucket", Key="test-key", Body=test_data)

    assert file_exists_in_s3("test-bucket", "test-key")

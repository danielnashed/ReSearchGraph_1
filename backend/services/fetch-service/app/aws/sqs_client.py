import boto3
import os
from typing import Optional
from dotenv import load_dotenv

class SQSClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('AWS_SQS_CLUSTER_URL')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION')
        self.client = boto3.client(
            'sqs',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def send_message(self, message: dict):
        self.client.send_message(
            QueueUrl=self.url,
            MessageBody=str(message)
        )
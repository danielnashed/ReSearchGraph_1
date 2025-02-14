import boto3
import os
from typing import Optional
from dotenv import load_dotenv
import asyncio

class SQSClient:

    def __init__(self, url, process_message):
        load_dotenv()
        self.url = url
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION')
        self.client = boto3.client(
            'sqs',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
        self.process_message = process_message

    def send_message(self, message: dict):
        self.client.send_message(
            QueueUrl=self.url,
            MessageBody=str(message)
        )

    # async def poll_sqs(self):
    #     stop_polling = False
    #     while not stop_polling:
    #         stop_polling = await self._receive_message()

    async def poll_sqs(self):
        while True:
            await self._receive_message()
            asyncio.sleep(5)

    async def _receive_message(self) -> Optional[dict]:
        print(f"Polling {self.url}")
        response = self.client.receive_message(
            QueueUrl=self.url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )
        messages = response.get('Messages', [])
        if not messages:
            return False
        print(f"Received {len(messages)} messages from {self.url}")
        for message in messages:
            # Process the message
            await self.process_message(message)
            receipt_handle = message['ReceiptHandle']
            self._delete_message(receipt_handle)
        print(f"Finished processing all messages at {self.url}")
        return True
    
    def _delete_message(self, receipt_handle: str):
        self.client.delete_message(
            QueueUrl=self.url,
            ReceiptHandle=receipt_handle
        )
import boto3
import os
from typing import Optional
from dotenv import load_dotenv
import json

class BedrockClient:

    def __init__(self, model_id):
        load_dotenv()
        self.model_id = model_id
        self.client = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

    def invoke_model(self, body: dict):
        response = self.client.invoke_model(
            body=body, 
            modelId=self.model_id,
            accept = '*/*',
            contentType = 'application/json'
        )
        response_body = json.loads(response.get('body').read())
        return response_body
        


import boto3
import os
from typing import Optional
from dotenv import load_dotenv
import json

class EventBridgeClient:

    def __init__(self, rule, target):
        load_dotenv()
        self.rule = rule
        self.target = target
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION')
        self.client = boto3.client(
            'events',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def create_rule(self, schedule):
        # Create the rule
        self.client.put_rule(
            Name=self.rule,
            ScheduleExpression=schedule,
            State='DISABLED'
        )

        # Attach the API Destination as the target
        self.client.put_targets(
            Rule=self.rule,
            Targets=[self.target]
        )

    def enable_rule(self):
        self.client.enable_rule(Name=self.rule)

    def disable_rule(self):
        self.client.disable_rule(Name=self.rule)

    def delete_rule(self):
        self.client.remove_targets(Rule=self.rule, Ids=[self.target])
        self.client.delete_rule(Name=self.rule)

from dotenv import load_dotenv
import os

load_dotenv()
AWS_TARGET_ARN = os.getenv("AWS_TARGET_ARN")
AWS_TARGET_ROLE_ARN= os.getenv("AWS_TARGET_ROLE_ARN")

def create_target_for_user(user_id):
    target_name = f"FetchPapersScheduledTarget_{user_id}"
    target = {"Id": target_name,
              "Arn": AWS_TARGET_ARN,
              "RoleArn": AWS_TARGET_ROLE_ARN,
              "Input": f'{{ "user_id": "{user_id}" }}'
             }
    return target
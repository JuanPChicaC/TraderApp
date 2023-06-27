from boto3 import resource
from os import getenv



dynamodb = resource(
    "dynamodb",
    aws_access_key_id = getenv(
        "AWS_ACCESS_KEY_ID"
        ),
    aws_secret_access_key = getenv(
        "AWS_SECRET_ACCESS_KEY"
        ),
    region_name = getenv(
        "REGION_NAME"
        )
    )





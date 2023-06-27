from boto3 import resource
from os import getenv
from .common import get_db_tables_config
from .common import get_db_tables_config

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


def create_tables():
    try:
        for table in get_db_tables_config()["structure"]:
            dynamodb.create_table(
                **table
                )
    except Exception as e:
        print(e)




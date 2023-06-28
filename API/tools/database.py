from boto3 import resource
from os import getenv
from .common import get_db_tables_config
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Sequence
from datetime import datetime, timedelta

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

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date_from():
    current_time = datetime.now()
    year_ago = current_time - timedelta(days = 365)
    return year_ago.strftime("%Y-%m-%d")
    
def get_date_to():    
    return datetime.now().strftime("%Y-%m-%d") 


class DPortfolio(BaseModel):
    user:str
    portfolio:Optional[str]
    
class UPortfolio(DPortfolio):

    portfolio:str
    symbols_list:List[str]
    last_update_datetime:Optional[str] = Field(default_factory = now)
    multiplier:Optional[str] = "1"
    timespan:Optional[str] = "day"
    date_from:Optional[str] = Field(default_factory = get_date_from)
    date_to:Optional[str] =Field(default_factory =  get_date_to)

class CPortfolio(UPortfolio):
    
    creation_datetime:Optional[str] = Field(default_factory = now)




    





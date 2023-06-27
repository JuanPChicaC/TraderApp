import os
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(
          os.path.abspath(
              __file__
              )
          )
        )
    )

from operations.supplier import *
from fastapi import APIRouter
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io
from datetime import datetime
        
external_api = APIRouter()



@external_api.get(
    "/get_symbols_info"
    )
def get_symbols():
    arguments = locals()
    try:
        answer = get_symbols_information(
            **arguments
            )
        return JSONResponse(
            **answer
            )
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 500
            )


    
    
    
    
    
    
    
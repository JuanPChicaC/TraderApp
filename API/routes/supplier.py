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

@external_api.get(
    "/bars_information/{stocksTicker}/{date_from}/{date_to}"
    )
def get_symbol_bars(
    stocksTicker:str, date_from:str, date_to:str, multiplier:str=None,
    timespan:str=None,adjusted:str = None,sort:str = None,
    limit:str = None
    ):
    arguments = locals()
    
    try:
        answer = get_symbols_data(
            **arguments
            )
        return JSONResponse(
            content = answer,
            status_code=200
            )
    
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 500
            )

@external_api.get(
    "/export/bars_information/{stocksTicker}/{date_from}/{date_to}"
    )
async def get_symbol_bars_csv(
    stocksTicker:str, date_from:str, date_to:str, multiplier:str=None,
    timespan:str=None,adjusted:str = None,sort:str = None,
    limit:str = None
    ):
    arguments = locals()
    
    try:
        answer = get_symbols_data(
            **arguments
            )
        
        df = get_df(
            answer
            )
        
        stream = io.StringIO()
        df.to_csv(
            stream,
            index=False
            )
        
        response = StreamingResponse(
            iter([stream.getvalue()]),
            media_type = "text/csv"
            )
        
        response.headers["Content-Disposition"] = "attachment; filename={symbols}_{datetime}_info.csv".format(
            symbols = stocksTicker.replace(" ", "").replace(",", "_"),
            datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            )
        
        
        
        return response
    
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 500
            )



    
    
    
    
    
    
    
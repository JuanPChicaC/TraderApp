from fastapi import APIRouter
import os
import sys
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io
from datetime import datetime
from typing import List, Optional, Dict


sys.path.append(
    os.path.dirname(
        os.path.dirname(
          os.path.abspath(
              __file__
              )
          )
        )
    )
from tools.database import CPortfolio,UPortfolio,DPortfolio, get_date_from, get_date_to
import operations.watchlist as wl


watchlist_routes = APIRouter()

@watchlist_routes.post(
    "/create_portfolio",
    response_model= CPortfolio,
    tags = ["Portfolio Manager"]
    )
def create(cportfolio:CPortfolio):
    
    return wl.create_portfolio(
        cportfolio.dict()
        )

@watchlist_routes.get(
    "/portfolio_details",
    tags = ["Portfolio Manager"]
    )
def get(user:str, portfolio:str = None):
    return wl.get_portfolios(
        **locals()
        )

@watchlist_routes.post(
    "/delete_portfolio",
    tags = ["Portfolio Manager"]
    )
def delete(dportfolio:DPortfolio):
    
    return wl.delete_portfolio(
        dportfolio.dict()
        )   

@watchlist_routes.get(
    "/portfolio_data",
    tags = ["Portfolio Manager"]
    )
def get_data(
        user:str,
        portfolio:str,
        date_to:str = get_date_to(),
        date_from:str = get_date_from(),        
        multiplier:str=None,        
        timespan:str=None,
        adjusted:str = None,
        sort:str = None,
        limit:str = None
        ):
    
    return wl.get_portfolio_data(
        **locals()
        )
    
@watchlist_routes.get(
    "/portfolio_csv_data",
    tags = ["Portfolio Manager"]
    )
async def get_csv(
        user:str,
        portfolio:str,
        date_to:str = get_date_to(),
        date_from:str = get_date_from(),        
        multiplier:str=None,        
        timespan:str=None,
        adjusted:str = None,
        sort:str = None,
        limit:str = None
        ):
    return await wl.get_portfolio_data_csv(
        **locals()
        )

@watchlist_routes.post(
    "/add_symbols",
    tags = ["Portfolio Manager"]
    )
async def add_symbols(portfolio:UPortfolio):
    return await wl.add_portfolio_symbols(
        portfolio.dict()
        )
@watchlist_routes.post(
    "/drop_symbols",
    tags = ["Portfolio Manager"]
    )
async def drop_symbols(portfolio:UPortfolio):
    return await wl.drop_portfolio_symbols(
        portfolio.dict()
        )

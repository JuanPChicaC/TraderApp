import sys
import os
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key
from pandas import DataFrame, concat
from .supplier import get_symbols_data, get_df
import io
from fastapi.responses import StreamingResponse
from datetime import datetime
sys.path.append(
    os.path.dirname(
        os.path.dirname(
          os.path.abspath(
              __file__
              )
          )
        )
    )
from tools.database import dynamodb
from tools.ai import OptimalPortfolio


table = dynamodb.Table(
    "watchlist"
    )

def get_market_data(request_dict:dict):
    
    add_info = {
     "stocksTicker" : ",".join(
         request_dict["symbols_list"]
         )
     }
        
    
    data = get_symbols_data(
        **{
            **request_dict,
            **add_info
            }
        )

    works = True    
    for symbol,info in data.items():
        if not "content" in info.keys():
            works = False
    
    return works,data
    
    
def clean_symbol_info(symbol_info: tuple):
    
    info = symbol_info[1]["content"]
    
    info_df = DataFrame().from_dict(
        info
        )
    info_df.set_index(
        't', inplace = True
        )
    info_df.rename(
        inplace = True,
        columns = {'l':symbol_info[0]}
        )
    
    return info_df[symbol_info[0]]
    
    
def prices_consolidation(prices_info:dict):
    
    info_collection = map(
        clean_symbol_info,
        prices_info.items()
        )
    
    consolidated_info = concat(
        info_collection,
        axis = 1
        )
    
    consolidated_info.dropna(
        inplace = True
        )
    
    return consolidated_info

def get_optimal_portfolio(market_info:DataFrame):
    
    optimal_portfolio = OptimalPortfolio(
        market_info
        )
    
    optimal_distribution = optimal_portfolio.optimize()
    
    assets = optimal_portfolio.asset_names
    
    return assets, optimal_distribution

def get_investment_suggestion(portfolio_info:dict):
    
    if len(portfolio_info["symbols_list"]) < 2:
        return True, {
            "assets" : portfolio_info["symbols_list"],
            "optimal_distribution" : []
            }
    
    data_works, market_data = get_market_data(
        portfolio_info    
        )
    
    if not data_works:
        return False, {}
    
    consolidated_prices = prices_consolidation(
        market_data
        )
    
    assets, optimal_distribution = get_optimal_portfolio(
        consolidated_prices
        )
    
    optimal_distribution = list(map(
        lambda x: "{}%".format(str(round(x*100,2))[:5]),
        optimal_distribution
        ))
    
    return True, {
        "assets" : portfolio_info["symbols_list"],
        "optimal_distribution" : optimal_distribution
        }
    

def create_portfolio(portfolio:dict):
    
    try:
        
        get_optimallity, invest_suggest = get_investment_suggestion(
            portfolio
            )
        if get_optimallity:
            portfolio["distribution_advice"] = invest_suggest["optimal_distribution"] 
            portfolio["symbols_list"] = invest_suggest["assets"]
        else: 
            portfolio["distribution_advice"] = []
        
        table.put_item(
            Item = portfolio
            )
        return portfolio
    
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 400
            )       
    
    
def get_portfolios(user: str, portfolio:str):
    try:
        if not portfolio:
            response = table.query(
                KeyConditionExpression=Key("user").eq(user)
            )
        else: 
            response = table.query(
                KeyConditionExpression=Key("user").eq(user) & Key("portfolio").eq(portfolio)
            )    
        return response["Items"]  
    
    except ClientError as e:
        return JSONResponse(
            content=e.response["Error"],
            status_code=400
            )

def delete_portfolio(dportfolio:dict):
    try:
        response = table.delete_item(
            Key={
                key : value
                for key, value in dportfolio.items() #if value
                }
        )
        return response
    except ClientError as e:
        return JSONResponse(
            content=e.response["Error"],
            status_code=400
            )    

def get_portfolio_data(**kwargs):
    try:
         
        portfolio_list = get_portfolios(
            kwargs['user'],
            kwargs["portfolio"]
            )
        
        portfolio = portfolio_list[0]
        
        kwargs["stocksTicker"] = ",".join(
            portfolio["symbols_list"]
            )
        
        data = get_symbols_data(
            **kwargs
            )
        
        return data
        
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 400
            )
    
def get_portfolio_data_csv(**kwargs):
    try:
        
        data =get_portfolio_data(
            **kwargs
            )

        df = get_df(
            data
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
        
        response.headers["Content-Disposition"] = "attachment; filename={portfolio}_{datetime}_info.csv".format(
            portfolio = kwargs["portfolio"],
            datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            )
        return response        
    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 400
            )

    
def add_portfolio_symbols(portfolio_info:dict):
    try:
        
        current_portfolios = get_portfolios(
            portfolio_info["user"],
            portfolio_info["portfolio"]
            )
        current_portfolio = current_portfolios[0]
        
        current_symbols = current_portfolio["symbols_list"]
        
        symbols_to_add = portfolio_info["symbols_list"]
        
        new_symbols = []
        for symbol in  current_symbols+symbols_to_add:
            if not symbol in new_symbols:
                new_symbols.append(symbol)
        
        portfolio_info["symbols_list"] = new_symbols
        
        get_optimallity, invest_suggest = get_investment_suggestion(
            portfolio_info
            )
        if get_optimallity:
            portfolio_info["distribution advice"] = invest_suggest["optimal_distribution"] 
            portfolio_info["symbols_list"] = invest_suggest["assets"]
        else: 
            portfolio_info["distribution advice"] = []    
            
        response = table.update_item(
            Key={
                "user": portfolio_info["user"],
                "portfolio": portfolio_info["portfolio"]
                },
            UpdateExpression="""
                SET 
                symbols_list = :symbols_list, 
                age = :portfolio, 
                last_update_datetime = :last_update_datetime,
                date_to = :date_to,
                date_from = :date_from,
                multiplier = :multiplier,
                timespan = :timespan,
                distribution_advice = :distribution_advice
                """,
            ExpressionAttributeValues={
                ":symbols_list": invest_suggest["assets"],
                ":portfolio": portfolio_info["portfolio"],
                ":last_update_datetime": portfolio_info["last_update_datetime"],
                ":date_to": portfolio_info["date_to"],
                ":date_from": portfolio_info["date_from"],
                ":multiplier": portfolio_info["multiplier"],
                ":timespan": portfolio_info["timespan"],
                ":distribution_advice": invest_suggest["optimal_distribution"]
                }
            )   
        return response

    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 400
            )    
    

def drop_portfolio_symbols(portfolio_info:dict):
    try:
        
        current_portfolios = get_portfolios(
            portfolio_info["user"],
            portfolio_info["portfolio"]
            )
        current_portfolio = current_portfolios[0]
        
        current_symbols = current_portfolio["symbols_list"]
        
        symbols_to_drop = portfolio_info["symbols_list"]
        
        new_symbols = [symbol for symbol in current_symbols if symbol not in symbols_to_drop]

        portfolio_info["symbols_list"] = new_symbols
        
        get_optimallity, invest_suggest = get_investment_suggestion(
            portfolio_info
            )
        if get_optimallity:
            portfolio_info["distribution_advice"] = invest_suggest["optimal_distribution"] 
            portfolio_info["symbols_list"] = invest_suggest["assets"]
        else: 
            portfolio_info["distribution advice"] = []    
    
        response = table.update_item(
            Key={
                "user": portfolio_info["user"],
                "portfolio": portfolio_info["portfolio"]
                },
            UpdateExpression="""
                SET 
                symbols_list = :symbols_list, 
                age = :portfolio, 
                last_update_datetime = :last_update_datetime,
                date_to = :date_to,
                date_from = :date_from,
                multiplier = :multiplier,
                timespan = :timespan,
                distribution_advice = :distribution_advice
                """,
            ExpressionAttributeValues={
                ":symbols_list": invest_suggest["assets"],
                ":portfolio": portfolio_info["portfolio"],
                ":last_update_datetime": portfolio_info["last_update_datetime"],
                ":date_to": portfolio_info["date_to"],
                ":date_from": portfolio_info["date_from"],
                ":multiplier": portfolio_info["multiplier"],
                ":timespan": portfolio_info["timespan"],
                ":distribution_advice": invest_suggest["optimal_distribution"]
                }
            )   
        return response

    except ClientError as e:
        return JSONResponse(
            content = e.response["Error"],
            status_code = 400
            )    
    
    
    
    
    
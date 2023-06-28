import os
import sys
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(
          os.path.abspath(
              __file__
              )
          )
        )
    )

from tools.data_supplier import Supplier

supplier = Supplier(
    )

symbols_info_input = supplier.symbols_info_input

def get_symbols_information(**kwargs):
    return supplier.get_symbols_universe(
        **kwargs
        )
    
def get_symbol_data(**kwargs):
    return supplier.get_historical_data(
        **kwargs
        )
    
def get_symbols_data(**kwargs):
    
    stocksTicker_list = kwargs["stocksTicker"].replace(
        " ",
        ""
        ).split(
            ","
            )
            
    data = {
        symbol : get_symbol_data(
            **{
                **kwargs,**{"stocksTicker":symbol}
                }
            )
        for symbol in stocksTicker_list
        }
    
    return data
    

def transform_json_df(symbol_info:tuple):
    
    df = pd.DataFrame().from_dict(
        symbol_info[1]
        )
    df["symbol"] = symbol_info[0]
    
    return df
    
    
def get_df(answer): 
    
    
    data_array = [
        (symbol,info["content"]) for symbol,info in answer.items() if info["status_code"] == 200
        ]
    
    df_array = map(
        transform_json_df,
        data_array
        )
        
    df = pd.concat(
        df_array
        )  
    
    return  df









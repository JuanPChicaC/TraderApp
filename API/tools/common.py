import json
import sys
import os

api_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            __file__
            )
        )
    )
    
__supp_queries = None
    
def get_supp_queries():
    
    global __supp_queries
    
    if not __supp_queries:
        with open(f"{api_path}/sources/configuration/supplier_queries.json","r") as file:
            __supp_queries = json.loads(
                file.read()
                )
            file.close()
        
    return __supp_queries


__db_tables_config = None

def get_db_tables_config():
    global __db_tables_config
    
    if not __db_tables_config:
        with open(f"{api_path}/sources/configuration/database.json","r") as file:
            __db_tables_config = json.loads(
                file.read()
                )
            file.close()
    
    return __db_tables_config

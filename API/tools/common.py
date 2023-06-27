import json

__supp_queries = None
    
def get_supp_queries():
    global __supp_queries
    
    if not __supp_queries:
        with open("../sources/configuration/supplier_queries.json","r") as file:
            __supp_queries = json.loads(
                file.read()
                )
            file.close()
        
    return __supp_queries
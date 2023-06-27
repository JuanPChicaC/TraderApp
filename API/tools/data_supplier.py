# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 20:23:25 2023

@author: juanp
"""

import requests
from os import getenv
import re
from common import get_supp_queries

class Supplier():

    def __init__(self):
        
        self.__base_url = getenv(
            "INFORMATION_SERVICE_URL"
            )
        self.__key = getenv(
            "INFORMATION_SERVICE_KEY"
            )
        self.__headers = {
            "Authorization" : "Bearer {key}".format(
                key= self.__key
                )
            }
        
    def set_endpoint_url(self, endpoint:str, params:dict):
        return "{url}{endpoint}{params_statement}".format(
            url = self.__base_url ,
            endpoint = endpoint,
            params_statement = "" if len(params) == 0 else "?"+"&".join(
                [
                    "{key}={value}".format(
                        key = key, 
                        value = params[key]
                        )
                    for key in params.keys()
                    ]
                )
            )
    
    def valid_content(self,value:str,pattern:str):
        
        pat = re.compile(
            r"{}".format(
                pattern
                )
            )
    
        match = re.fullmatch(
            pat,
            value
            )
    
        return bool(
            match
            )
    
    
    def required_fields_sanity_check(self,required_fields:dict,input_dict:dict,validations:dict):
        
        required_fields_processed = {}
        
        for name in required_fields.keys():
            
            if not required_fields[name]:
                if not name in input_dict.keys():
                    return False , "the key {} is required in the http request params".format(
                        name
                        )

                elif not input_dict[name]:
                    return False, "the key {} can´t be set null in the http request params".format(
                        name
                        )

                else:
                    valid_value = self.valid_content(input_dict[name], validations[name])
                    
                    if not valid_value:
                        return False, "the value for the key {} is not valid, check teh documentation".format(
                            name
                            )
                    else:
                        required_fields_processed[name] = input_dict[name]
            
            else:
                if not name in input_dict.keys():
                    required_fields_processed[name] = required_fields[name]
                elif not input_dict[name]:
                    required_fields_processed[name] = required_fields[name]
                else:
                    
                    valid_value = self.valid_content(input_dict[name], validations[name])
                    
                    required_fields_processed[name] = required_fields[name] if not valid_value else input_dict[name]
                
                
        return True, required_fields_processed

    def params_sanity_check(self,params:dict,input_dict:dict,validations:dict):    

        params_processed = {}
        for name in params.keys():
            if not name in input_dict.keys():
                if not params[name]:
                    continue
                params_processed[name] = params[name]
            elif not input_dict[name]:
                if not params[name]:
                    continue
                params_processed[name] = params[name]
            else:
    
                valid_value = self.valid_content(input_dict[name], validations[name])

                if not params[name] and not valid_value:
                    continue

                params_processed[name] = params[name] if not valid_value else input_dict[name]
        
        return params_processed       


    def get_query(self,url):
        
        response = requests.get(
            url,
            self.__headers
            )
        
        jsonified_reponse = response.json()
        
        return {
            "status_code": response.status_code,
            "content" : jsonified_reponse["results"]
            }
        
        

    def get_symbols_universe(self,**kwargs):
        
        
        rf_pass, rf_sanity_content = self.required_fields_sanity_check(
            get_supp_queries()["stock_symbols_universe"]["required_fields"], 
            kwargs, 
            get_supp_queries()["stock_symbols_universe"]["validations"]
            )
      
        if not rf_pass:
            return {
                "status_code": 404,
                "message" : rf_sanity_content
                }
        
        params_content = self.params_sanity_check(
            get_supp_queries()["stock_symbols_universe"]["params"], 
            kwargs, 
            get_supp_queries()["stock_symbols_universe"]["validations"]
            )
        
        query_url = self.set_endpoint_url(
            get_supp_queries["queries"]["stock_symbols_universe"]["endpoint"],
            params_content
            )
        
        formated_query_url = query_url.format(
            **rf_sanity_content
            )
        
        result = self.get_query(
            formated_query_url
            )
        
        return result
        
        
    def get_historical_data(self,stock_ticker:str):
        
        pass
    
        
        
    
    
    
    
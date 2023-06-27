# -*- coding: utf-8 -*-

from fastapi import FastAPI
from routes.supplier import external_api

app = FastAPI()

app.include_router(
    external_api 
    )
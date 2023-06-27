# -*- coding: utf-8 -*-

from fastapi import FastAPI
from routes.supplier import external_api
from tools.database import create_tables

app = FastAPI()

app.include_router(
    external_api 
    )

create_tables()


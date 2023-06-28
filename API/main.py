# -*- coding: utf-8 -*-

from fastapi import FastAPI
from routes.supplier import external_api
from routes.watchlist import watchlist_routes
from tools.database import create_tables
from tools.common import get_api_doc
app = FastAPI(
    **get_api_doc()
    )

app.include_router(
    external_api,
    )
app.include_router(
    watchlist_routes 
    )
create_tables()


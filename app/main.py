from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from jwt import router


app = FastAPI()
app.add_api_route(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


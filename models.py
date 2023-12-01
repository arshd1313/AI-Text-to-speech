from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class TextInput(BaseModel):
    inputs: str

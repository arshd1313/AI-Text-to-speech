from pydantic import BaseModel
# from datasets import load_dataset
class Sound( BaseModel):
    filename:str
    xvector:str
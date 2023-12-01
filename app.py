from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import uvicorn
import os
import pickle
import io

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
HEADERS = {"Authorization": "Bearer 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"}

class TextInput(BaseModel):
    inputs: str

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.content

def save_to_pkl(file_path, data):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)

@app.post("/text2audio")
def text_to_audio(text_input: TextInput, save_pkl: bool = True):
    try:
        payload = {"inputs": text_input.inputs}
        audio_bytes = query(payload)

        if save_pkl:
            # Save the audio to a PKL file
            save_to_pkl("output.pkl", audio_bytes)

        def generate():
            yield audio_bytes

        response = StreamingResponse(generate(), media_type="audio/wav")
        response.headers["Content-Disposition"] = 'attachment; filename="output.wav"'
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":  
    uvicorn.run(app, host="127.0.0.1", port=8001)

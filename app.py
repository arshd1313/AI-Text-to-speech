from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import FileResponse
import requests
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

#from hugging face

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
HEADERS = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.content

app = FastAPI()

class TextInput(BaseModel):
    inputs: str

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.content

@app.post("/text2audio")
def text_to_audio(text_input: TextInput):
    try:
        payload = {"Please Enter your Inputs": text_input.inputs}
        audio_bytes = query(payload)

        def generate():
            yield audio_bytes

        response = StreamingResponse(generate(), media_type="audio/wav")
        response.headers["Content-Disposition"] = 'attachment; filename="output.wav"'
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8001)
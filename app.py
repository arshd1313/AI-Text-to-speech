from fastapi import FastAPI, HTTPException,UploadFile
import pickle
from pydantic import BaseModel
import uvicorn
from models import Sound
from gtts import gTTS
import os
import soundfile as sf
from pydantic import BaseModel
from fastapi.responses import FileResponse
import subprocess
from typing import List


with open("model.pkl", "wb") as file:
    pickle.dump(Sound, file)


app = FastAPI()
class Sound(BaseModel):
    filename: str
    xvector: str

class Sound(BaseModel):
    filename:str
    xvector:str

sound_instance = Sound(filename="example.wav", xvector="dummy_vector")


model=pickle.load(open("model.pkl","rb"))

with open("model.pkl", "rb") as file:
    loaded_sound_instance = pickle.load(file)

with open("model.pkl", "wb") as file:
    pickle.dump(sound_instance, file)

@app.get("/get_all_audio_files", response_model=List[str])
def get_all_audio_files():
    # Specify the folder where audio files are stored
    audio_folder = "audio_files"

    # Get a list of all MP3 files in the folder
    mp3_files = [f for f in os.listdir(audio_folder) if f.endswith(".mp3")]

    # Construct URLs or paths for each MP3 file
    mp3_urls = [f"/audio_files/{mp3_file}" for mp3_file in mp3_files]

    return mp3_urls

@app.post("/predict")
def predict(req: Sound):
    filename = req.filename
    
    # Create a folder if it doesn't exist
    output_folder = "audio_files"
    os.makedirs(output_folder, exist_ok=True)
    
    sound_file_path = os.path.join(output_folder, "output.mp3")
   
    tts_text = f"{filename}."
    tts = gTTS(text=tts_text, lang="en-us", slow=True)

    tts.save(sound_file_path)
   
    # Convert MP3 to WAV without confirmation prompt
    wav_file_path = os.path.join(output_folder, "output.wav")
    subprocess.run(["ffmpeg", "-y", "-i", sound_file_path, wav_file_path])
    
    # If the user needs to remove the MP3 file
    # os.remove(sound_file_path)
    
    # Return the sound response
    return FileResponse(wav_file_path, media_type="audio/mp3", filename="output.mp3")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

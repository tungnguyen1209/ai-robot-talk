import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import emoji
import edge_tts
import base64
import tempfile
import asyncio

# Import Brain
from modules.brain import Brain

app = FastAPI()

# Mount static for local dev (Vercel handles static differently usually, but this helps)
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Initialize Brain
brain = Brain()

class ChatRequest(BaseModel):
    message: str

def split_emoji(text):
    emoji_list = emoji.emoji_list(text)
    distinct_emojis = "".join([e['emoji'] for e in emoji_list])
    clean_text = emoji.replace_emoji(text, replace="")
    return clean_text, distinct_emojis

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_text = request.message
    
    # 1. Think
    full_response = brain.think(user_text)
    
    # 2. Process
    text_to_speak, emojis_found = split_emoji(full_response)
    
    # 3. Generate Audio (Edge TTS)
    # We generate in memory or temp file and convert to base64
    communicate = edge_tts.Communicate(text_to_speak, "vi-VN-HoaiMyNeural")
    
    # Create a temporary file to save audio then read bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_filename = fp.name
        
    await communicate.save(temp_filename)
    
    with open(temp_filename, "rb") as f:
        audio_bytes = f.read()
    
    # Clean up
    os.remove(temp_filename)
    
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    return JSONResponse({
        "response": full_response,
        "emojis": emojis_found,
        "audio": audio_base64
    })

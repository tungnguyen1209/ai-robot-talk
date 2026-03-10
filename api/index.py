import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import asyncio

# Import các module của Sếp
from modules.brain import Brain
from modules.tts import Mouth

app = FastAPI()

# Cấu hình đường dẫn cho Vercel (sử dụng thư mục gốc hoặc /web)
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Khởi tạo Sumo
brain = Brain()
mouth = Mouth()

class AskRequest(BaseModel):
    text: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_endpoint(ask_request: AskRequest):
    user_text = ask_request.text
    
    if not user_text:
        return JSONResponse({"error": "Bé chưa nói gì với Sumo nè!"}, status_code=400)
        
    # 1. Sumo suy nghĩ
    # Chạy đồng bộ trong thread để không làm block event loop của FastAPI
    bot_response = await asyncio.to_thread(brain.think, user_text)
    
    # 2. Sumo chuẩn bị giọng nói (Dùng Edge TTS đã tối ưu)
    audio_base64 = await asyncio.to_thread(mouth.get_audio_base64, bot_response)
    
    # 3. Trả về kết quả đúng định dạng mà Giao diện Web đang chờ
    return JSONResponse({
        "response": bot_response,
        "audio": audio_base64
    })

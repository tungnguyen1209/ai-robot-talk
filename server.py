import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import threading
import queue
import time
import emoji
import pygame

# Import existing modules
from modules.brain import Brain
from modules.tts import Mouth
# Note: SpeechRecognition blocking might be an issue. We might want to use a non-blocking approach
# or run the loop in a thread.
import speech_recognition as sr
from modules.stt import Ear

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Communication queues
msg_queue = queue.Queue()

# Global state
active_sockets = []
LOOP = None

@app.on_event("startup")
async def startup_event():
    global LOOP
    LOOP = asyncio.get_running_loop()
    # Start Robot logic in background thread
    robot_thread = threading.Thread(target=run_robot_logic, daemon=True)
    robot_thread.start()

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_sockets.append(websocket)
    try:
        while True:
            # Receive message from client
            import json
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "chat":
                    # Put chat message into the queue for the brain to process
                    msg_queue.put(message.get("content"))
            except:
                pass
    except:
        if websocket in active_sockets:
            active_sockets.remove(websocket)

async def broadcast(message_type, content):
    """
    Send message to all connected clients.
    """
    to_remove = []
    for ws in active_sockets:
        try:
            await ws.send_json({"type": message_type, "content": content})
        except:
            to_remove.append(ws)
    
    for ws in to_remove:
        if ws in active_sockets:
            active_sockets.remove(ws)

def run_robot_logic():
    """
    The main robot loop running in a separate thread.
    """
    print("🤖 Robot Thread Started!")
    
    # Initialize components
    try:
        brain = Brain()
        mouth = Mouth()
        ear = Ear()
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return

    # Helper to clean text
    def split_emoji(text):
        emoji_list = emoji.emoji_list(text)
        distinct_emojis = "".join([e['emoji'] for e in emoji_list])
        clean_text = emoji.replace_emoji(text, replace="")
        return clean_text, distinct_emojis

    def process_input(text):
        """Helper to process text input (from voice or chat)"""
        if not text: return

        if "dừng lại" in text.lower():
             if LOOP:
                asyncio.run_coroutine_threadsafe(broadcast("response", "Tạm biệt bé nhé!"), LOOP)
             mouth.say("Tạm biệt bé nhé!")
             # Note: break here only affects the inner function, handle in loop
             return "STOP"

        # Think
        full_response = brain.think(text)
        
        # Process Response
        text_to_speak, emojis_found = split_emoji(full_response)
        
        # Broadcast to UI
        if LOOP:
            asyncio.run_coroutine_threadsafe(broadcast("response", full_response), LOOP)
            if emojis_found:
                 asyncio.run_coroutine_threadsafe(broadcast("expression", emojis_found), LOOP)
        
        # Speak (Clean text only)
        mouth.say(text_to_speak)
        
        # Reset expression after speaking (optional)
        time.sleep(1)
        if LOOP:
            asyncio.run_coroutine_threadsafe(broadcast("expression", ""), LOOP)
        return "CONTINUE"

    mouth.say("Chào bé, Sumo đã sẵn sàng!")
    
    # Run the loop
    while True:
        # 1. Check for text chat messages first (non-blocking if queue not empty)
        try:
            chat_text = msg_queue.get_nowait()
            if chat_text:
                print(f"Nhận tin nhắn chat: {chat_text}")
                result = process_input(chat_text)
                if result == "STOP": break
                continue # Skip listening this turn if we just processed a chat
        except queue.Empty:
            pass

        # 2. Listen from Microphone (Blocking with timeout handled in Ear)
        # We need a way to not block forever so we can check the queue
        # For now Ear.listen() has a timeout but it prints "Không nghe rõ".
        # We might want to adjust Ear to be less noisy or just quick check.
        
        # For this version, let's treat voice as primary but check queue between listens
        user_text = ear.listen()
        
        if user_text:
            if LOOP:
                asyncio.run_coroutine_threadsafe(broadcast("transcript", user_text), LOOP)
            
            result = process_input(user_text)
            if result == "STOP": break

if __name__ == "__main__":
    # Start Web Server
    print("🚀 Starting Web Interface at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

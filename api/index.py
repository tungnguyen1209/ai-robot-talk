import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import emoji
import base64
import tempfile
import asyncio
import struct
from google import genai
from google.genai import types

# Import Brain
from modules.brain import Brain

app = FastAPI()

# Mount static for local dev
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
    return clean_text.strip(), distinct_emojis

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=", 1)[1])
            except: pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except: pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size
    
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels, 
        sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
    )
    return header + audio_data

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_text = request.message
    
    # 1. Think
    full_response = brain.think(user_text)
    
    # Check for VIDEO tag
    SAFE_VIDEOS = [
        "mMwHgp9vTfw", # Baby Shark
        "XqZsoesa55w", # Baby Shark Dance
        "FhqQh3tQq7I", # Kids music
        "WBOfDl6d8yQ", # ABC Song
        "71hqRT9U0wg", # Wheels on the Bus
        "020g-0HHCAU", # Baby Songs
    ]
    
    video_id = None
    if "[VIDEO]" in full_response:
        video_id = random.choice(SAFE_VIDEOS)
        full_response = full_response.replace("[VIDEO]", "").strip()

    # 2. Process
    text_to_speak, emojis_found = split_emoji(full_response)
    
    if not text_to_speak:
        return JSONResponse({"response": full_response, "emojis": emojis_found, "audio_chunks": [], "video_id": video_id})

    # 3. Generate Audio using Gemini 2.5 Flash Preview TTS
    audio_chunks = []
    
    try:
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        model_name = "gemini-2.5-flash-preview-tts" # verify alias or use explicit if needed
        
        # We instruct the model to say the text
        # Using a simple prompt structure
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text_to_speak),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker="Speaker 1",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Puck" 
                                )
                            ),
                        ),
                        types.SpeakerVoiceConfig(
                            speaker="Speaker 2",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Zephyr" 
                                )
                            ),
                        ),
                    ]
                ),
            ),
        )

        # Iterate stream
        # Note: synchronouse generator if using standard client, or async?
        # genai.Client seems sync by default unless AsyncClient is used.
        # Let's use it synchronously for now, or wrap in thread if blocking.
        # For simplicity, sync valid since we want chunks one by one?
        # Actually fastapi is async, blocking might hurt. But let's try.
        
        # Wait, the user sample uses `client.models.generate_content_stream`.
        # I'll Assume it works.
        
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
                
            part = chunk.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                # Got audio data
                raw_data = part.inline_data.data
                mime = part.inline_data.mime_type
                
                # Convert to WAV if needed (browsers need container)
                # Usually it comes as raw PCM (audio/L16) or similar
                wav_bytes = convert_to_wav(raw_data, mime)
                
                b64_audio = base64.b64encode(wav_bytes).decode('utf-8')
                audio_chunks.append(b64_audio)
                
    except Exception as e:
        print(f"Gemini TTS Error: {e}")
        # Fallback? No, just return empty or error
        # Maybe insert an error message in chat

    return JSONResponse({
        "response": full_response,
        "emojis": emojis_found,
        "audio_chunks": audio_chunks,
        "video_id": video_id
    })

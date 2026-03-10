from flask import Flask, render_template, request, jsonify
from modules.brain import Brain
from modules.tts import Mouth
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

# Khởi tạo Sumo một lần khi server chạy
sumo_brain = Brain()
sumo_mouth = Mouth()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_text = data.get('text', '')
    
    if not user_text:
        return jsonify({'error': 'Bé chưa nói gì với Sumo nè!'})
        
    # 1. Sumo suy nghĩ
    bot_response = sumo_brain.think(user_text)
    
    # 2. Sumo chuẩn bị giọng nói (Base64)
    audio_base64 = sumo_mouth.get_audio_base64(bot_response)
    
    # 3. Trả về kết quả
    return jsonify({
        'response': bot_response,
        'audio': audio_base64
    })

if __name__ == '__main__':
    # Chạy cục bộ (Local)
    app.run(debug=True, port=5000)

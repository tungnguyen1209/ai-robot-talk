# AI Robot Talk 🤖

Một ứng dụng robot AI đơn giản có khả năng giao tiếp 2 chiều (Nghe - Suy nghĩ - Nói) với trẻ em, hỗ trợ Tiếng Việt và Tiếng Anh.

## Tính năng
- **Nghe (STT)**: Sử dụng Google Speech Recognition để chuyển giọng nói thành văn bản.
- **Suy nghĩ (Brain)**: Sử dụng **Google AI (Gemini)** để xử lý hội thoại thông minh và linh hoạt.
- **Nói (TTS)**: Sử dụng Microsoft Edge TTS để tạo giọng đọc tự nhiên.

## Cài đặt

1.  **Clone dự án** (hoặc tải về):
    ```bash
    git clone <your-repo-url>
    cd ai-robot-talk
    ```

2.  **Cài đặt thư viện Python**:
    Yêu cầu Python 3.10 trở lên.
    ```bash
    pip install -r requirements.txt
    ```
    *Lưu ý: Nếu chưa có `requirements.txt`, hãy chạy:*
    ```bash
    pip install google-generativeai edge-tts SpeechRecognition pyaudio
    ```

3.  **Cấu hình Google AI (Gemini)**:
    - Lấy API Key tại [Google AI Studio](https://aistudio.google.com/).
    - Thiết lập biến môi trường `GOOGLE_API_KEY`:
        - **Windows (Powershell)**:
          ```powershell
          $env:GOOGLE_API_KEY="your_api_key_here"
          ```
        - **Linux/Mac**:
          ```bash
          export GOOGLE_API_KEY="your_api_key_here"
          ```
    - Hoặc tạo file `.env` nếu bạn cập nhật code để hỗ trợ `python-dotenv`.

## Hướng dẫn sử dụng

Chạy lệnh sau để khởi động robot:
```bash
python main.py
```

- Robot sẽ chào bạn.
- Hãy nói chuyện với robot qua microphone.
- Để dừng cuộc trò chuyện, hãy nói "Tạm biệt" hoặc "Dừng lại".

## Cấu trúc dự án
- `main.py`: Chương trình chính.
- `modules/`:
    - `stt.py`: Module xử lý âm thanh đầu vào.
    - `brain.py`: Module xử lý logic hội thoại (Google Gemini).
    - `tts.py`: Module xử lý âm thanh đầu ra.

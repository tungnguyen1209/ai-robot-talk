# AI Robot Talk 🤖

Một ứng dụng robot AI đơn giản có khả năng giao tiếp 2 chiều (Nghe - Suy nghĩ - Nói) với trẻ em, hỗ trợ Tiếng Việt và Tiếng Anh.

## Tính năng
- **Nghe (STT)**: Sử dụng Google Speech Recognition để chuyển giọng nói thành văn bản.
- **Suy nghĩ (Brain)**: Sử dụng **Local AI (Ollama)** để xử lý hội thoại offline trên máy tính, bảo mật và nhanh chóng.
- **Nói (TTS)**: Sử dụng Microsoft Edge TTS để tạo giọng đọc tự nhiên.

## Cài đặt

1.  **Clone dự án** (hoặc tải về):
    ```bash
    git clone <your-repo-url>
    cd ai-robot-talk
    ```

2.  **Cài đặt Ollama (Local AI)**:
    - Tải và cài đặt [Ollama](https://ollama.com/)
    - Mở terminal và tải model khuyến nghị (nhẹ, thông minh, hỗ trợ tiếng Việt tốt):
    ```powershell
    ollama pull qwen2.5:3b
    ```

3.  **Cài đặt thư viện Python**:
    Yêu cầu Python 3.10 trở lên.
    ```bash
    pip install -r requirements.txt
    ```

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
    - `brain.py`: Module xử lý logic hội thoại (Gemini).
    - `tts.py`: Module xử lý âm thanh đầu ra.

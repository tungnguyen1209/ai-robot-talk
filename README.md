# AI Robot Talk 🤖

Một ứng dụng robot AI đơn giản có khả năng giao tiếp 2 chiều (Nghe - Suy nghĩ - Nói) với trẻ em, hỗ trợ Tiếng Việt và Tiếng Anh.

## Tính năng
- **Nghe (STT)**: Sử dụng Google Speech Recognition để chuyển giọng nói thành văn bản.
- **Suy nghĩ (Brain)**: Sử dụng Google Gemini (LLM) để xử lý hội thoại thông minh, thân thiện.
- **Nói (TTS)**: Sử dụng Microsoft Edge TTS để tạo giọng đọc tự nhiên.

## Cài đặt

1.  **Clone dự án** (hoặc tải về):
    ```bash
    git clone <your-repo-url>
    cd ai-robot-talk
    ```

2.  **Cài đặt thư viện**:
    Yêu cầu Python 3.10 trở lên.
    ```bash
    pip install -r requirements.txt
    ```
    *Lưu ý: Nếu gặp lỗi cài đặt PyAudio trên Windows, hãy tìm file .whl phù hợp hoặc cài đặt các công cụ build của Microsoft Visual C++.*

3.  **Cấu hình API Key**:
    - Tạo file `.env` từ file mẫu (nếu chưa có).
    - Lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/).
    - Thêm vào file `.env`:
        ```text
        GEMINI_API_KEY=AIzaSy...
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

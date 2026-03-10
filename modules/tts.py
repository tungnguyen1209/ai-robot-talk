import asyncio
import edge_tts
import base64
import os

class Mouth:
    def __init__(self, voice='vi-VN-HoaiMyNeural'):
        self.voice = voice
        # Pitch: +15% (giọng cao, đáng yêu), Rate: +10% (nói nhanh, năng động)
        self.pitch = "+15Hz"
        self.rate = "+5%"
        self.output_file = "response.mp3"

    async def _generate_audio_base64(self, text):
        communicate = edge_tts.Communicate(text, self.voice, pitch=self.pitch, rate=self.rate)
        # Lưu ra file tạm rồi đọc lại dạng base64 (hoặc stream trực tiếp nếu muốn)
        await communicate.save(self.output_file)
        
        with open(self.output_file, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
            
        # Dọn dẹp file tạm
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            
        return encoded_string

    def get_audio_base64(self, text):
        """
        Trả về chuỗi Base64 của âm thanh để trình duyệt tự phát.
        """
        if not text:
            return ""
        try:
            return asyncio.run(self._generate_audio_base64(text))
        except Exception as e:
            print(f"Lỗi TTS: {e}")
            return ""

    def say(self, text):
        """
        Dùng cho chế độ chạy local (vẫn giữ nguyên cho Sếp nếu muốn test local).
        """
        print(f"Sumo nói: {text}")

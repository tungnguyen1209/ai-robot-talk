import asyncio
import edge_tts
import pygame
import os

class Mouth:
    def __init__(self, language='vi-VN-HoaiMyNeural'):
        self.language = language
        self.output_file = "response.mp3"
        pygame.mixer.init()

    async def _generate_audio(self, text):
        communicate = edge_tts.Communicate(text, self.language)
        await communicate.save(self.output_file)

    def say(self, text):
        """
        Chuyển văn bản thành giọng nói và phát ra loa.
        """
        print(f"Robot nói: {text}")
        if not text:
            return

        try:
            # Tạo file âm thanh (cần chạy async trong môi trường sync)
            asyncio.run(self._generate_audio(text))
            
            # Phát âm thanh
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            
            # Chờ phát xong
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Giải phóng file để có thể ghi đè lần sau
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f"Lỗi TTS: {e}")

if __name__ == "__main__":
    mouth = Mouth()
    mouth.say("Xin chào, mình là người máy thông minh.")

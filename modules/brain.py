import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("CẢNH BÁO: Chưa cấu hình GEMINI_API_KEY trong file .env")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
            self.chat = self.model.start_chat(history=[])
            
            # System prompt dưới dạng tin nhắn đầu tiên (hoặc config nếu model hỗ trợ)
            self.system_instruction = """
            Bạn là một robot AI thân thiện, nói chuyện với trẻ em. 
            Hãy trả lời ngắn gọn, dễ hiểu, vui vẻ. 
            Không dùng từ ngữ phức tạp. 
            Luôn xưng hô là "bạn" và "mình" hoặc "tớ".
            """
            
            # Khởi tạo ngữ cảnh ban đầu
            self.chat.send_message(self.system_instruction)

    def think(self, text):
        """
        Gửi văn bản đến LLM và nhận câu trả lời.
        """
        if not self.model:
            return "Mình chưa được kích hoạt trí tuệ nhân tạo. Hãy kiểm tra API Key nhé."
        
        try:
            response = self.chat.send_message(text)
            return response.text
        except Exception as e:
            print(f"Lỗi Brain: {e}")
            return "Xin lỗi, mình đang bị đau đầu chút xíu."

if __name__ == "__main__":
    brain = Brain()
    print(brain.think("Chào bạn, bạn tên là gì?"))

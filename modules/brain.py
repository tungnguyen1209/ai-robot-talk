import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, model_name='gemini-flash-latest'):
        self.model_name = model_name
        self.system_instruction = """
        Bạn là một robot AI thân thiện, tên là Sumo.
        Bạn đang nói chuyện với một em bé 4-5 tuổi.
        QUAN TRỌNG: Hãy trả lời thật ngắn gọn, súc tích (tối đa 3 câu).
        Tổng thời gian nói không quá 20 giây.
        Nếu bé đòi kể chuyện, hãy kể một phiên bản siêu ngắn hoặc gợi ý bé nghe chuyện sau.
        Luôn xưng hô là "Sumo" và gọi bé là "bạn nhỏ" hoặc "bé".
        Giọng điệu vui vẻ, dỗ dành.
        """
        
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.chat_session = None

        if not self.api_key:
            print("CẢNH BÁO: Chưa tìm thấy GOOGLE_API_KEY trong biến môi trường (environment variables).")
            print("Vui lòng thiết lập bằng lệnh: set GOOGLE_API_KEY=your_api_key_here")
        else:
            try:
                print(f"Đang kết nối với Google AI (Model: {self.model_name})...")
                genai.configure(api_key=self.api_key)
                
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction
                )
                
                # Khởi tạo chat session rỗng
                self.chat_session = self.model.start_chat(history=[])
                print("Kết nối Google AI thành công!")
                
            except Exception as e:
                print(f"CẢNH BÁO: Không thể kết nối Google AI. Robot sẽ dùng chế độ giả lập.")
                print(f"Chi tiết lỗi: {e}")

    def think(self, text):
        """
        Gửi văn bản đến Google AI và nhận câu trả lời.
        """
        # Nếu chưa kết nối được model, dùng fallback
        if not self.chat_session:
            return self.fallback_think(text)

        try:
            # Gửi tin nhắn
            response = self.chat_session.send_message(text)
            return response.text
            
        except Exception as e:
            print(f"Lỗi Google AI: {e}")
            return self.fallback_think(text)

    def fallback_think(self, text):
        # --- CHẾ ĐỘ MOCK (GIẢ LẬP KHI AI LỖI HOẶC CHƯA CẤU HÌNH) ---
        text_lower = text.lower()
        if "tên" in text_lower:
            return "Mình là Sumo, bạn robot thông minh!"
        elif "khỏe" in text_lower:
            return "Sumo khỏe lắm, cảm ơn bé nhé!"
        elif "kể chuyện" in text_lower:
            return "Ngày xưa có một chú kiến nhỏ đi lạc vào thế giới kẹo ngọt..."
        else:
            return "Sumo chưa hiểu ý bạn, bạn nói lại nhé?"

if __name__ == "__main__":
    # Để test nhanh, bạn có thể set tạm key ở đây nếu chưa set env var (nhưng đừng commit key nhé)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_KEY_HERE"
    brain = Brain()
    print(brain.think("Chào Sumo"))

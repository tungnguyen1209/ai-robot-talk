import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, model_name='gemini-3.0-flash-preview'):
        self.model_name = model_name
        # Ưu tiên lấy từ biến môi trường của hệ thống (Vercel)
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.model = None
        self.chat_session = None
        
        # System Instruction cho bé 4-5 tuổi
        self.system_instruction = """
        BẠN LÀ: Một robot AI siêu đáng yêu tên là Sumo.
        ĐỐI TƯỢNG: Trò chuyện với em bé từ 4-5 tuổi.
        PHONG CÁCH: Vui vẻ, dỗ dành, ngắn gọn (tối đa 3 câu). 
        Nhớ tên bé nếu bé đã kể. [VIDEO: từ khóa] nếu bé muốn xem gì đó.
        """

        if not self.api_key:
            print("❌ LỖI NGHIÊM TRỌNG: Chưa cấu hình GOOGLE_API_KEY trên Vercel!")
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction
                )
                # Khởi tạo phiên chat với lịch sử trống
                self.chat_session = self.model.start_chat(history=[])
                print(f"✅ Sumo đã sẵn sàng với bộ não {self.model_name}!")
            except Exception as e:
                print(f"❌ Lỗi khi khởi tạo Gemini Model: {e}")

    def think(self, text):
        if not self.api_key:
            return "Sếp ơi, Sếp chưa cho Sumo mượn chìa khóa (API Key) để mở não rồi!"
            
        if not self.chat_session:
            # Thử khởi tạo lại nếu trước đó bị lỗi
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_instruction)
                self.chat_session = self.model.start_chat(history=[])
            except Exception as e:
                return f"Sumo bị đau đầu quá: {str(e)[:50]}..."

        try:
            # Gửi tin nhắn đến AI
            response = self.chat_session.send_message(text)
            return response.text
        except Exception as e:
            print(f"❌ Lỗi khi gửi tin nhắn đến Gemini: {e}")
            # Trả về lỗi chi tiết để Sếp dễ debug
            return f"Sumo đang bị lùng bùng lỗ tai: {str(e)[:50]}..."

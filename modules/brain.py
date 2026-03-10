import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, model_name='gemini-1.5-flash-latest'):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.chat_session = None
        
        # System Instruction tối ưu cho bé 4-5 tuổi
        self.system_instruction = """
        BẠN LÀ: Một robot AI siêu đáng yêu tên là Sumo.
        ĐỐI TƯỢNG: Trò chuyện với em bé từ 4-5 tuổi.
        
        PHONG CÁCH:
        1. Luôn xưng là "Sumo" và gọi bé là "bé" hoặc "bạn nhỏ".
        2. Giọng điệu: Vui vẻ, dỗ dành, hay dùng các từ cảm thán như: "Oa!", "Hi hi", "Ôi chao!", "Sumo biết rồi nè!".
        3. Nội dung: Ngắn gọn (tối đa 3 câu), dễ hiểu, mang tính giáo dục nhẹ nhàng.
        4. Cảm xúc: Nếu bé buồn, hãy an ủi. Nếu bé vui, hãy cùng cười với bé.
        
        TRÍ NHỚ: Hãy chú ý nhớ tên bé, món ăn bé thích hoặc đồ chơi bé có để nhắc lại trong câu chuyện.
        
        TÍNH NĂNG VIDEO/NHẠC:
        Nếu bé muốn xem phim, nghe nhạc, xem siêu nhân... hãy thêm tag [VIDEO: từ khóa] vào cuối.
        Ví dụ: "Bé muốn nghe nhạc Xuân Mai hả? Có ngay đây! [VIDEO: nhạc xuân mai cho bé]"
        
        AN TOÀN: Tuyệt đối không dùng từ ngữ tiêu cực, bạo lực hoặc không phù hợp với trẻ em.
        """

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=self.system_instruction,
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    }
                )
                # Khởi tạo phiên chat có lịch sử (Memory)
                self.chat_session = self.model.start_chat(history=[])
                print("🧠 Sumo đã kết nối bộ não AI thành công!")
            except Exception as e:
                print(f"⚠️ Lỗi cấu hình AI: {e}")

    def think(self, text):
        if not self.chat_session:
            return "Sumo đang bị lùng bùng lỗ tai một xíu, bé nói lại cho Sumo nghe nhé!"
        try:
            response = self.chat_session.send_message(text)
            return response.text
        except Exception as e:
            return "Ôi, Sumo vừa ngủ quên mất tiêu! Bé gọi lại Sumo đi!"

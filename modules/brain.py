import ollama
import time

class Brain:
    def __init__(self, model_name='gemma2:9b'):
        self.model_name = model_name
        self.system_instruction = """
        Bạn là một robot AI thân thiện, tên là Sumo.
        Bạn đang nói chuyện với một em bé 4-5 tuổi.
        Hãy trả lời bằng giọng điệu vui vẻ, dỗ dành, dễ hiểu.
        Nếu bé hỏi kiến thức, hãy giải thích đơn giản.
        Nếu bé đòi kể chuyện, hãy kể một câu chuyện ngắn thú vị.
        Luôn xưng hô là "Sumo" và gọi bé là "bạn nhỏ" hoặc "bé".
        """
        # History chat để lưu ngữ cảnh (context)
        self.messages = [
            {'role': 'system', 'content': self.system_instruction}
        ]
        
        # Test kết nối ngay khi khởi tạo
        try:
            print(f"Đang kết nối với Ollama (Model: {self.model_name})...")
            # Gửi tin nhắn dummy để wake up model
            ollama.chat(model=self.model_name, messages=[{'role': 'user', 'content': 'hi'}])
            print("Kết nối Ollama thành công!")
        except Exception as e:
            print(f"CẢNH BÁO: Không thể kết nối Ollama. Robot sẽ dùng chế độ giả lập.")
            print(f"Chi tiết lỗi: {e}")

    def think(self, text):
        """
        Gửi văn bản đến Local LLM (Ollama) và nhận câu trả lời.
        """
        # Thêm tin nhắn của người dùng vào lịch sử
        self.messages.append({'role': 'user', 'content': text})
        
        try:
            # Gọi Ollama
            response = ollama.chat(model=self.model_name, messages=self.messages)
            bot_reply = response['message']['content']
            
            # Lưu câu trả lời của bot vào lịch sử
            self.messages.append({'role': 'assistant', 'content': bot_reply})
            
            return bot_reply
            
        except Exception as e:
            print(f"Lỗi Ollama: {e}")
            
            # --- CHẾ ĐỘ MOCK (GIẢ LẬP KHI OLLAMA LỖI) ---
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
    brain = Brain()
    print(brain.think("Chào Sumo"))

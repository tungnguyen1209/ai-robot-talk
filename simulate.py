from modules.brain import Brain
from modules.tts import Mouth
import time

def simulate():
    print("--- CHẾ ĐỘ MÔ PHỎNG (CHAT BẰNG PHÍM) ---")
    print("Nhập nội dung và nhấn Enter để trò chuyện. Gõ 'dừng lại' để thoát.")
    
    # Khởi tạo các bộ phận
    print("Đang khởi tạo não bộ và giọng nói...")
    try:
        brain = Brain()
        mouth = Mouth()
    except Exception as e:
        print(f"Lỗi khởi tạo: {e}")
        return

    # Lời chào đầu tiên
    start_msg = "Chào bạn, mình đang ở chế độ mô phỏng. Hãy gõ tin nhắn cho mình nhé."
    mouth.say(start_msg)
    
    while True:
        try:
            # 1. Mô phỏng Nghe (nhập liệu từ bàn phím thay vì mic)
            user_text = input("\nBạn: ")
            
            if not user_text.strip():
                continue
                
            # Kiểm tra lệnh dừng
            if "tạm biệt" in user_text.lower() or "dừng lại" in user_text.lower() or "exit" in user_text.lower():
                bye_msg = "Tạm biệt bạn nhé. Hẹn gặp lại!"
                print(f"Robot: {bye_msg}")
                mouth.say(bye_msg)
                break
                
            # 2. Suy nghĩ
            # print("Robot đang suy nghĩ...") 
            # (Không cần in dòng này nếu muốn giao diện chat sạch hơn, nhưng để debug thì tốt)
            bot_response = brain.think(user_text)
            print(f"Robot: {bot_response}")
            
            # 3. Nói
            mouth.say(bot_response)
            
        except KeyboardInterrupt:
            print("\nĐã dừng chương trình mô phỏng.")
            break
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            break

if __name__ == "__main__":
    simulate()

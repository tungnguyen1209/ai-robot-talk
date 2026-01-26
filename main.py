from modules.stt import Ear
from modules.brain import Brain
from modules.tts import Mouth
import time

def main():
    print("--- KHỞI ĐỘNG ROBOT ---")
    
    # Khởi tạo các bộ phận
    ear = Ear()
    brain = Brain()
    mouth = Mouth()
    
    mouth.say("Xin chào, mình đã sẵn sàng nói chuyện với bạn.")
    time.sleep(1) # Chờ một chút

    while True:
        # 1. Nghe
        user_text = ear.listen()
        
        if not user_text:
            continue
            
        print(f"Người dùng: {user_text}")
        
        # Kiểm tra lệnh dừng
        if "tạm biệt" in user_text.lower() or "dừng lại" in user_text.lower():
            mouth.say("Tạm biệt bạn nhé. Hẹn gặp lại!")
            break
            
        # 2. Suy nghĩ
        bot_response = brain.think(user_text)
        print(f"Robot nghĩ: {bot_response}")
        
        # 3. Nói
        mouth.say(bot_response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")

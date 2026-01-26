import speech_recognition as sr

class Ear:
    def __init__(self, language='vi-VN'):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()
        
        # Điều chỉnh ngưỡng tiếng ồn môi trường
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen(self):
        """
        Lắng nghe từ microphone và trả về văn bản.
        """
        print("Đang nghe...")
        try:
            with self.microphone as source:
                # Nghe lệnh, timeout sau 5s nếu không có tiếng, giới hạn câu nói 10s
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Đang nhận diện...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"Bạn nói: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Không nghe rõ...")
            return None
        except sr.RequestError as e:
            print(f"Lỗi kết nối Google Speech API: {e}")
            return None

if __name__ == "__main__":
    ear = Ear()
    while True:
        text = ear.listen()
        if text:
            if "dừng lại" in text.lower():
                break

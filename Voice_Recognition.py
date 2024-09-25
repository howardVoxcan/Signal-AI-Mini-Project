import speech_recognition as sr
import threading
import keyboard

# Khởi tạo recognizer
r = sr.Recognizer()

# Sự kiện để báo hiệu dừng chương trình
stop_event = threading.Event()

# Biến lưu trữ văn bản cuối cùng
final_text = ""

def listen_and_recognize():
    global final_text
    with sr.Microphone() as source:
        print("Đang lắng nghe... Nhấn 'Enter' để tách đoạn văn bản, 'Backspace' để kết thúc.")
        while not stop_event.is_set():  # Kiểm tra xem có sự kiện dừng không
            try:
                # Lắng nghe âm thanh từ micro mà không có giới hạn thời gian
                audio = r.listen(source)
                # Chuyển đổi âm thanh thành văn bản
                new_text = r.recognize_google(audio, language='vi-VN')
                
                # Kiểm tra các phím đặc biệt
                if keyboard.is_pressed('Enter'):
                    print(new_text + ".")
                elif keyboard.is_pressed('Backspace'):
                    stop_event.set()  # Kết thúc lắng nghe
                    print("Chương trình đã kết thúc. Đoạn văn bản cuối cùng: " + final_text + new_text)
                    return
                elif keyboard.is_pressed('.'):
                    final_text += new_text + "."
                    print("Thêm dấu chấm. " + new_text + ".")
                elif keyboard.is_pressed(','):
                    final_text += new_text + ", "
                    print("Thêm dấu phẩy. " + new_text + ".")
                else:
                    final_text += new_text + " "
                    print(new_text + ".")
                    
            except sr.UnknownValueError:
                print("Không thể nhận dạng âm thanh")
            except sr.RequestError as e:
                print(f"Lỗi khi yêu cầu từ Google Speech Recognition; {e}")
                break
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")

def check_backspace():
    while True:
        if keyboard.is_pressed('Backspace'):
            stop_event.set()
            print("Đã nhấn Backspace. Chương trình sẽ kết thúc.")
            break

def main():
    # Tạo thread để lắng nghe và nhận dạng
    listen_thread = threading.Thread(target=listen_and_recognize)
    listen_thread.start()

    # Tạo thread để kiểm tra phím Backspace
    backspace_thread = threading.Thread(target=check_backspace)
    backspace_thread.start()

    # Đợi cho đến khi người dùng nhấn Backspace để kết thúc chương trình
    listen_thread.join()
    backspace_thread.join()
if __name__ == "__main__":
    main()

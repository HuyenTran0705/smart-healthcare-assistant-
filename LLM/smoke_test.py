# smoke_test.py - test nhanh WS + Face Player
import time
from orchestrator_ws import post_mode, post_talk

print("Send: happy")
post_mode("happy")
time.sleep(1.0)

print("Send: talk_start")
post_talk("start")
time.sleep(1.0)

print("Send: talk_end")
post_talk("end")
time.sleep(0.5)

print("Send: sad")
post_mode("sad")
time.sleep(1.0)

print("Send: neural")
post_mode("neural")
print("Done.")


# # >>> THÊM: import 2 hàm gửi tín hiệu sang mặt
# try:
#     from orchestrator_ws import post_mode, post_talk
# except Exception:
#     # Nếu chưa chạy orchestrator_ws.py thì các lệnh dưới sẽ try/except an toàn
#     def post_mode(mode: str): pass
#     def post_talk(evt: str): pass


# >>> THÊM: bộ từ khoá đơn giản để quyết định mode
# POSITIVE_KWS = ["xin chào","hello","chào","cảm ơn","tốt","tuyệt","vui",
#                 "khỏe","ok","được rồi","chúc mừng","hoan hô","haha","hài","cười"]
# EMPATHY_KWS  = ["buồn","khóc","đau","mệt","lo","sợ","không ổn","không khỏe",
#                 "xin lỗi","thất vọng","khó chịu","nhớ","cô đơn","đau lòng"]

# def pick_mode_vi(user_text: str, assistant_text: str = "") -> str:
#     t = f"{user_text} {assistant_text}".lower()
#     if any(k in t for k in EMPATHY_KWS):
#         return "sad"
#     if any(k in t for k in POSITIVE_KWS):
#         return "happy"
#     return "happy"  # đang nói thì mặc định mặt vui cho thân thiện

# # >>> THÊM: gói phát TTS + điều khiển khuôn mặt
# def speak_with_face(text_vi: str, user_text: str = "", fallback_mode: str = "happy"):
#     mode = pick_mode_vi(user_text, text_vi) if (user_text or text_vi) else fallback_mode
#     try:
#         post_mode(mode)         # chuyển mặt (happy/sad)
#         post_talk("start")      # bắt đầu nói
#     except Exception:
#         pass

#     try:
#         tmp_path = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3")
#         gTTS(text=text_vi, lang='vi').save(tmp_path)
#         pygame.mixer.music.load(tmp_path)
#         pygame.mixer.music.play()
#         clock = pygame.time.Clock()
#         while pygame.mixer.music.get_busy():
#             clock.tick(20)
#     except Exception as e:
#         print("Lỗi phát âm thanh:", e)
#     finally:
#         try:
#             post_talk("end")    # kết thúc nói
#             post_mode("neural") # về idle
#         except Exception:
#             pass
#         try:
#             pygame.mixer.music.unload()
#         except Exception:
#             pass
#         try:
#             if os.path.exists(tmp_path):
#                 os.remove(tmp_path)
#         except Exception:
#             pass


#  # >>> Thay MỌI đoạn phát âm thanh bằng 1 dòng sau:
#     speak_with_face(robot_brain, you, fallback_mode="happy")
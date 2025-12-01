from datetime import date, datetime
import pyttsx3
import speech_recognition as sr

robot_ear = sr.Recognizer()
robot_brain = ""
robot_mouth = pyttsx3.init()

while True:
    with sr.Microphone() as mic:
        print("Robot: Listening...")
        try:
            # Thêm timeout để tránh treo máy
            audio = robot_ear.listen(mic, timeout=5)
            print("Robot: ...")
            you = robot_ear.recognize_google(audio)
        except sr.WaitTimeoutError:
            print("Robot: No speech detected (timeout).")
            you = ""
        except sr.UnknownValueError:
            print("Robot: Could not understand audio.")
            you = ""
        except sr.RequestError as e:
            print(f"Robot: Could not request results; {e}")
            you = ""
        except Exception as e:
            print(f"Robot: Other error: {e}")
            you = ""

    print("You: " + you)

    if you == "":
        robot_brain = "I can't hear you, try again."
    elif "hello" in you:
        robot_brain = "Hello Evelyn, how can I help you today?"
    elif "today" in you:
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    elif "time" in you:
        now = datetime.now()
        robot_brain = now.strftime("%H hours %M minutes %S seconds")
    elif "sad" in you:
        robot_brain = "Don't be sad, I'm here for you."
    elif "bye" in you:
        robot_brain = "Goodbye Evelyn, have a nice day!"
        print("Robot:" + robot_brain)
        robot_mouth.say(robot_brain)
        robot_mouth.runAndWait()
        break
    else:
        robot_brain = "I'm fine thank you and you?"

    print("Robot:" + robot_brain)
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()

# Không cần gọi runAndWait hoặc stop ở cuối nữa

#testtttt
from gtts import gTTS
import speech_recognition as sr
from openai import OpenAI
import pygame, os, time, tempfile
import datetime

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",   
)

robot_ear = sr.Recognizer()
robot_brain = ""
pygame.mixer.init()

# Lịch sử hội thoại 
messages = [
    {"role": "system",
     "content": "Bạn là một trợ lý AI trả lời NGẮN GỌN, không markdown, không ký hiệu đặc biệt, ngữ cảnh là đang ở trong một viện dưỡng lão hoặc bệnh viện."}
]

def trim_history(msgs, max_turns=6):
    """Giữ lại system + tối đa max_turns tin nhắn gần nhất (user/assistant)."""
    sys = [msgs[0]]
    rest = msgs[1:]
    return sys + rest[-max_turns:]


while True:
    with sr.Microphone() as mic:
        print("Robot: Tôi đang nghe...")
        audio = robot_ear.listen(mic)
        print("Robot: ...")

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except:
        you = ""

    print("Bạn:", you)

    #  Thoát khi nghe "tạm biệt"/"bye"
    if "tạm biệt" in you.lower() or "bye" in you.lower():
        goodbye = "Chào tạm biệt! Hẹn gặp lại bạn 👋"
        print("Robot:", goodbye)
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3")
            gTTS(text=goodbye, lang='vi').save(tmp_path)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(10)
            try:
                pygame.mixer.music.unload()
            except:
                pass
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception as e:
            print("Lỗi phát âm thanh:", e)
        break

    normalized = you.lower().strip()

    #  Lệnh reset chủ đề 
    if any(k in normalized for k in ["xóa lịch sử", "reset", "đổi chủ đề", "doi chu de"]):
        messages = messages[:1]  # giữ lại mỗi system
        robot_brain = "Đã xóa lịch sử. Bạn muốn nói về chủ đề nào?"
        print("Robot:" + robot_brain)
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3")
            gTTS(text=robot_brain, lang='vi').save(tmp_path)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(10)
            try:
                pygame.mixer.music.unload()
            except:
                pass
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception as e:
            print("Lỗi phát âm thanh:", e)
        continue

    # Tạo phản hồi tùy chỉnh
    custom_responses = {
        "mấy giờ": lambda: f"Bây giờ là {datetime.datetime.now().strftime('%H:%M:%S')}",
        "đau đầu": lambda: "Hãy thử uống một cốc nước ấm và nghỉ ngơi chút nhé.",
    }

    robot_brain = None
    for key, make_resp in custom_responses.items():
        if key in normalized:          
            robot_brain = make_resp()
            
            messages.append({"role": "user", "content": you})
            messages.append({"role": "assistant", "content": robot_brain})
            messages = trim_history(messages)
            break

    # Nếu không khớp thì fallback sang LLM 
    if robot_brain is None:
        messages.append({"role": "user", "content": you})
        messages = trim_history(messages)
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,         
                max_tokens=200,
                temperature=0.6,
            )
            robot_brain = completion.choices[0].message.content.strip()
        except Exception as e:
            print("Lỗi khi gọi API:", e)
            robot_brain = "Xin lỗi, vui lòng thử lại sau."
        # cập nhật lịch sử với câu trả lời của bot
        messages.append({"role": "assistant", "content": robot_brain})
        messages = trim_history(messages)

    
    print("Robot:" + robot_brain)
    try:
        tmp_path = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3")
        gTTS(text=robot_brain, lang='vi').save(tmp_path)
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        try:
            pygame.mixer.music.unload()
        except:
            pass
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    except Exception as e:
        print("Lỗi phát âm thanh:", e)


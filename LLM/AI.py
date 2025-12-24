from gtts import gTTS
import speech_recognition as sr
from openai import OpenAI
import pygame, os, time, tempfile
from datetime import datetime, date
import locale

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

robot_ear = sr.Recognizer()
robot_brain = ""
pygame.mixer.init()

# mặc định ~0.8s → nới để không cắt sớm khi ngập ngừng
robot_ear.pause_threshold = 1.8
# cho phép im lặng dài hơn giữa câu
robot_ear.non_speaking_duration = 1.0


def get_vietnamese_date():
    weekdays = {
        0: "Thứ Hai",
        1: "Thứ Ba",
        2: "Thứ Tư",
        3: "Thứ Năm",
        4: "Thứ Sáu",
        5: "Thứ Bảy",
        6: "Chủ Nhật",
    }
    today = datetime.now()
    thu = weekdays[today.weekday()]
    return f"Hôm nay là {thu}, ngày {today.day} tháng {today.month} năm {today.year}"


# Đặt locale sang tiếng Việt để hiển thị thứ/ngày bằng tiếng Việt
try:
    locale.setlocale(locale.LC_TIME, "vi_VN.UTF-8")
except:
    # Nếu máy Windows không có gói locale vi_VN, sẽ fallback sang mặc định
    pass

# Lịch sử hội thoại
messages = [
    {
        "role": "system",
        "content": "Bạn là một trợ lý AI hỗ trợ các điều dưỡng ở viện dưỡng lão hãy trả lời NGẮN GỌN, không markdown, không ký hiệu đặc biệt.",
    }
]


def trim_history(msgs, max_turns=6):
    """Giữ lại system + tối đa max_turns tin nhắn gần nhất (user/assistant)."""
    sys = [msgs[0]]
    rest = msgs[1:]
    return sys + rest[-max_turns:]


while True:
    with sr.Microphone() as mic:
        # cân chỉnh chống ồn 1s để threshold hợp lý
        robot_ear.adjust_for_ambient_noise(mic, duration=1.0)
        print("Robot: Tôi đang nghe...")
        audio = robot_ear.listen(mic, timeout=8, phrase_time_limit=12)
        print("Robot: ...")

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except:
        you = ""

    print("Bạn:", you)

    # Thoát khi nghe "tạm biệt"/"bye"
    if "tạm biệt" in you.lower() or "bye" in you.lower():
        goodbye = "Chào tạm biệt! Hẹn gặp lại bạn 👋"
        print("Robot:", goodbye)
        try:
            tmp_path = os.path.join(
                tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3"
            )
            gTTS(text=goodbye, lang="vi").save(tmp_path)
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

    # Lệnh reset chủ đề
    if any(k in normalized for k in ["xóa lịch sử", "reset", "đổi chủ đề", "doi chu de"]):
        messages = messages[:1]  # giữ lại mỗi system
        robot_brain = "Đã xóa lịch sử. Bạn muốn nói về chủ đề nào?"
        print("Robot:" + robot_brain)
        try:
            tmp_path = os.path.join(
                tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3"
            )
            gTTS(text=robot_brain, lang="vi").save(tmp_path)
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
        "mấy giờ": lambda: f"Bây giờ là {datetime.now().strftime('%H:%M:%S')}",
        "ngày mấy": get_vietnamese_date,
        "hôm nay": get_vietnamese_date,
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
                temperature=0.7,
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
        tmp_path = os.path.join(
            tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.mp3"
        )
        gTTS(text=robot_brain, lang="vi").save(tmp_path)
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


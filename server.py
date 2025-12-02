from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from datetime import datetime
import locale

# --- CẤU HÌNH CỦA BẠN ---
# Lưu ý: Điền API Key của bạn vào dấu ngoặc kép bên dưới
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="", 
)

app = Flask(__name__)
CORS(app)  # Cho phép HTML kết nối


# Đặt locale sang tiếng Việt
try:
    locale.setlocale(locale.LC_TIME, "vi_VN.UTF-8")
except:
    pass

def get_vietnamese_date():
    weekdays = {
        0: "Thứ Hai", 1: "Thứ Ba", 2: "Thứ Tư", 3: "Thứ Năm",
        4: "Thứ Sáu", 5: "Thứ Bảy", 6: "Chủ Nhật",
    }
    today = datetime.now()
    thu = weekdays[today.weekday()]
    return f"Hôm nay là {thu}, ngày {today.day} tháng {today.month} năm {today.year}"

# Lịch sử hội thoại (Lưu trong RAM khi server chạy)
messages = [
    {
        "role": "system",
        "content": "Bạn là một trợ lý AI hỗ trợ các điều dưỡng ở viện dưỡng lão hãy trả lời NGẮN GỌN, không markdown, không ký hiệu đặc biệt.",
    }
]

def trim_history(msgs, max_turns=6):
    """Giữ lại system + tối đa max_turns tin nhắn gần nhất."""
    sys = [msgs[0]]
    rest = msgs[1:]
    return sys + rest[-max_turns:]

# --- HÀM XỬ LÝ CHÍNH (Thay thế cho vòng lặp while True cũ) ---
def process_ai_logic(user_text):
    global messages # Dùng biến toàn cục để nhớ lịch sử chat
    
    normalized = user_text.lower().strip()
    robot_brain = None

    # 1. Xử lý lệnh Reset/Xóa lịch sử
    if any(k in normalized for k in ["xóa lịch sử", "reset", "đổi chủ đề", "doi chu de"]):
        messages = messages[:1]  # Reset về tin nhắn system ban đầu
        return "Đã xóa lịch sử. Bạn muốn nói về chủ đề nào?"

    # 2. Xử lý các câu hỏi Custom (Ngày giờ, sức khỏe...)
    custom_responses = {
        "mấy giờ": lambda: f"Bây giờ là {datetime.now().strftime('%H:%M:%S')}",
        "ngày mấy": get_vietnamese_date,
        "hôm nay": get_vietnamese_date,
        "đau đầu": lambda: "Hãy thử uống một cốc nước ấm và nghỉ ngơi chút nhé.",
    }

    for key, make_resp in custom_responses.items():
        if key in normalized:
            robot_brain = make_resp()
            # Cập nhật lịch sử
            messages.append({"role": "user", "content": user_text})
            messages.append({"role": "assistant", "content": robot_brain})
            messages = trim_history(messages)
            return robot_brain

    # 3. Nếu không trúng custom, gọi OpenAI/OpenRouter
    if robot_brain is None:
        messages.append({"role": "user", "content": user_text})
        messages = trim_history(messages)
        
        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free", 
                messages=messages,
                max_tokens=200,
                temperature=0.7,
            )
            robot_brain = completion.choices[0].message.content.strip()
        except Exception as e:
            print("Lỗi API:", e)
            robot_brain = "Xin lỗi, hệ thống đang bận, vui lòng thử lại sau."

        # Lưu câu trả lời vào lịch sử
        messages.append({"role": "assistant", "content": robot_brain})
        messages = trim_history(messages)
        
    return robot_brain


# --- API ENDPOINT (Cổng giao tiếp với HTML) ---
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_text = data.get('message', '')
    
    print(f"Nhận từ HTML: {user_text}") # Log để kiểm tra

    if not user_text:
        return jsonify({'reply': 'Tôi không nghe rõ.'})

    # Gọi hàm xử lý logic ở trên
    response_text = process_ai_logic(user_text)
    
    print(f"Trả về HTML: {response_text}") # Log để kiểm tra

    # Trả kết quả về cho HTML (để HTML tự đọc)
    return jsonify({'reply': response_text})

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    print("Server AI đang chạy... Hãy mở file index.html lên!")

    app.run(host='0.0.0.0', port=5000, debug=True)

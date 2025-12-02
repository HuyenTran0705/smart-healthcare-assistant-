document.addEventListener('DOMContentLoaded', () => {
    // ==============================================
    // KHAI BÁO BIẾN (UI ELEMENTS)
    // ==============================================
    
    // Màn hình chính & Voice
    const homeScreen = document.getElementById('home-screen');
    const voiceScreen = document.getElementById('voice-screen');
    const startVoiceBtn = document.getElementById('start-voice-btn');
    const backBtn = document.getElementById('back-btn');
    
    const voiceContainer = document.querySelector('.voice-interface-container');
    const micToggleBtn = document.getElementById('mic-toggle-btn');
    const voiceStatus = document.getElementById('voice-status');
    const transcriptText = document.getElementById('transcript-text');

    let isListening = false;

    // Nút chức năng & Modal
    const adminBtn = document.getElementById('admin-btn');
    const medBtn = document.getElementById('med-btn');
    
    // Modal Mật khẩu
    const passwordModal = document.getElementById('password-modal');
    const passInput = document.getElementById('admin-password');
    const confirmPassBtn = document.getElementById('confirm-pass-btn');
    const cancelPassBtn = document.getElementById('cancel-pass-btn');

    // Modal Thuốc
    const medModal = document.getElementById('med-modal');
    const medYesBtn = document.getElementById('med-yes-btn');
    const medNoBtn = document.getElementById('med-no-btn');
    const closeMedBtn = document.getElementById('close-med-btn');


    // ==============================================
    // 1. PHẦN ĐIỀU HƯỚNG MÀN HÌNH CHÍNH
    // ==============================================
    startVoiceBtn.addEventListener('click', () => {
        homeScreen.classList.remove('active');
        voiceScreen.classList.add('active');
        // Tự động bật mic sau 0.5s
        setTimeout(startListeningState, 500);
    });

    backBtn.addEventListener('click', () => {
        stopListeningState();
        voiceScreen.classList.remove('active');
        homeScreen.classList.add('active');
    });

    micToggleBtn.addEventListener('click', () => {
        if (isListening) {
            stopListeningState();
        } else {
            startListeningState();
        }
    });

    // ==============================================
    // 2. PHẦN XỬ LÝ CÁC NÚT CHỨC NĂNG (Admin/Thuốc)
    // ==============================================

    // --- A. Logic cho nút QUẢN LÝ (Admin) ---
    adminBtn.addEventListener('click', () => {
        passwordModal.classList.add('show');
        passInput.value = ''; 
        passInput.focus();
    });

    cancelPassBtn.addEventListener('click', () => {
        passwordModal.classList.remove('show');
    });

    // Nút Xác nhận pass
    confirmPassBtn.addEventListener('click', () => {
        const password = passInput.value;
        
        // KIỂM TRA MẬT KHẨU
        if (password === '1234') {
            passwordModal.classList.remove('show'); // Tắt popup
            
            // --- LOGIC CHUYỂN TRANG ---
            
            // 1. Nếu đang chạy trong App Mobile (Flutter Mobile)
            if (window.ManagementChannel) {
                window.ManagementChannel.postMessage('open_management_ui');
            } 
            // 2. Nếu đang chạy nhúng trong Iframe (Flutter Web dạng tích hợp)
            else if (window.parent !== window) {
                window.parent.postMessage('open_management_ui', '*');
            }
            // 3. Nếu đang chạy 2 tab riêng biệt trên trình duyệt
            else {
                alert("Mật khẩu đúng! Đang chuyển sang trang Quản lý...");
                
                // 👇 QUAN TRỌNG: Link này phải là link tab Flutter đang chạy
                // Thường Flutter Web chạy ở port 8080. Hãy kiểm tra lại trình duyệt của bạn.
                window.location.href = 'http://localhost:8080'; 
            }

        } else {
            alert("Mật khẩu không đúng!");
            passInput.value = '';
        }
    });


    // --- B. Logic cho nút XÁC NHẬN THUỐC ---
    medBtn.addEventListener('click', () => {
        medModal.classList.add('show');
    });

    closeMedBtn.addEventListener('click', () => {
        medModal.classList.remove('show');
    });

    medYesBtn.addEventListener('click', () => {
        alert("Đã ghi nhận: Bệnh nhân ĐÃ uống thuốc ✅");
        medModal.classList.remove('show');
        // Có thể gửi log về Python ở đây nếu muốn
    });

    medNoBtn.addEventListener('click', () => {
        alert("Cảnh báo: Bệnh nhân CHƯA uống thuốc ❌");
        medModal.classList.remove('show');
    });


    // ==============================================
    // 3. CÁC HÀM XỬ LÝ GIỌNG NÓI (KẾT NỐI PYTHON THẬT)
    // ==============================================

    // Hàm BẬT trạng thái nghe
    function startListeningState() {
        isListening = true;
        voiceContainer.classList.add('listening');
        voiceStatus.textContent = "Đang lắng nghe bạn...";
        transcriptText.textContent = "...";

        // Sử dụng Web Speech API của trình duyệt
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!Recognition) {
            alert("Trình duyệt này không hỗ trợ nhận diện giọng nói. Hãy dùng Chrome.");
            return;
        }

        const recognition = new Recognition();
        recognition.lang = 'vi-VN'; // Ngôn ngữ tiếng Việt
        recognition.start();

        // KHI NHẬN DIỆN XONG
        recognition.onresult = function(event) {
            const userSpeech = event.results[0][0].transcript;
            transcriptText.textContent = `Bạn: "${userSpeech}"`;
            
            stopListeningState();
            voiceStatus.textContent = "Đang suy nghĩ...";

            // Gửi dữ liệu sang Python xử lý
            sendToPython(userSpeech);
        };

        // KHI CÓ LỖI HOẶC KHÔNG NGHE THẤY
        recognition.onerror = function(event) {
            console.error("Lỗi voice:", event.error);
            stopListeningState();
            voiceStatus.textContent = "Không nghe rõ. Nhấn micro thử lại.";
        };

        // KHI MICRO TỰ NGẮT
        recognition.onend = function() {
            if (isListening) {
                stopListeningState();
            }
        };
    }

    // Hàm TẮT trạng thái nghe
    function stopListeningState() {
        isListening = false;
        voiceContainer.classList.remove('listening');
        if (voiceStatus.textContent === "Đang lắng nghe bạn...") {
             voiceStatus.textContent = "Đang xử lý...";
        }
    }

    // Hàm gửi tin nhắn sang Python Server (localhost:5000)
    async function sendToPython(text) {
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            const aiReply = data.reply;

            // Hiển thị câu trả lời
            transcriptText.textContent = `AI: "${aiReply}"`;
            
            // Robot đọc to câu trả lời (Dùng hàm speak mới)
            speak(aiReply);

        } catch (error) {
            console.error("Lỗi kết nối Python:", error);
            transcriptText.textContent = "Lỗi: Chưa bật file server.py!";
        }
    }

    // ==============================================
    // [QUAN TRỌNG] HÀM ĐỌC GIỌNG NÓI (TEXT-TO-SPEECH)
    // Đã nâng cấp để chọn đúng giọng Tiếng Việt
    // ==============================================
    function speak(text) {
        // Ngắt lời nếu đang nói câu cũ
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        
        // Lấy danh sách giọng đọc có sẵn trong máy/trình duyệt
        const voices = window.speechSynthesis.getVoices();
        
        // Tìm giọng ưu tiên: Google Tiếng Việt > Microsoft An > Bất kỳ giọng 'vi-VN' nào
        const vnVoice = voices.find(v => v.name.includes('Google') && v.lang.includes('vi')) 
                     || voices.find(v => v.lang === 'vi-VN') 
                     || voices.find(v => v.name.includes('Vietnamese'));

        if (vnVoice) {
            utterance.voice = vnVoice; // Ép dùng giọng Việt tìm được
            // console.log("Đang đọc bằng giọng: " + vnVoice.name);
        } else {
            utterance.lang = 'vi-VN'; // Fallback nếu không tìm thấy
        }
        
        // Hiệu ứng robot nhỏ nhún nhảy khi nói
        const smallRobot = document.querySelector('.small-robot');
        if(smallRobot) smallRobot.classList.add('talking');

        utterance.onend = function() {
            if(smallRobot) smallRobot.classList.remove('talking');
            voiceStatus.textContent = "Nhấn micro để nói tiếp.";
        };

        utterance.onerror = function(e) {
            console.error("Lỗi đọc:", e);
        };

        window.speechSynthesis.speak(utterance);
    }

    // Sự kiện này giúp Chrome load danh sách giọng (fix lỗi lần đầu không có tiếng)
    window.speechSynthesis.onvoiceschanged = function() {
        window.speechSynthesis.getVoices();
    };
});

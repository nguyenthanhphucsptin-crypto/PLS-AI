import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN SIÊU DỄ THƯƠNG
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

# Lời chào mặc định
welcome_message = """
✨ **PLS xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖
"""

# ==========================================
# 2. KHỞI TẠO BỘ NHỚ LƯU TRỮ NHIỀU ĐOẠN CHAT
# ==========================================
# Tạo một cuốn sổ lưu tất cả các đoạn chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {"Đoạn chat 1": [{"role": "assistant", "content": welcome_message}]}

# Theo dõi xem người dùng đang mở đoạn chat nào
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "Đoạn chat 1"

# Bộ đếm số lượng đoạn chat đã tạo
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1

# ==========================================
# 3. THANH SIDEBAR (MENU BÊN TRÁI)
# ==========================================
with st.sidebar:
    st.markdown("### 💬 Lịch sử trò chuyện")
    
    # Nút Tạo đoạn chat mới
    if st.button("➕ Tạo đoạn chat mới", use_container_width=True):
        st.session_state.chat_counter += 1
        new_name = f"Đoạn chat {st.session_state.chat_counter}"
        # Tạo phòng chat mới với lời chào mặc định
        st.session_state.chat_history[new_name] = [{"role": "assistant", "content": welcome_message}]
        # Chuyển sang phòng chat vừa tạo
        st.session_state.current_chat_name = new_name
        st.rerun() # Tải lại trang để cập nhật giao diện
        
    st.markdown("---")
    st.markdown("**Các cuộc trò chuyện:**")
    
    # Hiển thị danh sách các đoạn chat dưới dạng nút bấm
    for chat_name in list(st.session_state.chat_history.keys()):
        # Thêm icon 👉 để biết đang ở phòng chat nào
        prefix = "👉" if chat_name == st.session_state.current_chat_name else "💭"
        if st.button(f"{prefix} {chat_name}", key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat_name = chat_name
            st.rerun()
            
    st.markdown("---")
    
    # Nút Xóa lịch sử cuộc trò chuyện HIỆN TẠI
    if st.button("🗑️ Xóa sạch chat hiện tại", type="primary", use_container_width=True):
        st.session_state.chat_history[st.session_state.current_chat_name] = [{"role": "assistant", "content": welcome_message}]
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 💌 Hỗ Trợ Kỹ Thuật")
    st.markdown("👨‍💻 **Nguyễn Thanh Phúc**\n\n📞 **SĐT:** 0367102957\n\n🏫 **Đại Học Cần Thơ**")

# ==========================================
# 4. CẤU HÌNH AI & TÍNH NĂNG TỰ ĐỔI KEY DỰ PHÒNG
# ==========================================
now = datetime.now()
days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
thu_hom_nay = days_vi.get(now.strftime("%A"), "")
thoi_gian_thuc = f"{thu_hom_nay}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

instruction = f"""
Bạn là trợ lý AI thông minh, gia sư nhiệt tình của PLS.
- CÁCH XƯNG HÔ: xưng "mình", gọi "bạn". 
- NGÔN NGỮ: 100% tiếng Việt chuẩn. Tuyệt đối KHÔNG chèn chữ Hán, chữ Nôm.
- THỜI GIAN HIỆN TẠI: {thoi_gian_thuc}.
- TÍNH CÁCH: tự nhiên, nhẹ nhàng, lịch sự, siêu đáng yêu.
- KỸ NĂNG: Khuyến khích & Lắng nghe, Giải thích từng bước.
"""

api_keys = []
for k in ["GOOGLE_API_KEY", "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3"]:
    val = st.secrets.get(k)
    if val and val not in api_keys:
        api_keys.append(val)

if not api_keys:
    st.error("Trùi ui, chưa được cấp API Key rồi!")
    st.stop()

# Hàm AI gửi tin nhắn thông minh
def generate_response_with_fallback(user_prompt, current_messages):
    formatted_history = []
    # Đọc lại lịch sử của riêng phòng chat hiện tại để AI nhớ
    for msg in current_messages[:-1]: # Bỏ qua câu hỏi vừa hỏi
        if msg["role"] == "user":
            formatted_history.append({"role": "user", "parts": [msg["content"]]})
        elif msg["role"] == "assistant":
            formatted_history.append({"role": "model", "parts": [msg["content"]]})

    last_error = None
    for key in api_keys:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=instruction)
            chat = model.start_chat(history=formatted_history)
            response = chat.send_message(user_prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue 
            
    raise last_error

# ==========================================
# 5. HIỂN THỊ KHUNG CHAT (Của đoạn chat đang chọn)
# ==========================================
# Lấy danh sách tin nhắn của phòng chat hiện tại
current_messages = st.session_state.chat_history[st.session_state.current_chat_name]

# In các tin nhắn cũ ra màn hình
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Khi người dùng nhập tin nhắn mới
if prompt := st.chat_input("Nhắn tin cho mình ở đây nha... ⌨️"):
    # Lưu vào danh sách
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đợi mình chút xíu nha, mình đang suy nghĩ... 💭"):
            try:
                # Trả lời dựa trên lịch sử của riêng phòng này
                answer = generate_response_with_fallback(prompt, current_messages)
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Huhu mình bị lỗi mất rồi: {e}")

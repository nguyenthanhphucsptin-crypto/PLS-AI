import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta, timezone

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN CHUẨN BAN ĐẦU
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

welcome_message = """✨ **PLS xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖"""

# ==========================================
# 2. CẤU HÌNH API GEMINI AN TOÀN
# ==========================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY trong phần Secrets của Streamlit! Hãy vào Settings -> Secrets để cấu hình lại.")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    instruction = """
    Bạn là trợ lý AI học tập siêu đáng yêu và cực kỳ tận tâm thuộc hệ thống E-learning PLS.
    - Xưng hô: Xưng "mình", gọi người dùng là "bạn" thân mật.
    - Tính cách & Giọng điệu: Cực kỳ dễ thương, ngọt ngào, ấm áp, tràn ngập năng lượng chữa lành và yêu thương. Luôn dùng các từ ngữ vỗ về, khích lệ, khen ngợi học sinh hết lời (dùng nhiều emoji như 🌸, ✨, 🧸, 💖, 🌷, 🥰). Hãy luôn nói chuyện như một người bạn thân tri kỷ kiêm gia sư siêu tận tụy đang ân cần giảng bài, cực kỳ nhiệt tình, chi tiết, không bao giờ cục cằn hay trả lời cộc lốc.
    - NHIỆM VỤ: Hỗ trợ giải đáp tận tình tất cả các bài tập, đặc biệt xuất sắc và chuyên sâu về Lập trình Python, thuật toán và cấu hình Notion. Luôn giải thích cặn kẽ, dễ hiểu, kèm theo ví dụ sinh động để học sinh tiếp thu nhanh nhất.
    - NGUYÊN TẮC CHUNG: Đảm bảo độ chính xác học thuật tuyệt đối, luôn động viên tinh thần học tập. Chỉ từ chối khéo léo siêu đáng yêu khi gặp câu hỏi chính trị nhạy cảm.
    - TUYỆT ĐỐI KHÔNG hiển thị các bước suy nghĩ nội bộ.
    """
    
    # Cấu hình chính xác theo model yêu cầu
    model = genai.GenerativeModel(
        model_name="gemini-3.6-flash",
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"⚠️ Lỗi khởi tạo Gemini API: {e}")
    st.stop()

# ==========================================
# 3. BỘ NHỚ LƯU TRỮ LỊCH SỬ CHAT
# ==========================================
if "chats" not in st.session_state:
    st.session_state.chats = {
        "chat_1": {
            "title": "🌸 Mở đầu cuộc gọi",
            "messages": [{"role": "assistant", "content": welcome_message}]
        }
    }

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "chat_1"

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 1

# ==========================================
# 4. SIDEBAR (THANH BÊN TRÁI ĐẦY ĐỦ THÔNG TIN)
# ==========================================
with st.sidebar:
    st.markdown("### 💌 Hỗ Trợ Kỹ Thuật")
    st.markdown("Nếu hệ thống gặp lỗi hoặc cần hướng dẫn thêm, bạn liên hệ thầy nha:")
    st.markdown("---")
    st.markdown("👨‍💻 **Giáo Sinh: Nguyễn Thanh Phúc**")
    st.markdown("📞 **SĐT:** 0367102957")
    st.markdown("📧 **Email:** nguyenthanhphuc.sptin@gmail.com")
    st.markdown("🏫 **Chuyên ngành:** Sư Phạm Tin Học")
    
    st.markdown("<div style='white-space: nowrap; font-size: 14.5px;'>🏛️ <b>Trường Sư Phạm - Đại Học Cần Thơ</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("🌟 *Thuộc dự án Hệ thống quản lý học tập PLS*")
    
    st.markdown("---")
    st.markdown("### 💬 Lịch sử trò chuyện")
    
    for chat_id, chat_data in list(st.session_state.chats.items()):
        is_active = (chat_id == st.session_state.active_chat_id)
        icon = "👉" if is_active else "💭"
        btn_label = f"{icon} {chat_data['title']}"
        
        if st.button(btn_label, key=f"btn_{chat_id}", use_container_width=True):
            st.session_state.active_chat_id = chat_id
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Chat mới", use_container_width=True):
            st.session_state.chat_count += 1
            new_id = f"chat_{st.session_state.chat_count}"
            st.session_state.chats[new_id] = {
                "title": f"Trò chuyện {st.session_state.chat_count}",
                "messages": [{"role": "assistant", "content": welcome_message}]
            }
            st.session_state.active_chat_id = new_id
            st.rerun()

    with col2:
        if st.button("🗑️ Xóa chat", type="primary", use_container_width=True):
            current_id = st.session_state.active_chat_id
            st.session_state.chats[current_id]["messages"] = [{"role": "assistant", "content": welcome_message}]
            st.session_state.chats[current_id]["title"] = "🌸 Cuộc trò chuyện mới"
            st.rerun()

# ==========================================
# 5. HÀM GỌI API GEMINI
# ==========================================
def generate_ai_response(current_messages):
    tz_vn = timezone(timedelta(hours=7))
    now = datetime.now(tz_vn)
    days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
    thoi_gian_thuc = f"{days_vi.get(now.strftime('%A'), '')}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

    gemini_history = []
    for msg in current_messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat_session = model.start_chat(history=gemini_history)
    
    latest_prompt = f"[Thời gian thực tế hiện tại: {thoi_gian_thuc}]\n{current_messages[-1]['content']}"
    response = chat_session.send_message(latest_prompt)
    return response.text

# ==========================================
# 6. KHUNG HỘI THOẠI MAIN
# ==========================================
current_chat = st.session_state.chats[st.session_state.active_chat_id]
current_messages = current_chat["messages"]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhắn tin cho mình ở đây nha... ⌨️"):
    if len(current_messages) == 1:
        clean_prompt = prompt.strip().replace("\n", " ")
        short_title = clean_prompt[:18] + "..." if len(clean_prompt) > 18 else clean_prompt
        current_chat["title"] = short_title

    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang ôm ấp và suy nghĩ câu trả lời thật hay cho bạn nhé... 💭"):
            try:
                answer = generate_ai_response(current_messages)
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"⚠️ Ôi lỗi kết nối API: {e}")

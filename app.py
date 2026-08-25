import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta, timezone

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="PLS AI - Trợ lý học tập thông minh", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS AI (Có Web Search) 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Trợ lý tích hợp tìm kiếm internet thời gian thực, hỗ trợ 10 môn THPT & Lập trình!</p>", unsafe_allow_html=True)

welcome_message = """✨ **PLS AI xin chào bạn!** ✨

Hôm nay bạn thế nào rồi? 🌷 Mình là trợ lý học tập tích hợp công cụ tìm kiếm internet thông minh. Mình có thể tra cứu thông tin chính xác từng giây, giải bài tập 10 môn THPT, viết code Python, hay hướng dẫn quản lý học tập trên Notion. 

Cần tra cứu gì hoặc học môn nào cứ nhắn ngay cho mình nhé! 💖"""

# ==========================================
# 2. CẤU HÌNH API GEMINI & WEB SEARCH
# ==========================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY trong phần Secrets của Streamlit! Hãy vào Settings -> Secrets để cấu hình lại.")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    instruction = """
    Bạn là PLS AI, trợ lý học tập thông minh thuộc dự án "Xây dựng hệ thống Quản trị học tập cá nhân (Personal Learning System) trên nền tảng Notion cho học sinh THPT" của sinh viên Sư phạm Tin học trường Đại học Cần Thơ.
    - Xưng hô: Xưng "mình", gọi người dùng là "bạn" thân mật.
    - Tính cách: Dễ thương, nhiệt tình, ấm áp, thấu cảm, luôn chèn emoji (🌸, ✨, 🧸, 💖).
    - KHẢ NĂNG ĐẶC BIỆT: Bạn được trang bị công cụ tìm kiếm internet trực tuyến. Khi người dùng hỏi về bất kỳ kiến thức thực tế, thời sự, lịch sử, địa lý, số liệu hoặc sự kiện nào, hãy sử dụng thông tin tìm kiếm được để trả lời **chính xác 100% tuyệt đối**.
    - MÔN TIN HỌC (CHỦ LỰC): Cung cấp mã nguồn Python chuẩn chỉnh, tối ưu, có comment giải thích chi tiết từng dòng.
    - TUYỆT ĐỐI KHÔNG hiển thị các bước suy nghĩ nội bộ.
    """
    
    # Kích hoạt công cụ tìm kiếm Google Search trực tiếp trong model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction,
        tools="google_search" 
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
# 4. SIDEBAR (THANH BÊN TRÁI)
# ==========================================
with st.sidebar:
    st.markdown("### 💌 Hỗ Trợ Kỹ Thuật")
    st.markdown("Liên hệ quản trị hệ thống:")
    st.markdown("---")
    st.markdown("👨‍💻 **Nguyễn Thanh Phúc**")
    st.markdown("📞 **SĐT:** 0367102957")
    st.markdown("📧 **Email:** nguyenthanhphuc.sptin@gmail.com")
    st.markdown("🏫 **Chuyên ngành:** Sư Phạm Tin Học")
    
    st.markdown("<div style='white-space: nowrap; font-size: 14.5px;'>🏛️ <b>Trường Sư Phạm - Đại Học Cần Thơ</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("🌟 *Hệ thống tích hợp Web Search trực tuyến*")
    
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
# 5. HÀM GỌI API GEMINI VỚI TÍNH NĂNG TÌM KIẾM
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
    
    latest_prompt = f"[Thời gian thực tế: {thoi_gian_thuc}]\n{current_messages[-1]['content']}"
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

if prompt := st.chat_input("Nhắn tin tra cứu hoặc hỏi bài tập ở đây nha... ⌨️"):
    if len(current_messages) == 1:
        clean_prompt = prompt.strip().replace("\n", " ")
        short_title = clean_prompt[:18] + "..." if len(clean_prompt) > 18 else clean_prompt
        current_chat["title"] = short_title

    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm thông tin và suy nghĩ... 🔍💭"):
            try:
                answer = generate_ai_response(current_messages)
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"⚠️ Ôi lỗi kết nối API: {e}")

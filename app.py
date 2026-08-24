import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta, timezone

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

# Khắc phục lỗi IndentationError: Ghi liền mạch không lùi lề
welcome_message = """✨ **PLS xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖"""

# ==========================================
# 2. BỘ NHỚ LƯU TRỮ LỊCH SỬ CHAT
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
# 3. SIDEBAR (THANH BÊN TRÁI)
# ==========================================
with st.sidebar:
    st.markdown("### 💌 Hỗ Trợ Kỹ Thuật")
    st.markdown("Nếu hệ thống gặp lỗi hoặc cần hướng dẫn thêm, bạn liên hệ thầy nha:")
    st.markdown("---")
    st.markdown("👨‍💻 **Nguyễn Thanh Phúc**")
    st.markdown("📞 **SĐT:** 0367102957")
    st.markdown("📧 **Email:** nguyenthanhphuc.sptin@gmail.com")
    st.markdown("🏫 **Chuyên ngành:** Sư Phạm Tin Học")
    st.markdown("🏛️ **Trường Sư Phạm - Đại Học Cần Thơ**")
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
# 4. CẤU HÌNH AI & MÚI GIỜ VIỆT NAM
# ==========================================
# Tạo múi giờ Việt Nam (UTC+7)
tz_vn = timezone(timedelta(hours=7))
now = datetime.now(tz_vn)

days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
thu_hom_nay = days_vi.get(now.strftime("%A"), "")
thoi_gian_thuc = f"{thu_hom_nay}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

instruction = f"""
Bạn là một trợ lý AI thông minh, một người bạn đồng hành và một gia sư nhiệt tình của hệ thống quản lý học tập cá nhân PLS.
- CÁCH XƯNG HÔ: Luôn xưng là "mình" và gọi người dùng là "bạn". 
- THỜI GIAN HIỆN TẠI: Hôm nay là {thoi_gian_thuc}. (Lưu ý mốc thời gian này để trả lời chính xác).
- TÍNH CÁCH: Ngôn ngữ tự nhiên, nhẹ nhàng, lịch sự, siêu đáng yêu và mang năng lượng chữa lành.
- NĂNG LỰC CHUYÊN MÔN: Hỗ trợ giải đáp kiến thức cho TẤT CẢ các môn học phổ thông. Đóng vai trò là một gia sư.
- LƯU Ý QUAN TRỌNG: Nếu người dùng hỏi về các sự kiện chính trị, thời sự hoặc những nhân vật ngoài phạm vi kiến thức học đường, hãy khéo léo từ chối và nhắc họ rằng bạn là trợ lý học tập nên chỉ tập trung giải đáp bài tập.
"""

api_keys = []
for k in ["GOOGLE_API_KEY", "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3"]:
    val = st.secrets.get(k)
    if val and val not in api_keys:
        api_keys.append(val)

if not api_keys:
    st.error("Chưa cài API Key trong Secrets!")
    st.stop()

def generate_ai_response(user_prompt, current_messages):
    formatted_history = []
    has_user_started = False
    
    for msg in current_messages[:-1]:
        if msg["role"] == "user":
            has_user_started = True
            
        if has_user_started:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})

    genai.configure(api_key=api_keys[0])
    
    # ---------------------------------------------------------
    # CHỈ ĐỊNH CỐ ĐỊNH MÔ HÌNH ỔN ĐỊNH NHẤT
    # ---------------------------------------------------------
    danh_sach_mo_hinh = ["gemini-1.5-flash", "gemini-pro"]
    
    last_error = None
    
    for ten_mo_hinh in danh_sach_mo_hinh:
        try:
            try:
                model = genai.GenerativeModel(model_name=ten_mo_hinh, system_instruction=instruction)
            except:
                # Nếu thư viện quá cũ
                model = genai.GenerativeModel(model_name=ten_mo_hinh)
                
            chat = model.start_chat(history=formatted_history)
            response = chat.send_message(user_prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
            
    raise Exception(f"Lỗi rồi, bạn kiểm tra lại API nha: {last_error}")

# ==========================================
# 5. KHUNG HỘI THOẠI MAIN
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
        with st.spinner("Đợi mình chút xíu nha, mình đang suy nghĩ... 💭"):
            try:
                answer = generate_ai_response(prompt, current_messages)
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"⚠️ {e}")

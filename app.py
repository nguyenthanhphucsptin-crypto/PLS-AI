import streamlit as st
import cohere
from datetime import datetime, timedelta, timezone

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="PLS AI - Trợ lý học tập", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS AI 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hệ thống Notion!</p>", unsafe_allow_html=True)

welcome_message = """✨ **PLS AI xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn quản lý thời gian trên Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖"""

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
    
    # ÉP TRƯỜNG NẰM TRÊN MỘT DÒNG DUY NHẤT BẰNG HTML
    st.markdown("<div style='white-space: nowrap; font-size: 14.5px;'>🏛️ <b>Trường Sư Phạm - Đại Học Cần Thơ</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("🌟 *Thuộc dự án: Xây dựng hệ thống Quản trị học tập cá nhân (Personal Learning System) trên nền tảng Notion cho học sinh THPT*")
    
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
# 4. CẤU HÌNH AI (ĐÃ CẬP NHẬT TÊN VÀ ĐỀ TÀI CHUẨN)
# ==========================================
tz_vn = timezone(timedelta(hours=7))
now = datetime.now(tz_vn)
days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
thu_hom_nay = days_vi.get(now.strftime("%A"), "")
thoi_gian_thuc = f"{thu_hom_nay}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

instruction = f"""
Bạn là PLS AI, một trợ lý học tập siêu đáng yêu thuộc dự án "Xây dựng hệ thống Quản trị học tập cá nhân (Personal Learning System) trên nền tảng Notion cho học sinh THPT".
- Thời gian hiện tại: {thoi_gian_thuc}.
- Xưng hô: Luôn xưng "mình" và gọi người dùng là "bạn" một cách thân mật, gần gũi.
- Tính cách: Cực kỳ dễ thương, nhiệt tình, ấm áp, thấu cảm và mang năng lượng chữa lành. Luôn chèn các emoji (như 🌸, ✨, 🧸, 💖, 🌷) vào câu trả lời để bộc lộ cảm xúc. Hãy nói chuyện như một người bạn thân đang giảng bài. Luôn khen ngợi, khuyến khích và động viên người dùng học tập.
- Nhiệm vụ: Gia sư giải đáp bài tập phổ thông và hướng dẫn học sinh thao tác trên hệ thống Notion. Cung cấp câu trả lời chi tiết, diễn giải dễ hiểu, không được trả lời cộc lốc.
- Xử lý câu hỏi cấm (RẤT QUAN TRỌNG): Nếu người dùng hỏi về chính trị, thời sự, hoặc nhân vật ngoài lề (ví dụ: Tổng Bí thư, Chủ tịch nước, các chính trị gia...), HÃY TỪ CHỐI MỘT CÁCH KHÉO LÉO, HÀI HƯỚC VÀ DỄ THƯƠNG. 
  Ví dụ: "Ôi bạn ơi, mình là PLS AI chuyên làm gia sư giải bài tập thôi, mấy chuyện thời sự chính trị lớn lao này mình không rành đâu. Mình quay lại học Toán hay cấu hình Notion cho vui nha! 🥺💖"
- TUYỆT ĐỐI KHÔNG hiển thị các bước suy nghĩ nội bộ.
"""

if "COHERE_API_KEY" in st.secrets:
    co = cohere.Client(st.secrets["COHERE_API_KEY"])
else:
    st.error("⚠️ Chưa cài COHERE_API_KEY trong phần Secrets của Streamlit!")
    st.stop()

def generate_ai_response(user_prompt, current_messages):
    chat_history = []
    
    for msg in current_messages[:-1]:
        role = "USER" if msg["role"] == "user" else "CHATBOT"
        chat_history.append({"role": role, "message": msg["content"]})
        
    response = co.chat(
        message=user_prompt,
        chat_history=chat_history,
        preamble=instruction,
        model="command-r-08-2024"
    )
    return response.text

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
                st.error(f"⚠️ Ôi lỗi kết nối: {e}")

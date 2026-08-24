import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN SIÊU DỄ THƯƠNG
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

welcome_message = """
✨ **PLS xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖
"""

# ==========================================
# 2. BỘ NHỚ LƯU LỊCH SỬ CHAT
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
# 3. SIDEBAR (ĐỦ 3 PHẦN ĐÚNG CẤU TRÚC YÊU CẦU)
# ==========================================
with st.sidebar:
    # 🌟 PHẦN 1: THÔNG TIN HỖ TRỢ VIP PRO (TRÊN CÙNG)
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
    
    # 💬 PHẦN 2: DANH SÁCH CÁC ĐOẠN CHAT (TỰ ĐỔI TÊN THEO CÂU HỎI)
    for chat_id, chat_data in list(st.session_state.chats.items()):
        is_active = (chat_id == st.session_state.active_chat_id)
        icon = "👉" if is_active else "💭"
        btn_label = f"{icon} {chat_data['title']}"
        
        if st.button(btn_label, key=f"btn_{chat_id}", use_container_width=True):
            st.session_state.active_chat_id = chat_id
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ⚙️ PHẦN 3: 2 NÚT THAO TÁC NẰM NGANG
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
# 4. CẤU HÌNH AI VÀ THỜI GIAN THỰC
# ==========================================
now = datetime.now()
days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
thu_hom_nay = days_vi.get(now.strftime("%A"), "")
thoi_gian_thuc = f"{thu_hom_nay}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

instruction = f"""
Bạn là một trợ lý AI thông minh, một người bạn đồng hành và một gia sư nhiệt tình của hệ thống quản lý học tập cá nhân PLS.
- CÁCH XƯNG HÔ: Luôn xưng là "mình" và gọi người dùng là "bạn". 
- NGÔN NGỮ BẮT BUỘC: 100% tiếng Việt chuẩn. Tuyệt đối KHÔNG chèn chữ Hán, chữ Nôm hay các ký tự ngoại ngữ lạ.
- THỜI GIAN HIỆN TẠI: Hôm nay là {thoi_gian_thuc}. Dùng thông tin này để tính toán chính xác thứ/ngày/tháng khi người dùng hỏi.
- TÍNH CÁCH: Ngôn ngữ tự nhiên, nhẹ nhàng, lịch sự, siêu đáng yêu và mang năng lượng chữa lành.
- NĂNG LỰC CHUYÊN MÔN: Hỗ trợ giải đáp kiến thức cho TẤT CẢ các môn học phổ thông.
- KỸ NĂNG SƯ PHẠM: Khuyến khích & Lắng nghe, Giải thích từng bước, Gợi ý phương pháp học tập hiệu quả.
"""

api_keys = []
for k in ["GOOGLE_API_KEY", "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3"]:
    val = st.secrets.get(k)
    if val and val not in api_keys:
        api_keys.append(val)

if not api_keys:
    st.error("Trùi ui, chưa được cấp API Key rồi! Bạn kiểm tra lại phần Secrets trên Streamlit nha 😭")
    st.stop()

def generate_ai_response(user_prompt, current_messages):
    formatted_history = []
    for msg in current_messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg["content"]]})

    last_error = None
    for key in api_keys:
        try:
            genai.configure(api_key=key)
            # DÙNG CHÍNH XÁC GEMINI-3.6-FLASH DỰA TRÊN CẤU HÌNH CỦA BẠN
            model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=instruction)
            chat = model.start_chat(history=formatted_history)
            response = chat.send_message(user_prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
    raise last_error

# ==========================================
# 5. KHUNG CHAT CHÍNH
# ==========================================
current_chat = st.session_state.chats[st.session_state.active_chat_id]
current_messages = current_chat["messages"]

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhắn tin cho mình ở đây nha... ⌨️"):
    # Đổi tiêu đề đoạn chat theo câu hỏi đầu tiên
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
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower():
                    st.warning("⏳ Trùi ui, hệ thống đang bận một chút! Bạn chờ khoảng 15-30 giây rồi nhắn lại giúp mình nha 💖")
                else:
                    st.error(f"Huhu mình bị lỗi mất rồi: {e}")

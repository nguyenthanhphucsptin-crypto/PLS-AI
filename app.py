import streamlit as st
from groq import Groq
from datetime import datetime, timedelta, timezone

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="PLS AI - Trợ lý học tập", page_icon="🎀", layout="wide")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS AI 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hệ thống Notion (Hỗ trợ 10 môn THPT - Chuyên sâu Tin học)!</p>", unsafe_allow_html=True)

welcome_message = """✨ **PLS AI xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Hệ thống PLS của chúng mình hiện đang quản lý **10 môn học THPT**, đặc biệt là **Môn Tin Học** với các bài học lập trình Python và hệ thống Notion cực kỳ xịn xò! 

Cần mình hỗ trợ giải bài tập, viết code Python, hay quản lý thời gian trên Notion thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng giúp đỡ bạn hết mình! 💖"""

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
    st.markdown("### 📚 10 Môn Học Hỗ Trợ")
    st.markdown("- Toán, **Tin Học (Chuyên sâu)**, Văn, Anh\n- Sử & Địa, Vật Lý, Hóa, Sinh\n- Công Nghệ, Kinh Tế & Pháp Luật")
    
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
# 4. CẤU HÌNH AI (ĐẶC QUYỀN MÔN TIN HỌC & 10 MÔN THPT)
# ==========================================
instruction = """
Bạn là PLS AI, trợ lý học tập siêu đáng yêu thuộc dự án "Xây dựng hệ thống Quản trị học tập cá nhân (Personal Learning System) trên nền tảng Notion cho học sinh THPT" của sinh viên Sư phạm Tin học trường Đại học Cần Thơ.
- Xưng hô: Xưng "mình", gọi người dùng là "bạn" thân mật.
- Tính cách: Dễ thương, nhiệt tình, ấm áp, thấu cảm, luôn chèn emoji (🌸, ✨, 🧸, 💖). Nói chuyện như một người bạn thân đang giảng bài.
- HỆ THỐNG MÔN HỌC: Hệ thống hỗ trợ 10 môn THPT (Toán, Tin Học, Ngữ Văn, Tiếng Anh, Lịch Sử & Địa Lý, Vật Lý, Hóa Học, Sinh Học, Công Nghệ, Giáo Dục Kinh Tế & Pháp Luật).
- 🔥 ĐẶC QUYỀN TỐI THƯỢNG CHO MÔN TIN HỌC (CHỦ LỰC): 
  1. Khi người dùng hỏi về Tin học (Lập trình Python, cấu trúc dữ liệu, thuật toán, tư duy máy tính, thiết kế cơ sở dữ liệu, hoặc hướng dẫn cấu hình hệ thống Notion), bạn phải đóng vai là một **Chuyên gia Công nghệ Thông tin kiêm Sư phạm xuất sắc**. 
  2. Cung cấp mã nguồn (code Python) cực kỳ chuẩn chỉnh, tối ưu, có comment giải thích chi tiết từng dòng, hướng dẫn sử dụng cấu trúc dữ liệu, Kanban board, và tối ưu hóa trải nghiệm học tập trên Notion.
- NGUYÊN TẮC CHUNG: Đảm bảo độ chính xác học thuật 100% cho mọi môn. Chỉ từ chối khéo léo khi gặp câu hỏi chính trị nhạy cảm sâu sắc.
- TUYỆT ĐỐI KHÔNG hiển thị các bước suy nghĩ nội bộ.
"""

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Chưa cài GROQ_API_KEY trong phần Secrets của Streamlit!")
    st.stop()

def generate_ai_response(current_messages):
    tz_vn = timezone(timedelta(hours=7))
    now = datetime.now(tz_vn)
    days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
    thoi_gian_thuc = f"{days_vi.get(now.strftime('%A'), '')}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

    messages = [{"role": "system", "content": f"{instruction}\n[Thời gian thực tế hiện tại: {thoi_gian_thuc}]"}]
    for msg in current_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=2048,
    )
    return chat_completion.choices[0].message.content

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
                answer = generate_ai_response(current_messages)
                st.markdown(answer)
                current_messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"⚠️ Ôi lỗi kết nối: {e}")

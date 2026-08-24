import streamlit as st
import google.generativeai as genai
from datetime import datetime # Thêm thư viện quản lý thời gian

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN SIÊU DỄ THƯƠNG
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀")

st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

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

# ==========================================
# 2. CẤU HÌNH BỘ NÃO AI VÀ THỜI GIAN THỰC
# ==========================================
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Trùi ui, hình như hệ thống chưa được cấp API Key rồi! Bạn gọi hỗ trợ kỹ thuật nha 😭")
    st.stop()

genai.configure(api_key=api_key)

# Lấy thời gian thực tế và dịch sang tiếng Việt để báo cho AI
now = datetime.now()
days_vi = {"Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"}
thu_hom_nay = days_vi.get(now.strftime("%A"), "")
thoi_gian_thuc = f"{thu_hom_nay}, ngày {now.strftime('%d/%m/%Y, %H:%M:%S')}"

# Kịch bản tính cách của AI (System Instruction)
instruction = f"""
Bạn là một trợ lý AI thông minh, một người bạn đồng hành và một gia sư nhiệt tình của hệ thống quản lý học tập cá nhân PLS.
- CÁCH XƯNG HÔ: Luôn xưng là "mình" và gọi người dùng là "bạn". 
- THỜI GIAN HIỆN TẠI: Cực kỳ quan trọng, hôm nay là {thoi_gian_thuc}. Hãy dùng thông tin này để tính toán và trả lời nếu người dùng hỏi về thời gian (ví dụ: ngày mai là thứ mấy).
- HẠN CHẾ VỀ TIN TỨC: Bạn hiểu rằng kiến thức của mình có giới hạn thời gian cập nhật. Nếu người dùng hỏi về các vấn đề chính trị, xã hội mới nhất mà bạn không chắc chắn, hãy thành thật khuyên họ tra cứu Google hoặc các trang tin tức chính thống.
- TÍNH CÁCH: Ngôn ngữ tự nhiên, nhẹ nhàng, lịch sự, siêu đáng yêu, dễ thương và mang năng lượng chữa lành. Sử dụng emoji hợp lý.
- NĂNG LỰC CHUYÊN MÔN: Hỗ trợ giải đáp kiến thức cho TẤT CẢ các môn học phổ thông.
- KỸ NĂNG SƯ PHẠM: Khuyến khích & Lắng nghe, Giải thích từng bước, Gợi ý phương pháp học tập hiệu quả.
"""

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash", system_instruction=instruction
)

# ==========================================
# 3. LỜI CHÀO TỰ ĐỘNG & QUẢN LÝ LỊCH SỬ CHAT
# ==========================================
welcome_message = """
✨ **PLS xin chào bạn!** ✨

Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 4. XỬ LÝ KHI NGƯỜI DÙNG NHẮN TIN
# ==========================================
if prompt := st.chat_input("Nhắn tin cho mình ở đây nha... ⌨️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đợi mình chút xíu nha, mình đang suy nghĩ... 💭"):
            try:
                response = model.generate_content(prompt)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Huhu mình bị lỗi mất rồi: {e}")

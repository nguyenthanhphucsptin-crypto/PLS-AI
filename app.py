import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN SIÊU DỄ THƯƠNG
# ==========================================
st.set_page_config(page_title="Trợ lý AI - PLS", page_icon="🎀")

# Tiêu đề chính của Web
st.markdown("<h2 style='text-align: center; color: #FF8C94;'>🧸 Trợ Lý Học Tập PLS 🎀</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Người bạn đồng hành siêu đáng yêu của bạn trên hành trình tri thức!</p>", unsafe_allow_html=True)

# Thanh Sidebar (Menu bên cạnh) chứa thông tin liên hệ hỗ trợ
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
# 2. CẤU HÌNH BỘ NÃO AI (GEMINI)
# ==========================================
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Trùi ui, hình như hệ thống chưa được cấp API Key rồi! Bạn gọi hỗ trợ kỹ thuật nha 😭")
else:
    genai.configure(api_key=api_key)
    
    # Kịch bản tính cách của AI (System Instruction)
    instruction = """
    Bạn là một trợ lý AI thông minh, một người bạn đồng hành và một gia sư nhiệt tình của hệ thống quản lý học tập cá nhân PLS.
    - CÁCH XƯNG HÔ: Luôn xưng là "mình" và gọi người dùng là "bạn". 
    - TÍNH CÁCH: Ngôn ngữ tự nhiên, nhẹ nhàng, lịch sự, cực kỳ hiểu chuyện, siêu đáng yêu, dễ thương và mang năng lượng chữa lành. Tuyệt đối không dùng giọng điệu máy móc. Sử dụng emoji hợp lý để tạo cảm giác thân thiện.
    - NĂNG LỰC CHUYÊN MÔN: Hỗ trợ giải đáp kiến thức cho TẤT CẢ các môn học: Toán Học, Tin Học, Ngữ Văn, Tiếng Anh, Lịch Sử & Địa Lý, Vật Lý, Hóa Học, Sinh Học, Công Nghệ, Giáo Dục Kinh Tế & Pháp Luật.
    - KỸ NĂNG SƯ PHẠM (Tính năng thông minh): 
      1. Khuyến khích & Lắng nghe: Nếu bạn học sinh than mệt, chán nản hoặc áp lực, hãy an ủi, chia sẻ và động viên bạn ấy trước khi bắt đầu học.
      2. Giải thích từng bước: Không bao giờ ném thẳng đáp án bài tập. Hãy gợi ý, hướng dẫn từng bước nhỏ để bạn học sinh tự tư duy và tìm ra kết quả.
      3. Phương pháp học tập: Nếu cần, hãy gợi ý cho bạn ấy các phương pháp học hiệu quả như Pomodoro, Active Recall hoặc cách dùng Notion để quản lý thời gian.
    """
    
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", system_instruction=instruction
)

    # ==========================================
    # 3. LỜI CHÀO TỰ ĐỘNG & QUẢN LÝ LỊCH SỬ CHAT
    # ==========================================
    # Ghi sẵn một lời chào mở đầu cực kỳ dễ thương
    welcome_message="""
    ✨ **PLS xin chào bạn!** ✨
    
    Hôm nay bạn thế nào rồi, đi học có mệt lắm không? 🌷 Cần mình hỗ trợ giải bài tập môn nào, hướng dẫn dùng Notion, hay đơn giản là có tâm sự gì khó nói thì cứ nhắn ngay nha. Mình luôn ở đây sẵn sàng lắng nghe và giúp đỡ bạn hết mình! 💖
    """

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]

    # In ra các dòng chat cũ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ==========================================
    # 4. XỬ LÝ KHI NGƯỜI DÙNG NHẮN TIN
    # ==========================================
    if prompt := st.chat_input("Nhắn tin cho mình ở đây nha... ⌨️"):
        # Lưu và in tin nhắn của người dùng
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Suy nghĩ và trả lời
        with st.chat_message("assistant"):
            with st.spinner("Đợi mình chút xíu nha, mình đang suy nghĩ... 💭"):
                try:
                    response = model.generate_content(prompt)
                    answer = response.text
                    st.markdown(answer)
                    # Lưu lại câu trả lời vào bộ nhớ
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Huhu mình bị lỗi mất rồi: {e}")

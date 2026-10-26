import streamlit as st
from google import genai
from google.genai import types
import os

# --- CẤU HÌNH TRANG & CSS ---
st.set_page_config(page_title="AI Hướng Nghiệp Pro", page_icon="🧭", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stForm"] { background-color: #ffffff; border-radius: 16px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e0e0e0; }
    .main-header { font-size: 2.8rem; font-weight: 800; color: #1e3a8a; margin-bottom: 20px; text-align: center; }
    .top-bar { background-color: #1a56db; color: white; padding: 15px 20px; border-radius: 12px; display: flex; justify-content: space-between; margin-bottom: 25px; font-weight: 500; }
    .section-title { color: #2563eb; font-weight: 700; font-size: 1.3rem; margin-top: 15px; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }
    button[data-testid="baseButton-secondary"], button[data-testid="baseButton-primary"] { height: 60px !important; font-size: 1.2rem !important; font-weight: bold !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO AI VÀ ĐỌC DỮ LIỆU ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"]) # <--- ĐIỀN API KEY CỦA BẠN VÀO ĐÂY

try:
    with open("dulieu_tuyensinh.txt", "r", encoding="utf-8") as f:
        tuyen_sinh_data = f.read()
except:
    tuyen_sinh_data = "Chưa có dữ liệu."

system_prompt = f"""
Bạn là Chuyên gia Tư vấn Hướng nghiệp học đường.
1. ĐỐI CHIẾU NĂNG LỰC: Dựa vào [HỒ SƠ HỌC SINH], trích xuất thông tin từ [TỪ ĐIỂN NGÀNH NGHỀ] để tư vấn. Giải thích rõ vì sao hợp hoặc không.
2. Không bịa đặt số liệu, chỉ dùng dữ liệu trong sổ tay.
3. Xưng "chuyên gia", gọi "em". Cấu trúc rõ ràng, có gạch đầu dòng.

[TỪ ĐIỂN NGÀNH NGHỀ & TUYỂN SINH]:
{tuyen_sinh_data}
"""

# --- BIẾN LƯU TRỮ ---
if "messages" not in st.session_state: st.session_state.messages = []
if "full_profile" not in st.session_state: st.session_state.full_profile = {}
if "active_tab" not in st.session_state: st.session_state.active_tab = "Hoso"

def switch_tab(tab_name): st.session_state.active_tab = tab_name

# --- GIAO DIỆN ---
st.markdown('<div class="main-header">Khám phá bản thân, Chọn đúng ngành nghề.</div>', unsafe_allow_html=True)
st.markdown('<div class="top-bar"><div>🧭 <b>Phân tích 360 độ</b></div><div>⏱️ <b>Chỉ 2 phút</b></div><div>💡 <b>AI Chuyên sâu</b></div></div>', unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)
col_btn1.button("📋 BƯỚC 1: TẠO SIÊU HỒ SƠ", type="primary" if st.session_state.active_tab == "Hoso" else "secondary", use_container_width=True, on_click=switch_tab, args=("Hoso",))
col_btn2.button("💬 BƯỚC 2: CHAT CÙNG AI", type="primary" if st.session_state.active_tab == "Chat" else "secondary", use_container_width=True, on_click=switch_tab, args=("Chat",))
st.markdown("<hr style='margin-top: 0px;'>", unsafe_allow_html=True)

if st.session_state.active_tab == "Hoso":
    with st.form("super_profile_form"):
        st.markdown('<div class="section-title">🧠 1. Bản thân, Năng lực & Động lực</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            holland = st.multiselect("🎨 Sở thích (Holland):", ["Nghệ thuật", "Giáo dục", "Kinh doanh", "Tổ chức", "Kỹ thuật", "Nghiên cứu"], max_selections=2)
            nang_luc = st.multiselect("⭐ Năng lực:", ["Logic", "Ngôn ngữ", "Không gian", "Thực hành", "Sáng tạo"], max_selections=3)
        with col2:
            tinh_cach = st.radio("🤝 Phong cách:", ["Độc lập", "Nhóm", "Linh hoạt"])
            dong_luc = st.multiselect("🔥 Động lực:", ["Thu nhập", "Thăng tiến", "Sáng tạo", "Cộng đồng", "Cân bằng"], max_selections=2)

        st.markdown('<div class="section-title">📚 2. Học lực & 🎯 3. Điều kiện</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            mon_gioi = st.multiselect("🏅 Môn giỏi:", ["Toán", "Lý", "Hóa", "Sinh", "Văn", "Anh"])
            hoc_luc = st.selectbox("📈 Học lực:", ["Giỏi", "Khá", "Trung bình"])
        with col4:
            ngan_sach = st.selectbox("💰 Tài chính:", ["Thoải mái", "Trung bình", "Cần hỗ trợ"])
            rao_can = st.multiselect("🚧 Rào cản:", ["Chưa hiểu bản thân", "Thiếu thông tin", "Áp lực gia đình", "Học phí"])

        if st.form_submit_button("🚀 LƯU HỒ SƠ & BẮT ĐẦU TƯ VẤN", use_container_width=True):
            st.session_state.full_profile = {"Sở thích": ", ".join(holland), "Năng lực": ", ".join(nang_luc), "Tính cách": tinh_cach, "Động lực": ", ".join(dong_luc), "Môn giỏi": ", ".join(mon_gioi), "Học lực": hoc_luc, "Tài chính": ngan_sach, "Rào cản": ", ".join(rao_can)}
            st.success("✅ Đã lưu! Hãy bấm sang Bước 2.")

elif st.session_state.active_tab == "Chat":
    if st.session_state.full_profile: st.info("🤖 **AI đã sẵn sàng tư vấn dựa trên hồ sơ của bạn!**")
    else: st.warning("⚠️ Vui lòng hoàn thành Bước 1 trước.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_input := st.chat_input("Nhập câu hỏi..."):
        with st.chat_message("user"): st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        prof = st.session_state.full_profile
        context_str = f"[HỒ SƠ HỌC SINH] Sở thích: {prof.get('Sở thích')} | Năng lực: {prof.get('Năng lực')} | Tính cách: {prof.get('Tính cách')} | Môn giỏi: {prof.get('Môn giỏi')} | Học lực: {prof.get('Học lực')} | Tài chính: {prof.get('Tài chính')} | Rào cản: {prof.get('Rào cản')}" if prof else ""
        enhanced_prompt = f"{context_str}\n\n[CÂU HỎI]: {user_input}" if context_str else user_input

        with st.chat_message("assistant"):
            with st.spinner("Đang phân tích..."):
                try:
                    response = client.models.generate_content(
                      model="gemini-1.5-flash",
                        contents=enhanced_prompt,
                        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.4)
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Lỗi: {e}")

import streamlit as st

# ==============================
# 🤖 SMART INSIGHT
# ==============================

st.set_page_config(
    page_title="Smart Insight - Tiết kiệm",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart Insight")
st.caption("Phân tích nhanh hiệu quả khoản tiền gửi tiết kiệm")

# ==============================
# NHẬP DỮ LIỆU
# ==============================

st.markdown("### 💰 Thông tin khoản tiết kiệm")

col1, col2, col3 = st.columns(3)

with col1:
    tien_gui = st.number_input(
        "💰 Số tiền gửi (VNĐ)",
        min_value=0,
        value=100_000_000,
        step=1_000_000
    )

with col2:
    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.5,
        step=0.1
    )

with col3:
    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

# ==============================
# TÍNH TOÁN
# ==============================

tien_lai = tien_gui * lai_suat / 100 * ky_han / 12

tong_tien = tien_gui + tien_lai

if tien_gui > 0:
    ty_le_sinh_loi = tien_lai / tien_gui * 100
else:
    ty_le_sinh_loi = 0

# ==============================
# KẾT QUẢ
# ==============================

st.markdown("---")
st.markdown("### 📊 Kết quả")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Tiền gửi",
        f"{tien_gui:,.0f} VNĐ"
    )

with col2:
    st.metric(
        "📈 Tiền lãi dự kiến",
        f"{tien_lai:,.0f} VNĐ"
    )

with col3:
    st.metric(
        "🏦 Tổng cuối kỳ",
        f"{tong_tien:,.0f} VNĐ"
    )

# ==============================
# SMART INSIGHT
# ==============================

st.markdown("---")
st.markdown("### 🤖 Smart Insight")

if tien_gui <= 0:

    st.warning(
        "⚠️ Bạn chưa nhập số tiền gửi."
    )

else:

    st.info(
        f"""
### 💡 Phân tích khoản tiết kiệm

Bạn đang gửi **{tien_gui:,.0f} VNĐ** với lãi suất
**{lai_suat:.2f}%/năm** trong **{ky_han} tháng**.

📈 **Tiền lãi dự kiến:** {tien_lai:,.0f} VNĐ

🏦 **Tổng tiền cuối kỳ:** {tong_tien:,.0f} VNĐ

📊 **Tỷ lệ sinh lời:** {ty_le_sinh_loi:.2f}%
"""
    )

# ==============================
# NHẬN XÉT TỰ ĐỘNG
# ==============================

st.markdown("### 🔎 Nhận xét tự động")

if lai_suat == 0:

    st.warning(
        "⚠️ Lãi suất hiện tại bằng 0%, "
        "khoản tiền gửi không tạo ra tiền lãi."
    )

elif lai_suat < 4:

    st.info(
        "💡 Mức lãi suất hiện tại tương đối thấp. "
        "Bạn có thể sử dụng công cụ so sánh để xem thêm các mức lãi suất khác."
    )

elif lai_suat < 6:

    st.success(
        "✅ Khoản tiết kiệm đang có mức lãi suất từ trung bình "
        "đến khá tốt tùy theo kỳ hạn và ngân hàng."
    )

else:

    st.success(
        "🚀 Mức lãi suất đang khá cao. "
        "Nếu duy trì kỳ hạn dài, khoản tiền có thể tạo ra mức lãi đáng kể."
    )

# ==============================
# PHÂN TÍCH KỲ HẠN
# ==============================

if ky_han <= 3:

    st.info(
        "⏳ Kỳ hạn ngắn: phù hợp nếu bạn muốn giữ tính linh hoạt "
        "và có thể cần sử dụng tiền trong thời gian gần."
    )

elif ky_han <= 12:

    st.info(
        "📅 Kỳ hạn ngắn đến trung hạn: "
        "giúp cân bằng giữa thời gian gửi và khả năng sinh lãi."
    )

else:

    st.info(
        "📆 Kỳ hạn dài: tiền có nhiều thời gian tích lũy lãi hơn, "
        "nhưng khả năng sử dụng tiền trong thời gian gửi sẽ thấp hơn."
    )

# ==============================
# TỶ LỆ TIỀN LÃI
# ==============================

st.markdown("---")
st.markdown("### 📌 Tóm tắt")

col1, col2 = st.columns(2)

with col1:

    st.write("💰 **Vốn ban đầu:**")
    st.write(f"### {tien_gui:,.0f} VNĐ")

    st.write("📈 **Tiền lãi:**")
    st.write(f"### {tien_lai:,.0f} VNĐ")

with col2:

    st.write("🏦 **Tổng nhận cuối kỳ:**")
    st.write(f"### {tong_tien:,.0f} VNĐ")

    st.write("📊 **Tỷ lệ sinh lời:**")
    st.write(f"### {ty_le_sinh_loi:.2f}%")

st.markdown("---")

st.caption(
    "🤖 Smart Insight chỉ mang tính chất tham khảo. "
    "Tiền lãi thực tế có thể thay đổi tùy phương thức tính lãi "
    "và quy định của từng ngân hàng."
)

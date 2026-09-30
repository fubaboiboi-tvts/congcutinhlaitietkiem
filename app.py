import streamlit as st
import math

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 ỨNG DỤNG TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.markdown(
    "Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép** "
    "với nhiều hình thức nhận lãi."
)

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin khoản tiền gửi")

# Số tiền gửi
tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han_thang = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

# Lãi suất
lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

# Hình thức tính lãi
hinh_thuc_lai = st.selectbox(
    "🧮 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

# Hình thức nhận lãi
hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_vnd(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("❌ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if ky_han_thang <= 0:
        st.error("❌ Kỳ hạn phải lớn hơn 0 tháng.")
        st.stop()

    if lai_suat < 0:
        st.error("❌ Lãi suất không được nhỏ hơn 0%.")
        st.stop()

    # Chuyển lãi suất từ % sang số thập phân
    r = lai_suat / 100

    # Thời gian gửi tính theo năm
    so_nam = ky_han_thang / 12

    # ==================================================
    # LÃI ĐƠN
    # ==================================================
    if hinh_thuc_lai == "Lãi đơn":

        # Công thức:
        # Tiền lãi = Gốc × Lãi suất × Thời gian
        tong_lai = tien_gui * r * so_nam

        tong_tien = tien_gui + tong_lai

        # Tính lãi theo tháng
        lai_thang = tien_gui * r / 12

        # Tính lãi theo quý
        lai_quy = tien_gui * r / 4

        # Tiền lãi định kỳ
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            lai_dinh_ky = lai_thang
            so_ky = ky_han_thang

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            lai_dinh_ky = lai_quy
            so_ky = math.ceil(ky_han_thang / 3)

        else:
            lai_dinh_ky = tong_lai
            so_ky = 1

    # ==================================================
    # LÃI KÉP
    # ==================================================
    else:

        # Lãi suất tháng
        lai_suat_thang = r / 12

        # Lãi suất quý
        lai_suat_quy = r / 4

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":

            # Số kỳ ghép lãi
            so_ky = ky_han_thang

            # Công thức lãi kép:
            # A = P(1 + r)^n
            tong_tien = tien_gui * (1 + lai_suat_thang) ** so_ky

            tong_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_thang

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":

            # Làm tròn số quý
            so_ky = math.ceil(ky_han_thang / 3)

            tong_tien = tien_gui * (1 + lai_suat_quy) ** so_ky

            tong_lai = tong_tien - tien_gui

            # Lãi của quý đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_quy

        else:

            # Lãi kép cuối kỳ:
            # Số lần ghép lãi theo tháng
            so_ky = ky_han_thang

            tong_tien = tien_gui * (1 + lai_suat_thang) ** so_ky

            tong_lai = tong_tien - tien_gui

            # Với cuối kỳ, toàn bộ lãi nhận một lần
            lai_dinh_ky = tong_lai

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền gửi ban đầu",
            format_vnd(tien_gui)
        )

    with col2:
        st.metric(
            "📈 Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Tiền lãi định kỳ",
            format_vnd(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "💰 Tổng tiền lãi",
            format_vnd(tong_lai)
        )

    st.metric(
        "🏦 TỔNG TIỀN GỐC + LÃI",
        format_vnd(tong_tien)
    )

    st.divider()

    # ==============================
    # THÔNG TIN CHI TIẾT
    # ==============================
    st.subheader("📝 Thông tin chi tiết")

    st.write(
        f"**Hình thức tính lãi:** {hinh_thuc_lai}"
    )

    st.write(
        f"**Hình thức nhận lãi:** {hinh_thuc_nhan}"
    )

    st.write(
        f"**Kỳ hạn:** {ky_han_thang} tháng ({so_nam:.2f} năm)"
    )

    if hinh_thuc_nhan == "Lãnh lãi theo tháng":
        st.write(
            f"**Số kỳ nhận lãi:** {ky_han_thang} tháng"
        )

    elif hinh_thuc_nhan == "Lãnh lãi theo quý":
        st.write(
            f"**Số kỳ nhận lãi:** {math.ceil(ky_han_thang / 3)} quý"
        )

    else:
        st.write(
            "**Số lần nhận lãi:** 1 lần vào cuối kỳ"
        )

    # ==============================
    # GIẢI THÍCH CÔNG THỨC
    # ==============================
    with st.expander("📚 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":

            st.markdown("""
            **Công thức lãi đơn:**

            > Tiền lãi = Tiền gốc × Lãi suất × Thời gian

            **Tổng tiền nhận được:**

            > Tổng tiền = Tiền gốc + Tiền lãi
            """)

        else:

            st.markdown("""
            **Công thức lãi kép:**

            > A = P × (1 + r)ⁿ

            Trong đó:

            - **A:** Tổng số tiền cuối kỳ
            - **P:** Số tiền gốc ban đầu
            - **r:** Lãi suất của mỗi kỳ
            - **n:** Số kỳ tính lãi

            Phần lãi được cộng vào vốn để tiếp tục sinh lãi ở các kỳ tiếp theo.
            """)

st.divider()

st.caption(
    "💡 Lưu ý: Kết quả mang tính mô phỏng. "
    "Lãi suất thực tế của ngân hàng có thể thay đổi theo sản phẩm tiền gửi, "
    "kỳ hạn và phương thức nhận lãi."
)

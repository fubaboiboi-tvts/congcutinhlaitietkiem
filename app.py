import streamlit as st
import pandas as pd
import io
st.image("logo.jpg")
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
st.title("NHÀ CÁI ĐẾN TỪ CHÂU ÂU - BÙI BỘI NGỌC ")
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
# ============================================================
# TAB SO SÁNH LÃI ĐƠN VÀ LÃI KÉP
# ============================================================

st.divider()

st.header("📊 So sánh lãi đơn và lãi kép")

st.write(
    "Tính năng này giúp bạn so sánh số tiền nhận được "
    "giữa phương pháp lãi đơn và lãi kép."
)

# -----------------------------
# NHẬP DỮ LIỆU
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    tien_so_sanh = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=1.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="so_sanh_tien"
    )

with col2:
    ky_han_so_sanh = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=36,
        step=1,
        key="so_sanh_ky_han"
    )

with col3:
    lai_suat_so_sanh = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f",
        key="so_sanh_lai_suat"
    )


# -----------------------------
# TÍNH LÃI
# -----------------------------

if st.button(
    "📊 SO SÁNH",
    use_container_width=True,
    type="primary"
):

    lai_suat_nam = lai_suat_so_sanh / 100

    # LÃI ĐƠN
    tong_lai_don = (
        tien_so_sanh
        * lai_suat_nam
        * (ky_han_so_sanh / 12)
    )

    tong_tien_don = (
        tien_so_sanh
        + tong_lai_don
    )

    # LÃI KÉP
    lai_suat_thang = lai_suat_nam / 12

    tong_tien_kep = (
        tien_so_sanh
        * (1 + lai_suat_thang) ** ky_han_so_sanh
    )

    tong_lai_kep = (
        tong_tien_kep
        - tien_so_sanh
    )

    # -----------------------------
    # HIỂN THỊ KẾT QUẢ
    # -----------------------------

    st.subheader("📌 Kết quả so sánh")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🔵 Lãi đơn")

        st.metric(
            "Tổng tiền lãi",
            f"{tong_lai_don:,.0f} VNĐ"
        )

        st.metric(
            "Tổng tiền cuối kỳ",
            f"{tong_tien_don:,.0f} VNĐ"
        )

    with col2:

        st.markdown("### 🟢 Lãi kép")

        st.metric(
            "Tổng tiền lãi",
            f"{tong_lai_kep:,.0f} VNĐ"
        )

        st.metric(
            "Tổng tiền cuối kỳ",
            f"{tong_tien_kep:,.0f} VNĐ"
        )

    # -----------------------------
    # CHÊNH LỆCH
    # -----------------------------

    chenh_lech = (
        tong_tien_kep
        - tong_tien_don
    )

    st.info(
        f"💡 Chênh lệch giữa lãi kép và lãi đơn: "
        f"**{chenh_lech:,.0f} VNĐ**"
    )

    # ========================================================
    # BIỂU ĐỒ TĂNG TRƯỞNG
    # ========================================================

    st.subheader("📈 Biểu đồ tăng trưởng theo thời gian")

    data = []

    for thang in range(
        ky_han_so_sanh + 1
    ):

        # Lãi đơn tại từng tháng
        tien_don = (
            tien_so_sanh
            * (
                1
                + lai_suat_nam
                * thang / 12
            )
        )

        # Lãi kép tại từng tháng
        tien_kep = (
            tien_so_sanh
            * (1 + lai_suat_thang) ** thang
        )

        data.append({
            "Tháng": thang,
            "Lãi đơn": tien_don,
            "Lãi kép": tien_kep
        })

    df = pd.DataFrame(data)

    # Hiển thị biểu đồ
    st.line_chart(
        df.set_index("Tháng")[
            ["Lãi đơn", "Lãi kép"]
        ]
    )

    st.caption(
        "Biểu đồ mô phỏng sự tăng trưởng của khoản tiền "
        "theo từng tháng."
    )

    # -----------------------------
    # BẢNG CHI TIẾT
    # -----------------------------

    with st.expander("📋 Xem bảng chi tiết"):

        df_hien_thi = df.copy()

        df_hien_thi["Lãi đơn"] = (
            df_hien_thi["Lãi đơn"]
            .map(lambda x: f"{x:,.0f} VNĐ")
        )

        df_hien_thi["Lãi kép"] = (
            df_hien_thi["Lãi kép"]
            .map(lambda x: f"{x:,.0f} VNĐ")
        )

        st.dataframe(
            df_hien_thi,
            use_container_width=True,
            hide_index=True
        )
# ============================================================
# TÍNH NĂNG MỤC TIÊU TIẾT KIỆM
# ============================================================

st.divider()

st.header("🎯 Mục tiêu tiết kiệm")

st.write(
    "Nhập mục tiêu tài chính của bạn. "
    "Ứng dụng sẽ ước tính số tiền cần tiết kiệm mỗi tháng."
)

# -----------------------------
# NHẬP THÔNG TIN
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    muc_tieu = st.number_input(
        "🎯 Số tiền mục tiêu (VNĐ)",
        min_value=1.0,
        value=200_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="muc_tieu"
    )

    tien_hien_co = st.number_input(
        "💵 Số tiền hiện có (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="tien_hien_co"
    )

with col2:

    thoi_gian = st.number_input(
        "📅 Thời gian đạt mục tiêu (tháng)",
        min_value=1,
        max_value=600,
        value=24,
        step=1,
        key="thoi_gian_muc_tieu"
    )

    lai_suat_muc_tieu = st.number_input(
        "📈 Lãi suất dự kiến (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f",
        key="lai_suat_muc_tieu"
    )


# -----------------------------
# TÍNH TOÁN
# -----------------------------

if st.button(
    "🎯 TÍNH KẾ HOẠCH",
    use_container_width=True,
    type="primary"
):

    if tien_hien_co >= muc_tieu:

        st.success(
            "🎉 Bạn đã đạt hoặc vượt mục tiêu!"
        )

    else:

        r = lai_suat_muc_tieu / 100 / 12
        n = thoi_gian

        # Giá trị tương lai của số tiền hiện có
        gia_tri_tien_hien_co = (
            tien_hien_co
            * (1 + r) ** n
        )

        # Số tiền còn thiếu
        tien_con_thieu = (
            muc_tieu
            - gia_tri_tien_hien_co
        )

        # -----------------------------
        # TÍNH TIỀN GỬI HÀNG THÁNG
        # -----------------------------

        if r > 0:

            he_so = (
                ((1 + r) ** n - 1)
                / r
            )

            tien_gui_thang = (
                tien_con_thieu
                / he_so
            )

        else:

            tien_gui_thang = (
                (muc_tieu - tien_hien_co)
                / n
            )

        # Không cho kết quả âm
        tien_gui_thang = max(
            tien_gui_thang,
            0
        )

        # -----------------------------
        # TÍNH TỔNG KẾT
        # -----------------------------

        tong_tien_tu_gui = (
            tien_gui_thang * n
        )

        if r > 0:

            gia_tri_khoan_gui = (
                tien_gui_thang
                * (
                    ((1 + r) ** n - 1)
                    / r
                )
            )

        else:

            gia_tri_khoan_gui = (
                tong_tien_tu_gui
            )

        tong_du_kien = (
            gia_tri_tien_hien_co
            + gia_tri_khoan_gui
        )

        tong_lai = (
            tong_du_kien
            - tien_hien_co
            - tong_tien_tu_gui
        )

        # ====================================================
        # HIỂN THỊ KẾT QUẢ
        # ====================================================

        st.success(
            "✅ Đã tạo kế hoạch tiết kiệm!"
        )

        st.subheader("📊 Kết quả")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Mục tiêu",
                f"{muc_tieu:,.0f} VNĐ"
            )

        with col2:

            st.metric(
                "💰 Cần gửi mỗi tháng",
                f"{tien_gui_thang:,.0f} VNĐ"
            )

        with col3:

            st.metric(
                "📈 Lãi dự kiến",
                f"{tong_lai:,.0f} VNĐ"
            )

        # ====================================================
        # THANH TIẾN ĐỘ
        # ====================================================

        st.subheader("📊 Tiến độ hiện tại")

        tien_do = (
            tien_hien_co
            / muc_tieu
        )

        tien_do = min(
            max(tien_do, 0),
            1
        )

        st.progress(tien_do)

        st.write(
            f"Bạn đã có **{tien_do * 100:.1f}%** "
            f"mục tiêu."
        )

        # ====================================================
        # TÓM TẮT
        # ====================================================

        st.subheader("📋 Kế hoạch của bạn")

        st.write(
            f"💵 Số tiền hiện có: "
            f"**{tien_hien_co:,.0f} VNĐ**"
        )

        st.write(
            f"🎯 Số tiền mục tiêu: "
            f"**{muc_tieu:,.0f} VNĐ**"
        )

        st.write(
            f"📅 Thời gian: "
            f"**{thoi_gian} tháng**"
        )

        st.write(
            f"💰 Cần tiết kiệm mỗi tháng: "
            f"**{tien_gui_thang:,.0f} VNĐ**"
        )

        st.write(
            f"📈 Tổng tiền dự kiến cuối kỳ: "
            f"**{tong_du_kien:,.0f} VNĐ**"
        )

        # ====================================================
        # BIỂU ĐỒ MỤC TIÊU
        # ====================================================

        st.subheader("📈 Quá trình đạt mục tiêu")

        timeline = []

        for thang in range(
            thoi_gian + 1
        ):

            # Giá trị tiền hiện có sau khi sinh lãi
            gia_tri_goc = (
                tien_hien_co
                * (1 + r) ** thang
            )

            # Giá trị các khoản gửi thêm
            if r > 0:

                gia_tri_gui = (
                    tien_gui_thang
                    * (
                        ((1 + r) ** thang - 1)
                        / r
                    )
                )

            else:

                gia_tri_gui = (
                    tien_gui_thang * thang
                )

            tong_gia_tri = (
                gia_tri_goc
                + gia_tri_gui
            )

            timeline.append({
                "Tháng": thang,
                "Số tiền tích lũy": tong_gia_tri
            })

        df_goal = pd.DataFrame(
            timeline
        )

        st.line_chart(
            df_goal.set_index("Tháng"),
            use_container_width=True
        )

# =========================================================
# 🏠 DASHBOARD HIỆN ĐẠI
# =========================================================

st.markdown("""
<style>

.dashboard-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 15px;
    color: #777;
    margin-bottom: 25px;
}

.dashboard-card {
    background: linear-gradient(135deg, #ffffff, #f7f9fc);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e8ebf0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    min-height: 135px;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.card-label {
    font-size: 14px;
    color: #777;
    margin-bottom: 7px;
}

.card-value {
    font-size: 25px;
    font-weight: 800;
}

.card-small {
    font-size: 13px;
    color: #888;
    margin-top: 5px;
}

.insight-box {
    background: linear-gradient(135deg, #f5f7ff, #ffffff);
    border-radius: 18px;
    padding: 22px;
    margin-top: 25px;
    border: 1px solid #e5e8f0;
}

.section-title {
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="dashboard-title">🏠 Tổng quan tài chính</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Theo dõi khoản tiết kiệm của bạn một cách trực quan và dễ hiểu'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INPUT RIÊNG CHO DASHBOARD
# =========================================================

col_input1, col_input2 = st.columns(2)

with col_input1:
    dashboard_tien = st.number_input(
        "💰 Số tiền gửi",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f",
        key="dashboard_tien"
    )

with col_input2:
    dashboard_lai = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        value=5.5,
        step=0.1,
        key="dashboard_lai"
    )


col_input3, col_input4 = st.columns(2)

with col_input3:
    dashboard_kyhan = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        value=12,
        step=1,
        key="dashboard_kyhan"
    )

with col_input4:
    dashboard_hinhthuc = st.selectbox(
        "💳 Hình thức tính",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        key="dashboard_hinhthuc"
    )


# =========================================================
# TÍNH TOÁN
# =========================================================

if dashboard_hinhthuc == "Lãi đơn":

    dashboard_lai_tien = (
        dashboard_tien
        * dashboard_lai / 100
        * dashboard_kyhan / 12
    )

else:

    dashboard_lai_thang = dashboard_lai / 100 / 12

    dashboard_tong = (
        dashboard_tien
        * (1 + dashboard_lai_thang) ** dashboard_kyhan
    )

    dashboard_lai_tien = dashboard_tong - dashboard_tien


dashboard_tong_tien = dashboard_tien + dashboard_lai_tien


if dashboard_tien > 0:
    dashboard_ty_le = (
        dashboard_lai_tien / dashboard_tien * 100
    )
else:
    dashboard_ty_le = 0


# =========================================================
# 4 CARD CHÍNH
# =========================================================

st.markdown(
    '<div class="section-title">📊 Tổng quan khoản tiết kiệm</div>',
    unsafe_allow_html=True
)

card1, card2, card3, card4 = st.columns(4)


with card1:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-icon">💰</div>
            <div class="card-label">Tiền gửi ban đầu</div>
            <div class="card-value">
                {dashboard_tien:,.0f} ₫
            </div>
            <div class="card-small">Số vốn ban đầu</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with card2:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-icon">📈</div>
            <div class="card-label">Tiền lãi dự kiến</div>
            <div class="card-value">
                {dashboard_lai_tien:,.0f} ₫
            </div>
            <div class="card-small">
                Sinh lời {dashboard_ty_le:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with card3:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-icon">🏦</div>
            <div class="card-label">Tổng cuối kỳ</div>
            <div class="card-value">
                {dashboard_tong_tien:,.0f} ₫
            </div>
            <div class="card-small">
                Sau {dashboard_kyhan} tháng
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with card4:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-icon">🚀</div>
            <div class="card-label">Lãi suất</div>
            <div class="card-value">
                {dashboard_lai:.2f}%
            </div>
            <div class="card-small">
                {dashboard_hinhthuc}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PHÂN TÍCH KHOẢN TIẾT KIỆM
# =========================================================

st.markdown(
    """
    <div class="insight-box">
        <div class="section-title">💡 Smart Overview</div>
    """,
    unsafe_allow_html=True
)

if dashboard_tien == 0:

    st.warning(
        "⚠️ Bạn chưa nhập số tiền gửi. "
        "Hãy nhập số tiền để xem phân tích."
    )

elif dashboard_lai == 0:

    st.warning(
        "📌 Lãi suất hiện tại là 0%, "
        "khoản tiền gửi chưa tạo ra lợi nhuận."
    )

elif dashboard_kyhan <= 3:

    st.info(
        "⏳ Kỳ hạn khá ngắn. "
        "Nếu mục tiêu của bạn là tối đa hóa tiền lãi, "
        "có thể cân nhắc kỳ hạn dài hơn."
    )

elif dashboard_kyhan <= 12:

    st.success(
        "👍 Đây là khoản tiết kiệm ngắn đến trung hạn. "
        "Mức kỳ hạn này phù hợp nếu bạn vẫn muốn duy trì "
        "khả năng sử dụng tiền trong tương lai gần."
    )

else:

    st.success(
        "🚀 Kỳ hạn dài giúp tiền có nhiều thời gian tích lũy "
        "lãi hơn và phù hợp với mục tiêu tiết kiệm dài hạn."
    )


# =========================================================
# THANH TỶ LỆ VỐN / LÃI
# =========================================================

st.markdown("### 📊 Cơ cấu khoản tiền")

if dashboard_tong_tien > 0:

    ty_le_von = dashboard_tien / dashboard_tong_tien
    ty_le_lai = dashboard_lai_tien / dashboard_tong_tien

    st.write(
        f"💰 Vốn ban đầu: **{ty_le_von * 100:.2f}%**"
    )

    st.progress(min(ty_le_von, 1.0))

    st.write(
        f"📈 Tiền lãi: **{ty_le_lai * 100:.2f}%**"
    )

    st.progress(min(ty_le_lai, 1.0))


# =========================================================
# KẾT LUẬN
# =========================================================

st.markdown("### 🎯 Đánh giá nhanh")

if dashboard_lai_tien > 0:

    st.write(
        f"""
        Với **{dashboard_tien:,.0f} ₫** gửi trong **{dashboard_kyhan} tháng**
        ở mức lãi suất **{dashboard_lai:.2f}%/năm**,
        bạn dự kiến nhận được khoảng
        **{dashboard_lai_tien:,.0f} ₫ tiền lãi**.

        👉 Tổng giá trị khoản tiết kiệm cuối kỳ khoảng
        **{dashboard_tong_tien:,.0f} ₫**.
        """
    )

else:

    st.write(
        "Hãy nhập số tiền và lãi suất để hệ thống đưa ra đánh giá."
    )

st.subheader("🏦 So sánh lãi suất nhiều ngân hàng")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0
)

ky_han_nam = st.number_input(
    "Kỳ hạn (năm)",
    min_value=1,
    value=1,
    step=1
)

st.write("### Nhập thông tin ngân hàng")

ngan_hang = {}

for i in range(5):
    col1, col2 = st.columns(2)

    with col1:
        ten = st.text_input(
            f"Tên ngân hàng {i+1}",
            value=f"Ngân hàng {i+1}"
        )

    with col2:
        lai = st.number_input(
            f"Lãi suất {i+1} (%/năm)",
            min_value=0.0,
            value=5.0 + i * 0.2,
            step=0.1
        )

    ngan_hang[ten] = lai

# Tính toán
ket_qua = []

for ten, lai in ngan_hang.items():

    tien_lai = tien_gui * lai / 100 * ky_han_nam
    tong_nhan = tien_gui + tien_lai

    ket_qua.append({
        "Ngân hàng": ten,
        "Lãi suất (%/năm)": lai,
        "Tiền lãi (VNĐ)": tien_lai,
        "Tổng nhận được (VNĐ)": tong_nhan
    })

df_ngan_hang = pd.DataFrame(ket_qua)

st.dataframe(
    df_ngan_hang,
    use_container_width=True
)

st.bar_chart(
    df_ngan_hang.set_index("Ngân hàng")[
        "Tổng nhận được (VNĐ)"
    ]
)
    
st.subheader("📅 Kế hoạch tiết kiệm theo tháng")

von_ban_dau = st.number_input(
    "Vốn ban đầu (VNĐ)",
    min_value=0.0,
    value=50_000_000.0,
    step=1_000_000.0
)

gui_hang_thang = st.number_input(
    "Số tiền gửi thêm mỗi tháng (VNĐ)",
    min_value=0.0,
    value=3_000_000.0,
    step=500_000.0
)

thoi_gian = st.number_input(
    "Thời gian (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat_nam = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.5,
    step=0.1
)

lai_suat_thang = lai_suat_nam / 100 / 12

so_du = von_ban_dau
du_lieu = []

for thang in range(1, thoi_gian + 1):

    tien_lai = so_du * lai_suat_thang

    so_du += tien_lai
    so_du += gui_hang_thang

    du_lieu.append({
        "Tháng": thang,
        "Tiền gửi thêm": gui_hang_thang,
        "Tiền lãi": tien_lai,
        "Số dư": so_du
    })

df_ke_hoach = pd.DataFrame(du_lieu)

st.dataframe(
    df_ke_hoach,
    use_container_width=True
)

st.line_chart(
    df_ke_hoach.set_index("Tháng")["Số dư"]
)

# ==========================================
# 🔄 GỬI THÊM TIỀN HÀNG THÁNG
# ==========================================

st.subheader("🔄 Nếu gửi thêm tiền hàng tháng thì sao?")

col1, col2 = st.columns(2)

with col1:
    tien_ban_dau = st.number_input(
        "💰 Tiền ban đầu (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        key="tien_ban_dau"
    )

    tien_gui_thang = st.number_input(
        "💵 Gửi thêm mỗi tháng (VNĐ)",
        min_value=0.0,
        value=3_000_000.0,
        step=500_000.0,
        key="tien_gui_thang"
    )

with col2:
    so_thang = st.number_input(
        "📅 Thời gian (tháng)",
        min_value=1,
        value=24,
        step=1,
        key="so_thang"
    )

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        value=5.5,
        step=0.1,
        key="lai_suat_gui_them"
    )


# ==========================================
# TÍNH TOÁN
# ==========================================

lai_suat_thang = lai_suat / 100 / 12

so_du = tien_ban_dau
tong_tien_lai = 0

du_lieu = []


for thang in range(1, so_thang + 1):

    # Tính lãi trên số dư hiện tại
    tien_lai = so_du * lai_suat_thang

    # Cộng lãi
    so_du += tien_lai

    # Gửi thêm tiền cuối tháng
    so_du += tien_gui_thang

    # Cộng tổng lãi
    tong_tien_lai += tien_lai

    du_lieu.append({
        "Tháng": thang,
        "Tiền gửi thêm": tien_gui_thang,
        "Tiền lãi": tien_lai,
        "Số dư": so_du
    })


# ==========================================
# TỔNG KẾT
# ==========================================

tong_tien_gui = (
    tien_ban_dau +
    tien_gui_thang * so_thang
)

tong_nhan_duoc = so_du


# ==========================================
# HIỂN THỊ KẾT QUẢ
# ==========================================

st.markdown("### 📊 Kết quả dự kiến")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Tổng tiền tự gửi",
        f"{tong_tien_gui:,.0f} VNĐ"
    )

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        f"{tong_tien_lai:,.0f} VNĐ"
    )

with col3:
    st.metric(
        "🏦 Số dư cuối kỳ",
        f"{tong_nhan_duoc:,.0f} VNĐ"
    )

with col4:
    st.metric(
        "🚀 Lợi nhuận",
        f"{tong_tien_lai:,.0f} VNĐ"
    )


# ==========================================
# BẢNG CHI TIẾT
# ==========================================

df_gui_them = pd.DataFrame(du_lieu)

st.markdown("### 📅 Chi tiết tăng trưởng theo tháng")

st.dataframe(
    df_gui_them,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# BIỂU ĐỒ
# ==========================================

st.markdown("### 📈 Biểu đồ tăng trưởng")

st.line_chart(
    df_gui_them.set_index("Tháng")["Số dư"]
)


# ==========================================
# SMART INSIGHT
# ==========================================

st.markdown("### 🤖 Smart Insight")

if tong_tien_gui > 0:

    ty_le_lai = (
        tong_tien_lai /
        tong_tien_gui *
        100
    )

    st.info(
        f"""
        💡 Sau **{so_thang} tháng**, bạn đã tự bỏ vào
        **{tong_tien_gui:,.0f} VNĐ**.

        Khoản tiền lãi dự kiến là **{tong_tien_lai:,.0f} VNĐ**,
        tương đương khoảng **{ty_le_lai:.2f}%** trên tổng số tiền bạn đã gửi.

        👉 Số dư dự kiến cuối kỳ:
        **{tong_nhan_duoc:,.0f} VNĐ**
        """
    )
    
st.subheader("🎯 Bao lâu để đạt mục tiêu?")
muc_tieu = st.number_input(
    "Mục tiêu tài chính (VNĐ)",
    min_value=1_000_000.0,
    value=1_000_000_000.0,
    step=10_000_000.0
)

von_hien_tai = st.number_input(
    "Số tiền hiện có (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0
)

tiet_kiem_thang = st.number_input(
    "Tiết kiệm mỗi tháng (VNĐ)",
    min_value=0.0,
    value=5_000_000.0,
    step=500_000.0
)

lai_suat_nam = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.5,
    step=0.1,
    key="lai_muc_tieu"
)

r = lai_suat_nam / 100 / 12

so_du = von_hien_tai
thang = 0

lich_su = []

while so_du < muc_tieu and thang < 1000:

    thang += 1

    so_du = so_du * (1 + r)
    so_du += tiet_kiem_thang

    lich_su.append({
        "Tháng": thang,
        "Số dư": so_du
    })

if so_du >= muc_tieu:

    st.success(
        f"🎉 Có thể đạt mục tiêu sau khoảng **{thang} tháng** "
        f"(tương đương **{thang / 12:.1f} năm**)."
    )

    df_muc_tieu = pd.DataFrame(lich_su)

    st.line_chart(
        df_muc_tieu.set_index("Tháng")["Số dư"]
    )

else:

    st.warning(
        "Chưa đạt mục tiêu trong khoảng thời gian mô phỏng."
    )
# ==============================
# 📊 XUẤT FILE EXCEL/CSV
# ==============================

st.title("📊 Xuất Excel")

# Dữ liệu mẫu
data = {
    "Tháng": [1, 2, 3, 4, 5],
    "Tiền lãi": [100000, 200000, 300000, 400000, 500000],
    "Số dư": [10100000, 20300000, 30600000, 41000000, 51500000]
}

# Tạo DataFrame
df = pd.DataFrame(data)

# Chuyển sang CSV
csv_file = df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

# Nút tải xuống
st.download_button(
    label="📥 Tải file Excel",
    data=csv_file,
    file_name="bao_cao_tiet_kiem.csv",
    mime="text/csv"
)

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
st.subheader("🏠 Dashboard tổng quan")

col1, col2, col3, col4 = st.columns(4)

with col1:
    tien_goc = st.number_input(
    "Số tiền gửi",
    min_value=0.0,
    value=10000000.0,
    step=1000000.0
)

tong_tien_lai = 0
tong_tien = tien_goc

st.metric(
    "💰 Tiền gửi",
    f"{tien_goc:,.0f} VNĐ"
)

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        f"{tong_tien_lai:,.0f} VNĐ"
    )

with col3:
    st.metric(
        "💵 Tổng nhận được",
        f"{tong_tien:,.0f} VNĐ"
    )

with col4:
    st.metric(
        "📊 Lãi suất",
        f"{lai_suat:.2f}%/năm"
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
st.subheader("🤖 Smart Insight")

# Tính tỷ lệ lãi
if tien_goc > 0:
    ty_le_lai = tong_tien_lai / tien_goc * 100
else:
    ty_le_lai = 0

if tong_tien_lai > 0:

    st.info(
        f"""
        💡 **Phân tích khoản tiết kiệm**

        • Số tiền ban đầu: **{tien_goc:,.0f} VNĐ**

        • Tổng tiền lãi dự kiến: **{tong_tien_lai:,.0f} VNĐ**

        • Tổng số tiền nhận được: **{tong_tien:,.0f} VNĐ**

        • Tỷ lệ tiền lãi trên vốn: **{ty_le_lai:.2f}%**
        """
    )

    if ty_le_lai < 5:
        st.warning(
            "💭 Khoản tiền lãi hiện chiếm tỷ trọng tương đối thấp "
            "so với số vốn ban đầu."
        )

    elif ty_le_lai < 10:
        st.info(
            "📊 Khoản tiết kiệm đang tạo ra mức tăng trưởng "
            "đáng kể so với số vốn ban đầu."
        )

    else:
        st.success(
            "🚀 Khoản tiền đang tạo ra mức tăng trưởng "
            "tương đối lớn so với số vốn ban đầu."
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
st.subheader("🔄 Nếu gửi thêm tiền hàng tháng thì sao?")

tien_ban_dau = st.number_input(
    "Tiền ban đầu",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    key="tien_ban_dau"
)

tien_gui_thang = st.number_input(
    "Gửi thêm mỗi tháng",
    min_value=0.0,
    value=3_000_000.0,
    step=500_000.0,
    key="tien_gui_thang"
)

so_thang = st.number_input(
    "Thời gian",
    min_value=1,
    value=24,
    step=1,
    key="so_thang"
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.5,
    step=0.1,
    key="lai_suat_thang"
)

r = lai_suat / 100 / 12

so_du = tien_ban_dau

for i in range(so_thang):

    so_du = so_du * (1 + r)
    so_du += tien_gui_thang

tong_tien_gui = (
    tien_ban_dau +
    tien_gui_thang * so_thang
)

tong_lai = so_du - tong_tien_gui

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Tổng tiền đã gửi",
        f"{tong_tien_gui:,.0f} VNĐ"
    )

with col2:
    st.metric(
        "📈 Tiền lãi",
        f"{tong_lai:,.0f} VNĐ"
    )

with col3:
    st.metric(
        "🏦 Số dư cuối kỳ",
        f"{so_du:,.0f} VNĐ"
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

st.subheader("📊 Xuất dữ liệu")

csv = df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="📥 Tải dữ liệu mở bằng Excel",
    data=csv,
    file_name="bao_cao_tiet_kiem.csv",
    mime="text/csv"
)

import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Trà Sữa - Tính Tiền Bill",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# DỮ LIỆU MENU
# =========================================================

DRINKS = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa bạc hà": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
}

SIZES = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding": 7000,
    "Kem cheese": 10000,
}

SUGAR_LEVELS = [
    "0% - Không đường",
    "30% - Ít đường",
    "50% - Vừa",
    "70% - Nhiều",
    "100% - Bình thường"
]

ICE_LEVELS = [
    "0% - Không đá",
    "30% - Ít đá",
    "50% - Vừa",
    "70% - Nhiều đá",
    "100% - Bình thường"
]

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def money(value):
    return f"{value:,.0f} đ".replace(",", ".")


# =========================================================
# KHỞI TẠO SESSION
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🧋 TRÀ SỮA")
st.subheader("💵 Hệ thống tính tiền & xuất hóa đơn")

st.divider()


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.markdown("### 👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

col1, col2 = st.columns(2)

with col1:
    payment_method = st.selectbox(
        "💳 Phương thức thanh toán",
        ["Tiền mặt", "Chuyển khoản", "Ví điện tử"]
    )

with col2:
    note = st.text_input(
        "📝 Ghi chú",
        placeholder="Ví dụ: Không lấy ống hút..."
    )


st.divider()


# =========================================================
# THÊM MÓN
# =========================================================

st.markdown("### 🧋 Thêm món")

col1, col2, col3 = st.columns(3)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / nước",
        list(DRINKS.keys())
    )

    size = st.selectbox(
        "Size",
        list(SIZES.keys())
    )

with col2:
    topping = st.selectbox(
        "Topping",
        list(TOPPINGS.keys())
    )

    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVELS
    )

with col3:
    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVELS
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


# =========================================================
# TÍNH GIÁ MÓN
# =========================================================

drink_price = DRINKS[drink]
size_price = SIZES[size]
topping_price = TOPPINGS[topping]

unit_price = drink_price + size_price + topping_price
total_item = unit_price * quantity


st.info(
    f"💰 Đơn giá: **{money(unit_price)}** | "
    f"Thành tiền: **{money(total_item)}**"
)


# =========================================================
# NÚT THÊM MÓN
# =========================================================

if st.button("➕ THÊM MÓN VÀO HÓA ĐƠN", use_container_width=True):

    item = {
        "Tên món": drink,
        "Size": size,
        "Topping": topping,
        "Đường": sugar,
        "Đá": ice,
        "SL": quantity,
        "Đơn giá": unit_price,
        "Thành tiền": total_item
    }

    st.session_state.cart.append(item)

    st.success(f"Đã thêm {quantity} x {drink} vào hóa đơn!")


# =========================================================
# HIỂN THỊ GIỎ HÀNG
# =========================================================

st.divider()

st.markdown("### 🛒 Danh sách món trong hóa đơn")

if len(st.session_state.cart) == 0:

    st.warning("Chưa có món nào trong hóa đơn.")

else:

    # Tạo bảng hiển thị
    table_data = []

    for i, item in enumerate(st.session_state.cart):

        table_data.append({
            "STT": i + 1,
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "SL": item["SL"],
            "Đơn giá": money(item["Đơn giá"]),
            "Thành tiền": money(item["Thành tiền"])
        })

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Tổng tiền
    subtotal = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:24px;
            font-weight:bold;
            padding:15px;
            background:#f5f5f5;
            border-radius:10px;
        ">
        TỔNG TIỀN: {money(subtotal)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Nút xóa
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🗑️ XÓA MÓN CUỐI",
            use_container_width=True
        ):
            st.session_state.cart.pop()
            st.rerun()

    with col2:
        if st.button(
            "❌ XÓA TOÀN BỘ HÓA ĐƠN",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.session_state.invoice = None
            st.rerun()


# =========================================================
# THANH TOÁN
# =========================================================

st.divider()

st.markdown("### 💳 Thanh toán")

if len(st.session_state.cart) > 0:

    subtotal = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    # Giảm giá
    discount_percent = st.number_input(
        "Giảm giá (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

    discount = subtotal * discount_percent / 100

    final_total = subtotal - discount

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tiền hàng",
            money(subtotal)
        )

    with col2:
        st.metric(
            "Giảm giá",
            money(discount)
        )

    with col3:
        st.metric(
            "KHÁCH CẦN TRẢ",
            money(final_total)
        )

    st.write("")

    if st.button(
        "✅ THANH TOÁN & TẠO HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():
            st.error("Vui lòng nhập tên khách hàng!")

        else:

            invoice_code = (
                "HD"
                + datetime.now().strftime("%Y%m%d%H%M%S")
            )

            invoice_time = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            st.session_state.invoice = {
                "code": invoice_code,
                "time": invoice_time,
                "customer": customer_name,
                "payment": payment_method,
                "note": note,
                "items": st.session_state.cart.copy(),
                "subtotal": subtotal,
                "discount_percent": discount_percent,
                "discount": discount,
                "total": final_total
            }

            st.success("🎉 Thanh toán thành công!")

            st.rerun()


# =========================================================
# HIỂN THỊ HÓA ĐƠN
# =========================================================

if st.session_state.invoice is not None:

    invoice = st.session_state.invoice

    st.divider()

    st.markdown("## 🧾 HÓA ĐƠN")

    # Khung hóa đơn
    st.markdown(
        f"""
        <div style="
            border:2px solid #333;
            border-radius:12px;
            padding:25px;
            background:white;
        ">

        <div style="text-align:center;">
            <h1>🧋 TRÀ SỮA</h1>
            <p>HÓA ĐƠN THANH TOÁN</p>
        </div>

        <hr>

        <p><b>Mã hóa đơn:</b> {invoice["code"]}</p>
        <p><b>Thời gian:</b> {invoice["time"]}</p>
        <p><b>Khách hàng:</b> {invoice["customer"]}</p>
        <p><b>Thanh toán:</b> {invoice["payment"]}</p>

        <hr>

        """,
        unsafe_allow_html=True
    )

    # Danh sách món trong hóa đơn
    invoice_table = []

    for i, item in enumerate(invoice["items"]):

        invoice_table.append({
            "STT": i + 1,
            "Món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "SL": item["SL"],
            "Đơn giá": money(item["Đơn giá"]),
            "Thành tiền": money(item["Thành tiền"])
        })

    invoice_df = pd.DataFrame(invoice_table)

    st.dataframe(
        invoice_df,
        use_container_width=True,
        hide_index=True
    )

    # Tổng hóa đơn
    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:18px;
            line-height:1.8;
        ">

        <b>Tiền hàng:</b> {money(invoice["subtotal"])}<br>

        <b>Giảm giá:</b>
        {invoice["discount_percent"]}% -
        {money(invoice["discount"])}<br>

        <hr>

        <b style="font-size:26px;">
        TỔNG THANH TOÁN: {money(invoice["total"])}
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )

    if invoice["note"]:
        st.info(f"📝 Ghi chú: {invoice['note']}")

    st.success("Cảm ơn quý khách! Hẹn gặp lại ❤️")


    # =====================================================
    # XUẤT HÓA ĐƠN
    # =====================================================

    st.divider()

    st.markdown("### 📥 Xuất hóa đơn")

    # Tạo file Excel
    export_rows = []

    for i, item in enumerate(invoice["items"]):

        export_rows.append({
            "STT": i + 1,
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Mức độ đường": item["Đường"],
            "Mức độ đá": item["Đá"],
            "Số lượng": item["SL"],
            "Đơn giá": item["Đơn giá"],
            "Thành tiền": item["Thành tiền"]
        })

    export_df = pd.DataFrame(export_rows)

    # Xuất Excel
    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Hoa Don"
        )

        # Thông tin tổng
        summary_df = pd.DataFrame({
            "Thông tin": [
                "Mã hóa đơn",
                "Thời gian",
                "Khách hàng",
                "Phương thức thanh toán",
                "Tiền hàng",
                "Giảm giá",
                "Tổng thanh toán"
            ],
            "Giá trị": [
                invoice["code"],
                invoice["time"],
                invoice["customer"],
                invoice["payment"],
                invoice["subtotal"],
                invoice["discount"],
                invoice["total"]
            ]
        })

        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Thong Tin"
        )

    excel_buffer.seek(0)

    st.download_button(
        label="📊 TẢI HÓA ĐƠN EXCEL",
        data=excel_buffer,
        file_name=f"{invoice['code']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧋 Ứng dụng tính tiền trà sữa - Streamlit"
)

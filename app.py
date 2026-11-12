
import streamlit as st
import sqlite3
import pandas as pd
import uuid
from datetime import datetime, date, time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="DeliveryNow | Smart Parcel Delivery",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB = "deliveries.db"

# ---------------- DATABASE ----------------

def connect_db():
    return sqlite3.connect(DB)

def initialize_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deliveries (
            booking_id TEXT PRIMARY KEY,
            sender TEXT,
            receiver TEXT,
            phone TEXT,
            pickup TEXT,
            destination TEXT,
            delivery_date TEXT,
            delivery_time TEXT,
            parcel_type TEXT,
            weight REAL,
            service TEXT,
            price REAL,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_booking(data):
    conn = connect_db()
    conn.execute("""
        INSERT INTO deliveries VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, data)
    conn.commit()
    conn.close()

def get_booking(booking_id):
    conn = connect_db()
    result = pd.read_sql_query(
        "SELECT * FROM deliveries WHERE booking_id = ?",
        conn,
        params=(booking_id,)
    )
    conn.close()
    return result

def get_all_bookings():
    conn = connect_db()
    result = pd.read_sql_query(
        "SELECT * FROM deliveries ORDER BY created_at DESC",
        conn
    )
    conn.close()
    return result

def update_status(booking_id, status):
    conn = connect_db()
    conn.execute(
        "UPDATE deliveries SET status = ? WHERE booking_id = ?",
        (status, booking_id)
    )
    conn.commit()
    conn.close()

initialize_db()

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #080d1c, #111a32);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(120deg, #172b56, #44318b);
    border: 1px solid #465b94;
    padding: 45px;
    border-radius: 24px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    color: white;
}

.hero p {
    color: #d0d9f2;
    font-size: 17px;
}

.metric-card {
    background: #17233c;
    border: 1px solid #2d4166;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 12px;
}

.metric-card h2 {
    color: #8eacff;
    font-size: 28px;
}

.metric-card p {
    color: #c1cce0;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

div[data-testid="stForm"] {
    background: #121f38;
    border: 1px solid #34476b;
    border-radius: 18px;
    padding: 22px;
}

.stButton button {
    background: linear-gradient(90deg, #5965e8, #8655d8);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

.stButton button:hover {
    border: 1px solid white;
    color: white;
}

label, .stMarkdown p {
    color: #e2e9f7;
}

[data-testid="stSidebar"] {
    background: #101a30;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------

st.markdown("""
<div style="display:flex;justify-content:space-between;
align-items:center;padding:10px 0 25px;">
    <div style="font-size:25px;font-weight:800;color:#9caeff;">
        📦 DeliveryNow
    </div>
    <div style="color:#aab8d4;font-size:14px;">
        SMART DELIVERY EXPERIENCE
    </div>
</div>
""", unsafe_allow_html=True)

page = st.radio(
    "Navigation",
    ["Home", "Book Delivery", "Track Parcel", "Admin Dashboard"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------------- HOME ----------------

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Deliver on Your Time.</h1>
        <p>
        Smart parcel scheduling, convenient time slots,
        transparent pricing and easy tracking.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_bookings()

    total = len(df)
    delivered = 0 if df.empty else len(
        df[df["status"] == "Delivered"]
    )
    active = total - delivered

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<div class="metric-card"><h2>{total}</h2>'
            '<p>Total Bookings</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<div class="metric-card"><h2>{active}</h2>'
            '<p>Active Deliveries</p></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f'<div class="metric-card"><h2>{delivered}</h2>'
            '<p>Delivered Parcels</p></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Why Choose DeliveryNow?</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            '<div class="metric-card"><h2>🕒</h2>'
            '<b>Flexible Scheduling</b><p>Select your preferred '
            'delivery date and time.</p></div>',
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            '<div class="metric-card"><h2>📍</h2>'
            '<b>Parcel Tracking</b><p>Check the latest status '
            'of your parcel.</p></div>',
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            '<div class="metric-card"><h2>⚡</h2>'
            '<b>Express Service</b><p>Choose a faster delivery '
            'service.</p></div>',
            unsafe_allow_html=True
        )

    st.info("Choose Book Delivery from the navigation to schedule a parcel.")

# ---------------- BOOK DELIVERY ----------------

elif page == "Book Delivery":

    st.title("📦 Book Your Delivery")
    st.write("Enter your parcel details and choose your preferred time.")

    with st.form("booking_form"):

        st.subheader("Sender Information")

        sender = st.text_input("Sender Name")
        phone = st.text_input("Contact Number")

        pickup = st.text_input("Pickup Address")

        st.divider()

        st.subheader("Receiver Information")

        receiver = st.text_input("Receiver Name")
        destination = st.text_input("Delivery Address")

        st.divider()

        st.subheader("Parcel Information")

        col1, col2 = st.columns(2)

        with col1:
            parcel_type = st.selectbox(
                "Parcel Type",
                ["Documents", "Electronics", "Clothing", "Other"]
            )

            weight = st.number_input(
                "Parcel Weight (kg)",
                min_value=0.1,
                max_value=100.0,
                value=1.0,
                step=0.5
            )

        with col2:
            service = st.selectbox(
                "Delivery Service",
                ["Standard", "Express"]
            )

            delivery_date = st.date_input(
                "Preferred Delivery Date",
                min_value=date.today()
            )

            delivery_time = st.time_input(
                "Preferred Delivery Time",
                value=time(12, 0)
            )

        submitted = st.form_submit_button(
            "Calculate & Book Parcel",
            use_container_width=True
        )

        if submitted:

            if not all([
                sender.strip(),
                receiver.strip(),
                phone.strip(),
                pickup.strip(),
                destination.strip()
            ]):
                st.error("Please complete all required fields.")

            elif not phone.isdigit() or len(phone) != 10:
                st.error("Enter a valid 10-digit contact number.")

            elif (
                delivery_date == date.today()
                and delivery_time <= datetime.now().time()
            ):
                st.error("Choose a future delivery time.")

            else:

                # Demo pricing calculation
                base_price = 50
                weight_charge = weight * 20

                service_charge = (
                    100 if service == "Express" else 0
                )

                price = base_price + weight_charge + service_charge

                booking_id = "DN" + uuid.uuid4().hex[:8].upper()

                booking_data = (
                    booking_id,
                    sender.strip(),
                    receiver.strip(),
                    phone,
                    pickup.strip(),
                    destination.strip(),
                    str(delivery_date),
                    str(delivery_time),
                    parcel_type,
                    weight,
                    service,
                    price,
                    "Booked",
                    datetime.now().isoformat(timespec="seconds")
                )

                try:
                    save_booking(booking_data)

                    st.success("Your parcel has been booked!")
                    st.balloons()

                    st.markdown(
                        f"""
                        <div class="hero">
                            <h2>Booking Confirmed!</h2>
                            <p>Your booking ID is</p>
                            <h1>{booking_id}</h1>
                            <p>Estimated demo price: ₹{price:.2f}</p>
                            <p>Keep this booking ID to track your parcel.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except sqlite3.Error:
                    st.error("Unable to save booking. Please try again.")

# ---------------- TRACK PARCEL ----------------

elif page == "Track Parcel":

    st.title("📍 Track Your Parcel")
    st.write("Enter your booking ID to check delivery status.")

    booking_id = st.text_input("Booking ID")

    if st.button("Track Now"):

        if not booking_id.strip():
            st.warning("Please enter a booking ID.")

        else:
            result = get_booking(booking_id.strip().upper())

            if result.empty:
                st.error("No booking found. Check your booking ID.")

            else:
                parcel = result.iloc[0]

                st.markdown(
                    f"""
                    <div class="hero">
                        <h2>Parcel Tracking</h2>
                        <h1>{parcel['status']}</h1>
                        <p>Booking ID: {parcel['booking_id']}</p>
                        <p>Receiver: {parcel['receiver']}</p>
                        <p>Destination: {parcel['destination']}</p>
                        <p>Scheduled: {parcel['delivery_date']}
                        at {parcel['delivery_time']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                steps = [
                    "Booked",
                    "Picked Up",
                    "In Transit",
                    "Out for Delivery",
                    "Delivered"
                ]

                current = parcel["status"]

                if current in steps:
                    progress = steps.index(current) / (len(steps) - 1)
                    st.progress(progress)

                    for step in steps:
                        if steps.index(step) <= steps.index(current):
                            st.success("✓ " + step)
                        else:
                            st.write("○ " + step)

                elif current == "Cancelled":
                    st.warning("This booking has been cancelled.")

# ---------------- ADMIN DASHBOARD ----------------

elif page == "Admin Dashboard":

    st.title("⚙️ Admin Dashboard")

    st.write("Authorized administrators can manage bookings.")

    try:
        admin_password = st.secrets["ADMIN_PASSWORD"]
    except Exception:
        admin_password = None

    if not admin_password:
        st.warning(
            "Configure ADMIN_PASSWORD in .streamlit/secrets.toml "
            "before using the admin dashboard."
        )

    else:
        entered_password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("Login"):

            if entered_password == admin_password:
                st.session_state["admin_logged_in"] = True
            else:
                st.error("Incorrect password.")

        if st.session_state.get("admin_logged_in", False):

            df = get_all_bookings()

            st.subheader("All Parcel Bookings")

            if df.empty:
                st.info("No bookings yet.")

            else:
                st.dataframe(df, use_container_width=True)

                selected_id = st.selectbox(
                    "Select Booking ID",
                    df["booking_id"].tolist()
                )

                new_status = st.selectbox(
                    "Update Delivery Status",
                    [
                        "Booked",
                        "Picked Up",
                        "In Transit",
                        "Out for Delivery",
                        "Delivered",
                        "Cancelled"
                    ]
                )

                if st.button("Update Status"):
                    update_status(selected_id, new_status)
                    st.success("Delivery status updated!")
                    st.rerun()

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Booking Records",
                    csv,
                    "delivery_bookings.csv",
                    "text/csv"
                )

            if st.button("Logout"):
                st.session_state["admin_logged_in"] = False
                st.rerun()

# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center;color:#8999b8;padding:20px;">
    <b>DeliveryNow</b><br>
    Smart Delivery Scheduling Platform<br>
    Built with Python and Streamlit
</div>
""", unsafe_allow_html=True)

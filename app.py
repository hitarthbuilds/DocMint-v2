import streamlit as st
from utils.session import init_session
from core.auth import login_ui, logout_user

# Page config
st.set_page_config(
    page_title="DocMint",
    page_icon="🍃",
    layout="wide"
)

# Init session state
init_session()

# Ensure logout flag exists
if "logout_trigger" not in st.session_state:
    st.session_state.logout_trigger = False


# -------------------------
# AUTH CHECK
# -------------------------
if st.session_state.user is None:
    login_ui()

else:
    # Sidebar for authenticated users
    with st.sidebar:
        st.title("🍃 DocMint")
        st.write(f"Logged in as **{st.session_state.user['email']}**")

        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/2_Documents.py", label="📁 Documents")
        st.page_link("pages/3_Chat.py", label="💬 Chat")
        st.page_link("pages/4_Profile.py", label="👤 Profile")
        st.page_link("pages/5_Billing.py", label="💳 Billing")

        # Safe logout button (NO rerun here)
        if st.button("Logout"):
            logout_user()

    # After logout, handle rerun safely
    if st.session_state.logout_trigger:
        st.session_state.logout_trigger = False
        st.rerun()

    st.title("Welcome to DocMint")
    st.write("Choose a page from the sidebar to get started.")

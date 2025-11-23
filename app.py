import streamlit as st
from utils.session import init_session
from core.auth import login_ui, logout_user

# Page configuration
st.set_page_config(
    page_title="DocMint",
    page_icon="🍃",
    layout="wide"
)

# Initialize session state keys
init_session()

# AUTH CHECK
if st.session_state.user is None:

    # User not logged in → show login UI only
    login_ui()

else:
    # Sidebar navigation for logged-in users
    with st.sidebar:
        st.title("🍃 DocMint")

        st.write(f"Logged in as **{st.session_state.user['email']}**")

        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/2_Documents.py", label="📁 Documents")
        st.page_link("pages/3_Chat.py", label="💬 Chat")
        st.page_link("pages/4_Profile.py", label="👤 Profile")
        st.page_link("pages/5_Billing.py", label="💳 Billing")

        st.button("Logout", on_click=logout_user)

    st.title("Welcome to DocMint")
    st.write("Choose a page from the sidebar to get started.")

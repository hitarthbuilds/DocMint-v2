import streamlit as st

# -------------------------
# LOGIN UI
# -------------------------
def login_ui():
    st.title("Login to DocMint")
    st.write("Enter your credentials to continue.")

    # Ensure state keys exist
    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_trigger" not in st.session_state:
        st.session_state.login_trigger = False

    # Normal fields (NO FORM — no callback trap)
    email = st.text_input("Email", placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

    # Login button (safe)
    if st.button("Login"):
        if not email or not password:
            st.error("Both fields are required.")
        else:
            st.session_state.user = {"email": email}
            st.session_state.login_trigger = True

    # Safe rerun OUTSIDE callback
    if st.session_state.login_trigger:
        st.session_state.login_trigger = False
        st.rerun()


# -------------------------
# LOGOUT HANDLER
# -------------------------
def logout_user():
    # ONLY modify session state. No reruns here.
    st.session_state.user = None
    st.session_state.logout_trigger = True

import streamlit as st

def login_ui():
    st.title("Login to DocMint")
    st.write("Enter your credentials to continue.")

    # initialize flags
    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_trigger" not in st.session_state:
        st.session_state.login_trigger = False

    # normal inputs (NOT inside a form)
    email = st.text_input("Email", placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

    # login button (safe callback)
    if st.button("Login"):
        if not email or not password:
            st.error("Both fields required.")
        else:
            st.session_state.user = {"email": email}
            st.session_state.login_trigger = True

    # RERUN (outside any callback)
    if st.session_state.login_trigger:
        st.session_state.login_trigger = False
        st.rerun()


def logout_user():
    # initialize flag
    if "logout_trigger" not in st.session_state:
        st.session_state.logout_trigger = False

    # set user to None
    st.session_state.user = None
    st.session_state.logout_trigger = True

    # rerun completely safely
    if st.session_state.logout_trigger:
        st.session_state.logout_trigger = False
        st.rerun()

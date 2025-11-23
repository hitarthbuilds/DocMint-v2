import streamlit as st

def login_ui():
    st.title("Login to DocMint")
    st.write("Enter your credentials to continue.")

    # temporary flag for rerun
    if "login_trigger_rerun" not in st.session_state:
        st.session_state.login_trigger_rerun = False

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Both email and password are required.")
            else:
                # store login data
                st.session_state.user = {"email": email}
                st.session_state.login_trigger_rerun = True
                st.success("Logged in successfully!")

    # rerun OUTSIDE callback
    if st.session_state.login_trigger_rerun:
        st.session_state.login_trigger_rerun = False
        st.rerun()


def logout_user():
    # same logic for logout
    st.session_state.user = None
    st.session_state.logout_trigger_rerun = True

    if "logout_trigger_rerun" not in st.session_state:
        st.session_state.logout_trigger_rerun = False

    if st.session_state.logout_trigger_rerun:
        st.session_state.logout_trigger_rerun = False
        st.rerun()

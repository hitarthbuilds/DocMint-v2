import streamlit as st

def login_ui():
    st.title("Login to DocMint")
    st.write("Enter your credentials to continue.")

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Both email and password are required.")
                return

            # This is TEMPORARY login logic
            # Later replaced with Supabase or Firebase
            st.session_state.user = {
                "email": email
            }

            st.success("Logged in successfully!")
            st.experimental_rerun()

def logout_user():
    st.session_state.user = None
    st.experimental_rerun()

import streamlit as st
import hashlib

from auth.database import add_user, get_user, create_users_table


# -------------------------
# Password Hashing
# -------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------
# Signup Logic
# -------------------------
def signup_user():
    st.subheader("Create New Account")

    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Signup"):
        if not username or not password:
            st.warning("Please fill all fields")
            return

        create_users_table()
        hashed_password = hash_password(password)

        success = add_user(username, hashed_password)

        if success:
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists")


# -------------------------
# Login Logic
# -------------------------
def login_user():
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not username or not password:
            st.warning("Please fill all fields")
            return

        create_users_table()
        user = get_user(username)

        if user:
            stored_username, stored_password = user
            if hash_password(password) == stored_password:
                st.session_state.logged_in = True
                st.session_state.username = stored_username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")

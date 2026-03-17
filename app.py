import streamlit as st

# =========================
# Load Custom CSS
# =========================
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =========================
# Auth Modules
# =========================
from auth.auth import login_user, signup_user

# =========================
# Analytics Modules
# =========================
from analytics import (
    eda,
    volatility,
    forecasting,
    insights,
    sentiment_analysis
)

# =========================
# App Configuration
# =========================
st.set_page_config(
    page_title="Crypto Time Series Dashboard",
    layout="wide"
)

# =========================
# Session State Init
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# =========================
# Authentication Page
# =========================
def auth_page():
    st.title("🔐 Crypto Analytics Platform")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        login_user()

    with tab2:
        signup_user()


# =========================
# Dashboard
# =========================
def dashboard():
    st.sidebar.title("📊 Dashboard")
    st.sidebar.write(f"👤 User: {st.session_state.username}")

    page = st.sidebar.radio(
        "Go to",
        [
            "EDA",
            "Volatility Analysis",
            "Forecasting",
            "Insights",
            "Sentiment Analysis"
        ]
    )

    st.sidebar.button("🚪 Logout", on_click=logout)

    # -------- Routing Only --------
    if page == "EDA":
        eda.render()

    elif page == "Volatility Analysis":
        volatility.render()

    elif page == "Forecasting":
        forecasting.render()

    elif page == "Insights":
        insights.render()

    elif page == "Sentiment Analysis":
        sentiment_analysis.render()


# =========================
# Logout
# =========================
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()


# =========================
# Main Controller
# =========================
def main():
    load_css()  # ✅ APPLY CSS GLOBALLY

    if not st.session_state.logged_in:
        auth_page()
    else:
        dashboard()


main()

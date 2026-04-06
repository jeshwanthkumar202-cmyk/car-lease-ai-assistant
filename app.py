# ===============================
# app.py (FINAL FIXED WHITE UI + EXTRA FEATURES)
# ===============================

import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Car Lease AI Assistant", layout="wide")

# ---------------- FORCE WHITE THEME ----------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: white !important;
    color: black !important;
}

h1, h2, h3 {
    color: #003366 !important;
    font-weight: bold;
}

p, label, div, span {
    color: black !important;
    font-size: 17px !important;
}

.stTextInput input {
    background-color: #f5f5f5 !important;
    color: black !important;
}

.stButton>button {
    background-color: #007acc !important;
    color: white !important;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

section[data-testid="stSidebar"] {
    background-color: #f2f2f2 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")


def analyze(text):
    risks = []

    if "interest" in text.lower():
        risks.append("High Interest Rate")
    if "penalty" in text.lower():
        risks.append("Penalty Charges")
    if "fee" in text.lower():
        risks.append("Hidden Fees")
    if "termination" in text.lower():
        risks.append("Termination Clause")

    if not risks:
        risks.append("No major risks found ✅")

    return risks

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login Page")

    st.markdown("---")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Credentials ❌")

# ---------------- MAIN APP ----------------
def main():

    st.sidebar.title("🚗 Car Lease AI Assistant")

    menu = st.sidebar.selectbox("Select Option", [
        "🏠 Home",
        "📄 Upload Contract",
        "⚠️ Risk Analysis",
        "💬 Chatbot",
        "📊 Dashboard",
        "📥 Download Report"
    ])

    # HOME
    if menu == "🏠 Home":
        st.title("🚗 Car Lease AI Assistant")
        st.write("AI tool to analyze lease/loan contracts.")

    # UPLOAD
    elif menu == "📄 Upload Contract":
        st.title("📄 Upload Contract")
        file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

        if file:
            text = extract_text(file)
            st.session_state.text = text
            st.success("File uploaded successfully ✅")

            st.subheader("Summary")
            st.write(text[:500])

    # RISK
    elif menu == "⚠️ Risk Analysis":
        st.title("⚠️ Risk Analysis")

        if "text" in st.session_state:
            risks = analyze(st.session_state.text)

            for r in risks:
                st.warning(r)
        else:
            st.info("Upload contract first")

    # CHATBOT
    elif menu == "💬 Chatbot":
        st.title("💬 AI Chatbot")

        q = st.text_input("Ask question")

        if q:
            st.success("Try negotiating interest rate and removing hidden charges.")

    # DASHBOARD
    elif menu == "📊 Dashboard":
        st.title("📊 Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Contracts", "10")
        col2.metric("Risks", "4")
        col3.metric("Savings", "₹20,000")

    # DOWNLOAD
    elif menu == "📥 Download Report":
        st.title("📥 Download")

        if "text" in st.session_state:
            st.download_button("Download Report", st.session_state.text)
        else:
            st.info("Upload file first")

# ---------------- RUN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main()
else:
    login()

# ===============================
# requirements.txt
# ===============================
# streamlit
# pandas
# PyPDF2

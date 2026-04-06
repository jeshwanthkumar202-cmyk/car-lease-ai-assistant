# ===============================
# app.py (FINAL FIX - TEXT VISIBILITY 100%)
# ===============================

import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Car Lease AI Assistant", layout="wide")

# ---------------- FORCE FULL LIGHT MODE ----------------
st.markdown("""
<style>

/* Force entire app white */
html, body, .stApp {
    background-color: white !important;
}

/* Fix ALL text visibility */
* {
    color: black !important;
}

/* FIX SIDEBAR DARK TEXT ISSUE */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* Fix selectbox selected value */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Fix dropdown menu items */
ul[role="listbox"] li {
    color: black !important;
}

/* Fix file uploader text */
div[data-testid="stFileUploader"] span {
    color: black !important;
}

/* Fix success/alert text */
div[data-testid="stAlert"] * {
    color: black !important;
}

/* Headings */
h1, h2, h3 {
    color: #003366 !important;
    font-weight: bold !important;
}

/* Sidebar fix */
section[data-testid="stSidebar"] {
    background-color: #f0f2f6 !important;
    color: black !important;
}

/* Fix dropdown/selectbox text visibility */
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: black !important;
}

/* Fix uploaded file box */
div[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    color: black !important;
}

/* Fix success box */
.stAlert {
    color: black !important;
}

/* Inputs */
input, textarea {
    background-color: #ffffff !important;
    color: black !important;
}

/* Buttons */
.stButton>button {
    background-color: #007acc !important;
    color: white !important;
    border-radius: 8px;
    font-size: 16px;
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

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Credentials ❌")

# ---------------- MAIN ----------------
def main():

    st.sidebar.title("🚗 Car Lease AI Assistant")

    menu = st.sidebar.selectbox("Select Option", [
        "Home",
        "Upload",
        "Risk",
        "Chat",
        "Dashboard",
        "Download"
    ])

    if menu == "Home":
        st.title("Car Lease AI Assistant")
        st.write("AI tool to analyze lease/loan contracts.")

    elif menu == "Upload":
        st.title("Upload Contract")
        file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

        if file:
            text = extract_text(file)
            st.session_state.text = text
            st.success("Uploaded successfully")
            st.write(text[:500])

    elif menu == "Risk":
        st.title("Risk Analysis")

        if "text" in st.session_state:
            risks = analyze(st.session_state.text)
            for r in risks:
                st.warning(r)
        else:
            st.info("Upload file first")

    elif menu == "Chat":
        st.title("Chatbot")
        q = st.text_input("Ask question")
        if q:
            st.success("Negotiate interest and remove hidden fees.")

    elif menu == "Dashboard":
        st.title("Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Contracts", "10")
        c2.metric("Risks", "3")
        c3.metric("Savings", "₹15,000")

    elif menu == "Download":
        st.title("Download Report")
        if "text" in st.session_state:
            st.download_button("Download", st.session_state.text)
        else:
            st.info("Upload first")

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

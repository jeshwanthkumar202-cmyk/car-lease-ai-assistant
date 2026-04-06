# ===============================
# app.py (ULTIMATE FINAL VERSION - PRO MAX UI + AI FEATURES)
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Car Lease AI Assistant", layout="wide")

# ---------------- CUSTOM CSS (HIGH VISIBILITY UI) ----------------
st.markdown("""
<style>
body, .main {
    background-color: white;
}

h1, h2, h3 {
    color: #0b3c5d;
    font-weight: 800;
}

p, label, div {
    color: #000000 !important;
    font-size: 17px;
}

.stButton>button {
    background: linear-gradient(90deg, #007acc, #005f99);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

section[data-testid="stSidebar"] {
    background-color: #f0f2f6;
}

.stTextInput>div>div>input {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def analyze_contract(text):
    risks = []

    patterns = {
        "High Interest Clause": ["interest", "apr", "rate"],
        "Penalty Clause": ["penalty", "fine", "charge"],
        "Hidden Fees": ["processing fee", "hidden", "extra charge"],
        "Termination Risk": ["termination", "cancel", "closure"],
        "Insurance Add-ons": ["insurance", "coverage"],
        "Late Payment Risk": ["late payment", "delay fee"]
    }

    for risk, keywords in patterns.items():
        for word in keywords:
            if word in text.lower():
                risks.append(risk)
                break

    if not risks:
        risks.append("No major risks detected ✅")

    return risks


def risk_score(risks):
    return min(len(risks) * 20, 100)


def generate_summary(text):
    return text[:700] + "..." if len(text) > 700 else text


def chatbot_response(query):
    query = query.lower()

    if "interest" in query:
        return "Negotiate a lower APR and compare with other lenders before signing."
    elif "penalty" in query:
        return "Request removal or reduction of penalty clauses."
    elif "fees" in query:
        return "Ask for a full fee breakdown and eliminate unnecessary charges."
    elif "insurance" in query:
        return "Check if insurance add-ons are optional and remove if not needed."
    else:
        return "Focus on reducing interest, removing hidden fees, and flexible terms."

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 Secure Login")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("👤 Username")
        pwd = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            if user == "admin" and pwd == "1234":
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
            else:
                st.error("Invalid Credentials ❌")

# ---------------- MAIN APP ----------------
def main_app():
    st.sidebar.title("🚗 Car Lease AI Pro")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False

    menu = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "📄 Upload & Analyze",
        "⚠️ Risk Analysis",
        "💬 AI Chat",
        "📈 Analytics",
        "📑 Report Download",
        "ℹ️ About"
    ])

    # ---------- DASHBOARD ----------
    if menu == "📊 Dashboard":
        st.title("📊 Executive Dashboard")

        col1, col2, col3 = st.columns(3)
        col1.metric("Contracts", "25")
        col2.metric("Risks Found", "12")
        col3.metric("Savings Potential", "₹75,000")

        st.info("💡 Upload a contract to get started with AI analysis.")

    # ---------- UPLOAD ----------
    elif menu == "📄 Upload & Analyze":
        st.title("📄 Upload Contract")

        file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

        if file:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")

            st.session_state.contract_text = text

            st.success("✅ Contract processed successfully")

            st.subheader("📑 AI Summary")
            st.write(generate_summary(text))

    # ---------- RISK ----------
    elif menu == "⚠️ Risk Analysis":
        st.title("⚠️ Smart Risk Detection")

        if "contract_text" in st.session_state:
            risks = analyze_contract(st.session_state.contract_text)
            score = risk_score(risks)

            for r in risks:
                st.warning(f"⚠️ {r}")

            st.subheader("📊 Risk Score")
            st.progress(score)
            st.write(f"Risk Level: {score}%")
        else:
            st.info("Upload contract first")

    # ---------- CHAT ----------
    elif menu == "💬 AI Chat":
        st.title("💬 Negotiation AI Assistant")

        query = st.text_input("Ask anything about your contract...")

        if query:
            response = chatbot_response(query)
            st.success(response)

    # ---------- ANALYTICS ----------
    elif menu == "📈 Analytics":
        st.title("📈 Insights Dashboard")

        data = pd.DataFrame({
            "Category": ["Interest", "Penalty", "Fees", "Termination", "Insurance"],
            "Count": [5, 4, 6, 3, 2]
        })

        st.bar_chart(data.set_index("Category"))

    # ---------- REPORT ----------
    elif menu == "📑 Report Download":
        st.title("📑 Download Report")

        if "contract_text" in st.session_state:
            report = generate_summary(st.session_state.contract_text)
            st.download_button("📥 Download Summary", report, file_name="report.txt")
        else:
            st.info("Upload contract first")

    # ---------- ABOUT ----------
    elif menu == "ℹ️ About":
        st.title("ℹ️ About Project")
        st.write("AI-powered system for analyzing car lease and loan contracts.")
        st.write("Includes risk detection, smart insights, and negotiation support.")

# ---------------- APP CONTROL ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main_app()

# ===============================
# requirements.txt
# ===============================
# streamlit
# pandas
# numpy
# PyPDF2


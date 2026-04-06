  import streamlit as st
import PyPDF2

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Car Contract AI Assistant", layout="wide")

# ------------------ FINAL UI FIX ------------------
st.markdown("""
<style>

/* Force white theme */
html, body, .stApp {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* Force ALL text visible */
* {
    color: #000000 !important;
}

/* Headings */
h1, h2, h3 {
    color: #1A5276 !important;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F4F6F7 !important;
}

/* Buttons */
.stButton > button {
    background-color: #1A5276 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 15px;
    font-size: 16px;
}

/* Inputs */
input, textarea {
    background-color: #F8F9F9 !important;
    color: black !important;
    border-radius: 8px;
}

/* Cards */
.card {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

/* Fix text inside cards */
.card * {
    color: #000000 !important;
}

/* Metric fix */
[data-testid="stMetricValue"] {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ LOGIN ------------------
def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

# ------------------ SIDEBAR ------------------
def sidebar():
    st.sidebar.title("🚗 Navigation")

    page = st.sidebar.radio("Go to", [
        "Dashboard",
        "Upload & Analyze",
        "AI Assistant",
        "Negotiation Helper",
        "History"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    return page

# ------------------ DASHBOARD ------------------
def dashboard():
    st.title("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
        <h3>Total Contracts</h3>
        <h2>{len(st.session_state.history)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>Status</h3>
        <p>System Running Smoothly ✅</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("🚗 Welcome! Upload and analyze car lease contracts easily.")

# ------------------ PDF READER ------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ------------------ ANALYSIS ------------------
def analyze_contract(text):
    risks = []

    if "interest" in text.lower():
        risks.append("⚠ Interest rate clause detected")
    if "penalty" in text.lower():
        risks.append("⚠ Penalty clause detected")
    if "fine" in text.lower():
        risks.append("⚠ Hidden fine detected")

    summary = text[:500]

    return summary, risks

# ------------------ UPLOAD PAGE ------------------
def upload_page():
    st.title("📄 Upload & Analyze Contract")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        text = read_pdf(file)
        summary, risks = analyze_contract(text)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Contract Summary")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠ Risk Analysis")
        if risks:
            for r in risks:
                st.warning(r)
        else:
            st.success("No major risks detected ✅")
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.history.append(summary)

# ------------------ AI ASSISTANT ------------------
def ai_assistant():
    st.title("🤖 AI Assistant")

    query = st.text_input("Ask about your contract")

    if st.button("Get Answer"):
        st.success("👉 Suggestion: Carefully review interest rates, penalties, and loan tenure before signing.")

# ------------------ NEGOTIATION ------------------
def negotiation():
    st.title("💬 Negotiation Helper")

    issue = st.selectbox("Select Issue", [
        "High Interest Rate",
        "Penalty Charges",
        "Loan Tenure"
    ])

    if st.button("Generate Message"):
        st.success(f"""
Dear Sir/Madam,

I would like to request a revision of the {issue.lower()} to better align with fair and flexible terms.

Kindly consider my request.

Thank you.
""")

# ------------------ HISTORY ------------------
def history():
    st.title("📁 History")

    if not st.session_state.history:
        st.info("No contracts analyzed yet.")

    for i, item in enumerate(st.session_state.history):
        st.markdown(f"""
        <div class="card">
        <b>Contract {i+1}</b><br>
        {item[:150]}...
        </div>
        """, unsafe_allow_html=True)

# ------------------ MAIN ------------------
if not st.session_state.logged_in:
    login()
else:
    page = sidebar()

    if page == "Dashboard":
        dashboard()
    elif page == "Upload & Analyze":
        upload_page()
    elif page == "AI Assistant":
        ai_assistant()
    elif page == "Negotiation Helper":
        negotiation()
    elif page == "History":
        history()

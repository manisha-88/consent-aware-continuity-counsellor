import streamlit as st

# 1. Page Config
st.set_page_config(
    page_title="Consent-Aware Continuity Counsellor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# 2. Master CSS for Top-to-Bottom Flex Alignment & Clean Tabs
st.markdown("""
    <style>
    /* Hide Default Streamlit Navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Remove padding around sidebar to align header flush at the top */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        padding-bottom: 1rem;
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    /* Uniform Nav Buttons (Same height, width, and alignment) */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-align: left !important;
        padding-left: 16px !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #e2e8f0 !important;
        border-color: #cbd5e1 !important;
    }
    
    /* Highlight Active Button */
    div[data-testid="stSidebar"] .stButton > button[aria-selected="true"],
    div[data-testid="stSidebar"] .active-tab > button {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Container Construction
with st.sidebar:
    # TOP: Header Card (Flush to Top)
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            padding: 20px 16px;
            margin: 0 -0.8rem 20px -0.8rem;
            color: white;
            border-radius: 0 0 12px 12px;
        ">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-size: 16px; font-weight: 700;">🛡️ Consent-Aware Counsellor</div>
            </div>
            <div style="font-size: 11px; color: #93c5fd; margin-top: 4px;">
                Respecting Consent. Ensuring Continuity.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # MIDDLE: Navigation Tabs (Same Size Buttons, No Radio Circles)
    if st.button("🏠  Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("📋  Case Handover", use_container_width=True):
        st.session_state.page = "Case Handover"
        st.rerun()

    if st.button("🕘  Audit History", use_container_width=True):
        st.session_state.page = "Audit History"
        st.rerun()

    # FLEX SPACER: Pushes bottom card to the absolute bottom of sidebar
    st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)

    # BOTTOM: Confidentiality Disclaimer Card
    st.markdown("""
        <div style="
            background-color: #eff6ff; 
            border: 1px solid #bfdbfe; 
            padding: 12px; 
            border-radius: 8px; 
            color: #1e40af; 
            font-size: 12px;
            margin-bottom: 10px;
        ">
            <strong>🛡️ Safe. Ethical. Confidential.</strong><br>
            <span style="font-size: 11px; color: #3b82f6;">
                This system uses synthetic data for educational and research purposes only.
            </span>
        </div>
    """, unsafe_allow_html=True)

# Main App View Routing
page = st.session_state.page

if page == "Dashboard":
    st.title("🏠 Counselling Continuity Dashboard")
    st.caption("An overview of the consent-aware continuity handover system.")
elif page == "Case Handover":
    st.title("📋 Case Handover")
    st.caption("Generate a consent-aware continuity handover summary.")
elif page == "Audit History":
    st.title("🕘 Audit History")
    st.caption("System activity logs and handover verification history.")
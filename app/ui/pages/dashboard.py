import streamlit as st
import pandas as pd

def show_dashboard():
    # Page Header
    st.title("🏠 Counselling Continuity Dashboard")
    st.caption("An overview of the consent-aware continuity handover system.")
    st.divider()

    # 1. System Overview Section
    st.subheader("System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Clients", value=12)
    with col2:
        st.metric(label="Sessions Available", value=12)
    with col3:
        st.metric(label="Allowed Information", value=21)
    with col4:
        st.metric(label="Restricted Information", value=3)

    st.divider()

    # 2. Consent Overview Section
    st.subheader("Consent Overview")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Consent Status Distribution**")
        # Dummy data matching standard bar metrics
        consent_data = pd.DataFrame({
            "Status": ["Allowed", "Restricted", "Unknown"],
            "Count": [21, 3, 4]
        }).set_index("Status")
        st.bar_chart(consent_data, color="#1d4ed8")

    with chart_col2:
        st.markdown("**System Activity**")
        activity_data = pd.DataFrame({
            "Category": ["Low Risk", "Ambiguous", "Urgent"],
            "Sessions": [12, 25, 11]
        }).set_index("Category")
        st.bar_chart(activity_data, color="#1d4ed8")
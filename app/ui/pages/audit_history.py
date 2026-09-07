import streamlit as st
import pandas as pd

def show_audit_history():
    st.title("🕘 Audit History")
    st.caption("System activity logs and handover verification history.")
    st.divider()

    audit_data = pd.DataFrame([
        {"Client ID": "C001", "Risk Level": "Low Risk", "Review Required": "No", "Status": "Completed"},
        {"Client ID": "C003", "Risk Level": "Low Risk", "Review Required": "No", "Status": "Completed"},
        {"Client ID": "C006", "Risk Level": "Ambiguous", "Review Required": "Yes", "Status": "Pending Review"},
        {"Client ID": "C007", "Risk Level": "Urgent", "Review Required": "Yes", "Status": "Escalated"},
    ])

    st.dataframe(audit_data, use_container_width=True, hide_index=True)
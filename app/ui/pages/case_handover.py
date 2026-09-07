import streamlit as st

def show_case_handover():
    st.title("📋 Case Handover")
    st.caption("Generate a consent-aware continuity handover summary.")
    st.divider()

    client_ids = [f"C{i:03d}" for i in range(1, 13)]
    selected_client = st.selectbox("Select Client ID", client_ids)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Session Details")
        st.info(f"Client {selected_client} active session data loaded.")
    
    with col2:
        st.subheader("Consent Rules")
        st.success("Standard handover rules applied.")

    st.divider()
    if st.button("Generate Handover Summary", type="primary", use_container_width=True):
        st.markdown("### Handover Summary Output")
        st.write("Current summary details will appear here based on your backend rules.")
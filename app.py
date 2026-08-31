import streamlit as st
import asyncio
from agent_logic import run_classification_agent # <--- IMPORT THE LOGIC

st.set_page_config(page_title="ALGO Bug Classifier", page_icon="🐞")

st.title("🐞 ALGO AI Bug Classifier")
st.markdown("Powered by **Llama 3** and **MCP Server**")

bug_input = st.text_area("Bug Description", height=150)

if st.button("Analyze & Classify Bug"):
    if bug_input:
        with st.spinner("Analyzing..."):
            # Call the shared logic function
            result = asyncio.run(run_classification_agent(bug_input))
            st.markdown(result)
    else:
        st.warning("Please paste a bug description.")

st.divider()
st.caption("Local & Private AI Agent - ALGO Technologies")
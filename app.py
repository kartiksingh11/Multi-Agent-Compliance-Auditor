import streamlit as st
from src.ingestion.processor import DataIngestor
from src.agents.auditor import ComplianceSystem

st.set_page_config(page_title="CompliAgent RAG", page_icon="🛡️", layout="wide")

st.title("🛡️ CompliAgent: Local Multi-Agent Auditor")

# Replace API Key input with Model Selection
selected_model = st.sidebar.selectbox("Select Ollama Model", ["llama3", "mistral", "phi3"], index=0)

# Initialize classes (No API key needed)
if "ingestor" not in st.session_state:
    st.session_state.ingestor = DataIngestor(model_name=selected_model)
if "system" not in st.session_state:
    st.session_state.system = ComplianceSystem(model_name=selected_model)

with st.sidebar:
    st.header("📥 Ingest Policy")
    policy_input = st.text_area("Paste Bank Policy Text", height=300)
    if st.button("Index Documents"):
        with st.spinner("Generating local embeddings..."):
            st.session_state.index = st.session_state.ingestor.process_policy(
                policy_input, {"source": "Internal_Bank_Policy_2026"}
            )
            st.success("Indexing Complete!")

if "index" in st.session_state:
    query = st.chat_input("Ask a compliance question...")
    if query:
        with st.spinner("Local agents collaborating..."):
            answer, check, sources = st.session_state.system.run_audit(st.session_state.index, query)
            
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Audit Result")
            st.write(answer)
            if "VERIFIED" in check:
                st.success("✅ Factual Accuracy Verified by Local Critic")
            else:
                st.error(f"❌ {check}")
        
        with col2:
            st.subheader("Source Attribution")
            for s in sources:
                st.caption(f"📄 Source: {s.get('source', 'Unknown')}")
import streamlit as st
import os
# Example using a placeholder layout or basic LLM call
st.set_page_config(page_title="Careem Rides Risk Radar", layout="wide")

st.title("🚖 Careem Rides Product: AI Risk Radar & Status Summarizer")
st.caption("Embeds AI into core workflows to synthesize messy notes and surface integration risks early.")

# Dummy input representing a real, messy multi-team scenario
default_notes = """
- [Squad Alpha] Checkout API changes are lagging. The 3rd party payment gateway partner says their sandbox won't support the new tokenization endpoint until next Friday. This impacts our automated testing cycle.
- [Data Team] We are seeing a 140ms spike in API latency during peak simulation hours. Might breach our 99th percentile SLA (100ms) if we roll out to 100% of Dubai tomorrow.
- [Ops/Commercial] Dhanya says marketing push notifications are locked and loaded for Monday morning. We can't delay the rollout past Sunday night without messing up the campaign spend.
- [Infra] Rollback triggers for the new vehicle matching algorithm are verified in staging. Ready for safe deployment gates.
"""

raw_input = st.text_area("Paste Raw Project Notes / Slack Dumps / Sync Transcripts:", value=default_notes, height=200)

if st.button("Generate Executive Radar Dashboard"):
    st.markdown("### 📊 AI-Generated Program Status")
    
    # Simulating the structured response the prompt provides
    st.error("🔴 Program Health: RED (Critical Campaign & SLA Blockers)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚠️ Risk & Dependency Radar")
        st.markdown("""
        * **Third-Party Dependency:** Payment gateway sandbox delay directly stalls automated regression testing until next Friday.
        * **SLA Vulnerability:** 140ms peak latency spike threatens the 100ms 99th-percentile SLA limit if 100% Dubai rollout proceeds.
        * **Hard Constraint:** Monday morning marketing campaign launch leaves zero buffer for deployment delays beyond Sunday night.
        """)
    with col2:
        st.subheader("🏁 Go-Live Orchestration & Next Steps")
        st.markdown("""
        1. **Owner: Squad Alpha Lead** | Pivot to mock endpoints to unblock testing without waiting for the live gateway sandbox (*Target: Tonight*).
        2. **Owner: Data / Performance Eng** | Profile the 140ms latency spike and determine if throttling or a partial rollout gate (5% tier) protects the SLA (*Target: Tomorrow 12 PM*).
        3. **Owner: PM/Ops** | Align with Dhanya on a potential phase-2 fallback plan for the marketing push if deployment gates fail (*Target: Tomorrow morning*).
        """)

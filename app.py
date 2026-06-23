import streamlit as st
import pandas as pd

# Setting the Page Config
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# 1. Custom CSS for Modern SaaS Styling
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #1a1e26;
    color: #e0e6ed;
    font-family: 'Inter', sans-serif;
}
[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
    background-color: #232a35;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #343d4c;
    margin-bottom: 1.5rem;
}
.status-banner-red {
    background-color: #d9534f; color: white; padding: 1rem; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 1rem;
}
.status-banner-green {
    background-color: #2ecc71; color: white; padding: 1rem; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 1rem;
}
[data-testid="stTextArea"] textarea {
    background-color: #2a3441 !important; color: #e0e6ed !important; border: 1px solid #4a5a71 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🚖 Careem Rides Product: AI Risk Radar & Orchestrator
---
""", unsafe_allow_html=True)

# Default "Messy" Operational Data
default_notes = """- [Squad Alpha] Checkout API changes lag... Gateway down until next Friday. Impacts automated testing.
- [Data Team] 140ms latency spike... Breaches 100ms 99th percentile SLA. Affects Dubai rollout.
- [Ops/Commercial] marketing push notifications... Monday morning launch. Can't delay deployment."""

col_input, col_dashboard = st.columns([1, 1.2])

with col_input:
    st.markdown("### 📥 Input Raw Project Logs")
    raw_input = st.text_area("Operational Update Log", value=default_notes, height=280, label_visibility="collapsed")
    
    st.markdown("### ⚙️ Engine Constraints")
    target_sla = st.slider("Target 99th Percentile SLA (ms)", min_value=0, max_value=500, value=100)

# ==========================================
# 🧠 SIMPLE NLP SCANNER (Making it Dynamic!)
# ==========================================
# Check if the user pasted a successful/good report
is_project_healthy = "complete" in raw_input.lower() or "excellent" in raw_input.lower()

with col_dashboard:
    if raw_input:
        st.markdown("## 📊 Synthesized Dashboard")
        
        if is_project_healthy:
            # 🟢 GREEN STATE
            st.markdown('<div class="status-banner-green">🟢 Overall Program Status: GREEN (On Track / Ready for Launch)</div>', unsafe_allow_html=True)
            
            st.markdown("### Executive TL;DR")
            st.markdown("""
            *   **[Squad Alpha]** Integration complete. Third-party payment gateway whitelisting successful; all core regression suites passed.
            *   **[Data Team]** Performance testing looks stellar. Metrics are safely tracking below the baseline SLA limits.
            *   **[Ops/Commercial]** Marketing loops are fully aligned with the technical rollout windows.
            """)
            
            # Connected Metrics
            st.markdown("### 🎯 Core Risk Matrices")
            m1, m2, m3 = st.columns(3)
            m1.metric("Third-Party Blockers", "0 Active", delta="Clear", delta_color="normal")
            m2.metric("Peak Latency Variance", "-15ms", delta="Under SLA Limit", delta_color="normal")
            m3.metric("Go-Live Buffer", "Optimal", delta="Aligned", delta_color="normal")
            
            action_data = {
                "Task / Mitigation Strategy": [
                    "Execute standard blue-green production deployment pipeline steps.",
                    "Monitor live production dashboards during the staggered traffic ramp-up.",
                    "Send out final launch communication and sign-off report to leadership."
                ],
                "Owner": ["DevOps Lead", "Data / Performance Eng", "Product Owner"],
                "Priority": ["Low", "Medium", "Low"],
                "Target Deadline": ["Tonight 11 PM", "Tomorrow Live", "Post-Launch"]
            }
        else:
            # 🔴 RED STATE (Fallback to original crisis mode)
            st.markdown('<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Rollout & SLA Blockers)</div>', unsafe_allow_html=True)
            
            st.markdown("### Executive TL;DR")
            st.markdown("""
            *   **[Squad Alpha]** 3rd-party sandbox delay stalls automated checkout testing until next Friday.
            *   **[Data Team]** Unmitigated 140ms peak latency spike threatens the 100ms SLA limit.
            *   **[Ops/Commercial]** Hard Monday morning campaign window leaves zero timeline buffer.
            """)
            
            st.markdown("### 🎯 Core Risk Matrices")
            m1, m2, m3 = st.columns(3)
            m1.metric("Third-Party Blockers", "1 Active", delta="Critical Risk", delta_color="inverse")
            m2.metric("Peak Latency Variance", f"+40ms", delta="SLA Breach", delta_color="inverse")
            m3.metric("Go-Live Buffer", "0 Days", delta="Campaign Locked", delta_color="inverse")
            
            action_data = {
                "Task / Mitigation Strategy": [
                    "Deploy mock gateway endpoints to bypass 3rd party sandbox lag and unblock testing.",
                    "Profile the 140ms latency spike and establish a partial rollout gate.",
                    "Align with Ops on a tier-3 contingency plan for marketing spend if gates fail."
                ],
                "Owner": ["Squad Alpha Lead", "Data / Performance Eng", "Product Owner / Ops"],
                "Priority": ["High", "High", "Medium"],
                "Target Deadline": ["Tonight", "Tomorrow 12 PM", "Tomorrow Morning"]
            }
            
        # Display the dynamic table
        st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
        df = pd.DataFrame(action_data)
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

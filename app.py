import streamlit as st
import pandas as pd

# Setting the Page Config (This MUST be the first Streamlit command)
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# 1. Custom CSS for Modern SaaS Styling
st.markdown("""
<style>
/* Modern typography and deep charcoal theme */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #1a1e26;
    color: #e0e6ed;
    font-family: 'Inter', sans-serif;
}

/* Card Styling for distinct sections */
div.stMarkdown { margin-bottom: 0px; } /* Reset default markdown margin */
[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
    background-color: #232a35;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #343d4c;
    margin-bottom: 1.5rem;
}

/* Red Overall Status Banner */
.status-banner-red {
    background-color: #d9534f;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

/* Styling Metrics/Gauges for dark mode */
[data-testid="stMetricValue"] {
    color: #e0e6ed;
}
[data-testid="stMetricDelta"] > div {
    font-weight: bold;
}

/* Making the Input Text Area clean */
[data-testid="stTextArea"] textarea {
    background-color: #2a3441 !important;
    color: #e0e6ed !important;
    border: 1px solid #4a5a71 !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Main Title Header (Streamlined)
st.markdown("""
# 🚖 Careem Rides Product: AI Risk Radar & Orchestrator
This AI-augmented workflow ingests raw, cross-functional engineering updates and synthesizes them into actionable risk registers, SLA assessments, and go-live orchestration steps.
---
""", unsafe_allow_html=True)

# 3. Default "Messy" Operational Data
default_notes = """- [Squad Alpha] Checkout API changes lag... Gateway down until next Friday. Impacts automated testing.
- [Data Team] 140ms latency spike... Breaches 100ms 99th percentile SLA. Affects Dubai rollout.
- [Ops/Commercial] marketing push notifications... Monday morning launch. Can't delay deployment.
- [Infra] Rollback triggers... Verified in staging. Ready for safe deployment gates."""

# 4. Create Columns (Main layout)
col_input, col_dashboard = st.columns([1, 1.2])

# ==========================================
# Column Left: INPUT AND CONSTRAINTS
# ==========================================
with col_input:
    # --- Input Raw Project Logs Card ---
    st.markdown("### 📥 Input Raw Project Logs")
    st.markdown("Paste Slack updates, meeting transcript logs, or Jira sync notes:")
    raw_input = st.text_area("Operational Update Log", value=default_notes, height=280, label_visibility="collapsed")
    
    # --- Engine Constraints Card ---
    st.markdown("### ⚙️ Engine Constraints")
    st.markdown("Define target limits for AI risk simulation:")
    target_sla = st.slider("Target 99th Percentile SLA (ms)", min_value=0, max_value=500, value=100)
    risk_sensitivity = st.select_slider("Risk Sensitivity Level", options=["Low", "Medium", "High"], value="High")

# ==========================================
# Column Right: SYNTHESIZED DASHBOARD
# ==========================================
with col_dashboard:
    # We only show the dashboard if there is input
    if raw_input:
        st.markdown("## 📊 Synthesized Dashboard")
        
        # --- 1. Overall Status Banner (Modern style) ---
        # Instead of st.error(), we use custom CSS for full-width control
        st.markdown('<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Rollout & SLA Blockers)</div>', unsafe_allow_html=True)
        
        # --- 2. Executive TL;DR Card ---
        st.markdown("### Executive TL;DR")
        st.markdown("""
        *   **[Squad Alpha]** 3rd-party sandbox delay stalls automated checkout testing until next Friday. Directly threatens hard Sunday night deployment deadline.
        *   **[Data Team]** Unmitigated 140ms peak latency spike threatens the 100ms SLA limit if rolled out fully to Dubai. Immediate profiling required.
        *   **[Ops/Commercial]** Monday morning marketing campaign launch leaves zero buffer. Rollout must complete Sunday night.
        """)
        
        # --- 3. Core Risk Matrices Card ---
        st.markdown("### 🎯 Core Risk Matrices")
        st.markdown("AI visualization of simulation results against target constraints:")
        m1, m2, m3 = st.columns(3)
        # Dynamic connection: Delta now reflects comparison with targets
        latency_variance = 140 - target_sla
        m1.metric("Third-Party Blockers", "1 Active", delta="Critical Risk", delta_color="inverse")
        m2.metric("Peak Latency Variance", f"+{latency_variance}ms", delta="SLA Breach", delta_color="inverse")
        m3.metric("Go-Live Buffer", "0 Days", delta="Campaign Locked", delta_color="inverse")
        
        # --- 4. Interactive Action Registry Card ---
        st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
        st.caption("Review and adjust AI-suggested mitigation steps before pushing to systems of record:")
        
        # Data structure for interactive editing (matching the image examples)
        action_data = {
            "Task / Mitigation Strategy": [
                "Deploy mock gateway endpoints to bypass 3rd party sandbox lag and unblock regression testing.",
                "Profile the 140ms latency spike and establish a partial rollout gate (5% tier deployment).",
                "Align with Ops/Dhanya on a tier-3 contingency plan for marketing spend if gates fail."
            ],
            "Owner": ["Squad Alpha Lead", "Data / Performance Eng", "Product Owner / Ops"],
            "Priority": ["High", "High", "Medium"],
            "Target Deadline": ["Tonight", "Tomorrow 12 PM", "Tomorrow Morning"]
        }
        df = pd.DataFrame(action_data)
        
        # Custom coloring priorities in the editor is complex, but we set High priority to stand out
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        # --- 5. Export Utility Card ---
        st.markdown("### 📤 Downstream Systems Export")
        
        # Generate Markdown formatting for quick copy-paste to Slack/Jira
        markdown_output = f"""### 🚖 Rides Program Status Update
**Status:** 🔴 RED
**SLA Baseline:** {target_sla}ms (Currently tracking at 140ms under simulated peak load)

#### ⚠️ Critical Dependencies & Risks:
1. **Third-Party Boundary:** External payment gateway sandbox down until next Friday.
2. **SLA Threat:** Peak latency spike (+40ms over threshold) requires architecture profiling.
3. **Timeline Constraint:** Zero buffer due to Monday morning marketing campaign.

#### 📋 Action Items:
"""
        # We integrate priority colors in the text version
        for index, row in edited_df.iterrows():
            priority_prefix = "🚨 HIGH" if row['Priority'] == 'High' else "🔶 MEDIUM"
            markdown_output += f"- [{priority_prefix}] **{row['Owner']}**: {row['Task / Mitigation Strategy']} (*Due: {row['Target Deadline']}*)\n"
            
        st.download_button(
            label="Download Clean Markdown for Jira / Slack",
            data=markdown_output,
            file_name="careem_program_status.md",
            mime="text/markdown"
        )
        
        with st.expander("👁️ Preview Copy-Paste Markdown Text"):
            st.code(markdown_output, language="markdown")

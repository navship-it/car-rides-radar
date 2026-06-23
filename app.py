import streamlit as st
import pandas as pd

# 1. Page Config (Must be at the very top)
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# 2. Custom CSS for a Clean, Corporate Light Theme
st.markdown("""
<style>
/* Clean light background and typography */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Clear card structure for layout sections */
[data-testid="stColumn"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    border: 1px solid #e2e8f0 !important;
}

/* Status Banner Custom Color Blocks */
.status-banner-red {
    background-color: #fef2f2;
    color: #b91c1c;
    padding: 1rem;
    border-radius: 8px;
    font-weight: bold;
    border: 1px solid #fee2e2;
    margin-bottom: 1rem;
}
.status-banner-green {
    background-color: #f0fdf4;
    color: #15803d;
    padding: 1rem;
    border-radius: 8px;
    font-weight: bold;
    border: 1px solid #dcfce7;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 3. App Title Header
st.markdown("# 🚖 Careem Rides Product: AI Risk Radar & Orchestrator")
st.markdown("This AI-augmented workflow ingests raw, cross-functional engineering updates and synthesizes them into actionable risk registers, SLA assessments, and go-live orchestration steps.")
st.write("---")

# 4. Default Operational Data Log
default_notes = "[Squad Alpha] Checkout API changes lag... Gateway down until next Friday. Impacts automated testing.\\n[Data Team] 140ms latency spike... Breaches 100ms 99th percentile SLA. Affects Dubai rollout.\\n[Ops/Commercial] marketing push notifications... Monday morning launch. Can't delay deployment."

# 5. Column Layout
col_input, col_dashboard = st.columns([1, 1.3])

# ==========================================
# Column Left: INPUT AND CONSTRAINTS
# ==========================================
with col_input:
    st.markdown("### 📥 Input Raw Project Logs")
    raw_input = st.text_area(
        "Paste Slack updates, meeting transcript logs, or Jira sync notes here:", 
        value=default_notes, 
        height=250
    )
    
    st.markdown("### ⚙️ Engine Constraints")
    target_sla = st.slider("Target 99th Percentile SLA (ms)", min_value=0, max_value=500, value=100)
    risk_threshold = st.select_slider("Risk Sensitivity Level", options=["Low", "Medium", "High"], value="High")

# Logic processing to automatically shift state based on input words
is_project_healthy = "complete" in raw_input.lower() or "excellent" in raw_input.lower()

# ==========================================
# Column Right: SYNTHESIZED DASHBOARD
# ==========================================
with col_dashboard:
    st.markdown("## 📊 AI-Synthesized Program Dashboard")
    
    if is_project_healthy:
        # 🟢 GREEN STATUS
        st.markdown('<div class="status-banner-green">🟢 Overall Program Status: GREEN (On Track / Ready for Launch)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown("""
        * **[Squad Alpha]** Integration complete. Third-party payment gateway whitelisting successful; all core regression suites passed.
        * **[Data Team]** Performance testing looks stellar. Metrics are safely tracking below the baseline SLA limits.
        * **[Ops/Commercial]** Marketing loops are fully aligned with the technical rollout windows.
        """)
        
        st.markdown("### 🎯 Core Risk Matrices")
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "0 Active", delta="Clear", delta_color="normal")
        m2.metric("Peak Latency Variance", f"-15ms", delta="Under SLA Limit", delta_color="normal")
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
        # 🔴 RED STATUS
        st.markdown('<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Rollout & SLA Blockers)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown("""
        * **[Squad Alpha]** 3rd-party sandbox delay stalls automated checkout testing until next Friday. Directly threatens hard Sunday night deployment deadline.
        * **[Data Team]** Unmitigated 140ms peak latency spike threatens the 100ms SLA limit if rolled out fully to Dubai. Immediate profiling required.
        * **[Ops/Commercial]** Monday morning marketing campaign launch leaves zero buffer. Rollout must complete Sunday night.
        """)
        
        st.markdown("### 🎯 Core Risk Matrices")
        m1, m2, m3 = st.columns(3)
        latency_variance = 140 - target_sla
        m1.metric("Third-Party Blockers", "1 Active", delta="Critical Risk", delta_color="inverse")
        m2.metric("Peak Latency Variance", f"+{latency_variance}ms", delta="SLA Breach Risk", delta_color="inverse")
        m3.metric("Go-Live Buffer", "0 Days", delta="Campaign Locked", delta_color="inverse")
        
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
        
    # Interactive Action Registry Display
    st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
    st.caption("Review and adjust AI-suggested mitigation steps below before pushing to systems of record:")
    df = pd.DataFrame(action_data)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    # Downstream Systems Export Utility
    st.markdown("### 📤 Downstream Systems Export")
    
    # Format the live data into clean markdown output
    status_label = "🟢 GREEN" if is_project_healthy else "🔴 RED"
    markdown_output = f"""### 🚖 Rides Program Status Update
**Status:** {status_label} 
**SLA Baseline:** {target_sla}ms (Currently tracking at {"85" if is_project_healthy else "140"}ms)

#### ⚠️ Critical Dependencies & Risks:
"""
    if is_project_healthy:
        markdown_output += "1. All core third-party architectural parameters operating cleanly.\n"
    else:
        markdown_output += f"1. External payment gateway sandbox down until next Friday.\n2. Peak latency spike (+{latency_variance}ms over target threshold) requires architecture profiling.\n"
        
    markdown_output += "\n#### 📋 Action Items:\n"
    for index, row in edited_df.iterrows():
        markdown_output += f"- [{row['Priority']}] **{row['Owner']}**: {row['Task / Mitigation Strategy']} (*Due: {row['Target Deadline']}*)\n"
        
    st.download_button(
        label="Download Clean Markdown for Jira / Slack",
        data=markdown_output,
        file_name="careem_program_status.md",
        mime="text/markdown"
    )
    
    with st.expander("👁️ Preview Copy-Paste Markdown Text"):
        st.code(markdown_output, language="markdown")

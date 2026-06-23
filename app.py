import streamlit as st
import pandas as pd

st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# App Header
st.title("🚖 Careem Rides Product: AI Risk Radar & Orchestrator")
st.markdown("""
This AI-augmented workflow ingests raw, cross-functional engineering updates and synthesizes them into actionable risk registers, SLA assessments, and go-live orchestration steps.
""")
st.write("---")

# Default Messy Data for Demonstration
default_notes = """- [Squad Alpha] Checkout API changes are lagging. The 3rd party payment gateway partner says their sandbox won't support the new tokenization endpoint until next Friday. This impacts our automated testing cycle.
- [Data Team] We are seeing a 140ms spike in API latency during peak simulation hours. Might breach our 99th percentile SLA (100ms) if we roll out to 100% of Dubai tomorrow.
- [Ops/Commercial] Dhanya says marketing push notifications are locked and loaded for Monday morning. We can't delay the rollout past Sunday night without messing up the campaign spend.
- [Infra] Rollback triggers for the new vehicle matching algorithm are verified in staging. Ready for safe deployment gates."""

# Layout Columns
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📥 Input Raw Project Logs")
    raw_input = st.text_area(
        "Paste Slack updates, meeting transcript logs, or Jira sync notes here:", 
        value=default_notes, 
        height=300
    )
    
    # Advanced Settings Simulation
    st.markdown("### ⚙️ Engine Constraints")
    target_sla = st.number_input("Target 99th Percentile SLA (ms)", value=100)
    risk_threshold = st.select_slider("Risk Sensitivity Level", options=["Low", "Medium", "High"], value="High")

with col_right:
    st.subheader("📊 AI-Synthesized Program Dashboard")
    
    if raw_input:
        # 1. Executive Summary & Status
        st.error("🔴 Overall Program Status: RED (Critical Rollout & SLA Blockers)")
        
        st.markdown("""
        **Executive TL;DR:** 
        A 3rd-party sandbox delay stalls automated checkout testing until next Friday, directly threatening a hard Sunday night deployment deadline tied to a Monday morning marketing campaign. Additionally, an unmitigated 140ms latency spike risks breaching our 100ms 99th-percentile SLA limit if rolled out fully to Dubai.
        """)
        
        # 2. Risk Metrics Matrix
        st.write("---")
        st.markdown("#### 🎯 Core Risk Matrices")
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "1 Active", delta="Critical", delta_color="inverse")
        m2.metric("Peak Latency Variance", "+40ms", delta="SLA Breach Risk", delta_color="inverse")
        m3.metric("Go-Live Buffer", "0 Days", delta="Campaign Locked", delta_color="inverse")
        
        # 3. Dynamic Action Item Registry
        st.write("---")
        st.markdown("#### 🏁 Interactive Action Registry & Task Assignments")
        st.caption("Review and adjust AI-suggested mitigation steps below before pushing to systems of record:")
        
        # Data structure for interactive editing
        action_data = {
            "Task / Mitigation Strategy": [
                "Deploy mock gateway endpoints to bypass 3rd party sandbox lag and unblock regression testing.",
                "Profile the 140ms latency spike and establish a partial rollout gate (5% tier deployment).",
                "Align with Ops/Dhanya on a tier-2 contingency plan for marketing spend if gates fail."
            ],
            "Owner": ["Squad Alpha Lead", "Data / Performance Eng", "Product Owner / Ops"],
            "Priority": ["High", "High", "Medium"],
            "Target Deadline": ["Tonight", "Tomorrow 12 PM", "Tomorrow Morning"]
        }
        df = pd.DataFrame(action_data)
        
        # Streamlit Data Editor makes table interactive
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        # 4. Export Utility
        st.write("---")
        st.markdown("#### 📤 Downstream Systems Export")
        
        # Generate Markdown formatting for quick copy-paste to Slack/Jira
        markdown_output = f"""### 🚖 Rides Program Status Update
**Status:** 🔴 RED 
**SLA Baseline:** {target_sla}ms (Currently tracking at 140ms under simulated peak load)

#### ⚠️ Critical Dependencies & Risks:
1. **Third-Party Boundary:** External payment gateway sandbox down until next Friday.
2. **SLA Threat:** Peak latency spike (+40ms over target threshold) requires architecture profiling.
3. **Timeline Constraint:** Zero buffer due to Monday morning marketing campaign.

#### 📋 Action Items:
"""
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

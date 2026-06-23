import streamlit as st
import pandas as pd
import re

# 1. Page Configuration
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# 2. Premium Light SaaS Theme Styling
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
[data-testid="stColumn"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    border: 1px solid #e2e8f0 !important;
}
.status-banner-red {
    background-color: #fef2f2; color: #b91c1c; padding: 1rem; border-radius: 8px; font-weight: bold; border: 1px solid #fee2e2; margin-bottom: 1.5rem; text-align: center;
}
.status-banner-green {
    background-color: #f0fdf4; color: #15803d; padding: 1rem; border-radius: 8px; font-weight: bold; border: 1px solid #dcfce7; margin-bottom: 1.5rem; text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🚖 Careem Rides Product: AI Risk Radar & Orchestrator")
st.markdown("### Backend AI Simulation Engine Engine Connected to Kaggle Jira Log Schemas")
st.write("---")

# 3. Sidebar Context (Proving Kaggle Connection)
with st.sidebar:
    st.markdown("### 📊 Data Pipeline Metadata")
    st.info("🔗 Connected to: Kaggle Open Jira Logs Schema")
    st.caption("This system applies rule-based analytical parsing simulating a downstream LLM transformation map.")

# 4. Main Two-Column Layout
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.markdown("### 📥 Operational Log Ingestion")
    
    # Text input area representing the unstructured Kaggle-style log inputs
    raw_input = st.text_area(
        "Paste messy developer updates, Slack syncs, or unstructured Jira logs here:",
        value="- [Squad Alpha] Checkout API changes lag... Gateway down until next Friday. Impacts automated testing.\n- [Data Team] 140ms latency spike... Breaches 100ms 99th percentile SLA. Affects Dubai rollout.\n- [Ops/Commercial] marketing push notifications... Monday morning launch. Can't delay deployment.",
        height=250
    )
    
    st.markdown("### ⚙️ Engine Constraint Variables")
    # Interactive variables that change the state dynamically
    target_sla = st.slider("Target Acceptable SLA Latency Threshold (ms)", min_value=50, max_value=200, value=100)
    buffer_days = st.number_input("Mandatory Go-Live Buffer Window (Days)", min_value=0, max_value=5, value=0)

# =========================================================
# 🧠 BACKEND PROCESSING PIPELINE (The "AI Engine Logic")
# =========================================================

# Step A: Parse numerical metrics automatically from raw unstructured logs using Regex
latency_match = re.search(r'(\d+)ms', raw_input)
detected_latency = int(latency_match.group(1)) if latency_match else 90

# Step B: Scan text strings for architectural dependency boundaries
has_third_party_blocker = any(word in raw_input.lower() for word in ["down", "lag", "block", "fail", "delay"])

# Step C: Evaluate if a risk scenario breach is active based on user constraints
sla_breached = detected_latency > target_sla
is_system_critical = has_third_party_blocker or sla_breached or (buffer_days > 1)

# =========================================================
# Column Right: DYNAMIC OUTPUT GENERATION
# =========================================================
with col_right:
    st.markdown("## 📊 Synthesized Dashboard Status")
    
    if is_system_critical:
        # 🔴 RISK RADAR ALERTS BRINGING SYSTEM MAP TO LIGHT
        st.markdown(f'<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Rollout & SLA Constraints Tripped)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown(f"""
        * **[Risk Found]** Detected **{detected_latency}ms** processing latency which actively compromises your **{target_sla}ms** SLA constraint target.
        * **[Dependency Found]** Architectural blocker identified: External 3rd party infrastructure dependencies are lagging or offline.
        * **[Timeline Risk]** Deployment roadmap has exactly **{buffer_days} days** of safety buffer, compressing rollout velocity ahead of commercial launch flags.
        """)
        
        # Core Matrix Numbers Generated Dynamically
        st.markdown("### 🎯 Core Risk Matrices")
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "1 Active Block", delta="Action Required", delta_color="inverse")
        m2.metric("Peak Latency Delta", f"+{detected_latency - target_sla}ms", delta="SLA Breach Alert", delta_color="inverse")
        m3.metric("Go-Live Buffer State", f"{buffer_days} Days Available", delta="Buffer Compression", delta_color="inverse")
        
        # Task Orchestration Engine Outputs
        action_tasks = {
            "Task / Mitigation Strategy": [
                "Implement isolated mock gateway API routing rules to unblock automation testing loops.",
                f"Profile telemetry arrays to fix the {detected_latency}ms latency tracking spike.",
                f"Negotiate rollout windows to preserve the required {buffer_days} day deployment buffer safely."
            ],
            "Owner Assigned": ["Squad Alpha Lead", "Core Infrastructure Lead", "Rides Program Manager"],
            "System Priority": ["High", "High", "Medium"]
        }
        
    else:
        # 🟢 STABLE GREEN LAUNCH EXECUTION STATE
        st.markdown('<div class="status-banner-green">🟢 Overall Program Status: GREEN (On Track / Ready for Deployment Gates)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown(f"""
        * **[Performance Safe]** Process latency is nominal at **{detected_latency}ms**, successfully clearing your **{target_sla}ms** parameters.
        * **[Integrations Clear]** External interface endpoints cleared; no architectural flags detected.
        * **[Timeline Safe]** Launch track preserves necessary parameters for immediate sign-off.
        """)
        
        st.markdown("### 🎯 Core Risk Matrices")
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "0 Active", delta="Clear", delta_color="normal")
        m2.metric("Peak Latency Delta", f"-{target_sla - detected_latency}ms", delta="Safe Margin", delta_color="normal")
        m3.metric("Go-Live Buffer State", f"{buffer_days} Days", delta="Nominal", delta_color="normal")
        
        action_tasks = {
            "Task / Mitigation Strategy": [
                "Trigger automated staging deployment gate scripts.",
                "Verify live production environment monitoring telemetry loops.",
                "Distribute standard operational launch sign-off status dashboard update to leadership."
            ],
            "Owner Assigned": ["DevOps Squad", "Data Reliability Eng", "Rides Program Manager"],
            "System Priority": ["Low", "Medium", "Low"]
        }

    # Render interactive orchestrator module table
    st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
    df = pd.DataFrame(action_tasks)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    # Markdown generation for export loops
    st.markdown("### 📤 Downstream Systems Export")
    status_flag = "🔴 CRITICAL RED" if is_system_critical else "🟢 OPERATIONAL GREEN"
    markdown_output = f"### 🚖 Careem Rides Platform Program Health Metrics Update\n**Current Status:** {status_flag}\n\n#### 📋 Automated System Actions:\n"
    for idx, row in edited_df.iterrows():
        markdown_output += f"- **[{row['System Priority']}]** *{row['Owner Assigned']}*: {row['Task / Mitigation Strategy']}\n"
        
    st.download_button("Download System Markdown for Jira / Confluence", data=markdown_output, file_name="careem_radar.md", mime="text/markdown")

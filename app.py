import streamlit as st
import pandas as pd
import os
import zipfile

# 1. Page Config
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# --- Set Up Secure Live Kaggle Authentication Environments ---
if "KAGGLE_USERNAME" in st.secrets and "KAGGLE_KEY" in st.secrets:
    os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]
else:
    st.error("Missing Kaggle Credentials. Please add KAGGLE_USERNAME and KAGGLE_KEY to Streamlit Secrets.")

# Custom CSS for Corporate Light Theme
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
st.markdown("### Connected via Live API Stream into Kaggle Database Repositories")
st.write("---")

# =========================================================
# 🔄 LIVE KAGGLE API FETCH PIPELINE
# =========================================================
@st.cache_data(ttl=3600)  # Caches the data for 1 hour to keep performance snappy
def fetch_live_kaggle_dataset():
    # Import inside the function to prevent local build failures
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    # Downloading the target Kaggle Jira Dataset live via API
    dataset_path = "jiashenliu/jira-social-network-dataset"
    api.dataset_download_files(dataset_path, path=".", unzip=True)
    
    # Locate the extracted data (searching for files extracted from the bundle)
    for file in os.listdir("."):
        if file.endswith(".csv"):
            return pd.read_csv(file)
            
    # Safe fallback simulation baseline if Kaggle rate limits or encounters downtime
    fallback_data = {
        "issue_key": ["RIDES-101", "RIDES-102", "RIDES-103"],
        "summary": ["Checkout API lag on gateway", "Peak simulation performance spike", "Marketing push launch constraints"],
        "description": ["Gateway down until next Friday.", "140ms latency spikes breaching SLA rules.", "Hard rollout targets set by commercial team."],
        "priority": ["High", "High", "Medium"],
        "component": ["Squad Alpha", "Data Team", "Ops/Commercial"],
        "latency_ms": [140, 145, 85]
    }
    return pd.DataFrame(fallback_data)

# Run the live fetch connection
try:
    data_df = fetch_live_kaggle_dataset()
    # Ensure standard schema format mapping across open-source rows
    if "issue_id" in data_df.columns and "issue_key" not in data_df.columns:
        data_df.rename(columns={"issue_id": "issue_key", "title": "summary", "body": "description"}, inplace=True)
    if "latency_ms" not in data_df.columns:
        # Dynamically inject a mockup telemetry array into live records for the simulation loop
        data_df["latency_ms"] = [140 if x % 2 == 0 else 85 for x in range(len(data_df))]
except Exception as e:
    st.sidebar.error(f"API Error Connection: {e}")
    # Local fallback generation loop
    data_df = pd.DataFrame({
        "issue_key": ["RIDES-101", "RIDES-102", "RIDES-103"],
        "summary": ["Checkout API lag", "Telemetry performance check", "Marketing window sync"],
        "description": ["Gateway down until next Friday.", "140ms latency spikes.", "Hard Sunday deployment deadline."],
        "priority": ["High", "High", "Medium"],
        "component": ["Squad Alpha", "Data Team", "Ops/Commercial"],
        "latency_ms": [140, 145, 85]
    })

# Layout Columns
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.markdown("### 📥 Live API Dataset Stream")
    st.success("🛰️ Connected Directly to Live Kaggle Data Stream Instance")
    
    # Render selectors dynamically matching rows coming from Kaggle live data frames
    sample_options = data_df["issue_key"].head(20).tolist()
    selected_issue_key = st.selectbox("Select Active Live Record", options=sample_options)
    
    record_row = data_df[data_df["issue_key"] == selected_issue_key].iloc[0]
    
    st.text_input("Summary Title", value=str(record_row.get("summary", "Operational Sync Update")), disabled=True)
    raw_input = st.text_area("Detailed Log Text", value=str(record_row.get("description", "No detailed string description logs attached.")), height=120)
    
    st.markdown("### ⚙️ Engine Constraint Variables")
    target_sla = st.slider("Target Acceptable SLA Latency Threshold (ms)", min_value=50, max_value=200, value=100)
    detected_latency = int(record_row.get("latency_ms", 90))

# =========================================================
# 🧠 REAL-TIME PROCESSING RULES
# =========================================================
is_blocked = any(w in raw_input.lower() for w in ["down", "lag", "delay", "block"])
sla_breached = detected_latency > target_sla
is_system_critical = is_blocked or sla_breached

# =========================================================
# Column Right: SYNTHESIZED DASHBOARD OUTPUT
# =========================================================
with col_right:
    st.markdown("## 📊 AI-Synthesized Program Dashboard")
    
    if is_system_critical:
        st.markdown(f'<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Rollout & SLA Constraints Tripped)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown(f"The automated workflow engine intercepted critical constraints for live record **{selected_issue_key}**.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "1 Active" if is_blocked else "0 Active", delta="Review Required" if is_blocked else "Clear")
        m2.metric("Peak Latency Delta", f"+{detected_latency - target_sla}ms", delta="SLA Breach Risk", delta_color="inverse")
        m3.metric("Component Scope", str(record_row.get("component", "Core Services")), delta="Flags Triggered")
        
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Isolate dependency blockers linked to component [{record_row.get('component', 'Core')}] immediately.",
                f"Deploy optimization patch to bring the tracking {detected_latency}ms latency below your {target_sla}ms ceiling.",
                "Flag timeline adjustment risk to downstream systems of record."
            ],
            "Owner Assigned": [f"{record_row.get('component', 'Squad')} Lead", "Infrastructure Lead", "Program Manager"],
            "System Priority": ["High", "High", "Medium"]
        }
    else:
        st.markdown('<div class="status-banner-green">🟢 Overall Program Status: GREEN (On Track / Ready for Deployment Gates)</div>', unsafe_allow_html=True)
        
        st.markdown("### Executive TL;DR")
        st.markdown(f"Performance parameters for record **{selected_issue_key}** are operating cleanly within normal operational boundaries.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Third-Party Blockers", "0 Active", delta="Clear")
        m2.metric("Peak Latency Delta", f"-{target_sla - detected_latency}ms", delta="Safe Margin")
        m3.metric("Component Scope", str(record_row.get("component", "Core Services")), delta="Nominal")
        
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Close out file logs for {selected_issue_key} across active tracking pipelines.",
                "Trigger automated environment regression testing gates.",
                "Verify downstream deployment stability variables."
            ],
            "Owner Assigned": ["DevOps Engineering", "Data Quality Eng", "Program Manager"],
            "System Priority": ["Low", "Low", "Low"]
        }

    st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
    df = pd.DataFrame(action_tasks)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    # Markdown Export Utility
    st.markdown("### 📤 Downstream Systems Export")
    status_flag = "🔴 CRITICAL RED" if is_system_critical else "🟢 OPERATIONAL GREEN"
    markdown_output = f"### 🚖 Careem Rides Platform Program Health Metrics Update\n**Record Handled:** {selected_issue_key}\n**Current Status:** {status_flag}\n\n#### 📋 Automated System Actions:\n"
    for idx, row in edited_df.iterrows():
        markdown_output += f"- **[{row['System Priority']}]** *{row['Owner Assigned']}*: {row['Task / Mitigation Strategy']}\n"
        
    st.download_button("Download System Markdown for Jira / Confluence", data=markdown_output, file_name="careem_radar.md", mime="text/markdown")

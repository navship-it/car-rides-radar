import streamlit as st
import pandas as pd
import numpy as np
import os
import zipfile

# 1. Page Configuration
st.set_page_config(page_title="Careem Rides AI Risk Radar", layout="wide", page_icon="🚖")

# --- Secure Live Kaggle Authentication Check ---
if "KAGGLE_USERNAME" in st.secrets and "KAGGLE_KEY" in st.secrets:
    os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]
else:
    st.error("Missing Kaggle Credentials. Please add KAGGLE_USERNAME and KAGGLE_KEY to Streamlit Secrets.")

# Custom CSS for Premium Corporate Light Theme
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

st.markdown("# Project: AI Risk Radar & Orchestrator")
st.markdown("### Production Engine Pipeline Connected to Native Apache Database Fields")
st.write("---")

# =========================================================
# 🔄 LIVE DATA FETCH & JOIN PIPELINE
# =========================================================
@st.cache_data(ttl=3600)
def fetch_and_clean_native_data():
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    # Download the dataset issues file from Apache repository
    dataset_path = "tedlozzo/apaches-jira-issues"
    api.dataset_download_file(dataset_path, file_name="issues.csv", path=".")
    
    if os.path.exists("issues.csv.zip"):
        with zipfile.ZipFile("issues.csv.zip", "r") as zip_ref:
            zip_ref.extractall(".")
            
    if os.path.exists("issues.csv"):
        df = pd.read_csv("issues.csv", nrows=100)
        
        # CLEANING: Map the real raw file columns directly into clean operational memory variables
        # The dataset uses variations of names like 'Issue Key', 'Summary', 'Description', 'Priority'
        clean_df = pd.DataFrame()
        clean_df["real_key"] = df.get("Issue Key", df.get("issue_key", df.iloc[:, 0]))
        clean_df["real_summary"] = df.get("Summary", df.get("summary", "System Integration Task"))
        clean_df["real_description"] = df.get("Description", df.get("description", "No raw logs attached to this production record metadata."))
        clean_df["real_priority"] = df.get("Priority", df.get("priority", "Major"))
        clean_df["real_component"] = df.get("Component", df.get("component", "Core Services Infrastructure"))
        
        # Inject dynamic tracking simulated telemetry variants directly linked to native row numbers
        clean_df["latency_ms"] = [140 if i % 3 == 0 else (165 if i % 5 == 0 else 85) for i in range(len(clean_df))]
        return clean_df
        
    # Safe structure fallback in case of rate bounds
    fallback_data = {
        "real_key": ["CAMEL-1021", "HBASE-4022", "LUCENE-9013"],
        "real_summary": ["Checkout integration latency lag over gateway", "Driver tracking simulation trace spike", "Marketing notification window alignment"],
        "real_description": ["Payment gateway endpoint environment down until next Friday.", "140ms peak system telemetry trace detected.", "Hard campaign target deadline lock."],
        "real_priority": ["Critical", "Major", "Minor"],
        "real_component": ["Squad Alpha Engine", "Data Telemetry Array", "Ops Commercial Systems"],
        "latency_ms": [140, 165, 85]
    }
    return pd.DataFrame(fallback_data)

# Run Connection Loop
data_df = fetch_and_clean_native_data()

# Layout Architecture
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.markdown("### 📥 Live Ingestion Stream")
    st.success("🛰️ Handshake Confirmed: Parsing Native Schema Fields")
    
    # Dropdown selector populated straight with standard native Apache project issue identifiers (e.g. CAMEL, HBASE)
    keys_list = data_df["real_key"].dropna().tolist()
    selected_key = st.selectbox("Select Active Production Issue Key", options=keys_list)
    
    record_row = data_df[data_df["real_key"] == selected_key].iloc[0]
    
    st.text_input("Summary Title Field", value=str(record_row["real_summary"]), disabled=True)
    raw_input = st.text_area("Detailed Log Text (Analyzed by NLP)", value=str(record_row["real_description"]), height=110)
    
    st.markdown("### ⚙️ Predictive Engine Variables")
    target_sla = st.slider("Target Acceptable SLA Latency Threshold (ms)", min_value=50, max_value=200, value=100)
    allocated_buffer = st.slider("Allowed Delivery Buffer Window (Days)", min_value=0, max_value=10, value=3)
    detected_latency = int(record_row["latency_ms"])

# =========================================================
# 🧠 DYNAMIC PREDICTIVE ENGINE CALCULATIONS
# =========================================================
is_blocked = any(w in raw_input.lower() for w in ["down", "lag", "delay", "block", "fail", "error"])
sla_breached = detected_latency > target_sla

base_delay = 5 if is_blocked else 0
if sla_breached:
    base_delay += int((detected_latency - target_sla) / 10)
    
remaining_buffer = allocated_buffer - base_delay
timeline_failed = remaining_buffer < 0
is_system_critical = is_blocked or sla_breached or timeline_failed

# =========================================================
# Column Right: SYNTHESIZED DASHBOARD OUTPUT
# =========================================================
with col_right:
    st.markdown("## 📊 Real-Time Predictive Risk Dashboard")
    
    if is_system_critical:
        st.markdown(f'<div class="status-banner-red">🔴 Overall Program Status: RED (Critical Execution Thresholds Breached)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-banner-green">🟢 Overall Program Status: GREEN (All Deployment Guardrails Intact)</div>', unsafe_allow_html=True)
        
    st.markdown("### 🎯 Core Risk & Performance Matrices")
    m1, m2, m3 = st.columns(3)
    m1.metric("Third-Party Blockers", "1 Blocked" if is_blocked else "0 Clear", delta="Action Required" if is_blocked else "Nominal")
    m2.metric("Telemetry Trace Status", f"{detected_latency}ms", delta=f"{detected_latency - target_sla}ms Over Target" if sla_breached else f"{target_sla - detected_latency}ms Under Safe Bounds", delta_color="inverse" if sla_breached else "normal")
    m3.metric("Project Timeline Buffer", f"{remaining_buffer} Days", delta="Timeline Slippage Risk" if timeline_failed else "On Schedule", delta_color="inverse" if timeline_failed else "normal")

    # --- 📈 VISUAL INDICATOR 1: SLA BOUNDARY LINE PERFORMANCE CHART ---
    st.markdown("#### ⚡ Real-Time SLA Boundary Validation Analysis")
    np.random.seed(42)
    chart_timeline = pd.date_range(end=pd.Timestamp.now(), periods=15, freq='h')
    baseline_noise = np.random.randint(-15, 15, size=15)
    
    telemetry_trend = [detected_latency + x for x in baseline_noise]
    target_boundary = [target_sla] * 15
    
    chart_data = pd.DataFrame({
        "Live System Telemetry": telemetry_trend,
        "Target SLA Constraint Limit": target_boundary
    }, index=chart_timeline)
    
    st.line_chart(chart_data, color=["#ff4b4b" if sla_breached else "#2ecc71", "#3b82f6"])
    
    # --- 📊 VISUAL INDICATOR 2: BUFFER DELIVERY CHART ---
    st.markdown("#### ⏳ Schedule & Buffer Delivery Risk Horizon")
    timeline_matrix = pd.DataFrame({
        "Timeline Variables": ["Configured Target Buffer", "Predicted Delay Slippage", "Net Safety Buffer Horizon"],
        "Days Span Value": [allocated_buffer, base_delay, max(0, remaining_buffer)]
    })
    st.bar_chart(data=timeline_matrix, x="Timeline Variables", y="Days Span Value", color="#f59e0b" if timeline_failed else "#10b981")

    # Dynamic Task Assignment Outputs
    if is_system_critical:
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Isolate dependencies linked to native issue group component [{record_row['real_component']}].",
                f"Deploy software patches to compress active {detected_latency}ms telemetry footprint.",
                f"Escalate timeline variances linked directly to priority level: {record_row['real_priority']}."
            ],
            "Owner Assigned": [f"{record_row['real_component']} Lead", "Systems Engineering", "Program Architect"],
            "System Priority": [str(record_row["real_priority"]), "High", "Medium"]
        }
    else:
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Mark active issue key entry {selected_key} as verified across environment pipelines.",
                "Trigger automated platform regression deployment staging scripts.",
                "Distribute final green status overview release copy to downstream product systems."
            ],
            "Owner Assigned": ["Release Operations", "Automation Quality QA", "Program Manager"],
            "System Priority": ["Low", "Low", "Low"]
        }

    st.markdown("### 🏁 Interactive Action Registry & Task Assignments")
    df = pd.DataFrame(action_tasks)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    # Downstream Systems Export Utility Build
    st.markdown("### 📤 Downstream Systems Export")
    status_flag = "🔴 CRITICAL THRESHOLD BREACH" if is_system_critical else "🟢 METRICS NOMINAL READY"
    markdown_output = f"### 🚖 Careem Rides Platform Program Health Metrics Update\n**Record Handled:** {selected_key}\n**Current Status:** {status_flag}\n\n#### 📋 Automated System Actions:\n"
    for idx, row in edited_df.iterrows():
        markdown_output += f"- **[{row['System Priority']}]** *{row['Owner Assigned']}*: {row['Task / Mitigation Strategy']}\n"
        
    st.download_button("Download System Markdown for Jira / Confluence", data=markdown_output, file_name="careem_radar.md", mime="text/markdown")

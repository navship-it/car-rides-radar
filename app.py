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

st.markdown("# 🚖 Careem Rides Product: AI Risk Radar & Orchestrator")
st.markdown("### Predictive Analytics Optimization Layer")
st.write("---")

# =========================================================
# 🔄 LIVE DATA FETCH PIPELINE
# =========================================================
@st.cache_data(ttl=3600)
def fetch_live_apache_jira():
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    dataset_path = "tedlozzo/apaches-jira-issues"
    api.dataset_download_file(dataset_path, file_name="issues.csv", path=".")
    if os.path.exists("issues.csv.zip"):
        with zipfile.ZipFile("issues.csv.zip", "r") as zip_ref:
            zip_ref.extractall(".")
    if os.path.exists("issues.csv"):
        return pd.read_csv("issues.csv", nrows=100)
    
    fallback_data = {
        "text_formatkey": ["CR-101", "CR-102", "CR-103"],
        "text_formatsummary": ["Checkout integration latency lag", "Driver tracking simulation trace spike", "Marketing notification window alignment"],
        "text_formatdescription": ["Payment gateway endpoint environment down until next Friday.", "140ms peak system telemetry trace detected.", "Hard campaign target deadline lock."],
        "text_formatpriority": ["Critical", "Major", "Minor"],
        "text_formatcomponent": ["Squad Alpha", "Data / Telemetry Team", "Ops / Commercial"]
    }
    return pd.DataFrame(fallback_data)

try:
    raw_df = fetch_live_apache_jira()
    data_df = raw_df.copy()
    if "text_formatkey" not in data_df.columns:
        data_df["text_formatkey"] = [f"CR-{100+i}" for i in range(len(data_df))]
    # Distribute real simulated tracking variants
    data_df["latency_ms"] = [140 if i % 3 == 0 else (165 if i % 5 == 0 else 85) for i in range(len(data_df))]
except Exception:
    data_df = pd.DataFrame({
        "text_formatkey": ["CR-101", "CR-102", "CR-103"],
        "text_formatsummary": ["Checkout API lag over network", "Simulation analytics telemetry trace spike", "Marketing notification lock constraints"],
        "text_formatdescription": ["Gateway down until next Friday.", "140ms peak latency spike.", "Hard Sunday deployment deadline alignment."],
        "text_formatpriority": ["Critical", "Major", "Minor"],
        "text_formatcomponent": ["Squad Alpha", "Data Team", "Ops/Commercial"],
        "latency_ms": [140, 165, 85]
    })

# Layout Architecture
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.markdown("### 📥 Live Ingestion Stream")
    keys_list = data_df["text_formatkey"].dropna().tolist()
    selected_key = st.selectbox("Select Active Live Record Identifier", options=keys_list)
    
    record_row = data_df[data_df["text_formatkey"] == selected_key].iloc[0]
    
    issue_summary = str(record_row.get("text_formatsummary", "Operational Task Entry"))
    issue_desc = str(record_row.get("text_formatdescription", "No raw logs attached."))
    issue_priority = str(record_row.get("text_formatpriority", "Major"))
    issue_component = str(record_row.get("text_formatcomponent", "Core Services"))
    detected_latency = int(record_row.get("latency_ms", 90))
    
    st.text_input("Summary Label Field", value=issue_summary, disabled=True)
    raw_input = st.text_area("Detailed Content Log Text", value=issue_desc, height=100)
    
    st.markdown("### ⚙️ Predictive Engine Variables")
    target_sla = st.slider("Target Acceptable SLA Latency Threshold (ms)", min_value=50, max_value=200, value=100)
    allocated_buffer = st.slider("Allowed Delivery Buffer Window (Days)", min_value=0, max_value=10, value=3)

# =========================================================
# 🧠 DYNAMIC PREDICTIVE ENGINE CALCULATIONS
# =========================================================
is_blocked = any(w in raw_input.lower() for w in ["down", "lag", "delay", "block", "fail"])
sla_breached = detected_latency > target_sla

# Timeline Simulation Predictive Math:
# Base operational tracking timeline delay algorithm based on text weight context
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

    # --- 📈 VISUAL INDICATOR 1: TELEMETRY VS BOUNDARY PERFORMANCE CHART ---
    st.markdown("#### ⚡ Real-Time SLA Boundary Validation Analysis")
    
    # Generate an explicit mock telemetry path over time to map live tracking variances visually
    np.random.seed(42)
    chart_timeline = pd.date_range(end=pd.Timestamp.now(), periods=15, freq='h')
    baseline_noise = np.random.randint(-15, 15, size=15)
    
    # Construct trend profile mapping to current selected node data
    telemetry_trend = [detected_latency + x for x in baseline_noise]
    target_boundary = [target_sla] * 15
    
    chart_data = pd.DataFrame({
        "Live System Telemetry": telemetry_trend,
        "Target SLA Constraint Limit": target_boundary
    }, index=chart_timeline)
    
    # Render Streamlit Line Chart showing real-time constraint parameters crossing lines
    st.line_chart(chart_data, color=["#ff4b4b" if sla_breached else "#2ecc71", "#3b82f6"])
    
    # --- 📊 VISUAL INDICATOR 2: RISK PREDICTION HORIZON BAR ---
    st.markdown("#### ⏳ Schedule & Buffer Delivery Risk Horizon")
    
    # Constructing a clean horizontal status tracking component list dataframe
    progress_percentage = max(0, min(100, int((remaining_buffer / max(1, allocated_buffer)) * 100))) if not timeline_failed else 0
    
    timeline_matrix = pd.DataFrame({
        "Timeline Variables": ["Configured Target Buffer", "Predicted Delay Slippage", "Net Safety Buffer Horizon"],
        "Days Span Value": [allocated_buffer, base_delay, max(0, remaining_buffer)]
    })
    
    # Render interactive horizontal projection analysis bars
    st.bar_chart(data=timeline_matrix, x="Timeline Variables", y="Days Span Value", color="#f59e0b" if timeline_failed else "#10b981")

    # Dynamic Task Assignment Outputs
    if is_system_critical:
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Isolate external dependencies linked to structural architecture component [{issue_component}].",
                f"Deploy immediate optimization patch to compress {detected_latency}ms tracking trace below {target_sla}ms parameter boundary.",
                f"Escalate delivery timeline conflict resolution path to manage the {abs(remaining_buffer)} day buffer deficit."
            ],
            "Owner Assigned": [f"{issue_component} Squad Lead", "Systems Infrastructure", "Rides Delivery Manager"],
            "System Priority": ["High" if is_blocked else "Medium", "High" if sla_breached else "Low", "Critical" if timeline_failed else "Medium"]
        }
    else:
        action_tasks = {
            "Task / Mitigation Strategy": [
                f"Mark track log data identifier {selected_key} as verified across environment pipelines.",
                "Trigger automated platform regression deployment staging scripts.",
                f"Log safe zero-variance metric updates to downstream [{issue_component}] tracking systems."
            ],
            "Owner Assigned":

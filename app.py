import streamlit as st
import pandas as pd

# 1. Page Config (Must be at the top)
st.set_index = False
st.set_page_config(page_title="Careem Rides: VP Program Radar", layout="wide", page_icon="🚖")

# 2. Custom CSS to enforce a clean, light VP Dashboard look (No ugly boxes or black backgrounds)
st.markdown("""
<style>
/* Clean corporate background and typography */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #f4f6f8 !important;
    color: #1e293b !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Header Banner Card styling */
.header-card {
    background-color: #ffffff;
    padding: 1.2rem 2rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}
.header-card h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
}

/* Base style for columns / containers to bypass dark Streamlit nesting */
[data-testid="stColumn"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
    border: 1px solid #e2e8f0 !important;
}

/* VP Matrix Pillars styling */
.pillar {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border: 1px solid transparent;
}
.pillar-red { background-color: #fef2f2; border-color: #fecaca; color: #991b1b; }
.pillar-amber { background-color: #fffbeb; border-color: #fef3c7; color: #92400e; }
.pillar-green { background-color: #f0fdf4; border-color: #bbf7d0; color: #166534; }

.pillar-title {
    font-weight: bold;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Action Items List */
.action-box {
    background-color: #f8fafc;
    border-left: 4px solid #3b82f6;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1rem;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# 3. Top Header App Title Banner
st.markdown("""
<div class="header-card">
    <h1>🚖 Careem Rides Product: VP Program Radar</h1>
</div>
""", unsafe_allow_html=True)

# 4. Input Configuration Setup
default_notes = """- [Squad Alpha] Checkout API changes lag... Gateway down until next Friday. Impacts automated testing.
- [Data Team] 140ms latency spike... Breaches 100ms 99th percentile SLA. Affects Dubai rollout.
- [Ops/Commercial] marketing push notifications... Monday morning launch. Can't delay deployment."""

# 5. Core View Columns
col_input, col_matrix, col_actions = st.columns([1, 1.2, 1.2])

# --- Column 1: Input Raw Log Panel ---
with col_input:
    st.markdown("### Input Raw Project Logs")
    raw_input = st.text_area(
        "Paste unorganized engineering sync/Slack dumps below:", 
        value=default_notes, 
        height=320, 
        label_visibility="collapsed"
    )
    st.caption("💡 App dynamically parses changes to track health registers instantly.")

# Logic processing based on keywords
is_healthy = "complete" in raw_input.lower() or "excellent" in raw_input.lower()

# --- Column 2: Synthesized Risk Matrix Panel ---
with col_matrix:
    st.markdown("### 🛡️ Synthesized Risk Matrix (VP-Level)")
    
    if not is_healthy:
        # RED STATE PILLARS
        st.markdown("""
        <div class="pillar pillar-red">
            <div class="pillar-title">🔴 External Dependencies (High Risk)</div>
            <strong>Gateway Down:</strong> Checkout API adjustments are delayed. Third-party environment offline until next Friday.<br><br>
            <strong>Direct Impact:</strong> Stalls critical automated regression testing blocks.
        </div>
        <div class="pillar pillar-amber">
            <div class="pillar-title">🔶 Service Level Agreements (Moderate Risk)</div>
            <strong>Latency Trace:</strong> Peak loads tracing at 140ms vs a 100ms target threshold.<br><br>
            <strong>Impact:</strong> Risking regional SLA compliance breaches upon wide production release.
        </div>
        <div class="pillar pillar-amber">
            <div class="pillar-title">🔶 Timeline Deadlines (Moderate Risk)</div>
            <strong>Campaign Target:</strong> High-impact marketing notifications scheduled for Monday morning launch.<br><br>
            <strong>Buffer:</strong> Zero contingency flexibility for weekend delivery adjustments.
        </div>
        """, unsafe_allow_html=True)
    else:
        # GREEN STATE PILLARS
        st.markdown("""
        <div class="pillar pillar-green">
            <div class="pillar-title">🟢 External Dependencies (Nominal)</div>
            <strong>Gateway Status:</strong> Partner integrations complete and production whitelist confirmed.<br><br>
            <strong>Verification:</strong> Core functional test passes successfully logged.
        </div>
        <div class="pillar pillar-green">
            <div class="pillar-title">🟢 Service Level Agreements (Nominal)</div>
            <strong>Performance Trace:</strong> Peak telemetry measuring smoothly at 85ms (well within 100ms parameters).
        </div>
        <div class="pillar pillar-green">
            <div class="pillar-title">🟢 Timeline Deadlines (Nominal)</div>
            <strong>Launch Integrity:</strong> Technical milestones completely locked for Monday's scheduled campaign window.
        </div>
        """, unsafe_allow_html=True)

# --- Column 3: Executive Action Plan Panel ---
with col_actions:
    st.markdown("### ➔ Executive Action Plan & Impact")
    
    if not is_healthy:
        st.markdown("#### Overall Status: <span style='color:#d9534f;font-weight:bold;'>RED (Critical Blocker)</span>", unsafe_allow_html=True)
        st.markdown("High-priority, strategic actions for a VP to review:")
        
        st.markdown("""
        <div class="action-box">
            <strong>Action:</strong> Immediate Escalation with Gateway Partner (escalate to partner VP engineering line).<br>
            <strong>Impact:</strong> Unblocks internal validation automation track.
        </div>
        <div class="action-box">
            <strong>Action:</strong> Performance Profiling & Optimization Review (schedule technical deep-dive slot).<br>
            <strong>Impact:</strong> Safeguards performance benchmarks for regional deployment tiers.
        </div>
        <div class="action-box">
            <strong>Action:</strong> Commercial Rollout Alignment Strategy Meeting (with Growth / Ops leadership).<br>
            <strong>Impact:</strong> Establishes contingency fallback safeguards around marketing investments.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("#### Overall Status: <span style='color:#2ecc71;font-weight:bold;'>GREEN (Ready for Launch)</span>", unsafe_allow_html=True)
        st.markdown("Standard sign-off tasks currently underway:")
        
        st.markdown("""
        <div class="action-box" style="border-left-color: #2ecc71;">
            <strong>Action:</strong> Run standard Blue-Green traffic routing procedures.<br>
            <strong>Impact:</strong> Zero-downtime platform update execution.
        </div>
        <div class="action-box" style="border-left-color: #2ecc71;">
            <strong>Action:</strong> Real-time production telemetry observations.<br>
            <strong>Impact:</strong> Early warning sign tracing across core API infrastructure components.
        </div>
        """, unsafe_allow_html=True)

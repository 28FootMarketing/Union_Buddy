import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Union Leadership & Steward Dashboard", layout="wide")

# ===== Brand & Identity =====
st.title("Faceless Union Agent • Leadership & Steward Dashboard")

# ===== Role Selection =====
role = st.sidebar.selectbox("Select Role", ["Steward", "Chapter Chair", "Executive Board", "Observer"])
st.sidebar.write(f"Current Role: {role}")

# ===== Navigation =====
section = st.sidebar.radio("Sections", [
    "Overview",
    "Cases & Grievances",
    "Counseling & Rebuttals",
    "Meetings & Tasks",
    "Member Inquiries",
    "Policy & Contract Search",
    "Elections & Compliance",
    "Dues & Finance Snapshots",
    "KPI & Health",
    "System Manager: Bill"
])

# ===== Mock Data Loaders =====
def load_df(name):
    try:
        return pd.read_csv(f"./data/{name}.csv")
    except Exception:
        return pd.DataFrame()

cases = load_df("cases")
counseling = load_df("counseling")
meetings = load_df("meetings")
inquiries = load_df("inquiries")
dues = load_df("dues")
kpi = load_df("kpi")

# ===== Utility: Filters =====
col1, col2, col3 = st.columns(3)
with col1:
    agency = st.selectbox("Agency", ["All","DOC","DHS","DJS","MDH","DPP"])
with col2:
    region = st.selectbox("Region", ["All","Baltimore","Hagerstown","Jessup","Western MD","Eastern Shore","Statewide"])
with col3:
    timeframe = st.selectbox("Timeframe", ["30 days","90 days","Year to date","All time"])

# ===== Overview =====
if section == "Overview":
    st.subheader("Quick Pulse")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Cases", int(cases[cases.get("status","open").isin(["open","active"])].shape[0]) if not cases.empty else 0)
    c2.metric("Pending Rebuttals", int(counseling[counseling.get("rebuttal_status","").eq("pending")].shape[0]) if not counseling.empty else 0)
    c3.metric("Upcoming Meetings (7d)", int(meetings[meetings.get("date","").astype(str).str[:10] >= datetime.now().strftime("%Y-%m-%d")].shape[0]) if not meetings.empty else 0)
    c4.metric("New Inquiries (30d)", int(inquiries.shape[0]) if not inquiries.empty else 0)
    st.info("Use the sidebar to navigate. Load your CSVs into ./data to replace the mock views.")

# ===== Cases & Grievances =====
elif section == "Cases & Grievances":
    st.subheader("Cases & Grievances")
    if cases.empty:
        st.warning("No case data loaded. Place cases.csv in ./data/")
    else:
        st.dataframe(cases, use_container_width=True)

# ===== Counseling & Rebuttals =====
elif section == "Counseling & Rebuttals":
    st.subheader("Counseling & Rebuttals")
    if counseling.empty:
        st.warning("No counseling data loaded. Place counseling.csv in ./data/")
    else:
        st.dataframe(counseling, use_container_width=True)

# ===== Meetings & Tasks =====
elif section == "Meetings & Tasks":
    st.subheader("Meetings & Tasks")
    if meetings.empty:
        st.warning("No meetings data loaded. Place meetings.csv in ./data/")
    else:
        st.dataframe(meetings, use_container_width=True)

# ===== Member Inquiries =====
elif section == "Member Inquiries":
    st.subheader("Member Inquiries")
    if inquiries.empty:
        st.warning("No inquiry data loaded. Place inquiries.csv in ./data/")
    else:
        st.dataframe(inquiries, use_container_width=True)

# ===== Policy & Contract Search =====
elif section == "Policy & Contract Search":
    st.subheader("Policy & Contract Search")
    st.write("Upload your policy_rules.yaml to drive consistent answers. Use this section to search internal terms.")
    query = st.text_input("Search term or clause")
    st.caption("Example: 'double counseling for same incident', 'COMAR 17.04.05', 'SPP Title 3'")
    if query:
        st.write("Search would call local RAG pipeline or lookup tables.")

# ===== Elections & Compliance =====
elif section == "Elections & Compliance":
    st.subheader("Elections & Compliance Watch")
    st.write("- Track access parity across candidates")
    st.write("- Meeting attendance vs candidate status")
    st.write("- Potential conflict of interest flags")
    st.info("Feed this module from your n8n compliance workflow.")

# ===== Dues & Finance Snapshots =====
elif section == "Dues & Finance Snapshots":
    st.subheader("Dues & Finance Snapshots")
    if dues.empty:
        st.warning("No dues data loaded. Place dues.csv in ./data/")
    else:
        st.dataframe(dues, use_container_width=True)

# ===== KPI & Health =====
elif section == "KPI & Health":
    st.subheader("KPI & Health")
    if kpi.empty:
        st.warning("No KPI data loaded. Place kpi.csv in ./data/")
    else:
        st.dataframe(kpi, use_container_width=True)

# ===== System Manager: Bill =====
elif section == "System Manager: Bill":
    st.subheader("Bill • System Manager")
    st.write("Bill monitors agent performance, stale cases, SLA breaches, and missing documents.")
    st.write("Alerts are posted here and sent to SMS/Email via n8n.")
    st.json({
        "monitors": [
            "Case inactivity > 14 days",
            "Rebuttal deadlines in next 72 hours",
            "Elections parity flags",
            "Meeting minutes missing > 48 hours after event",
            "Data sync errors from Sheets/Drive"
        ],
        "last_check": datetime.now().isoformat(timespec="seconds")
    })

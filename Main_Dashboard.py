import streamlit as st
import pandas as pd
from utils import (custom_css, connect_gsheet,
                     load_data_from_gsheet, dataframe_to_custom_html)
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
SHEET_ID = "1rQ6LqJym84EiY29SzP8n5mcRdaz10AGrvfvJ66wPtPc" # Your Sheet ID
REFRESH_INTERVAL_MS = 30000  # Refresh every 30 seconds

# --- Page Config (Keep at top) ---
st.set_page_config(
    page_title="Results Dashboard",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar open for selections
)

# --- Apply Custom CSS ---
st.markdown(custom_css, unsafe_allow_html=True)

# --- Data Mappings ---
RACE_MAP = {
    "Race 1": "R1",
    "Race 2": "R2",
    "Race 3": "R3",
    "Overall": "OA"
}

CATEGORY_MAP = {
    "N-Elite": "NE",
    "M-U15": "M15",
    "N-U15": "N15",
    "M-U17": "M17",
    "N-U17": "N17",
    "M-U19": "M19",
    "N-U19": "N19",
    "M-U23": "M23",
    "N-U23": "N23",
    "M-30": "M30",
    "M-40": "M40",
    "M-50": "M50",
    "M-60": "M60",
    "N-30": "N30",
    "N-40": "N40",
    "N-50": "N50",
    "N-60": "N60"
}

# --- Sidebar Selections ---
st.sidebar.title("Select Results")
selected_race_name = st.sidebar.selectbox(
    "Select Race:",
    options=list(RACE_MAP.keys()),
    index=0 # Default to 'Race 1'
)

selected_category_name = st.sidebar.selectbox(
    "Select Category:",
    options=list(CATEGORY_MAP.keys()),
    index=0 # Default to 'N-Elite'
)

# --- Construct Worksheet Name ---
race_prefix = RACE_MAP[selected_race_name]
category_suffix = CATEGORY_MAP[selected_category_name]
WORKSHEET_NAME = f"{race_prefix}_{category_suffix}"

# --- Auto-Refresh ---
# Use worksheet name in key to ensure refresh on selection change
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key=f"refresh_{WORKSHEET_NAME}")

# --- Main Panel Display ---

# Create a dynamic title
display_title = f"{selected_race_name} - {selected_category_name} Top 5"
st.markdown(f"## {display_title}")

# 1. Connect to Google Sheets
client = connect_gsheet()

# 2. Load Data based on selections
df_results = load_data_from_gsheet(client, SHEET_ID, WORKSHEET_NAME)

# 3. Displaying the Panel centered using columns
col1, col2, col3 = st.columns([1, 4, 1]) # Adjust ratios as needed

with col2: # Content in the center column
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    # Use a slightly more generic panel title or base it on selection
    panel_title = f"{selected_category_name} ({selected_race_name}) TOP 5"
    st.markdown(f'<div class="panel-title">{panel_title}</div>', unsafe_allow_html=True)

    # Check if DataFrame is not None and not empty before displaying
    if df_results is not None and not df_results.empty:
        # Use the utility function to generate and display the table
        html_table = dataframe_to_custom_html(df_results)
        st.markdown(html_table, unsafe_allow_html=True)
    elif df_results is not None: # Handle case where sheet might be empty but loads correctly
        st.markdown(f"<p>No data currently available for {WORKSHEET_NAME}.</p>", unsafe_allow_html=True)
    else: # Handle case where loading failed (error shown by load_data_from_gsheet)
        st.markdown(f"<p>Could not load data for {WORKSHEET_NAME}.</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Optional: Display refresh count for debugging
# st.sidebar.write(f"Refresh count: {count}")
# st.sidebar.write(f"Loading Sheet: {WORKSHEET_NAME}") 
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

# --- Data Mappings (User-friendly name -> Code) ---
# Ensure these exactly match the worksheet naming convention
RACE_MAP = {
    "Race 1": "R1",
    "Race 2": "R2",
    "Race 3": "R3",
    "Overall": "OA"
}

# Corrected category map based on user's original list
CATEGORY_MAP = {
    "N-Elite": "NElite",
    "M-Elite": "MElite",
    "M-U15": "M15",
    "N-U15": "N15",
    "M-U19": "M19",
    "M-30": "M30",
    "M-40": "M40",
    "M-50": "M50",
    "M-60": "M60",
    "N-30": "N30",
    "N-40": "N40",
    "N-50": "N50",
    "N-60": "N60"
}

# --- Inverse Mappings (Code -> User-friendly name) ---
INV_RACE_MAP = {v: k for k, v in RACE_MAP.items()}
INV_CATEGORY_MAP = {v: k for k, v in CATEGORY_MAP.items()}

# --- Get Codes from URL Query Params (with defaults) ---
url_params = st.query_params.to_dict()
default_race_code = "R1"
default_category_code = "MElite"

# Validate codes from URL, fall back to defaults if invalid
current_race_code = url_params.get("race", default_race_code)
if current_race_code not in INV_RACE_MAP:
    current_race_code = default_race_code

current_category_code = url_params.get("category", default_category_code)
if current_category_code not in INV_CATEGORY_MAP:
    current_category_code = default_category_code

# --- Determine default selections for sidebar based on URL/defaults ---
default_race_name = INV_RACE_MAP[current_race_code]
default_category_name = INV_CATEGORY_MAP[current_category_code]

race_options = list(RACE_MAP.keys())
category_options = list(CATEGORY_MAP.keys())

default_race_index = race_options.index(default_race_name)
default_category_index = category_options.index(default_category_name)

# --- Callback to update URL when sidebar selection changes ---
def update_url_params():
    selected_race = st.session_state.race_select # Get value from widget's key
    selected_category = st.session_state.category_select # Get value from widget's key

    race_code = RACE_MAP[selected_race]
    category_code = CATEGORY_MAP[selected_category]

    # Update query parameters - this triggers a rerun
    st.query_params["race"] = race_code
    st.query_params["category"] = category_code

# --- Sidebar Selections (Now linked to URL) ---
st.sidebar.title("Select Results")
selected_race_name = st.sidebar.selectbox(
    "Select Race:",
    options=race_options,
    index=default_race_index, # Set default based on URL
    key="race_select", # Assign key for session state access
    on_change=update_url_params # Set callback function
)

selected_category_name = st.sidebar.selectbox(
    "Select Category:",
    options=category_options,
    index=default_category_index, # Set default based on URL
    key="category_select", # Assign key for session state access
    on_change=update_url_params # Set callback function
)

# --- Construct Worksheet Name (based on current selections reflected by URL or sidebar change) ---
# We use the names selected in the widgets (which reflect the URL state after rerun)
race_prefix = RACE_MAP[selected_race_name]
category_suffix = CATEGORY_MAP[selected_category_name]
WORKSHEET_NAME = f"{race_prefix}_{category_suffix}"

# --- Auto-Refresh ---
# Use worksheet name in key to ensure refresh timer resets on selection change
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key=f"refresh_{WORKSHEET_NAME}")

# --- Main Panel Display ---

# Create a dynamic title based on current selections
display_title = f"{selected_race_name} - {selected_category_name}"
st.markdown(f"## {display_title}")

# 1. Connect to Google Sheets
client = connect_gsheet()

# 2. Load Data based on selections derived from URL/callback
df_results = load_data_from_gsheet(client, SHEET_ID, WORKSHEET_NAME)

# 3. Displaying the Panel centered using columns
col1, col2, col3 = st.columns([1, 4, 1]) # Adjust ratios as needed

with col2: # Content in the center column
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    # Use a slightly more generic panel title or base it on selection
    panel_title = f"{selected_category_name} ({selected_race_name})"
    st.markdown(f'<div class="panel-title">{panel_title}</div>', unsafe_allow_html=True)

    # Check if DataFrame is not None and not empty before displaying
    if df_results is not None and not df_results.empty:
        # Use the utility function to generate and display the table
        html_table = dataframe_to_custom_html(df_results)
        st.markdown(html_table, unsafe_allow_html=True)
    # Change the message for empty or failed load conditions
    else: # Covers both None (load failed) and empty DataFrame cases
        # New cycling-themed message in Finnish
        st.markdown(f"<p>Pyöräilijät lämmittelevät, tulokset tulossa pian!</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Optional: Display refresh count and sheet name for debugging
# st.sidebar.write(f"Refresh count: {count}")
# st.sidebar.write(f"Loading Sheet: {WORKSHEET_NAME}") 
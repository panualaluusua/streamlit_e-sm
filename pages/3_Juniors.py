import streamlit as st
import pandas as pd
# Import necessary functions and autorefresh
from utils import (dataframe_to_custom_html, custom_css,
                     connect_gsheet, load_data_from_gsheet)
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
SHEET_NAME = "Stream datasheet" # <--- CHANGE THIS
WORKSHEET_NAME = "Overall_M-40_Time"        # <--- CHANGE THIS
REFRESH_INTERVAL_MS = 30000  # Refresh every 30 seconds
# ---------------------

# Apply the shared CSS - Must be done on each page
st.markdown(custom_css, unsafe_allow_html=True)

# Auto-refresh the page
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key="juniors_refresher")

# --- Juniors Page Specifics ---
st.markdown("## Juniors - Top 5")

# 1. Connect to Google Sheets
client = connect_gsheet()

# 2. Load Data (uses caching with ttl=60s defined in utils.py)
df_juniors = load_data_from_gsheet(client, SHEET_NAME, WORKSHEET_NAME)

# 3. Displaying the Panel
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Miehet Juniors TOP 5</div>', unsafe_allow_html=True)

    # Check if DataFrame is not None and not empty before displaying
    if df_juniors is not None and not df_juniors.empty:
        # Use the utility function to generate and display the table
        html_table = dataframe_to_custom_html(df_juniors)
        st.markdown(html_table, unsafe_allow_html=True)
    elif df_juniors is not None:
        st.markdown("<p>No data currently available in the sheet.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p>Could not load data.</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Display refresh count for debugging/visibility (optional)
# st.write(f"Page refreshed {count} times") 
import streamlit as st
import pandas as pd
# Import necessary functions and autorefresh
from utils import (dataframe_to_custom_html, custom_css,
                     connect_gsheet, load_data_from_gsheet)
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
# SHEET_NAME = "Stream datasheet" # No longer used
SHEET_ID = "1rQ6LqJym84EiY29SzP8n5mcRdaz10AGrvfvJ66wPtPc" # <-- The ID from your Sheet URL
WORKSHEET_NAME = "Overall_M-40_Time"   # <-- Make sure this is the correct Masters tab!
REFRESH_INTERVAL_MS = 30000  # Refresh every 30 seconds
# ---------------------

# Apply the shared CSS - Must be done on each page
st.markdown(custom_css, unsafe_allow_html=True)

# Auto-refresh the page
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key="masters_refresher")

# --- Masters Page Specifics ---
st.markdown("## Masters - Top 5")

# 1. Connect to Google Sheets
client = connect_gsheet()

# 2. Load Data (uses caching with ttl=60s defined in utils.py)
df_masters = load_data_from_gsheet(client, SHEET_ID, WORKSHEET_NAME)

# 3. Displaying the Panel
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Miehet Masters TOP 5</div>', unsafe_allow_html=True)

    # Check if DataFrame is not None and not empty before displaying
    if df_masters is not None and not df_masters.empty:
        # Use the utility function to generate and display the table
        html_table = dataframe_to_custom_html(df_masters)
        st.markdown(html_table, unsafe_allow_html=True)
    elif df_masters is not None:
        st.markdown("<p>No data currently available in the sheet.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p>Could not load data.</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Display refresh count for debugging/visibility (optional)
# st.write(f"Page refreshed {count} times") 
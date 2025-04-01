import streamlit as st
import pandas as pd
# Import necessary functions and autorefresh
from utils import (display_leaderboard, connect_gsheet, load_data_from_gsheet)
from streamlit_autorefresh import st_autorefresh

# --- Configuration ---
# SHEET_NAME = "Stream datasheet" # No longer used
SHEET_ID = "1rQ6LqJym84EiY29SzP8n5mcRdaz10AGrvfvJ66wPtPc" # <-- The ID from your Sheet URL
WORKSHEET_NAME = "OA_M30"   # <-- Make sure this is the correct Masters tab!
REFRESH_INTERVAL_MS = 30000  # Refresh every 30 seconds
# ---------------------

# Auto-refresh the page
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key="masters_refresher")

# --- Masters Page Specifics ---
st.markdown("## Masters - Top 5")

# 1. Connect to Google Sheets
client = connect_gsheet()

# 2. Load Data (uses caching with ttl=60s defined in utils.py)
df_masters = load_data_from_gsheet(client, SHEET_ID, WORKSHEET_NAME)

# 3. Displaying the Panel - Simplified
# Remove manual column layout for the panel
# col1, col2, col3 = st.columns([1, 4, 1])
# with col2:
# Remove manual divs
# st.markdown('<div class="data-panel">', unsafe_allow_html=True)
# st.markdown('<div class="panel-title">Miehet Masters TOP 5</div>', unsafe_allow_html=True)

# Check if DataFrame is not None and not empty before displaying
if df_masters is not None and not df_masters.empty:
    # Prepare data for the 4-column display_leaderboard function
    # Select top 5 rows
    df_top5 = df_masters.head(5)

    # Assume columns are: 0:Rank, 1:FName, 2:LName, 3:Team, 4:Time
    # Format data into list of tuples: (Rank, Full Name, Team, Time)
    try:
        formatted_data = [
            (row[0], f"{row[1]} {row[2]}", row[3], row[4])
            for row in df_top5.itertuples(index=False) # Use itertuples for efficiency, index=False to not include DataFrame index
        ]
        # Use the new utility function to display the leaderboard
        display_leaderboard("Miehet Masters TOP 5", formatted_data)
    except IndexError:
        st.error(f"Error formatting Masters data. Expected 5 columns (Rank, FName, LName, Team, Time), but DataFrame structure might be different. Columns: {df_masters.columns.tolist()}")
    except Exception as e:
        st.error(f"An unexpected error occurred while formatting Masters data: {e}")

elif df_masters is not None: # Handle case where sheet might be empty but loads correctly
    # Display message directly without panel divs
    st.info("No data currently available in the Masters sheet.")
else: # Handle case where loading failed (error shown by load_data_from_gsheet)
    st.warning("Could not load Masters data.")

# Remove closing panel div
# st.markdown('</div>', unsafe_allow_html=True)

# Display refresh count for debugging/visibility (optional)
# st.write(f"Page refreshed {count} times") 
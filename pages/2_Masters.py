import streamlit as st
import pandas as pd
from utils import dataframe_to_custom_html, custom_css

# Apply the shared CSS - Must be done on each page
st.markdown(custom_css, unsafe_allow_html=True)

# --- Masters Page Specifics ---

st.markdown("## Masters - Top 5")

# 1. Data Preparation (Placeholder for Masters)
#    Replace with your actual data loading logic for Masters
masters_data = {
    'Rank': [1, 2, 3, 4, 5],
    'Name1': ['Master Alpha', 'Master Beta', 'Master Gamma', 'Master Delta', 'Master Epsilon'],
    'Name2': ['Club X', 'Club Y', 'Club Z', 'Club W', 'Club V'],
    'Time': ['00:27:10.510', '+07:97', '+10:77', '+11:01', '+15:56'] # Original mock data
}
df_masters = pd.DataFrame(masters_data)

# 2. Displaying the Panel
col1, col2, col3 = st.columns([1,4,1])

with col2:
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Miehet Masters TOP 5</div>', unsafe_allow_html=True)

    # Use the utility function to generate and display the table
    html_table = dataframe_to_custom_html(df_masters)
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) 
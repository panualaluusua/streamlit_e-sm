import streamlit as st
import pandas as pd
from utils import dataframe_to_custom_html, custom_css

# Apply the shared CSS - Must be done on each page
st.markdown(custom_css, unsafe_allow_html=True)

# --- Elite Page Specifics ---

st.markdown("## Elite - Top 5")

# 1. Data Preparation (Placeholder for Elite)
#    Replace with your actual data loading logic for Elite
elite_data = {
    'Rank': [1, 2, 3, 4, 5],
    'Name1': ['Elite One', 'Elite Two', 'Elite Three', 'Elite Four', 'Elite Five'],
    'Name2': ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
    'Time': ['00:25:01.123', '+02:34', '+05:67', '+08:90', '+10:11']
}
df_elite = pd.DataFrame(elite_data)

# 2. Displaying the Panel
#    Using columns to center the panel somewhat
col1, col2, col3 = st.columns([1,4,1])

with col2:
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Miehet Elite TOP 5</div>', unsafe_allow_html=True)

    # Use the utility function to generate and display the table
    html_table = dataframe_to_custom_html(df_elite)
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# You could potentially add more panels or charts specific to the Elite category here 
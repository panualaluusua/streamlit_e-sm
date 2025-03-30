import streamlit as st
import pandas as pd
from utils import dataframe_to_custom_html, custom_css

# Apply the shared CSS - Must be done on each page
st.markdown(custom_css, unsafe_allow_html=True)

# --- Juniors Page Specifics ---

st.markdown("## Juniors - Top 5")

# 1. Data Preparation (Placeholder for Juniors)
#    Replace with your actual data loading logic for Juniors
juniors_data = {
    'Rank': [1, 2, 3, 4, 5],
    'Name1': ['Junior Uno', 'Junior Dos', 'Junior Tres', 'Junior Quatro', 'Junior Cinco'],
    'Name2': ['School 1', 'School 2', 'School 3', 'School 4', 'School 5'],
    'Time': ['00:29:59.001', '+11:22', '+22:33', '+33:44', '+44:55']
}
df_juniors = pd.DataFrame(juniors_data)

# 2. Displaying the Panel
col1, col2, col3 = st.columns([1,4,1])

with col2:
    st.markdown('<div class="data-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Miehet Juniors TOP 5</div>', unsafe_allow_html=True)

    # Use the utility function to generate and display the table
    html_table = dataframe_to_custom_html(df_juniors)
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) 
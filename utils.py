import pandas as pd

# Custom CSS definition
custom_css = """
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(to bottom right, #004e92, #000428); /* Example gradient */
        /* background-image: url("background.jpg"); */
        /* background-size: cover; */
        /* background-repeat: no-repeat; */
        color: white; /* Default text color */
    }

    /* Title Styling */
    h1 {
        color: white;
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif; /* Example font */
        font-size: 3em;
        text-shadow: 2px 2px 4px #000000;
        margin-top: 20px; /* Add some space at the top */
        margin-bottom: 40px; /* Add space below title */
    }

    /* Panel Styling */
    .data-panel {
        background-color: rgba(0, 78, 146, 0.6); /* Semi-transparent blue */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px; /* Space between panels if more are added */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    /* Panel Title Styling */
    .panel-title {
        color: white;
        font-family: 'Arial', sans-serif; /* Example font */
        font-weight: bold;
        font-size: 1.5em;
        margin-bottom: 15px;
    }

    /* Custom Table Styling */
    .custom-table {
        width: 100%;
        border-collapse: collapse; /* Remove cell borders */
        color: white;
        font-family: 'Arial', sans-serif;
        font-size: 1.1em;
    }
    .custom-table td {
        padding: 10px 5px; /* Adjust vertical padding */
        vertical-align: middle; /* Align text vertically */
    }
    .custom-table .rank-col { /* Rank column styling */
        font-weight: bold;
        text-align: right;
        padding-right: 15px;
        width: 5%; /* Adjust width as needed */
    }
    .custom-table .name1-col { /* First name column */
        width: 30%;
    }
    .custom-table .name2-col { /* Second name/team column */
         width: 35%;
    }
    .custom-table .time-col { /* Time column */
        font-weight: bold;
        text-align: right;
        width: 30%;
     }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""

# Function to generate custom HTML Table
def dataframe_to_custom_html(df):
    html = '<table class="custom-table">'
    # Ensure column names match exactly what's expected
    rank_col = df.columns[0]
    name1_col = df.columns[1]
    name2_col = df.columns[2]
    time_col = df.columns[3]

    for index, row in df.iterrows():
        html += '<tr>'
        html += f'<td class="rank-col">{row[rank_col]}</td>'
        html += f'<td class="name1-col">{row[name1_col]}</td>'
        html += f'<td class="name2-col">{row[name2_col]}</td>'
        html += f'<td class="time-col">{row[time_col]}</td>'
        html += '</tr>'
    html += '</table>'
    return html 
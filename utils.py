import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time # Needed for caching demo if API fails
import streamlit.components.v1 as components # Import components

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

# --- Google Sheets Integration --- 

# Define scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

# Function to load credentials and authorize gspread
# Cache the gspread client authorization for efficiency
@st.cache_resource(ttl=3600) # Cache the connection for an hour
def connect_gsheet():
    try:
        # Try different possible locations for the credentials in st.secrets
        if "google_sheets_credentials" in st.secrets:
            # Found at top level
            creds_dict = st.secrets["google_sheets_credentials"]
        elif "type" in st.secrets and st.secrets["type"] == "service_account":
            # Credentials are at top level (not nested)
            creds_dict = st.secrets
        else:
            # Print available keys for debugging
            available_keys = list(st.secrets.keys())
            st.error(f"Could not find Google Sheets credentials in secrets. Available keys: {available_keys}")
            # If 'utils' is one of the keys (which seems likely from the error), try that path
            if "utils" in available_keys and "google_sheets_credentials" in st.secrets["utils"]:
                creds_dict = st.secrets["utils"]["google_sheets_credentials"]
            else:
                raise KeyError("Could not find a valid path to Google service account credentials in st.secrets")
        
        # Debug info (optional) - remove in production if secrets show up in logs
        # st.write(f"Found credential keys: {list(creds_dict.keys())}")
        
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {str(e)}")
        # More detailed error to help debug
        import traceback
        st.error(f"Details: {traceback.format_exc()}")
        return None

# Function to load data from a specific sheet and worksheet using Sheet ID
# Cache the data itself with a shorter TTL for updates
@st.cache_data(ttl=60) # Cache data for 60 seconds
def load_data_from_gsheet(_client, sheet_id, worksheet_name):
    if _client is None:
        st.error("Google Sheets client not available. Cannot load data.")
        # Return a dummy DataFrame to prevent downstream errors
        return pd.DataFrame({
            'Rank': [1], 'Name1': ['Error'], 'Name2': ['Loading Data'], 'Time': [str(time.time())]
        })
    try:
        st.info(f"Fetching data from sheet ID: ...{sheet_id[-10:]} / Worksheet: {worksheet_name}...") # User feedback
        # --- Open using Sheet ID instead of Name ---
        spreadsheet = _client.open_by_key(sheet_id)
        # --------------------------------------------
        worksheet = spreadsheet.worksheet(worksheet_name)
        # Get all values, assuming first row is header
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        # Basic validation: Check if expected columns are roughly there
        if df.shape[1] < 4:
             st.warning(f"Warning: Loaded data from {worksheet_name} has fewer than 4 columns.")
             # Pad with empty columns if needed to avoid breaking table generation
             while df.shape[1] < 4:
                 df[f'EmptyCol_{df.shape[1]+1}'] = ''
        elif df.empty:
             st.warning(f"Warning: Worksheet {worksheet_name} appears to be empty.")
             # Return specific structure if empty
             return pd.DataFrame(columns=['Rank', 'Name1', 'Name2', 'Time'])

        st.success(f"Data loaded successfully from {worksheet_name}!") # User feedback
        return df

    except gspread.exceptions.APIError as e:
        # More specific error for permission issues / sheet not found by ID
        st.error(f"Google API Error: Could not access Sheet ID ...{sheet_id[-10:]}. Check sharing permissions for the service account and ensure the Sheet ID is correct. Details: {e}")
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Error: Worksheet '{worksheet_name}' not found in sheet ID ...{sheet_id[-10:]}.")
    except Exception as e:
        st.error(f"Failed to load data from {worksheet_name}: {e}")

    # Return a dummy DataFrame on error
    return pd.DataFrame({
        'Rank': [1], 'Name1': ['Error'], 'Name2': ['Loading Data'], 'Time': [str(time.time())]
    })

# --- End Google Sheets Integration ---

# Function to generate custom HTML Table
def dataframe_to_custom_html(df):
    if df.empty or df.shape[1] < 4:
        return "<p>No data available or data format incorrect.</p>"

    html = '<table class="custom-table">'
    # Dynamically get column names from the DataFrame
    rank_col = df.columns[0]
    name1_col = df.columns[1]
    name2_col = df.columns[2]
    team_col = df.columns[3]
    time_col = df.columns[4]

    for index, row in df.iterrows():
        html += '<tr>'
        html += f'<td class="rank-col">{row[rank_col]}</td>'
        html += f'<td class="name1-col">{row[name1_col]}</td>'
        html += f'<td class="name2-col">{row[name2_col]}</td>'
        html += f'<td class="team_col">{row[team_col]}</td>'
        html += f'<td class="time-col">{row[time_col]}</td>'
        html += '</tr>'
    html += '</table>'
    return html 

def display_leaderboard(title: str, results: list[tuple]):
    """
    Displays a leaderboard with custom styling using HTML and CSS.

    Args:
        title (str): The title to display above the leaderboard.
        results (list[tuple]): A list of tuples, where each tuple represents a row.
                               Expected format: (rank, name, team, time)
    """
    # CSS for styling
    css = """
<style>
.leaderboard-container {
    background-color: #1c3d5a; /* Dark blue background */
    color: white;
    padding: 15px;
    border-radius: 8px;
    font-family: sans-serif; /* Basic sans-serif font */
    margin-bottom: 1em; /* Add some space below the leaderboard */
}
.leaderboard-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 15px;
    text-align: left;
}
.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
}
.leaderboard-table td {
    padding: 8px 5px;
    vertical-align: middle;
    border-top: 1px solid #3a5a7a; /* Lighter blue line between rows */
}
.leaderboard-table tr:first-child td {
    border-top: none; /* No line above the first row */
}
.rank-col {
    width: 5%;
    text-align: left;
    font-weight: bold;
}
.name-col {
    width: 40%;
    text-align: left;
}
.team-col {
    width: 30%;
    text-align: left;
}
.time-col {
    width: 25%;
    text-align: right;
    font-family: monospace; /* Monospace font for time */
}
</style>
"""

    # HTML structure
    html = f"""
<div class="leaderboard-container">
  <div class="leaderboard-title">{title}</div>
  <table class="leaderboard-table">
    <tbody>
"""

    # Add rows dynamically
    for row_data in results:
        # Basic validation to prevent errors if row is too short
        if len(row_data) == 4:
            # Explicitly cast data to string before formatting
            rank = str(row_data[0])
            name = str(row_data[1])
            team = str(row_data[2])
            time = str(row_data[3])
            html += f"""
              <tr>
                <td class="rank-col">{rank}</td>
                <td class="name-col">{name}</td>
                <td class="team-col">{team}</td>
                <td class="time-col">{time}</td>
              </tr>
        """
        else:
            # Handle potential malformed row data gracefully (e.g., log a warning or skip)
            st.warning(f"Skipping malformed row in leaderboard data: {row_data}")


    html += """
    </tbody>
  </table>
</div>
"""

    # --- DEBUG: Print the generated HTML --- 
    # print("--- Generated Leaderboard HTML ---")
    # print(html)
    # print("--- End Generated HTML ---")
    # -------------------------------------

    # Combine CSS and HTML into a single string for the component
    full_html = css + html

    # Use components.html instead of st.markdown for the table itself
    # Estimate height: ~60px for title/padding + ~35px per row
    component_height = 60 + (len(results) * 35)
    # Pass the combined HTML and CSS string
    components.html(full_html, height=component_height) 
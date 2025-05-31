# Project Description: E-pyöräilyn SM-kisojen Tulospalvelu Frontend

## Project Overview
This project was developed as the frontend for the results service of the Finnish E-cycling National Championships (e-pyöräilyn SM-kisat). The main goal was to create a web application that could deliver almost real-time race results both to the live stream and to viewers following the event online.

## Problem Statement
During the event, there was a need for a user-friendly frontend that could distribute up-to-date race results efficiently. The challenge was to provide a platform where results could be shared instantly with both the live stream production and the audience, ensuring everyone had access to the latest standings and information.

## Solution
To solve this, I built a Streamlit application that connects directly to a Google Sheet where the race results were being updated. Data was fetched using the `gspread` library and a Google service account, enabling almost real-time updates without a separate backend server. This lightweight and agile solution also allowed for easy manual corrections directly in the sheet, making it flexible for both data entry and result management. The frontend made it easy to present and distribute results, supporting both live updates for the stream and an accessible results service for later reference.

The user interface included options to select the race and category, making it easy for users to find the correct results quickly.

## Outcome
The solution proved highly effective, with over 400 unique visitors accessing the site during the event. The application successfully met the needs of both the organizers and the audience, providing a reliable and easy-to-use results service.

## Libraries Used
- **streamlit** – web-sovelluksen runko
- **pandas** – datan käsittely ja muokkaus
- **gspread** – integraatio Google Sheetsin kanssa
- **streamlit-autorefresh** – automaattinen päivitys

*Project created: May 2025*
*Author: Panua Alaluusua*

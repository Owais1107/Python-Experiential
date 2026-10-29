# Smart Home Energy Consumption Monitor

A Python + Streamlit dashboard for estimating household electricity consumption and cost.

## Features
- Editable appliance list with power, hours used per day, and quantity
- Estimated daily and billing-period energy use (kWh)
- Estimated electricity bill using a configurable ₹/kWh rate
- Appliance-wise bar chart and consumption-share pie chart
- High-usage appliance alerts
- Energy-saving recommendations
- Downloadable CSV report

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `streamlit run app.py`

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt` to the repository root.
3. Open Streamlit Community Cloud and connect your GitHub account.
4. Choose the repository and set the main file path to `app.py`.
5. Click Deploy.

All calculations are estimates based on the values entered by the user.

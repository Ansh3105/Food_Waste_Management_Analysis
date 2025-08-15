🍽️ Local Food Wastage Management System

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wasterecycle.streamlit.app)

**🔗 Live Demo:** [Click here to open the app](https://wasterecycle.streamlit.app)


Executive Summary

The Local Food Wastage Management System is a data-driven platform designed to reduce food waste and improve food accessibility by connecting surplus food providers with individuals and organizations in need. Built with Python, SQL, and Streamlit, this application enables real-time food listing, claim tracking, CRUD operations, and insightful analytics.

By integrating geolocation-based filtering, interactive dashboards, and 15+ SQL-powered reports, the system empowers communities to redistribute food efficiently, reduce environmental impact, and support social good initiatives.

It supports two deployment modes:

CSV-based – Optimized for cloud environments like Streamlit Cloud without database dependencies.

SQL-based – Live querying and updates via Microsoft SQL Server for on-premise or self-hosted deployments.



📂 Project Structure
.
├── App_Csv_Version.py                # Streamlit application (CSV-based)
├── App_SQL_Version.py                # Streamlit application (SQL-based)
├── requirements.txt                  # Python dependencies
│
├── SQL_Files/                         # SQL scripts and query documents
│   ├── Waste_Managemnt_SQL_File.sql
│   └── Waste-management_SQL_Queries.pdf
│
├── Original_Dataset_Files/            # Raw datasets (pre-cleaning)
│   ├── claims_data.csv
│   ├── food_listings_data.csv
│   ├── providers_data.csv
│   └── receivers_data.csv
│
└── Cleaned(EDA)_Dataset_Files/        # Cleaned datasets for CSV deployment
    ├── new_claims_data.csv
    ├── new_food_listing_data.csv
    ├── new_providers_data.csv
    └── new_receivers_data.csv






🎯 Objectives

Minimize food wastage through structured redistribution.

Provide actionable insights using data analytics.

Support real-time interaction between providers and receivers.

Enable CRUD operations for seamless data management.



🚀 Features
1. Food Listings

Filter by city, provider, food type, and meal type.

View interactive, real-time listings.

Geolocation-based accessibility for nearby resources.

2. Data Insights & Analytics

Provider and receiver distribution by city.

Top contributors and most popular food categories.

Claim statistics (pending, completed, canceled).

Total available quantities and high-demand locations.

3. CRUD Functionality

Add, update, and delete food listings.

Persist changes in CSV or SQL database depending on deployment mode.

4. Contact Management

Access direct contact details for providers and receivers.

Identify high-activity receivers for targeted outreach.



🛠️ Installation & Setup
1. Clone the Repository
   git clone https://github.com/Ansh3105/Food_Waste_Management_Analysis.git
cd Food_Waste_Management_Analysis


3. Install Dependencies
pip install -r requirements.txt


4. requirements.txt

pandas==2.3.1
pyodbc==5.2.0
streamlit==1.48.1



▶️ Running the Application
CSV Mode (Recommended for Streamlit Cloud)
streamlit run App_Csv_Version.py


Uses datasets from Cleaned(EDA)_Dataset_Files/

No database connection required.

SQL Mode (For Local / On-Premise)
Option 1 – Default SQL Mode
streamlit run App_SQL_Version.py


Requires Microsoft SQL Server with:

dbo.claims_data

dbo.listing_data

dbo.providers_data

dbo.receivers_data

Update the database connection inside App_SQL_Version.py.

Option 2 – Localhost with Windows Authentication (DESKTOP-SMR9LLQ Example)

Update the connection string in App_SQL_Version.py:

import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-SMR9LLQ;'
    'DATABASE=food_waste_management;'
    'Trusted_Connection=yes;'
)


Replace DESKTOP-SMR9LLQ with your machine’s SQL Server instance name if different.

Make sure the food_waste_management database exists locally.
If not, run:

SQL_Files/Waste_Managemnt_SQL_File.sql in SQL Server Management Studio (SSMS).

Run the app from CMD:

streamlit run "C:\Users\HP\PycharmProjects\Streamlit\App_SQL_Version.py"






🗄️ Database Setup

Execute SQL_Files/Waste_Managemnt_SQL_File.sql to create the database and import CSV data.

Use SQL_Files/Waste-management_SQL_Queries.pdf for predefined analytical queries and reports.



📊 Dataset Overview

Dataset File	Description

new_providers_data.csv	Provider details (ID, name, type, address, city, contact)
new_receivers_data.csv	Receiver details (ID, name, type, city, contact)
new_food_listing_data.csv	Food listings (ID, name, quantity, expiry, provider info, location, food type, meal type)
new_claims_data.csv	Claims (ID, food ID, receiver ID, status, timestamp)

📈 Key Analytical Queries

Provider count per city

Receiver count per city

Total quantity per provider type

Total claims per receiver

Total food quantity listed

Total food quantity available per provider

Top 5 cities by total listings

Top 5 cities with highest number of food listings

Most commonly available food types

Number of food claims made for each food item

Percentage of food claims by status

Average quantity of food claimed per receiver

Most claimed meal type

Total quantity of food donated by each provider

Receivers by total quantity of food claimed

Monthly total claims



💼 Business Impact

Efficient food redistribution and reduced wastage.

Greater accessibility through geolocation-enabled search.

Actionable insights for donation planning and community support.

Strengthened connections between providers and receivers.



🏷️ Technology Stack

Languages: Python, SQL

Framework: Streamlit

Database: Microsoft SQL Server

Libraries: Pandas, PyODBC

Domains: Food Management, Waste Reduction, Social Impact



📜 License

Licensed under the MIT License.

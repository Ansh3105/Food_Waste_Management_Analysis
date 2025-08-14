import streamlit as st
import pandas as pd
import pyodbc

# ---------------------------
# Database Connection
# ---------------------------
server = 'DESKTOP-SMR9LLQ'
database = 'food_waste_management'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")
st.title("🍽️ Local Food Wastage Management System")

# ---------------------------
# 1. Filtered Food Listings
# ---------------------------
st.sidebar.header("Filter Options")

cities = pd.read_sql("SELECT DISTINCT Location FROM dbo.listing_data", conn)["Location"].dropna().tolist()
providers = pd.read_sql("SELECT DISTINCT Name FROM dbo.providers_data", conn)["Name"].dropna().tolist()
food_types = pd.read_sql("SELECT DISTINCT Food_Type FROM dbo.listing_data", conn)["Food_Type"].dropna().tolist()
meal_types = pd.read_sql("SELECT DISTINCT Meal_Type FROM dbo.listing_data", conn)["Meal_Type"].dropna().tolist()

selected_city = st.sidebar.selectbox("Select City", ["All"] + cities)
selected_provider = st.sidebar.selectbox("Select Provider", ["All"] + providers)
selected_food_type = st.sidebar.selectbox("Select Food Type", ["All"] + food_types)
selected_meal_type = st.sidebar.selectbox("Select Meal Type", ["All"] + meal_types)

query = "SELECT * FROM dbo.listing_data WHERE 1=1"
if selected_city != "All":
    query += f" AND Location = '{selected_city}'"
if selected_provider != "All":
    query += f" AND Provider_ID IN (SELECT Provider_ID FROM dbo.providers_data WHERE Name = '{selected_provider}')"
if selected_food_type != "All":
    query += f" AND Food_Type = '{selected_food_type}'"
if selected_meal_type != "All":
    query += f" AND Meal_Type = '{selected_meal_type}'"

df = pd.read_sql(query, conn)
st.subheader("📋 Filtered Food Listings")
st.dataframe(df)

# ---------------------------
# 2. SQL Query Results
# ---------------------------
st.subheader("📊 SQL Query Results")

queries = {
    "Query 1: Provider count per city": """
        SELECT UPPER(LTRIM(RTRIM(City))) AS City,
               COUNT(DISTINCT Provider_ID) AS Provider_Count
        FROM dbo.providers_data
        GROUP BY UPPER(LTRIM(RTRIM(City)))
        ORDER BY City;
    """,
    "Query 2: Receiver count per city": """
        SELECT UPPER(LTRIM(RTRIM(City))) AS City,
               COUNT(DISTINCT Receiver_ID) AS Receiver_Count
        FROM dbo.receivers_data
        GROUP BY UPPER(LTRIM(RTRIM(City)))
        ORDER BY City;
    """,
    "Query 3: Total quantity per provider type": """
        SELECT Provider_Type,
               SUM(Quantity) AS Total_Quantity
        FROM dbo.listing_data
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC;
    """,
    "Query 4: Total claims per receiver": """
        SELECT Receiver_ID,
               COUNT(Claim_ID) AS Total_Claims
        FROM dbo.claims_data
        GROUP BY Receiver_ID
        ORDER BY Total_Claims DESC;
    """,
    "Query 5: Total food quantity listed": """
        SELECT SUM(Quantity) AS Total_Food_Quantity
        FROM dbo.listing_data;
    """,
    "Query 6: Total food quantity available per provider": """
        SELECT Provider_ID,
               SUM(Quantity) AS Total_Food_Quantity_Available
        FROM dbo.listing_data
        GROUP BY Provider_ID
        ORDER BY SUM(Quantity) DESC;
    """,
    "Query 7: Top 5 cities by total listings": """
        SELECT TOP 5 Location AS City,
               COUNT(Food_ID) AS Total_Listings
        FROM dbo.listing_data
        GROUP BY Location
        ORDER BY Total_Listings;
    """,
    "Query 8: Top 5 cities with highest number of food listings": """
        SELECT TOP 5 Location,
               COUNT(*) AS Listing_Count
        FROM dbo.listing_data
        GROUP BY Location
        ORDER BY Listing_Count DESC;
    """,
    "Query 9: Most commonly available food types": """
        SELECT Food_Type,
               COUNT(*) AS Listing_Count
        FROM dbo.listing_data
        GROUP BY Food_Type
        ORDER BY Listing_Count DESC;
    """,
    "Query 10: Number of food claims made for each food item": """
        SELECT Food_ID,
               COUNT(*) AS Claim_Count
        FROM dbo.claims_data
        GROUP BY Food_ID
        ORDER BY Claim_Count DESC;
    """,
    "Query 11: Percentage of food claims by status": """
        SELECT Status,
               COUNT(*) AS Claim_Count,
               CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dbo.claims_data) AS DECIMAL(5,2)) AS Percentage
        FROM dbo.claims_data
        GROUP BY Status
        ORDER BY Percentage DESC;
    """,
    "Query 12: Average quantity of food claimed per receiver": """
        SELECT r.Receiver_ID,
               AVG(l.Quantity) AS Avg_Quantity_Claimed
        FROM dbo.claims_data AS c
        JOIN dbo.listing_data AS l ON c.Food_ID = l.Food_ID
        JOIN dbo.receivers_data AS r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Receiver_ID
        ORDER BY Avg_Quantity_Claimed DESC;
    """,
    "Query 13: Most claimed meal type": """
        SELECT l.Meal_Type,
               COUNT(*) AS Claim_Count
        FROM dbo.claims_data AS c
        JOIN dbo.listing_data AS l ON c.Food_ID = l.Food_ID
        GROUP BY l.Meal_Type
        ORDER BY Claim_Count DESC;
    """,
    "Query 14: Total quantity of food donated by each provider": """
        SELECT p.Provider_ID,
               p.Name AS Provider_Name,
               SUM(l.Quantity) AS Total_Quantity_Donated
        FROM dbo.listing_data AS l
        JOIN dbo.providers_data AS p ON l.Provider_ID = p.Provider_ID
        GROUP BY p.Provider_ID, p.Name
        ORDER BY Total_Quantity_Donated DESC;
    """,
    "Query 15: Receivers by total quantity of food claimed": """
        SELECT r.Receiver_ID,
               r.Name AS Receiver_Name,
               SUM(l.Quantity) AS Total_Quantity_Claimed
        FROM dbo.claims_data AS c
        JOIN dbo.listing_data AS l ON c.Food_ID = l.Food_ID
        JOIN dbo.receivers_data AS r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Receiver_ID, r.Name
        ORDER BY Total_Quantity_Claimed DESC;
    """,
    "Query 16: Monthly total claims": """
        SELECT YEAR(Timestamp) AS Claim_Year,
               MONTH(Timestamp) AS Claim_Month,
               COUNT(*) AS Total_Claims
        FROM dbo.claims_data
        GROUP BY YEAR(Timestamp), MONTH(Timestamp)
        ORDER BY Claim_Year, Claim_Month;
    """
}

for title, sql in queries.items():
    st.markdown(f"**{title}**")
    result_df = pd.read_sql(sql, conn)
    st.dataframe(result_df)

# ---------------------------
# 3. CRUD Operations
# ---------------------------
st.title("🛠 Manage Food Listings (CRUD)")

# READ - Display Data
df_crud = pd.read_sql("SELECT * FROM dbo.listing_data", conn)
st.subheader("📋 Current Food Listings")
st.dataframe(df_crud)

# CREATE
st.subheader("➕ Add New Food Listing")
with st.form("add_form"):
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1)
    expiry_date = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1)
    location = st.text_input("Location")
    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
    submitted = st.form_submit_button("Add Listing")

    if submitted:
        cursor.execute("""
            INSERT INTO dbo.listing_data (Food_Name, Quantity, Expiry_Date, Provider_ID, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (food_name, quantity, expiry_date, provider_id, location, food_type, meal_type))
        conn.commit()
        st.success("✅ New food listing added!")

# UPDATE
st.subheader("✏️ Update Food Listing Quantity")
update_id = st.number_input("Enter Food ID to Update", min_value=1)
new_quantity = st.number_input("New Quantity", min_value=1, key="update_qty")
if st.button("Update Quantity"):
    cursor.execute("""
        UPDATE dbo.listing_data
        SET Quantity = ?
        WHERE Food_ID = ?
    """, (new_quantity, update_id))
    conn.commit()
    st.success(f"✅ Food listing {update_id} updated!")

# DELETE
st.subheader("🗑️ Delete Food Listing")
delete_id = st.number_input("Enter Food ID to Delete", min_value=1, key="delete_id")
if st.button("Delete Listing"):
    cursor.execute("DELETE FROM dbo.listing_data WHERE Food_ID = ?", (delete_id,))
    conn.commit()
    st.warning(f"⚠️ Food listing {delete_id} deleted!")

# ---------------------------
# 4. Provider Contact Details
# ---------------------------
if not df.empty:
    st.subheader("📞 Provider Contact Details")
    provider_ids = df["Provider_ID"].unique().tolist()
    contacts_query = f"""
    SELECT Provider_ID, Name, Contact 
    FROM dbo.providers_data
    WHERE Provider_ID IN ({','.join(map(str, provider_ids))})
    """
    contacts_df = pd.read_sql(contacts_query, conn)
    st.table(contacts_df)

# Close DB connection
conn.close()

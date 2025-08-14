import streamlit as st
import pandas as pd

# ---------------------------
# Load Data from CSVs
# ---------------------------
claims_df = pd.read_csv("Cleaned(EDA)_Dataset_file/new_claims_data.csv")
listing_df = pd.read_csv("Cleaned(EDA)_Dataset_file/new_food_listing_data.csv")
providers_df = pd.read_csv("Cleaned(EDA)_Dataset_file/new_providers_data.csv")
receivers_df = pd.read_csv("Cleaned(EDA)_Dataset_file/new_receivers_data.csv")

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")
st.title("🍽️ Local Food Wastage Management System")

# ---------------------------
# 1. Filtered Food Listings
# ---------------------------
st.sidebar.header("Filter Options")

cities = sorted(listing_df["Location"].dropna().unique())
providers = sorted(providers_df["Name"].dropna().unique())
food_types = sorted(listing_df["Food_Type"].dropna().unique())
meal_types = sorted(listing_df["Meal_Type"].dropna().unique())

selected_city = st.sidebar.selectbox("Select City", ["All"] + cities)
selected_provider = st.sidebar.selectbox("Select Provider", ["All"] + providers)
selected_food_type = st.sidebar.selectbox("Select Food Type", ["All"] + food_types)
selected_meal_type = st.sidebar.selectbox("Select Meal Type", ["All"] + meal_types)

filtered_df = listing_df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["Location"] == selected_city]
if selected_provider != "All":
    prov_id = providers_df.loc[providers_df["Name"] == selected_provider, "Provider_ID"]
    filtered_df = filtered_df[filtered_df["Provider_ID"].isin(prov_id)]
if selected_food_type != "All":
    filtered_df = filtered_df[filtered_df["Food_Type"] == selected_food_type]
if selected_meal_type != "All":
    filtered_df = filtered_df[filtered_df["Meal_Type"] == selected_meal_type]

st.subheader("📋 Filtered Food Listings")
st.dataframe(filtered_df)

# ---------------------------
# 2. Data Insights (Pandas instead of SQL)
# ---------------------------
st.subheader("📊 Data Insights")

queries = {
    "Provider count per city": providers_df.groupby(providers_df["City"].str.strip().str.upper())["Provider_ID"].nunique().reset_index(name="Provider_Count"),
    "Receiver count per city": receivers_df.groupby(receivers_df["City"].str.strip().str.upper())["Receiver_ID"].nunique().reset_index(name="Receiver_Count"),
    "Total quantity per provider type": listing_df.groupby("Provider_Type")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False),
    "Total claims per receiver": claims_df.groupby("Receiver_ID")["Claim_ID"].count().reset_index(name="Total_Claims").sort_values("Total_Claims", ascending=False),
    "Total food quantity listed": pd.DataFrame({"Total_Food_Quantity": [listing_df["Quantity"].sum()]}),
    "Total food quantity available per provider": listing_df.groupby("Provider_ID")["Quantity"].sum().reset_index(name="Total_Food_Quantity_Available").sort_values("Total_Food_Quantity_Available", ascending=False),
    "Top 5 cities by total listings": listing_df.groupby("Location")["Food_ID"].count().reset_index(name="Total_Listings").nlargest(5, "Total_Listings"),
    "Most commonly available food types": listing_df.groupby("Food_Type")["Food_ID"].count().reset_index(name="Listing_Count").sort_values("Listing_Count", ascending=False),
    "Number of food claims made for each food item": claims_df.groupby("Food_ID")["Claim_ID"].count().reset_index(name="Claim_Count").sort_values("Claim_Count", ascending=False),
    "Percentage of food claims by status": claims_df.groupby("Status")["Claim_ID"].count().reset_index(name="Claim_Count").assign(Percentage=lambda x: (x["Claim_Count"] * 100 / len(claims_df)).round(2)),
    "Average quantity of food claimed per receiver": claims_df.merge(listing_df, on="Food_ID").groupby("Receiver_ID")["Quantity"].mean().reset_index(name="Avg_Quantity_Claimed").sort_values("Avg_Quantity_Claimed", ascending=False),
    "Most claimed meal type": claims_df.merge(listing_df, on="Food_ID").groupby("Meal_Type")["Claim_ID"].count().reset_index(name="Claim_Count").sort_values("Claim_Count", ascending=False),
    "Total quantity of food donated by each provider": listing_df.merge(providers_df, on="Provider_ID").groupby(["Provider_ID", "Name"])["Quantity"].sum().reset_index(name="Total_Quantity_Donated").sort_values("Total_Quantity_Donated", ascending=False),
    "Receivers by total quantity of food claimed": claims_df.merge(listing_df, on="Food_ID").merge(receivers_df, on="Receiver_ID").groupby(["Receiver_ID", "Name"])["Quantity"].sum().reset_index(name="Total_Quantity_Claimed").sort_values("Total_Quantity_Claimed", ascending=False),
}

for title, df_q in queries.items():
    st.markdown(f"**{title}**")
    st.dataframe(df_q)

# ---------------------------
# 3. CRUD Operations (in-memory only)
# ---------------------------
st.title("🛠 Manage Food Listings (CRUD)")

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
        new_id = listing_df["Food_ID"].max() + 1
        new_row = pd.DataFrame({
            "Food_ID": [new_id],
            "Food_Name": [food_name],
            "Quantity": [quantity],
            "Expiry_Date": [expiry_date],
            "Provider_ID": [provider_id],
            "Location": [location],
            "Food_Type": [food_type],
            "Meal_Type": [meal_type]
        })
        listing_df = pd.concat([listing_df, new_row], ignore_index=True)
        st.success("✅ New food listing added! (Note: not saved to CSV in this demo)")

# UPDATE
st.subheader("✏️ Update Food Listing Quantity")
update_id = st.number_input("Enter Food ID to Update", min_value=1)
new_quantity = st.number_input("New Quantity", min_value=1, key="update_qty")
if st.button("Update Quantity"):
    listing_df.loc[listing_df["Food_ID"] == update_id, "Quantity"] = new_quantity
    st.success(f"✅ Food listing {update_id} updated! (Note: not saved to CSV in this demo)")

# DELETE
st.subheader("🗑️ Delete Food Listing")
delete_id = st.number_input("Enter Food ID to Delete", min_value=1, key="delete_id")
if st.button("Delete Listing"):
    listing_df = listing_df[listing_df["Food_ID"] != delete_id]
    st.warning(f"⚠️ Food listing {delete_id} deleted! (Note: not saved to CSV in this demo)")

# ---------------------------
# 4. Provider Contact Details
# ---------------------------
if not filtered_df.empty:
    st.subheader("📞 Provider Contact Details")
    provider_ids = filtered_df["Provider_ID"].unique()
    contacts_df = providers_df[providers_df["Provider_ID"].isin(provider_ids)][["Provider_ID", "Name", "Contact"]]
    st.table(contacts_df)

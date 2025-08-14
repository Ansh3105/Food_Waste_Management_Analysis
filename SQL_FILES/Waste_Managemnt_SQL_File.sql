CREATE DATABASE food_waste_management;

USE food_waste_management;



-- For the tables, I imported the required CSV files through the Import Flat File option
-- with the table names as:
-- dbo.claims_data, dbo.listing_data, dbo.providers_data, dbo.receivers_data




-- ===============================================
-- Query 1: Provider count per city
-- ===============================================
SELECT 
    UPPER(LTRIM(RTRIM(City))) AS City,
    COUNT(DISTINCT Provider_ID) AS Provider_Count
FROM dbo.providers_data
GROUP BY UPPER(LTRIM(RTRIM(City)))
ORDER BY City;
GO

-- ===============================================
-- Query 2: Receiver count per city
-- ===============================================
SELECT 
    UPPER(LTRIM(RTRIM(City))) AS City,
    COUNT(DISTINCT Receiver_ID) AS Receiver_Count
FROM dbo.receivers_data
GROUP BY UPPER(LTRIM(RTRIM(City)))
ORDER BY City;
GO

-- ===============================================
-- Query 3: Total quantity per provider type
-- ===============================================
SELECT 
    Provider_Type,
    SUM(Quantity) AS Total_Quantity
FROM dbo.listing_data
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;
GO

-- ===============================================
-- Query 4: Total claims per receiver
-- ===============================================
SELECT 
    Receiver_ID,
    COUNT(Claim_ID) AS Total_Claims
FROM dbo.claims_data
GROUP BY Receiver_ID
ORDER BY Total_Claims DESC;
GO

-- ===============================================
-- Query 5: Total food quantity listed
-- ===============================================
SELECT 
    SUM(Quantity) AS Total_Food_Quantity
FROM dbo.listing_data;
GO

-- ===============================================
-- Query 6: Total food quantity available per provider
-- ===============================================
SELECT
    Provider_ID,
    SUM(Quantity) AS Total_Food_Quantity_Available
FROM dbo.listing_data
GROUP BY Provider_ID
ORDER BY SUM(Quantity) DESC;
GO

-- ===============================================
-- Query 7: Top 5 cities by total listings
-- ===============================================
SELECT TOP 5
    Location AS City,
    COUNT(Food_ID) AS Total_Listings
FROM dbo.listing_data
GROUP BY Location
ORDER BY Total_Listings



-- ===============================================
-- Query 8: Top 5 Cities with the highest number of food listings
-- ===============================================
SELECT TOP 5 
    Location, 
    COUNT(*) AS Listing_Count
FROM 
    dbo.listing_data
GROUP BY 
    Location
ORDER BY 
    Listing_Count DESC;


-- ===============================================
-- Query 9: Most commonly available food types
-- ===============================================
SELECT 
    Food_Type, 
    COUNT(*) AS Listing_Count
FROM 
    dbo.listing_data
GROUP BY 
    Food_Type
ORDER BY 
    Listing_Count DESC;




-- ===============================================
-- Query 10: Number of food claims made for each food item
-- ===============================================
SELECT 
    Food_ID, 
    COUNT(*) AS Claim_Count
FROM 
    dbo.claims_data
GROUP BY 
    Food_ID
ORDER BY 
    Claim_Count DESC;



-- ===============================================
-- Query 11: Percentage of food claims by status
-- ===============================================
SELECT 
    Status,
    COUNT(*) AS Claim_Count,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM dbo.claims_data) AS DECIMAL(5,2)) AS Percentage
FROM 
    dbo.claims_data
GROUP BY 
    Status
ORDER BY 
    Percentage DESC;


-- ===============================================
-- Query 12: Average quantity of food claimed per receiver
-- ===============================================
SELECT 
    r.Receiver_ID,
    AVG(l.Quantity) AS Avg_Quantity_Claimed
FROM 
    dbo.claims_data AS c
JOIN 
    dbo.listing_data AS l ON c.Food_ID = l.Food_ID
JOIN 
    dbo.receivers_data AS r ON c.Receiver_ID = r.Receiver_ID
GROUP BY 
    r.Receiver_ID
ORDER BY 
    Avg_Quantity_Claimed DESC;


-- ===============================================
-- Query 13: Most claimed meal type
-- ===============================================
SELECT 
    l.Meal_Type,
    COUNT(*) AS Claim_Count
FROM 
    dbo.claims_data AS c
JOIN 
    dbo.listing_data AS l ON c.Food_ID = l.Food_ID
GROUP BY 
    l.Meal_Type
ORDER BY 
    Claim_Count DESC;



    -- ===============================================
-- Query 14: Total quantity of food donated by each provider
-- ===============================================
SELECT 
    p.Provider_ID,
    p.Name AS Provider_Name,
    SUM(l.Quantity) AS Total_Quantity_Donated
FROM 
    dbo.listing_data AS l
JOIN 
    dbo.providers_data AS p ON l.Provider_ID = p.Provider_ID
GROUP BY 
    p.Provider_ID, 
    p.Name
ORDER BY 
    Total_Quantity_Donated DESC;


-- ===============================================
-- Query 15: receivers by total quantity of food claimed
-- ===============================================
SELECT 
    r.Receiver_ID,
    r.Name AS Receiver_Name,
    SUM(l.Quantity) AS Total_Quantity_Claimed
FROM 
    dbo.claims_data AS c
JOIN 
    dbo.listing_data AS l ON c.Food_ID = l.Food_ID
JOIN 
    dbo.receivers_data AS r ON c.Receiver_ID = r.Receiver_ID
GROUP BY 
    r.Receiver_ID, r.Name
ORDER BY 
    Total_Quantity_Claimed DESC

-- ===============================================
-- Query 18: Monthly total claims
-- ===============================================
SELECT 
    YEAR(Timestamp) AS Claim_Year,
    MONTH(Timestamp) AS Claim_Month,
    COUNT(*) AS Total_Claims
FROM 
    dbo.claims_data
GROUP BY 
    YEAR(Timestamp), MONTH(Timestamp)
ORDER BY 
    Claim_Year, Claim_Month;



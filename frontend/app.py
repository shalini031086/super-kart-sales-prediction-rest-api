
import streamlit as st
import pandas as pd
import requests

# Backend URL
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction")

st.subheader("Online Prediction")

Store_Age_Years = st.number_input(
    "Store Age in Years",
    min_value=1,
    step=1,
    value=2
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Food Mart",
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3"
    ]
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    [
        "Dairy",
        "Soft Drinks",
        "Meat",
        "Fruits and Vegetables",
        "Frozen Foods",
        "Snack Foods",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Bread",
        "Breakfast",
        "Hard Drinks",
        "Others",
        "Seafood",
        "Starchy Foods",
        "Perishables",
        "Non Perishables"
    ]
)

Product_Id_char = st.selectbox(
    "Product ID Prefix",
    ["FD", "DR", "NC"]
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=100.0
)

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=5.0
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=100.0
)

input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type_Category": Product_Type_Category,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years
}

if st.button("Predict"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/superkart",
            json=input_data
        )

        if response.status_code == 200:

            prediction = response.json()[
                "Predicted_Product_Store_Sales_Total"
            ]

            st.success(
                f"Predicted Product Store Sales Total: {prediction}"
            )

        else:
            st.error(response.text)

    except Exception as e:
        st.error(str(e))

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict Batch"):

        files = {
            "file": uploaded_file
        }

        response = requests.post(
            f"{BACKEND_URL}/v1/superkartbatch",
            files=files
        )

        if response.status_code == 200:

            predictions = response.json()

            st.success("Batch Prediction Completed")

            st.write(predictions)

        else:

            st.error(response.text)

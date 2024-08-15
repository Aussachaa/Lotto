import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Lottery Data Explorer", layout="wide")

# Title
st.title("Lottery Data Explorer")

# Load data
@st.cache_data
def load_data():
    path_excel = "https://raw.githubusercontent.com/Aussachaa/Lotto/main/DB_Lottery.xlsx"
    return pd.read_excel(path_excel, sheet_name="DB", usecols="A:I")

df = load_data()

# Display data overview
st.subheader("Data Overview")
st.dataframe(df.head())

# Basic statistics
st.subheader("Basic Statistics")
st.write(df.describe())

# Add more interactive elements here, such as:
# - Filters for specific date ranges
# - Charts showing number frequency
# - Prediction features if required

# You can expand on this basic structure based on specific requirements
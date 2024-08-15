import streamlit as st
import pandas as pd
import openpyxl as xl


# Page config
st.set_page_config(page_title="Lottery Data Explorer", layout="wide")

# Title
st.title("Lottery Data Explorer")

# Load data
@st.cache_data
def load_data():
    path_excel = "https://raw.githubusercontent.com/Aussachaa/Lotto/main/DB_Lottery.xlsx"
    try:
        return pd.read_excel(path_excel, sheet_name="DB", usecols="A:I")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# Display data overview
st.subheader("Data Overview")
st.dataframe(df.head())

# Basic statistics
st.subheader("Basic Statistics")
st.write(df.describe())

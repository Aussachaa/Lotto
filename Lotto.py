import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Lottery Data Explorer", layout="wide")

# Title
st.title("Lottery Data Explorer")

# Load data
@st.cache_data  # Use cache to improve performance when reloading data
def load_data():
    path_excel = "https://raw.githubusercontent.com/Aussachaa/Lotto/main/DB_Lottery.xlsx"
    try:
        return pd.read_excel(path_excel, sheet_name="DB", usecols="A:I")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:  # Check if data loading was successful
    # Display data overview
    st.subheader("Data Overview")
    st.dataframe(df.head())  # Display the first 5 rows of data

    # Filter and Frequency Table section
    st.subheader("Lucky Number Frequency")

    # Create a list of Types available in the DataFrame
    types = df.columns.tolist()[1:]  # Exclude 'งวดที่' and 'Date' columns

    # Create filter options for Type (allow multiple selections)
    selected_types = st.multiselect("Select Types:", types, default=types[0])

    # Create filter options for Start Date and End Date (in the same row)
    col1, col2 = st.columns(2)  # Create two columns
    with col1:
        start_date = st.date_input("Start Date:", min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].min())
    with col2:
        end_date = st.date_input("End Date:", min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].max())

    # Filter data based on selected Types and Date range
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                     (df['Date'] <= pd.to_datetime(end_date))]

    # Combine and count the frequency of numbers in the selected columns
    frequency_table = pd.concat([filtered_df[col] for col in selected_types]).value_counts().reset_index()
    frequency_table.columns = ['Number', 'Frequency']

    # Display the frequency table
    st.dataframe(frequency_table,  use_container_width=True)

else:
    st.warning("No data available. Please check the data source or try again later.")

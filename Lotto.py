import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Lottery Data Explorer", layout="wide")

# Title
st.title("🔮 Lottery Data Explorer 🎱")  # Added emojis to the title

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
    # Reorder columns to put 'Date' first
    df = df[['Date'] + [col for col in df.columns if col != 'Date']]

    # Display data overview
    st.subheader("Data Overview 👀")  # Added emoji
    st.dataframe(df.head(), use_container_width=True) 

    # --- Filter Options ---
    st.markdown("---") # Add a horizontal line for visual separation

    # Filter and Frequency Table section
    st.subheader("Lucky Number Frequency 📈")  # Added emoji

    col1, col2 = st.columns(2) 

    with col1:
        combination_choice = st.radio("Select Combination:", ["2-Digit Combination", "3-Digit Combination"])
    with col2:
        if combination_choice == "2-Digit Combination":
            selected_type = st.selectbox("Select Type:", ['All', '2 ตัวบน', '2 ตัวล่าง'], index=0) 
        else:  
            selected_type = st.selectbox("Select Type:", ['All', '3 ตัวบน', '3 ตัวหน้า_1', '3 ตัวหน้า_2', '3 ตัวล่าง_1', '3 ตัวล่าง_2'], index=0) 

    # Filter by Year range
    col3, col4 = st.columns(2)
    with col3:
        start_year = st.number_input("Start Year:", min_value=df['Date'].dt.year.min(), max_value=df['Date'].dt.year.max(), value=df['Date'].dt.year.min())
    with col4:
        end_year = st.number_input("End Year:", min_value=df['Date'].dt.year.min(), max_value=df['Date'].dt.year.max(), value=df['Date'].dt.year.max())

    # Filter by Date range
    col5, col6 = st.columns(2)
    with col5:
        start_date = st.date_input("Start Date:", min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].min())
    with col6:
        end_date = st.date_input("End Date:", min_value=df['Date'].min(), max_value=df['Date'].max(), value=df['Date'].max())

    st.markdown("---") # Add another horizontal line
    # --- End of Filter Options ---

    # Filter data based on selected criteria
    if selected_type == 'All':
        if combination_choice == "2-Digit Combination":
            selected_columns = ['2 ตัวบน', '2 ตัวล่าง']
        else:
            selected_columns = ['3 ตัวบน', '3 ตัวหน้า_1', '3 ตัวหน้า_2', '3 ตัวล่าง_1', '3 ตัวล่าง_2']
        filtered_df = df[(df['Date'].dt.year >= start_year) & 
                         (df['Date'].dt.year <= end_year) &
                         (df['Date'] >= pd.to_datetime(start_date)) & 
                         (df['Date'] <= pd.to_datetime(end_date))][selected_columns]
        frequency_table = pd.concat([filtered_df[col] for col in selected_columns]).value_counts().reset_index()

    else:
        filtered_df = df[(df['Date'].dt.year >= start_year) & 
                         (df['Date'].dt.year <= end_year) &
                         (df['Date'] >= pd.to_datetime(start_date)) & 
                         (df['Date'] <= pd.to_datetime(end_date))][selected_type]
        frequency_table = filtered_df.value_counts().reset_index()

    frequency_table.columns = ['Number', 'Frequency']
    st.dataframe(frequency_table.style.format({'Frequency': '{:,}'}), use_container_width=True)  # Format numbers with commas

else:
    st.warning("No data available. Please check the data source or try again later.")
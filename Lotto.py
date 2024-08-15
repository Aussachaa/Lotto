import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Lottery Data Explorer", layout="wide")

# Title
st.title("Lottery Data Explorer")

# Load data
@st.cache_data  # ใช้ cache เพื่อเพิ่มประสิทธิภาพในการโหลดข้อมูลซ้ำ
def load_data():
    path_excel = "https://raw.githubusercontent.com/Aussachaa/Lotto/main/DB_Lottery.xlsx"
    try:
        return pd.read_excel(path_excel, sheet_name="DB", usecols="A:I")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:  # ตรวจสอบว่าข้อมูลโหลดสำเร็จหรือไม่
    # Display data overview
    st.subheader("Data Overview")
    st.dataframe(df.head())  # แสดง 5 แถวแรกของข้อมูล

    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())  # แสดงสถิติพื้นฐานของข้อมูลตัวเลข

    # ส่วนของ Filter
    st.subheader("Filter and Frequency Table")

    # สร้าง list ของ Type ที่มีอยู่ใน DataFrame
    types = df.columns.tolist()[1:]  # ไม่รวมคอลัมน์ 'งวดที่' และ 'Date'

    # สร้างตัวเลือก filter สำหรับ Type
    selected_type = st.selectbox("Select Type:", types)

    # สร้างตัวเลือก filter สำหรับ Date
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    selected_date_range = st.date_input("Select Date Range:", 
                                        value=(min_date, max_date), 
                                        min_value=min_date, 
                                        max_value=max_date)

    # กรองข้อมูลตาม Type และ Date ที่เลือก
    filtered_df = df[(df['Date'] >= pd.to_datetime(selected_date_range[0])) & 
                     (df['Date'] <= pd.to_datetime(selected_date_range[1]))]

    # นับความถี่ของตัวเลขในคอลัมน์ที่เลือก
    frequency_table = filtered_df[selected_type].value_counts().reset_index()
    frequency_table.columns = ['Number', 'Frequency']

    # แสดงตารางความถี่
    st.dataframe(frequency_table)

else:
    st.warning("No data available. Please check the data source or try again later.")

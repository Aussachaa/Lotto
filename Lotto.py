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

    # เพิ่มเติมส่วนอื่นๆ ตามที่คุณต้องการ เช่น การตรวจผลสลาก การแสดงสถิติเฉพาะ หรือการทำนายผล
else:
    st.warning("No data available. Please check the data source or try again later.")

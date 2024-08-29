import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
from datetime import datetime

CORRECT_PASSWORD = "12345"

# สร้าง Session State เพื่อเก็บสถานะการล็อกอิน
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def check_password():
    """ตรวจสอบรหัสผ่านที่ผู้ใช้ป้อน"""
    if st.session_state.password == CORRECT_PASSWORD:
        st.session_state.logged_in = True
    else:
        st.error("รหัสผ่านไม่ถูกต้อง")

# ส่วนของการล็อกอิน
if not st.session_state.logged_in:
    st.text_input("Password", type="password", key="password", on_change=check_password)
    st.stop()  # หยุดการแสดงผลส่วนอื่นๆ จนกว่าจะล็อกอินสำเร็จ

# ส่วนของเนื้อหาหลัก (จะแสดงเฉพาะเมื่อล็อกอินสำเร็จ)
if st.session_state.logged_in:
    st.set_page_config(page_title="Lottery Data Explorer", layout="wide")
    st.title("🔮 Lottery Data Explorer 🎱") 

    @st.cache_data 
    def load_data():
        path_excel = "https://raw.githubusercontent.com/Aussachaa/Lotto/main/DB_Lottery.xlsx"
        try:
            df = pd.read_excel(path_excel, sheet_name="DB", usecols="A:I", parse_dates=['Date'])
            df = df[['Date'] + [col for col in df.columns if col != 'Date']]
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}. Please check the file path or your internet connection.")
            return None

    df = load_data()

    if df is not None:
        st.subheader("Data Overview 👀") 
        st.dataframe(df.head(10), use_container_width=True) 

        st.markdown("---") 
        st.subheader("Lottery Number Analysis 📈") 

        # เพิ่มส่วนของการแสดงข้อมูลช่วงเวลา
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        st.info(f"Data Range: **{min_date.strftime('%d %B %Y')}** to **{max_date.strftime('%d %B %Y')}**") 

        col1, col2 = st.columns(2) 
        with col1:
            combination_choice = st.radio("Select Combination:", ["2-Digit Combination", "3-Digit Combination"])
        with col2:
            type_options = {
                "2-Digit Combination": ['All', '2 ตัวบน', '2 ตัวล่าง'],
                "3-Digit Combination": ['All', '3 ตัวบน', '3 ตัวหน้า_1', '3 ตัวหน้า_2', '3 ตัวล่าง_1', '3 ตัวล่าง_2']
            }
            selected_type = st.selectbox("Select Type:", type_options[combination_choice], index=0) 

        # ปรับปรุงส่วนของการเลือกช่วงเวลา
        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input("Start Date:", min_value=min_date, max_value=max_date, value=min_date)
        with col4:
            end_date = st.date_input("End Date:", min_value=min_date, max_value=max_date, value=max_date)

        # กรองข้อมูลตามช่วงเวลา
        filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        if selected_type == 'All':
            if combination_choice == "2-Digit Combination":
                selected_columns = ['2 ตัวบน', '2 ตัวล่าง']
            else:
                selected_columns = ['3 ตัวบน', '3 ตัวหน้า_1', '3 ตัวหน้า_2', '3 ตัวล่าง_1', '3 ตัวล่าง_2']
            frequency_table = pd.concat([filtered_df[col] for col in selected_columns]).value_counts().reset_index()
        else:
            frequency_table = filtered_df[selected_type].value_counts().reset_index()

        frequency_table.columns = ['Number', 'Frequency']

        # คำนวณ Probability และ Cumulative probability
        total_frequency = frequency_table['Frequency'].sum()
        frequency_table['Probability'] = frequency_table['Frequency'] / total_frequency * 100
        frequency_table['Cumulative probability'] = frequency_table['Probability'].cumsum()

        # ปรับแต่งตารางด้วย st.dataframe
        st.dataframe(frequency_table.style.format({
            'Frequency': '{:,}', 
            'Probability': '{:.2f}%',
            'Cumulative probability': '{:.2f}%'
        }).highlight_max(subset=['Frequency'], axis=0, color='#B2FEAB'), height=1000, use_container_width=True
        ) 

        # สร้างกราฟ Plotly
        fig = px.bar(frequency_table, x='Number', y='Frequency', 
                     title=f'Frequency of {selected_type} ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})',
                     labels={'Number': 'Number', 'Frequency': 'Frequency'},
                     color='Frequency', color_continuous_scale='Viridis') 
        fig.update_layout(xaxis_tickangle=-45, height=600)
        st.plotly_chart(fig, use_container_width=True) 

        # เพิ่มมุมมองการวิเคราะห์ที่น่าสนใจ
        st.markdown("---")
        st.subheader("Insights 💡")

        # 1. เลขที่ออกบ่อยที่สุด (2 อันดับแรก)
        top_2_numbers = frequency_table.nlargest(2, 'Frequency')
        st.write(f"**Top 2 most frequent {selected_type}:**")
        st.dataframe(top_2_numbers)

        # 2. เลขที่ออกน้อยที่สุด (2 อันดับสุดท้าย)
        bottom_2_numbers = frequency_table.nsmallest(2, 'Frequency')
        st.write(f"**Bottom 2 least frequent {selected_type}:**")
        st.dataframe(bottom_2_numbers)

        # 3. คำนวณช่วงเวลาที่เลขออกติดต่อกันนานที่สุด
        # ... (เพิ่ม logic สำหรับการวิเคราะห์เพิ่มเติม)

    else:
        st.warning("No data available. Please check the data source or try again later.")
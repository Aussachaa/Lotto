import pandas as pd




path_excel = r"C:\Users\aussa\OneDrive\เดสก์ท็อป\Python\Lottery\DB_Lottery.xlsx"
df = pd.read_excel(path_excel, sheet_name="DB", usecols="A:I")
df
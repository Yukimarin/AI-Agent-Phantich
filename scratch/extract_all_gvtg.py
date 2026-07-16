import sys
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx"
xls = pd.ExcelFile(file_path)

# Sheets to process (excluding SKL sheets as requested)
target_sheets = [
    'KS24-JavaAdvance', 'KS24_JavaWeb', 'KS24_JWS', 'KS24_AI',
    'KS25_Javascript', 'KS25_Database', 'KS25_Python', 'KS25_Python_Web',
    'KS25_QTKD_M103', 'KS25_QTKD_M104', 'KS25_QTKD_DTB201', 'KS25_QTKD_DTB202'
]

all_gv_tg = []

for sheet in target_sheets:
    if sheet not in xls.sheet_names:
        continue
    # Read sheet, header starts at row 1 or 2. Let's read it.
    df = pd.read_excel(file_path, sheet_name=sheet)
    
    # We find where the columns are: row with STT, Lớp, Giảng viên/Trợ giảng
    # Let's find it dynamically
    header_idx = None
    for idx, row in df.iterrows():
        row_vals = row.astype(str).tolist()
        if 'Lớp' in row_vals and 'Giảng viên/Trợ giảng' in row_vals:
            header_idx = idx
            break
            
    if header_idx is None:
        print(f"Could not find header row in sheet {sheet}")
        continue
        
    # Read with header row
    df_clean = pd.read_excel(file_path, sheet_name=sheet, skiprows=header_idx + 1)
    
    # Clean columns - find 'Lớp' and 'Giảng viên/Trợ giảng' columns
    class_col = None
    person_col = None
    for col in df_clean.columns:
        col_str = str(col)
        if 'Lớp' in col_str:
            class_col = col
        elif 'Giảng viên/Trợ giảng' in col_str or 'Giảng viên' in col_str or 'Trợ giảng' in col_str:
            person_col = col
            
    if class_col is None or person_col is None:
        print(f"Could not identify columns in sheet {sheet}: Lớp={class_col}, Person={person_col}")
        continue
        
    print(f"\n--- Sheet: {sheet} ---")
    current_class = None
    for idx, row in df_clean.iterrows():
        c_val = row[class_col]
        p_val = row[person_col]
        
        # If class is present, update current class
        if pd.notna(c_val):
            # Sometimes class has STT combined or something. Let's clean it
            current_class = str(c_val).strip()
            
        if pd.notna(p_val) and str(p_val).strip() != '' and str(p_val).strip() != 'nan':
            person_name = str(p_val).strip()
            # Determine role (GV or TG) based on row index relative to the class
            # Usually, the first row of a class is GV, the second row is TG (or we can check their roles)
            all_gv_tg.append({
                'Sheet': sheet,
                'Class': current_class,
                'Name': person_name,
                'RowIdx': idx
            })
            print(f"Class: {current_class} | Name: {person_name}")

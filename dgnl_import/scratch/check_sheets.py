import sys
import openpyxl
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx'
f2 = r'C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx'

wb1 = openpyxl.load_workbook(f1, read_only=True)
wb2 = openpyxl.load_workbook(f2, read_only=True)

print("Sheets in File 1 (cũ):", wb1.sheetnames)
print("Sheets in File 2 (mới):", wb2.sheetnames)

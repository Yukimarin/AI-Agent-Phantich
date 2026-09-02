import sys
import os
import openpyxl
import json
import pandas as pd
import re

sys.stdout.reconfigure(encoding="utf-8")

excel_path = "inputs/Danh sách thi ĐGNL.xlsx" if os.path.exists("inputs/Danh sách thi ĐGNL.xlsx") else r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Loaded excel workbook successfully.")

# Verify sheet names
print("Sheets:", wb.sheetnames)

import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

f1 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"
f2 = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL (1).xlsx"

for sname in ["Danh sách ĐGNL CNTT", "Danh sách ĐGNL QTKD", "Danh sách ĐGNL Kỹ năng mềm"]:
    df1 = pd.read_excel(f1, sheet_name=sname)
    df2 = pd.read_excel(f2, sheet_name=sname)
    print(f"\nSheet {sname}: df1 len={len(df1)}, df2 len={len(df2)}")
    # Check rows in df2 that might be duplicates or null SourceID
    null_ids1 = df1[df1["SourceID"].isna()]
    null_ids2 = df2[df2["SourceID"].isna()]
    print(f"  Null SourceID in df1: {len(null_ids1)}, in df2: {len(null_ids2)}")
    if len(null_ids2) > 0:
        print("  Null SourceID rows in df2:")
        print(null_ids2[["Họ và tên học viên", "Mã lớp hiện tại", "Email học viên"]].dropna(how="all"))
    # Check duplicate SourceIDs
    dup1 = df1[df1["SourceID"].duplicated(keep=False)]
    dup2 = df2[df2["SourceID"].duplicated(keep=False)]
    print(f"  Duplicated SourceIDs in df1: {len(dup1)}, in df2: {len(dup2)}")
    if len(dup2) > len(dup1):
        print("  Newly duplicated SourceIDs:")
        dup_diff = set(dup2["SourceID"]) - set(dup1["SourceID"])
        print(dup2[dup2["SourceID"].isin(dup_diff)][["Họ và tên học viên", "SourceID"]])


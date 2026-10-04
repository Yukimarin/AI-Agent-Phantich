import openpyxl
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\DELL\Downloads\Danh sách thi ĐGNL.xlsx"

if os.path.exists(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=True)
    sheet = wb["Danh sách ĐGNL CNTT"]
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    class_idx = headers.index('Mã lớp hiện tại')
    name_idx = headers.index('Họ và tên học viên')
    sp_idx = headers.index('Sản phẩm (Đ1)')
    vd_idx = headers.index('Vấn đáp (Đ1)')
    th_idx = headers.index('Thực hành (Đ1)')
    tn_idx = headers.index('Trắc nghiệm (Đ1)')
    final_idx = headers.index('Điểm final (Đ1)')
    dgnl_idx = headers.index('Điểm final ĐGNL (Lần 1)')
    
    print("HN-KS24 check:")
    count = 0
    for r in rows[1:]:
        cname = r[class_idx]
        if cname and "HN-KS24" in str(cname):
            sp = r[sp_idx]
            vd = r[vd_idx]
            th = r[th_idx]
            tn = r[tn_idx]
            final = r[final_idx]
            dgnl = r[dgnl_idx]
            
            if final is None or final == 0: continue
            
            # Check PDF formula: (sp_score + vd_score + th_score) / 12
            # sp_score: max 30. If sp in sheet is out of 100, then sp_score = sp * 0.3
            # vd_score: max 20. If vd in sheet is out of 100, then vd_score = vd * 0.2
            # th_score: max 70. If th in sheet is out of 100, then th_score = th * 0.7
            # Sum_score = sp_score + vd_score + th_score = sp * 0.3 + vd * 0.2 + th * 0.7
            # Final_10 = (Sum_score / 120) * 10 = Sum_score / 12
            # Let's compute this:
            sp_val = float(sp) if sp is not None else 0.0
            vd_val = float(vd) if vd is not None else 0.0
            th_val = float(th) if th is not None else 0.0
            tn_val = float(tn) if tn is not None else 0.0
            
            # Formula 1: (sp_val * 0.3 + vd_val * 0.2 + th_val * 0.7) / 12 * 10
            # Wait, PDF says: (Tổng điểm / 120) * 10. Since Tổng điểm is out of 120, and sp_val is out of 100 (graded out of 30, so sp_score = sp_val * 0.3), etc.
            # So: sp_score = sp_val * 0.3, vd_score = vd_val * 0.2, th_score = th_val * 0.7.
            # Then Final = (sp_score + vd_score + th_score) / 12
            # Let's check if this is equal to final!
            sp_score = sp_val * 0.3
            vd_score = vd_val * 0.2
            th_score = th_val * 0.7
            calculated_pdf_final = (sp_score + vd_score + th_score) / 12 * 10 # Wait, (Total / 120) * 10 = Total / 12. Let's see:
            # Wait, if Total is out of 120, then (sp_score + vd_score + th_score) is out of 120. So final = (sp_score + vd_score + th_score) / 12.
            # Let's check what calculated_pdf_final gives:
            f_pdf = (sp_score + vd_score + th_score) / 12.0
            
            # Let's print
            print(f"Name: {r[name_idx]} | Class: {cname}")
            print(f"  Values: sp={sp_val}, vd={vd_val}, th={th_val}, tn={tn_val} | final_excel={final} | dgnl_excel={dgnl}")
            print(f"  Calculated (sp*0.3 + vd*0.2 + th*0.7)/12 = {f_pdf:.2f}")
            
            # Let's also check what if sp is actually out of 100, vd out of 100, th out of 100 and they are weighted by 25%, 17%, 58%:
            # final = sp_val * 0.25 + vd_val * 0.1667 + th_val * 0.5833
            f_weighted = (sp_val * 25 + vd_val * 17 + th_val * 58) / 100.0
            print(f"  Calculated (sp*25 + vd*17 + th*58)/100 = {f_weighted:.2f}")
            
            # What if the columns in sheet are:
            # tn = Trắc nghiệm
            # sp = Sản phẩm
            # vd = Vấn đáp
            # th = Thực hành
            # But the final is: (vd * 30 + th * 14 + tn * 56)/100 = vd*0.3 + th*0.14 + tn*0.56?
            f_least_squares = vd_val * 0.3 + th_val * 0.14 + tn_val * 0.56
            print(f"  Calculated (vd*0.3 + th*0.14 + tn*0.56) = {f_least_squares:.2f}")
            
            count += 1
            if count >= 3:
                break
                
    print("\nHCM-KS24 check:")
    count = 0
    for r in rows[1:]:
        cname = r[class_idx]
        if cname and "HCM-KS24" in str(cname):
            sp = r[sp_idx]
            vd = r[vd_idx]
            th = r[th_idx]
            tn = r[tn_idx]
            final = r[final_idx]
            
            if final is None or final == 0: continue
            
            sp_val = float(sp) if sp is not None else 0.0
            vd_val = float(vd) if vd is not None else 0.0
            th_val = float(th) if th is not None else 0.0
            tn_val = float(tn) if tn is not None else 0.0
            
            # HCM weights: vd_val * 0.4 + th_val * 0.12 + tn_val * 0.48
            f_least_squares_hcm = vd_val * 0.4 + th_val * 0.12 + tn_val * 0.48
            # What if HCM has no Prod, and they only do:
            # (vd * 0.3 + th * 0.7) / 10 * 10? Or (vd * 20 + th * 70)/90 * 10?
            f_hcm_no_sp = (vd_val * 0.2 + th_val * 0.7) / 9.0
            
            print(f"Name: {r[name_idx]} | Class: {cname}")
            print(f"  Values: sp={sp_val}, vd={vd_val}, th={th_val}, tn={tn_val} | final_excel={final}")
            print(f"  Calculated Least Squares (vd*0.4 + th*0.12 + tn*0.48) = {f_least_squares_hcm:.2f}")
            print(f"  Calculated HCM (vd*0.2 + th*0.7)/9 = {f_hcm_no_sp:.2f}")
            
            count += 1
            if count >= 3:
                break
else:
    print("Excel file not found.")

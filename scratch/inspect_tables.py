import docx
import os

doc_path = r"C:\Users\DELL\Downloads\[QTKDS] MẪU BÁO CÁO TỔNG HỢP KẾT QUẢ CÔNG VIỆC HÀNG NGÀY (WORKLANE).docx"
output_path = r"c:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT\scratch\inspect_tables.txt"

def read_docx(path):
    doc = docx.Document(path)
    with open(output_path, "w", encoding="utf-8") as f:
        for t_idx, table in enumerate(doc.tables):
            f.write(f"\n--- TABLE {t_idx} ---\n")
            for r_idx, row in enumerate(table.rows):
                for c_idx, cell in enumerate(row.cells):
                    cell_text = cell.text.strip()
                    if cell_text:
                        f.write(f"Row {r_idx}, Col {c_idx}: {cell_text}\n")
                    else:
                        f.write(f"Row {r_idx}, Col {c_idx}: (EMPTY)\n")

if __name__ == "__main__":
    if os.path.exists(doc_path):
        read_docx(doc_path)
        print("Done")
    else:
        print("File not found")

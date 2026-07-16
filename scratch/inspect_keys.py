import json
import unicodedata

def normalize_name(name):
    name = name.strip()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    name = name.replace(" ", "_").lower()
    return name

with open("data/daily_log_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

monthly_stats = data.get("monthly_stats", {})

target_groups = {
    "Khối QTKD": ["Hoàng Thị Kim Oanh", "Hoàng Thị Hậu", "Lại Trung Lâm", "Đặng Quỳnh Trang", "Nguyễn Thị Hồng Minh", "Nguyễn Ngọc Vân Khanh", "Phạm Tuấn Bình"],
    "Khối CNTT - Cơ sở HN (KS25)": ["Lương Quốc Tuấn", "Lâm Tùng Dương", "Trịnh Quốc Hai", "Ngọ Văn Quý", "Nguyễn Bá Minh Đạo"],
    "Khối CNTT - Cơ sở HN (KS24)": ["Lê Thành Ngọc", "Phạm Viết Hùng", "Bùi Thanh Hải", "Trần Quốc Tuấn"],
    "Khối CNTT - Cơ sở HCM": ["Lê Hà Thanh Sang", "Phạm Ngọc Kiên", "Nguyễn Quảng An"],
    "Khối Ngoại ngữ - Kỹ năng mềm": ["Giáp Thị Minh Hằng", "Lò Thị Ngọc Anh", "Lê Thị Đỏ", "Ngô Quang Huấn"],
    "Khối Quản lý Đào tạo (QLĐT)": ["Nguyễn Thị Tươi", "Trần Thị Mỹ Phước", "Nguyễn Huyền Trang", "Nguyễn Xuân Bách"]
}

with open("scratch/inspect_keys.txt", "w", encoding="utf-8") as out:
    out.write("Sample monthly_stats keys:\n")
    for k in list(monthly_stats.keys()):
        out.write(f"{repr(k)}\n")
        
    out.write("\nSample normalized target names:\n")
    for group, names in target_groups.items():
        for name in names:
            out.write(f"{name} -> {repr(normalize_name(name))}\n")

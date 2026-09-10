# Báo cáo Đánh giá KPI GV/TG Học kỳ (PTITxRikkei Joint Venture)

> [!NOTE]
> Báo cáo này được tổng hợp và phân tích tự động từ các nguồn dữ liệu thực tế: Chỉ số vi phạm lớp học (`PTIT_Chiso.xlsx`), Báo cáo công việc (`daily_logs.txt`), Cơ sở dữ liệu học tập (`qldt.sql`), Tài liệu quy định (`quy_dinh.md`) và Nhật ký đào tạo tuần (`11.04.txt`).

> [!WARNING]
> **CẢNH BÁO BIẾN ĐỘNG SĨ SỐ LỚP HỌC (CLASS SIZE ALERTS):**
> Phát hiện có sự thay đổi sĩ số trong các lớp học mới cập nhật. Cần đặc biệt lưu ý khi đối chiếu tỷ lệ vi phạm:
> - ⚠️ **HN-K24-CNTT1(41-39)** (Môn: `KS24_JavaWeb`): Sĩ số thay đổi từ **41** ➔ **39** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT2(40-39)** (Môn: `KS24_JavaWeb`): Sĩ số thay đổi từ **40** ➔ **39** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT3(32-25)** (Môn: `KS24_JavaWeb`): Sĩ số thay đổi từ **32** ➔ **25** học viên (Biến động: **-7 SV**)
> - ⚠️ **HN-K24-CNTT4(38-34)** (Môn: `KS24_JavaWeb`): Sĩ số thay đổi từ **38** ➔ **34** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K24-CNTT5(29-19)** (Môn: `KS24_JavaWeb`): Sĩ số thay đổi từ **29** ➔ **19** học viên (Biến động: **-10 SV**)
> - ⚠️ **HN-K24-CNTT1(38)** (Môn: `KS24_JWS`): Sĩ số thay đổi từ **39** ➔ **38** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT3(48-43-42)** (Môn: `KS24_JWS`): Sĩ số thay đổi từ **48** ➔ **42** học viên (Biến động: **-6 SV**)
> - ⚠️ **HN-K24-CNTT3(48-43-42)** (Môn: `KS24_JWS`): Sĩ số thay đổi từ **25** ➔ **42** học viên (Biến động: **+17 SV**)
> - ⚠️ **HN-K24-CNTT1(38-36)** (Môn: `KS24_AI`): Sĩ số thay đổi từ **38** ➔ **36** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT1(38-36)** (Môn: `KS24_AI`): Sĩ số thay đổi từ **38** ➔ **36** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT4(34-32)** (Môn: `KS24_AI`): Sĩ số thay đổi từ **34** ➔ **32** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT4(34-32)** (Môn: `KS24_AI`): Sĩ số thay đổi từ **34** ➔ **32** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT1(36-33)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **36** ➔ **33** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K24-CNTT1(36-33)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **36** ➔ **33** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K24-CNTT3(42-41)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **42** ➔ **41** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT3(42-41)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **42** ➔ **41** học viên (Biến động: **-1 SV**)
> - ⚠️ **HCM-K24-CNTT1(44-43)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **44** ➔ **43** học viên (Biến động: **-1 SV**)
> - ⚠️ **HCM-K24-CNTT1(44-43)** (Môn: `KS24_AI_Intergration`): Sĩ số thay đổi từ **44** ➔ **43** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT1(35-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **35** ➔ **31** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K24-CNTT1(35-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **33** ➔ **31** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT3(42)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **41** ➔ **42** học viên (Biến động: **+1 SV**)
> - ⚠️ **HN-K24-CNTT4(32-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT4(32-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT1(47-44)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **47** ➔ **44** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K25-CNTT3(40-39)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **40** ➔ **39** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT4(47-43)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **47** ➔ **43** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K25-CNTT6(38-35)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **38** ➔ **35** học viên (Biến động: **-3 SV**)
> - ⚠️ **HCM-K25-CNTT5(43-39)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **43** ➔ **39** học viên (Biến động: **-4 SV**)
> - ⚠️ **HCM-K25-CNTT6(47-41)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **47** ➔ **41** học viên (Biến động: **-6 SV**)
> - ⚠️ **HCM-K25-CNTT7(43-42)** (Môn: `KS25_Database`): Sĩ số thay đổi từ **43** ➔ **42** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT1(44-42)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **44** ➔ **42** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT1(44-42)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **44** ➔ **42** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT3(40-39-37)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **40** ➔ **37** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K25-CNTT3(40-39-37)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **39** ➔ **37** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT4(44-43-42)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **44** ➔ **42** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT4(44-43-42)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **43** ➔ **42** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT5(43-40-42)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **43** ➔ **42** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT6(35-33)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **35** ➔ **33** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT6(35-33)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **35** ➔ **33** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT8(23-24)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **23** ➔ **24** học viên (Biến động: **+1 SV**)
> - ⚠️ **HN-K25-CNTT8(23-24)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **18** ➔ **24** học viên (Biến động: **+6 SV**)
> - ⚠️ **HCM-K25-CNTT8(38)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **39** ➔ **38** học viên (Biến động: **-1 SV**)
> - ⚠️ **HCM-K25-CNTT6(41-40)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **41** ➔ **40** học viên (Biến động: **-1 SV**)
> - ⚠️ **HCM-K25-CNTT6(41-40)** (Môn: `KS25_Python`): Sĩ số thay đổi từ **41** ➔ **40** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT1(40)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **42** ➔ **40** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT2(38)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **43** ➔ **38** học viên (Biến động: **-5 SV**)
> - ⚠️ **HN-K25-CNTT3(35)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **37** ➔ **35** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT4(41-40)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **41** ➔ **40** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT4(41-40)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **42** ➔ **40** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT5(37)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **42** ➔ **37** học viên (Biến động: **-5 SV**)
> - ⚠️ **HN-K25-CNTT6(32-31)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-CNTT6(32-31)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **33** ➔ **31** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT8(22)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **24** ➔ **22** học viên (Biến động: **-2 SV**)
> - ⚠️ **HCM-K25-CNTT8(36)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **38** ➔ **36** học viên (Biến động: **-2 SV**)
> - ⚠️ **HCM-K25-CNTT7(40-39)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **40** ➔ **39** học viên (Biến động: **-1 SV**)
> - ⚠️ **HCM-K25-CNTT7(40-39)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **42** ➔ **39** học viên (Biến động: **-3 SV**)
> - ⚠️ **HCM-K25-CNTT5(37)** (Môn: `KS25_Python_Web`): Sĩ số thay đổi từ **39** ➔ **37** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT1(41)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **41** học viên (Biến động: **+1 SV**)
> - ⚠️ **HN-K25-CNTT2(41)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **38** ➔ **41** học viên (Biến động: **+3 SV**)
> - ⚠️ **HN-K25-CNTT3(43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **35** ➔ **43** học viên (Biến động: **+8 SV**)
> - ⚠️ **HN-K25-CNTT4(38)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **38** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT5(41)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **37** ➔ **41** học viên (Biến động: **+4 SV**)
> - ⚠️ **HCM-K25-CNTT8(36-33-32)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **36** ➔ **32** học viên (Biến động: **-4 SV**)
> - ⚠️ **HCM-K25-CNTT8(36-33-32)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **36** ➔ **32** học viên (Biến động: **-4 SV**)
> - ⚠️ **HCM-K25-CNTT7(39-46)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **39** ➔ **46** học viên (Biến động: **+7 SV**)
> - ⚠️ **HCM-K25-CNTT7(39-46)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **39** ➔ **46** học viên (Biến động: **+7 SV**)
> - ⚠️ **HCM-K25-CNTT6(38-37-47)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **38** ➔ **47** học viên (Biến động: **+9 SV**)
> - ⚠️ **HCM-K25-CNTT6(38-37-47)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **47** học viên (Biến động: **+7 SV**)
> - ⚠️ **HCM-K25-CNTT5(39-44)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **39** ➔ **44** học viên (Biến động: **+5 SV**)
> - ⚠️ **HCM-K25-CNTT5(39-44)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **37** ➔ **44** học viên (Biến động: **+7 SV**)
> - ⚠️ **HN-K25-QTKD1(37-33)** (Môn: `KS25_QTKD_DTB202`): Sĩ số thay đổi từ **37** ➔ **33** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K25-QTKD1(37-33)** (Môn: `KS25_QTKD_DTB202`): Sĩ số thay đổi từ **37** ➔ **33** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K25-QTKD1(21-11-1)** (Môn: `KS25_QTKD_PRJ302`): Sĩ số thay đổi từ **21** ➔ **1** học viên (Biến động: **-20 SV**)
> - ⚠️ **HN-K25-QTKD1(21-11-1)** (Môn: `KS25_QTKD_PRJ302`): Sĩ số thay đổi từ **33** ➔ **1** học viên (Biến động: **-32 SV**)
> - ⚠️ **HN-K25-QTKD3(26)** (Môn: `KS25_QTKD_PRJ302`): Sĩ số thay đổi từ **27** ➔ **26** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-QTKD1(33)** (Môn: `KS25_QTKD_BA201`): Sĩ số thay đổi từ **1** ➔ **33** học viên (Biến động: **+32 SV**)
> - ⚠️ **HN-K25-QTKD2(40-39)** (Môn: `KS25_QTKD_BA201`): Sĩ số thay đổi từ **40** ➔ **39** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-QTKD2(40-39)** (Môn: `KS25_QTKD_BA201`): Sĩ số thay đổi từ **40** ➔ **39** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K25-QTKD3(28-26)** (Môn: `KS25_QTKD_BA201`): Sĩ số thay đổi từ **28** ➔ **26** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-QTKD1(46)** (Môn: `KS25_QTKD_MAN107`): Sĩ số thay đổi từ **33** ➔ **46** học viên (Biến động: **+13 SV**)
> - ⚠️ **HN-K25-QTKD2(42)** (Môn: `KS25_QTKD_MAN107`): Sĩ số thay đổi từ **39** ➔ **42** học viên (Biến động: **+3 SV**)
> - ⚠️ **HN-K25-QTKD (Tái cơ cấu)** (Môn: `KS25_QTKD_MAN107`): Sĩ số thay đổi từ **3** ➔ **2** học viên (Biến động: **-1 SV**)


## 1. Bảng tổng hợp đánh giá KPI theo Phòng ban

### 1.1. Khối CNTT

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Phạm Ngọc Kiên** | Trợ giảng |  | 100.0 | 100.0 | 90.8 | **97.24** |
| **Phan Ngọc Tài** | Trợ giảng thử việc |  | 100.0 | 100.0 | 89.8 | **96.94** |
| **Nguyễn Công Hưởng** | Giảng viên |  | 100.0 | 100.0 | 89.1 | **96.73** |
| **Nguyễn Ngọc Sơn** | Trợ giảng thử việc |  | 100.0 | 100.0 | 87.2 | **96.16** |
| **Đinh Thành Nam** | Trợ giảng |  | 100.0 | 100.0 | 86.6 | **95.98** |
| **Ngọ Văn Quý** | Giảng viên |  | 100.0 | 100.0 | 85.0 | **95.50** |
| **Nguyễn Đức Minh** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT7|HCM-K25-CNTT7(39-46) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT5|HCM-K25-CNTT5(39-44) (KS25_Phantichthietkehethong)]] | 97.5 | 94.9 | 92.2 | **95.11** |
| **Mai Xuân Chinh** | Trợ giảng |  | 100.0 | 100.0 | 83.5 | **95.05** |
| **Lương Quốc Tuấn** | Giảng viên |  | 100.0 | 100.0 | 77.8 | **93.34** |
| **Lại Trung Lâm** | Trợ giảng |  | 100.0 | 100.0 | 77.7 | **93.31** |
| **Lê Hà Thanh Sang** | Giảng viên |  | 100.0 | 100.0 | 77.6 | **93.28** |
| **Trịnh Quốc Hai** | Giảng viên |  | 100.0 | 100.0 | 76.8 | **93.04** |
| **Đặng Minh Luân** | Trợ giảng thử việc |  | 100.0 | 100.0 | 76.5 | **92.95** |
| **Phạm Viết Hùng** | Trợ giảng |  | 95.0 | 100.0 | 82.6 | **92.78** |
| **Lâm Tùng Dương** | Giảng viên |  | 100.0 | 100.0 | 75.4 | **92.62** |
| **Phạm Tuấn Bình** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT3|HN-K25-CNTT3(43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT4|HN-K25-CNTT4(38) (KS25_Phantichthietkehethong)]] | 91.5 | 98.0 | 81.3 | **90.38** |
| **Bùi Thanh Hải** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT1|HN-K24-CNTT1(35-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT4|HN-K24-CNTT4(32-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT2|HN-K24-CNTT2(39) (KS24_AI_Microservice)]] | 97.3 | 94.6 | 74.4 | **89.61** |
| **Lưu Hoàng Xuân Nguyên** | Trợ giảng |  | 92.5 | 100.0 | 73.3 | **88.99** |
| **Trần Minh Cường** | Leader |  | 100.0 | 100.0 | 62.3 | **88.69** |
| **Trần Quốc Tuấn** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT8|HCM-K25-CNTT8(36-33-32) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT6|HCM-K25-CNTT6(38-37-47) (KS25_Phantichthietkehethong)]] | 94.2 | 88.4 | 81.4 | **88.63** |
| **Nguyễn Quảng An** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT5|HN-K25-CNTT5(41) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT1|HN-K25-CNTT1(41) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT2|HN-K25-CNTT2(41) (KS25_Phantichthietkehethong)]] | 90.9 | 96.7 | 71.6 | **86.84** |
| **Hồ Xuân Hùng** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT3|HN-K24-CNTT3(42) (KS24_AI_Microservice)]] | 95.7 | 91.4 | 59.5 | **83.57** |
| **Nguyễn Bá Minh Đạo** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS24-CNTT1|HCM-K24-CNTT1(43) (KS24_AI_Microservice)]] | 83.9 | 97.9 | 64.7 | **82.34** |

### 1.2. Khối QTKD

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Hoàng Thị Hậu** | Giảng viên |  | 100.0 | 100.0 | 97.3 | **99.19** |
| **Hoàng Thị Kim Oanh** | Leader |  | 100.0 | 100.0 | 94.1 | **98.23** |
| **Nguyễn Thị Như Quỳnh** | Trợ giảng |  | 100.0 | 100.0 | 94.0 | **98.20** |
| **Lê Nhựt Mi** | Giảng viên |  | 100.0 | 100.0 | 93.5 | **98.05** |
| **Nguyễn Thị Hồng Minh** | Giảng viên |  | 100.0 | 100.0 | 92.8 | **97.84** |
| **Triệu Thị Thanh Tâm** | Trợ giảng |  | 100.0 | 100.0 | 92.4 | **97.72** |
| **Lê Thị Bảo Yến** | Trợ giảng |  | 100.0 | 100.0 | 88.8 | **96.64** |
| **Nguyễn Ngọc Vân Khanh** | Giảng viên |  | 100.0 | 100.0 | 86.8 | **96.04** |
| **Lê Thành Ngọc** | Giảng viên |  | 100.0 | 100.0 | 82.3 | **94.69** |
| **Đặng Quỳnh Trang** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD1|HN-K25-QTKD1(46) (KS25_QTKD_MAN107)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD2|HN-K25-QTKD2(42) (KS25_QTKD_MAN107)]] | 93.2 | 96.4 | 84.6 | **91.57** |

### 1.3. Khối Ngoại ngữ và kỹ năng mềm

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Lê Thị Đỏ** | Giảng viên |  | 100.0 | 100.0 | 94.5 | **98.35** |
| **Giáp Thị Minh Hằng** | Leader |  | 100.0 | 100.0 | 89.1 | **96.73** |
| **Lò Thị Ngọc Anh** | Giảng viên |  | 100.0 | 100.0 | 84.4 | **95.32** |
| **Ngô Quang Huấn** | Giảng viên |  | 100.0 | 100.0 | 72.1 | **91.63** |

### 1.4. Khối QLCLĐT

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Trần Thị Mỹ Phước** | Giáo vụ |  | 100.0 | 100.0 | 99.8 | **99.94** |
| **Nguyễn Xuân Bách** | Giảng viên |  | 100.0 | 100.0 | 92.3 | **97.69** |
| **Nguyễn Huyền Trang** | Giáo vụ |  | 100.0 | 100.0 | 84.3 | **95.29** |
| **Nguyễn Thị Tươi** | Leader |  | 100.0 | 100.0 | 66.3 | **89.89** |


---

## 2. Đánh giá chi tiết từng cá nhân

### 🔹 Chi tiết nhân sự Khối CNTT

#### Trợ giảng thử việc. Phan Ngọc Tài
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.94** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 89.8)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Có task chậm trễ/tồn đọng: HCM-KS25-CNTT8 - IT-215 - Session11: Dự giờ thực hành (0%), HCM-KS25-CNTT8 - IT-215 - Session10: Chấm bài tập về nhà. (0%), HCM-KS25-CNTT5 - IT-215 - Session10, 11: Chấm bài tập về nhà. (0%); Khai báo vượt định mức KPI Master: 06/07: Task 'HCM-KS25-CNTT8 - IT-215 - Session9: Dự giờ tiết thực hành - Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 06/07: Task 'HCM-KS25-CNTT5 - IT215 - Session9: Dự giờ tiết thực hành - Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'HCM-KS25-CNTT8 - IT215 : Hỗ trợ kiểm tra tiến độ project cuối môn' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'HCM-KS25-CNTT8 - IT-215 - Session4: Chấm bài tập về nhà.' chưa định dạng (gán tạm 30 phút); Task 'HCM-KS25-CNTT5 - IT-215 - Session4: Chấm bài tập về nhà.' chưa định dạng (gán tạm 30 phút); Task 'HCM-KS25-CNTT8 - IT-215 - Session4, 5: Dự giờ lớp lý thuyết.' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Công Hưởng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.73** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 89.1)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 03/07, 16/07, 24/07, 27/07, 21/08); Có task chậm trễ/tồn đọng: Chấm bài thi cuối môn AI Application lớp K24-CNTT2 (25%); Khai báo vượt định mức KPI Master: 07/07: Task 'Triển khai buổi 1 project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 08/07: Task 'Triển Khai buổi 2 project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task 'Triển khai buổi 3 Project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Chấm bảo vệ lớp K24-HCM-K24-CNTT1 môn Java Web Service' chưa định dạng (gán tạm 30 phút); Task 'Triển khai buổi thực hành session 12 môn AI Application K24-CNTT1' chưa định dạng (gán tạm 30 phút); Task 'chấm bài tập JB-IOC-PTHB251125 ,JB-IOC-PTHB260310,JB-IOC-PTHB260407' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng thử việc. Nguyễn Ngọc Sơn
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.16** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 87.2)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 17/07, 24/08); Có task chậm trễ/tồn đọng: 2. Nhận tài khoản pm kiểm tra và sử dụng ứng dụng pm với việc báo cáo task(9h00-10h00) (75%), KS25TICH-23 S02 - L03: Bài đọc (80%), KS25TICH-17 S02 - L02: Bài đọc (90%); Khai báo vượt định mức KPI Master: 06/07: Task '4. Chuẩn bị bài thực hành, và xem lại bài cũ ngày 07/07/2026 demo đứng lớp thực hành (1h00- 4h00)' khai báo 3.5h so với định mức tiêu chuẩn 0.8h; 09/07: Task 'Review lại phần chấm homework - up học liệu - chăm sóc sinh viên của lớp HCM-KS25-CNTT7_HK2, HCM-KS25-CNTT8_HK2' khai báo 1.5h so với định mức tiêu chuẩn 0.4h; 03/08: Task 'Thực hiện sửa và review lại học liệu môn PTTK theo feedback từ session02 - session07' khai báo 6.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task '1. Tham gia dự giờ lớp HCM-KS25-CNTT7  (7H00 - 9H00) link: https://tgu698gf9yo.sg.larksuite.com/docx/QVJtdp1LJotYz1xDMNflghkUglg' chưa định dạng (gán tạm 30 phút); Task '2. Nhận tài khoản pm kiểm tra và sử dụng ứng dụng pm với việc báo cáo task(9h00-10h00)' chưa định dạng (gán tạm 30 phút); Task 'Họp một số luu ý đầu tuân (10h00-11h30) link: https://tgu698gf9yo.sg.larksuite.com/docx/EU8SdEa0BoClMtxumculA7jXgBb' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Đinh Thành Nam
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.98** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 86.6)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 07/07, 08/07, 31/07, 06/08, 13/08, 18/08, 20/08); Khai báo vượt định mức KPI Master: 01/07: Task 'Triển khai mẫu SRS môn project trước kì nghỉ cho sinh viên k24' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 27/07: Task '[Sem 3 Review Exam] Chuẩn bị câu hỏi phỏng vấn và ôn tập' khai báo 3.0h so với định mức tiêu chuẩn 0.4h; 03/08: Task '[Review session 9] PTIT K24 Devops' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Hỗ trợ mentee' chưa định dạng (gán tạm 30 phút); Task '[Java Backend Devops] Nghiên cứu và triển khai github action thay cho gitlab ci' chưa định dạng (gán tạm 30 phút); Task '[Giám sát thi] K25 CNTT8 Thi cuối môn' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Ngọ Văn Quý
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.50** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 85.0)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 14/07, 17/07, 22/07, 23/07, 24/07, 27/07, 14/08); Khai báo vượt định mức KPI Master: 20/08: Task 'Họp review AI agent với bên Quản trị kinh doanh' khai báo 1.5h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Trông thi hackathon lớp CNTT 3' chưa định dạng (gán tạm 30 phút); Task 'Trông thi hackathon lớp CNTT 5' chưa định dạng (gán tạm 30 phút); Task 'Quay video + popup Session 16 - Lesson 01' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Đức Minh
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT7|HCM-K25-CNTT7(39-46) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT5|HCM-K25-CNTT5(39-44) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **95.11** (Kỷ luật: 97.5, Học tập: 94.9, Báo cáo ngày: 92.2)
- **Điểm mạnh**:
  - Khởi đầu xuất sắc môn mới Phân tích thiết kế hệ thống tại cả 2 lớp HCM-K25-CNTT5 (0.0% vi phạm tuyệt đối) và HCM-K25-CNTT7 (chỉ 0.85% vi phạm).
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không ghi nhận vi phạm nề nếp nghiêm trọng. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (07/07, 19/08, 26/08); Khai báo vượt định mức KPI Master: 02/07: Task 'Cấu hình và hiệu chỉnh AI Agent review backlog và sprint progress' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 06/07: Task 'Cải thiện AI Agent quản lý tiến độ project' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 14/07: Task 'Cải tiến AI Agent quản lý giám sát tiến độ mini project' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Kiểm tra tiến độ dự án ngày 4 lớp HCM KS24 CNTT1 môn java web service' chưa định dạng (gán tạm 30 phút); Task 'Chốt tiến độ các dự án lớp HCM KS24 CNTT1' chưa định dạng (gán tạm 30 phút); Task 'Tham gia buổi giảng demo của Thầy Phạm Viết Hùng' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Duy trì phong độ kiểm soát lớp học và nề nếp sinh viên hoàn hảo xuyên suốt toàn bộ môn học. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Mai Xuân Chinh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.05** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 83.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 07/07, 09/07, 15/07, 27/07, 30/07, 06/08, 13/08); Có task chậm trễ/tồn đọng: TRIEKHAI-22 Hỗ trợ SV làm dự án — CNTT2 (UNVERIFIED), TRIEKHAI-24 Hỗ trợ SV làm dự án — CNTT3 (UNVERIFIED), TRIEKHAI-18 Hỗ trợ SV làm dự án — CNTT4 (UNVERIFIED); Khai báo vượt định mức KPI Master: 21/07: Task 'Chấm bài Project cho sinh viên' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 28/07: Task 'Chấm bài project K24' khai báo 8.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'PTITTRIE-60 [Trông thi] IT212 K24 (HN-KS24-CNTT2)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-49 [Buổi 10] Check BTVN — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-41 [Buổi 08] Check BTVN — IT212 K24 (HN-KS24-CNTT3)' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lương Quốc Tuấn
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.34** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 77.8)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 06/07, 08/07, 09/07, 10/07, 16/07, 20/07, 27/07, 31/07, 04/08, 07/08, 13/08, 14/08, 28/08); Có task chậm trễ/tồn đọng: Chấm Bài Thi CNTT3 (30%); Khai báo vượt định mức KPI Master: 07/07: Task 'Chấm mini Project Lớp CNTT 1' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'Chấm mini Project Lớp CNTT5' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Chấm miniproject CNTT1' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Dạy CNTT1 KS25' chưa định dạng (gán tạm 30 phút); Task 'Dạy CNTT5 2 ca' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc sinh viên các bạn yếu' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lại Trung Lâm
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.31** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 77.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 09/07, 10/07, 20/07, 31/07, 06/08); Có task chậm trễ/tồn đọng: giảng dạy thực hành lớp CNTT1 SS6 (UNVERIFIED), giảng dạy thực hành lớp CNTT5 SS6 (UNVERIFIED), chuẩn bị cho môn k26( lesson 1) quizz + bài đọc+ câu hỏi tự luận (0%); Khai báo vượt định mức KPI Master: 01/07: Task 'CHUẨN BỊ BÀI DẠY TIẾT THỰC HÀNH SS6' khai báo 1.5h so với định mức tiêu chuẩn 0.8h; 03/07: Task 'chuẩn bị bài thực hành SS8' khai báo 2.0h so với định mức tiêu chuẩn 0.8h; 06/07: Task 'chấm mini project lớp CNTT5 session 9' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'giảng dạy thực hành lớp CNTT1 SS6' chưa định dạng (gán tạm 30 phút); UNVERIFIED: Task 'giảng dạy thực hành lớp CNTT1 SS6' khai báo xong nhưng trên Worklane chưa DONE.; Task 'giảng dạy thực hành lớp CNTT5 SS6' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lê Hà Thanh Sang
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.28** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 77.6)
- **Điểm mạnh**:
  - Quản lý giảng dạy hiệu quả 7 lớp học khối KS25, chỉ số vi phạm học tập ở mức thấp (trung bình 13.25%).
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không có vi phạm nghiêm trọng nào ghi nhận. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 03/07, 06/07, 16/07, 20/07, 22/07, 17/08, 19/08, 28/08); Khai báo vượt định mức KPI Master: 13/08: Task 'Triển khai miniproject lớp HCM-KS25-CNTT8' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 13/08: Task 'Triển khai miniproject lớp HCM-KS25-CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Triển khai thực hiện final project lớp HCM-KS25-CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Cập nhật tính năng của AI Agent' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc, quản lý chỉ số sinh viên' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy thực hành lớp HCM-KS25-CNTT5' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Tiếp tục phát huy phong cách quản lý lớp học tích cực. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Trịnh Quốc Hai
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.04** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 76.8)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 14/07, 17/07, 21/07, 30/07, 14/08, 21/08); Khai báo vượt định mức KPI Master: 09/07: Task 'review chấm bài, nhận xét bài tập các lớp, kiểm tra nhóm yếu, tài nguyên học tập' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 10/07: Task 'review lại 16 đề thi hackthon' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; 13/07: Task 'review tài nguyên session 16 lập trình ứng dụng web với fastAPI' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'ra 16 đề thi  hackathon môn fastapi' chưa định dạng (gán tạm 30 phút); Task 'ra bài tập ôn tập cho các lớp chuẩn bị ôn tập thi hackathon' chưa định dạng (gán tạm 30 phút); Task 'dạy thực hành session 13 CNTT2' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng thử việc. Đặng Minh Luân
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **92.95** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 76.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (03/07); Có task chậm trễ/tồn đọng: Chấm bài tập nhóm CNTT7 (70%), Làm  thử đề ôn tập giữa kỳ FastApi (70%), Tìm đọc tài liệu về Agile Scrum  chuẩn bị làm học liệu cho môn Phát triển phần mềm với Agile Scrum (30%); Khai báo vượt định mức KPI Master: 06/07: Task 'Tham gia buổi dạy môn [IT-215] S8 - Mini Project lớp HCM-KS25-CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'Review lại kết quả nhận xét AI chấm BTVN HCM-KS25-CNTT7 - S9' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 07/07: Task 'Review lại kết quả nhận xét AI chấm BTVN HCM-KS25-CNTT6 - S9' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Xem học liệu IT-215 S6 chuẩn bị demo lớp thực hành' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị nội dung cho demo lớp thực hành' chưa định dạng (gán tạm 30 phút); Task 'Tham gia buổi demo dạy lý thuyết thầy Hùng môn Java: Session 9: Kế thừa & đa hình' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Phạm Viết Hùng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **92.78** (Kỷ luật: 95.0, Học tập: 100.0, Báo cáo ngày: 82.6)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 06/07, 07/07, 08/07, 17/07, 10/08, 21/08); Khai báo vượt định mức KPI Master: 03/07: Task 'Chuẩn bị thực hành bài tập + Triển khai thực hành bài tập KS25' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 09/07: Task 'Tham gia hỗ trợ chuẩn bị thực hành và triển khai thực hành ss13 cho thầy Tài demo KS25-CNTT8' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 15/07: Task 'Chuẩn bị thực hành + Triển khai thực hành CNTT8 SS17' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; Có task lạ chưa có định mức: Task 'Tham gia buổi dạy Demo thầy Tài HCM' chưa định dạng (gán tạm 30 phút); Task 'Hỗ training phần ktbt + làm việc nhóm + raia cho thầy trợ giảng' chưa định dạng (gán tạm 30 phút); Task 'Chấm btvn và kiểm tra hoạt động nhóm KS25 và KS24' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lâm Tùng Dương
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **92.62** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 75.4)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 20/07, 23/07); Có task chậm trễ/tồn đọng: Sản xuất session 14 (25%), KS26NANG-133 S08: Mindmap (UNVERIFIED), KS26NANG-125 S08 - L02: Quiz (UNVERIFIED); Khai báo vượt định mức KPI Master: 30/07: Task 'Review tiến độ sinh viên CNTT2 giai đoạn hè' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 31/07: Task 'Review Kiến thức lớp CNTT2-KS25' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 03/08: Task 'Review kiến thức hè sinh viên' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'SANXUAT-28 bài đọc session 10' chưa định dạng (gán tạm 30 phút); Task 'Phát triển AI Agent' chưa định dạng (gán tạm 30 phút); Task 'Làm checkpoint' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Phạm Tuấn Bình
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT3|HN-K25-CNTT3(43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT4|HN-K25-CNTT4(38) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **90.38** (Kỷ luật: 91.5, Học tập: 98.0, Báo cáo ngày: 81.3)
- **Điểm mạnh**:
  - Đảm nhiệm giảng dạy các lớp CNTT3 và CNTT5 khối KS24.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Tỷ lệ chuyên cần và bài tập về nhà của sinh viên ở mức báo động 2 (sinh viên có nền tảng yếu). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (03/07, 28/08); Có task chậm trễ/tồn đọng: [Chấm thi] - AI Application In Action - HN-KS24-CNTT1 (0%), [Nguyên cứu] - Hyperframes - Sử dụng như nào và tích hợp vào như nào (0%), [Chấm thi] - Exam Hackaathon - HN-KS24-CNTT3 - AI Application (30%); Khai báo vượt định mức KPI Master: 02/07: Task '[Chấm thi sản phẩm] - Project - Java Web Service' khai báo 4.0h so với định mức tiêu chuẩn 0.5h; 10/07: Task '[Chấm project IOC] Chấm project' khai báo 8.0h so với định mức tiêu chuẩn 0.5h; 03/08: Task '[Học liệu] - Làm SRS Project cho hệ BE IOC - 2 đề tài' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task '[Microservice] - Làm slide - session 02' chưa định dạng (gán tạm 30 phút); Task '[Chấm thi] - AI Application In Action - HN-KS24-CNTT1' chưa định dạng (gán tạm 30 phút); Task '[Nguyên cứu] - Hyperframes - Sử dụng như nào và tích hợp vào như nào' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phối hợp với phòng CTSV kéo sinh viên quay lại và triển khai các buổi hỗ trợ kiến thức nền tảng. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Bùi Thanh Hải
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT1|HN-K24-CNTT1(35-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT4|HN-K24-CNTT4(32-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT2|HN-K24-CNTT2(39) (KS24_AI_Microservice)]]
- **Điểm KPI tổng**: **89.61** (Kỷ luật: 97.3, Học tập: 94.6, Báo cáo ngày: 74.4)
- **Điểm mạnh**:
  - Duy trì tỷ lệ vi phạm của lớp ở mức rất thấp (trung bình chỉ 12.02%). Quản lý tốt 10 lớp học khối KS24.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Một số sinh viên ở gần mức cảnh báo chuyên cần tại lớp CNTT4. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (20/07, 21/07, 22/07, 23/07, 24/07, 17/08); Khai báo vượt định mức KPI Master: 06/07: Task 'Triển khai thực hành Example Project Holiday - HN-K24-CNTT4 - Buổi 1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'Triển khai Example Project Holiday - HN-K24-CNTT4 - Buổi 2' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task '✓ TRIEKHAI- Project Example Holiday - HN-K24-CNTT3 - Buổi 1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'PTITTRIE-6 [Buổi 11] Giảng LT — IT212 K24 (HN-KS24-CNTT2)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-6 [Buổi 10] Giảng LT — IT212 K24 (HN-KS24-CNTT3)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-6 [Buổi 12] Giảng LT — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Cần làm việc sát sao hơn và thường xuyên thông báo tỷ lệ chuyên cần cho sinh viên. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lưu Hoàng Xuân Nguyên
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **88.99** (Kỷ luật: 92.5, Học tập: 100.0, Báo cáo ngày: 73.3)
- **Điểm mạnh**:
  - Nhiệt tình hỗ trợ giảng viên và giải đáp thắc mắc của sinh viên.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Chưa sát sao và tập trung trong việc kiểm tra bài tập và bài tập bổ sung cho sinh viên lớp HCM-CNTT2. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 07/07, 08/07, 13/07, 17/07, 20/07, 21/07, 29/07, 31/07, 05/08, 07/08, 11/08, 12/08, 13/08, 20/08, 21/08, 28/08); Khai báo vượt định mức KPI Master: 09/07: Task 'Triển khai thực hành CNTT' khai báo 4.0h so với định mức tiêu chuẩn 2.0h; 04/08: Task 'KS25-175 S11: Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 18/08: Task 'Chấm miniproject CNTT7' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'kiểm tra bài tập về nhà CNTT6' chưa định dạng (gán tạm 30 phút); Task 'kiểm tra bài tập về nhà CNTT7' chưa định dạng (gán tạm 30 phút); Task 'triển khai hoạt động nhóm CNTT6' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Cần chủ động và sát sao hơn trong việc kiểm tra bài tập, nhắc nhở sinh viên nộp bài bổ sung kịp thời. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Leader. Trần Minh Cường
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **88.69** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 62.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 15/07, 16/07, 17/07, 20/07, 21/07, 22/07, 23/07, 24/07, 27/07, 30/07, 31/07, 03/08, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 12/08, 13/08, 17/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08); Có task chậm trễ/tồn đọng: [Plan] Họp, bàn giao và lên kế hoạch sản xuất tài nguyên học tập cho CNTT (0%); Có task lạ chưa có định mức: Task '[Họp] Họp giao ban' chưa định dạng (gán tạm 30 phút); Task '[PTIT-KS26] Lên PM môn học Database' chưa định dạng (gán tạm 30 phút); Task '[Ngán hạn - 2026] Lên PM môn học lập trình FE cơ bản' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Trần Quốc Tuấn
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT8|HCM-K25-CNTT8(36-33-32) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT6|HCM-K25-CNTT6(38-37-47) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **88.63** (Kỷ luật: 94.2, Học tập: 88.4, Báo cáo ngày: 81.4)
- **Điểm mạnh**:
  - Khởi đầu môn mới Phân tích thiết kế hệ thống tốt tại lớp CNTT6 (vi phạm chỉ 1.75%). Quản lý kỷ luật tác nghiệp chuẩn mực.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Tại lớp HCM-K25-CNTT8, so với mốc 0% đầu môn mới, tỷ lệ vi phạm Elearning xuất hiện ngay buổi đầu ở mức 24.24%. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 07/07, 20/07, 21/07, 04/08); Khai báo vượt định mức KPI Master: 20/08: Task 'Đứng lớp buổi project lớp CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Đứng lớp buổi project lớp CNTT6' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'Đứng buổi project lớp CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Chấm thi môn python cuối môn lớp CNTT8' chưa định dạng (gán tạm 30 phút); Task 'Chấm thi môn python cuối môn lớp CNTT5' chưa định dạng (gán tạm 30 phút); Task 'Dự demo buổi thực hành của trợ giảng' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Cần kiểm soát chặt và chấn chỉnh nề nếp Elearning lớp HCM-K25-CNTT8 ngay trước buổi 2; đôn đốc sinh viên hoàn thành lý thuyết trước khi đến lớp. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Quảng An
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT5|HN-K25-CNTT5(41) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT1|HN-K25-CNTT1(41) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT2|HN-K25-CNTT2(41) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **86.84** (Kỷ luật: 90.9, Học tập: 96.7, Báo cáo ngày: 71.6)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 03/07, 07/07, 03/08, 04/08, 12/08, 17/08, 18/08, 20/08); Khai báo vượt định mức KPI Master: 09/07: Task 'Review học liệu' khai báo 1.5h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'Chấm minitest' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Review đề hackathon' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Giảng dạy CNTT3' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy CNTT4' chưa định dạng (gán tạm 30 phút); Task 'Chấm hackathon' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Leader. Hồ Xuân Hùng
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT3|HN-K24-CNTT3(42) (KS24_AI_Microservice)]]
- **Điểm KPI tổng**: **83.57** (Kỷ luật: 95.7, Học tập: 91.4, Báo cáo ngày: 59.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 13/07, 14/07, 15/07, 16/07, 17/07, 20/07, 21/07, 22/07, 23/07, 24/07, 31/07, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 13/08, 14/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08); Khai báo vượt định mức KPI Master: 27/07: Task 'Review tài liệu ôn tập sinh viên K24 đợt nghỉ hè' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 27/07: Task 'Review tài nguyên môn Microservice session7,8' khai báo 1.75h so với định mức tiêu chuẩn 0.4h; 28/07: Task 'Review tài nguyên học tập môn Microservice' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Họp giao ban khối đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Họp chốt kế hoạch triển khai thi ICPC' chưa định dạng (gán tạm 30 phút); Task 'Họp khác' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Nguyễn Bá Minh Đạo
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS24-CNTT1|HCM-K24-CNTT1(43) (KS24_AI_Microservice)]]
- **Điểm KPI tổng**: **82.34** (Kỷ luật: 83.9, Học tập: 97.9, Báo cáo ngày: 64.7)
- **Điểm mạnh**:
  - Có chuyên môn giảng dạy tốt, quản lý các lớp học lớn khối KS24 và KS25.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Từ đầu môn không set lịch học lớp HCM-CNTT2 dẫn đến không nắm bắt được chỉ số để xử lý kịp thời. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 13/07, 14/07, 16/07, 17/07, 20/07, 23/07, 24/07, 28/07, 29/07, 30/07, 31/07, 03/08, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 12/08, 13/08, 14/08, 17/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08); Có task lạ chưa có định mức: Task 'Phân chia công việc sản xuất học liệu môn Microservice' chưa định dạng (gán tạm 30 phút); Task 'Họp ĐT - Checkpoint' chưa định dạng (gán tạm 30 phút); Task 'Họp chốt nhiệm vụ SX TNHT - Kỳ nghỉ hè 2026' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải lập và thiết lập lịch học đầy đủ trên hệ thống trước khi bắt đầu khóa học để theo dõi chỉ số. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối QTKD

#### Leader. Hoàng Thị Kim Oanh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **98.23** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 94.1)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (05/08, 06/08, 21/08); Có task chậm trễ/tồn đọng: QTKDCAC-6 Xây dựng cẩm nang xử lý tình huống với sinh viên (dành cho GV, TG) - Cô Oanh (20%), Bổ sung báo cáo CTĐT K26 (30%), Rà soát thống kê báo cáo hàng ngày của nhân sự (50%); Khai báo vượt định mức KPI Master: 08/07: Task 'Hỗ trợ tư vấn sinh viên, giảng viên, Rà soát tình hình học tập các lớp, đánh giá các trường họp nguy cơ cao, cần can thiệp ngay.' khai báo 1.5h so với định mức tiêu chuẩn 0.3h; 13/07: Task 'Giảng dạy, chuẩn bị giảng dạy SS8 - PRB302' khai báo 2.5h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Chuẩn bị báo cáo + họp giao ban Đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị dữ liệu, họp trình bày CTĐT K26 với Giám đốc đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị + buổi training 1 cuộc thi Khởi Nguyên' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lê Thị Bảo Yến
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.64** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 88.8)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Có task chậm trễ/tồn đọng: Tìm hiểu chi tiết môn Kỹ năng bán hàng (Tóm tắt nội dung chương 1,2,3) (25%), Xây dựng quy trình làm việc cá nhân (Công việc chính, mục tiêu, thời gian thực hiện) (50%), Nghiên cứu nội dung môn Kỹ năng bán hàng (Nội dung chương 4,5) (40%); Khai báo vượt định mức KPI Master: 02/07: Task '- Review lại các nội dung để bổ trợ cho công tác liên quan đến sản xuất học liệu và ứng dụng AI' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 12/08: Task 'QTKDRA-10 Rà soát Tiêu chuẩn Mindmap (Cô Yến)' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 13/08: Task 'QTKDRA-10 Rà soát Tiêu chuẩn Mindmap (Cô Yến)' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task '- Nghiên cứu AI Antigravity và chạy thử demo môn quản trị vận hành để sản xuất học liệu' chưa định dạng (gán tạm 30 phút); Task '- Tiếp tục nghiên cứu các nội dung demo chương trình Nhập môn quản trị kinh doanh' chưa định dạng (gán tạm 30 phút); Task '- Tham gia buổi demo dạy lí thuyết của Mr Hùng - CNTT để nắm các thao tác thực chiến lớp học' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Ngọc Vân Khanh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.04** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 86.8)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (20/07, 21/07, 22/07, 23/07, 24/07); Có task chậm trễ/tồn đọng: Chuẩn bị nội dung session Stakeholder Analysis & Elicitation Techniques (BA) (70%), Nghiên cứu SS07 BA201 (20%), Nghiên cứu SS7 BA201 (48%); Khai báo vượt định mức KPI Master: 03/07: Task 'Chấm thi' khai báo 3.5h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Review phản biện PM' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 13/07: Task 'Review học liệu môn BA201' khai báo 4.0h so với định mức tiêu chuẩn 1.0h; Có task lạ chưa có định mức: Task 'Coi thi DTB202 - QTKD1 (Do 1 sv bị lỗi thi TN, phải coi thi bổ sung thêm 30')' chưa định dạng (gán tạm 30 phút); Task 'Hoàn thành báo cáo Check point' chưa định dạng (gán tạm 30 phút); Task 'Làm việc cùng 5 đội thi Khởi nguyên' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lê Thành Ngọc
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.69** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 82.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 10/07, 13/07, 17/07, 21/07, 29/07, 03/08, 05/08, 06/08, 07/08, 13/08, 18/08, 19/08, 26/08); Có task lạ chưa có định mức: Task 'RnD AI Agent for Learning Material' chưa định dạng (gán tạm 30 phút); Task 'Phối hợp xây dựng AI chấm bài QTKD' chưa định dạng (gán tạm 30 phút); Task 'Rà soát + Hoàn thiện điểm QTKD' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Đặng Quỳnh Trang
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD1|HN-K25-QTKD1(46) (KS25_QTKD_MAN107)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD2|HN-K25-QTKD2(42) (KS25_QTKD_MAN107)]]
- **Điểm KPI tổng**: **91.57** (Kỷ luật: 93.2, Học tập: 96.4, Báo cáo ngày: 84.6)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (07/07, 10/07, 17/07, 05/08, 06/08, 07/08); Có task chậm trễ/tồn đọng: Mentor đội Khởi nguyên Tuyệt (75%), Mentor đội Khởi nguyên Phoenix (50%), Hướng dẫn Khởi nguyên team Horizon, hướng dẫn xây dựng báo cáo chi tiết và khung tài chính, rủi ro (25%); Khai báo vượt định mức KPI Master: 08/07: Task 'Ngày 7/7/2026: Review và đọc lại các PM mà bản thân đã làm để điều chỉnh' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 13/07: Task 'Góp ý bài sinh viên về báo cáo cuối môn và slide' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; 20/07: Task 'Nghiên cứu, review, training Antigravity' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; Có task lạ chưa có định mức: Task 'Giảng dạy QTKD3' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc, hỗ trợ sinh viên, giải đáp thắc mắc ngoài giờ' chưa định dạng (gán tạm 30 phút); Task 'Nhận xét mentor cho bài làm cuộc thi Khởi nguyên' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối Ngoại ngữ và kỹ năng mềm

#### Leader. Giáp Thị Minh Hằng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.73** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 89.1)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (13/07, 20/08); Có task chậm trễ/tồn đọng: Review khảo thí bộ môn tiếng Anh (0%), Nộp báo cáo tuần (UNVERIFIED), Họp sản xuất tài nguyên học tập (0%); Khai báo vượt định mức KPI Master: 10/07: Task 'Review phiếu dự giờ các lớp tiếng Nhật KS24, KS25 của cô Lê Thị Đỏ' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; 23/07: Task 'Review timeline kaizen N4 HCM, N4 HN' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 28/07: Task 'Họp review thử việc' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'QLDTXAY-4 Chốt tiêu chuẩn GV/TG Ngoại ngữ' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị test kiến thức N5 HCM' chưa định dạng (gán tạm 30 phút); Task 'PTITXAY-1 Chỉnh sửa timeline chi tiết học kỳ I tiếng Nhật - KS26' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lò Thị Ngọc Anh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.32** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 84.4)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 08/07, 10/07, 23/07, 03/08); Có task chậm trễ/tồn đọng: REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC (90%), REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC (0%), REXPCHUO-18 [RExPREP] REVIEW PROGRESS TEST 4 (0%); Khai báo vượt định mức KPI Master: 06/07: Task 'REXPCHUO-18 [RExPREP] REVIEW PROGRESS TEST 4' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'REXPCHUO-13 [RE x PREP] REVIEW KẾT QUẢ LÀM VIỆC TRONG VÒNG 2 NĂM' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 21/07: Task 'REKHAO-23 2026.07.21 - [RE] REVIEW QUYẾT ĐỊNH KỲ THI ĐÁNH GIÁ NĂNG LỰC' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC' chưa định dạng (gán tạm 30 phút); Task 'REXPENGL-8 BÁO CÁO ĐÀO TẠO HÀNG TUẦN' chưa định dạng (gán tạm 30 phút); Task 'REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Ngô Quang Huấn
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **91.63** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 72.1)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (09/07, 15/07, 20/07, 22/07, 04/08, 12/08, 13/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08); Có task chậm trễ/tồn đọng: Xây dựng kho tài nguyên video truyền động lực cho sinh viên (20%), Sản xuất học liệu môn SKL04 Chinh phục nhà tuyển dụng (60%), Đánh giá lại và điều chỉnh khung CTĐT kỹ năng mềm và tiêu chí đánh giá (10%); Khai báo vượt định mức KPI Master: 14/07: Task 'Review lại đề thi đánh giá năng lực' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 23/07: Task 'Review nội dung môn kỹ năng Tư duy phân tích' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Phỏng vấn ứng viên GV Ký năng mềm HCM' chưa định dạng (gán tạm 30 phút); Task 'Cập nhật điểm thi môn SKL01 cho K24 và K25 CNTT' chưa định dạng (gán tạm 30 phút); Task 'Xây dựng kho tài nguyên video truyền động lực cho sinh viên' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối QLCLĐT

#### Giáo vụ. Nguyễn Huyền Trang
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.29** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 84.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (17/07, 27/07, 29/07, 21/08); Khai báo vượt định mức KPI Master: 01/07: Task 'Làm báo cáo Review công việc - Check pint' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 03/07: Task 'Báo cáo Review công việc Khảo thí tuần' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'Chỉnh sửa Quy trình dài hạn đang thực thi theo Review' khai báo 0.75h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Chốt Rpoint và tổ chức thi môn IT205-K25 HN-KS25-CNTT8' chưa định dạng (gán tạm 30 phút); Task 'Chốt Rpoint và tổ chức bảo vệ môn IT211-K24 lớp HCM-KS24-CNTT1' chưa định dạng (gán tạm 30 phút); Task 'Tổ chức thi và làm quy trình ngắn hạn' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Nguyễn Thị Tươi
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **89.89** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 66.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 16/07, 17/07, 04/08, 24/08); Có task chậm trễ/tồn đọng: Hoàn thiện báo cáo giao ban nội bộ khối ĐT (0%), Họp báo cáo giao ban nội bộ khối ĐT (0%), Review quyết định về tổ chức kỳ thi đánh giá năng lực dành cho SV K24, K25 (0%); Khai báo vượt định mức KPI Master: 09/07: Task 'Review quy định khảo thí dài hạn + ngắn hạn' khai báo 3.0h so với định mức tiêu chuẩn 0.4h; 13/07: Task 'Review quy định khảo thí PTIT' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 14/07: Task 'Review quyết định khen thưởng HK1 - K25 HCM + Phối hợp với P. TH&TN chốt danh sách' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Làm báo cáo giao ban nội bộ đào tạo Tuần 27/2026' chưa định dạng (gán tạm 30 phút); Task 'Họp giao ban nội bộ đào tạo Tuần 27/2026' chưa định dạng (gán tạm 30 phút); Task 'Họp giao ban với BLĐ' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.


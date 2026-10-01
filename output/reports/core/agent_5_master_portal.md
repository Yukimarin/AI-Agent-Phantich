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
> - ⚠️ **HN-K24-CNTT3(42-39)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **42** ➔ **39** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K24-CNTT3(42-39)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **41** ➔ **39** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K24-CNTT4(32-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT4(32-31)** (Môn: `KS24_AI_Microservice`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
> - ⚠️ **HN-K24-CNTT1(35-31)** (Môn: `KS24_DevOps`): Sĩ số thay đổi từ **35** ➔ **31** học viên (Biến động: **-4 SV**)
> - ⚠️ **HN-K24-CNTT3(42-39)** (Môn: `KS24_DevOps`): Sĩ số thay đổi từ **42** ➔ **39** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K24-CNTT4(32-31)** (Môn: `KS24_DevOps`): Sĩ số thay đổi từ **32** ➔ **31** học viên (Biến động: **-1 SV**)
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
> - ⚠️ **HN-K25-CNTT1(41-39-40-38)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **41** ➔ **38** học viên (Biến động: **-3 SV**)
> - ⚠️ **HN-K25-CNTT1(41-39-40-38)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **38** học viên (Biến động: **-2 SV**)
> - ⚠️ **HN-K25-CNTT2(41-45-44-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **41** ➔ **43** học viên (Biến động: **+2 SV**)
> - ⚠️ **HN-K25-CNTT2(41-45-44-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **38** ➔ **43** học viên (Biến động: **+5 SV**)
> - ⚠️ **HN-K25-CNTT3(43-42-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **43** ➔ **43** học viên (Biến động: **+0 SV**)
> - ⚠️ **HN-K25-CNTT3(43-42-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **35** ➔ **43** học viên (Biến động: **+8 SV**)
> - ⚠️ **HN-K25-CNTT4(38-42)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **38** ➔ **42** học viên (Biến động: **+4 SV**)
> - ⚠️ **HN-K25-CNTT4(38-42)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **42** học viên (Biến động: **+2 SV**)
> - ⚠️ **HN-K25-CNTT5(41-45)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **41** ➔ **45** học viên (Biến động: **+4 SV**)
> - ⚠️ **HN-K25-CNTT5(41-45)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **37** ➔ **45** học viên (Biến động: **+8 SV**)
> - ⚠️ **HCM-K25-CNTT8(36-33-32)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **36** ➔ **32** học viên (Biến động: **-4 SV**)
> - ⚠️ **HCM-K25-CNTT8(36-33-32)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **36** ➔ **32** học viên (Biến động: **-4 SV**)
> - ⚠️ **HCM-K25-CNTT7(43-44)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **43** ➔ **44** học viên (Biến động: **+1 SV**)
> - ⚠️ **HCM-K25-CNTT7(43-44)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **39** ➔ **44** học viên (Biến động: **+5 SV**)
> - ⚠️ **HCM-K25-CNTT6(41-42-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **41** ➔ **43** học viên (Biến động: **+2 SV**)
> - ⚠️ **HCM-K25-CNTT6(41-42-43)** (Môn: `KS25_Phantichthietkehethong`): Sĩ số thay đổi từ **40** ➔ **43** học viên (Biến động: **+3 SV**)
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
| **Phạm Ngọc Kiên** | Trợ giảng |  | 100.0 | 100.0 | 87.7 | **96.31** |
| **Nguyễn Công Hưởng** | Giảng viên |  | 100.0 | 100.0 | 87.3 | **96.19** |
| **Phan Ngọc Tài** | Trợ giảng thử việc |  | 100.0 | 100.0 | 86.5 | **95.95** |
| **Mai Xuân Chinh** | Trợ giảng |  | 100.0 | 100.0 | 85.7 | **95.71** |
| **Đinh Thành Nam** | Trợ giảng |  | 100.0 | 100.0 | 83.3 | **94.99** |
| **Ngọ Văn Quý** | Giảng viên |  | 100.0 | 100.0 | 82.8 | **94.84** |
| **Lâm Tùng Dương** | Giảng viên |  | 100.0 | 100.0 | 78.0 | **93.40** |
| **Lại Trung Lâm** | Trợ giảng |  | 100.0 | 100.0 | 75.7 | **92.71** |
| **Lê Hà Thanh Sang** | Giảng viên |  | 100.0 | 100.0 | 72.3 | **91.69** |
| **Phạm Viết Hùng** | Trợ giảng |  | 95.0 | 100.0 | 78.8 | **91.64** |
| **Trịnh Quốc Hai** | Giảng viên |  | 100.0 | 100.0 | 71.6 | **91.48** |
| **Lương Quốc Tuấn** | Giảng viên |  | 100.0 | 100.0 | 68.2 | **90.46** |
| **Lưu Hoàng Xuân Nguyên** | Trợ giảng |  | 92.5 | 100.0 | 76.4 | **89.92** |
| **Trần Quốc Tuấn** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT6|HCM-K25-CNTT6(41-42-43) (KS25_Phantichthietkehethong)]] | 95.3 | 90.7 | 80.8 | **89.59** |
| **Nguyễn Duy Quang** | GV | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-CNTT3|HN-K26-CNTT3(41) (KS26_SKL_Chudong)]] | 92.3 | 84.6 | 90.0 | **89.28** |
| **Nguyễn Đức Minh** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT5|HCM-K25-CNTT5(39-44) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT7|HCM-K25-CNTT7(43-44) (KS25_Phantichthietkehethong)]] | 91.5 | 83.0 | 86.4 | **87.43** |
| **Bùi Thanh Hải** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT1|HN-K24-CNTT1(35-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT2|HN-K24-CNTT2(39) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT4|HN-K24-CNTT4(32-31) (KS24_AI_Microservice)]] | 94.0 | 87.9 | 75.5 | **86.60** |
| **Phạm Tuấn Bình** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT3|HN-K25-CNTT3(43-42-43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT4|HN-K25-CNTT4(38-42) (KS25_Phantichthietkehethong)]] | 89.2 | 93.5 | 74.9 | **86.21** |
| **Nguyễn Quảng An** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT1|HN-K25-CNTT1(41-39-40-38) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT2|HN-K25-CNTT2(41-45-44-43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT5|HN-K25-CNTT5(41-45) (KS25_Phantichthietkehethong)]] | 84.5 | 84.0 | 73.5 | **81.07** |
| **Hồ Xuân Hùng** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT3|HN-K24-CNTT3(42-39) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-CNTT2|HN-K26-CNTT2(42) (KS26_SKL_Chudong)]] | 91.7 | 83.4 | 57.5 | **78.96** |
| **Trần Minh Cường** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS26-CNTT1|HN-KS26-CNTT1(40) (KS26_SKL_Chudong)]] | 79.2 | 58.3 | 61.1 | **67.50** |
| **Nguyễn Bá Minh Đạo** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS24-CNTT1|HCM-K24-CNTT1(43) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-CNTT1|HCM-KS26-CNTT1(47) (KS26_SKL_Chudong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-CNTT2|HCM-KS26-CNTT2(45) (KS26_SKL_Chudong)]] | 67.4 | 64.8 | 63.9 | **65.57** |

### 1.2. Khối QTKD

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Nguyễn Thị Như Quỳnh** | Trợ giảng |  | 100.0 | 100.0 | 95.5 | **98.65** |
| **Triệu Thị Thanh Tâm** | Trợ giảng |  | 100.0 | 100.0 | 91.5 | **97.45** |
| **Nguyễn Thị Hồng Minh** | Giảng viên |  | 100.0 | 100.0 | 84.5 | **95.35** |
| **Lê Thành Ngọc** | Giảng viên |  | 100.0 | 100.0 | 82.2 | **94.66** |
| **Nguyễn Ngọc Vân Khanh** | Giảng viên |  | 100.0 | 100.0 | 80.8 | **94.24** |
| **Lê Thị Bảo Yến** | Trợ giảng |  | 100.0 | 100.0 | 79.2 | **93.76** |
| **Hoàng Thị Hậu** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD1|HN-K26-QTKD1(44) (KS26_SKL_Chudong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD3|HN-K26-QTKD3(44) (KS26_SKL_Chudong)]] | 83.6 | 77.3 | 94.3 | **84.93** |
| **Lê Nhựt Mi** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-QTKD1|HCM-KS26-QTKD1 (KS26_SKL_Chudong)]] | 84.1 | 78.3 | 88.2 | **83.59** |
| **Đặng Quỳnh Trang** | Giảng viên | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD1|HN-K25-QTKD1(46) (KS25_QTKD_MAN107)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD2|HN-K25-QTKD2(42) (KS25_QTKD_MAN107)]] | 82.1 | 74.3 | 85.0 | **80.65** |
| **Hoàng Thị Kim Oanh** | Leader | [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD2|HN-K26-QTKD2(44) (KS26_SKL_Chudong)]] | 79.1 | 68.2 | 92.7 | **79.90** |

### 1.3. Khối Ngoại ngữ và kỹ năng mềm

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Lê Thị Đỏ** | Giảng viên |  | 100.0 | 100.0 | 91.0 | **97.30** |
| **Giáp Thị Minh Hằng** | Leader |  | 100.0 | 100.0 | 88.7 | **96.61** |
| **Lò Thị Ngọc Anh** | Giảng viên |  | 100.0 | 100.0 | 80.7 | **94.21** |
| **Ngô Quang Huấn** | Giảng viên |  | 100.0 | 100.0 | 64.4 | **89.32** |

### 1.4. Khối QLCLĐT

| Họ và tên | Vai trò | Lớp phụ trách | Điểm Kỷ luật SV & Tác nghiệp (40%) | Điểm Học tập (30%) | Điểm Báo cáo ngày (30%) | Điểm KPI tổng |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Trần Thị Mỹ Phước** | Giáo vụ |  | 100.0 | 100.0 | 99.8 | **99.94** |
| **Đỗ Hà Khanh** | GV |  | 100.0 | 100.0 | 98.0 | **99.40** |
| **Huỳnh Thị Kim Khánh** | GV |  | 100.0 | 100.0 | 97.4 | **99.22** |
| **Nguyễn Hồng Nhung** | GV |  | 100.0 | 100.0 | 97.0 | **99.10** |
| **Nguyễn Xuân Bách** | Giảng viên |  | 100.0 | 100.0 | 91.8 | **97.54** |
| **Nguyễn Huyền Trang** | Giáo vụ |  | 100.0 | 100.0 | 78.0 | **93.40** |
| **Nguyễn Thị Tươi** | Leader |  | 100.0 | 100.0 | 57.6 | **87.28** |


---

## 2. Đánh giá chi tiết từng cá nhân

### 🔹 Chi tiết nhân sự Khối CNTT

#### Trợ giảng. Phạm Ngọc Kiên
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.31** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 87.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (06/07, 10/07, 30/07, 13/08, 27/08, 28/08); Có task chậm trễ/tồn đọng: Dạy tiết thực hành CNTT 3 + 6 (0%), Chấm BTVN, record CNTT3 + 4 + 6 (0%); Khai báo vượt định mức KPI Master: 08/07: Task 'Chấm record, btvn, miniproject HN-KS25-CNTT3 ss11, HN-KS25-CNTT4 ss10+ss11, HN-KS25-CNTT6 ss9 miniprj,' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 03/08: Task 'KS26MON-180 S12: Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 19/08: Task 'Họp giải đáp cho sinh viên về project https://prnt.sc/Y1WNhZSpghos' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 07/09: Task 'Review lại tài liệu K25 + K26 theo chỉ đạo của leader https://prnt.sc/Ur1o1l4xUhhP - Báo cáo: https://docs.google.com/document/d/1Z1F-iPTq30mJGZ26gVKxg-WFlAJ2ionLH0l2rvNAFV8/edit?tab=t.0' khai báo 7.0h so với định mức tiêu chuẩn 0.4h; 10/09: Task 'Hỗ trợ sinh viên làm bài tập + Chuẩn bị bài tập trước khi vào hỗ trợ' khai báo 2.0h so với định mức tiêu chuẩn 0.8h; Có task lạ chưa có định mức: Task 'KS25GIAN-10 giảng dạy thực hành' chưa định dạng (gán tạm 30 phút); Task 'Chấm BTVN + record HN-KS25-CNTT3 ss5, HN-KS25-CNTT4 ss4+5 , HN-KS25-CNTT6 ss3' chưa định dạng (gán tạm 30 phút); Task 'Lên kế hoạch dạy bổ https://jjp9vfgkkr1i.jp.larksuite.com/wiki/ULIKwUH8xiziDMkrvepjJnixpoe?sheet=yuLsDL' chưa định dạng (gán tạm 30 phút); Task 'KS25GIAN-10 giảng dạy thực hành' chưa định dạng (gán tạm 30 phút); Task 'Chấm BTVN, record HN-KS25-CNTT3 ss 6+ss7, HN-KS25-CNTT4 ss 6+ss7, HN-KS25-CNTT3 ss4+ss5' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Công Hưởng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.19** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 87.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 03/07, 16/07, 24/07, 27/07, 21/08, 11/09); Có task chậm trễ/tồn đọng: Chấm bài thi cuối môn AI Application lớp K24-CNTT2 (25%); Khai báo vượt định mức KPI Master: 07/07: Task 'Triển khai buổi 1 project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 08/07: Task 'Triển Khai buổi 2 project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task 'Triển khai buổi 3 Project holiday lớp K24-CNTT1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/07: Task 'Viết tài nguyên học tập cho session 08 thực hành mini project cho môn PTIT Microservices' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/07: Task 'Chấm project holiday lớp K24-CNTT1' khai báo 4.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Chấm bảo vệ lớp K24-HCM-K24-CNTT1 môn Java Web Service' chưa định dạng (gán tạm 30 phút); Task 'Triển khai buổi thực hành session 12 môn AI Application K24-CNTT1' chưa định dạng (gán tạm 30 phút); Task 'chấm bài tập JB-IOC-PTHB251125 ,JB-IOC-PTHB260310,JB-IOC-PTHB260407' chưa định dạng (gán tạm 30 phút); Task 'Chấm bài tập K24-CNTT1 session 11 môn AI Application' chưa định dạng (gán tạm 30 phút); Task 'Chấm bài kiểm tra hackathon môn AI Application lớp K24-CNTT4' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng thử việc. Phan Ngọc Tài
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.95** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 86.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (11/09); Có task chậm trễ/tồn đọng: HCM-KS25-CNTT8 - IT-215 - Session11: Dự giờ thực hành (0%), HCM-KS25-CNTT8 - IT-215 - Session10: Chấm bài tập về nhà. (0%), HCM-KS25-CNTT5 - IT-215 - Session10, 11: Chấm bài tập về nhà. (0%), HCM-KS25-CNTT8 - IT-215 - Session13: Chăm sóc sinh viên (0%), HCM - CNTT: Tham gia Lễ sơ kết K25 (0%); Khai báo vượt định mức KPI Master: 06/07: Task 'HCM-KS25-CNTT8 - IT-215 - Session9: Dự giờ tiết thực hành - Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 06/07: Task 'HCM-KS25-CNTT5 - IT215 - Session9: Dự giờ tiết thực hành - Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'HCM-KS25-CNTT8 - IT215 : Hỗ trợ kiểm tra tiến độ project cuối môn' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'HCM-KS25-CNTT5 - IT215 - Session 21: Hỗ trợ kiểm tra tiến độ project cuối môn' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 24/08: Task 'Hỗ trợ kiểm tra tiến độ project lớp CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'HCM-KS25-CNTT8 - IT-215 - Session4: Chấm bài tập về nhà.' chưa định dạng (gán tạm 30 phút); Task 'HCM-KS25-CNTT5 - IT-215 - Session4: Chấm bài tập về nhà.' chưa định dạng (gán tạm 30 phút); Task 'HCM-KS25-CNTT8 - IT-215 - Session4, 5: Dự giờ lớp lý thuyết.' chưa định dạng (gán tạm 30 phút); Task 'HCM-CNTT: Tham gia dự giờ demo giảng thử Thầy Nguyễn Viết Hùng.' chưa định dạng (gán tạm 30 phút); Task 'HCM-CNTT: Tham gia dự giờ demo giảng thử Thầy Đặng Minh Luân.' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Mai Xuân Chinh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.71** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 85.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 07/07, 09/07, 15/07, 27/07, 30/07, 06/08, 13/08, 18/09, 24/09); Có task chậm trễ/tồn đọng: TRIEKHAI-22 Hỗ trợ SV làm dự án — CNTT2 (UNVERIFIED), TRIEKHAI-24 Hỗ trợ SV làm dự án — CNTT3 (UNVERIFIED), TRIEKHAI-18 Hỗ trợ SV làm dự án — CNTT4 (UNVERIFIED), TRIEKHAI-2 [Buổi 1] Hỗ trợ triển khai DA K24 — CNTT4 (UNVERIFIED), TRIEKHAI-5 [Buổi 1] Hỗ trợ triển khai DA K24 — CNTT2 (UNVERIFIED); Khai báo vượt định mức KPI Master: 21/07: Task 'Chấm bài Project cho sinh viên' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 28/07: Task 'Chấm bài project K24' khai báo 8.0h so với định mức tiêu chuẩn 0.5h; 10/09: Task 'Review học liệu' khai báo 4.0h so với định mức tiêu chuẩn 0.4h; 11/09: Task 'Review học liệu' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'PTITTRIE-60 [Trông thi] IT212 K24 (HN-KS24-CNTT2)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-49 [Buổi 10] Check BTVN — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-41 [Buổi 08] Check BTVN — IT212 K24 (HN-KS24-CNTT3)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-42 [Buổi 08] Chăm sóc SV — IT212 K24 (HN-KS24-CNTT3)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-49 [Buổi 10] Check BTVN — IT212 K24 (HN-KS24-CNTT2)' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Đinh Thành Nam
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.99** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 83.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 07/07, 08/07, 31/07, 06/08, 13/08, 18/08, 20/08, 10/09, 14/09, 23/09, 24/09, 25/09, 28/09, 29/09); Khai báo vượt định mức KPI Master: 01/07: Task 'Triển khai mẫu SRS môn project trước kì nghỉ cho sinh viên k24' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 27/07: Task '[Sem 3 Review Exam] Chuẩn bị câu hỏi phỏng vấn và ôn tập' khai báo 3.0h so với định mức tiêu chuẩn 0.4h; 03/08: Task '[Review session 9] PTIT K24 Devops' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 11/08: Task '[Session 9 + 10 + 11] K24 PTIT - Devops - Review tài liệu đọc và quizz' khai báo 5.0h so với định mức tiêu chuẩn 0.4h; 25/08: Task '[SRS SS13 Devops] - xây dựng SRS session 13 và dự án mẫu (base project)' khai báo 4.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Hỗ trợ mentee' chưa định dạng (gán tạm 30 phút); Task '[Java Backend Devops] Nghiên cứu và triển khai github action thay cho gitlab ci' chưa định dạng (gán tạm 30 phút); Task '[Giám sát thi] K25 CNTT8 Thi cuối môn' chưa định dạng (gán tạm 30 phút); Task '[Hỗ trợ Mentee thi khởi nguyên]' chưa định dạng (gán tạm 30 phút); Task '[Chấm bài tập] BRSE tháng 6' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Ngọ Văn Quý
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.84** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 82.8)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 14/07, 17/07, 22/07, 23/07, 24/07, 27/07, 14/08, 04/09, 11/09, 14/09, 17/09, 23/09, 25/09, 29/09); Khai báo vượt định mức KPI Master: 20/08: Task 'Họp review AI agent với bên Quản trị kinh doanh' khai báo 1.5h so với định mức tiêu chuẩn 0.4h; 21/09: Task 'Review học liệu lớp học lại môn JavaScript + Lập trình C session 04, 05 và 06' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 22/09: Task 'Review và đẩy học liệu môn lập trình C' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Trông thi hackathon lớp CNTT 3' chưa định dạng (gán tạm 30 phút); Task 'Trông thi hackathon lớp CNTT 5' chưa định dạng (gán tạm 30 phút); Task 'Quay video + popup Session 16 - Lesson 01' chưa định dạng (gán tạm 30 phút); Task 'Quay video + popup Session 16 - Lesson 02' chưa định dạng (gán tạm 30 phút); Task 'Quay video + popup Session 16 - Lesson 03' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lâm Tùng Dương
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.40** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 78.0)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 20/07, 23/07); Có task chậm trễ/tồn đọng: Sản xuất session 14 (25%); Khai báo vượt định mức KPI Master: 30/07: Task 'Review tiến độ sinh viên CNTT2 giai đoạn hè' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 31/07: Task 'Review Kiến thức lớp CNTT2-KS25' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 03/08: Task 'Review kiến thức hè sinh viên' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 04/08: Task 'Review kiến thúc sinh viên hàng ngày kỳ hè - KS25 - CNTT2' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 05/08: Task 'review kiến thức trong kỳ ôn tập hè của lớp CNTT2-KS25' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'SANXUAT-28 bài đọc session 10' chưa định dạng (gán tạm 30 phút); Task 'Phát triển AI Agent' chưa định dạng (gán tạm 30 phút); Task 'Làm checkpoint' chưa định dạng (gán tạm 30 phút); Task 'SANXUAT-28 bài đọc session 10' chưa định dạng (gán tạm 30 phút); Task 'Giảng Dạy lớp CNTT8-KS25' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lại Trung Lâm
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **92.71** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 75.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (02/07, 09/07, 10/07, 20/07, 31/07, 06/08); Có task chậm trễ/tồn đọng: giảng dạy thực hành lớp CNTT1 SS6 (UNVERIFIED), giảng dạy thực hành lớp CNTT5 SS6 (UNVERIFIED), chuẩn bị cho môn k26( lesson 1) quizz + bài đọc+ câu hỏi tự luận (0%), Chấm bài lớp CNTT1 2 5 (0%); Khai báo vượt định mức KPI Master: 01/07: Task 'CHUẨN BỊ BÀI DẠY TIẾT THỰC HÀNH SS6' khai báo 1.5h so với định mức tiêu chuẩn 0.8h; 03/07: Task 'chuẩn bị bài thực hành SS8' khai báo 2.0h so với định mức tiêu chuẩn 0.8h; 06/07: Task 'chấm mini project lớp CNTT5 session 9' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'chuẩn bị thực hành Session 11' khai báo 1.25h so với định mức tiêu chuẩn 0.8h; 13/07: Task 'Chuẩn bị thực hành session 16' khai báo 4.0h so với định mức tiêu chuẩn 0.8h; Có task lạ chưa có định mức: Task 'giảng dạy thực hành lớp CNTT1 SS6' chưa định dạng (gán tạm 30 phút); UNVERIFIED: Task 'giảng dạy thực hành lớp CNTT1 SS6' khai báo xong nhưng trên Worklane chưa DONE.; Task 'giảng dạy thực hành lớp CNTT5 SS6' chưa định dạng (gán tạm 30 phút); UNVERIFIED: Task 'giảng dạy thực hành lớp CNTT5 SS6' khai báo xong nhưng trên Worklane chưa DONE.; Task 'CHẤM BÀI TẬP SS4 SS5 LỚP CNTT1' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lê Hà Thanh Sang
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **91.69** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 72.3)
- **Điểm mạnh**:
  - Quản lý giảng dạy hiệu quả 7 lớp học khối KS25, chỉ số vi phạm học tập ở mức thấp (trung bình 13.25%).
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không có vi phạm nghiêm trọng nào ghi nhận. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 03/07, 06/07, 16/07, 20/07, 22/07, 17/08, 19/08, 28/08, 07/09, 14/09, 29/09); Khai báo vượt định mức KPI Master: 13/08: Task 'Triển khai miniproject lớp HCM-KS25-CNTT8' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 13/08: Task 'Triển khai miniproject lớp HCM-KS25-CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Triển khai thực hiện final project lớp HCM-KS25-CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Triển khai thực hiện final project lớp HCM-KS25-CNTT8' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'Kiểm tra task project lớp HCM-KS25-CNTT5' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Cập nhật tính năng của AI Agent' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc, quản lý chỉ số sinh viên' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy thực hành lớp HCM-KS25-CNTT5' chưa định dạng (gán tạm 30 phút); Task 'Bổ trợ kiến thức môn Python' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc, quản lý chỉ số sinh viên' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Tiếp tục phát huy phong cách quản lý lớp học tích cực. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Phạm Viết Hùng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **91.64** (Kỷ luật: 95.0, Học tập: 100.0, Báo cáo ngày: 78.8)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 06/07, 07/07, 08/07, 17/07, 10/08, 21/08); Khai báo vượt định mức KPI Master: 03/07: Task 'Chuẩn bị thực hành bài tập + Triển khai thực hành bài tập KS25' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 09/07: Task 'Tham gia hỗ trợ chuẩn bị thực hành và triển khai thực hành ss13 cho thầy Tài demo KS25-CNTT8' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 15/07: Task 'Chuẩn bị thực hành + Triển khai thực hành CNTT8 SS17' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 16/07: Task 'Chuẩn bị thực hành + triển khai thực hành SS19 K25 CNTT8' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; 16/07: Task 'Chuẩn bị thực hành + triển khai thực hành SS19 K25 CNTT5' khai báo 3.0h so với định mức tiêu chuẩn 0.8h; Có task lạ chưa có định mức: Task 'Tham gia buổi dạy Demo thầy Tài HCM' chưa định dạng (gán tạm 30 phút); Task 'Hỗ training phần ktbt + làm việc nhóm + raia cho thầy trợ giảng' chưa định dạng (gán tạm 30 phút); Task 'Chấm btvn và kiểm tra hoạt động nhóm KS25 và KS24' chưa định dạng (gán tạm 30 phút); Task 'Hỗ trợ sinh viên KS24 giải đáp thắc mắc, hỗ trợ sinh viên yếu KS25 môn python fastapi' chưa định dạng (gán tạm 30 phút); Task 'Kiểm tra lại các bài tập về nhà sinh viên 2 lớp KS25 và bài tập về nhà KS24 + hoạt động nhóm' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Trịnh Quốc Hai
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **91.48** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 71.6)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 14/07, 17/07, 21/07, 30/07, 14/08, 21/08, 07/09); Khai báo vượt định mức KPI Master: 09/07: Task 'review chấm bài, nhận xét bài tập các lớp, kiểm tra nhóm yếu, tài nguyên học tập' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 10/07: Task 'review lại 16 đề thi hackthon' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; 13/07: Task 'review tài nguyên session 16 lập trình ứng dụng web với fastAPI' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; 15/07: Task 'review học liệu session 19, xem session 21' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 31/07: Task 'review bài tập session 06 AI Promting' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'ra 16 đề thi  hackathon môn fastapi' chưa định dạng (gán tạm 30 phút); Task 'ra bài tập ôn tập cho các lớp chuẩn bị ôn tập thi hackathon' chưa định dạng (gán tạm 30 phút); Task 'dạy thực hành session 13 CNTT2' chưa định dạng (gán tạm 30 phút); Task 'dạy thực hành session 13 CNTT6' chưa định dạng (gán tạm 30 phút); Task 'kiểm tra lại 100 câu đề thi trắc nghiệm FASTAPI' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lương Quốc Tuấn
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **90.46** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 68.2)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 06/07, 08/07, 09/07, 10/07, 16/07, 20/07, 27/07, 31/07, 04/08, 07/08, 13/08, 14/08, 28/08, 09/09, 16/09, 18/09); Có task chậm trễ/tồn đọng: Chấm Bài Thi CNTT3 (30%); Khai báo vượt định mức KPI Master: 07/07: Task 'Chấm mini Project Lớp CNTT 1' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'Chấm mini Project Lớp CNTT5' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Chấm miniproject CNTT1' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Chấm miniproject CNTT5' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 17/07: Task 'Dạy CNTT1 Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Dạy CNTT1 KS25' chưa định dạng (gán tạm 30 phút); Task 'Dạy CNTT5 2 ca' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc sinh viên các bạn yếu' chưa định dạng (gán tạm 30 phút); Task 'Hỗ trợ quản lý các nhóm trong lớp 1,5' chưa định dạng (gán tạm 30 phút); Task 'Dạy CNTT1 : Session 10' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lưu Hoàng Xuân Nguyên
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **89.92** (Kỷ luật: 92.5, Học tập: 100.0, Báo cáo ngày: 76.4)
- **Điểm mạnh**:
  - Nhiệt tình hỗ trợ giảng viên và giải đáp thắc mắc của sinh viên.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Chưa sát sao và tập trung trong việc kiểm tra bài tập và bài tập bổ sung cho sinh viên lớp HCM-CNTT2. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 07/07, 08/07, 13/07, 17/07, 20/07, 21/07, 29/07, 31/07, 05/08, 07/08, 11/08, 12/08, 13/08, 20/08, 21/08, 28/08, 09/09, 14/09, 29/09); Có task chậm trễ/tồn đọng: Giám sát ca thi CNTT7 (0%), Giám sát ca thi CNTT5&CNTT6 (0%); Khai báo vượt định mức KPI Master: 09/07: Task 'Triển khai thực hành CNTT' khai báo 4.0h so với định mức tiêu chuẩn 2.0h; 14/07: Task 'chuẩn bị thực hành CNTT6' khai báo 1.0h so với định mức tiêu chuẩn 0.8h; 15/07: Task 'Chuẩn bị thực hành CNTT7' khai báo 1.0h so với định mức tiêu chuẩn 0.8h; 16/07: Task 'Chuẩn bị thực hành' khai báo 1.0h so với định mức tiêu chuẩn 0.8h; 04/08: Task 'KS25-175 S11: Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'kiểm tra bài tập về nhà CNTT6' chưa định dạng (gán tạm 30 phút); Task 'kiểm tra bài tập về nhà CNTT7' chưa định dạng (gán tạm 30 phút); Task 'triển khai hoạt động nhóm CNTT6' chưa định dạng (gán tạm 30 phút); Task 'triển khai hoạt động nhóm CNTT7' chưa định dạng (gán tạm 30 phút); Task 'Quản lý chỉ số 2 lớp CNTT6, 7' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Cần chủ động và sát sao hơn trong việc kiểm tra bài tập, nhắc nhở sinh viên nộp bài bổ sung kịp thời. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Trần Quốc Tuấn
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT6|HCM-K25-CNTT6(41-42-43) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **89.59** (Kỷ luật: 95.3, Học tập: 90.7, Báo cáo ngày: 80.8)
- **Điểm mạnh**:
  - Khởi đầu môn mới Phân tích thiết kế hệ thống tốt tại lớp CNTT6 (vi phạm chỉ 1.75%). Quản lý kỷ luật tác nghiệp chuẩn mực.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Cần tiếp tục bám sát và kiểm soát chặt chẽ nề nếp Elearning của sinh viên. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 07/07, 20/07, 21/07, 04/08, 04/09, 09/09); Khai báo vượt định mức KPI Master: 20/08: Task 'Đứng lớp buổi project lớp CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Đứng lớp buổi project lớp CNTT6' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'Đứng buổi project lớp CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 21/08: Task 'Đứng buổi project lớp CNTT6' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 24/08: Task 'Đứng lớp buổi 3 project CNTT7' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Chấm thi môn python cuối môn lớp CNTT8' chưa định dạng (gán tạm 30 phút); Task 'Chấm thi môn python cuối môn lớp CNTT5' chưa định dạng (gán tạm 30 phút); Task 'Dự demo buổi thực hành của trợ giảng' chưa định dạng (gán tạm 30 phút); Task 'Quản lý chỉ số, chăm sóc sinh viên' chưa định dạng (gán tạm 30 phút); Task 'Xử lý những vi phạm gian lận trong lúc thi không bắt được, phải rà soát lại và điểm số.' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Đôn đốc sinh viên hoàn thành lý thuyết Elearning đầy đủ trước khi lên lớp, duy trì nề nếp lớp học ổn định. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### GV. Nguyễn Duy Quang
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-CNTT3|HN-K26-CNTT3(41) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **89.28** (Kỷ luật: 92.3, Học tập: 84.6, Báo cáo ngày: 90.0)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không ghi nhận vi phạm nghiêm trọng.
- **Đề xuất cải thiện cụ thể**:
  - Tiếp tục duy trì và nâng cao chất lượng quản lý lớp học.

#### Giảng viên. Nguyễn Đức Minh
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT5|HCM-K25-CNTT5(39-44) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS25-CNTT7|HCM-K25-CNTT7(43-44) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **87.43** (Kỷ luật: 91.5, Học tập: 83.0, Báo cáo ngày: 86.4)
- **Điểm mạnh**:
  - Khởi đầu xuất sắc môn mới Phân tích thiết kế hệ thống tại cả 2 lớp HCM-K25-CNTT5 (0.0% vi phạm tuyệt đối) và HCM-K25-CNTT7 (chỉ 0.85% vi phạm).
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không ghi nhận vi phạm nề nếp nghiêm trọng. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (07/07, 19/08, 26/08, 28/09); Khai báo vượt định mức KPI Master: 02/07: Task 'Cấu hình và hiệu chỉnh AI Agent review backlog và sprint progress' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 06/07: Task 'Cải thiện AI Agent quản lý tiến độ project' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 14/07: Task 'Cải tiến AI Agent quản lý giám sát tiến độ mini project' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 07/08: Task 'KS242-138 S18: SRS Mini Project' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 25/08: Task 'Hỗ trợ kiểm tra tiến độ project lớp KS25 CNTT6 thầy Tuấn yêu cầu hỗ trợ' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Kiểm tra tiến độ dự án ngày 4 lớp HCM KS24 CNTT1 môn java web service' chưa định dạng (gán tạm 30 phút); Task 'Chốt tiến độ các dự án lớp HCM KS24 CNTT1' chưa định dạng (gán tạm 30 phút); Task 'Tham gia buổi giảng demo của Thầy Phạm Viết Hùng' chưa định dạng (gán tạm 30 phút); Task 'Tham gia buổi giảng demo thực hành của Thầy Đặng Minh Luân' chưa định dạng (gán tạm 30 phút); Task 'Tham gia quy trình coi thi lý thuyết và vấn đáp lớp HCM KS24 CNTT1' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Duy trì phong độ kiểm soát lớp học và nề nếp sinh viên hoàn hảo xuyên suốt toàn bộ môn học. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Bùi Thanh Hải
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT1|HN-K24-CNTT1(35-31) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT2|HN-K24-CNTT2(39) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT4|HN-K24-CNTT4(32-31) (KS24_AI_Microservice)]]
- **Điểm KPI tổng**: **86.60** (Kỷ luật: 94.0, Học tập: 87.9, Báo cáo ngày: 75.5)
- **Điểm mạnh**:
  - Duy trì tỷ lệ vi phạm của lớp ở mức rất thấp (trung bình chỉ 12.02%). Quản lý tốt 10 lớp học khối KS24.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Một số sinh viên ở gần mức cảnh báo chuyên cần tại lớp CNTT4. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (20/07, 21/07, 22/07, 23/07, 24/07, 17/08, 25/09); Khai báo vượt định mức KPI Master: 06/07: Task 'Triển khai thực hành Example Project Holiday - HN-K24-CNTT4 - Buổi 1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 07/07: Task 'Triển khai Example Project Holiday - HN-K24-CNTT4 - Buổi 2' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task '✓ TRIEKHAI- Project Example Holiday - HN-K24-CNTT3 - Buổi 1' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task '✓ TRIEKHAI- Project Example Holiday - HN-K24-CNTT4 - Buổi 4' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 09/07: Task '✓ TRIEKHAI- Project Example Holiday - HN-K24-CNTT2 - Buổi 2' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'PTITTRIE-6 [Buổi 11] Giảng LT — IT212 K24 (HN-KS24-CNTT2)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-6 [Buổi 10] Giảng LT — IT212 K24 (HN-KS24-CNTT3)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-6 [Buổi 12] Giảng LT — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút); Task 'PTITTRIE-6 [Buổi 13] Giảng LT — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút); Task 'Giảng LT — IT212 K24 (HN-KS24-CNTT4)' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Cần làm việc sát sao hơn và thường xuyên thông báo tỷ lệ chuyên cần cho sinh viên. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Phạm Tuấn Bình
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT3|HN-K25-CNTT3(43-42-43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT4|HN-K25-CNTT4(38-42) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **86.21** (Kỷ luật: 89.2, Học tập: 93.5, Báo cáo ngày: 74.9)
- **Điểm mạnh**:
  - Đảm nhiệm giảng dạy các lớp CNTT3 và CNTT5 khối KS24.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Tỷ lệ chuyên cần và bài tập về nhà của sinh viên ở mức báo động 2 (sinh viên có nền tảng yếu). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (03/07, 28/08, 07/09, 23/09, 25/09); Có task chậm trễ/tồn đọng: [Chấm thi] - AI Application In Action - HN-KS24-CNTT1 (0%), [Nguyên cứu] - Hyperframes - Sử dụng như nào và tích hợp vào như nào (0%), [Chấm thi] - Exam Hackaathon - HN-KS24-CNTT3 - AI Application (30%), [Nguyên cứu] - AI Agent HTML Slide để quay video (0%), [Nguyên cứu] - Môn mới AI Intergrard In Action (Môn sau) (0%); Khai báo vượt định mức KPI Master: 02/07: Task '[Chấm thi sản phẩm] - Project - Java Web Service' khai báo 4.0h so với định mức tiêu chuẩn 0.5h; 10/07: Task '[Chấm project IOC] Chấm project' khai báo 8.0h so với định mức tiêu chuẩn 0.5h; 03/08: Task '[Học liệu] - Làm SRS Project cho hệ BE IOC - 2 đề tài' khai báo 3.0h so với định mức tiêu chuẩn 0.5h; 04/08: Task '[Học liệu] - review lại các câu hỏi trắc nghiệm đợt thi ĐGNL' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 12/08: Task '[Review] - Reivew học liệu môn Microservice' khai báo 3.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task '[Microservice] - Làm slide - session 02' chưa định dạng (gán tạm 30 phút); Task '[Chấm thi] - AI Application In Action - HN-KS24-CNTT1' chưa định dạng (gán tạm 30 phút); Task '[Nguyên cứu] - Hyperframes - Sử dụng như nào và tích hợp vào như nào' chưa định dạng (gán tạm 30 phút); Task '[Trông thi] TN + TL - Python Exam Final - HN-KS24-CNTT8' chưa định dạng (gán tạm 30 phút); Task '[Nguyên cứu] AI Agent' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phối hợp với phòng CTSV kéo sinh viên quay lại và triển khai các buổi hỗ trợ kiến thức nền tảng. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Quảng An
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT1|HN-K25-CNTT1(41-39-40-38) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT2|HN-K25-CNTT2(41-45-44-43) (KS25_Phantichthietkehethong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-CNTT5|HN-K25-CNTT5(41-45) (KS25_Phantichthietkehethong)]]
- **Điểm KPI tổng**: **81.07** (Kỷ luật: 84.5, Học tập: 84.0, Báo cáo ngày: 73.5)
- **Điểm mạnh**:
  - Giảng dạy tốt các môn chính khối KS25 CNTT.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Không kiểm tra lại sau khi đẩy task lên QLDT dẫn đến chấm thi sai về điểm số; triển khai làm PRJ chưa tốt (sinh viên lạm dụng AI, chia file chưa tốt). Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 03/07, 07/07, 03/08, 04/08, 12/08, 17/08, 18/08, 20/08, 23/09); Khai báo vượt định mức KPI Master: 09/07: Task 'Review học liệu' khai báo 1.5h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'Chấm minitest' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Review đề hackathon' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 14/07: Task 'Review học liệu + nghiên cứu fastapi' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 20/07: Task 'Review học liệu' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Giảng dạy CNTT3' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy CNTT4' chưa định dạng (gán tạm 30 phút); Task 'Chấm hackathon' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy CNTT3' chưa định dạng (gán tạm 30 phút); Task 'Giảng dạy CNTT4' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải rà soát kỹ điểm thi sau khi đẩy lên hệ thống QLDT; hướng dẫn kỹ sinh viên cách chia file và hạn chế lạm dụng AI khi làm Project. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức kpi master, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

#### Leader. Hồ Xuân Hùng
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS24-CNTT3|HN-K24-CNTT3(42-39) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-CNTT2|HN-K26-CNTT2(42) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **78.96** (Kỷ luật: 91.7, Học tập: 83.4, Báo cáo ngày: 57.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 13/07, 14/07, 15/07, 16/07, 17/07, 20/07, 21/07, 22/07, 23/07, 24/07, 31/07, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 13/08, 14/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08, 03/09, 04/09, 07/09, 08/09, 09/09, 10/09, 11/09, 14/09, 15/09, 16/09, 17/09, 18/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Khai báo vượt định mức KPI Master: 27/07: Task 'Review tài liệu ôn tập sinh viên K24 đợt nghỉ hè' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 27/07: Task 'Review tài nguyên môn Microservice session7,8' khai báo 1.75h so với định mức tiêu chuẩn 0.4h; 28/07: Task 'Review tài nguyên học tập môn Microservice' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 29/07: Task 'Review công việc team Ngọc Trục' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 29/07: Task 'Review Tài nguyên K24' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Họp giao ban khối đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Họp chốt kế hoạch triển khai thi ICPC' chưa định dạng (gán tạm 30 phút); Task 'Họp khác' chưa định dạng (gán tạm 30 phút); Task 'Xây dựng kế hoạch ICPC' chưa định dạng (gán tạm 30 phút); Task 'Duyệt công việc các thầy Ngọc Trục' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Trần Minh Cường
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS26-CNTT1|HN-KS26-CNTT1(40) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **67.50** (Kỷ luật: 79.2, Học tập: 58.3, Báo cáo ngày: 61.1)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 15/07, 16/07, 17/07, 20/07, 21/07, 22/07, 23/07, 24/07, 27/07, 30/07, 31/07, 03/08, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 12/08, 13/08, 17/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08, 03/09, 04/09, 07/09, 08/09, 09/09, 10/09, 11/09, 14/09, 15/09, 16/09, 17/09, 18/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Có task chậm trễ/tồn đọng: [Plan] Họp, bàn giao và lên kế hoạch sản xuất tài nguyên học tập cho CNTT (0%); Có task lạ chưa có định mức: Task '[Họp] Họp giao ban' chưa định dạng (gán tạm 30 phút); Task '[PTIT-KS26] Lên PM môn học Database' chưa định dạng (gán tạm 30 phút); Task '[Ngán hạn - 2026] Lên PM môn học lập trình FE cơ bản' chưa định dạng (gán tạm 30 phút); Task '[Khởi nguyên] Chấm điểm 5 bài thi đầu tiên' chưa định dạng (gán tạm 30 phút); Task '[Họp] Họp AI Agent team' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Nguyễn Bá Minh Đạo
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS24-CNTT1|HCM-K24-CNTT1(43) (KS24_AI_Microservice)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-CNTT1|HCM-KS26-CNTT1(47) (KS26_SKL_Chudong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-CNTT2|HCM-KS26-CNTT2(45) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **65.57** (Kỷ luật: 67.4, Học tập: 64.8, Báo cáo ngày: 63.9)
- **Điểm mạnh**:
  - Có chuyên môn giảng dạy tốt, quản lý các lớp học lớn khối KS24 và KS25.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Từ đầu môn không set lịch học lớp HCM-CNTT2 dẫn đến không nắm bắt được chỉ số để xử lý kịp thời. Lỗi báo cáo ngày: Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 13/07, 14/07, 16/07, 17/07, 20/07, 23/07, 24/07, 28/07, 29/07, 30/07, 31/07, 03/08, 04/08, 05/08, 06/08, 07/08, 10/08, 11/08, 12/08, 13/08, 14/08, 17/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08, 03/09, 07/09, 08/09, 09/09, 10/09, 11/09, 14/09, 15/09, 16/09, 17/09, 18/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Có task lạ chưa có định mức: Task 'Phân chia công việc sản xuất học liệu môn Microservice' chưa định dạng (gán tạm 30 phút); Task 'Họp ĐT - Checkpoint' chưa định dạng (gán tạm 30 phút); Task 'Họp chốt nhiệm vụ SX TNHT - Kỳ nghỉ hè 2026' chưa định dạng (gán tạm 30 phút); Task 'Điều chỉnh nội dung môn Microservice' chưa định dạng (gán tạm 30 phút); Task 'Hướng dẫn thiết kế TNHT 2 môn học trong kỳ hè' chưa định dạng (gán tạm 30 phút).
- **Đề xuất cải thiện cụ thể**:
  - Phải lập và thiết lập lịch học đầy đủ trên hệ thống trước khi bắt đầu khóa học để theo dõi chỉ số. Đồng thời, cần tuân thủ lịch nộp báo cáo ngày đầy đủ, báo cáo qlđt bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối QTKD

#### Giảng viên. Nguyễn Thị Hồng Minh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **95.35** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 84.5)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (27/07, 28/07, 29/07, 30/07, 31/07); Có task chậm trễ/tồn đọng: Thiết kế hành trình trải nghiệm sinh viên (50%), Nghiên cứu đề xuất bổ sung tính năng cho LMS AI & Hệ thống tiêu chí đánh giá năng lực đầu ra cho sinh viên QTKD theo kỳ học (50%), QTKDHANH-6 Góp ý Khung Hành trình trải nghiệm sinh viên (70%), QTKDHANH-6 Góp ý Khung Hành trình trải nghiệm sinh viên (70%), Nghiên cứu khung PM môn Business Analysis mới (60%); Khai báo vượt định mức KPI Master: 14/08: Task 'Hỗ trợ trợ giảng kiểm tra btvn Session 01' khai báo 0.75h so với định mức tiêu chuẩn 0.5h; 20/08: Task 'Hỗ trợ trợ giảng chấm BTVN Session 06' khai báo 0.75h so với định mức tiêu chuẩn 0.5h; 07/09: Task 'Chấm thi vấn đáp BA 201 lớp HN-K25-QTKD3' khai báo 3.5h so với định mức tiêu chuẩn 0.5h; 07/09: Task 'Chấm thi vấn đáp BA201 lớp HN-K25-QTKD2' khai báo 4.5h so với định mức tiêu chuẩn 0.5h; 14/09: Task 'Họp cùng giảng viên môn SSK102 về lesson plan' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Tham gia giảng dạy lớp QTKD2 môn PRJ302' chưa định dạng (gán tạm 30 phút); Task 'Coi thi DTB202 QTKD1' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị bài giảng lên lớp' chưa định dạng (gán tạm 30 phút); Task 'Nghiên cứu AI agent để sản xuất học liệu' chưa định dạng (gán tạm 30 phút); Task 'Phản hồi tin nhắn mentor cuộc thi' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lê Thành Ngọc
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.66** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 82.2)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 10/07, 13/07, 17/07, 21/07, 29/07, 03/08, 05/08, 06/08, 07/08, 13/08, 18/08, 19/08, 26/08, 09/09, 10/09, 15/09, 16/09, 17/09, 18/09, 24/09); Khai báo vượt định mức KPI Master: 22/09: Task 'Chỉnh sửa slide session 03 - SSK101' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'RnD AI Agent for Learning Material' chưa định dạng (gán tạm 30 phút); Task 'Phối hợp xây dựng AI chấm bài QTKD' chưa định dạng (gán tạm 30 phút); Task 'Rà soát + Hoàn thiện điểm QTKD' chưa định dạng (gán tạm 30 phút); Task 'Xây dựng PM PowerBI' chưa định dạng (gán tạm 30 phút); Task 'Mentor 3 đội thi Khởi nguyên' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Nguyễn Ngọc Vân Khanh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.24** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 80.8)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (20/07, 21/07, 22/07, 23/07, 24/07); Có task chậm trễ/tồn đọng: Chuẩn bị nội dung session Stakeholder Analysis & Elicitation Techniques (BA) (70%), Nghiên cứu SS07 BA201 (20%), Nghiên cứu SS7 BA201 (48%), Nghiên cứu lên lesson plan cho môn BA201 (50%), Thiết kế case study theo từng lesson BA201 (50%); Khai báo vượt định mức KPI Master: 03/07: Task 'Chấm thi' khai báo 3.5h so với định mức tiêu chuẩn 0.5h; 13/07: Task 'Review phản biện PM' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 13/07: Task 'Review học liệu môn BA201' khai báo 4.0h so với định mức tiêu chuẩn 1.0h; 11/08: Task 'Coi thi - Chấm thi vấn đáp ĐGNL' khai báo 3.75h so với định mức tiêu chuẩn 0.5h; 24/08: Task 'Thống nhất nội dung ss9 với giảng viên bộ môn' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Coi thi DTB202 - QTKD1 (Do 1 sv bị lỗi thi TN, phải coi thi bổ sung thêm 30')' chưa định dạng (gán tạm 30 phút); Task 'Hoàn thành báo cáo Check point' chưa định dạng (gán tạm 30 phút); Task 'Làm việc cùng 5 đội thi Khởi nguyên' chưa định dạng (gán tạm 30 phút); Task 'Chấm thi môn DTB202' chưa định dạng (gán tạm 30 phút); Task 'Kiểm tra kết quả hiệu suất tháng 6' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Trợ giảng. Lê Thị Bảo Yến
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.76** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 79.2)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Có task chậm trễ/tồn đọng: Tìm hiểu chi tiết môn Kỹ năng bán hàng (Tóm tắt nội dung chương 1,2,3) (25%), Xây dựng quy trình làm việc cá nhân (Công việc chính, mục tiêu, thời gian thực hiện) (50%), Nghiên cứu nội dung môn Kỹ năng bán hàng (Nội dung chương 4,5) (40%), Nghiên cứu quy trình phối hợp CVHT và Ban cán sự lớp (Nội dung, quy trình, lưu ý) (50%), Nghiên cứu nội dung môn Kỹ năng bán hàng (Nội dung chương 6,10,11) (65%); Khai báo vượt định mức KPI Master: 02/07: Task '- Review lại các nội dung để bổ trợ cho công tác liên quan đến sản xuất học liệu và ứng dụng AI' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 12/08: Task 'QTKDRA-10 Rà soát Tiêu chuẩn Mindmap (Cô Yến)' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 13/08: Task 'QTKDRA-10 Rà soát Tiêu chuẩn Mindmap (Cô Yến)' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 14/08: Task 'QTKDRA-22 Tiêu chuẩn mindmap mới' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 17/08: Task 'QTKDRA-22 Tiêu chuẩn mindmap mới' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task '- Nghiên cứu AI Antigravity và chạy thử demo môn quản trị vận hành để sản xuất học liệu' chưa định dạng (gán tạm 30 phút); Task '- Tiếp tục nghiên cứu các nội dung demo chương trình Nhập môn quản trị kinh doanh' chưa định dạng (gán tạm 30 phút); Task '- Tham gia buổi demo dạy lí thuyết của Mr Hùng - CNTT để nắm các thao tác thực chiến lớp học' chưa định dạng (gán tạm 30 phút); Task '- Nghiên cứu kỹ về quy trình, quy định sản xuất học liệu cho từng nội dung: Bài đọc, Quizz, Video, bài tập' chưa định dạng (gán tạm 30 phút); Task '- Test hệ thống mới Simple care Mr Phước để hiểu được cách vận hành giao diện' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Hoàng Thị Hậu
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD1|HN-K26-QTKD1(44) (KS26_SKL_Chudong)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD3|HN-K26-QTKD3(44) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **84.93** (Kỷ luật: 83.6, Học tập: 77.3, Báo cáo ngày: 94.3)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (28/08); Có task chậm trễ/tồn đọng: Nghiên cứu xây dựng khung PM môn học (0%), Đọc dự án, nghiên cứu tìm kiếm thông tin để góp ý cuộc thi khởi nguyên (0%), Nghiên cứu AI agent (0%), QTKDPM-33 Rà soát, điều chỉnh Lesson plan KN giao tiếp, thuyết trình, phản biện (K25) (50%), Nghiên cứu góp ý là PM môn Kỹ năng học tập chủ động và phát triển bản thân (0%); Khai báo vượt định mức KPI Master: 16/09: Task 'Làm BTTH Kỹ năng HTCĐ' khai báo 2.0h so với định mức tiêu chuẩn 1.2h; 17/09: Task 'Chuẩn bị giảng dạy demo môn Kỹ năng học tập chủ động' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 17/09: Task 'Xây dựng BTVN, lesson plan, kịch bản giảng dạy Môn Kỹ năng học tập chủ động' khai báo 6.0h so với định mức tiêu chuẩn 0.7h; 21/09: Task 'Review lại slide ss1 và ss2' khai báo 1.0h so với định mức tiêu chuẩn 0.3h; Có task lạ chưa có định mức: Task 'Nghiên cứu AI agent' chưa định dạng (gán tạm 30 phút); Task 'Nghiên cứu làm nội dung khung chương trình Nhập môn quản trị kinh doanh' chưa định dạng (gán tạm 30 phút); Task 'Nghiên cứu góp ý cho cuộc thi khởi nguyên' chưa định dạng (gán tạm 30 phút); Task 'Đọc dự án, nghiên cứu tìm kiếm thông tin để góp ý cuộc thi khởi nguyên' chưa định dạng (gán tạm 30 phút); Task 'Nghiên cứu AI agent' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lê Nhựt Mi
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HCM-KS26-QTKD1|HCM-KS26-QTKD1 (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **83.59** (Kỷ luật: 84.1, Học tập: 78.3, Báo cáo ngày: 88.2)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Có task chậm trễ/tồn đọng: Tổng hợp thông tin chương trình KNM, chuẩn bị buổi họp sáng mai (0%), Phản biện đề thi ĐGNL lần 1 dựa trên đề thi do cô Hậu đề xuất. Kết quả: Hoàn thành bản nhận xét/góp ý bước đầu cho đề thi ĐGNL lần 1. Link đề thi do cô Hậu đề xuất: https://m4beo6fqhrl.sg.larksuite.com/wiki/UKo1wbLByiBQN2ksiadlsN2OgKg (50%), QTKDCAC-41 Mentor Khởi nguyên - Vòng 3: Theo dõi tiến độ các đội thi được phân công mentor vòng 3, rà soát nội dung trao đổi và ghi nhận các điểm cần tiếp tục hỗ trợ trong giai đoạn chuẩn bị pitching. Minh chứng báo cáo: https://csgakl5bs8aj.sg.larksuite.com/wiki/OGhrwov5DitSn4kDDq3ltsn2gdc?from=aut (50%), Nghiên cứu và đề xuất triển khai môn Kỹ năng làm việc nhóm và giải quyết xung đột. Minh chứng: https://jjp9vfgkkr1i.jp.larksuite.com/wiki/HB8GwLR0vikQunkH30WjxBDwp4e?from=from_copylink (70%), Phối hợp hoàn thiện đề thi ĐGNL. Kết quả: Đã gửi bản đề xuất cho cô Oanh, điều chỉnh lại độ khó, độ dài đề thì phù hợp năng lực sinh viên. Minh chứng: https://csgakl5bs8aj.sg.larksuite.com/wiki/B258wZzNWi9FRVkxd38lgBvCgcf (70%); Khai báo vượt định mức KPI Master: 01/07: Task 'Thiết lập agent hỗ trợ xây dựng học liệu, thử nghiệm quy trình tạo bài đọc, quiz, bài tập thực hành và mindmap.' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; 09/07: Task 'Sửa bài và slide cho 4 đội thi Khởi nguyên: Rà soát nội dung bài dự thi và slide trình bày của 4 đội' khai báo 3.5h so với định mức tiêu chuẩn 0.5h; 14/07: Task 'Rà soát khả năng ứng dụng AI Agent vào công việc: Xác định một số hướng ứng dụng AI Agent vào công việc cá nhân, gồm hỗ trợ chuẩn bị bài giảng, tổng hợp case study, gợi ý câu hỏi thảo luận, rà soát tài liệu và hỗ trợ lập kế hoạch công việc' khai báo 1.5h so với định mức tiêu chuẩn 1.0h; 21/07: Task 'Xác định điểm chạm và vấn đề trong hành trình sinh viên: Rà soát các điểm chạm chính như LMS, học liệu, quiz, thông báo, giảng viên, mentor và hoạt động tương tác; ghi nhận một số vấn đề có thể ảnh hưởng đến trải nghiệm học tập.' khai báo 1.0h so với định mức tiêu chuẩn 0.5h; 14/08: Task 'QTKDRA-23 Tiêu chuẩn BTVN, BTTH mới' khai báo 3.0h so với định mức tiêu chuẩn 2.0h; Có task lạ chưa có định mức: Task 'Rà soát cách agent phản hồi, điều chỉnh prompt để nội dung đầu ra phù hợp với yêu cầu sản xuất học liệu.' chưa định dạng (gán tạm 30 phút); Task 'Tham gia nhóm trao đổi, cập nhật thông tin đội thi và nắm bắt các nội dung cần hỗ trợ trong vai trò mentor cuộc thi Khởi nguyên' chưa định dạng (gán tạm 30 phút); Task 'Trao đổi lịch họp, tổng hợp thời gian phù hợp và chuẩn bị cho buổi định hướng cùng các đội thi' chưa định dạng (gán tạm 30 phút); Task 'Tạo AI Agent hỗ trợ công việc cá nhân' chưa định dạng (gán tạm 30 phút); Task 'Hệ thống lại các nội dung đã thực hiện, xác định các việc cần tiếp tục hoàn thiện trong ngày làm việc tiếp theo.' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Đặng Quỳnh Trang
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD1|HN-K25-QTKD1(46) (KS25_QTKD_MAN107)]], [[output/reports/core/agent_2_academic_prediction#Lớp: HN-KS25-QTKD2|HN-K25-QTKD2(42) (KS25_QTKD_MAN107)]]
- **Điểm KPI tổng**: **80.65** (Kỷ luật: 82.1, Học tập: 74.3, Báo cáo ngày: 85.0)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (07/07, 10/07, 17/07, 05/08, 06/08, 07/08, 14/09, 15/09); Có task chậm trễ/tồn đọng: Mentor đội Khởi nguyên Tuyệt (75%), Mentor đội Khởi nguyên Phoenix (50%), Hướng dẫn Khởi nguyên team Horizon, hướng dẫn xây dựng báo cáo chi tiết và khung tài chính, rủi ro (25%), QTKDCAC-50 Tham gia thiết kế Hành trình trải nghiệm SV (cô Trang) (30%), QTKDCAC-50 Tham gia thiết kế Hành trình trải nghiệm SV (cô Trang) (30%); Khai báo vượt định mức KPI Master: 08/07: Task 'Ngày 7/7/2026: Review và đọc lại các PM mà bản thân đã làm để điều chỉnh' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 13/07: Task 'Góp ý bài sinh viên về báo cáo cuối môn và slide' khai báo 1.5h so với định mức tiêu chuẩn 0.5h; 20/07: Task 'Nghiên cứu, review, training Antigravity' khai báo 2.0h so với định mức tiêu chuẩn 1.0h; 27/07: Task 'Training AI Antigravity tạo các bảng giao diện html, slides và cấu trúc lại các học liệu' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; 27/07: Task 'Training xây dựng học liệu MAN101 và điều chỉnh đầu ra sản phẩm html, slides' khai báo 2.0h so với định mức tiêu chuẩn 0.5h; Có task lạ chưa có định mức: Task 'Giảng dạy QTKD3' chưa định dạng (gán tạm 30 phút); Task 'Chăm sóc, hỗ trợ sinh viên, giải đáp thắc mắc ngoài giờ' chưa định dạng (gán tạm 30 phút); Task 'Nhận xét mentor cho bài làm cuộc thi Khởi nguyên' chưa định dạng (gán tạm 30 phút); Task 'Check BTVN sinh viên và đọc học liệu, trao đổi với sinh viên' chưa định dạng (gán tạm 30 phút); Task 'Nghiên cứu chuyên môn môn học' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Hoàng Thị Kim Oanh
- **Lớp phụ trách**: [[output/reports/core/agent_2_academic_prediction#Lớp: HN-K26-QTKD2|HN-K26-QTKD2(44) (KS26_SKL_Chudong)]]
- **Điểm KPI tổng**: **79.90** (Kỷ luật: 79.1, Học tập: 68.2, Báo cáo ngày: 92.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (05/08, 06/08, 21/08, 24/09); Có task chậm trễ/tồn đọng: QTKDCAC-6 Xây dựng cẩm nang xử lý tình huống với sinh viên (dành cho GV, TG) - Cô Oanh (20%), Bổ sung báo cáo CTĐT K26 (30%), Rà soát thống kê báo cáo hàng ngày của nhân sự (50%), Rà soát, chỉnh sửa CTĐT K26 theo yêu cầu của BGĐ (50%), Điều chỉnh báo cáo CTĐT (20%); Khai báo vượt định mức KPI Master: 08/07: Task 'Hỗ trợ tư vấn sinh viên, giảng viên, Rà soát tình hình học tập các lớp, đánh giá các trường họp nguy cơ cao, cần can thiệp ngay.' khai báo 1.5h so với định mức tiêu chuẩn 0.3h; 13/07: Task 'Giảng dạy, chuẩn bị giảng dạy SS8 - PRB302' khai báo 2.5h so với định mức tiêu chuẩn 0.5h; 18/09: Task 'Kịch bản hướng dẫn giảng dạy KNM Ver1' khai báo 3.0h so với định mức tiêu chuẩn 0.7h; 18/09: Task 'Review học liệu BTVN, BTTH lần 2 KN học tập chủ động' khai báo 2.0h so với định mức tiêu chuẩn 1.2h; 29/09: Task 'Giảng dạy lý thuyết BI301 SS02' khai báo 3.0h so với định mức tiêu chuẩn 2.0h; Có task lạ chưa có định mức: Task 'Chuẩn bị báo cáo + họp giao ban Đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị dữ liệu, họp trình bày CTĐT K26 với Giám đốc đào tạo' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị + buổi training 1 cuộc thi Khởi Nguyên' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị lên lớp DAKD số 2 (SS01)' chưa định dạng (gán tạm 30 phút); Task 'Công việc khác: hỗ trợ SV, đồng nghiệp, phối hợp công việc vỡi bộ phận quản lý chất lượng, khảo thí, BTC cuộc thi...' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối Ngoại ngữ và kỹ năng mềm

#### Leader. Giáp Thị Minh Hằng
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **96.61** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 88.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (13/07, 20/08, 24/09, 29/09); Có task chậm trễ/tồn đọng: Review khảo thí bộ môn tiếng Anh (0%), Họp sản xuất tài nguyên học tập (0%), nghi om (0%), Ra đề thi nói cuối kỳ (0%), PTITORIE-4 Tạo bộ câu hỏi cho quiz văn hóa Nhật Bản (UNVERIFIED); Khai báo vượt định mức KPI Master: 10/07: Task 'Review phiếu dự giờ các lớp tiếng Nhật KS24, KS25 của cô Lê Thị Đỏ' khai báo 2.5h so với định mức tiêu chuẩn 0.4h; 23/07: Task 'Review timeline kaizen N4 HCM, N4 HN' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 28/07: Task 'Họp review thử việc' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 29/07: Task 'Review bộ tiêu chuẩn tài nguyên học tập' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 25/08: Task 'Làm việc với nhân sự tiếng Nhật về kỳ review sau thử việc' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'QLDTXAY-4 Chốt tiêu chuẩn GV/TG Ngoại ngữ' chưa định dạng (gán tạm 30 phút); Task 'Chuẩn bị test kiến thức N5 HCM' chưa định dạng (gán tạm 30 phút); Task 'PTITXAY-1 Chỉnh sửa timeline chi tiết học kỳ I tiếng Nhật - KS26' chưa định dạng (gán tạm 30 phút); Task 'Xử lý đơn xin chuyển môn ngoại ngữ Mai Đức Thuy N4.4' chưa định dạng (gán tạm 30 phút); Task 'PTITQUAN-1 Lên kế hoạch dự giờ các lớp tiếng Nhật KS24, KS25' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Lò Thị Ngọc Anh
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **94.21** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 80.7)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 08/07, 10/07, 23/07, 03/08, 14/09, 17/09, 29/09); Có task chậm trễ/tồn đọng: REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC (90%), REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC (0%), REXPCHUO-18 [RExPREP] REVIEW PROGRESS TEST 4 (0%), REKHAO-2 [RE] BỘ ĐỀ TOEIC TEST 1 (LISTENING & READING) (90%), REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC (80%); Khai báo vượt định mức KPI Master: 06/07: Task 'REXPCHUO-18 [RExPREP] REVIEW PROGRESS TEST 4' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'REXPCHUO-13 [RE x PREP] REVIEW KẾT QUẢ LÀM VIỆC TRONG VÒNG 2 NĂM' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 21/07: Task 'REKHAO-23 2026.07.21 - [RE] REVIEW QUYẾT ĐỊNH KỲ THI ĐÁNH GIÁ NĂNG LỰC' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 31/07: Task 'REXPENGL-47 2026.07.31 - [RE] REVIEW CÔNG VIỆC & KẾ HOẠCH CẢI THIỆN CHO GV' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 19/08: Task 'REXPENGL-85 [RE] REVIEW NHÂN SỰ' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC' chưa định dạng (gán tạm 30 phút); Task 'REXPENGL-8 BÁO CÁO ĐÀO TẠO HÀNG TUẦN' chưa định dạng (gán tạm 30 phút); Task 'REXPCHUO-1 🔵 [RE x PREP/JAXTINA] GIAO TIẾP & XỬ LÝ CÔNG VIỆC HÀNG NGÀY VỚI ĐỐI TÁC' chưa định dạng (gán tạm 30 phút); Task 'REKHAO-2 [RE] BỘ ĐỀ TOEIC TEST 1 (LISTENING & READING)' chưa định dạng (gán tạm 30 phút); Task 'REKHAO-8 [RE] TỔ CHỨC KỲ THI SÁT HẠCH TIẾNG ANH TOEIC ĐỢT 1 2026' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Giảng viên. Ngô Quang Huấn
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **89.32** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 64.4)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (09/07, 15/07, 20/07, 22/07, 04/08, 12/08, 13/08, 18/08, 19/08, 20/08, 21/08, 24/08, 25/08, 26/08, 27/08, 28/08, 03/09, 04/09, 07/09, 08/09, 09/09, 10/09, 11/09, 14/09, 15/09, 16/09, 17/09, 18/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Có task chậm trễ/tồn đọng: Xây dựng kho tài nguyên video truyền động lực cho sinh viên (20%), Sản xuất học liệu môn SKL04 Chinh phục nhà tuyển dụng (60%), Đánh giá lại và điều chỉnh khung CTĐT kỹ năng mềm và tiêu chí đánh giá (10%), Sản xuất học liệu môn SKL04 Chinh phục nhà tuyển dụng (60%), Sản xuất kho tài nguyên video truyền động lực cho sinh viên (50%); Khai báo vượt định mức KPI Master: 14/07: Task 'Review lại đề thi đánh giá năng lực' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 23/07: Task 'Review nội dung môn kỹ năng Tư duy phân tích' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Phỏng vấn ứng viên GV Ký năng mềm HCM' chưa định dạng (gán tạm 30 phút); Task 'Cập nhật điểm thi môn SKL01 cho K24 và K25 CNTT' chưa định dạng (gán tạm 30 phút); Task 'Xây dựng kho tài nguyên video truyền động lực cho sinh viên' chưa định dạng (gán tạm 30 phút); Task 'Sản xuất học liệu môn SKL04 Chinh phục nhà tuyển dụng' chưa định dạng (gán tạm 30 phút); Task 'Đánh giá lại và điều chỉnh khung CTĐT kỹ năng mềm và tiêu chí đánh giá' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

### 🔹 Chi tiết nhân sự Khối QLCLĐT

#### Giáo vụ. Nguyễn Huyền Trang
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **93.40** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 78.0)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (17/07, 27/07, 29/07, 21/08, 04/09, 15/09, 16/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Khai báo vượt định mức KPI Master: 01/07: Task 'Làm báo cáo Review công việc - Check pint' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 03/07: Task 'Báo cáo Review công việc Khảo thí tuần' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 09/07: Task 'Chỉnh sửa Quy trình dài hạn đang thực thi theo Review' khai báo 0.75h so với định mức tiêu chuẩn 0.4h; 10/07: Task 'Review Khảo thí LMS cùng rikasoft' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 10/07: Task 'Review Khảo thí đối tác về LMS AI, trao đổi lại Rika về phương án đề thi' khai báo 0.75h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Chốt Rpoint và tổ chức thi môn IT205-K25 HN-KS25-CNTT8' chưa định dạng (gán tạm 30 phút); Task 'Chốt Rpoint và tổ chức bảo vệ môn IT211-K24 lớp HCM-KS24-CNTT1' chưa định dạng (gán tạm 30 phút); Task 'Tổ chức thi và làm quy trình ngắn hạn' chưa định dạng (gán tạm 30 phút); Task 'Thiết kế danh sách thi hệ ngắn hạn' chưa định dạng (gán tạm 30 phút); Task 'Liên hệ trao đổi với SV K25 môn IT215 - GV không liên hệ được và thực hiện xoá khỏi lớp sau 3 buổi' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.

#### Leader. Nguyễn Thị Tươi
- **Lớp phụ trách**: 
- **Điểm KPI tổng**: **87.28** (Kỷ luật: 100.0, Học tập: 100.0, Báo cáo ngày: 57.6)
- **Điểm mạnh**:
  - Duy trì các chỉ số học tập của sinh viên ở mức ổn định.
- **Điểm yếu / Lỗi vi phạm đã mắc**:
  - Thiếu nộp báo cáo ngày (01/07, 02/07, 03/07, 16/07, 17/07, 04/08, 24/08, 09/09, 10/09, 17/09, 18/09, 21/09, 22/09, 23/09, 24/09, 25/09, 28/09, 29/09); Có task chậm trễ/tồn đọng: Hoàn thiện báo cáo giao ban nội bộ khối ĐT (0%), Họp báo cáo giao ban nội bộ khối ĐT (0%), Review quyết định về tổ chức kỳ thi đánh giá năng lực dành cho SV K24, K25 (0%), Review quy định khảo thí PTIT (0%), Hoàn thiện báo cáo tình trạng SV (BL/BH, ...) (0%); Khai báo vượt định mức KPI Master: 09/07: Task 'Review quy định khảo thí dài hạn + ngắn hạn' khai báo 3.0h so với định mức tiêu chuẩn 0.4h; 13/07: Task 'Review quy định khảo thí PTIT' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 14/07: Task 'Review quyết định khen thưởng HK1 - K25 HCM + Phối hợp với P. TH&TN chốt danh sách' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; 20/07: Task 'Review quy định đào tạo' khai báo 1.0h so với định mức tiêu chuẩn 0.4h; 21/07: Task 'Review Quy trình phối hợp khảo thí nội bộ' khai báo 2.0h so với định mức tiêu chuẩn 0.4h; Có task lạ chưa có định mức: Task 'Làm báo cáo giao ban nội bộ đào tạo Tuần 27/2026' chưa định dạng (gán tạm 30 phút); Task 'Họp giao ban nội bộ đào tạo Tuần 27/2026' chưa định dạng (gán tạm 30 phút); Task 'Họp giao ban với BLĐ' chưa định dạng (gán tạm 30 phút); Task 'Xếp TKB và cập nhật thông tin HV 02 lớp ngắn hạn' chưa định dạng (gán tạm 30 phút); Task 'Phản hồi và xử lý các công việc phát sinh' chưa định dạng (gán tạm 30 phút)
- **Đề xuất cải thiện cụ thể**:
  - Cần tuân thủ lịch nộp báo cáo ngày đầy đủ, đẩy nhanh tiến độ hoàn thành task, kiểm soát giờ khai báo đúng định mức KPI Master, báo cáo QLĐT bổ sung định mức cho đầu việc lạ.


---

## 3. Báo Cáo Kiểm Toán Giờ Công & Tuân Thủ KPI Master Worklane (Chốt Đến 18/09/2026)

> [!IMPORTANT]
> **MỤC TIÊU KIỂM TOÁN TÁC NGHIỆP THỜI GIAN THỰC (WORKLANE AUDIT):**
> - **Thời gian chốt số liệu**: Từ **01/09/2026 đến hết ngày 18/09/2026** (12 ngày làm việc chính thức, đã loại trừ nghỉ lễ 31/08 - 02/09 và các ngày nghỉ phép được phê duyệt).
> - **Quỹ thời gian tiêu chuẩn**: **8.0h/ngày** (Tổng định mức chuẩn trong 12 ngày là **96.0 giờ/nhân sự**).
> - **Quy tắc KPI Master từng khối**: Khối CNTT (chuẩn hóa dạy 2.0h/buổi, 18 task Review độc lập, khảo thí 120p/lớp, cấm nghiệm thu soạn học liệu tự do ngoài barem); Khối QTKD (chuẩn dạy 3.0h, CVHT Rank 1 là 1.5h, Rank 2 là 2.0h).

### 3.1. Bảng Tổng Hợp Giờ Công & Vi Phạm KPI Master Theo 4 Khối Đào Tạo

| Khối Đào Tạo | Tổng NS | Số NS Thiếu Giờ | Tổng Giờ Thiếu | Lỗi Over-reporting | Lỗi Ngoài Barem (Wildcard) | Lỗi Lệch Pha Worklane |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Khối QTKD** | 10 | **8** | **103.0h** | 56 | 699 | 2 |
| **Khối CNTT** | 22 | **22** | **920.0h** | 114 | 1339 | 0 |
| **Khối Ngoại ngữ và kỹ năng mềm** | 7 | **5** | **245.5h** | 14 | 405 | 1 |
| **Khối QLCLĐT** | 3 | **2** | **170.0h** | 7 | 232 | 0 |


### 3.2. Danh Sách Chi Tiết Nhân Sự Làm Thiếu Giờ (< 8h/ngày trong Tháng 9)

| STT | Họ và tên | Khối | Vai trò & Rank | Giờ Thực Tế | Giờ Chuẩn | Giờ Thiếu | Công Suất (%) | Số Ngày < 8h | Mức Độ Cảnh Báo |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | **Trần Minh Cường** | Khối CNTT | Giảng viên (R3) | 0.0h | 152.0h | **152.0h** | **0.0%** | 19/11 | 🔴 **Nghiêm trọng** |
| 2 | **Hồ Xuân Hùng** | Khối CNTT | Giảng viên (R3) | 0.0h | 152.0h | **152.0h** | **0.0%** | 19/11 | 🔴 **Nghiêm trọng** |
| 3 | **Ngô Quang Huấn** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 0.0h | 152.0h | **152.0h** | **0.0%** | 19/11 | 🔴 **Nghiêm trọng** |
| 4 | **Nguyễn Bá Minh Đạo** | Khối CNTT | Giảng viên (R3) | 7.2h | 152.0h | **144.8h** | **4.8%** | 19/11 | 🔴 **Nghiêm trọng** |
| 5 | **Nguyễn Thị Tươi** | Khối QLCLĐT | Giảng viên (R3) | 64.5h | 152.0h | **87.5h** | **42.4%** | 13/11 | 🔴 **Nghiêm trọng** |
| 6 | **Nguyễn Huyền Trang** | Khối QLCLĐT | Giảng viên (R3) | 69.5h | 152.0h | **82.5h** | **45.7%** | 16/11 | 🔴 **Nghiêm trọng** |
| 7 | **Đinh Thành Nam** | Khối CNTT | Giảng viên (R3) | 85.0h | 152.0h | **67.0h** | **55.9%** | 13/11 | 🔴 **Nghiêm trọng** |
| 8 | **Lê Thị Đỏ** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 90.5h | 152.0h | **61.5h** | **59.5%** | 9/11 | 🔴 **Nghiêm trọng** |
| 9 | **Lê Thành Ngọc** | Khối QTKD | Giảng viên (R3) | 96.0h | 152.0h | **56.0h** | **63.2%** | 7/11 | 🔴 **Nghiêm trọng** |
| 10 | **Nguyễn Xuân Bách** | Khối CNTT | Giảng viên (R4) | 103.8h | 152.0h | **48.2h** | **68.3%** | 16/11 | 🔴 **Nghiêm trọng** |
| 11 | **Lưu Hoàng Xuân Nguyên** | Khối CNTT | Giảng viên (R3) | 107.8h | 152.0h | **44.2h** | **70.9%** | 15/11 | 🔴 **Nghiêm trọng** |
| 12 | **Lê Hà Thanh Sang** | Khối CNTT | Giảng viên (R3) | 112.5h | 152.0h | **39.5h** | **74.0%** | 11/11 | 🔴 **Nghiêm trọng** |
| 13 | **Trần Quốc Tuấn** | Khối CNTT | Giảng viên (R3) | 113.0h | 152.0h | **39.0h** | **74.3%** | 17/11 | 🔴 **Nghiêm trọng** |
| 14 | **Nguyễn Đức Minh** | Khối CNTT | Giảng viên (R3) | 114.2h | 152.0h | **37.8h** | **75.2%** | 13/11 | 🔴 **Nghiêm trọng** |
| 15 | **Phạm Ngọc Kiên** | Khối CNTT | Giảng viên (R3) | 119.0h | 152.0h | **33.0h** | **78.3%** | 8/11 | 🔴 **Nghiêm trọng** |
| 16 | **Ngọ Văn Quý** | Khối CNTT | Giảng viên (R3) | 122.5h | 152.0h | **29.5h** | **80.6%** | 7/11 | 🔴 **Nghiêm trọng** |
| 17 | **Phan Ngọc Tài** | Khối CNTT | Giảng viên (R3) | 125.5h | 152.0h | **26.5h** | **82.6%** | 15/11 | 🔴 **Nghiêm trọng** |
| 18 | **Bùi Thanh Hải** | Khối CNTT | Giảng viên (R3) | 127.0h | 152.0h | **25.0h** | **83.6%** | 9/11 | 🔴 **Nghiêm trọng** |
| 19 | **Phạm Tuấn Bình** | Khối CNTT | Giảng viên (R3) | 128.0h | 152.0h | **24.0h** | **84.2%** | 3/11 | 🔴 **Nghiêm trọng** |
| 20 | **Lương Quốc Tuấn** | Khối CNTT | Giảng viên (R3) | 129.2h | 152.0h | **22.8h** | **85.0%** | 3/11 | 🔴 **Nghiêm trọng** |
| 21 | **Giáp Thị Minh Hằng** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 131.5h | 152.0h | **20.5h** | **86.5%** | 4/11 | 🔴 **Nghiêm trọng** |
| 22 | **Triệu Thị Thanh Tâm** | Khối QTKD | Trợ giảng (R1) | 131.8h | 152.0h | **20.2h** | **86.7%** | 5/11 | 🔴 **Nghiêm trọng** |
| 23 | **Mai Xuân Chinh** | Khối CNTT | Giảng viên (R3) | 139.0h | 152.0h | **13.0h** | **91.4%** | 6/11 | 🟡 Cảnh báo |
| 24 | **Đặng Quỳnh Trang** | Khối QTKD | Giảng viên (R3) | 140.5h | 152.0h | **11.5h** | **92.4%** | 2/11 | 🟡 Cảnh báo |
| 25 | **Lò Thị Ngọc Anh** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 141.0h | 152.0h | **11.0h** | **92.8%** | 5/11 | 🟡 Cảnh báo |
| 26 | **Trịnh Quốc Hai** | Khối CNTT | Giảng viên (R3) | 141.8h | 152.0h | **10.2h** | **93.3%** | 2/11 | 🟡 Cảnh báo |
| 27 | **Lê Nhựt Mi** | Khối QTKD | Giảng viên (R3) | 142.2h | 152.0h | **9.8h** | **93.6%** | 14/11 | 🟡 Cảnh báo |
| 28 | **Nguyễn Quảng An** | Khối CNTT | Giảng viên (R3) | 144.0h | 152.0h | **8.0h** | **94.7%** | 1/11 | 🟢 Đạt chuẩn |
| 29 | **Lê Thị Bảo Yến** | Khối QTKD | Giảng viên (R3) | 147.5h | 152.0h | **4.5h** | **97.0%** | 7/11 | 🟢 Đạt chuẩn |
| 30 | **Phạm Viết Hùng** | Khối CNTT | Giảng viên (R3) | 150.0h | 152.0h | **2.0h** | **98.7%** | 3/11 | 🟢 Đạt chuẩn |
| 31 | **Lâm Tùng Dương** | Khối CNTT | Giảng viên (R3) | 150.5h | 152.0h | **1.5h** | **99.0%** | 6/11 | 🟢 Đạt chuẩn |
| 32 | **Nguyễn Thị Hồng Minh** | Khối QTKD | Giảng viên (R3) | 151.0h | 152.0h | **1.0h** | **99.3%** | 1/11 | 🟢 Đạt chuẩn |
| 33 | **Huỳnh Thị Kim Khánh** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 87.5h | 88.0h | **0.5h** | **99.4%** | 2/11 | 🟢 Đạt chuẩn |
| 34 | **Trần Thị Mỹ Phước** | Khối QLCLĐT | Giảng viên (R3) | 152.0h | 152.0h | **0.0h** | **100.0%** | 0/11 | 🟢 Đạt chuẩn |
| 35 | **Nguyễn Thị Như Quỳnh** | Khối QTKD | Trợ giảng (R1) | 152.2h | 152.0h | **0.0h** | **100.2%** | 1/11 | 🟢 Đạt chuẩn |
| 36 | **Hoàng Thị Hậu** | Khối QTKD | Giảng viên (R5) | 153.0h | 152.0h | **0.0h** | **100.7%** | 0/11 | 🟢 Đạt chuẩn |
| 37 | **Lại Trung Lâm** | Khối CNTT | Giảng viên (R3) | 153.0h | 152.0h | **0.0h** | **100.7%** | 1/11 | 🟢 Đạt chuẩn |
| 38 | **Nguyễn Ngọc Vân Khanh** | Khối QTKD | Giảng viên (R3) | 154.2h | 152.0h | **0.0h** | **101.5%** | 0/11 | 🟢 Đạt chuẩn |
| 39 | **Nguyễn Hồng Nhung** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 65.0h | 64.0h | **0.0h** | **101.6%** | 0/11 | 🟢 Đạt chuẩn |
| 40 | **Đỗ Hà Khanh** | Khối Ngoại ngữ và kỹ năng mềm | Giảng viên (R3) | 131.0h | 128.0h | **0.0h** | **102.3%** | 0/11 | 🟢 Đạt chuẩn |
| 41 | **Hoàng Thị Kim Oanh** | Khối QTKD | Giảng viên (R5) | 156.0h | 152.0h | **0.0h** | **102.6%** | 2/11 | 🟢 Đạt chuẩn |
| 42 | **Nguyễn Công Hưởng** | Khối CNTT | Giảng viên (R3) | 157.0h | 152.0h | **0.0h** | **103.3%** | 1/11 | 🟢 Đạt chuẩn |


### 3.3. Thống Kê Các Hành Vi Khai Báo Sai Quy Định KPI Master

Hệ thống kiểm toán tự động phát hiện 3 nhóm sai phạm khai báo công việc phổ biến trên Worklane:

1. **Khai báo vượt định mức (Over-reporting)**: Khai báo giờ thực tế cao gấp 1.3x - 2.0x so với định mức KPI Master ban hành của khối (ví dụ: giảng dạy trực tiếp barem 2.0h nhưng khai báo 3h, 4h; chấm bài vượt trần).
2. **Khai báo đầu việc tự do ngoài barem (Wildcard Tasks)**: Tự ý khai báo các công việc 'soạn bài', 'nghiên cứu', 'hỗ trợ tự do' mà không có mã task hoặc không nằm trong danh mục 18 task type được nghiệm thu.
3. **Lệch pha Worklane (UNVERIFIED)**: Khai báo trong nhật ký ngày là hoàn thành 100%, nhưng đối soát ticket trên hệ thống Worklane PM vẫn đang ở trạng thái 'Cần làm' hoặc 'Đang làm'.

| Họ và tên | Khối | Tổng Lỗi KPI | Vượt Định Mức | Ngoài Barem | Chưa DONE Worklane | Chi Tiết Vi Phạm Điển Hình |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Lâm Tùng Dương** | Khối CNTT | **164** | 15 | 149 | 0 | Giảng dạy CNTT2 - Ôn tập... (Khai báo ngoài barem KPI Master khối (2.5h)); Thay đổi format quiz phù hợp v... (Khai báo ngoài barem KPI Master khối (1.5h)) |
| **Trần Thị Mỹ Phước** | Khối QLCLĐT | **136** | 0 | 136 | 0 | Tổng hợp thông tin về CVHT x B... (Khai báo ngoài barem KPI Master khối (0.25h)); Tổng hợp thông tin về mô hình ... (Khai báo ngoài barem KPI Master khối (0.25h)) |
| **Lò Thị Ngọc Anh** | Khối Ngoại ngữ và kỹ năng mềm | **112** | 5 | 107 | 0 | REXPCHUO-73 XIN BÁO CÁO VỀ TÌN... (Khai báo ngoài barem KPI Master khối (1.0h)); REXPENGL-112 [RE] FEEDBACK INT... (Khai báo ngoài barem KPI Master khối (2.0h)) |
| **Nguyễn Thị Như Quỳnh** | Khối QTKD | **110** | 0 | 109 | 1 | Nghiên cứu và hệ thống hoá kiế... (Khai báo ngoài barem KPI Master khối (6.0h)); Kiểm tra BTVN - QTKD2... (Khai báo ngoài barem KPI Master khối (1.0h)) |
| **Nguyễn Công Hưởng** | Khối CNTT | **110** | 3 | 107 | 0 | Trông thi kết thúc học phần mô... (Khai báo ngoài barem KPI Master khối (2.5h)); Trông thi kết thúc học phần mô... (Khai báo ngoài barem KPI Master khối (2.5h)) |
| **Lại Trung Lâm** | Khối CNTT | **108** | 5 | 103 | 0 | Em ngã xe xin nghỉ hôm nay ạ... (Khai báo ngoài barem KPI Master khối (8.0h)); coi thi lớp cntt2... (Khai báo ngoài barem KPI Master khối (1.0h)) |
| **Lê Thị Bảo Yến** | Khối QTKD | **106** | 17 | 89 | 0 | Chủ động nghiên cứu thống tin ... (Khai báo ngoài barem KPI Master khối (0.5h)); Xem lại mô hình phối hợp CVHT ... (Khai báo ngoài barem KPI Master khối (0.5h)) |
| **Triệu Thị Thanh Tâm** | Khối QTKD | **103** | 0 | 102 | 1 | Làm biên bản về sự việc thay đ... (Khai báo ngoài barem KPI Master khối (1.0h)); Check BTVN và chăm sóc sinh vi... (Khai báo ngoài barem KPI Master khối (2.25h)) |
| **Phạm Viết Hùng** | Khối CNTT | **103** | 7 | 96 | 0 | Hỗ trợ xây dựng học liệu câu h... (Khai báo ngoài barem KPI Master khối (4.5h)); Hỗ trợ kiểm tra BTVN 2 lớp K25... (Khai báo ngoài barem KPI Master khối (2.0h)) |
| **Phan Ngọc Tài** | Khối CNTT | **102** | 3 | 99 | 0 | HCM-KS25-CNTT7: Chăm sóc sinh ... (Khai báo ngoài barem KPI Master khối (1.0h)); HCM-KS25-CNTT5: Chăm sóc sinh ... (Khai báo ngoài barem KPI Master khối (1.0h)) |
| **Nguyễn Xuân Bách** | Khối CNTT | **101** | 0 | 101 | 0 | Làm báo cáo họp giao ban... (Khai báo ngoài barem KPI Master khối (0.75h)); Họp giao ban nội bộ đào tạo... (Khai báo ngoài barem KPI Master khối (2.25h)) |
| **Giáp Thị Minh Hằng** | Khối Ngoại ngữ và kỹ năng mềm | **90** | 2 | 87 | 1 | PTITXAY-21 bàn giao lại CTĐT n... (Khai báo ngoài barem KPI Master khối (1.0h)); PTITJPN-4 Soạn Cam kết lớp Tal... (Khai báo ngoài barem KPI Master khối (1.5h)) |


### 3.4. Kiến Nghị & Hành Động Quản Trị Từ Ban Lãnh Đạo Đào Tạo

1. **Chấn chỉnh nhân sự không báo cáo ngày và thiếu giờ nghiêm trọng**:
   - Yêu cầu các Leader (Thầy Hồ Xuân Hùng, Thầy Nguyễn Bá Minh Đạo, Thầy Trần Minh Cường) làm việc trực tiếp với các nhân sự có công suất < 75% hoặc quên báo cáo nhiều ngày (Trần Minh Cường 0h, Hồ Xuân Hùng 0h, Ngô Quang Huấn 0h, Nguyễn Bá Minh Đạo 7.2h, Nguyễn Ngọc Sơn 11.5h, Đặng Minh Luân 37.8h, Lê Thành Ngọc 48h).
   - Áp dụng trừ điểm kỷ luật tác nghiệp theo Quy chế đào tạo và không xét khen thưởng học kỳ cho nhân sự có tỷ lệ nộp log < 80%.
2. **Kiểm soát chặt chẽ định mức KPI Master**:
   - Khối CNTT: Giảng viên chỉ được khai báo tối đa 120 phút (2.0h) cho một buổi lên lớp trực tiếp. Nghiêm cấm gộp giờ hoặc khai báo vượt trần mà không có phê duyệt của Giám đốc Đào tạo.
   - Loại bỏ 100% các task tự sản xuất học liệu ngoài kế hoạch. Mọi sản phẩm học liệu phải có biên bản nghiệm thu độc lập và ticket Worklane tương ứng.
   - Toàn bộ công việc khai báo 'Hoàn thành' trên log ngày bắt buộc phải đồng bộ chuyển trạng thái `DONE` trên Worklane PM trước 22h00 hàng ngày.


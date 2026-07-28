-- File SQL mẫu: qldt.sql
-- Chứa thông tin môn tiên quyết và điểm thi giữa kỳ của sinh viên

-- 1. Tạo bảng điểm thi giữa kỳ
CREATE TABLE IF NOT EXISTS student_grades (
    student_id VARCHAR(10) PRIMARY KEY,
    student_name VARCHAR(100),
    class_id VARCHAR(10),
    subject VARCHAR(100),
    midterm_score REAL
);

-- 2. Tạo bảng môn tiên quyết
CREATE TABLE IF NOT EXISTS prerequisites (
    subject_id VARCHAR(10),
    subject_name VARCHAR(100),
    prerequisite_id VARCHAR(10),
    prerequisite_name VARCHAR(100)
);

-- 3. Chèn dữ liệu mẫu cho bảng điểm sinh viên
-- Lớp L01 - Môn Lập trình Python (GV: Nguyễn Văn A phụ trách)
INSERT OR REPLACE INTO student_grades VALUES ('SV001', 'Lê Văn Nam', 'L01', 'Lập trình Python', 8.5);
INSERT OR REPLACE INTO student_grades VALUES ('SV002', 'Trần Thị Mai', 'L01', 'Lập trình Python', 4.5);
INSERT OR REPLACE INTO student_grades VALUES ('SV003', 'Phạm Minh Đức', 'L01', 'Lập trình Python', 7.0);
INSERT OR REPLACE INTO student_grades VALUES ('SV004', 'Hoàng Thanh Tùng', 'L01', 'Lập trình Python', 3.0);
INSERT OR REPLACE INTO student_grades VALUES ('SV005', 'Đỗ Thùy Linh', 'L01', 'Lập trình Python', 9.0);

-- Lớp L02 - Môn Cấu trúc dữ liệu (TG: Trần Thị B phụ trách trợ giảng)
INSERT OR REPLACE INTO student_grades VALUES ('SV006', 'Vũ Hoàng Long', 'L02', 'Cấu trúc dữ liệu', 5.5);
INSERT OR REPLACE INTO student_grades VALUES ('SV007', 'Nguyễn Phương Thảo', 'L02', 'Cấu trúc dữ liệu', 3.5);
INSERT OR REPLACE INTO student_grades VALUES ('SV008', 'Phan Văn Hải', 'L02', 'Cấu trúc dữ liệu', 4.0);
INSERT OR REPLACE INTO student_grades VALUES ('SV009', 'Lê Thu Trang', 'L02', 'Cấu trúc dữ liệu', 6.0);
INSERT OR REPLACE INTO student_grades VALUES ('SV010', 'Bùi Anh Tuấn', 'L02', 'Cấu trúc dữ liệu', 5.0);

-- 4. Chèn dữ liệu môn tiên quyết
INSERT OR REPLACE INTO prerequisites VALUES ('CS102', 'Cấu trúc dữ liệu', 'CS101', 'Lập trình Python');
INSERT OR REPLACE INTO prerequisites VALUES ('CS103', 'Cơ sở dữ liệu', 'CS101', 'Lập trình Python');

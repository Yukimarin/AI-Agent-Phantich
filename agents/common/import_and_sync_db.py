import os
import sys
import subprocess
import socket
import time
import sqlite3
import mysql.connector

sys.stdout.reconfigure(encoding='utf-8')

def check_mysql_port(port=3307):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect(('127.0.0.1', port))
        s.close()
        return True
    except socket.error:
        s.close()
        return False

def ensure_mysql_started():
    print("Kiểm tra trạng thái MySQL Server (port 3307)...")
    if check_mysql_port(3307):
        print("✓ MySQL Server đã hoạt động trên cổng 3307.")
        return True

    print("⚠️ MySQL Server cổng 3307 đang tắt. Đang khởi động tự động...")
    mysql_bin = r"C:\Program Files\MySQL\MySQL Server 9.7\bin\mysqld.exe"
    data_dir = os.path.abspath("data/mysql_data_97")
    
    if not os.path.exists(mysql_bin):
        print(f"✗ Lỗi: Không tìm thấy MySQL binary tại {mysql_bin}.")
        return False

    cmd = [
        mysql_bin,
        "--no-defaults",
        f"--datadir={data_dir}",
        "--port=3307",
        "--shared-memory"
    ]
    
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        # Chờ tối đa 15 giây cho port mở
        for i in range(15):
            time.sleep(1.0)
            if check_mysql_port(3307):
                print("✓ Khởi động MySQL Server 3307 thành công!")
                return True
        print("✗ Quá thời gian chờ khởi động MySQL Server.")
        return False
    except Exception as e:
        print(f"✗ Lỗi khởi động MySQL: {e}")
        return False

def find_latest_sql_dump():
    default_path = r"C:\Users\DELL\Downloads\qldt_el-13-08-26.sql"
    if os.path.exists(default_path):
        return default_path
    
    # Tìm kiếm trong thư mục Downloads
    downloads_dir = r"C:\Users\DELL\Downloads"
    if os.path.exists(downloads_dir):
        sql_files = [os.path.join(downloads_dir, f) for f in os.listdir(downloads_dir) if f.startswith("qldt_el") and f.endswith(".sql")]
        if sql_files:
            # Lấy file có thời gian sửa đổi mới nhất
            latest_file = max(sql_files, key=os.path.getmtime)
            return latest_file
            
    return None

def import_sql_dump(sql_path):
    print(f"Bắt đầu import SQL dump: {sql_path}")
    
    mysql_cli = r"C:\Program Files\MySQL\MySQL Server 9.7\bin\mysql.exe"
    if not os.path.exists(mysql_cli):
        print(f"✗ Lỗi: Không tìm thấy MySQL client tại {mysql_cli}")
        return False
        
    # 1. Tạo database nếu chưa tồn tại
    try:
        print("Tạo database qldt_el nếu chưa tồn tại...")
        create_cmd = [
            mysql_cli,
            "-h", "127.0.0.1",
            "-P", "3307",
            "-u", "root",
            "-e", "CREATE DATABASE IF NOT EXISTS qldt_el;"
        ]
        subprocess.run(create_cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Lỗi tạo database: {e.stderr.decode('utf-8', errors='ignore')}")
        return False
        
    # 2. Thực hiện import qua stdin redirection sử dụng file binary mode
    cmd = [
        mysql_cli,
        "-h", "127.0.0.1",
        "-P", "3307",
        "-u", "root",
        "qldt_el"
    ]
    
    start_time = time.time()
    try:
        print("Đang thực thi lệnh import qua MySQL CLI... Vui lòng chờ...")
        # Mở file chế độ binary mode để OS tự động chuyển tiếp file descriptor, không tốn RAM của Python
        with open(sql_path, "rb") as f:
            result = subprocess.run(cmd, stdin=f, check=True, capture_output=True)
        elapsed = time.time() - start_time
        print(f"✓ Import thành công! Thời gian thực hiện: {elapsed:.2f} giây.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Lỗi import SQL dump:")
        print(e.stdout.decode('utf-8', errors='ignore'))
        print(e.stderr.decode('utf-8', errors='ignore'))
        return False

def sync_to_sqlite():
    print("Bắt đầu đồng bộ dữ liệu tinh gọn sang SQLite fallback (qldt.db)...")
    sqlite_db_path = "data/inputs/qldt.db"
    
    # Kết nối MySQL
    try:
        mysql_conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="qldt_el"
        )
        mysql_cursor = mysql_conn.cursor(dictionary=True)
    except Exception as e:
        print(f"✗ Lỗi kết nối MySQL để đồng bộ: {e}")
        return False
        
    # Kết nối SQLite
    try:
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # 1. Tạo các bảng cần thiết trong SQLite
        sqlite_cursor.execute("DROP TABLE IF EXISTS student_grades")
        sqlite_cursor.execute("DROP TABLE IF EXISTS prerequisites")
        
        sqlite_cursor.execute("""
        CREATE TABLE student_grades (
            student_id VARCHAR(10),
            student_name VARCHAR(100),
            class_id VARCHAR(100),
            subject VARCHAR(100),
            midterm_score REAL
        );
        """)
        sqlite_cursor.execute("""
        CREATE TABLE prerequisites (
            subject_id VARCHAR(10),
            subject_name VARCHAR(100),
            prerequisite_id VARCHAR(10),
            prerequisite_name VARCHAR(100)
        );
        """)
        sqlite_conn.commit()
        
        # 2. Xóa dữ liệu cũ
        sqlite_cursor.execute("DELETE FROM student_grades")
        sqlite_cursor.execute("DELETE FROM prerequisites")
        sqlite_conn.commit()
        
        # 3. Lấy dữ liệu sinh viên thực tế từ MySQL
        print("Đang truy vấn dữ liệu sinh viên thực tế từ MySQL...")
        query = """
        SELECT 
            s.id AS student_id, 
            s.full_name AS student_name, 
            c.name AS class_name, 
            co.name AS course_name,
            COALESCE(f.rpoints, 0.0) AS midterm_score
        FROM qldt_el.final_results f
        JOIN qldt_el.students s ON f.student_id = s.id
        JOIN qldt_el.classes c ON f.class_id = c.id
        JOIN qldt_el.courses co ON f.course_id = co.id
        """
        mysql_cursor.execute(query)
        students_data = mysql_cursor.fetchall()
        print(f"Lấy thành công {len(students_data)} bản ghi sinh viên.")
        
        # 4. Ghi vào SQLite
        print("Đang ghi dữ liệu vào SQLite student_grades...")
        sqlite_cursor.executemany(
            "INSERT INTO student_grades VALUES (?, ?, ?, ?, ?)",
            [(f"SV{r['student_id']}", r['student_name'], r['class_name'], r['course_name'], float(r['midterm_score'])) for r in students_data]
        )
        
        # 5. Đồng bộ bảng prerequisites (nếu có dữ liệu)
        try:
            mysql_cursor.execute("SHOW TABLES LIKE 'prerequisites'")
            has_prereq = mysql_cursor.fetchone()
            if has_prereq:
                mysql_cursor.execute("SELECT subject_id, subject_name, prerequisite_id, prerequisite_name FROM prerequisites")
                prereq_data = mysql_cursor.fetchall()
                sqlite_cursor.executemany(
                    "INSERT INTO prerequisites VALUES (?, ?, ?, ?)",
                    [(r['subject_id'], r['subject_name'], r['prerequisite_id'], r['prerequisite_name']) for r in prereq_data]
                )
                print(f"Lấy thành công {len(prereq_data)} bản ghi prerequisites.")
            else:
                # Chèn dữ liệu mẫu nếu MySQL không có bảng này
                sqlite_cursor.execute("INSERT INTO prerequisites VALUES ('CS102', 'Cấu trúc dữ liệu', 'CS101', 'Lập trình Python')")
                sqlite_cursor.execute("INSERT INTO prerequisites VALUES ('CS103', 'Cơ sở dữ liệu', 'CS101', 'Lập trình Python')")
                print("Chèn dữ liệu prerequisites mẫu mặc định.")
        except Exception as pe:
            print(f"Warning: Không thể đồng bộ prerequisites ({pe}). Sử dụng mặc định.")
            
        sqlite_conn.commit()
        
        # Kiểm tra kích thước file SQLite
        sqlite_size = os.path.getsize(sqlite_db_path) / (1024 * 1024)
        print(f"✓ Đồng bộ thành công! Dung lượng SQLite qldt.db: {sqlite_size:.2f} MB")
        
    except Exception as e:
        print(f"✗ Lỗi trong quá trình đồng bộ sang SQLite: {e}")
        return False
    finally:
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()
            
    return True

def main():
    print("================================================================================")
    print("KHỞI CHẠY TIẾN TRÌNH IMPORT & ĐỒNG BỘ DỮ LIỆU ĐÀO TẠO (QLĐT)")
    print("================================================================================")
    
    # 1. Khởi động MySQL Server
    if not ensure_mysql_started():
        print("✗ Thất bại: Không thể khởi chạy MySQL Server. Tiến trình dừng lại.")
        sys.exit(1)
        
    # 2. Tìm file SQL dump mới nhất
    dump_path = find_latest_sql_dump()
    if not dump_path:
        print("⚠️ Cảnh báo: Không tìm thấy file SQL dump dạng qldt_el*.sql nào tại Downloads.")
        print("Tiến hành đồng bộ SQLite từ cơ sở dữ liệu MySQL hiện tại...")
        sync_to_sqlite()
        sys.exit(0)
        
    # 3. Thực hiện import
    print(f"Phát hiện file SQL dump: {dump_path}")
    
    # Lưu trạng thái timestamp để tránh import lặp lại không cần thiết
    sync_meta_path = "data/processed/last_db_import.json"
    mtime = os.path.getmtime(dump_path)
    
    should_import = True
    if os.path.exists(sync_meta_path):
        try:
            import json
            with open(sync_meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                last_mtime = meta.get("mtime", 0.0)
                if abs(mtime - last_mtime) < 0.01:
                    should_import = False
                    print("✓ Dữ liệu SQL dump này đã được import trước đó và là mới nhất.")
        except Exception:
            pass
            
    if should_import:
        success = import_sql_dump(dump_path)
        if success:
            import json
            # Ghi nhận log import
            with open(sync_meta_path, "w", encoding="utf-8") as f:
                json.dump({"mtime": mtime, "file": dump_path}, f)
        else:
            print("✗ Lỗi: Tiến trình import thất bại.")
            sys.exit(1)
    
    # 4. Đồng bộ sang SQLite
    sync_success = sync_to_sqlite()
    if sync_success:
        print("✓ Hoàn tất toàn bộ quy trình import và đồng bộ!")
        sys.exit(0)
    else:
        print("⚠️ Cảnh báo: Đồng bộ SQLite thất bại, nhưng MySQL đã được cập nhật.")
        sys.exit(0)

if __name__ == "__main__":
    main()

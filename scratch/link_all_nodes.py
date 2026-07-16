import os
import glob

def link_all_nodes():
    base_dir = r"C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT"
    
    # 1. Đổi tên file lỗi encoding trong data/
    data_dir = os.path.join(base_dir, "data")
    for file in os.listdir(data_dir):
        if file.startswith("QUY") and file.endswith(".md") and "CHE_TAI" not in file:
            filepath = os.path.join(data_dir, file)
            new_basename = "QUY_DINH_KHUNG_CHE_TAI_VA_KHEN_THUONG_NANG_SUAT_DAO_TAO.md"
            new_filepath = os.path.join(data_dir, new_basename)
            if not os.path.exists(new_filepath):
                os.rename(filepath, new_filepath)
                print(f"Renamed encoding bug file to: {new_basename}")
            else:
                try:
                    os.remove(filepath)
                except:
                    pass
                print(f"Cleaned up redundant encoding bug file.")

    # 2. Quét các thư mục đích để chèn Backlink
    target_dirs = [
        os.path.join(base_dir, "docs", "agents"),
        os.path.join(base_dir, "docs", "plans"),
        os.path.join(base_dir, "reports")
    ]
    
    backlink_str = "\n\n---\nTrở về: [[docs/knowledge_map|Bản đồ Tri thức dự án]]\n"
    
    for t_dir in target_dirs:
        if not os.path.exists(t_dir):
            continue
        for root, dirs, files in os.walk(t_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        if "[[docs/knowledge_map" not in content:
                            with open(filepath, "a", encoding="utf-8") as f:
                                f.write(backlink_str)
                            print(f"Linked: {os.path.relpath(filepath, base_dir)}")
                    except Exception as e:
                        print(f"Error processing file {file}: {e}")

if __name__ == "__main__":
    link_all_nodes()

import os
import sys
import requests

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

html_path = 'output/5_unified_dashboard.html'
link_path = 'output/unified_dashboard_link.txt'

print("Đang tải file 5_unified_dashboard.html lên Catbox qua requests...")
try:
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Không tìm thấy file: {html_path}")

    with open(html_path, 'rb') as f:
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': f}
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        
    if response.status_code == 200:
        url_online = response.text.strip()
        if url_online.startswith('https://files.catbox.moe/'):
            print(f"Upload thành công! Link online: {url_online}")
            
            with open(link_path, 'w', encoding='utf-8') as lf:
                lf.write(url_online)
                
            # Tạo file Bao_Cao_Tich_Hop.url ở thư mục gốc
            url_content = f"[InternetShortcut]\nURL={url_online}\n"
            with open('Bao_Cao_Tich_Hop.url', 'w', encoding='utf-8') as sf:
                sf.write(url_content)
            print(f"Đã tạo file internet shortcut tại: Bao_Cao_Tich_Hop.url")
            
            # Cập nhật Xem_Bao_Cao_Online.html ở gốc
            redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={url_online}" />
    <title>Hệ thống Tích hợp Chỉ số Đào tạo & Dự báo Học lực</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #faf5ff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center;
        }}
        a {{
            color: #7c3aed;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Đang chuyển hướng đến Web Dashboard Tích hợp Premium...</h2>
        <p>Nếu trình duyệt không tự động chuyển hướng, vui lòng <a href="{url_online}">nhấp vào đây</a> để xem trực tiếp.</p>
    </div>
</body>
</html>
"""
            with open('Xem_Bao_Cao_Online.html', 'w', encoding='utf-8') as rf:
                rf.write(redirect_html)
            print(f"Đã cập nhật Xem_Bao_Cao_Online.html sang redirect link online.")
        else:
            print(f"Lỗi phản hồi từ Catbox: {url_online}")
    else:
        print(f"Lỗi kết nối Catbox. Status code: {response.status_code}, Response: {response.text}")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình upload: {e}")

import requests

html_path = 'output/kpi_report.html'
try:
    with open(html_path, 'rb') as f:
        files = {'file': ('kpi_report.html', f, 'text/html')}
        # Thử thêm headers User-Agent thông dụng
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.post('https://file.io', files=files, headers=headers)
        print("Status code:", response.status_code)
        print("Response headers:", response.headers)
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

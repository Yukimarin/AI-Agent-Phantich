import requests

html_path = 'output/kpi_report.html'
try:
    with open(html_path, 'rb') as f:
        files = {'file': ('kpi_report.html', f, 'text/html')}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        # Gửi tới www.file.io/
        response = requests.post('https://www.file.io/', files=files, headers=headers, allow_redirects=False)
        print("Status code:", response.status_code)
        print("Headers:", response.headers)
        safe_text = response.text[:500].encode('ascii', 'ignore').decode('ascii')
        print("Response text (safe):", safe_text)
except Exception as e:
    print("Error:", str(e))

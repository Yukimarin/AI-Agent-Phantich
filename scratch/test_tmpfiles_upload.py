import requests
import os

html_path = 'output/5_unified_dashboard.html'
if not os.path.exists(html_path):
    print("File not found")
    exit(1)

try:
    with open(html_path, 'rb') as f:
        files = {'file': f}
        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

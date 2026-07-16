import requests

html_path = 'output/kpi_report.html'
try:
    with open(html_path, 'rb') as f:
        files = {'file': f}
        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

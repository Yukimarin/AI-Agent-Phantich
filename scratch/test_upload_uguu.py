import requests

html_path = 'output/kpi_report.html'
try:
    with open(html_path, 'rb') as f:
        files = {'files[]': f} # uguu.se yêu cầu files[]
        response = requests.post('https://uguu.se/api.php?d=upload-tool', files=files)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

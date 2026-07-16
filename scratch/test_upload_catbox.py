import requests

html_path = 'output/kpi_report.html'
try:
    with open(html_path, 'rb') as f:
        data = {
            'reqtype': 'fileupload'
        }
        files = {
            'fileToUpload': f
        }
        # Tải lên Catbox
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

import requests
import json

html_path = 'output/5_unified_dashboard.html'
try:
    # 1. Get best server
    res_server = requests.get('https://api.gofile.io/servers')
    if res_server.status_code == 200:
        server_data = res_server.json()
        if server_data['status'] == 'ok' and server_data['data']['servers']:
            server = server_data['data']['servers'][0]['name']
            print(f"Using server: {server}")
            
            # 2. Upload file
            upload_url = f'https://{server}.gofile.io/contents/uploadfile'
            with open(html_path, 'rb') as f:
                files = {'file': f}
                res_upload = requests.post(upload_url, files=files)
                
            print("Upload status:", res_upload.status_code)
            print("Response:", res_upload.text)
        else:
            print("No server available:", server_data)
    else:
        print("Failed to get server list:", res_server.status_code)
except Exception as e:
    print("Error:", str(e))

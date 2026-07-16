import requests

try:
    # Upload text đơn giản
    response = requests.post('https://file.io', files={'file': ('test.txt', 'Hello World from Antigravity')})
    print("Status code:", response.status_code)
    print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))

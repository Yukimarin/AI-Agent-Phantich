import urllib.request
import os

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

assets = {
    "chart.js": "https://cdn.jsdelivr.net/npm/chart.js",
    "tailwind.js": "https://cdn.tailwindcss.com"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for name, url in assets.items():
    path = os.path.join(output_dir, name)
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read()
        with open(path, "wb") as f:
            f.write(content)
        print(f"Successfully downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

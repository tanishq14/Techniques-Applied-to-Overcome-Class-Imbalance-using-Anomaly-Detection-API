import os
import requests
from PIL import Image

# prepare
os.makedirs('static/uploads', exist_ok=True)
img_path = 'static/uploads/test_mvtec_post.png'
Image.new('L', (224, 224), color=128).save(img_path)
print('Saved:', img_path)

url = 'http://127.0.0.1:5000/api/predict/mvtec'
with open(img_path, 'rb') as f:
    files = {'file': ('test_mvtec_post.png', f, 'image/png')}
    try:
        r = requests.post(url, files=files, timeout=30)
        print('Status:', r.status_code)
        print('Response:', r.text[:4000])
    except Exception as e:
        print('Request failed:', e)

# print last lines of api.log
log_path = 'api.log'
if os.path.exists(log_path):
    print('\n--- api.log (last 200 lines) ---')
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as h:
        lines = h.readlines()
        for L in lines[-200:]:
            print(L, end='')
else:
    print('api.log not found')

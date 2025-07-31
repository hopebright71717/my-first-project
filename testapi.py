import hashlib
import hmac
import json
import time
import requests

# ✅ 金鑰資訊
api_key = "ecvnjgqz6hgrn5k6jd3q497n76nh69yd"
salt_key = "bc6pfkqxj22c"
secret_key = b"5kt9tmhqtzrg7bmvxqf99kajcz9jyyru"

# ✅ 商品 ID
item_id = "22429606318058"

# ✅ API 路徑與完整網址
url_path = "/api/v1/product/item/image"
full_url = "https://partner.ruten.com.tw" + url_path

# ✅ 時間戳記
timestamp = str(int(time.time()))

# ✅ 請求內容
payload = {
    "item_id": item_id
}

# ✅ 產生簽章
def gen_sign(salt_key, url, request_body, timestamp) -> str:
    request_body_json = json.dumps(request_body, separators=(',', ':'))
    data_for_sign = salt_key + url + request_body_json + timestamp
    return hmac.new(secret_key, data_for_sign.encode('utf-8'), hashlib.sha256).hexdigest()

signature = gen_sign(salt_key, full_url, payload, timestamp)

# ✅ 設定 headers（包含 User-Agent）
headers = {
    'User-Agent': 'ruten-api',  # 🔥 關鍵所在
    'X-RT-Timestamp': timestamp,
    'X-RT-Key': api_key,
    'X-RT-Authorization': signature
}

# ✅ 上傳的圖片
files = [
    ('images[]', ('test.png', open('C:/Users/hopeb/Documents/露天API-專案/test.png', 'rb'), 'image/png'))
]

# ✅ 發送 POST 請求
response = requests.post(full_url, headers=headers, data=payload, files=files)

# ✅ 顯示回傳結果
print("狀態碼：", response.status_code)
print("回傳內容：", response.text)

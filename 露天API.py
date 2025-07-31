import time
import hashlib
import hmac
import requests

# 老徐提供的憑證
API_KEY = "ecvnjgqz6hgrn5k6jd3q497n76nh69yd"
SECRET_KEY = "5kt9tmhqtzrg7bmvxqf99kajcz9jyyru"
SALT_KEY = "bc6pfkqxj22c"

# 建立簽章 function
def generate_signature(api_key, secret_key, salt, timestamp):
    data = api_key + str(timestamp) + salt
    sign = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
    return sign

# Step 1：設定 timestamp 與簽章
timestamp = int(time.time())
sign = generate_signature(API_KEY, SECRET_KEY, SALT_KEY, timestamp)

# Step 2：測試 API（舉例為分類查詢）
url = "https://api.ruten.com.tw/openapi/v1/categories"
headers = {
    "Content-Type": "application/json",
    "API-Key": API_KEY,
    "Timestamp": str(timestamp),
    "Sign": sign
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 顯示結果
print(response.status_code)
print(response.text)

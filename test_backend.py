import requests

url = "http://127.0.0.1:5000/api/gesture/"
payload = {"gesture": "peace_sign"}

response = requests.post(url, json=payload)
print(response.json())

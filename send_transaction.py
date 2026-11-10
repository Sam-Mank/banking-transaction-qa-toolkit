
import requests

url = "http://127.0.0.1:5000/transactions"

payload = {
    "transaction_id": "TXN3001",
    "amount": 125.50,
    "account_reference": "ACC2001"
}

response = requests.post(
    url,
    json=payload,
    timeout=10
)

print("HTTP STATUS:", response.status_code)
print("API RESPONSE:")
print(response.json())

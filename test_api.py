import requests

BASE_URL = "http://localhost:8000"

# Test login
login_data = {"username": "your_username", "password": "your_password"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json().get("access_token")

headers = {"Authorization": f"Bearer {token}"}

# Test create order
order_data = {"quantity": 2, "pizza_size": "MEDIUM"}
response = requests.post(f"{BASE_URL}/order/", json=order_data, headers=headers)
print("Create order:", response.status_code, response.json())

# Test get orders
response = requests.get(f"{BASE_URL}/order/user/orders", headers=headers)
print("Get orders:", response.status_code, response.json())
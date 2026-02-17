import requests

api = "https://httpbin.org/post"

payload = {
    "username" : "john",
    "password": "123"
}

response = requests.post(api,data=payload,timeout=5)

print(response.json())
print(response.headers)

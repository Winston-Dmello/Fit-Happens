import requests

data = {"Object": "pipe"}

response = requests.post("http://192.168.193.27:8000/spawn", json=data)
response.raise_for_status()
print(f"Successfully sent pose: {data}")

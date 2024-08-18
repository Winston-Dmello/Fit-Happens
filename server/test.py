import requests

data = {"Object": "hurdle"}

response = requests.post("http://localhost:8000/spawn", json=data)
response.raise_for_status()
print(f"Successfully sent Spawn: {data}")

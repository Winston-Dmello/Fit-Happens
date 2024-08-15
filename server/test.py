import requests

data = {"Pose": "Squat"}

response = requests.post("http://localhost:8000/message", json=data)
response.raise_for_status()
print(f"Successfully sent pose: {data}")

datas = {"username": "Winston", "score": 2000}

response = requests.post("http://localhost:8000/scoreboard", json=datas)
response = requests.get("http://localhost:8000/scoreboard")
print(response.text)

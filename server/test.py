import requests

data = {"Pose": "LeanRight"}

response = requests.post("http://192.168.193.27:8000/message", json=data)
response.raise_for_status()
print(f"Successfully sent pose: {data}")

datas = {"username": "Winston", "score": 2000}

response = requests.post("http://192.168.193.27:8000/scoreboard", json=datas)
response = requests.get("http://192.168.193.27:8000/scoreboard")
print(response.text)

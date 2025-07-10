import requests

url = "http://127.0.0.1:5000/predict"

features = [80, 4, 1]
data = {"features": features}

response = requests.post(url, json=data)

prediction = response.json()
print(prediction)
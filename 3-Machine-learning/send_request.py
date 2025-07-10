import requests

url = "http://127.0.0.1:5000/predict"

response = requests.get(url)
prediction = response.json()
print(prediction)
import requests
import json

url = "http://0.0.0.0:3333/invocations"

data = {
  "instances": [
    [5.1, 3.5, 1.4, 0.2]
  ]
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
  prediction = response.json()
  print(prediction)
else:
  print(f"Error: {response.status_code}")
  print(response.text)
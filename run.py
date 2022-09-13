import requests
import json

url = "http://47.250.49.41/myproject1/delete_department"

payload = json.dumps({
  "dep_name": "5"
})
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'session=eyJ1c2VybmFtZSI6IkUwMSJ9.Yxg5tw.FSW-qju4j1n4OI55TyrbRAPDNAc'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
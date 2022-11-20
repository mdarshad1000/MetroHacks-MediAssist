import requests


url = "	https://healthservice.priaid.ch/symptoms"

response = requests.get(url)
print(response)
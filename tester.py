import requests
link = 'http://127.0.0.1:5000/allow/3'
p = requests.get(link).content
print(p)
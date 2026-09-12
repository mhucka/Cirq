import requests
import json
url = "https://api.github.com/repos/sympy/sympy/issues/16074"
response = requests.get(url)
body = response.json().get('body')
print(body)

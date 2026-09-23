import requests
import json
url = "https://api.github.com/repos/sympy/sympy/issues/16074"
response = requests.get(url)
print(response.json().get('state'))
print(response.json().get('body'))
events_url = url + "/events"
events = requests.get(events_url).json()
for ev in events:
    if ev.get('event') == 'closed':
        print('Closed by:', ev.get('commit_id'), ev.get('url'))

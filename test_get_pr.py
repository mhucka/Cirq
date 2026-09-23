import requests
url = "https://api.github.com/repos/sympy/sympy/issues/16074/timeline"
headers = {"Accept": "application/vnd.github.v3+json"}
response = requests.get(url, headers=headers)
for event in response.json():
    if event.get('event') == 'cross-referenced' and event.get('source'):
        print(event['source']['issue']['html_url'])
        print(event['source']['issue']['state'])
        print(event['source']['issue']['title'])

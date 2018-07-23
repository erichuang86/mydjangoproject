import requests

# query event list interface
url = "http://127.0.0.1:8000/api/get_event_list/"
r = requests.get(url, params={'eid':'1'})
result = r.json()

# assertion return of interface
assert result['status'] == 200
assert result['message'] == "success"
assert result['data']['name'] == "DevOps site release conf"
assert result['data']['address'] == "M401"
assert result['data']['start_time'] == "2018-07-31T08:00:00"
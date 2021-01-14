import requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post('http://127.0.0.1:5000/test', params=payload)
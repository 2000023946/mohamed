import requests
import json
post_rest = requests.get('http://127.0.0.1:8000/api/recent/momoabucar')

print(post_rest.json())

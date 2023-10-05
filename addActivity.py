import requests
import json
import time


base_url = 'https://api.github.com/search/issues?q=-label:invalid+type:pr+is:public+author:zhangkaihua88&per_page=300'

response = requests.get(base_url)

data = json.loads(response.text)
print(data)
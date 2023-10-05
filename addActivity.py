from collections import defaultdict
import requests
import json
import time


base_url = 'https://api.github.com/search/issues?q=-label:invalid+type:pr+is:public+author:zhangkaihua88&per_page=1000'


def get_json(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data


raw_data = get_json(base_url)
raw_data = [item for item in raw_data['items'] if item['state'] == 'closed']
# print(data)

data = defaultdict(dict)

for item_data in raw_data:
    item_repo = item_data['repository_url'].split('/')[-1]
    item_name = item_data['repository_url'].split('/')[-2]

    item_repo_url = item_data['repository_url'].replace('api.', '').replace('repos/', '')
    item_name_url = item_data['repository_url'].replace('api.', '').replace('repos/', '').replace(f'/{item_repo}', '')

    item_data_appended = get_json(item_data['pull_request']['url'])
    if item_data_appended['merged']:
        add_base = data[f'{item_name}/{item_repo}'].get('additions', 0)
        del_base = data[f'{item_name}/{item_repo}'].get('deletions', 0)
        count_base = data[f'{item_name}/{item_repo}'].get('count', 0)
        data[f'{item_name}/{item_repo}'] = {
            'additions':item_data_appended['additions']+add_base, 
            'deletions':item_data_appended['deletions']+del_base,
            'count':count_base+1,
        }
keys = sorted(data, key=lambda x: data[x]['additions']+data[x]['deletions'], reverse=True)

def gen_item(data, key):
    strings = f"- [{key}](https://github.com/{key}) PR " + str(data['count']) + " times with ${\color{green}{-" + str(data['deletions']) + "}} \ {\color{red}{+" + str(data['additions']) + "}}$\n"
    return strings

# https://danmarshall.github.io/google-font-to-svg-path/
strings = '<p align="center"><img src="./images/Merge.svg" height="50px" style="max-width: 100%;"><img src="./images/git-merge.svg" width="60px" style="max-width: 100%;"></p>\n'
for item in keys:
    strings += gen_item(data[item], item)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
    readme = readme.replace("<!-- [**PR**] -->", strings)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
import vk_api
import time
from tinydb import TinyDB, where

db = TinyDB('./vkdb.json')
record_fetch_table = db.table('record_fetch_table')
records = db.table('records')
comments = db.table('comments') # shall we separate these two entities?

last_fetched = record_fetch_table.all()
last_fetched_id = -1
if len(last_fetched) > 0:
    last_fetched_id = last_fetched[0]['id']


vk_session = vk_api.VkApi(login, pwd)
vk_session.authorization()
vk = vk_session.get_api()

fetched_count = 0
found_last_fetched = False
new_fetched_id = -1

print('fetch')

while fetched_count < 100 and not found_last_fetched:
    print('+')
    objects= vk.wall.get(owner_id='-68471405', count=20, offset=fetched_count)
    fetched_count += 20
    print(type(objects['items']))
    for post in objects['items']:
        if new_fetched_id == -1:
            new_fetched_id = post['id']
        if post['id'] == last_fetched_id and not found_last_fetched:
            found_last_fetched = True
        else:
            records.insert(post)

print('updating recs')
record_fetch_table.update({'id': new_fetched_id}, 1 == 1)
if last_fetched_id == -1:
    record_fetch_table.insert({'id': new_fetched_id})
            
print('done')

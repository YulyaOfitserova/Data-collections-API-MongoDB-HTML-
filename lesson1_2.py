# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Сайт https://www.flickr.com
# Фото из галереи Maldives

import requests
from pprint import pprint
import json

apikey = '03805ef**************'
galleryid = '189717202-72157719400635344'
doc_format = 'json'
no_json_callback = '1'
url = 'https://www.flickr.com/services/rest/?method=flickr.galleries.getPhotos'
params = {'api_key': apikey, 'gallery_id': galleryid, 'format': doc_format, 'nojsoncallback': no_json_callback}

response = requests.get(url, params=params)
j_data = response.json()
pprint(j_data)

with open('maldives.json', 'w') as f:
    json.dump(j_data, f)


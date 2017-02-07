import requests
import json
response=requests.post('http://tangshitao.51vip.biz:54123/UCS/',data=json.dumps({"password":"dasd","username":"dsadas","commend":"login"}))
print response.text

response=requests.post('http://tangshitao.51vip.biz:54123/UCS/',data=json.dumps({"token":"dasd","commend":"search_by_name","center":"dsad","placename":"dsads"}))
print response.text

response=requests.post('http://tangshitao.51vip.biz:54123/UCS/',data=json.dumps({"token":"dasd","commend":"search_bounding_box","xmin":1,"xmax":2,"ymin":3,"ymax":4,"placename":"dsads"}))
print response.text

response=requests.post('http://tangshitao.51vip.biz:54123/UCS/',data=json.dumps({"token":"dasd","commend":"search_coordinate","longtitude":2,"latitude":3}))
print response.text
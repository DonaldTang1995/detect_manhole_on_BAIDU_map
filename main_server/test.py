import requests,json
host="http://cs-linux:32134/UCS"
response=requests.post(host,data=json.dumps({"password":"dasd","username":"dsadas","command":"login"})) 

print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_by_name","center":"dsad","placename":"dsads"})) 
print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_bounding_box","xmin":1,"xmax":2,"ymin":3,"ymax":4,"placename":"dsads"})) 
print response.text 

response=requests.post(host,data=json.dumps({"token":"dasd","command":"search_coordinate","longtitude":2,"latitude":3})) 
print response.text

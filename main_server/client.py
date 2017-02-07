import requests
import urllib
import json
def sendImgUrls(address,image_urls):
	response=requests.post(address,data=json.dumps(image_urls))
	print response.text
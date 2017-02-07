import requests
import urllib
import json
def sendImgUrls(urls):
	response=requests.post('http://tangshitao.51vip.biz:54123/UCS/',data=json.dumps(urls))
	print response.text
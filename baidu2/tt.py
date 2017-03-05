# coding=utf-8
import json, requests, urllib2, httplib

placename="银行"
url = "http://api.map.baidu.com/place/v2/search?"+"query="+placename+"&bounds=39.915,116.404,39.975,116.414&output=json&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
print(url)
temp = urllib2.urlopen(url)
hjson = json.loads(temp.read())
places={placename:[]}
urls=[]
i=0
name = hjson["results"][i]["name"]
print name
longitude = hjson["results"][i]["location"]["lng"]
print longitude
latitude = hjson["results"][i]["location"]["lat"]
info = hjson["results"][i]["detail"]
print info

url1 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
url2 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=90"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
url3 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=180"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
url4 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=270"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
            
places=places[placename]+[{"name":name,"longitude":longitude,"latitude":latitude,"information":info}]
print places
urls=urls+[url1,url2,url3,url4]
from map_engine import map
from common import check_keys
import json, requests, urllib2, httplib,logging


class baidu_map(map):
    instance=None
    
    @staticmethod
    def getInstance():
        if baidu_map.instance==None:
            baidu_map.instance=baidu_map()
        return baidu_map.instance

    # data contains {"name":"...","max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def search_by_name(self,data): 
        temp=check_keys(data,['placename','max_long','min_long','max_lat','min_lat'])
        if temp!=None:
            return temp+ " not found"
       
        logging.info('begin running search_by_name')    
        placename=data['placename']
        max_long=data["max_long"]
        min_long=data["min_long"]
        max_lat=data["max_lat"]
        min_lat=data["min_lat"]
        
        #url = "http://api.map.baidu.com/geocoder/v2/"+'?'+"&address="+name+"&output=json&pois=0"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"       
        url = "http://api.map.baidu.com/place/v2/search?"+"query="+placename+"&bounds="+min_long+","+min_lat+","+max_long+","+max_lat+"&output=json&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        print(url)
        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        places=[]
        urls=[]

        for i in range(len(hjson["results"])):
            name = hjson["results"][i]["name"]
            longitude = hjson["results"][i]["location"]["lng"]
            latitude = hjson["results"][i]["location"]["lat"]
            info = hjson["results"][i]["detail"]

            url1 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
            url2 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=90"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
            url3 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=180"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
            url4 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+str(longitude)+","+str(latitude)+"&width=1000&height=512&fov=120&pitch=40"+"&heading=270"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
            
            places=places+[{"name":name,"longitude":longitude,"latitude":latitude,"information":info}]
            urls=urls+[url1,url2,url3,url4]
        return ({placename:places},urls)


    # data contains {"max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def search_bounding_box(self,data):  
        temp=check_keys(data,['max_long','min_long','max_lat','min_lat'])
        if temp!=None:
            return temp+ " not found"
       
        logging.info('begin running search_bounding_box')  
        max_long=data["max_long"]
        min_long=data["min_long"]
        max_lat=data["max_lat"]
        min_lat=data["min_lat"]
        url="http://www.openstreetmap.org/api/0.6/map?bbox="+min_long+"%2C"+min_lat+"%2C"+max_long+"%2C"+max_lat
        #print(url)
        urls=[]
        places=[]        

        try:
            temp = urllib2.urlopen(url)
            dom=temp.read()
            i=0
            while i+1:
                i=dom.find("lat=",i)
                latitude=dom[i+5:i+13]
                i=dom.find("lon=",i)
                longitude=dom[i+5:i+13]

                if "l" not in latitude:
                    url1 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
                    url2 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=90"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
                    url3 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=180"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
                    url4 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=270"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
                    
                    places=places+[{"longitude":longitude,"latitude":latitude}]
                    urls=urls+[url1,url2,url3,url4]            
        except urllib2.HTTPError,e:
            logging.info('This bounding box cannot be found on openstreetmap.org, please try other bounding box.')
        return ({"search_bounding_box":places},urls)


    # data contains {"longtitude":"...","latitude":"..."}
    # this funciton is not very accurate due to baidu api
    def search_coordinate(self,data):  
        temp=check_keys(data,['longitude', 'latitude'])
        if temp!=None:
            return temp+ " not found"

        logging.info('begin running search_coordinate')
        longitude=data['longitude']
        latitude=data['latitude']
        
        url = "http://api.map.baidu.com/geocoder/v2/"+'?'+"&location="+longitude+","+latitude+"&output=json&pois=1"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        print url
        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        address = hjson["result"]["formatted_address"]
        info = hjson["result"]["sematic_description"]

        url1 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        url2 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=90"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        url3 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=180"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        url4 = "http://api.map.baidu.com/panorama/v2"+ '?'+"&location="+longitude+","+latitude+"&width=1000&height=512&fov=120&pitch=40"+"&heading=270"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"

        return ({address:{"longitude":longitude,"latitude":latitude,"information":info}},
                [url1,url2,url3,url4])







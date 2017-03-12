from map_engine import map
from common import check_keys,check_float
import json, requests, urllib2, httplib,logging


class baidu_map(map):
    instance=None
    
    @staticmethod
    def getInstance():
        if baidu_map.instance==None:
            baidu_map.instance=baidu_map()
        return baidu_map.instance

    # data contains {"name":"...","max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def generate_image_urls(self,longitude,latitude):
        urls=[]
        for i in [0,90,180,270]:
            url="http://api.map.baidu.com/panorama/v2&location=%f,%f&width=1000&height=512&fov=120&pitch=40&heading=%d&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb1"%(longitude,latitude,i)
            urls.append({'long':longitude,'lat':latitude,'url':url})
        return urls
    
    def search_by_name(self,data): 
        temp=check_keys(data,['placename','max_long','min_long','max_lat','min_lat'])
        if temp!=None:
            return (temp+ " not found",[])
       
        logging.info('begin running search_by_name')    
        placename=data['placename']
        values=[check_float(data[i],-180,180) for i in ['max_long','min_long','max_lat','min_lat']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        max_long,min_long,max_lat,min_lat=values    
        
        #url = "http://api.map.baidu.com/geocoder/v2/"+'?'+"&address="+name+"&output=json&pois=0"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"       
        url = "http://api.map.baidu.com/place/v2/search?query=%s&bounds=%f,%f,%f,%f&output=json&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"%(placename,min_long,min_lat,max_long,max_lat)
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

            
            places=places+[{"name":name,"longitude":longitude,"latitude":latitude,"information":info}]
            urls=urls+self.generate_image_urls(longtitude,latitude)

        return ({placename:places},urls)


    # data contains {"max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def search_bounding_box(self,data):  
        temp=check_keys(data,['max_long','min_long','max_lat','min_lat'])
        
        if temp!=None:
            return ({temp+ " not found"},[])
        logging.info('begin running search_bounding_box')  
        values=[check_float(data[i],-180,180) for i in ['max_long','min_long','max_lat','min_lat']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        max_long,min_long,max_lat,min_lat=values    
        url="http://www.openstreetmap.org/api/0.6/map?bbox={},{},{},{}".format(min_long,min_lat,max_long,max_lat)
        #print(url)
        urls=[]
        places=[]        
        try:
            temp = urllib2.urlopen(url)
            dom=temp.read()
            i=0
            import re
            pattern1=re.compile('lat="[0-9]+.[0-9]+" lon="[0-9]+.[0-9]+"')
            pattern2=re.compile('[0-9]+.[0-9]+')
            
            for string in pattern1.findall(dom):
                print string 
                latitude,longitude=[float(i) for i in pattern2.findall(string)] 
                urls=urls+self.generate_image_urls(longitude,latitude)            
        
        except urllib2.HTTPError,e:
            logging.info('This bounding box cannot be found on openstreetmap.org, please try other bounding box.')
        return urls


    # data contains {"longtitude":"...","latitude":"..."}
    # this funciton is not very accurate due to baidu api
    def search_coordinate(self,data):  
        temp=check_keys(data,['longitude', 'latitude'])
        if temp!=None:
            return ({temp+ " not found"},[])

        logging.info('begin running search_coordinate')
        longitude=data['longitude']
        latitude=data['latitude']
        
        url = "http://api.map.baidu.com/geocoder/v2/"+'?'+"&location="+longitude+","+latitude+"&output=json&pois=1"+"&ak=CkMdH2rDm1ypzW7ODG7hU6rGAXRr4nYb"
        print url
        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        address = hjson["result"]["formatted_address"]
        info = hjson["result"]["sematic_description"]


        return ({address:{"longitude":longitude,"latitude":latitude,"information":info}},
                self.generate_image_urls(longitude,latitude))







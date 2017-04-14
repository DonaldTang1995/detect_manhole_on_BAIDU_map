from map_engine import map
import googlemaps
from googlemaps import client
import urllib2
import xml.etree.cElementTree as ET

yourkey = 'AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'
gmaps = googlemaps.Client(key=yourkey)

class google_map(map):
    instance=None

    @staticmethod
    def getInstance():
        if google_map.instance==None:
            google_map.instance=google_map()
        return google_map.instance
   
    # data contains {"name":"...","max_long":"...","min_long":"...","max_lat":"...","min_lat":"..."}
    def generate_image_urls(self,longitude,latitude):
        urls=[]
        for pitch,head in [(270,0),(300,0),(300,270),(300,90)]:
            url = 'https://maps.googleapis.com/maps/api/streetview?size=700x700&location={},{}&fov=120&pitch={}&heading={}&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'.format(longitude,latitude,pitch,head)
            urls.append({'long':longitude,'lat':latitude,'url':url})
        return urls

    def search_by_name(self,data): #need to add function for multiple images of same place, e.g. topshop
 
        address = data['name']
        geocode_result = gmaps.geocode(address)[0]
        geocode_result.keys()
        lat1=geocode_result['geometry']['location']['lat']
        lng1=geocode_result['geometry']['location']['lng']
        
        url=self.generate_image_urls(lng1,lat1)

        return [],url

<<<<<<< HEAD

    def search_by_name(self,data): #need to add function for multiple images of same place, e.g. topshop
        """search by the name and center. 
        find corresponding street view images
        return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])"""
        
        address = data
        geocode_result = gmaps.geocode(address)[0]
        geocode_result.keys()
        lat1=geocode_result['geometry']['location']['lat']
        lng1=geocode_result['geometry']['location']['lng']
        #Solve metadata later https://maps.googleapis.com/maps/api/streetview/metadata?parameters        
        imageURL ='http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + str(lat1) + ',' + str(lng1) + '&heading=90&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'
        print imageURL
        return ({'hotel':{"longtitude":str(lng1),"latitude":str(lat1),"information":["this is a good hotel"]}},
                [imageURL])

=======
>>>>>>> 6153991177fb57eaed64fe2a07aa0878d6dd672c

    def search_bounding_box(self,data):
        """if name is specified, search the name in the bounding box, find corresponding street view images 
           return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])
           if not, find all streetview images in the bounding box
           return (None,[image urls]"""

<<<<<<< HEAD
        #return ({'hotel':{"longtitude":12,"latitude":12,"information":["this is a good hotel"]}},
        #        ["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])
        """If no name, all images:"""

        #Input data currently string = -2.0846,52.0039,-2.0077,52.0342
        boundingBox = data
        #later look at using url parameters to only request lat and lon values
        url = 'http://www.overpass-api.de/api/map?bbox=' + boundingBox
        
=======
        """If no name, all images:"""
        temp=check_keys(data,['north','south','east','west'])
        if temp!=None:
            return ({temp+ " not found"},[])
        logging.info('begin running search_bounding_box')  
        values=[check_float(data[i],-180,180) for i in ['north','south','east','west']]
        for v in values:
            if v==None:
                return ("invalid value",[])
        north,south,east,west=values    
        url="http://www.overpass-api.de/api/map?bbox={},{},{},{}".format(north,south,east,west)
>>>>>>> 6153991177fb57eaed64fe2a07aa0878d6dd672c
        #save and decode file
        s = urllib2.urlopen(url)
        
        #parse xml for lat and lng values
        tree = ET.parse(s)
        root = tree.getroot()
        allnodes=root.findall('node')
<<<<<<< HEAD
        listURL = []
        
        for node in allnodes:
            lat=node.get('lat')
            lon=node.get('lon')
            listURL.append('http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + str(lat) + ',' + str(lon) + '&heading=90&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY')
            print lat,lon

        """add camera facing algorithm here"""
        
        return (None,[listURL])

    def search_coordinate(self,data):

        """find information of the place and the corresponding street view
        return (dict{place name:information},image url)"""

        latLng = data
        imageURL ='http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + latLng +'&heading=90&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'
        return ({'hotel':["this is a good hotel"]},
                [imageURL])

    def search_by_street(self,data):

        """find information of the place and the corresponding street view
        return (dict{place name:information},image url)"""
        latLng = data

        imageURL ='http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + latLng +'&heading=90&key=AIzaSyAoaOH-XDMVKlm8KJoCXDLR8Twkz0rVkcY'
        return ({'hotel':["this is a good hotel"]},
                ["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])

=======
        urls=[]

        for node in allnodes:
            lat=node.get('lat')
            lon=node.get('lon')
            urls=urls+self.generate_image_urls(lon,lat)
            print lat, lon

        """add camera facing algorithm here"""

        return [],urls

    def search_coordinate(self,data):

        urls=[]
        for longitude,latitude in data:
            urls=urls+self.generate_image_urls(longitude,latitude)

        return [],urls

    def search_by_street(self,data):

        urls=[]
        for longitude,latitude in data:
            urls=urls+self.generate_image_urls(longitude,latitude)

        return [],urls
>>>>>>> 6153991177fb57eaed64fe2a07aa0878d6dd672c

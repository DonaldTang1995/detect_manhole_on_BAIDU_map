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


    def search_bounding_box(self,data):
        """if name is specified, search the name in the bounding box, find corresponding street view images 
           return (dict{place name:{"longtitude":longtitude,"latitude":latitude,"information":information}},[image urls])
           if not, find all streetview images in the bounding box
           return (None,[image urls]"""

        #return ({'hotel':{"longtitude":12,"latitude":12,"information":["this is a good hotel"]}},
        #        ["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])
        """If no name, all images:"""

        #Input data currently string = -2.0846,52.0039,-2.0077,52.0342
        boundingBox = data
        #later look at using url parameters to only request lat and lon values
        url = 'http://www.overpass-api.de/api/map?bbox=' + boundingBox
        
        #save and decode file
        s = urllib2.urlopen(url)
        
        #parse xml for lat and lng values
        tree = ET.parse(s)
        root = tree.getroot()
        allnodes=root.findall('node')
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


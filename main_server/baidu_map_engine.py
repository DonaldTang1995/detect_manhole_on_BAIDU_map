from map_engine import map
class baidu_map(map):
	instance=None

	@staticmethod
	def getInstance():
		if baidu_map.instance==None:
			baidu_map.instance=baidu_map()
		return baidu_map.instance

	def search_by_name(self,name,center): #not implement
		return ({'hotel':(12,12,["this is a good hotel"])},
			["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])

	def search_bounding_box(self,xmin,ymin,xmax,ymax,name):
		return ({'hotel':(12,12,["this is a good hotel"])},
			["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])

	def search_coordinate(self,longtitude,latitude):
		return (('hotel',["this is a good hotel"]),
			"http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg")

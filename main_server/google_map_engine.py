from map_engine import map
class google_map(map):
	instance=None

	@staticmethod
	def getInstance():
		if google_map.instance==None:
			google_map.instance=google_map()
		return google_map.instance

	def search_by_name(self,data): #not implement
		return ({'hotel':(12,12,["this is a good hotel"])},
			["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])

	def search_bounding_box(self,data):
		return ({'hotel':(12,12,["this is a good hotel"])},
			["http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg"])

	def search_coordinate(self,data):
		return (('hotel',["this is a good hotel"]),
			"http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg")

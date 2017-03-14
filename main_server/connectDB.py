import MySQLdb
class database():
    instance=None
    def __init__(self):
        pass 
    @staticmethod
    def getInstance():
        if database.instance==None:
            database.instance=database()
        return database.instance
    def save_image_url(self,token,time,longtitude,latitude,url): #not implement
        pass


    def get_image_infos(self,token,time,limit):
        return [{'long':121.55798,'lat':29.877452,'url':'http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg'},
   {'long':121.55798,'lat':29.877452,'url': 'http://n1.itc.cn/img8/wb/recom/2016/08/03/147021514873965284.JPEG'}]

    def save_xml_filename(self,token,time,filename): #not implement
        pass

    def remove_image_infos(self,token,time,image_infos):
        pass


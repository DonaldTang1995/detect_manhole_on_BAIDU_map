import MySQLdb,logging
from config import conf
class database():
    instance=None
    def __init__(self):
        self.conn=None
        self.curs=None
        self.connect()

    @staticmethod
    def getInstance():
        if database.instance==None:
            database.instance=database()
        return database.instance

    def connect(self):
        if self.conn!=None:
            return
        try:
            self.conn= MySQLdb.connect(
                        host=conf.HOST,
                        port=conf.PORT,
                        user=conf.USERNAME,
                        passwd=conf.PASSWORD,
                        db =conf.DATABASE
                        )
            self.curs=self.conn.cursor()
        except MySQLdb.Error as err:
            print err
            logging.error('{}'.format(err))

    def save_image_url(self,token,time,longitude,latitude,url): #not implement
        self.connect()
        sql='INSERT INTO image_info VALUES("{}",{},{},{},"{}");'.format(token,time,longitude,latitude,url)
        try:
            self.curs.execute(sql)
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))
            
    def get_image_infos(self,token,time,limit):
        return [{'long':121.55798,'lat':29.877452,'url':'http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg'},
   {'long':121.55798,'lat':29.877452,'url': 'http://n1.itc.cn/img8/wb/recom/2016/08/03/147021514873965284.JPEG'}]

    def save_xml_filename(self,token,time,filename): #not implement
        pass

    def remove_image_infos(self,token,time,image_infos):
        pass


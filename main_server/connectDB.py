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
    
    def create_account(self,username,password_md5):
        self.connect()
        sql1='SELECT * FROM account WHERE username="{}"'.format(username)
        sql2='INSERT INTO account VALUES("{}","{}")'.format(username,password_md5)
   
        try: 
            self.curs.execute(sql1)
            if len(self.curs.fetchall())!=0:
                return 'username already exists'
            self.curs.execute(sql2)
            return "Signup successfully"
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))
            return 'Fail to signup'
        
    def authenticate_account(self,username,password_md5):
        self.connect()
        sql='SELECT * FROM account WHERE username="{}" and password_md5="{}"'.format(username,password_md5)
        try:
            self.curs.execute(sql)
            if len(self.curs.fetchall())!=0:
                return True
            else:
                return False
        except MySQLdb.Error,e:
           try:
               logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
           except IndexError:
               logging.error("Mysql error {}".format(str(e)))
           return 'Fail to signup'
        
         
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
        self.connect()
        sql='SELECT longitude,latitude,url FROM image_info WHERE token="{}" and time={} LIMIT {}'.format(token,time,limit)
        results=[]
        try:
            self.curs.execute(sql)
            res=self.curs.fetchall()
            for row in res:
                results.append({'long':float(row[0]),'lat':float(row[1]),'urk':row[2]})
        except MySQLdb.Error, e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))

        return results
         
        return [{'long':121.55798,'lat':29.877452,'url':'http://pic.58pic.com/58pic/13/30/91/06u58PICHDR_1024.jpg'},
   {'long':121.55798,'lat':29.877452,'url': 'http://n1.itc.cn/img8/wb/recom/2016/08/03/147021514873965284.JPEG'}]

    def remove_image_infos(self,token,time,image_infos):
        sql='DELETE FROM image_info where token="{}" and time = "{}" and longitude = "{}" and latitude = "{}" and url ="{}"'
        try:
            for image_info in image_infos:
                latitude,longitude,url=image_info.items()
                self.curs.execute(sql.format(token,time,longitude,latitude,url))
        except MySQLdb.Error,e:
            try:
                logging.error("Mysql error [{}]:{}".format(e.args[0],e.args[1]))
            except IndexError:
                logging.error("Mysql error {}".format(str(e)))


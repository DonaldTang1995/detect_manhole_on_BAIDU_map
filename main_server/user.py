from config import conf
from google_map_engine import google_map
from baidu_map_engine import baidu_map
from connectDB import save_image_url,get_image_infos,save_xml_filename,remove_image_infos 
from manage_cache import search_xml_in_cache, save_xml_to_cache
from common import check_keys
import json,logging,requests,xml.etree.ElementTree,hashlib,Queue,threading,os
class user:
    def __init__(self,token,map_engine):
        self.token=token
        self.change_map_engine(map_engine)
        self.image_xml=[] #list to put results of image anaylsis
        self.search_time=0
        self.annotation_path=os.path.join(conf.CACHE,conf.ANNOTATION)
        self.functions={'change_map_engine':self.change_map_engine,'search_by_name':self.search_by_name,'search_bounding_box':self.search_bounding_box,'search_coordinate':self.search_coordinate,'image_analysis':self.image_analysis}

    def change_map_engine(self,map_engine):
        if map_engine==conf.GOOGLE:
            self.map_engine=google_map.getInstance() #map_engine to use
        elif map_engine==conf.BAIDU:
            self.map_engine=baidu_map.getInstance()

    def save_image_urls_to_database(self,image_infos):
        logging.info("begin putting image urls to database")

        for image in image_infos:
            logging.info("save "+self.token+" : "+image['url']+" to database" )
            save_image_url(self.token,self.search_time,image['long'],image['lat'],image['url'])

    def search_by_name(self,data):
        """search places by name and center"""
        logging.info('prepare to run search_by_name')

        results,image_infos=self.map_engine.search_by_name(data)
        self.save_image_urls_to_database(image_infos)
        if len(image_infos)!=0:
            results=json.dumps((results),len(image_infos))
        self.search_time+=1
        return results

    def search_bounding_box(self,data):
        """search places in a boudning box """
        logging.info("prepare to run search_bounding_box")
        results,image_infos=self.map_engine.search_bounding_box(data)
        self.save_image_urls_to_database(image_infos)
        self.search_time+=1
        return json.dumps(len(image_infos))

    def search_coordinate(self,data):
        """search place of the coordinate"""
        logging.info("parpare to run search_coordinate")

        results,image_urls=self.map_engine.search_coordinate(data)
        self.save_image_urls_to_database(image_urls)
        if len(image_urls)!=0:
            results=json.dumps((results),len(image_urls))
        self.search_time+=1
        return results

    def send_image_urls(self,address,images):
        """send image url and its md5 to address to run image ananlysis"""
        self.image_xml=search_xml_in_cache(images)

        for md5,url,_ in self.image_xml:
            images.remove((md5,url))
    
        for md5,url in images:
            logging.info('send '+url+' to '+address)
        if len(images)>0:
            response=requests.post(address,data=json.dumps(images),timeout=0.1)
        logging.info('receive results from '+address)
        
        for msg in json.loads(response.text):
            md5,url,xml=msg[0],msg[1],msg[2]
            self.image_xml.append((url,xml))
            save_xml_to_cache(md5,xml)

    def image_analysis(self,data):
        """take image url from database and run image analysis"""
        logging.info('run image analysis')

        temp=check_keys(data,['limit'])
        if temp!=None:
            return temp+" not found"
        limit=int(data['limit'])

        image_infos=get_image_infos(self.token,self.seach_time-1,limit)
        logging.info('generate md5 according to image url')
        images=[]
        md5_to_place={}
        for image in image_infos:
            md5=hashlib.sha224(image['url']).hexdigest()
            images.append((md5,image['url']))
            md5_to_place[md5]=(image['long'],image['lat'])

        total_size=len(images)
        group_size=total_size/conf.NUMBER_OF_IMAGE_ANALYSIS_SERVER
        thread_pool=[]
        
        for i in range(conf.NUMBER_OF_IMAGE_ANALYSIS_SERVER):
            t=threading.Thread(target=self.send_image_urls,args=(conf.ADDRESSES[i],
                images[i*group_size:min((i+1)*group_size,total_size)]))
            thread_pool.append(t)
            t.start()

        for thread in thread_pool:
            thread.join()
        logging.info('all results are returned')
        results=[]
        for md5,url,xml in self.image_xml:
            longtitude,latitude=md5_to_place[md5]
            results.append({'long':longtitude,'lat':latitude,'url':url,'xml':xml})
        remove_image_infos(self.token,self.search_time,image_infos)
        return json.dumps(results)

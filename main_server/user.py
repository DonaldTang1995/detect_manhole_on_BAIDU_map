from config import conf
from google_map_engine import google_map
from baidu_map_engine import baidu_map
from connectDB import save_image_url
import json,logging
class user:
    def __init__(self,token,map_engine):
        self.token=token
        self.change_map_engine(map_engine)

    def change_map_engine(self,map_engine):
        if map_engine==conf.GOOGLE:
            self.map_engine=google_map.getInstance() #map_engine to use
        elif map_engine==conf.BAIDU:
            self.map_engine=baidu_map.getInstance()

    def save_image_urls_to_database(self,image_urls):
        logging.info("begin putting image urls to database")
        for url in image_urls:
            logging.info("save "+self.token+" : "+url+" to database" )
            save_image_url(self.token,url)

    def search_by_name(self,place_name,center):
        """search places by name and center"""
        logging.info("search "+place_name+" of center: "+center)

        results,image_urls=self.map_engine.search_by_name(place_name,center)
        self.save_image_urls_to_database(image_urls)
        return json.dumps(results)

    def search_bounding_box(self,xmin,ymin,xmax,ymax,place_name):
        """search places in a boudning box """
        logging.info("search "+place_name+" in (xmin:%f ymin:%f xmax:%f ymax:%f)"%(xmin,ymin,xmax,ymax))

        results,image_urls=self.map_engine.search_bounding_box(xmin,ymin,xmax,ymax,place_name)
        self.save_image_urls_to_database(image_urls)
        return json.dumps(results)

    def search_coordinate(self,longtitude,latitude):
        """search place of the coordinate"""
        logging.info("search (longtitude:%f latitude:%f)"%(longtitude,latitude))

        results,image_url=self.map_engine.search_coordinate(longtitude,latitude)
        self.save_image_urls_to_database([image_url])
        return json.dumps(results)

    def image_analysis(self):
        pass


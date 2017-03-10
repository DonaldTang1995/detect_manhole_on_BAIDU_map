import logging,os
from config import conf

def search_xml_in_cache(images):

    image_xml=[]
    for md5,url in images:
        xml_path=os.path.join(conf.CACHE,conf.ANNOTATION,md5+'.xml')
        if os.path.isfile(xml_path):
            logging.info('found '+md5+' in cache')
            with open(xml_path,'r') as f:
                image_xml.append((md5,url,f.readlines()))
        else:
            logging.info(md5+' not found in cache')

    #for md5,url,xml in image_xml:
    #    images.remove((md5,url))

    return image_xml

def save_xml_to_cache(md5,xml):
    logging.info('save '+md5+' to cache')
    path=os.path.join(conf.CACHE,conf.ANNOTATION,md5+'.xml')
    with open(path,'w') as f:
        f.write(xml)

import web
import urllib
import urllib2
import Queue
import json
import threading
import load_net
from config import conf
urls = (
    '/detect/(.*)', 'detect'
)



class detect:
    net=None
    def __init__(self):
        if detect.net==None:
            detect.net=load_net.load()

    def delete_images(self):
        import os
        for file in os.listdir(conf.IMAGES_DIR):
            image_path=os.path.join(conf.IMAGES_DIR,file)
            os.remove(image_path)

    def download_image(self,image_url,md5):
        print "try downloading"
        try: 
            urllib2.urlopen(image_url)

            saved_name=md5+'.jpg'
            import os
            saved_path=os.path.join(conf.IMAGES_DIR,saved_name)
            print "downloading "+image_url
            urllib.urlretrieve (image_url, saved_path)
            self.waiting_for_analysis.put(saved_name)

            self.image_analysis_lock.release()

        except Exception:
            self.unable_to_download.put(image_url)

        self.mutex.acquire()
        self.downloading_tried+=1
        if self.downloading_tried==self.images_number:
            self.image_analysis_semaphore.release()
        self.mutex.release()

        self.number_of_threads_downloading_images_semaphore.release()

    def run_image_analysis(self,gpu_id):
        from generate_bounding_boxes import detectImageByName
        while self.downloading_tried<self.images_number or self.waiting_for_analysis.qsize()!=0:
            if self.waiting_for_analysis.qsize()==0:
                self.image_analysis_semaphore.acquire()
            else:
                image_name=self.waiting_for_analysis.get()
                print "detect "+image_name
                self.successfully_detected.put((image_name,detectImageByName(detect.net,image_name,gpu_id)))

        self.number_of_gpus_semaphore.release()

    def POST(self,name):
        self.waiting_for_analysis=Queue.Queue()
        self.unable_to_download=Queue.Queue()
        self.successfully_detected=Queue.Queue()
        self.image_analysis_semaphore=threading.Semaphore(0)
        self.number_of_threads_downloading_images_semaphore=threading.Semaphore(conf.NUMBER_OF_THREADS_TO_DOWNLOAD_IMAGES)
        self.number_of_gpus_semaphore=threading.Semaphore(conf.NUMBER_OF_GPUS)
        self.mutex=threading.Lock()
        self.downloading_tried=0

        images=json.loads(web.data())
        self.images_number=len(images)


        for i in range(conf.NUMBER_OF_GPUS):
            self.number_of_gpus_semaphore.acquire()
            threading.Thread(target=self.run_image_analysis,args=(i,)).start()

        for image_url,md5 in images.items():
            self.number_of_threads_downloading_images_semaphore.acquire()
            threading.Thread(target=self.download_image,args=(image_url,md5)).start()

        for i in range(conf.NUMBER_OF_GPUS):
            self.number_of_gpus_semaphore.acquire()

        for i in range(conf.NUMBER_OF_THREADS_TO_DOWNLOAD_IMAGES):
            self.number_of_threads_downloading_images_semaphore.acquire()


        result={}
        while self.successfully_detected.qsize()!=0:
            image_name,xml=self.successfully_detected.get()
            result[image_name]=xml

        threading.Thread(target=self.delete_images).start()

        return json.dumps(result)


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
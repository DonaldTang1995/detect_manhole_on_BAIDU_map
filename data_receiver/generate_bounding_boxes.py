import __init__
import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
from write_annotation import generate_image_xml

CLASSES = ('__background__', # always index 0
                 'bicycle', 'bus', 'car', 'cat', 'dog', 'horse',
                 'motorbike', 'person', 'pottedplant',
                 'train', 'manhole_cover')

def detect(img,net_name="resnet50_rfcn_class_12_scales_3",mode='gpu',gpu_id=0):

    manhole_net_path="manhole_net"
    model_path="final_models"
    prototxt_path="final_prototxt"


    cfg.TEST.HAS_RPN=True

    prototxt_name=net_name+'.prototxt'
    model_name=net_name+'.caffemodel'
    prototxt=os.path.join(manhole_net_path,prototxt_path,prototxt_name)
    model=os.path.join(manhole_net_path,model_path,model_name)

    if not os.path.isfile(model):
        raise IOError(('Model {:s} not found.\n').format(model))

    if not os.path.isfile(prototxt):
        raise IOError(('Prototxt {:s} not found.\n').format(prototxt))

    #set mode
    if mode=="gpu":
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
        cfg.GPU_ID = gpu_id
    elif mode=="cpu":
        caffe.set_mode_cpu()

    net = caffe.Net(prototxt, model, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(model)

    return im_detect(net, img)
    
def detectImageByName(img_name):
    images_dir='images'
    image_path=os.path.join(images_dir,img_name)
    if not os.path.isfile(image_path):
        raise IOError(('Image {:s} not found.\n').format(model))
    img=cv2.imread(image_path)
    scores,boxes=detect(img)

    CONF_THRESH = 0.8
    NMS_THRESH = 0.3

    bounding_box={}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4:8]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        bounding_box[cls]=dets[dets[:,-1]>CONF_THRESH]

    generate_image_xml(img_name,img.shape,bounding_box)


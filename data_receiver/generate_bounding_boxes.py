import __init__
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from fast_rcnn.config import cfg
import numpy as np
import caffe, os, sys, cv2
from write_annotation import generate_image_xml
from config import conf

CLASSES = conf.CLASSES

def detectImageByName(net,img_name,gpu_id=0):
    images_dir='images'
    image_path=os.path.join(images_dir,img_name)
    if not os.path.isfile(image_path):
        raise IOError(('Image {:s} not found.\n').format(model))

    if conf.mode=='cpu':
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(gpu_id)
        cfg.GPU_ID = gpu_id

    img=cv2.imread(image_path)
    scores,boxes=im_detect(net,img)

    SOFTMAX_THRESH = conf.SOFTMAX_THRESH
    NMS_THRESH = conf.NMS_THRESH

    bounding_box={}
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4:8]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        bounding_box[cls]=dets[dets[:,-1]>SOFTMAX_THRESH]

    generate_image_xml(img_name,img.shape,bounding_box)


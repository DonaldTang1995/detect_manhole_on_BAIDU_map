import __init__
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import numpy as np
import caffe, os, sys, cv2
from write_annotation import generate_image_xml

CLASSES = ('__background__', # always index 0
                 'bicycle', 'bus', 'car', 'cat', 'dog', 'horse',
                 'motorbike', 'person', 'pottedplant',
                 'train', 'manhole_cover')

def detectImageByName(net,img_name):
    images_dir='images'
    image_path=os.path.join(images_dir,img_name)
    if not os.path.isfile(image_path):
        raise IOError(('Image {:s} not found.\n').format(model))
    img=cv2.imread(image_path)
    scores,boxes=detect(net,img)

    CONF_THRESH = 0.7
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


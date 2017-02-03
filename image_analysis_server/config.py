from easydict import EasyDict as edict
__C=edict()

conf=__C
#classes that can be detected
__C.CLASSES = ('__background__', # always index 0
                 'bicycle', 'bus', 'car', 'cat', 'dog', 'horse',
                 'motorbike', 'person', 'pottedplant',
                 'train', 'manhole_cover')

#name of the net
__C.net_name="resnet50_rfcn_class_12_scales_3"

#use gpu or cpu to run
__C.mode='gpu'

#confidence greater than this thresh will be detected
__C.SOFTMAX_THRESH=0.7

#non maximum suppression 
__C.NMS_THRESH=0.3


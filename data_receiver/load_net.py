import __init__
import os
import caffe
from fast_rcnn.config import cfg

def load_net(net_name="resnet50_rfcn_class_12_scales_3",mode='gpu',gpu_id=0):

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

    return caffe.Net(prototxt, model, caffe.TEST)
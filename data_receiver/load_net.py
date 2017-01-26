import __init__
import os
import caffe
from config import conf
def load():
    net_name=conf.net_name

    manhole_net_path="manhole_net"
    model_path="final_models"
    prototxt_path="final_prototxt"

    prototxt_name=net_name+'.prototxt'
    model_name=net_name+'.caffemodel'
    prototxt=os.path.join(manhole_net_path,prototxt_path,prototxt_name)
    model=os.path.join(manhole_net_path,model_path,model_name)

    if not os.path.isfile(model):
        raise IOError(('Model {:s} not found.\n').format(model))

    if not os.path.isfile(prototxt):
        raise IOError(('Prototxt {:s} not found.\n').format(prototxt))


    return caffe.Net(prototxt, model, caffe.TEST)

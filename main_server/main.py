import web
import logging
import __init__
import sys

from ucs_server import UCS
from index import index
from baidu import baidu
urls = (
    '/UCS', 'UCS',
    '/index','index',
    '/baidu','baidu',

)
if __name__ == "__main__": 
    reload(sys)
    sys.setdefaultencoding('utf8')
    web.config.debug=False
    logging.info("UCS starting...")
    app = web.application(urls, globals())
    app.run()

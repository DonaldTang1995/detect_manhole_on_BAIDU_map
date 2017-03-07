import web
import logging
import __init__

from ucs_server import UCS
from index import index
from baidu import baidu
from baidu2 import baidu
urls = (
    '/UCS', 'UCS',
    '/index','index',
    '/baidu','baidu',
    '/sadas','baidu2',

)
if __name__ == "__main__": 
    web.config.debug=False
    logging.info("UCS starting...")
    app = web.application(urls, globals())
    app.run()

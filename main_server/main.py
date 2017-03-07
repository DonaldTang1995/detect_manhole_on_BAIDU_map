import web
import logging
import __init__

from ucs_server import UCS
from index import index
from baidu import baidu
urls = (
    '/UCS', 'UCS',
    '/index','index',
    '/baidu','baidu',

)
if __name__ == "__main__": 
    web.config.debug=False
    logging.info("UCS starting...")
    app = web.application(urls, globals())
    app.run()

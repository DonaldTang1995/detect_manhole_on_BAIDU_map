import web
import logging
import __init__
from ucs_server import UCS

urls = (
    '/(.*)', 'UCS'
)
if __name__ == "__main__": 
    logging.info("UCS starting...")
    app = web.application(urls, globals())
    app.run()
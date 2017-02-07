import web
import logging
import logging.config
import detect

urls = (
    '/detect/(.*)', 'detect.detect'
)
if __name__ == "__main__": 
    logging.info('Starting image analysis server...')
    app = web.application(urls, globals())
    app.run()
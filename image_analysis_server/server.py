import web
from detect
urls = (
    '/detect/(.*)', 'detect.detect'
)

if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
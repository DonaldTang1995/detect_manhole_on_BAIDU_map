import web
render=web.template.render('/home/team201603/ucs/client/')

class baidu:
    def GET(self):
        return render.baidu()

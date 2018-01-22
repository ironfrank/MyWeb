# -*- coding:utf-8 -*-
import os
import sys
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
from dbbox import *

reload(sys)
sys.setdefaultencoding('utf-8')


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

db = DB('film', '127.0.0.1')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/search', search_handler),
            (r'/test', AjaxHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
        )


class AjaxHandler(tornado.web.RequestHandler):

    def post(self):
        search_content = self.get_argument("message")
        rows = db.query_film_table(search_content)
        namelist = []
        for item,val in rows:
            if not item or not val:
                continue
            namelist.append({"name": item, "link": val})

        filmdict = {}
        filmdict['film'] = namelist
        encode_json = json.dumps(filmdict)
        self.write(encode_json)


class search_handler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)

    def get(self):
        keyword = self.get_argument('search_keyword')
        rows = {}
        if keyword:
            self.db = DB('film', '127.0.0.1')
            rows = self.db.query_film_table(keyword)
            self.render(
                "search.html", films=rows
            )
        else:
            self.redirect('/')
            # self.render(
            #     "index.html",
            # )



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    # options.port = 8888
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

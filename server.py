#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import define, options
from dhash import main as get_dhashes

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("views/index.html")

  def post(self):
    data = tornado.escape.json_decode(self.request.body)
    paths = data.get('paths')
    dhashes = get_dhashes(paths)

    self.write({"result": dhashes})

if __name__ == "__main__":
  app = tornado.web.Application([
    (r"/", MainHandler)
  ])

  app.listen(options.port)

  print("Listening port %d" % options.port)

  tornado.ioloop.IOLoop.instance().start()

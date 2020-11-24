#!/usr/bin/env python3
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.netutil
import wsgi
import argparse
import socket

HOST = '0.0.0.0'
PORT = 8000
WORKERS = 0


def host_port(s):
    global HOST, PORT

    if s.find(':') is not -1:
        HOST, PORT = s.split(':')
    else:
        PORT = s


def main():

    # path to your settings module
    sockets = tornado.netutil.bind_sockets(PORT, address=HOST)
    tornado.process.fork_processes(WORKERS)
    container = tornado.wsgi.WSGIContainer(wsgi.application)

    from django.conf import settings

    tornado_app = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings.STATIC_ROOT}),
        (r'.*', tornado.web.FallbackHandler, dict(fallback=container)),
    ])

    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.add_sockets(sockets)

    print("Startig web server in %s:%s" % (HOST, PORT))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'portaddr',
        help="Optional port number, or ipaddr:port",
        metavar="portaddr",
        type=host_port
    )
    parser.add_argument(
        '-w', '--workers',
        help="How many workers will be used for this server. (default: 0, autodetect)",
        metavar='N',
        type=int,
        default=0
    )

    args = parser.parse_args()

    try:
        socket.inet_aton(HOST)
    except socket.error:
        parser.error("Invalid host %s" % (HOST,))

    if isinstance(PORT, str):
        if PORT.isdigit():
            PORT = int(PORT)
        else:
            parser.error("Invalid port %d" % (PORT,))

    WORKERS = args.workers
    main()
